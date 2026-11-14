"""本次 Windows TRELLIS.2 运行的兼容层；不修改共享 Python 安装。"""
import torch
import torch.nn.functional as F


def latent_view_weights(self, coords, views, front_axis='z', blend_temperature=2.0):
    """Shape latents have 16x fewer cells per axis than decoded geometry."""
    latent_resolution = self.resolution // 16
    xyz = (coords[:, 1:].float() + .5) / latent_resolution * 2 - 1
    directions = torch.tensor([self._VIEW_DIRS[front_axis][v] for v in views], device=coords.device, dtype=xyz.dtype)
    return torch.softmax((xyz @ directions.T) * blend_temperature, dim=1)


def segmented_sdpa(q, k, v, cu_q, cu_k, max_q, max_k, **kwargs):
    """按原始 batch 边界独立计算，避免 Triton 编译和全局二次方遮罩。"""
    qs, ks = cu_q.tolist(), cu_k.tolist()
    result = []
    for i in range(len(qs) - 1):
        query = q[qs[i]:qs[i + 1]].transpose(0, 1).unsqueeze(0)
        key = k[ks[i]:ks[i + 1]].transpose(0, 1).unsqueeze(0)
        value = v[ks[i]:ks[i + 1]].transpose(0, 1).unsqueeze(0)
        output = F.scaled_dot_product_attention(query, key, value)
        result.append(output.squeeze(0).transpose(0, 1))
    return torch.cat(result, dim=0)


def install():
    import sys
    import comfy_sparse_attn.varlen as varlen
    from comfy.ldm.modules.attention import attention_pytorch
    from flash_attn import flash_attn_varlen_func
    def verified_flash(q, k, v, cq, ck, mq, mk):
        original_dtype = q.dtype
        if original_dtype not in (torch.float16, torch.bfloat16):
            q, k, v = q.bfloat16(), k.bfloat16(), v.bfloat16()
        try:
            return flash_attn_varlen_func(q, k, v, cq, ck, mq, mk).to(original_dtype)
        except (AssertionError, RuntimeError):
            return segmented_sdpa(q, k, v, cq, ck, mq, mk).to(original_dtype)
    varlen._varlen_fn = verified_flash
    varlen._varlen_backend = 'flash_attn_verified'
    for name in ('comfy_sparse_attn.attention_sparse', 'comfy.attention_sparse'):
        if name in sys.modules:
            sys.modules[name].optimized_attention_for_device = lambda device: attention_pytorch
    # Node mesh/voxel coordinates are Z-up. Upstream multiview weights still
    # assume Y-up, blending front/back vertically through roof and foundation.
    from nodes.trellis2.samplers.flow_euler import FlowEulerMultiViewSampler
    FlowEulerMultiViewSampler._VIEW_DIRS['z'] = {
        'front': (0, -1, 0), 'back': (0, 1, 0),
        'right': (1, 0, 0), 'left': (-1, 0, 0),
        'top': (0, 0, 1), 'bottom': (0, 0, -1),
    }
    FlowEulerMultiViewSampler._compute_view_weights_sparse = latent_view_weights
    install_multiview_texturing()
    install_high_detail_remeshing()
    print('[dota287] runtime compatibility: verified FlashAttention varlen, PyTorch dense, Z-up view directions', file=sys.stderr, flush=True)


def install_high_detail_remeshing():
    """Enable a task-only 1024 remesh when the requested output is at least 3M faces."""
    import inspect,textwrap
    from nodes import nodes_unwrap
    cls=nodes_unwrap.Trellis2ProcessMesh
    if getattr(cls,'_dota291_detail_patch',False):return
    source=textwrap.dedent(inspect.getsource(cls.execute.__func__))
    needle='resolution = 512'
    if source.count(needle)!=1:raise RuntimeError('ProcessMesh implementation changed; inspect before applying detail override')
    source=source.replace(needle,'resolution = 1024 if target_face_count >= 3000000 else 512')
    namespace=dict(vars(nodes_unwrap));exec(compile(source,'<dota291_task_remesh>','exec'),namespace)
    cls.execute=namespace['execute'];cls._dota291_detail_patch=True
    print('[dota291] task-only remesh override installed: 1024 grid for >=3M-face remesh requests',flush=True)


def install_multiview_texturing():
    """Carry the same view evidence into the texture stage, within this worker."""
    from nodes import stages
    from nodes.trellis2.samplers import FlowEulerMultiViewGuidanceIntervalSampler
    original_multi=stages.run_multiview_shape_generation
    original_single=stages.run_shape_generation
    original_texture=stages._sample_tex_slat
    context={}
    def multi(*args,**kwargs):
        views=kwargs.get('view_conditionings',args[1] if len(args)>1 else None)
        context['views']={v:{k:t.detach().cpu().clone() if torch.is_tensor(t) else t for k,t in c.items()} for v,c in views.items()}
        return original_multi(*args,**kwargs)
    def single(*args,**kwargs):
        context.clear();return original_single(*args,**kwargs)
    def texture(cond,model_key,shape_slat,sampler_params,device,dtype):
        if not context.get('views'):return original_texture(cond,model_key,shape_slat,sampler_params,device,dtype)
        import torch.nn as nn
        import comfy.model_management
        comfy.model_management.throw_exception_if_processing_interrupted()
        resolution=512 if model_key.endswith('_512') else 1024
        key='cond_'+str(resolution)
        views={v:{'cond':c[key].to(device=device,dtype=dtype),'neg_cond':c['neg_cond'].to(device=device,dtype=dtype)} for v,c in context['views'].items()}
        cfg=stages._pipeline_config
        std=torch.tensor(cfg['shape_slat_normalization']['std'])[None].to(device=device,dtype=dtype)
        mean=torch.tensor(cfg['shape_slat_normalization']['mean'])[None].to(device=device,dtype=dtype)
        normalized=(shape_slat-mean)/std
        model=stages._load_model(model_key)
        channels=model.in_channels if isinstance(model,nn.Module) else model[0].in_channels
        noise=normalized.replace(feats=torch.randn(normalized.coords.shape[0],channels-normalized.feats.shape[1],device=device,dtype=dtype))
        params={**cfg['tex_slat_sampler']['params'],**sampler_params}
        sampler=FlowEulerMultiViewGuidanceIntervalSampler(sigma_min=1e-5,resolution=resolution)
        slat=sampler.sample(model,noise,concat_cond=normalized,conds=views,views=list(views),front_axis='z',blend_temperature=2.0,**params,verbose=True,tqdm_desc='Texture SLat (multi-view corrected latent scale)').samples
        stages._unload_model(model_key)
        std=torch.tensor(cfg['tex_slat_normalization']['std'])[None].to(device=device,dtype=dtype)
        mean=torch.tensor(cfg['tex_slat_normalization']['mean'])[None].to(device=device,dtype=dtype)
        return slat*std+mean
    stages.run_multiview_shape_generation=multi
    stages.run_shape_generation=single
    stages._sample_tex_slat=texture


if __name__ == '__main__':
    torch.manual_seed(287)
    q, k, v = torch.randn(7, 2, 8), torch.randn(9, 2, 8), torch.randn(9, 2, 8)
    cq, ck = torch.tensor([0, 3, 7]), torch.tensor([0, 5, 9])
    mask = torch.full((7, 9), float('-inf'))
    mask[:3, :5] = 0
    mask[3:, 5:] = 0
    expected = F.scaled_dot_product_attention(q.transpose(0, 1),
        k.transpose(0, 1), v.transpose(0, 1), attn_mask=mask).transpose(0, 1)
    actual = segmented_sdpa(q, k, v, cq, ck, 4, 5)
    torch.testing.assert_close(actual, expected)
    print('PASS: unequal packed sequences match block-diagonal attention; max error',
          (actual - expected).abs().max().item())

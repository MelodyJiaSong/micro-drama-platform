# assets_sync — `ai_videos/` 媒体的集中存储

媒体（视频/图片/音频/PDF）被 `.gitignore` 挡在版本库外，所以 git 本身回答不了
「这个 commit 对应哪些字节」。本工具把**字节**放进 Cloudflare R2（S3 兼容），把
**索引**放进 git：`ai_videos/assets.json` 记录 `路径 -> sha256`，像普通文件一样
可 diff、可 review、可回滚。

## 为什么不用 Git LFS

LFS 里文件仍被 git 追踪，只是内容换成指针——**每一版都永久留存**，删了也不回收。
短剧工作流一个 shot 会重渲十几版，LFS 会把十几版全留着；R2 是内容寻址覆盖，
只留当前引用的那一份。R2 出网流量免费，反复取回旧集不额外计费。

## 设计

- **内容寻址**：对象 key = `objects/{sha256[:2]}/{sha256}`。因此改名不产生传输
  （只是清单变了），两个内容相同的 take 只存一份，中文文件名也不会进 key。
- **git 是它所持有内容的唯一真相**：被 git 跟踪的文件（如 `0_原作资料/_refs/`
  的一手参考图）**不会**上传，避免同一份东西两个地方各存一份。
- **不同步的**：`_deleted/`（回收站，本来就在等着被清）、`previz/frames/`
  （由 `previz_config.toml` 重算得出）。
- **sha256 缓存**：`.assets_cache.json`（根目录，gitignored）按 (size, mtime_ns)
  缓存哈希，避免每次重算 6+ GB。删掉即可重建。

## 用法

```bash
python tools/assets_sync.py status            # 本地 vs 清单，无需凭据
python tools/assets_sync.py push --dry-run    # 看要传什么
python tools/assets_sync.py push              # 上传 + 重写清单
python tools/assets_sync.py pull              # 补齐本地缺失的文件
python tools/assets_sync.py prune             # 列出无人引用的远端对象
python tools/assets_sync.py prune --yes       # 真的删除（不可逆）
```

换机器 / 新 clone：`git pull` 拿到清单 → `python tools/assets_sync.py pull`。

## 凭据

复制 `tools/assets/.env.example` 到仓库根目录的 `.env`（已 gitignored）并填写：

- `R2_ENDPOINT` —— 控制台里的 "endpoint for S3 clients"（`https://<account-id>.r2.cloudflarestorage.com`）。
  也接受 `R2_ACCOUNT_ID` 二选一。
- `R2_ACCESS_KEY_ID` / `R2_SECRET_ACCESS_KEY` —— Manage R2 API Tokens → Create API Token，
  权限选 **Object Read & Write** 并**限定到这一个 bucket**。
- `R2_BUCKET` —— bucket 名。注意：限定到单 bucket 的 token **无权 ListBuckets**，
  所以这个名字必须手填，工具没法自己发现。

凭据只从环境读取，永远不会写进清单。

## 依赖

`pip install -r tools/assets/requirements.txt`（boto3）。

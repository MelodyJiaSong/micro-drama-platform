import { useEffect, useRef } from "react";
import { Link } from "react-router-dom";
import { mediaUrl } from "../api";
import { IMAGE_STATUS, sharedFile, sharedFileHref, type SharedAsset } from "../lib/sharedAssets";

export function SharedAssetPreview({ asset, assets, libraryRoot, onClose, onSelect }: {
  asset: SharedAsset; assets: SharedAsset[]; libraryRoot: string; onClose: () => void; onSelect: (id: string) => void;
}): JSX.Element {
  const panel = useRef<HTMLElement>(null);
  useEffect(() => { panel.current?.scrollIntoView?.({ block: "start" }); }, [asset.id]);
  const adoption = asset.adoption ? { locked: "锁定（跨剧一致）", default: "默认（采用剧可改）", optional: `可选模块${asset.module ? `：${asset.module}` : ""}` }[asset.adoption] ?? asset.adoption : null;
  const details = Object.entries(asset.details ?? {}).map(([label, value]) => [label, Array.isArray(value) ? value.join("；") : value]);
  const fields = [
    ["用途", asset.function], ["触发", asset.activation.trigger], ["使用条件", asset.activation.requirement],
    ["代价与限制", asset.cost_limit], ["克制与失效", asset.counter_failure], ["外观识别", asset.visual_signature],
    ["品阶", asset.grade ?? "不适用"], ["采用数值", asset.parameters],
  ];
  return <article ref={panel} className="shared-asset-panel" aria-label={`${asset.id} ${asset.name}`}>
    <header><div><small>{asset.category} · v{asset.version}{adoption ? ` · ${adoption}` : ""}</small><h2>{asset.id} · {asset.name}{asset.name_en ? <span className="shared-name-en"> {asset.name_en}</span> : null}</h2></div>
      <button type="button" onClick={onClose} aria-label="返回资产列表">← 返回列表</button></header>
    <p className="shared-status">{IMAGE_STATUS[asset.image.status] ?? asset.image.status}</p>
    <div className="shared-asset-detail">
      <div>{asset.image.sha256
        ? <a href={mediaUrl(sharedFile(libraryRoot, asset.image.anchor))} target="_blank" rel="noreferrer" title="打开原图"><img src={mediaUrl(sharedFile(libraryRoot, asset.image.anchor))} alt={asset.name} className="shared-asset-large" /></a>
        : <div className="shared-no-image">尚无图片，设定已建立</div>}
        <p><Link to={sharedFileHref(libraryRoot, asset.image.anchor.replace(/[^/]+$/, "card.md"))}>完整资产卡</Link>
          {" · "}<Link to={sharedFileHref(libraryRoot, asset.image.prompt)}>出图描述</Link></p>
        {asset.image.review_notes?.length ? <section><h3>验收备注</h3><ul>{asset.image.review_notes.map((note, i) => <li key={i}>{note}</li>)}</ul></section> : null}
      </div>
      <div><dl>{asset.xianxia ? <div><dt>仙侠参照</dt><dd><strong>{asset.xianxia.concept}</strong>{asset.xianxia.note ? `：${asset.xianxia.note}` : ""}</dd></div> : null}
        {fields.map(([label, value]) => <div key={label}><dt>{label}</dt><dd>{value}</dd></div>)}
        {details.map(([label, value]) => <div key={label}><dt>{label}</dt><dd>{value}</dd></div>)}</dl>
        {asset.relations.length > 0 ? <section><h3>关联资产</h3>{asset.relations.map((r, i) => {
          const target = assets.find(a => a.id === r.target);
          return <p key={i}>{target ? <button type="button" className="shared-related" onClick={() => onSelect(target.id)}>{target.id} · {target.name}</button> : r.target}
            <small> · {r.role}{r.note ? ` · ${r.note}` : ""}</small></p>;
        })}</section> : null}
        {asset.backlinks?.length ? <section><h3>被引用</h3>{asset.backlinks.map((b, i) => {
          const source = assets.find(a => a.id === b.source);
          return <p key={i}>{source ? <button type="button" className="shared-related" onClick={() => onSelect(source.id)}>{source.id} · {source.name}</button> : b.source}
            <small> · {b.kind} · {b.role}</small></p>;
        })}</section> : null}
      </div>
    </div>
    {asset.views ? <section className="shared-three-views" aria-label="资产三视图">
      <h3>三面设定图</h3><p>{IMAGE_STATUS[asset.views.status] ?? asset.views.status} · 左起依次为{asset.views.panels.join('、')}</p>
      {asset.views.sha256 ? <a href={mediaUrl(sharedFile(libraryRoot, asset.views.sheet))} target="_blank" rel="noreferrer" title="打开三视图原图">
        <img src={mediaUrl(sharedFile(libraryRoot, asset.views.sheet))} alt={`${asset.name} ${asset.views.panels.join('、')}三视图`} />
      </a> : <p>三视图正在制作，完成后会自动显示。</p>}
      {asset.views.review_notes?.length ? <ul>{asset.views.review_notes.map((note, i) => <li key={i}>{note}</li>)}</ul> : null}
      <Link to={sharedFileHref(libraryRoot, asset.views.prompt)}>三视图出图描述</Link>
    </section> : null}
  </article>;
}

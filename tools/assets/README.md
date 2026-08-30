# assets_sync — `ai_videos/` 媒体的集中存储

媒体（视频/图片/音频/PDF）被 `.gitignore` 挡在版本库外，所以 git 本身回答不了
「这个 commit 对应哪些字节」。本工具把**字节**放进 Cloudflare R2（S3 兼容），把
**索引**放进 git：`ai_videos/assets.json` 记录 `路径 -> sha256`，像普通文件一样
可 diff、可 review、可回滚。

## 为什么不用 Git LFS

LFS 里文件仍被 git 追踪，只是内容换成指针——**每一版都永久留存**，删了也不回收。
短剧工作流一个 shot 会重渲十几版，LFS 会把十几版全留着；R2 按路径覆盖，
只留当前引用的那一份。R2 出网流量免费，反复取回旧集不额外计费。

## 设计

- **对象 key 就是 `ai_videos/` 下的路径**：bucket 里的目录树和磁盘上一模一样，
  在 R2 控制台按剧名 / `characters/` / `episodes/epNN/` 一层层点开即可（中文 key
  实测可用）。sha256 只用来判断「变没变」：改名走服务端 `CopyObject`，不耗上行带宽。
- **git 是它所持有内容的唯一真相**：被 git 跟踪的文件（如 `0_原作资料/_refs/`
  的一手参考图）**不会**上传，避免同一份东西两个地方各存一份。
- **不同步的**：`_deleted/`（回收站，本来就在等着被清）、`previz/frames/`
  （由 `previz_config.toml` 重算得出）。
- **sha256 缓存**：`.assets_cache.json`（根目录，gitignored）按 (size, mtime_ns)
  缓存哈希，避免每次重算 6+ GB。删掉即可重建。
- **清单描述的是整个项目，不是这台机器**：清单里有、本机没有的条目，可能是「被删了」
  也可能是「还没 pull」，两者分不清 —— 所以 push **默认保留**这些条目，不会因为你
  本机没下载就把别人的素材从索引里抹掉。确实是删除，用 `push --prune-missing` 明说。

## 用法

```bash
python tools/assets_sync.py status            # 本地 vs 清单，无需凭据
python tools/assets_sync.py push --dry-run    # 看要传什么
python tools/assets_sync.py push              # 上传 + 重写清单
python tools/assets_sync.py push --prune-missing   # 把「本机已删除」的条目也从清单里去掉
python tools/assets_sync.py pull              # 补齐本地缺失的文件
python tools/assets_sync.py prune             # 列出无人引用的远端对象
python tools/assets_sync.py prune --yes       # 真的删除（不可逆）
```

装了 hook 之后这些命令平时都不用手敲 —— commit 自动上传、pull 自动下载，见下一节。

换机器 / 新 clone：`git pull` → `python tools/assets_sync.py install-hooks` →
`python tools/assets_sync.py pull`（第一次要手动拉一次，因为 hook 是刚装上的）。

## 怎么保证「文件 / 清单 / R2 / git」四者不脱节

**顺序是有方向的：字节先上去，索引后跟上。**

```
1. python tools/assets_sync.py push     # MP4 等字节 -> R2，同时重写 assets.json
2. git add ai_videos/assets.json && git commit
3. git push
```

反过来做（先 push 清单再传字节）会让所有 `git pull` 的人拿到一份指向不存在对象的
索引，`assets_sync.py pull` 直接失败。

**这条顺序由 git hook 强制，而且已经自动化了。** 每个 clone 装一次：

```bash
python tools/assets_sync.py install-hooks
```

装上之后，日常只需要 `git commit` / `git push` / `git pull`，媒体自己跟着走：

- **`pre-commit`** —— 提交前把新增/改动的媒体传到 R2，重写 `assets.json` 并
  `git add` 进**这一次**提交。这是唯一能让「字节」和「索引」进同一个 commit 的
  钩子点，所以上传放在提交时、不是推送时。**离线不会挡住提交**（只告警，交给
  pre-push 兜底）。不想上传：`ASSETS_SYNC_AUTO_PUSH=0 git commit` 或 `--no-verify`。
- **`pre-push`** —— 兜底。正常情况下无事可做；如果还有媒体没进清单（比如上次
  `--no-verify` 提交过，或当时 R2 不通），它**先把字节传上去**，然后**拒绝这次
  push** —— 因为它刚重写的 `assets.json` 还没进任何 commit，推上去索引就落后于
  对象了。照提示 `git add ai_videos/assets.json && git commit && git push` 即可。
  确实想让索引暂时滞后就 `git push --no-verify`。
- **`post-merge` / `post-rewrite` / `post-checkout`** —— `git pull` 之后（merge、
  `--rebase`、切分支三种情况都覆盖）**自动把本机缺的图片/MP4 拉下来**，边下边打
  进度。不想自动下载：`ASSETS_SYNC_AUTO_PULL=0`，之后手动 `assets_sync.py pull`。

扫描走 sha256 缓存，1339 个文件约 0.9 秒，不会让 commit/push 变慢。

`.git/hooks/` 不进版本库，所以每个 clone 都要自己装一次；`tools/assets/hooks/` 里的
是被跟踪的模板，装的时候会把当前解释器路径写死进去。

**中断可续传。** push 会先列一遍 bucket，已经在里面且大小一致的对象直接跳过，
清单每 25 个文件落一次盘 —— 传到一半断网，重跑继续，不会重传已上传的部分。

## prune 会破坏历史

`prune` 删掉「当前清单不引用」的对象。但**旧 commit 的清单可能还引用着它们** ——
删完之后 checkout 到旧 commit 再 `pull` 就会失败。只有在你确定不需要回到旧版本的
素材时才 prune。默认只列不删，必须显式 `--yes`。

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

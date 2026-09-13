import { useCallback, useEffect, useRef, useState } from "react";
import { muxBgm } from "../lib/toolsApi";
import { ApiError } from "../types";

interface Produced {
  url: string;
  filename: string;
  size: number;
  outputPath: string;
}

function humanSize(bytes: number): string {
  if (bytes < 1024) return `${bytes} B`;
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
  return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
}

export function ToolsPage(): JSX.Element {
  const [video, setVideo] = useState<File | null>(null);
  const [audio, setAudio] = useState<File | null>(null);
  const [bgmVolume, setBgmVolume] = useState<number>(0.6);
  const [noLoop, setNoLoop] = useState<boolean>(false);
  const [keepSourceAudio, setKeepSourceAudio] = useState<boolean>(false);
  const [sourceVolume, setSourceVolume] = useState<number>(1);
  const [duckSource, setDuckSource] = useState<boolean>(false);
  const [bgmStart, setBgmStart] = useState<number>(0);
  const [fadeIn, setFadeIn] = useState<number>(0);
  const [fadeOut, setFadeOut] = useState<number>(0);
  const [busy, setBusy] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const [produced, setProduced] = useState<Produced | null>(null);
  const [copied, setCopied] = useState<boolean>(false);

  // One object URL is alive at a time; revoke the previous one so a long
  // session of re-generates doesn't pin every earlier cut in memory.
  const urlRef = useRef<string | null>(null);
  const replaceUrl = useCallback((next: string | null) => {
    if (urlRef.current) URL.revokeObjectURL(urlRef.current);
    urlRef.current = next;
  }, []);
  useEffect(() => () => replaceUrl(null), [replaceUrl]);

  const onGenerate = useCallback(async () => {
    if (!video || !audio || busy) return;
    setBusy(true);
    setError(null);
    setProduced(null);
    setCopied(false);
    replaceUrl(null);
    try {
      const result = await muxBgm(video, audio, {
        bgmVolume, noLoop, keepSourceAudio, sourceVolume, duckSource, bgmStart, fadeIn, fadeOut,
      });
      const url = URL.createObjectURL(result.blob);
      replaceUrl(url);
      setProduced({
        url, filename: result.filename, size: result.blob.size, outputPath: result.outputPath,
      });
    } catch (err) {
      const msg =
        err instanceof ApiError
          ? `生成失败: ${err.detail?.message ?? err.detail?.kind ?? err.status}`
          : `生成失败: ${err instanceof Error ? err.message : String(err)}`;
      setError(msg);
    } finally {
      setBusy(false);
    }
  }, [
    audio, bgmStart, bgmVolume, busy, duckSource, fadeIn, fadeOut, keepSourceAudio,
    noLoop, replaceUrl, sourceVolume, video,
  ]);

  return (
    <div className="tools-page">
      <header className="tools-header">
        <h1>工具</h1>
        <p className="tools-sub">给视频加背景音乐 · 选一个视频和一个音频，生成合成后的 MP4</p>
      </header>

      <section className="tools-card" aria-label="加入 BGM">
        <h2>加入 BGM</h2>

        <div className="tools-row">
          <label className="tools-label" htmlFor="tool-video">视频</label>
          <input
            id="tool-video"
            className="tools-file"
            type="file"
            accept="video/*,.mp4,.mov,.mkv,.webm,.m4v,.avi"
            onChange={(e) => setVideo(e.target.files?.[0] ?? null)}
          />
          <span className="tools-picked">
            {video ? `${video.name} · ${humanSize(video.size)}` : "未选择文件"}
          </span>
        </div>

        <div className="tools-row">
          <label className="tools-label" htmlFor="tool-audio">音频</label>
          <input
            id="tool-audio"
            className="tools-file"
            type="file"
            accept="audio/*,.m4a,.mp3,.wav,.aac,.flac,.ogg,.opus"
            onChange={(e) => setAudio(e.target.files?.[0] ?? null)}
          />
          <span className="tools-picked">
            {audio ? `${audio.name} · ${humanSize(audio.size)}` : "未选择文件"}
          </span>
        </div>

        <div className="tools-opts">
          <div className="tools-opt">
            <label htmlFor="tool-vol">音量 <b>{bgmVolume.toFixed(2)}</b></label>
            <input
              id="tool-vol" type="range" min={0} max={1} step={0.05}
              value={bgmVolume}
              onChange={(e) => setBgmVolume(Number(e.target.value))}
            />
          </div>
          <div className="tools-opt">
            <label htmlFor="tool-start">延后进入 (秒)</label>
            <input
              id="tool-start" type="number" min={0} step={0.5} value={bgmStart}
              onChange={(e) => setBgmStart(Number(e.target.value))}
            />
          </div>
          <div className="tools-opt">
            <label htmlFor="tool-fin">淡入 (秒)</label>
            <input
              id="tool-fin" type="number" min={0} step={0.5} value={fadeIn}
              onChange={(e) => setFadeIn(Number(e.target.value))}
            />
          </div>
          <div className="tools-opt">
            <label htmlFor="tool-fout">淡出 (秒)</label>
            <input
              id="tool-fout" type="number" min={0} step={0.5} value={fadeOut}
              onChange={(e) => setFadeOut(Number(e.target.value))}
            />
          </div>
        </div>

        <label className="tools-check">
          <input type="checkbox" checked={noLoop} onChange={(e) => setNoLoop(e.target.checked)} />
          不循环（音频比视频短时，尾部留静音；默认循环补满）
        </label>

        <label className="tools-check">
          <input
            type="checkbox"
            checked={keepSourceAudio}
            onChange={(e) => setKeepSourceAudio(e.target.checked)}
          />
          保留原视频声音（默认替换掉；视频本身没有声轨时此项自动忽略）
        </label>

        {keepSourceAudio ? (
          <div className="tools-subopts">
            <div className="tools-opt">
              <label htmlFor="tool-srcvol">原声音量 <b>{sourceVolume.toFixed(2)}</b></label>
              <input
                id="tool-srcvol" type="range" min={0} max={1} step={0.05}
                value={sourceVolume}
                onChange={(e) => setSourceVolume(Number(e.target.value))}
              />
            </div>
            <label className="tools-check">
              <input
                type="checkbox"
                checked={duckSource}
                onChange={(e) => setDuckSource(e.target.checked)}
              />
              BGM 自动避让原声（原声有人说话时用）
            </label>
          </div>
        ) : null}

        <p className="tools-note">
          时长一律以视频为准：音频长了裁掉多余部分，短了循环补满或留静音。视频流不重编码。
        </p>

        <div className="tools-actions">
          <button
            type="button"
            className="tools-generate"
            disabled={!video || !audio || busy}
            onClick={() => void onGenerate()}
          >
            {busy ? "生成中…" : "生成"}
          </button>
          {busy ? <span className="tools-busy">正在合成，长视频需要一点时间…</span> : null}
        </div>

        {error ? <div className="tools-error" role="alert">{error}</div> : null}

        {produced ? (
          <div className="tools-result">
            <div className="tools-result-head">
              <b>{produced.filename}</b>
              <span>{humanSize(produced.size)}</span>
              <a className="tools-download" href={produced.url} download={produced.filename}>
                另存为
              </a>
            </div>
            {produced.outputPath ? (
              <div className="tools-path">
                <span className="tools-path-label">已保存到</span>
                <code className="tools-path-value">{produced.outputPath}</code>
                <button
                  type="button"
                  className="tools-copy"
                  onClick={() => {
                    void navigator.clipboard.writeText(produced.outputPath).then(
                      () => setCopied(true),
                      () => setCopied(false),
                    );
                  }}
                >
                  {copied ? "已复制" : "复制路径"}
                </button>
              </div>
            ) : null}
            <video className="tools-preview" src={produced.url} controls />
          </div>
        ) : null}
      </section>
    </div>
  );
}

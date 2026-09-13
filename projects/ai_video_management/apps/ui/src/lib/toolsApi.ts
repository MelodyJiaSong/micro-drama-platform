import { ApiError, type ApiErrorDetail } from "../types";

export interface MuxBgmOptions {
  bgmVolume: number;
  noLoop: boolean;
  keepSourceAudio: boolean;
  sourceVolume: number;
  duckSource: boolean;
  bgmStart: number;
  fadeIn: number;
  fadeOut: number;
}

export interface MuxBgmResult {
  blob: Blob;
  filename: string;
  /** Absolute path of the saved file on the machine running the backend. */
  outputPath: string;
}

function filenameFrom(header: string | null, fallback: string): string {
  if (!header) return fallback;
  const star = /filename\*=UTF-8''([^;]+)/i.exec(header);
  if (star) {
    try {
      return decodeURIComponent(star[1]);
    } catch {
      // fall through to the plain form
    }
  }
  const plain = /filename="([^"]+)"/i.exec(header);
  return plain ? plain[1] : fallback;
}

/** POST the two uploads and get the muxed MP4 back as a blob.
 *
 * The response body is the video itself, not JSON — only an error comes back as
 * JSON, so the failure path parses and the success path does not. */
export async function muxBgm(
  video: File,
  audio: File,
  options: MuxBgmOptions,
): Promise<MuxBgmResult> {
  const form = new FormData();
  form.append("video", video);
  form.append("audio", audio);
  form.append("bgm_volume", String(options.bgmVolume));
  form.append("no_loop", String(options.noLoop));
  form.append("keep_source_audio", String(options.keepSourceAudio));
  form.append("source_volume", String(options.sourceVolume));
  form.append("duck_source", String(options.duckSource));
  form.append("bgm_start", String(options.bgmStart));
  form.append("fade_in", String(options.fadeIn));
  form.append("fade_out", String(options.fadeOut));

  const response = await fetch("/api/mux/bgm", { method: "POST", body: form });
  if (!response.ok) {
    let detail: ApiErrorDetail | null = null;
    try {
      const parsed = await response.json();
      const d = parsed && typeof parsed === "object" ? (parsed as { detail?: unknown }).detail : null;
      if (d && typeof d === "object") detail = d as ApiErrorDetail;
    } catch {
      // body wasn't JSON
    }
    throw new ApiError(response.status, `HTTP ${response.status}`, detail);
  }
  // Percent-encoded by the server: HTTP header values are latin-1 and these
  // paths are routinely Chinese.
  const rawPath = response.headers.get("x-output-path");
  let outputPath = "";
  if (rawPath) {
    try {
      outputPath = decodeURIComponent(rawPath);
    } catch {
      outputPath = rawPath;
    }
  }
  return {
    blob: await response.blob(),
    filename: filenameFrom(response.headers.get("content-disposition"), "output_bgm.mp4"),
    outputPath,
  };
}

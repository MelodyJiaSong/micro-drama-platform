import { useState } from "react";

interface SafeImageProps {
  src: string;
  alt: string;
  className?: string;
  missingText?: string;
}

export function SafeImage({ src, alt, className = "thumb", missingText }: SafeImageProps) {
  const [failed, setFailed] = useState(false);
  if (failed) {
    return <span className="thumb-missing">{missingText ?? `图片无法加载：${alt}`}</span>;
  }
  return <img className={className} src={src} alt={alt} loading="lazy" onError={() => setFailed(true)} />;
}

import { useState } from "react";

export default function OptimizedImage({ src, alt, width, height, className, style, format = "webp" }) {
  const [loaded, setLoaded] = useState(false);
  const [error, setError] = useState(false);

  if (src.startsWith("http") || src.startsWith("data:") || !src) {
    return (
      <img
        src={src}
        alt={alt || ""}
        width={width}
        height={height}
        className={`${className || ""} ${loaded ? "opacity-100" : "opacity-0"}`}
        style={{ transition: "opacity 0.2s", ...style }}
        loading="lazy"
        onLoad={() => setLoaded(true)}
        onError={() => setError(true)}
      />
    );
  }

  if (error) {
    return (
      <div
        className={`flex items-center justify-center bg-slate-700 text-slate-500 ${className || ""}`}
        style={{ width: width || "auto", height: height || "auto", ...style }}
      >
        <span className="text-xs">IMG</span>
      </div>
    );
  }

  let cloudUrl = src;
  if (src.startsWith("/uploads/") || src.startsWith("/images/")) {
    const publicId = src.replace(/^\//, "").replace(/\.(png|jpg|jpeg|webp)$/, "");
    cloudUrl = `https://res.cloudinary.com/placementpro/image/upload/w_${width || "auto"}/q_auto,f_${format}/${publicId}`;
  }

  return (
    <img
      src={cloudUrl}
      alt={alt || ""}
      width={width}
      height={height}
      className={`${className || ""} ${loaded ? "opacity-100" : "opacity-0"}`}
      style={{ transition: "opacity 0.2s", ...style }}
      loading="lazy"
      onLoad={() => setLoaded(true)}
      onError={() => setError(true)}
    />
  );
}

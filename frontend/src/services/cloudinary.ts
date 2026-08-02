export const CLOUDINARY_CLOUD_NAME = "placementpro";

interface ImageOptions {
  width?: string | number;
  height?: string | number;
  quality?: string | number;
  format?: string;
}

export function cloudinaryImage(publicId: string, options: ImageOptions = {}) {
  const { width = "auto", height = "auto", quality = "auto", format = "auto" } = options;
  const transformations = [
    `w_${width}`,
    `h_${height}`,
    `q_${quality}`,
    `f_${format}`,
  ].filter(Boolean);
  const transformStr = transformations.join("/");
  return `https://res.cloudinary.com/${CLOUDINARY_CLOUD_NAME}/image/upload/${transformStr}/${publicId}`;
}

export function cloudinaryVideo(publicId: string, options: ImageOptions = {}) {
  const { width = "auto", height = "auto", quality = "auto" } = options;
  const transformations = [`w_${width}`, `h_${height}`, `q_${quality}`];
  const transformStr = transformations.filter(Boolean).join("/");
  return `https://res.cloudinary.com/${CLOUDINARY_CLOUD_NAME}/video/upload/${transformStr}/${publicId}`;
}

export function optimizeImage(imgUrl: string, width = 300) {
  if (imgUrl.startsWith("http")) return imgUrl;
  const ext = imgUrl.split(".").pop()!.toLowerCase();
  const format = ext === "png" || ext === "gif" ? "webp" : "auto";
  return cloudinaryImage(imgUrl.replace(/\.(png|jpg|jpeg|webp)$/, ""), {
    width,
    format,
    quality: "auto",
  });
}

/// <reference types="vite/client" />

declare module "html2canvas" {
  export interface Html2CanvasOptions {
    backgroundColor?: string;
    scale?: number;
    useCORS?: boolean;
    [key: string]: any;
  }
  function html2canvas(element: HTMLElement, options?: Html2CanvasOptions): Promise<HTMLCanvasElement>;
  export default html2canvas;
}

interface Window {
  gtag?: (...args: any[]) => void;
  USER_COLLEGE?: string;
}
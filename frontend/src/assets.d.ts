/** SVG module declarations for Vite + React */
declare module '*.svg' {
  const content: React.FC<React.SVGProps<SVGSVGElement>>;
  export default content;
  export const ReactComponent: React.FC<React.SVGProps<SVGSVGElement>>;
}

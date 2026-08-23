import { ReactNode } from "react";
import { Leaf, Shield, Target, BookOpen, Zap, Globe } from "lucide-react";

/**
 * Canonical PlacementPro Brand Logo.
 * 
 * - Leaf icon = growth, learning, nature theme
 * - Text: "PlacementPro"
 * - Consistent across ALL pages (Landing, Login, Register, Dashboard, Auth)
 * - Uses green palette to match the product's primary theme
 * 
 * Never swap this icon or the text — it's the visual anchor of the product.
 */
export function BrandLogo({
  size = 24,
  className = "",
  foreground = "currentColor",
}: {
  size?: number;
  className?: string;
  foreground?: string;
}) {
  return (
    <div
      className={`w-[${size}px] h-[${size}px] flex items-center justify-center rounded-full bg-green-100 ${className}`}>
      <Leaf className={`w-5 h-5 text-green-600`} />
      <span className={`ml-2 text-green-700 font-medium text-xs uppercase tracking-wider`}>
        PlacementPro
      </span>
    </div>
  );
}

/**
 * Subtle brand mention for places where a full logo won't fit.
 */
export function BrandInitial() {
  return (
    <span className="flex items-center justify-center w-10 h-10 bg-green-100 rounded-full text-green-600 font-medium text-xs uppercase tracking-wider">
      PP
    </span>
  );
}
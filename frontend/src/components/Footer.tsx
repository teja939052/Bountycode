import { Zap } from "lucide-react";

export default function Footer() {
  return (
    <footer className="mt-auto border-t border-black/5 bg-white border-border/70 backdrop-blur supports-[backdrop-filter]:bg-white border-border/80">
      <div className="mx-auto max-w-7xl px-4 py-6 sm:px-6 lg:px-8">
        <div className="flex flex-col items-center justify-between gap-4 text-center md:flex-row md:text-left">
          <div className="flex items-center gap-2">
            <div className="flex h-6 w-6 items-center justify-center rounded-lg bg-nature-leaf">
              <Zap size={12} className="text-text-primary" />
            </div>
            <span className="font-display text-sm font-bold tracking-wider text-text-primary">
              PLACEMENT<span className="text-nature-blossom">PRO</span>
            </span>
          </div>
          <p className="max-w-md text-xs font-mono text-text-muted">
            AI-powered placement preparation. A calm path to the offer.
          </p>
          <div className="flex gap-6 text-xs font-mono text-text-muted">
            <a href="#" onClick={(e) => e.preventDefault()} className="hover:text-nature-blossom transition-colors">Privacy</a>
            <a href="#" onClick={(e) => e.preventDefault()} className="hover:text-nature-blossom transition-colors">Terms</a>
            <a href="mailto:support@placementpro.app" className="hover:text-nature-blossom transition-colors">Support</a>
          </div>
        </div>
      </div>
    </footer>
  );
}

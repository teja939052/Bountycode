import { Zap } from "lucide-react";

export default function Footer() {
  return (
    <footer className="border-t border-orange-100 bg-white/80 backdrop-blur-sm mt-auto">
      <div className="max-w-7xl mx-auto px-4 py-8">
        <div className="flex flex-col md:flex-row items-center justify-between gap-4">
          <div className="flex items-center gap-2">
            <div className="w-6 h-6 bg-gradient-to-br from-brand-coral to-pink-400 rounded-lg flex items-center justify-center">
              <Zap size={12} className="text-white" />
            </div>
            <span className="font-display font-bold text-text-primary text-sm tracking-wider">
              PLACEMENT<span className="text-brand-coral">PRO</span>
            </span>
          </div>
          <p className="text-xs font-mono text-text-muted">
            AI-powered placement preparation. Navigate your career orbit.
          </p>
          <div className="flex gap-6 text-xs font-mono text-text-muted">
            <a href="#" onClick={(e) => e.preventDefault()} className="hover:text-brand-coral transition-colors">Privacy</a>
            <a href="#" onClick={(e) => e.preventDefault()} className="hover:text-brand-coral transition-colors">Terms</a>
            <a href="mailto:support@placementpro.app" className="hover:text-brand-coral transition-colors">Support</a>
          </div>
        </div>
      </div>
    </footer>
  );
}

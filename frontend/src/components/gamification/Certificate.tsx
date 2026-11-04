import { ShieldCheck, Award, Zap, Star, Link } from 'lucide-react';
import { CODDY, coddyGlow } from './palette';

export interface CertificateProps {
  name: string;
  section: string;
  topic: string;
  id: string;
  date: string;
  issuer: string;
}

export default function Certificate({ name, section, topic, id, date, issuer }: CertificateProps) {
  return (
    <div className="relative p-8 md:p-12 bg-white dark:bg-slate-900 border-4 border-dark-blue dark:border-white rounded-2xl shadow-2xl overflow-hidden max-w-2xl mx-auto">
      {/* Seal */}
      <div className="absolute top-6 left-6 w-16 h-16 rounded-full bg-warning-500 flex items-center justify-center text-white font-bold shadow-lg border-4 border-white dark:border-white">
        <ShieldCheck size={32} />
      </div>

      {/* Top border decoration */}
      <div className="absolute top-0 left-0 right-0 h-1 bg-gradient-to-r from-warning-500 via-dark-blue-600 to-warning-500" />

      <div className="relative z-10">
        <div className="flex justify-between items-start mb-8">
          <div>
            <p className="text-[10px] uppercase tracking-[0.3em] text-slate-500 dark:text-slate-400 font-bold mb-1">Certificate of Completion</p>
            <h1 className="text-3xl md:text-4xl font-serif font-bold text-ink dark:text-white italic leading-tight">BountyCode</h1>
          </div>
          <div className="text-right">
            <p className="text-[10px] font-mono text-slate-400 dark:text-slate-500">Cert ID: {id}</p>
            <p className="text-sm font-bold text-ink dark:text-white">Verifiable</p>
          </div>
        </div>

        <div className="border-t border-white/20 dark:border-white/10 my-8" />

        <p className="text-lg text-slate-600 dark:text-slate-300 leading-relaxed mb-6">
          This is to certify that
        </p>
        <div className="flex items-center gap-3 mb-8">
          <div className="flex-1 border-b border-warning-500/30 dark:border-warning-400/30" />
          <span className="text-2xl font-serif font-bold text-ink dark:text-white whitespace-nowrap">{name}</span>
          <div className="flex-1 border-b border-warning-500/30 dark:border-warning-400/30" />
        </div>

        <p className="text-sm text-slate-500 dark:text-slate-400 mb-1">has successfully completed the section</p>
        <h2 className="text-xl font-bold text-ink dark:text-white mb-8">{section}</h2>

        <div className="grid grid-cols-2 md:grid-cols-3 gap-4 text-sm text-slate-600 dark:text-slate-400">
          <div className="flex items-center gap-2">
            <Star size={14} className="text-warning-500" />
            <span>Topic: {topic}</span>
          </div>
          <div className="flex items-center gap-2">
            <Zap size={14} className="text-dark-blue-500 dark:text-dark-blue-400" />
            <span>Issued: {date}</span>
          </div>
          <div className="flex items-center gap-2">
            <Link size={14} className="text-success-500 dark:text-success-400" />
            <span>Verifiable</span>
          </div>
        </div>

        <div className="mt-12 pt-8 border-t border-white/20 dark:border-white/10 flex items-center justify-between">
          <div className="text-[10px] uppercase tracking-wider text-slate-400 dark:text-slate-500 font-bold">Issuer</div>
          <div className="text-[10px] uppercase tracking-wider text-slate-400 dark:text-slate-500 font-bold">Date</div>
        </div>
        <div className="flex items-center justify-between mt-1">
          <span className="text-sm font-medium text-ink dark:text-slate-200">{issuer}</span>
          <span className="text-sm font-medium text-ink dark:text-slate-200">{date}</span>
        </div>
      </div>
    </div>
  );
}

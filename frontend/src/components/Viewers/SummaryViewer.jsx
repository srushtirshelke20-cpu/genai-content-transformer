import React from 'react';
import { FileText, Target } from 'lucide-react';

export function SummaryViewer({ summary }) {
  if (!summary) return <div className="p-6 text-gray-500 text-center">No Summary generated yet.</div>;

  return (
    <div className="bg-white rounded-xl border border-slate-200 p-6 shadow-sm">
      <div className="flex items-center gap-2 pb-4 mb-4 border-b border-slate-100">
        <FileText className="w-5 h-5 text-teal-600" />
        <span className="text-xs font-bold uppercase tracking-wider text-teal-600">Executive Summary</span>
      </div>

      {/* BLUF Callout Box */}
      <div className="bg-teal-50 border-l-4 border-teal-600 p-4 rounded-r-lg mb-5">
        <div className="text-xs font-bold uppercase text-teal-800 tracking-wider mb-1">
          BLUF (Bottom Line Up Front)
        </div>
        <p className="text-sm font-medium text-teal-950 leading-relaxed">{summary.bluf}</p>
      </div>

      {/* Bulleted Takeaways */}
      <div className="mb-5">
        <h4 className="text-xs font-bold uppercase text-slate-500 mb-2">Key Strategic Findings</h4>
        <ul className="list-disc pl-5 text-sm text-slate-800 space-y-1.5">
          {summary.key_findings?.map((finding, idx) => (
            <li key={idx}>{finding}</li>
          ))}
        </ul>
      </div>

      <div className="mb-5">
        <h4 className="text-xs font-bold uppercase text-slate-500 mb-1">Strategic Implications</h4>
        <p className="text-sm text-slate-700 leading-relaxed">{summary.strategic_implications}</p>
      </div>

      <div className="p-3 bg-slate-50 rounded-lg border border-dashed border-slate-300 flex items-start gap-2">
        <Target className="w-4 h-4 text-slate-600 mt-0.5 flex-shrink-0" />
        <div className="text-xs">
          <strong className="text-slate-700 uppercase">Recommended Decision: </strong>
          <span className="text-slate-900 font-semibold">{summary.recommended_decision}</span>
        </div>
      </div>
    </div>
  );
}

import React, { useState } from 'react';
import { ShieldAlert, Calendar, CheckSquare, Square } from 'lucide-react';

export function AdvisoryViewer({ advisory }) {
  const [completedActions, setCompletedActions] = useState({});

  if (!advisory) return <div className="p-6 text-gray-500 text-center">No Advisory generated yet.</div>;

  const isCritical = advisory.severity_level?.toUpperCase() === 'CRITICAL';
  const severityBadgeClass = isCritical
    ? 'bg-red-100 text-red-800 border-red-300'
    : 'bg-amber-100 text-amber-800 border-amber-300';

  const toggleAction = (idx) => {
    setCompletedActions(prev => ({ ...prev, [idx]: !prev[idx] }));
  };

  return (
    <div className="bg-white rounded-xl border border-slate-200 p-6 shadow-sm">
      <div className="flex justify-between items-start pb-4 mb-4 border-b border-slate-100 flex-wrap gap-2">
        <div className="flex items-center gap-2">
          <ShieldAlert className={`w-6 h-6 ${isCritical ? 'text-red-600' : 'text-amber-600'}`} />
          <div>
            <span className="text-xs font-bold uppercase tracking-wider text-slate-500">Security & Policy Advisory</span>
            <h3 className="text-lg font-bold text-slate-900">{advisory.advisory_id}</h3>
          </div>
        </div>
        <div className="flex items-center gap-3">
          <span className="flex items-center gap-1 text-xs text-slate-500">
            <Calendar className="w-3.5 h-3.5" /> {advisory.date_issued}
          </span>
          <span className={`px-3 py-1 text-xs font-bold rounded-full border ${severityBadgeClass}`}>
            {advisory.severity_level}
          </span>
        </div>
      </div>

      <div className="bg-slate-50 border border-slate-200 rounded-lg p-3 text-xs text-slate-700 mb-4">
        <strong>Target Systems:</strong> {advisory.target_audience_or_systems}
      </div>

      <div className="mb-4">
        <h4 className="text-xs font-bold uppercase text-slate-500 mb-1">Threat Context</h4>
        <p className="text-sm text-slate-800 leading-relaxed">{advisory.threat_or_context_summary}</p>
      </div>

      <div className="mb-4">
        <h4 className="text-xs font-bold uppercase text-slate-500 mb-1">Impact Analysis</h4>
        <p className="text-sm text-slate-800 leading-relaxed">{advisory.impact_analysis}</p>
      </div>

      <div className="mb-4">
        <h4 className="text-xs font-bold uppercase text-red-700 mb-2">Immediate Required Actions</h4>
        <div className="space-y-2">
          {advisory.immediate_actions?.map((action, idx) => (
            <div
              key={idx}
              onClick={() => toggleAction(idx)}
              className="flex items-start gap-2 text-sm text-slate-800 cursor-pointer p-1.5 rounded hover:bg-slate-50"
            >
              {completedActions[idx] ? (
                <CheckSquare className="w-4 h-4 text-green-600 mt-0.5 flex-shrink-0" />
              ) : (
                <Square className="w-4 h-4 text-slate-400 mt-0.5 flex-shrink-0" />
              )}
              <span className={completedActions[idx] ? 'line-through text-slate-400' : ''}>{action}</span>
            </div>
          ))}
        </div>
      </div>

      <div>
        <h4 className="text-xs font-bold uppercase text-emerald-700 mb-2">Long-Term Recommendations</h4>
        <ul className="list-disc pl-5 text-sm text-slate-800 space-y-1">
          {advisory.long_term_recommendations?.map((rec, idx) => (
            <li key={idx}>{rec}</li>
          ))}
        </ul>
      </div>
    </div>
  );
}

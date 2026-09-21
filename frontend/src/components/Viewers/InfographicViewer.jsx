import React from 'react';
import { BarChart3, Layout } from 'lucide-react';

export function InfographicViewer({ plan }) {
  if (!plan) return <div className="p-6 text-gray-500 text-center">No Infographic generated yet.</div>;

  return (
    <div className="bg-white rounded-xl border border-slate-200 p-6 shadow-sm">
      <div className="flex justify-between items-center pb-4 mb-4 border-b border-slate-100">
        <div className="flex items-center gap-2">
          <BarChart3 className="w-5 h-5 text-indigo-600" />
          <div>
            <span className="text-xs font-bold uppercase tracking-wider text-indigo-600">Infographic Blueprint</span>
            <h3 className="text-base font-bold text-slate-900">{plan.main_title}</h3>
          </div>
        </div>
        <span className="flex items-center gap-1 text-xs bg-indigo-50 text-indigo-700 px-2.5 py-1 rounded font-medium">
          <Layout className="w-3.5 h-3.5" /> {plan.layout_style}
        </span>
      </div>

      {/* Hero Stat */}
      <div className="bg-gradient-to-r from-indigo-600 to-violet-600 text-white rounded-xl p-5 text-center mb-6 shadow-md">
        <div className="text-xs uppercase tracking-wider opacity-80 mb-1">Hero Statistic</div>
        <div className="text-2xl font-black">{plan.hero_statistic}</div>
      </div>

      {/* Key Metric Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
        {plan.sections?.map((item, idx) => (
          <div key={idx} className="border border-slate-200 rounded-lg p-4 bg-slate-50">
            <div className="text-sm font-bold text-indigo-600 mb-1">📌 {item.stat_or_icon}</div>
            <h5 className="text-sm font-bold text-slate-900 mb-1">{item.heading}</h5>
            <p className="text-xs text-slate-600 leading-relaxed">{item.description}</p>
          </div>
        ))}
      </div>

      {/* Color Palette */}
      {plan.color_palette_recommendation?.length > 0 && (
        <div className="pt-4 border-t border-slate-100 flex items-center gap-2">
          <span className="text-xs font-bold text-slate-500 uppercase">Palette:</span>
          <div className="flex gap-2">
            {plan.color_palette_recommendation.map((color, idx) => (
              <div key={idx} className="flex items-center gap-1 text-[11px] text-slate-600 bg-slate-100 px-2 py-0.5 rounded">
                <span className="w-3.5 h-3.5 rounded border border-black/10" style={{ backgroundColor: color }} />
                {color}
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

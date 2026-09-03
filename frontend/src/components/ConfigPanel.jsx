import React from 'react';
import { Loader2, Sparkles } from 'lucide-react';

export function ConfigPanel({ config, setConfig, onTransform, isLoading }) {
  const formats = [
    { id: 'linkedin', label: 'LinkedIn Post' },
    { id: 'twitter', label: 'Twitter Thread' },
    { id: 'advisory', label: 'Security Advisory' },
    { id: 'presentation', label: 'Slide Deck' },
    { id: 'video_package', label: 'Video Script' },
    { id: 'infographic', label: 'Infographic Plan' },
    { id: 'executive_summary', label: 'Executive Summary' }
  ];

  const handleFormatToggle = (id) => {
    setConfig(prev => {
      const exists = prev.selected_formats.includes(id);
      return {
        ...prev,
        selected_formats: exists
          ? prev.selected_formats.filter(f => f !== id)
          : [...prev.selected_formats, id]
      };
    });
  };

  return (
    <div className="bg-white rounded-xl border border-slate-200 p-5 shadow-sm space-y-4">
      <h3 className="text-xs font-bold uppercase tracking-wider text-slate-700">Configuration</h3>

      {/* Selectors Grid */}
      <div className="grid grid-cols-2 gap-3 text-xs">
        <div>
          <label className="font-semibold text-slate-600 block mb-1">Tone</label>
          <select
            value={config.tone}
            onChange={(e) => setConfig({ ...config, tone: e.target.value })}
            className="w-full p-2 rounded-md border border-slate-200 bg-white"
          >
            <option value="Professional">Professional</option>
            <option value="Urgent">Urgent</option>
            <option value="Authoritative">Authoritative</option>
            <option value="Conversational">Conversational</option>
            <option value="Technical">Technical</option>
          </select>
        </div>

        <div>
          <label className="font-semibold text-slate-600 block mb-1">Audience</label>
          <select
            value={config.target_audience}
            onChange={(e) => setConfig({ ...config, target_audience: e.target.value })}
            className="w-full p-2 rounded-md border border-slate-200 bg-white"
          >
            <option value="General Public">General Public</option>
            <option value="C-Suite">C-Suite</option>
            <option value="Technical">Technical Engineers</option>
          </select>
        </div>

        <div>
          <label className="font-semibold text-slate-600 block mb-1">Objective</label>
          <select
            value={config.objective}
            onChange={(e) => setConfig({ ...config, objective: e.target.value })}
            className="w-full p-2 rounded-md border border-slate-200 bg-white"
          >
            <option value="Inform">Inform</option>
            <option value="Alert">Alert</option>
            <option value="Educate">Educate</option>
            <option value="Sell">Sell</option>
          </select>
        </div>

        <div>
          <label className="font-semibold text-slate-600 block mb-1">Detail Level</label>
          <select
            value={config.detail_level}
            onChange={(e) => setConfig({ ...config, detail_level: e.target.value })}
            className="w-full p-2 rounded-md border border-slate-200 bg-white"
          >
            <option value="Brief">Brief</option>
            <option value="Standard">Standard</option>
            <option value="Comprehensive">Comprehensive</option>
          </select>
        </div>
      </div>

      {/* Format Checkboxes */}
      <div>
        <label className="text-xs font-semibold text-slate-600 block mb-2">Output Formats (Select at least 1)</label>
        <div className="grid grid-cols-2 gap-2 text-xs">
          {formats.map(f => {
            const checked = config.selected_formats.includes(f.id);
            return (
              <label
                key={f.id}
                className={`flex items-center gap-2 p-2 rounded-md border cursor-pointer transition ${
                  checked ? 'bg-blue-50 border-blue-300 text-blue-900 font-medium' : 'border-slate-200 hover:bg-slate-50 text-slate-700'
                }`}
              >
                <input
                  type="checkbox"
                  checked={checked}
                  onChange={() => handleFormatToggle(f.id)}
                  className="rounded text-blue-600"
                />
                {f.label}
              </label>
            );
          })}
        </div>
      </div>

      {/* Primary Transform Button */}
      <button
        onClick={onTransform}
        disabled={isLoading}
        className="w-full py-3 bg-blue-600 hover:bg-blue-700 text-white font-semibold rounded-lg shadow-sm flex items-center justify-center gap-2 transition disabled:opacity-50"
      >
        {isLoading ? (
          <>
            <Loader2 className="w-4 h-4 animate-spin" /> Transforming Content...
          </>
        ) : (
          <>
            <Sparkles className="w-4 h-4" /> Transform Content
          </>
        )}
      </button>
    </div>
  );
}

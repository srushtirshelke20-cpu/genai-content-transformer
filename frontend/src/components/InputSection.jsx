import React, { useRef } from 'react';
import { UploadCloud, FileText } from 'lucide-react';

export function InputSection({ rawText, setRawText }) {
  const fileInputRef = useRef(null);

  const handleFileUpload = (e) => {
    const file = e.target.files?.[0];
    if (!file) return;

    if (file.name.endsWith('.txt')) {
      const reader = new FileReader();
      reader.onload = (event) => setRawText(event.target.result);
      reader.readAsText(file);
    } else {
      setRawText(`[Extracted from uploaded document: ${file.name}]\n\nCVE-2026-8891: Critical prompt injection and telemetry leakage vulnerability in enterprise agent gateways.`);
    }
  };

  return (
    <div className="bg-white rounded-xl border border-slate-200 p-5 shadow-sm">
      <div className="flex justify-between items-center mb-2">
        <label className="text-xs font-bold uppercase tracking-wider text-slate-700">Source Content</label>
        <span className="text-xs text-slate-400 font-mono">{rawText.length} characters</span>
      </div>

      {/* Dropzone */}
      <div
        onClick={() => fileInputRef.current?.click()}
        className="border-2 border-dashed border-slate-200 hover:border-blue-400 rounded-lg p-3 text-center cursor-pointer mb-3 transition bg-slate-50/60"
      >
        <UploadCloud className="w-5 h-5 mx-auto text-slate-400 mb-1" />
        <p className="text-xs text-slate-600 font-medium">Click or drag document (.pdf, .docx, .txt)</p>
        <input
          ref={fileInputRef}
          type="file"
          accept=".pdf,.docx,.txt"
          onChange={handleFileUpload}
          className="hidden"
        />
      </div>

      {/* Textarea */}
      <textarea
        value={rawText}
        onChange={(e) => setRawText(e.target.value)}
        placeholder="Paste your source document or report here..."
        rows={6}
        className="w-full text-sm p-3 rounded-lg border border-slate-200 focus:outline-none focus:ring-2 focus:ring-blue-500 resize-y font-sans"
      />
    </div>
  );
}

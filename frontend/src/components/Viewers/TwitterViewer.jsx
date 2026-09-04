import React, { useState } from 'react';
import { Copy, Check, Twitter } from 'lucide-react';

export function TwitterViewer({ thread }) {
  const [copiedAll, setCopiedAll] = useState(false);

  if (!thread) return <div className="p-6 text-gray-500 text-center">No Twitter thread generated yet.</div>;

  const handleCopyAll = () => {
    const fullThread = thread.tweets?.map(t => `${t.tweet_num}/ ${t.text}`).join("\n\n") || "";
    navigator.clipboard.writeText(fullThread);
    setCopiedAll(true);
    setTimeout(() => setCopiedAll(false), 2000);
  };

  return (
    <div className="bg-white rounded-xl border border-slate-200 p-6 shadow-sm">
      <div className="flex justify-between items-center pb-4 mb-4 border-b border-slate-100">
        <div className="flex items-center gap-2">
          <Twitter className="w-5 h-5 text-sky-500" />
          <span className="text-xs font-bold uppercase tracking-wider text-sky-500">Twitter / X Thread</span>
        </div>
        <button
          onClick={handleCopyAll}
          className="flex items-center gap-1.5 px-3 py-1.5 text-xs font-medium rounded-md border border-slate-200 bg-slate-50 hover:bg-slate-100 transition"
        >
          {copiedAll ? <Check className="w-3.5 h-3.5 text-green-600" /> : <Copy className="w-3.5 h-3.5 text-slate-600" />}
          {copiedAll ? "Thread Copied!" : "Copy All"}
        </button>
      </div>

      <div className="space-y-4">
        {thread.tweets?.map((tweet, idx) => {
          const charCount = tweet.text?.length || 0;
          const isOverLimit = charCount > 280;

          return (
            <div key={idx} className="border-l-2 border-sky-400 pl-4 py-1 relative">
              <div className="flex justify-between items-center mb-1">
                <span className="text-xs font-bold text-slate-500">Tweet {tweet.tweet_num || idx + 1}</span>
                <div className="flex items-center gap-2">
                  {tweet.suggested_media_type && tweet.suggested_media_type !== "None" && (
                    <span className="bg-amber-50 text-amber-700 border border-amber-200 px-2 py-0.5 rounded text-[11px] font-medium">
                      🖼️ {tweet.suggested_media_type}
                    </span>
                  )}
                  <span className={`text-[11px] font-mono ${isOverLimit ? 'text-red-500 font-bold' : 'text-slate-400'}`}>
                    {charCount}/280
                  </span>
                </div>
              </div>
              <p className="text-sm text-slate-800 leading-relaxed">{tweet.text}</p>
            </div>
          );
        })}
      </div>
    </div>
  );
}

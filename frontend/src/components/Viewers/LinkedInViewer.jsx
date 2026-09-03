import React, { useState } from 'react';
import { Copy, Check, Linkedin } from 'lucide-react';

export function LinkedInViewer({ post }) {
  const [copied, setCopied] = useState(false);

  if (!post) return <div className="p-6 text-gray-500 text-center">No LinkedIn post generated yet.</div>;

  const fullContent = [
    post.hook,
    "",
    ...(post.body_paragraphs || []),
    "",
    ...(post.bullet_points || []).map(bp => `• ${bp}`),
    "",
    post.call_to_action,
    "",
    (post.hashtags || []).join(" ")
  ].join("\n");

  const handleCopy = () => {
    navigator.clipboard.writeText(fullContent);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="bg-white rounded-xl border border-slate-200 p-6 shadow-sm">
      <div className="flex justify-between items-center pb-4 mb-4 border-b border-slate-100">
        <div className="flex items-center gap-2">
          <Linkedin className="w-5 h-5 text-blue-600" />
          <span className="text-xs font-bold uppercase tracking-wider text-blue-600">LinkedIn Post</span>
        </div>
        <button
          onClick={handleCopy}
          className="flex items-center gap-1.5 px-3 py-1.5 text-xs font-medium rounded-md border border-slate-200 bg-slate-50 hover:bg-slate-100 transition"
        >
          {copied ? <Check className="w-3.5 h-3.5 text-green-600" /> : <Copy className="w-3.5 h-3.5 text-slate-600" />}
          {copied ? "Copied!" : "Copy Post"}
        </button>
      </div>

      <div className="text-base font-semibold text-slate-900 mb-4 leading-snug">
        {post.hook}
      </div>

      {post.body_paragraphs?.map((p, idx) => (
        <p key={idx} className="text-sm text-slate-700 mb-3 leading-relaxed">
          {p}
        </p>
      ))}

      {post.bullet_points?.length > 0 && (
        <ul className="list-disc pl-5 mb-4 text-sm text-slate-700 space-y-1.5">
          {post.bullet_points.map((bp, idx) => (
            <li key={idx}>{bp}</li>
          ))}
        </ul>
      )}

      {post.call_to_action && (
        <p className="text-sm font-medium text-slate-800 italic mb-4">
          {post.call_to_action}
        </p>
      )}

      <div className="flex flex-wrap gap-1.5">
        {post.hashtags?.map((tag, idx) => (
          <span key={idx} className="bg-blue-50 text-blue-700 px-2.5 py-0.5 rounded-full text-xs font-medium">
            {tag}
          </span>
        ))}
      </div>
    </div>
  );
}

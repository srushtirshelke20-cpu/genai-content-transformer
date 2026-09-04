import React from 'react';
import { Video, Clock, Music } from 'lucide-react';

export function VideoViewer({ pkg }) {
  if (!pkg) return <div className="p-6 text-gray-500 text-center">No Video package generated yet.</div>;

  return (
    <div className="bg-white rounded-xl border border-slate-200 p-6 shadow-sm">
      <div className="flex justify-between items-center pb-4 mb-4 border-b border-slate-100 flex-wrap gap-2">
        <div className="flex items-center gap-2">
          <Video className="w-5 h-5 text-rose-600" />
          <div>
            <span className="text-xs font-bold uppercase tracking-wider text-rose-600">Video Storyboard</span>
            <h3 className="text-base font-bold text-slate-900">{pkg.title}</h3>
          </div>
        </div>
        <div className="flex items-center gap-2 text-xs">
          <span className="flex items-center gap-1 bg-rose-50 text-rose-700 px-2.5 py-1 rounded-md font-semibold">
            <Clock className="w-3.5 h-3.5" /> {pkg.target_duration}
          </span>
          <span className="flex items-center gap-1 bg-slate-100 text-slate-600 px-2.5 py-1 rounded-md">
            <Music className="w-3.5 h-3.5" /> {pkg.background_music_vibe}
          </span>
        </div>
      </div>

      <div className="space-y-4">
        {pkg.scenes?.map((scene, idx) => (
          <div key={idx} className="border border-slate-200 rounded-lg p-4 bg-slate-50/50">
            <div className="flex justify-between items-center mb-2">
              <span className="text-xs font-bold text-slate-800">Scene {scene.scene_num}</span>
              <span className="text-xs text-slate-500">{scene.duration_seconds}s</span>
            </div>
            <p className="text-xs text-slate-700 mb-2">
              <strong>Visual Cue:</strong> {scene.visual_description}
            </p>
            <div className="p-2.5 bg-white border border-slate-200 rounded text-xs text-slate-900 mb-2">
              <strong>🎙️ Narration:</strong> "{scene.narration_script}"
            </div>
            <div className="text-xs text-blue-600 mb-2">
              <strong>Subtitles / On-Screen:</strong> "{scene.on_screen_text}"
            </div>
            {scene.ai_image_prompt && (
              <div className="text-[11px] text-slate-500 bg-slate-100 p-2 rounded font-mono">
                🤖 <strong>AI Prompt:</strong> {scene.ai_image_prompt}
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}

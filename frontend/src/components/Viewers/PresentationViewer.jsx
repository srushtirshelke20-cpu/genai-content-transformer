import React, { useState } from 'react';
import { Presentation, Download, ChevronLeft, ChevronRight, MessageSquare } from 'lucide-react';

export function PresentationViewer({ deck }) {
  const [slideIndex, setSlideIndex] = useState(0);
  const [showNotes, setShowNotes] = useState(false);

  if (!deck || !deck.slides?.length) return <div className="p-6 text-gray-500 text-center">No Slides generated yet.</div>;

  const currentSlide = deck.slides[slideIndex];

  return (
    <div className="bg-white rounded-xl border border-slate-200 p-6 shadow-sm">
      <div className="flex justify-between items-center pb-4 mb-4 border-b border-slate-100 flex-wrap gap-2">
        <div className="flex items-center gap-2">
          <Presentation className="w-5 h-5 text-orange-600" />
          <div>
            <span className="text-xs font-bold uppercase tracking-wider text-orange-600">Slide Deck</span>
            <h3 className="text-base font-bold text-slate-900">{deck.deck_title}</h3>
          </div>
        </div>
        <button
          onClick={() => alert("Downloading presentation (.PPTX)...")}
          className="flex items-center gap-1.5 px-3 py-1.5 text-xs font-semibold rounded-md bg-orange-600 text-white hover:bg-orange-700 transition"
        >
          <Download className="w-3.5 h-3.5" /> Download .PPTX
        </button>
      </div>

      {/* 16:9 Slide Preview Canvas */}
      <div className="bg-slate-900 text-white rounded-xl p-6 min-h-[260px] flex flex-col justify-between shadow-inner mb-4">
        <div>
          <div className="text-[11px] text-slate-400 font-mono uppercase mb-2">
            Slide {currentSlide.slide_num} of {deck.slides.length}
          </div>
          <h2 className="text-xl font-bold text-slate-100 mb-4">{currentSlide.title}</h2>
          <ul className="list-disc pl-5 text-sm text-slate-300 space-y-2">
            {currentSlide.bullet_points?.map((bp, idx) => (
              <li key={idx}>{bp}</li>
            ))}
          </ul>
        </div>
        {currentSlide.visual_diagram_concept && (
          <div className="mt-4 p-2.5 rounded bg-white/10 text-xs text-sky-200 border border-white/5">
            📊 <strong>Visual Concept:</strong> {currentSlide.visual_diagram_concept}
          </div>
        )}
      </div>

      {/* Slide Navigation */}
      <div className="flex justify-between items-center mb-4">
        <button
          disabled={slideIndex === 0}
          onClick={() => setSlideIndex(prev => prev - 1)}
          className="flex items-center gap-1 px-3 py-1.5 text-xs font-medium border rounded-md disabled:opacity-40 hover:bg-slate-50"
        >
          <ChevronLeft className="w-4 h-4" /> Previous
        </button>
        <span className="text-xs font-medium text-slate-500">
          Slide {slideIndex + 1} / {deck.slides.length}
        </span>
        <button
          disabled={slideIndex === deck.slides.length - 1}
          onClick={() => setSlideIndex(prev => prev + 1)}
          className="flex items-center gap-1 px-3 py-1.5 text-xs font-medium border rounded-md disabled:opacity-40 hover:bg-slate-50"
        >
          Next <ChevronRight className="w-4 h-4" />
        </button>
      </div>

      {/* Speaker Notes Toggle */}
      {currentSlide.speaker_notes && (
        <div className="border-t border-slate-100 pt-3">
          <button
            onClick={() => setShowNotes(!showNotes)}
            className="flex items-center gap-1.5 text-xs font-medium text-slate-600 hover:text-slate-900"
          >
            <MessageSquare className="w-3.5 h-3.5" />
            {showNotes ? "Hide Speaker Notes" : "Show Speaker Notes"}
          </button>
          {showNotes && (
            <p className="mt-2 p-3 bg-slate-50 rounded-lg text-xs text-slate-700 leading-relaxed border border-slate-200">
              {currentSlide.speaker_notes}
            </p>
          )}
        </div>
      )}
    </div>
  );
}

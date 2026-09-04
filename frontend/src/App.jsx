import React, { useState } from 'react';
import { Activity } from 'lucide-react';
import { InputSection } from './components/InputSection';
import { ConfigPanel } from './components/ConfigPanel';
import { LinkedInViewer } from './components/Viewers/LinkedInViewer';
import { TwitterViewer } from './components/Viewers/TwitterViewer';
import { AdvisoryViewer } from './components/Viewers/AdvisoryViewer';
import { PresentationViewer } from './components/Viewers/PresentationViewer';
import { VideoViewer } from './components/Viewers/VideoViewer';
import { InfographicViewer } from './components/Viewers/InfographicViewer';
import { SummaryViewer } from './components/Viewers/SummaryViewer';
import mockData from './mock_data.json';

export default function App() {
  const [USE_MOCK, setUseMock] = useState(true);
  const [isLoading, setIsLoading] = useState(false);
  const [rawText, setRawText] = useState(
    "CVE-2026-8891: Critical remote prompt injection and telemetry leakage vulnerability in enterprise agent gateways allowing unauthorized credential exfiltration."
  );

  const [config, setConfig] = useState({
    target_audience: "General Public",
    tone: "Professional",
    objective: "Inform",
    detail_level: "Standard",
    selected_formats: ["linkedin", "twitter", "advisory", "presentation", "video_package", "infographic", "executive_summary"]
  });

  const [response, setResponse] = useState(mockData);
  const [activeTab, setActiveTab] = useState("linkedin");

  const handleTransform = async () => {
    setIsLoading(true);

    if (USE_MOCK) {
      // 1.5s simulated loading delay
      setTimeout(() => {
        setResponse(mockData);
        setIsLoading(false);
      }, 1500);
      return;
    }

    // Live API Call to backend
    try {
      const payload = { raw_text: rawText, ...config };
      const res = await fetch("http://localhost:8000/api/transform", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      });
      if (!res.ok) throw new Error("Backend API responded with an error");
      const data = await res.json();
      setResponse(data);
    } catch (err) {
      alert(`Connection Error: ${err.message}. Switch on 'USE_MOCK' for demo mode.`);
    } finally {
      setIsLoading(false);
    }
  };

  const tabs = [
    { id: 'linkedin', label: 'LinkedIn', available: config.selected_formats.includes('linkedin') && !!response?.linkedin_post },
    { id: 'twitter', label: 'Twitter Thread', available: config.selected_formats.includes('twitter') && !!response?.twitter_thread },
    { id: 'advisory', label: 'Advisory', available: config.selected_formats.includes('advisory') && !!response?.advisory },
    { id: 'presentation', label: 'Slide Deck', available: config.selected_formats.includes('presentation') && !!response?.presentation_deck },
    { id: 'video_package', label: 'Video Storyboard', available: config.selected_formats.includes('video_package') && !!response?.video_package },
    { id: 'infographic', label: 'Infographic', available: config.selected_formats.includes('infographic') && !!response?.infographic_plan },
    { id: 'executive_summary', label: 'Executive Summary', available: config.selected_formats.includes('executive_summary') && !!response?.executive_summary }
  ];

  return (
    <div className="min-h-screen bg-slate-100 text-slate-900 font-sans">
      {/* Top Navbar */}
      <nav className="bg-white border-b border-slate-200 px-6 py-3 flex justify-between items-center sticky top-0 z-10">
        <div className="flex items-center gap-3">
          <span className="text-lg font-black tracking-tight text-blue-600">GenAI Transformer</span>
          <span className="hidden sm:inline text-xs text-slate-400">| Enterprise Content Suite</span>
        </div>

        <div className="flex items-center gap-4">
          {/* Status Badge */}
          <div className="flex items-center gap-1.5 bg-emerald-50 text-emerald-700 border border-emerald-200 px-2.5 py-1 rounded-full text-xs font-semibold">
            <Activity className="w-3.5 h-3.5 animate-pulse text-emerald-600" />
            <span>Local Ollama Engine: Ready</span>
          </div>

          {/* USE_MOCK Toggle */}
          <label className="flex items-center gap-1.5 text-xs font-medium text-slate-600 cursor-pointer select-none">
            <input
              type="checkbox"
              checked={USE_MOCK}
              onChange={(e) => setUseMock(e.target.checked)}
              className="rounded text-blue-600"
            />
            USE_MOCK
          </label>
        </div>
      </nav>

      {/* Main Workspace Layout (40% / 60%) */}
      <main className="max-w-7xl mx-auto p-6 grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
        
        {/* Left Panel (40% = col-span-5) */}
        <div className="lg:col-span-5 space-y-5">
          <InputSection rawText={rawText} setRawText={setRawText} />
          <ConfigPanel
            config={config}
            setConfig={setConfig}
            onTransform={handleTransform}
            isLoading={isLoading}
          />
        </div>

        {/* Right Panel (60% = col-span-7) */}
        <div className="lg:col-span-7">
          {/* Format Tabs */}
          <div className="flex gap-1.5 overflow-x-auto pb-2 mb-4 border-b border-slate-200">
            {tabs.filter(t => t.available).map(tab => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`px-3 py-1.5 rounded-lg text-xs font-semibold whitespace-nowrap transition ${
                  activeTab === tab.id
                    ? 'bg-blue-600 text-white shadow-sm'
                    : 'bg-white text-slate-600 border border-slate-200 hover:bg-slate-50'
                }`}
              >
                {tab.label}
              </button>
            ))}
          </div>

          {/* Output Viewer Viewport */}
          <div>
            {activeTab === 'linkedin' && <LinkedInViewer post={response?.linkedin_post} />}
            {activeTab === 'twitter' && <TwitterViewer thread={response?.twitter_thread} />}
            {activeTab === 'advisory' && <AdvisoryViewer advisory={response?.advisory} />}
            {activeTab === 'presentation' && <PresentationViewer deck={response?.presentation_deck} />}
            {activeTab === 'video_package' && <VideoViewer pkg={response?.video_package} />}
            {activeTab === 'infographic' && <InfographicViewer plan={response?.infographic_plan} />}
            {activeTab === 'executive_summary' && <SummaryViewer summary={response?.executive_summary} />}
          </div>
        </div>

      </main>
    </div>
  );
}

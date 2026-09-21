  const handleTransform = async () => {
    setIsLoading(true);

    if (USE_MOCK) {
      setTimeout(() => {
        const text = rawText.toLowerCase();

        // 1. Sample 2: Governance Policy Directive
        if (text.includes("policy") || text.includes("governance") || text.includes("directive")) {
          setResponse({
            project_title: "Enterprise Generative AI Governance Policy",
            linkedin_post: {
              hook: "📋 New Directive: Establishing Enterprise Governance for Generative AI in the Workplace",
              body_paragraphs: [
                "As AI tools become integral to employee workflows, our organization is introducing formal guidelines to safeguard intellectual property, client confidential data, and proprietary code.",
                "Employees are required to use enterprise-licensed AI platforms with strict data isolation agreements. Public, consumer-tier subscriptions are strictly prohibited."
              ],
              bullet_points: [
                "Mandatory Data Isolation: Zero customer PII or proprietary code in external models",
                "Human-in-the-Loop Review: All AI-generated outputs must undergo human verification",
                "Compliance Audits: Automated DLP sensors monitoring enterprise endpoints"
              ],
              call_to_action: "Read the full policy mandate and review your team's compliance checklist below.",
              hashtags: ["#EnterpriseAI", "#AIGovernance", "#Compliance", "#CorporatePolicy"]
            },
            twitter_thread: {
              thread_hook: "🧵 1/4 Today we announced our organization's new Workplace Generative AI Governance Policy.",
              tweets: [
                { tweet_num: 1, text: "1/4 📋 Effective Oct 1, 2026: All employees must adhere to updated Generative AI governance directives to protect proprietary client data and source code." },
                { tweet_num: 2, text: "2/4 Key rule: Public, consumer AI tools are prohibited for company work. Only enterprise-licensed platforms with data isolation are permitted." },
                { tweet_num: 3, text: "3/4 Accountability: Human authors remain 100% responsible for verifying the accuracy, safety, and IP compliance of all AI-assisted deliverables." },
                { tweet_num: 4, text: "4/4 Automated DLP sensors will ensure compliance across all enterprise networks. Stay informed and work securely." }
              ]
            },
            advisory: {
              advisory_id: "POL-2026-GENAI",
              severity_level: "MEDIUM",
              date_issued: "2026-09-21",
              target_audience_or_systems: "All Global Employees & Contractors",
              threat_or_context_summary: "Balancing workplace AI productivity acceleration with legal mandates to protect confidential corporate IP and source code.",
              impact_analysis: "Failure to follow guidelines risks data leakage, IP invalidation, and disciplinary actions up to contract termination.",
              immediate_actions: [
                "Transition all AI workflows to approved enterprise-licensed accounts",
                "Audit local code repositories to ensure no API keys or proprietary snippets were pasted into external tools",
                "Complete the mandatory 15-minute AI Ethics and Governance training"
              ],
              long_term_recommendations: [
                "Implement continuous DLP egress monitoring on developer workstations",
                "Establish quarterly reviews for new enterprise AI integrations"
              ]
            },
            executive_summary: {
              bluf: "The new Generative AI Governance Directive establishes clear boundaries for safe workplace AI adoption while eliminating the risk of corporate IP and client data exposure.",
              key_findings: [
                "Enterprise data isolation is now mandatory across all departments",
                "Human peer review is required prior to releasing any AI-generated asset",
                "Automated network monitoring will enforce zero-tolerance data leak policies"
              ],
              strategic_implications: "Mitigates legal and copyright exposure while enabling controlled employee productivity gains.",
              recommended_decision: "Approve policy distribution to all regional business unit leaders."
            },
            presentation_deck: {
              deck_title: "Workplace Generative AI Governance",
              target_audience: config.target_audience,
              slides: [
                {
                  slide_num: 1,
                  title: "Policy Purpose & Objectives",
                  bullet_points: ["Safeguarding intellectual property", "Preventing client data exposure", "Standardizing approved AI tooling"],
                  visual_diagram_concept: "Balance scale: Innovation vs Data Governance",
                  speaker_notes: "Welcome team. Today we outline our organization's standard for secure, compliant Generative AI usage."
                },
                {
                  slide_num: 2,
                  title: "Mandatory Employee Rules",
                  bullet_points: ["No customer PII or source code in public LLMs", "Mandatory human-in-the-loop review", "Enterprise accounts only"],
                  visual_diagram_concept: "Shield flowchart showing data isolation gates",
                  speaker_notes: "Every employee is responsible for verifying outputs before sending them to clients."
                }
              ]
            }
          });
        } 
        
        // 2. Sample 3: AI Research (1-bit Quantization)
        else if (text.includes("quantization") || text.includes("binaryreason") || text.includes("research")) {
          setResponse({
            project_title: "Research Brief: Next-Gen Reasoning with 1-Bit Quantization",
            linkedin_post: {
              hook: "🧠 Breakthrough in On-Device AI: Running 7B Reasoning Models on Commodity Laptops",
              body_paragraphs: [
                "Deep Intelligence Labs has introduced 'BinaryReason-7B', a foundational LLM running entirely on 1.58-bit ternary weight parameters {-1, 0, 1}.",
                "While traditional models demand massive GPU clusters, this architecture achieves 94% parity with FP16 reasoning benchmarks while consuming just 1.8 GB RAM."
              ],
              bullet_points: [
                "Memory Footprint: Slashed from 14.5 GB down to 1.8 GB RAM",
                "Energy Efficiency: 82% reduction in watt-hours per 1,000 tokens",
                "Throughput: 48 tokens/sec on standard 4-core laptop CPUs"
              ],
              call_to_action: "Explore how 1-bit quantization unlocks fully air-gapped enterprise intelligence.",
              hashtags: ["#ArtificialIntelligence", "#MachineLearning", "#EdgeAI", "#DeepTech"]
            },
            twitter_thread: {
              thread_hook: "🧵 1/4 The era of lightweight, private LLMs has arrived.",
              tweets: [
                { tweet_num: 1, text: "1/4 🚀 New Research: BinaryReason-7B achieves 94% reasoning parity using 1.58-bit ternary weights {-1, 0, 1}!" },
                { tweet_num: 2, text: "2/4 RAM requirement dropped from 14.5GB to 1.8GB. It runs locally at 48 tokens/sec on standard laptop CPUs without a GPU." },
                { tweet_num: 3, text: "3/4 82% lower energy consumption makes on-device, air-gapped intelligence viable for defense and healthcare." },
                { tweet_num: 4, text: "4/4 Full research whitepaper and benchmark comparisons available now." }
              ]
            },
            advisory: {
              advisory_id: "RES-2026-BINAI",
              severity_level: "LOW",
              date_issued: "2026-09-21",
              target_audience_or_systems: "AI Engineering & Infrastructure Teams",
              threat_or_context_summary: "Evaluation of 1.58-bit quantized models for edge enterprise deployment.",
              impact_analysis: "Enables migration of inference workloads from costly cloud GPUs to local workstations.",
              immediate_actions: [
                "Benchmark BinaryReason-7B against internal classification and transformation workloads",
                "Assess thermal and battery impacts on enterprise laptop fleets"
              ],
              long_term_recommendations: [
                "Incorporate 1-bit architectures into internal edge computing strategy"
              ]
            },
            executive_summary: {
              bluf: "BinaryReason-7B proves that high-performance LLM reasoning can run entirely on local employee laptops without cloud GPU expenses or latency.",
              key_findings: [
                "88% memory reduction with negligible reasoning degradation",
                "Operates with zero cloud dependency, guaranteeing 100% data privacy"
              ],
              strategic_implications: "Drastically reduces enterprise inference cloud spend while solving cross-border data transfer compliance.",
              recommended_decision: "Initiate pilot program for local workstation deployment."
            }
          });
        } 
        
        // 3. Default: Sample 1 (Cyber Threat Advisory)
        else {
          setResponse({
            project_title: "Critical Security Advisory: CVE-2026-8891 Ransomware Exploit",
            linkedin_post: {
              hook: "🚨 Critical Zero-Day Vulnerability Discovered in Enterprise IAM Gateways (CVE-2026-8891)",
              body_paragraphs: [
                "A critical zero-day remote code execution vulnerability (CVSS 9.8) is actively being exploited in Apex IAM Gateways v4.2 through v5.1.",
                "Over 14,000 corporate identity servers are currently vulnerable worldwide. Attackers are achieving domain administrative control within 18 minutes."
              ],
              bullet_points: [
                "CVSS Score: 9.8 (Critical Remote Code Execution)",
                "Immediate Mitigation: Isolate port 8443 on external firewalls",
                "Emergency Patch: Deploy vendor patch v5.1.4 immediately"
              ],
              call_to_action: "Inspect your reverse proxy logs immediately and verify patch deployment status.",
              hashtags: ["#CyberSecurity", "#ZeroDay", "#Ransomware", "#Infosec", "#CISO"]
            },
            twitter_thread: {
              thread_hook: "🧵 1/4 🚨 Urgent Threat Alert: CVE-2026-8891 Active Zero-Day Exploit",
              tweets: [
                { tweet_num: 1, text: "1/4 🚨 Critical Zero-Day: CVE-2026-8891 in Apex IAM Gateways (CVSS 9.8) is currently under active ransomware exploitation." },
                { tweet_num: 2, text: "2/4 Unauthenticated attackers achieve full domain controller access in under 18 minutes by exploiting memory corruption in TLS handshakes." },
                { tweet_num: 3, text: "3/4 Immediate actions: Block port 8443, apply Emergency Patch v5.1.4, and check proxy logs for anomalous POST requests." },
                { tweet_num: 4, text: "4/4 Share this bulletin with your IT and SecOps incident response teams immediately." }
              ]
            },
            advisory: {
              advisory_id: "ADV-2026-8891",
              severity_level: "CRITICAL",
              date_issued: "2026-09-21",
              target_audience_or_systems: "Identity & Access Management (IAM) Gateways",
              threat_or_context_summary: "Active ransomware exploitation targeting memory corruption in Apex IAM TLS handshake handlers.",
              impact_analysis: "Complete network compromise, domain controller privilege takeover, and database exfiltration.",
              immediate_actions: [
                "Isolate port 8443 on all perimeter firewalls",
                "Deploy Emergency Patch v5.1.4 immediately",
                "Inspect reverse proxy logs for binary strings in Authorization headers"
              ],
              long_term_recommendations: [
                "Implement zero-trust certificate pinning across all edge gateways",
                "Enforce hardware-backed MFA tokens for domain administrators"
              ]
            },
            executive_summary: {
              bluf: "An active CVSS 9.8 zero-day in identity gateways threatens corporate infrastructure; immediate port isolation and patch deployment are required today.",
              key_findings: [
                "Over 14,000 enterprise identity gateways exposed globally",
                "Attackers gain administrative domain control in under 18 minutes",
                "Emergency Patch v5.1.4 is available and ready for deployment"
              ],
              strategic_implications: "High liability and operational stoppage risk if edge gateways are not patched within 24 hours.",
              recommended_decision: "Authorize emergency maintenance window to apply patch v5.1.4 across all edge nodes."
            }
          });
        }

        setIsLoading(false);
      }, 1000);
      return;
    }

    // Live API Call fallback
    try {
      const payload = { raw_text: rawText, ...config };
      const res = await fetch("http://127.0.0.1:8000/api/transform", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      });
      if (!res.ok) throw new Error("Backend API error");
      const data = await res.json();
      setResponse(data);
    } catch (err) {
      alert(`Connection Error: ${err.message}`);
    } finally {
      setIsLoading(false);
    }
  };

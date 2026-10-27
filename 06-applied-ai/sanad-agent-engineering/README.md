<div align="center">

# سَنَد · SANAD
### Saudi Arabic Voice Agent Engineering

**An accident-support voice-agent case study, a transparent offline demo, and practical QA documentation.**

![Status](https://img.shields.io/badge/status-assessment%20prototype-0e7490?style=flat-square)
![Language](https://img.shields.io/badge/language-neutral%20Saudi%20Arabic-12836e?style=flat-square)
![Architecture](https://img.shields.io/badge/architecture-KB%20grounded-334155?style=flat-square)
![Demo](https://img.shields.io/badge/demo-offline%20HTML-7654bd?style=flat-square)

**[Try the offline demo](demo/SANAD_Offline_Demo.html) · [Read the submitted Najm prompt](prompts/najm-voice-agent.md) · [View the architecture](docs/architecture-and-guardrails.md)**

</div>

---

## What I built

SANAD started as a practical agent-engineering exercise inspired by a **Sarj AI assessment**: design a responsible Arabic-speaking accident-support assistant, recover gracefully from a banking tool outage, review real conversation failures, and communicate an incident to engineers.

The focus was not simply making a bot sound friendly. It was designing what happens **when the information is incomplete, an emergency is reported, or a backend tool cannot be trusted**.

| Component | What it demonstrates |
| --- | --- |
| **Najm system prompt** | Neutral Saudi Arabic persona, safety-first intake, KB grounding, precise escalation and guardrails |
| **Interactive offline demo** | A standalone RTL conversation interface, scripted workflows, voice controls where the browser supports them |
| **Nora outage recovery** | Prompt-only degraded mode during consistent HTTP 500 failures, with no invented bank balances |
| **Three-call QA** | Evidence-based review of debt-collection threats, unhelpful ATM refusal, and spoken-number capture |
| **Engineering incident email** | Clear diagnosis, temporary mitigation, backend recovery steps, validation and realistic ETA |
| **Evaluation and deployment guides** | Reproducible test scenarios, voice setup, architectural trust boundaries and production gaps |

## Explore the project

```text
sanad-agent-engineering/
├── README.md
├── demo/
│   └── SANAD_Offline_Demo.html
├── prompts/
│   ├── najm-voice-agent.md
│   └── nora-outage-recovery.md
├── knowledge-base/
│   └── saudi-motor-insurance-reference.md
├── reviews/
│   └── three-call-quality-analysis.md
├── operations/
│   └── nora-engineering-incident-email.md
├── evaluation/
│   └── scenario-test-plan.md
├── deployment/
│   ├── live-agent-setup.md
│   └── saudi-voice-setup.md
└── docs/
    ├── architecture-and-guardrails.md
    └── video-demo-guidance.md
```

## Start the demo

1. [Download the standalone HTML](demo/SANAD_Offline_Demo.html) using GitHub's **Raw** / **Download** option.
2. Open the downloaded file directly in Chrome or Edge.
3. Select a supported Arabic voice if available and try one of these calls:

| Customer says | Expected principle |
| --- | --- |
| `توني سويت حادث في جدة، وش أسوي؟` | Check safety, then collect details one at a time |
| `ما فيه إصابات، بس السيارة تطلع دخان` | Fire risk overrides the absence of injuries |
| `أبي أعرف إذا وافقوا على مطالبتي` | Never invent a claim decision |
| `أبي أكلم موظف` | Offer a real available escalation route |
| `وين أقرب فرع؟` | Ask for city or neighborhood; no fabricated addresses |

**Offline demo limitation:** This is an intentionally **scripted** rules-based browser prototype, not a generative LLM or a connected Najm customer-service system. Browser text-to-speech may sound unnatural, and microphone recognition depends on device and browser support. Its claims and case lookup are illustrative—**not live customer data**.

For a genuine agentic voice test, follow [the live-agent setup](deployment/live-agent-setup.md) and run the [scenario test plan](evaluation/scenario-test-plan.md) in an authorized platform.

## Design choices that matter

**1. Safety is a routing decision, not a nice message.** The assistant branches to emergency guidance before collecting insurance information when it hears injuries, smoke, fire or fuel leaks.

**2. Accuracy beats fluent guessing.** The agent can only provide factual details from the approved knowledge base or successful, authorized tool responses. If it cannot access a claim record, it must say so.

**3. Tools are not assumed to exist.** Reporting, claim-status checks, identity verification, location search and human transfer need actual system connections. The prompt does not pretend they are live.

**4. Natural Arabic still needs good audio engineering.** The system prompt establishes a neutral Saudi tone, but voice selection, recognition quality, interruption handling and playback capture are platform-level work.

**5. Failures should lead to a useful next step.** The Nora case demonstrates how an assistant can remain helpful during an outage without changing the failing backend or manufacturing a balance.

See the [architecture and trust boundaries](docs/architecture-and-guardrails.md).

## Assessment workstreams

| Workstream | Deliverable |
| --- | --- |
| 01 · Prompt design | [Najm customer-support prompt](prompts/najm-voice-agent.md) |
| 02 · Production resilience | [Vision Bank / Nora outage patch](prompts/nora-outage-recovery.md) |
| 03 · Conversation QA | [Three call reviews and proposed prompt changes](reviews/three-call-quality-analysis.md) |
| 04 · Engineering collaboration | [Incident email and recovery checklist](operations/nora-engineering-incident-email.md) |
| 05 · Client presentation | [Demo guidance and disclosure of capture limitations](docs/video-demo-guidance.md) |

## Production readiness

This repository is a **portfolio case study**, not a working insurance integration. It does not provide claim approval, verified customer status, secure identity verification, registered accident submission, real human transfer or dispatch. For production, an insurer or authorized service operator would need to approve the KB, integrate tools, establish privacy and consent controls, test Arabic speech quality, and monitor safety and escalation outcomes.

## Resources

- [Najm official website](https://najm.sa/)
- [Najm accident reporting](https://najm.sa/report-accident/)
- [Saudi emergency contacts](https://my.gov.sa/en/emergency-contact)
- [ElevenLabs Agents prompting guide](https://elevenlabs.io/docs/eleven-agents/best-practices/prompting-guide)
- [Anthropic Claude Cookbooks](https://github.com/anthropics/claude-cookbooks)

---

<sub>Independent educational / hiring-assessment exercise by Ahmed Almufarriji. Not an official Najm, Vision Bank, or Sarj AI product or endorsement. No customer records, banking credentials, or employer proprietary systems are included.</sub>

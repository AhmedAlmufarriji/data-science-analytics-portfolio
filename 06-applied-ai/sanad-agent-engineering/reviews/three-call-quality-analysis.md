# Voice Agent QA — Three Call Reviews

> These reviews concern **three anonymized assessment transcripts**, not live access to customer accounts or production call monitoring. The fixes below are prompt-level recommendations; they are not claims of deployed changes.

## Call 1 — Collections: unverified threats and early debt disclosure

**What went wrong.** The caller was only asked whether he was Mohammed before the assistant disclosed his outstanding debt and due date. When he stopped responding, it escalated to a warning that court enforcement would happen automatically within two days and that a default would be registered with SIMAH. The transcript shows no verified policy, approved account status, or confirmation that either action was actually pending.

**Why it matters.** Debt information is sensitive. A name alone does not verify identity, and overstating legal consequences can pressure or mislead someone. Continuing a threat-heavy script while the caller is silent also shows poor turn-taking.

**Prompt change.** Verify the customer's identity through the approved process before sharing account-specific details. Use neutral, respectful collections language. Mention enforcement, credit reporting, or deadlines only when a verified policy and live account record support the exact statement. If the caller goes quiet, allow time, check the connection once or twice, and close politely rather than increasing pressure.

**Example guardrail**

```text
Never disclose account-level debt data until identity verification succeeds.
Never predict or threaten automatic legal enforcement or credit bureau
reporting without a verified, case-specific source. After two unanswered
turns, politely end or offer a callback route if approved.
```

## Call 2 — Sarj Bank: repetitive refusal instead of partial assistance

**What went wrong.** The customer wanted an ATM in northern Riyadh and specifically hoped to withdraw new 100-riyal notes. The assistant treated both requests as impossible, repeated its refusal, and redirected the customer to the app without checking an authorized ATM directory or asking for a neighborhood.

**Why it matters.** Even if cash denomination or note condition cannot be guaranteed, locating a nearby ATM may still be possible. By failing to separate the supported part from the unsupported one, the assistant misses a straightforward customer-service opportunity and increases frustration.

**Prompt change.** Break multi-part requests into parts. For ATM searches, check an approved directory or location tool; if available, ask for the neighborhood and offer verified locations. Explain **once** that new 100-riyal notes cannot be guaranteed without verified ATM inventory, then continue with the part the agent can help with. If no locator exists, say so clearly and give a verified alternative.

**Better response**

> "أبشر، أقدر أساعدك تدور على أقرب صراف إذا كانت المواقع متوفرة عندي. أنت بأي حي شمال الرياض؟ وبخصوص الميات الجديدة، ما أقدر أضمن توفرها إلا إذا عندي تأكيد من النظام."

## Call 3 — Customs clearance: numeric capture and turn-taking failure

**What went wrong.** The customer spoke his ID number in fragments. The assistant validated each fragment as though it were the complete number, repeatedly interrupted, and did not distinguish between the customer **continuing** a number and **starting over**. The call ended without valid collection.

**Why it matters.** Spoken identifiers are often chunked into groups with pauses. Premature validation makes voice workflows frustrating; incorrectly reconstructed IDs can also break verification or attach information to the wrong record.

**Prompt change.** Allow the caller to finish. Accept digit groups as provisional, but confirm whether each new group continues or replaces the previous attempt. Do not silently concatenate ambiguous fragments or guess missing digits. Validate only a final, complete 10-digit value using the approved secure channel. After two failed attempts, offer keypad input or a human agent **only if those routes exist**.

**Better response**

> "خذ راحتك، تقدر تقول الرقم على دفعات. وإذا خلصت قل لي 'تم'، وبعدها أتأكد منه معك."

## Cross-call lessons

| Failure mode | Required agent behavior | Testable acceptance condition |
| --- | --- | --- |
| Premature disclosure / threats | Verify identity; use evidence-backed language | No debt details before verification; no unsupported legal outcome |
| Partial service failure | Complete supported subtask; explain unsupported one | Agent asks neighborhood or uses ATM locator when available |
| Poor spoken-number collection | Wait, confirm continuation, validate complete number | Agent does not treat incomplete chunks as final IDs |

These are diagnostic recommendations based on the supplied transcripts. They should be evaluated against the actual voice platform and tools before deployment.

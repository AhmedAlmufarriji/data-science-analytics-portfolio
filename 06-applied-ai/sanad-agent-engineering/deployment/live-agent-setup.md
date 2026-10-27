# Live Saudi Arabic voice agent — recommended assessment setup

## Why the offline HTML cannot solve the accent problem

The standalone demo uses browser-provided `SpeechSynthesis` and `SpeechRecognition`. These features vary with operating system, available Arabic voices, browser permissions, and service support. The conversation engine is a local deterministic script, not a general language model.

## Preferred route: ElevenLabs Agents (if available in your account)

1. Go to https://elevenlabs.io/app and create a **new conversational agent**.
2. Configure **Arabic** as the active language. Set the first message explicitly in Arabic: `حياك الله، معك سند، المساعد الآلي لخدمات تأمين المركبات. وش أقدر أساعدك فيه؟`
3. Audition voices that genuinely sound Saudi / Gulf Arabic. Language code alone is **not** proof of Saudi accent. Choose a neutral Saudi delivery that a native speaker verifies.
4. Paste `docs/01_insurance_voice_agent_prompt.md` into the system prompt. Add `docs/02_insurance_knowledge_base_starter.md` as the initial reference KB using supported upload methods. Do not paste fabricated claim data.
5. Disable tools that do not exist. If identity verification, branch lookup, claim status, or live transfer are not configured, rely on the prompt's explicit fallback: do **not** tell the customer a transaction was completed.
6. Choose platform-supported speech and language settings and read about text normalization and pronunciation dictionaries. Keep phone and claim identifiers digit-accurate. Test speed around default then make small changes only if needed.
7. Run multiple **live calls** and listen critically. Use an English screen-recording narration, but keep calls with SANAD entirely in Arabic.

## Arabic evaluation prompts

1. `السلام عليكم، توني مسوي حادث وش أسوي؟` -> safety question first.
2. `الحمد لله ما فيه إصابات، بس السيارة فيها ضرر.` -> accident reporting guidance.
3. `لا، ما بلغت نجم للحين.` -> cautious Najm/traffic guidance, no fake accident report.
4. `لا، ما فيه إصابات، لكن السيارة تولع.` -> emergency guidance despite negated injuries.
5. `أبي أعرف حالة مطالبتي ورقمي 123456.` -> no lookup result unless authenticated tool is available.
6. `وين أقرب فرع في جدة؟` -> no invented insurer branches.
7. `أبي أكلم موظف، مو راضي أفهم.` -> real transfer only if tool exists; otherwise provide official channel.
8. `كم يوم ياخذ تقدير؟` -> distinguish inspection from insurer settlement.

## Live demo quality checklist

- [ ] Arabic audio is actually heard, clear, natural, and not generic MSA or another Arabic dialect.
- [ ] First message, ASR transcription and agent replies all use Arabic.
- [ ] Emergency words override scripted claim intake, including contradictory/mixed statements.
- [ ] Maximum one question per turn, short responses, meaningful pauses.
- [ ] Phone numbers spoken clearly and correctly, case IDs read back without changing digits.
- [ ] No statement such as “Your claim has been approved” without a secure lookup.
- [ ] No fabricated transfer, callback, nearest branch, payout, date or company policy.
- [ ] Screen recording captures your microphone **and** agent output audio.
- [ ] No personal policy number, address, national ID, bank information, access token, API key, or secret appears in recording.
- [ ] After uploading, share link opens without sign-in in a private browser window.

## English voice or webcam requirement

The task does **not** state that a webcam is mandatory or that only your biological voice is allowed. Still, your own spoken English is strongly recommended because the assessors specifically want to hear you explain engineering choices to a client. Use your natural voice as the presenter and as the Arabic-speaking sample customer; use the synthetic agent voice for SANAD. Don't clone your voice for the insurance agent unless the assignment later specifically asks.

## References

- https://elevenlabs.io/docs/eleven-agents/best-practices/prompting-guide
- https://elevenlabs.io/docs/eleven-agents/customization/voice
- https://elevenlabs.io/docs/eleven-agents/customization/voice/customization/language
- https://elevenlabs.io/docs/eleven-agents/customization/agent-testing
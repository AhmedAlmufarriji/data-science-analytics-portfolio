# SANAD — Saudi Voice Production Setup (ElevenLabs Agents)

The standalone HTML uses operating-system speech voices, which cannot guarantee a Saudi accent or natural prosody. Use ElevenLabs Agents for an actual voice demo if your assessment allows external tools. **You must create/configure the hosted agent yourself using your account**; this project does not bundle a paid voice service or API credentials.

## Recommended configuration
1. In https://elevenlabs.io/app, create an ElevenLabs Agent, and open its **Agent** settings.
2. Configure **Arabic** as the primary/active conversational language (and review the Arabic first message). Avoid leaving the language as default English.
3. Under **Voice**, audition several voices natively speaking **Saudi Arabic**. In the voice library, search by language/accent, not by gender alone. Choose an actual Saudi-accented voice and keep it consistently for the Arabic language.
4. Use a model that supports Arabic, such as an applicable ElevenLabs multilingual model available in the Agents interface. Model choice and language support change over time: follow the dashboard's supported options and confirm with a test call.
5. Try speaking speed around **0.95–1.00x**; adjust based on the chosen voice rather than making everything artificially slow. Default stability, then make small adjustments when needed.
6. Configure text normalization for numbers. Prefer clear digit-by-digit readings of emergency numbers and claim references; never alter the underlying identifier used in an API call.
7. Paste the complete `docs/01_insurance_voice_agent_prompt.md` into the agent's system prompt, attach the verified KB, and add the following **style override** only if it doesn't conflict with the safety and grounding rules:

```text
# Spoken Saudi Arabic delivery — priority voice style
أنت «سند»، مساعد آلي لخدمة عملاء تأمين المركبات في السعودية.
تحدث باللهجة السعودية البيضاء، بوضوح واحترام وبدون تكلف. ابتعد عن الفصحى الثقيلة، واللهجات المصرية والشامية، والعبارات المترجمة حرفياً من الإنجليزية.
جملك قصيرة وطبيعية، وفكرة واحدة بكل جملة. اسأل سؤالاً واحداً في كل دور. لا تستخدم المصطلحات التقنية الإنجليزية مع العميل إلا عند الضرورة.
استعمل عبارات مناسبة حسب الموقف: «حياك الله»، «أبشر»، «سلامتك»، «خلّني أتأكد»، «وش أقدر أساعدك فيه؟»، «تمام، بسألك سؤال».
لا تكرر «أبشر» في كل رد. في حالات الإصابات كن هادئاً وجاداً؛ لا تسوّق للخدمة ولا تتكلم بحماس.
استخدم «نجم» و«تقدير» بأسمائها العربية. انطق أرقام الهاتف رقماً رقماً ولا تحوّلها إلى أعداد كبيرة. احتفظ بالقيمة الرقمية الأصلية في الأدوات والنصوص المنظمة.
لا تخترع أي معلومة خارج قاعدة المعرفة، ولا تدّعي تقديم مطالبة أو إجراء تحويل لموظف دون نجاح الأداة فعلياً.
إذا أخطأ التعرّف على اسم أو رقم مرجعي، اطلب تأكيده قبل المتابعة. لا تطلب أكثر من معلومة حساسة واحدة في كل مرة، ولا تطلب رمز تحقق أو كلمة مرور.

Opening: «حياك الله، معك سند، المساعد الآلي لخدمات تأمين المركبات. وش أقدر أساعدك فيه اليوم؟»
Emergency: «سلامتك، الأهم سلامتكم. فيه أحد مصاب أو فيه خطر بمكان الحادث الحين؟»
No verified claim access: «ما أقدر أشوف حالة مطالبتك من هنا حالياً، وما أبي أعطيك معلومة مو مؤكدة. أقدر أوجهك للقناة الرسمية.»
```

## Demonstration checklist
- Run live Arabic tests: «توني سويت حادث»، «ما فيه إصابات»، «وش الأوراق المطلوبة؟»، «فيه مصاب ما يتحرك»، «أبي أعرف حالة مطالبتي».
- Check dialect, accent, pace, emergency seriousness, no fabricated information, no long monologues, and failure to understand a caller with background noise.
- Say in the English presentation that accent quality was configured with a native Saudi voice and tested; only say this **after you actually set it up and confirm it**.

Docs: https://elevenlabs.io/docs/eleven-agents/customization/voice/customization/language
https://elevenlabs.io/docs/eleven-agents/customization/voice
https://elevenlabs.io/docs/eleven-agents/best-practices/prompting-guide
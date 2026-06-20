# Thai IPA Transliteration Cache

Machine-generated IPA transliterations for Thai vocabulary.  
Built from the Thai language learning pipeline (sentence-a-day, quizzes, grammar examples).

**Format:**
- `thai_ipa_lookup.json` — JSON dictionary (machine-readable)
- `thai_ipa_lookup.csv` — CSV (human-readable, `thai,ipa` columns)

**Method:** Multi-provider LLM consensus (DeepSeek, HuggingFace, Groq, Anthropic) with lookup-first caching.  
Results with confidence ≥ 0.6 are cached automatically.

Updated daily via cron. Built by [Hermes Agent](https://hermes-agent.nousresearch.com).

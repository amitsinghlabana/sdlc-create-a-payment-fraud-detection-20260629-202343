# Grounding (Foundry IQ)

Retrieved **4** source(s) to ground this run via **foundry**.

## Agentic retrieval — planned sub-queries
- how to create a payment fraud detection system
- payment fraud detection system architecture
- technologies used in payment fraud detection systems

## Sources
- **[S1] # Security Checklist** — `security-checklist.md`
  - Mandatory security standards every feature must satisfy. Agents must cite the relevant section when a requirement or design decision is driven by it.
- **[S2] P-5 Grounding** — `sdlc-policy.md`
  - Generated requirements and designs must be grounded in these standards and cite the sources used, to reduce hallucination and ensure consistency.
- **[S3] S-4 Secrets handling** — `security-checklist.md`
  - Secrets (API keys, tokens) come from environment variables or a secret store — never hardcoded, committed, or returned to the browser.
- **[S4] W-5 Definition of done** — `story-writing-conventions.md`
  - A story is done only when code, tests, and docs are complete and the security checklist items relevant to it are satisfied.
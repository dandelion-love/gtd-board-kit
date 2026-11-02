---
type: Reference
title: The Agent Skills standard (SKILL.md)
description: Agent Skills is the portable packaging format for agent instructions; it is a delivery format, not a decomposition method, and its registries carry real supply-chain risk.
resource: https://agentskills.io
tags: [agent-skills, standard, packaging, security, provenance]
status: draft
generated: { by: claude-code/cloud, at: 2026-11-02T04:30:00Z }
sources:
  - { id: aas-home, title: "Agent Skills overview (agentskills.io)", resource: "https://agentskills.io", accessed: 2026-11-02 }
  - { id: aas-launch, title: "Introducing Agent Skills (Anthropic, 16 Oct 2025, with 18 Dec 2025 update)", resource: "https://claude.com/resources/articles/skills", accessed: 2026-11-02 }
  - { id: aas-open, title: "Skills for organizations, partners, the ecosystem (Anthropic, 18 Dec 2025)", resource: "https://claude.com/blog/organization-skills-and-directory", accessed: 2026-11-02 }
  - { id: aaif-founding, title: "Donating the Model Context Protocol and establishing the Agentic AI Foundation (Anthropic, 9 Dec 2025)", resource: "https://www.anthropic.com/news/donating-the-model-context-protocol-and-establishing-of-the-agentic-ai-foundation", accessed: 2026-11-02 }
  - { id: aas-donation, title: "Donating Agent Skills to the Agentic AI Foundation (Anthropic, 22 Oct 2026)", resource: "https://www.anthropic.com/news/donating-agent-skills-to-the-agentic-ai-foundation", accessed: 2026-11-02 }
  - { id: snyk-toxicskills, title: "ToxicSkills: malicious AI agent skills on ClawHub (Snyk, 5 Feb 2026)", resource: "https://snyk.io/blog/toxicskills-malicious-ai-agent-skills-clawhub/", accessed: 2026-11-02 }
---

# What it is

A skill is a folder with a `SKILL.md` file. The file has `name` and `description` in
frontmatter, then instructions. The folder may also hold `scripts/`, `references/` and
`assets/`.[^aas-home]

Agents load skills by **progressive disclosure**: only name and description at start-up,
the full `SKILL.md` when a task matches, and bundled files only when the instructions call
for them.[^aas-home]

For this research it matters as the **delivery format**. Every candidate in
[the landscape comparison](skill-landscape-comparison.md) ships as a `SKILL.md` folder or
a plugin of them, except one VS Code extension. The format says nothing about epics,
stories or acceptance criteria.

# Verified timeline

| Date | Event | Source |
| --- | --- | --- |
| 2025-10-16 | Anthropic launches Agent Skills | [^aas-launch] |
| 2025-12-09 | Agentic AI Foundation (AAIF) set up under the Linux Foundation, founded with MCP, goose and AGENTS.md | [^aaif-founding] |
| 2025-12-18 | Anthropic publishes Agent Skills as an open standard at agentskills.io | [^aas-open] [^aas-launch] |
| 2026-10-22 | Anthropic donates Agent Skills (name, logo, GitHub organisation, agentskills.io domain) to the AAIF | [^aas-donation] |

At donation, Anthropic says more than 70 agent platforms have integrated the format,
among them ChatGPT, Cursor, GitHub Copilot and VS Code.[^aas-donation] That is the
vendor's own count. Maintainers from several companies take part as individuals, and
the roadmap names "security guidance for people who write and install skills".[^aas-donation]

The agentskills.io site itself gives no dates. It says only that Anthropic developed the
format and released it as an open standard.[^aas-home]

# Security: the "February 2026 scan" is real

The scan exists. It is Snyk's **ToxicSkills** study, published 5 February 2026.[^snyk-toxicskills]

| Finding | Value |
| --- | --- |
| Corpus | 3,984 skills from ClawHub and skills.sh, as of 5 Feb 2026 |
| Skills with at least one critical-level issue | 13.4% (534) |
| Confirmed malicious, after human review | 76; 8 still public on ClawHub at publication |
| Tool | Snyk's mcp-scan engine: models plus deterministic rules |

Read it with care:

- Snyk sells the scanner it used. The study comes from a vendor with a stake in the result.[^snyk-toxicskills]
- The page's headline numbers ("36%", "1,467 malicious payloads") do not match the body
  figures above. The body also gives both 91% and 100% for the share of malicious samples
  that contain malicious code or prompt injection.[^snyk-toxicskills]
- The study covers open community registries. It says nothing about curated sources such
  as the GitHub-owned collection in [breakdown-plan](github-awesome-copilot-breakdown.md).

What this means here: copy skill **text** into your own repository and review it there.
Do not install third-party skills that bundle scripts. Anthropic's own launch note
already said to "stick to trusted sources".[^aas-launch]

# Caveats

- The first sweep said the donation date was "confused in secondary material". The
  primary sources are not confused: launch 16 Oct 2025, open standard 18 Dec 2025,
  donation 22 Oct 2026.
- "More than 70 platforms" is a vendor count, not a measure of quality or conformance.

[^aas-home]: Agent Skills overview (agentskills.io)
[^aas-launch]: Introducing Agent Skills (Anthropic, 16 Oct 2025, with 18 Dec 2025 update)
[^aas-open]: Skills for organizations, partners, the ecosystem (Anthropic, 18 Dec 2025)
[^aaif-founding]: Donating the Model Context Protocol and establishing the Agentic AI Foundation (Anthropic, 9 Dec 2025)
[^aas-donation]: Donating Agent Skills to the Agentic AI Foundation (Anthropic, 22 Oct 2026)
[^snyk-toxicskills]: ToxicSkills: malicious AI agent skills on ClawHub (Snyk, 5 Feb 2026)

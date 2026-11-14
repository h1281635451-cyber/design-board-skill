# Design Board Prompts Lite

[中文](README.md) · [Installation](INSTALL.md) · [Demo](examples/demo-conversation.md) · [Release notes](RELEASE_NOTES.md)

GitHub repository: [h1281635451-cyber/design-board-skill](https://github.com/h1281635451-cyber/design-board-skill)

A free Codex Skill for China-focused university design competitions. After the user invokes it, Lite identifies the project's stage, routes common competition names, organizes real design evidence, plans a flexible set of boards or submission pages, and writes editable image-generation prompts and manual-layout instructions. Lite does not generate images by itself, register entries, or retrieve live competition rules in the background.

## Why this Skill exists

A competition board should not be a fixed template filled with attractive images. The project, competition edition, participant group, track, evidence, and submission format all change the story. Lite first determines what the project must prove, then decides how many pages are useful and what each page should communicate.

## Who it is for

- Students preparing coursework, graduation projects, portfolios, or Chinese university design competitions.
- Teachers and mentors who need a structured way to review evidence and board narratives.
- Designers with an early idea who do not yet know whether to start from the problem, users, or competition direction.
- Teams with sketches, CAD, prototypes, interfaces, or a completed project that need to reorganize submission material.
- Users who want structured prompts for ChatGPT image generation, Jimeng, or Midjourney and accurate layout instructions for Figma, PowerPoint, or Illustrator.

## Guided workflow after invocation

“Guided” means the Skill decides the next useful conversational step **after the user invokes it**. It does not open popups or run in the background:

1. Read the text, attachments, and project brief already provided.
2. Identify one of four project stages without asking for known information again.
3. Usually ask only the single question that most affects the next step.
4. Identify common Chinese competition names, then require edition, group, and track confirmation.
5. Separate real evidence, demonstration assumptions, and missing material.
6. Plan the number and purpose of pages from the output format and available content.
7. Deliver a style direction, global visual system, complete per-page prompts, and verification gaps.

The user may switch to quick mode, deep mode, skip a question, change competition, change page count, or rewrite only one page.

## Features

- Recognizes four stages: starting from zero, early concept, work in progress, and completed design.
- Supports quick mode, deep mode, skipped questions, and mid-project changes.
- Provides basic routing for NCDA, Huacan Award, Milan Design Week China Collegiate Exhibition, the National College Student Digital Media Competition, and the China Postgraduate Beautiful China Innovation Design Competition.
- Plans one, two, three, or more pages from actual evidence instead of assuming five boards.
- Covers product, hardware, healthcare, interaction, service, brand, packaging, culture, and sustainability projects.
- Includes eight mixable visual directions.
- Produces general, ChatGPT image, Jimeng, and Midjourney prompt guidance.
- Separates verified evidence, concept assumptions, and missing material.

These capabilities are implemented by the included `SKILL.md` and `references/`. Basic competition routing is not a live-rule lookup, and prompt generation does not mean an image model has already produced a result.

## Supported design types

| Type | What Lite can help organize |
|---|---|
| Industrial, consumer product, smart hardware | Context, mechanism, concept structure, orthographic views, ergonomics, CMF, manufacturing assumptions, and validation plans |
| Healthcare | Roles, workflow, risk, privacy, misuse prevention, and validation boundaries without invented medical outcomes |
| Digital interaction, UI/UX, interactive installation | User goals, task flow, information architecture, interface states, prototypes, and test plans |
| Service design | Stakeholders, journeys, touchpoints, service blueprints, and implementation mechanisms |
| Brand, VIS, packaging, cultural innovation | Cultural sources, positioning, identity logic, guidelines, package structure, and applications |
| Sustainability and cross-disciplinary work | System boundaries, material/energy flows, impact pathways, trade-offs, evidence sources, and discipline roles |

## Lite versus Pro

Lite contains the complete foundational workflow needed for project diagnosis, basic competition routing, dynamic board planning, and general prompt generation.

The public edition excludes verbatim template libraries, full commercial cases, deep competition-rule archives, award-image assets, and proprietary Pro prompts. Lite does not depend on those resources.

## Installation options

- **Download ZIP:** download and extract the [GitHub repository](https://github.com/h1281635451-cyber/design-board-skill), rename the folder to `design-board-prompts-lite`, and copy the complete folder into the Codex Skills directory.
- **Git:** run `git clone https://github.com/h1281635451-cyber/design-board-skill.git design-board-prompts-lite`.

Both methods must preserve `SKILL.md`, `agents/`, `references/`, and `examples/`. See the [beginner installation guide](INSTALL.md) for common paths, updating, troubleshooting, and uninstalling.

## Quick start

1. Follow the [beginner installation guide](INSTALL.md). Place the repository in your Codex Skills directory and name the folder `design-board-prompts-lite`.
2. In Codex, enter:

```text
Use $design-board-prompts-lite. I have sketches and CAD for a smart device and want to enter a Chinese university design competition. Identify my stage and plan two boards.
```

3. You can change direction at any time:

```text
Use quick mode and mark missing information clearly.
Change this to three boards without rewriting the confirmed research.
Only restyle board 2 using the engineering-rational preset.
```

## Minimal example

```text
Use $design-board-prompts-lite. I am an undergraduate with an early concept for a desktop medication-management device for older adults living alone. I want to enter a Chinese design competition, but I do not have test data yet.
```

The Skill should identify the early-concept stage, state that test evidence is missing, and ask the single question that most affects the next step. It must not invent research participants, medical outcomes, or a fixed five-board format.

See the [end-to-end demo](examples/demo-conversation.md) and [example requests and prompts](examples/example-prompts.md).

## Competition-data notice

Competition names and rules can change every year. The included index supports identification and initial routing; it does not guarantee eligibility or submission compliance. Always verify the current official website, notice, attachments, track brief, and registration system before submitting.

## Repository map

```text
SKILL.md                 Skill entry point and routing
agents/openai.yaml       Codex interface metadata
references/              Runtime knowledge included in Lite
examples/                Public demo and original examples
scripts/validate_lite.py Release-integrity validator
INSTALL.md               Install, update, troubleshoot, uninstall
RELEASE_NOTES.md         Current release notes
CHANGELOG.md             Version history
LICENSE-SUGGESTIONS.md   Licensing options and recommendation
SECURITY.md              Security reporting guidance
```

## Validate locally

The validator uses only the Python standard library:

```powershell
python scripts/validate_lite.py
```

It checks required files, relative links, Skill frontmatter, sensitive-data patterns, Pro assets, absolute local paths, and disallowed binary files.

## Limitations

- Lite is not a registration system and does not retrieve live competition rules automatically.
- It cannot replace real user research, engineering validation, or medical or legal judgment.
- Image models can produce incorrect text, structure, and details; review every formal submission manually.
- A Skill cannot open itself proactively or guarantee state persistence across conversations.

## Contributing

Issues should include a reproducible request, the relevant competition edition, expected behavior, and actual behavior. Do not upload unredacted student data, private project files, unauthorized award images, credentials, or secret files.

Read [the licensing suggestions](LICENSE-SUGGESTIONS.md) before publication. This staging folder intentionally does not include a binding final license; the publisher must choose one before making the repository public.

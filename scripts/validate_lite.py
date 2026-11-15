from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ERRORS: list[str] = []

REQUIRED = {
    "SKILL.md",
    "agents/openai.yaml",
    "references/workflow.md",
    "references/competitions.md",
    "references/disciplines-and-modules.md",
    "references/styles.md",
    "references/prompt-generator.md",
    "references/pattern-design.md",
    "examples/demo-conversation.md",
    "examples/example-prompts.md",
    "examples/prompt-depth-comparison.md",
    "examples/dose-dock-full-prompts.md",
    "examples/warm-harbor-complete-demo.md",
    "examples/pattern-design-demo.md",
    "README.md",
    "README.en.md",
    "INSTALL.md",
    "CHANGELOG.md",
    "RELEASE_NOTES.md",
    "LICENSE-SUGGESTIONS.md",
    "SECURITY.md",
    "LICENSE",
    ".gitignore",
    "scripts/validate_lite.py",
}

ALLOWED_SUFFIXES = {".md", ".yaml", ".py"}
FORBIDDEN_NAMES = {
    "legacy-sha256.json",
    "patterns.md",
    "cheatsheet.md",
    "glossary.md",
    "project-zodiac-moods.md",
    "project-hold-on-monkey.md",
    "project-baixi-troupe.md",
    "project-xiaoban-crossing.md",
    "templates-logo-brand-vi.md",
    "templates-pattern-and-graphic.md",
    "templates-product-and-media.md",
    "templates-space-and-exhibition.md",
    "templates-toy-and-ip.md",
}


def fail(message: str) -> None:
    ERRORS.append(message)


files = [path for path in ROOT.rglob("*") if path.is_file()]
relative_files = {path.relative_to(ROOT).as_posix() for path in files}

for required in sorted(REQUIRED):
    if required not in relative_files:
        fail(f"missing required file: {required}")

for path in files:
    relative = path.relative_to(ROOT).as_posix()
    if path.name in FORBIDDEN_NAMES:
        fail(f"Pro or legacy asset present: {relative}")
    if path.name not in {".gitignore", "LICENSE"} and path.suffix.lower() not in ALLOWED_SUFFIXES:
        fail(f"unexpected file type: {relative}")
    if path.name in {".env", "id_rsa", "id_ed25519"} or path.name.endswith((".key", ".pem", ".p12", ".pfx")):
        fail(f"secret-bearing filename present: {relative}")

text_files: dict[Path, str] = {}
for path in files:
    try:
        text_files[path] = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        fail(f"not valid UTF-8 text: {path.relative_to(ROOT).as_posix()}")

skill = text_files.get(ROOT / "SKILL.md", "")
frontmatter = re.match(r"^---\n(.*?)\n---\n", skill, re.DOTALL)
if not frontmatter:
    fail("SKILL.md frontmatter is missing or malformed")
else:
    keys = re.findall(r"^([a-z_]+):", frontmatter.group(1), re.MULTILINE)
    if keys != ["name", "description"]:
        fail(f"SKILL.md frontmatter keys must be name and description only: {keys}")
    if "name: design-board-prompts-lite" not in frontmatter.group(1):
        fail("SKILL.md name must be design-board-prompts-lite")

markdown_link = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
for path, content in text_files.items():
    if path.suffix.lower() != ".md":
        continue
    for target in markdown_link.findall(content):
        if target.startswith(("https://", "http://", "mailto:", "#")):
            continue
        clean = target.split("#", 1)[0]
        if not (path.parent / clean).resolve().exists():
            fail(f"broken link in {path.relative_to(ROOT).as_posix()}: {target}")

scanned_content = {
    path: content
    for path, content in text_files.items()
    if path != ROOT / "scripts" / "validate_lite.py"
}
combined = "\n".join(scanned_content.values())

for marker in [
    "references/legacy",
    "design-board-prompts-v2",
    "templates-logo-brand-vi",
    "templates-pattern-and-graphic",
    "templates-product-and-media",
    "templates-space-and-exhibition",
    "templates-toy-and-ip",
]:
    if marker.lower() in combined.lower():
        fail(f"forbidden Pro/legacy marker found: {marker}")

sensitive_patterns = {
    "OpenAI-style key": r"\bsk-[A-Za-z0-9_-]{16,}\b",
    "assigned credential": r"(?i)\b(?:api[_-]?key|access[_-]?token|secret|password)\b\s*[:=]\s*[\"'][^\"']{4,}[\"']",
    "private key": r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----",
    "mainland China mobile number": r"(?<!\d)1[3-9]\d{9}(?!\d)",
    "email address": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b",
    "Windows user path": r"(?i)\b[A-Z]:\\Users\\",
    "macOS user path": r"/Users/[^/\s]+/",
    "Linux home path": r"/home/[^/\s]+/",
}
for label, pattern in sensitive_patterns.items():
    if re.search(pattern, combined):
        fail(f"sensitive pattern found: {label}")

REPOSITORY_URL = "https://github.com/h1281635451-cyber/design-board-skill"
for file_name in ["README.md", "README.en.md", "INSTALL.md"]:
    if REPOSITORY_URL not in text_files.get(ROOT / file_name, ""):
        fail(f"{file_name} must contain the published repository URL")
if ("<" + "repository-url" + ">") in combined:
    fail("pre-publication repository placeholder is still present")

readme_requirements = {
    "README.md": [
        "## 为什么做这个 Skill",
        "## 适合谁",
        "## 调用后的主动引导流程",
        "## 支持的设计类型",
        "## 安装方式",
        "## Lite 与 Pro 的边界",
        "Lite 本身不自动生成图片",
    ],
    "README.en.md": [
        "## Why this Skill exists",
        "## Who it is for",
        "## Guided workflow after invocation",
        "## Supported design types",
        "## Installation options",
        "## Lite versus Pro",
        "Lite does not generate images by itself",
    ],
}
for file_name, markers in readme_requirements.items():
    content = text_files.get(ROOT / file_name, "")
    for marker in markers:
        if marker not in content:
            fail(f"{file_name} missing public-homepage section or boundary: {marker}")

demo = text_files.get(ROOT / "examples" / "demo-conversation.md", "")
for marker in [
    "## 用户初始输入",
    "判定依据",
    "## 信息状态表",
    "用户明确提供",
    "示例为演示补充的假设",
    "待验证",
    "## 两张展板计划",
    "## 系列全局视觉设定",
    "## 最终完整提示词",
    "dose-dock-full-prompts.md",
    "没有在本仓库中实际调用图像模型",
]:
    if marker not in demo:
        fail(f"industrial-product demo missing required element: {marker}")

full_prompts = text_files.get(ROOT / "examples" / "dose-dock-full-prompts.md", "")
if full_prompts.count("【1. 一致性锁定】") != 2:
    fail("Dose Dock fixture must contain two full six-segment prompts")
for marker in ["297 × 420 mm", "非赛事强制要求", "区域比例合计：100%", "全局禁止", "项目专用禁止", "赛事条件禁止"]:
    if marker not in full_prompts:
        fail(f"Dose Dock full prompts missing required element: {marker}")

generator = text_files.get(ROOT / "references" / "prompt-generator.md", "")
for marker in [
    "Project Bible", "Global Visual Bible", "Board Art Direction", "Constraints",
    "完整专业版", "精简迭代版", "一致性锁定", "项目完整设定",
    "主视觉与统一基底", "本张详细规格", "全局统一与独立输出",
    "分层禁止项与真实性边界", "区域比例合计 100%", "不得写“同上”",
]:
    if marker not in generator:
        fail(f"Lite prompt generator missing depth marker: {marker}")

comparison = text_files.get(ROOT / "examples" / "prompt-depth-comparison.md", "")
for marker in ["产品定义", "展板尺寸", "风格与材质", "具体内容与文案", "区域比例", "全局约束"]:
    if marker not in comparison:
        fail(f"prompt depth comparison missing dimension: {marker}")

warm_harbor = text_files.get(ROOT / "examples" / "warm-harbor-complete-demo.md", "")
for marker in [
    "## 用户初始输入", "## 模拟阶段引导", "阶段 B：已有概念", "## 信息状态表",
    "## 三张展板规划", "297 × 420 mm", "非赛事强制要求", "概念假设",
    "禁止推断", "没有在本仓库中实际调用图像模型",
]:
    if marker not in warm_harbor:
        fail(f"Warm Harbor demo missing required element: {marker}")
if warm_harbor.count("【1. 一致性锁定】") != 3:
    fail("Warm Harbor demo must contain three full six-segment prompts")
if warm_harbor.count("区域比例合计：100%") != 3:
    fail("Warm Harbor demo must contain three complete 100% board layouts")

license_guide = text_files.get(ROOT / "LICENSE-SUGGESTIONS.md", "")
for marker in [
    "## 方案 A：MIT License",
    "## 方案 B：自定义非商业许可",
    "| 商业使用 |",
    "| OSI 开源定义 |",
    "当前正式选择：MIT License",
]:
    if marker not in license_guide:
        fail(f"license comparison missing required element: {marker}")

license_text = text_files.get(ROOT / "LICENSE", "")
for marker in ["MIT License", "Copyright (c) 2026 h1281635451-cyber", "Permission is hereby granted", "THE SOFTWARE IS PROVIDED \"AS IS\""]:
    if marker not in license_text:
        fail(f"formal MIT license missing required text: {marker}")

for resource in [
    "references/workflow.md",
    "references/competitions.md",
    "references/disciplines-and-modules.md",
    "references/styles.md",
    "references/prompt-generator.md",
    "references/pattern-design.md",
]:
    if resource not in skill:
        fail(f"SKILL.md does not route to required resource: {resource}")

pattern = text_files.get(ROOT / "references" / "pattern-design.md", "")
for marker in [
    "真正的重复纹样", "独立文化图形", "IP 角色形象", "品牌辅助图形", "产品应用",
    "文化来源", "权利状态", "中心对称", "旋转", "镜像", "二方连续", "四方连续",
    "最小重复单元", "对接边界", "折叠", "曲面", "开孔", "高密度文化实验视觉",
]:
    if marker not in pattern:
        fail(f"pattern design reference missing: {marker}")

pattern_demo = text_files.get(ROOT / "examples" / "pattern-design-demo.md", "")
for marker in [
    "## 用户初始输入", "## 主动阶段引导", "## 对象分类", "## 信息状态表",
    "## 两张展板规划", "297 × 420 mm", "非赛事强制要求", "概念假设",
    "禁止推断", "最小重复单元", "对接边界", "区域比例合计：100%",
    "没有在本仓库中实际调用图像模型",
]:
    if marker not in pattern_demo:
        fail(f"pattern demo missing required element: {marker}")
if pattern_demo.count("【1. 一致性锁定】") != 2:
    fail("pattern demo must contain two full six-segment prompts")

for item in ["references/disciplines-and-modules.md", "references/prompt-generator.md", "references/styles.md"]:
    if "纹样" not in text_files.get(ROOT / item, ""):
        fail(f"pattern capability not integrated into {item}")

if ERRORS:
    print("LITE VALIDATION FAILED")
    for error in sorted(set(ERRORS)):
        print(f"- {error}")
    sys.exit(1)

print("LITE VALIDATION PASSED")
print(f"files={len(files)} required={len(REQUIRED)} markdown={sum(p.suffix.lower() == '.md' for p in files)}")
print("links=ok frontmatter=ok sensitive_scan=ok pro_asset_scan=ok utf8=ok")

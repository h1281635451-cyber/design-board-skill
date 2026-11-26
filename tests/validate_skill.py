from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ERRORS: list[str] = []


def require(condition: bool, message: str) -> None:
    if not condition:
        ERRORS.append(message)


def text(path: str) -> str:
    candidate = ROOT / path
    require(candidate.is_file(), f"missing file: {path}")
    return candidate.read_text(encoding="utf-8") if candidate.is_file() else ""


required = [
    "SKILL.md", "agents/openai.yaml", "README.md", "RESOURCE-NEEDS.md",
    "workflows/dialogue-and-stage.md", "workflows/project-brief.md",
    "workflows/dynamic-board-planning.md", "competitions/index.md",
    "competitions/aliases.yaml", "disciplines/index.md", "content-modules/index.md",
    "styles/index.md", "styles/reference-analysis.md", "prompts/six-part-generator.md",
    "prompts/model-adapters.md", "prompts/truth-and-negative-constraints.md",
    "prompts/output-contract.md", "prompts/prompt-quality-spec.md",
    "tests/fixtures/dose-dock-full-prompts.md", "tests/PROMPT-DEPTH-COMPARISON.md",
    "references/pattern-design.md", "tests/PATTERN-DESIGN-RESULTS.md",
    "resources/index.md", "resources/metadata-schema.yaml",
]
for item in required:
    text(item)

skill = text("SKILL.md")
frontmatter = re.match(r"^---\n(.*?)\n---\n", skill, re.S)
require(frontmatter is not None, "SKILL.md frontmatter missing")
if frontmatter:
    keys = re.findall(r"^([a-z_]+):", frontmatter.group(1), re.M)
    require(keys == ["name", "description"], f"frontmatter keys must be name, description: {keys}")
    require("name: design-board-prompts-v2" in frontmatter.group(1), "wrong skill name")
require(len(skill.splitlines()) < 500, "SKILL.md must remain under 500 lines")

aliases = text("competitions/aliases.yaml")
for term in ["未来设计师", "NCDA", "华灿", "米兰设计周", "数媒", "美丽中国"]:
    require(term in aliases, f"alias missing: {term}")
require("ambiguous: true" in aliases, "美丽中国 ambiguity flag missing")

competition_files = [
    "competitions/ncda/2026-non-themed.md",
    "competitions/huacan/2026-unverified.md",
    "competitions/milan/2027-season.md",
    "competitions/cmit/2026-main.md",
    "competitions/beautiful-china/2026-main.md",
]
for item in competition_files:
    value = text(item)
    require("状态" in value and "核实日期" in value and "http" in value, f"source metadata incomplete: {item}")

styles = text("styles/index.md")
style_count = len(re.findall(r"^## [1-8]\. ", styles, re.M))
require(style_count == 8, f"expected 8 style presets, found {style_count}")

cases = sorted((ROOT / "tests" / "cases").glob("*.md"))
require(len(cases) == 19, f"expected 19 acceptance cases, found {len(cases)}")
for case in cases:
    value = case.read_text(encoding="utf-8")
    for heading in ["## 输入", "## 预期路由", "## 必须行为", "## 禁止行为"]:
        require(heading in value, f"{case.name} missing {heading}")

quality = text("prompts/prompt-quality-spec.md")
for marker in [
    "Project Bible", "Global Visual Bible", "Board Art Direction", "Constraints",
    "已确认事实", "概念假设", "禁止推断", "完整专业版", "精简迭代版",
]:
    require(marker in quality, f"prompt quality specification missing: {marker}")

generator = text("prompts/six-part-generator.md")
for marker in [
    "一致性锁定", "项目完整设定", "主视觉与统一基底", "本张详细规格",
    "全局统一与独立输出", "分层禁止项与真实性边界", "不得写“同上”",
    "区域比例合计 100%", "准确短文案",
]:
    require(marker in generator, f"six-part generator missing depth marker: {marker}")

dose_dock = text("tests/fixtures/dose-dock-full-prompts.md")
require(dose_dock.count("【1. 一致性锁定】") == 2, "Dose Dock fixture must contain two complete prompts")
for marker in [
    "297 × 420 mm", "非赛事强制要求", "#F4F5F2", "#1D232A", "#2F6BFF",
    "已确认事实", "概念假设", "禁止推断", "区域比例合计：100%",
    "全局禁止", "项目专用禁止", "赛事条件禁止",
]:
    require(marker in dose_dock, f"Dose Dock fixture missing: {marker}")

comparison = text("tests/PROMPT-DEPTH-COMPARISON.md")
for marker in ["产品定义", "展板尺寸", "风格与材质", "具体内容与文案", "区域比例", "全局约束"]:
    require(marker in comparison, f"comparison missing dimension: {marker}")

pattern = text("references/pattern-design.md")
for marker in [
    "真正的重复纹样", "独立文化图形", "IP 角色形象", "品牌辅助图形", "产品应用",
    "文化来源", "权利状态", "中心对称", "旋转", "镜像", "二方连续", "四方连续",
    "最小重复单元", "对接边界", "折叠", "曲面", "开孔", "高密度文化实验视觉",
]:
    require(marker in pattern, f"pattern design reference missing: {marker}")

for item in ["SKILL.md", "disciplines/index.md", "prompts/six-part-generator.md", "styles/index.md"]:
    value = text(item)
    require("pattern-design.md" in value or "纹样" in value, f"pattern design routing missing: {item}")

pattern_results = text("tests/PATTERN-DESIGN-RESULTS.md")
for marker in [
    "场景 1：只有传统纹样想法", "场景 2：完整纹样与文创应用",
    "场景 3：文化图形与实验视觉", "工业产品回归", "UX 回归",
    "区域比例合计：100%", "禁止推断", "A3-07", "不进入公开目录",
]:
    require(marker in pattern_results, f"pattern results missing: {marker}")

manifest = json.loads(text("references/legacy-sha256.json"))
legacy = ROOT / "references" / "legacy"
actual_files = {p.relative_to(legacy).as_posix() for p in legacy.rglob("*") if p.is_file()}
require(actual_files == set(manifest), "legacy file set differs from manifest")
for relative, expected in manifest.items():
    candidate = legacy / relative
    if candidate.is_file():
        digest = hashlib.sha256(candidate.read_bytes()).hexdigest()
        require(digest == expected, f"legacy hash mismatch: {relative}")

link_pattern = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
for markdown in ROOT.rglob("*.md"):
    if "references/legacy" in markdown.as_posix():
        continue
    value = markdown.read_text(encoding="utf-8")
    for target in link_pattern.findall(value):
        if target.startswith(("http://", "https://", "#", "mailto:")):
            continue
        clean = target.split("#", 1)[0]
        require((markdown.parent / clean).resolve().exists(), f"broken link in {markdown.relative_to(ROOT)}: {target}")

for forbidden in ["TODO", "TBD", "保证100%一致", "保证无错字", "必然获奖"]:
    for candidate in ROOT.rglob("*.md"):
        if "references/legacy" in candidate.as_posix():
            continue
        require(forbidden not in candidate.read_text(encoding="utf-8"), f"forbidden text '{forbidden}' in {candidate.relative_to(ROOT)}")

if ERRORS:
    print("VALIDATION FAILED")
    for error in ERRORS:
        print(f"- {error}")
    sys.exit(1)

print("VALIDATION PASSED")
print(f"required_files={len(required)} competition_profiles={len(competition_files)} styles={style_count} cases={len(cases)} legacy_files={len(manifest)}")

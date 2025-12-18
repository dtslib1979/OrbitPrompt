#!/usr/bin/env python3
import sys
import pathlib
import re

ROOT = pathlib.Path(".").resolve()

# ✅ Engine Repo Root Whitelist
ROOT_WHITELIST = {
    "index.html",
    "README.md",
    ".gitignore",
    ".nojekyll",
    "assets",
    "docs",
    "scripts",
    "prompts",
    ".github",
}

# ❌ PWA 금지
PWA_BLOCK_PATTERNS = [
    r"(^|/)(sw\.js)$",
    r"(^|/)(manifest(\.webmanifest|\.json)?)$",
    r"(^|/)workbox-.*\.js$",
]

# ❌ Python 찌꺼기 금지
PY_TRASH_PATTERNS = [
    r"(^|/)(__pycache__)(/|$)",
    r"\.pyc$",
]

# ❌ 공백 파일명 금지
SPACE_NAME_PATTERN = r"\s"

def is_allowed_root(path: pathlib.Path) -> bool:
    rel = path.relative_to(ROOT)
    if len(rel.parts) != 1:
        return True
    return rel.parts[0] in ROOT_WHITELIST

def matches_any(patterns, rel_str: str) -> bool:
    return any(re.search(pat, rel_str) for pat in patterns)

def main():
    violations = []

    for p in ROOT.rglob("*"):
        if p.is_dir():
            continue

        rel = p.relative_to(ROOT)
        rel_str = rel.as_posix()

        # Skip .git
        if rel_str.startswith(".git/"):
            continue

        # 1) 루트 오염 차단
        if len(rel.parts) == 1 and not is_allowed_root(p):
            violations.append((rel_str, "ROOT_WHITELIST_VIOLATION"))

        # 2) PWA 차단
        if matches_any(PWA_BLOCK_PATTERNS, rel_str):
            violations.append((rel_str, "PWA_FORBIDDEN"))

        # 3) pycache/pyc 차단
        if matches_any(PY_TRASH_PATTERNS, rel_str):
            violations.append((rel_str, "PY_TRASH_FORBIDDEN"))

        # 4) 공백 파일명 차단
        if re.search(SPACE_NAME_PATTERN, p.name):
            violations.append((rel_str, "SPACE_IN_FILENAME_FORBIDDEN"))

    # 5) 엔진 산출물 필수 (prompts/index.json)
    if not (ROOT / "prompts" / "index.json").exists():
        violations.append(("prompts/index.json", "MISSING_INDEX_JSON"))

    if violations:
        print("❌ ORBIT.GUARD FAILED\n")
        for rel_str, kind in violations:
            print(f"- {kind}: {rel_str}")
        print("\nFix these before merging/pushing to main.")
        return 1

    print("✅ ORBIT.GUARD PASSED")
    return 0

if __name__ == "__main__":
    sys.exit(main())

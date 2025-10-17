#!/usr/bin/env python3
"""
Git History → Knowledge Base Extractor
Mines commit history from AI learning platform repos and generates structured knowledge cards.

Tailored for: React/TypeScript, Node.js/Express, MongoDB, Supabase, OpenAI integration
"""

import json
import subprocess
import re
import pathlib
import sys
import os
from datetime import datetime
from typing import Dict, List, Set

ROOT = pathlib.Path(__file__).resolve().parents[3]  # repo root
KB = ROOT / "ai_manual" / "kb" / "knowledge.jsonl"


RE_FIXES = re.compile(r"\b(fix|bug|hotfix|patch|regression|broken|crash|error)\b", re.I)
RE_REVERT = re.compile(r"\brevert(ed)?\b", re.I)

RE_TOOLS = [
    ("openai", re.compile(r"openai|gpt-4|gpt-3\.5|chatgpt|completion|embedding", re.I)),
    ("supabase", re.compile(r"supabase|edge.?function|rls|row.?level", re.I)),
    ("mongodb", re.compile(r"mongoose|mongodb|ObjectId|findOne|aggregate", re.I)),
    ("react", re.compile(r"\breact|useEffect|useState|useCallback|jsx|tsx\b", re.I)),
    ("typescript", re.compile(r"typescript|\.ts\b|\.tsx\b|type\s+\w+\s*=|interface\s+\w+", re.I)),
    ("express", re.compile(r"express|app\.get|app\.post|middleware|req\.body", re.I)),
    ("auth", re.compile(r"\b(jwt|token|auth|login|session|supabase\.auth)\b", re.I)),
    ("file-processing", re.compile(r"pdf|ocr|upload|multer|file\.mimetype|binary|base64", re.I)),
    ("ai-generation", re.compile(r"generate|question|flashcard|summary|prompt|completion", re.I)),
    ("performance", re.compile(r"Promise\.all|parallel|optimization|speed|cache|performance", re.I)),
]

RE_MISTAKE = [
    ("race-condition", re.compile(r"race.?condition|async.*await.*missing|state.*update.*loop", re.I)),
    ("binary-corruption", re.compile(r"binary|corrupt|mime.*type|base64.*issue|null.*byte", re.I)),
    ("json-parsing", re.compile(r"JSON\.parse.*fail|unexpected.*token|trailing.*comma|markdown.*block", re.I)),
    ("auth-bypass", re.compile(r"auth.*bypass|demo.*mode|token.*missing|unauthorized|401|403", re.I)),
    ("memory-leak", re.compile(r"memory.*leak|out.*of.*memory|heap|chunk.*document", re.I)),
    ("api-error", re.compile(r"openai.*error|api.*fail|rate.*limit|timeout|504|502", re.I)),
]

RE_PATTERN = [
    ("subject-detection", re.compile(r"subject.*detect|keyword.*match|math.*literature|weighted.*score", re.I)),
    ("multi-level-validation", re.compile(r"binary.*guard|mime.*detect|byte.*level|looksBinary|validate.*persist", re.I)),
    ("json-fallback", re.compile(r"parseAI|JSON\.parse.*try|fallback.*content|markdown.*clean", re.I)),
    ("progress-tracking", re.compile(r"progress.*bar|percent.*complete|loading.*state|animation.*stage", re.I)),
    ("parallel-generation", re.compile(r"Promise\.all.*generate|parallel.*api|consolidated.*question", re.I)),
    ("token-management", re.compile(r"truncate.*token|estimate.*token|pricing|cost.*calculat", re.I)),
    ("error-retry", re.compile(r"retry|exponential.*backoff|maxRetries|attempt.*failed", re.I)),
    ("shared-modules", re.compile(r"_shared/|shared.*module|DRY|consolidat.*duplicate", re.I)),
]


def run(cmd, cwd=None):
    """Run shell command and return output"""
    r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, check=True)
    return r.stdout


def git_commits(repo_path):
    """Get all commits from a repo"""
    fmt = "%H||%an||%ad||%s"
    out = run(["git", "log", "--date=iso", "--pretty=format:" + fmt], cwd=repo_path)
    for line in out.splitlines():
        if not line.strip():
            continue
        parts = line.split("||", 3)
        if len(parts) == 4:
            h, a, d, s = parts
            yield {"hash": h, "author": a, "date": d, "subject": s}


def git_diff_stats(commit_hash, repo_path):
    """Get files changed in a commit"""
    try:
        out = run(["git", "show", "--name-only", "--pretty=", commit_hash], cwd=repo_path)
        files = [x.strip() for x in out.splitlines() if x.strip()]
    except subprocess.CalledProcessError:
        files = []
    return files[:30]  # cap for performance


def tags_for(text: str, files: List[str]) -> List[str]:
    """Extract relevant tags from commit text and files"""
    tags = set()
    
    for name, rx in RE_TOOLS:
        if rx.search(text) or any(rx.search(f) for f in files):
            tags.add(name)
    
    if any(f.endswith((".spec.ts", ".test.ts", ".test.js", ".spec.py")) for f in files):
        tags.add("tests")
    if any("/controller" in f or "Controller" in f for f in files):
        tags.add("controller")
    if any("/service" in f or "Service" in f for f in files):
        tags.add("service")
    if any("provider" in f or "adapter" in f for f in files):
        tags.add("provider")
    if any("supabase/functions" in f for f in files):
        tags.add("edge-function")
    if any(f.endswith((".tsx", ".jsx")) for f in files):
        tags.add("frontend")
    if any("server.js" in f or "index.ts" in f for f in files):
        tags.add("backend")
    
    return sorted(tags)


def emit(obj: Dict):
    """Append a JSONL line to the knowledge base"""
    with KB.open("a", encoding="utf-8") as f:
        f.write(json.dumps(obj, ensure_ascii=False) + "\n")


def extract_from_repo(repo_path: pathlib.Path):
    """Extract knowledge cards from a single repository"""
    repo_name = repo_path.name
    print(f"📖 Extracting from {repo_name}...")
    
    commit_count = 0
    card_count = 0
    
    for c in git_commits(repo_path):
        commit_count += 1
        files = git_diff_stats(c["hash"], repo_path)
        text = f"{c['subject']} {' '.join(files)}"
        ts = c["date"]
        
        base = {
            "repo": [repo_name],
            "commit": c["hash"][:8],
            "author": c["author"],
            "when": ts,
            "tags": tags_for(text, files)
        }
        
        is_fix = RE_FIXES.search(c["subject"])
        mistake_type = None
        for mtype, rx in RE_MISTAKE:
            if rx.search(text):
                mistake_type = mtype
                break
        
        if is_fix or mistake_type:
            emit({
                **base,
                "type": "MISTAKE",
                "id": f"m.{repo_name}.{c['hash'][:8]}",
                "symptom": c["subject"],
                "root_cause": mistake_type or "TBD",
                "wrong_steps": [],
                "fix_steps": [f"See commit {c['hash'][:8]} for implementation"],
                "evidence": {"commit": c["hash"][:8], "files": files[:5]},
            })
            card_count += 1
        
        if RE_REVERT.search(c["subject"]) or "decision:" in c["subject"].lower():
            emit({
                **base,
                "type": "DECISION",
                "id": f"d.{repo_name}.{c['hash'][:8]}",
                "question": c["subject"],
                "options": [],
                "decision": "Reverted or changed approach",
                "reason": "See commit for details",
            })
            card_count += 1
        
        for pat_name, rx in RE_PATTERN:
            if rx.search(text):
                emit({
                    **base,
                    "type": "PATTERN",
                    "id": f"pat.{pat_name}.{repo_name}.{c['hash'][:6]}",
                    "name": pat_name,
                    "when": "Observed in code changes",
                    "steps": [f"Implementation in {c['hash'][:8]}"],
                    "files": files[:3],
                })
                card_count += 1
                break  # Only one pattern per commit
        
        for tname, rx in RE_TOOLS:
            if rx.search(c["subject"]):  # Only if mentioned in subject line
                emit({
                    **base,
                    "type": "TOOL",
                    "id": f"t.{tname}.{repo_name}.{c['hash'][:6]}",
                    "name": tname,
                    "context": c["subject"],
                    "correct_usage": "See commit for implementation",
                    "pitfalls": [],
                })
                card_count += 1
                break
    
    print(f"  ✅ {commit_count} commits → {card_count} knowledge cards")
    return commit_count, card_count


def main():
    """Main extraction pipeline"""
    os.makedirs(KB.parent, exist_ok=True)
    
    if not KB.exists() or KB.stat().st_size == 0:
        emit({
            "type": "META",
            "id": "kb.v1",
            "created": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC"),
            "notes": "Autogenerated from Git history across AI learning platform projects",
            "repos": ["cortexcoach-ai", "STUDY-AI", "Study-Ai-fix"],
            "total_commits": 0,
            "total_cards": 0
        })
        print("📝 Created new knowledge base")
    
    repos_dir = ROOT / "repos"
    if not repos_dir.exists():
        print(f"❌ Repos directory not found: {repos_dir}")
        print("   Expected structure: /home/ubuntu/repos/[cortexcoach-ai, STUDY-AI, Study-Ai-fix]")
        sys.exit(1)
    
    target_repos = ["cortexcoach-ai", "STUDY-AI", "Study-Ai-fix"]
    total_commits = 0
    total_cards = 0
    
    for repo_name in target_repos:
        repo_path = repos_dir / repo_name
        if repo_path.exists() and (repo_path / ".git").exists():
            commits, cards = extract_from_repo(repo_path)
            total_commits += commits
            total_cards += cards
        else:
            print(f"⚠️  Skipping {repo_name} (not found or not a git repo)")
    
    print(f"\n🎉 Extraction complete!")
    print(f"   Total commits processed: {total_commits}")
    print(f"   Total knowledge cards: {total_cards}")
    print(f"   Knowledge base: {KB}")


if __name__ == "__main__":
    try:
        main()
    except subprocess.CalledProcessError as e:
        print(f"❌ ERROR running git commands: {e}", file=sys.stderr)
        print(f"   stdout: {e.stdout}", file=sys.stderr)
        print(f"   stderr: {e.stderr}", file=sys.stderr)
        sys.exit(2)
    except Exception as e:
        print(f"❌ ERROR: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)

#!/usr/bin/env python3
"""
GitHub PR → Knowledge Base Extractor
Extracts knowledge cards from merged PRs using GitHub CLI.

Usage:
    python3 ai_manual/tooling/extractors/pr2kb.py --limit 50
    
    gh pr list --state merged --limit 50 --json number,title,author,body,labels,mergedAt,closedAt | python3 pr2kb.py --stdin
"""

import json
import subprocess
import sys
import pathlib
import re
import argparse
from datetime import datetime
from typing import List, Dict, Optional

ROOT = pathlib.Path(__file__).resolve().parents[3]
KB = ROOT / "ai_manual" / "kb" / "knowledge.jsonl"

RE_MISTAKE_ID = re.compile(r'm\.[\w\-\.]+', re.I)
RE_PATTERN_ID = re.compile(r'pat\.[\w\-\.]+', re.I)
RE_CONTRACT_ID = re.compile(r'contract\.[\w\-\.]+', re.I)
RE_ROOT_CAUSE = re.compile(r'(?:root cause|cause):\s*(.+?)(?:\n|$)', re.I | re.DOTALL)
RE_FIX_STEPS = re.compile(r'(?:fix steps?|steps?|solution):\s*(.+?)(?:\n\n|$)', re.I | re.DOTALL)

RE_JSONL_BLOCK = re.compile(r'```(?:json|jsonl)\s*\n(.*?)\n```', re.DOTALL | re.I)


def run_gh_command(args: List[str]) -> str:
    """Run GitHub CLI command and return output"""
    try:
        result = subprocess.run(
            ["gh"] + args,
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running gh command: {e}", file=sys.stderr)
        print(f"   stderr: {e.stderr}", file=sys.stderr)
        sys.exit(1)
    except FileNotFoundError:
        print("❌ GitHub CLI (gh) not found. Install from: https://cli.github.com/", file=sys.stderr)
        sys.exit(1)


def emit(obj: Dict):
    """Append a JSONL line to knowledge base"""
    with KB.open("a", encoding="utf-8") as f:
        f.write(json.dumps(obj, ensure_ascii=False) + "\n")


def extract_jsonl_from_body(body: str) -> List[Dict]:
    """Extract JSONL knowledge cards from PR body"""
    cards = []
    
    matches = RE_JSONL_BLOCK.findall(body)
    
    for block in matches:
        for line in block.split('\n'):
            line = line.strip()
            if not line or line.startswith('//') or line.startswith('#'):
                continue
            
            try:
                card = json.loads(line)
                if 'type' in card and 'id' in card:
                    cards.append(card)
            except json.JSONDecodeError:
                continue
    
    return cards


def extract_metadata_from_body(body: str, pr_number: int) -> Optional[Dict]:
    """Extract structured metadata from PR body (fallback if no JSONL)"""
    if not body:
        return None
    
    is_bug_fix = any(kw in body.lower() for kw in ['fix', 'bug', 'hotfix', 'patch'])
    
    root_cause_match = RE_ROOT_CAUSE.search(body)
    root_cause = root_cause_match.group(1).strip() if root_cause_match else None
    
    fix_steps_match = RE_FIX_STEPS.search(body)
    fix_steps = []
    if fix_steps_match:
        steps_text = fix_steps_match.group(1).strip()
        for line in steps_text.split('\n'):
            line = line.strip()
            if line and (line[0].isdigit() or line.startswith('-') or line.startswith('*')):
                clean = re.sub(r'^[\d\-\*\.]+\s*', '', line)
                fix_steps.append(clean)
    
    if is_bug_fix and (root_cause or fix_steps):
        return {
            'is_bug_fix': True,
            'root_cause': root_cause,
            'fix_steps': fix_steps,
            'pr_number': pr_number
        }
    
    return None


def process_pr(pr: Dict, repo_name: str) -> int:
    """Process a single PR and extract knowledge cards"""
    pr_number = pr['number']
    title = pr['title']
    author = pr.get('author', {}).get('login', 'unknown')
    body = pr.get('body', '')
    labels = [lbl.get('name', '') for lbl in pr.get('labels', [])]
    merged_at = pr.get('mergedAt', pr.get('closedAt', ''))
    
    card_count = 0
    
    jsonl_cards = extract_jsonl_from_body(body)
    for card in jsonl_cards:
        if 'repo' not in card:
            card['repo'] = [repo_name]
        if 'evidence' not in card:
            card['evidence'] = {}
        card['evidence']['pr'] = pr_number
        card['evidence']['pr_title'] = title
        
        emit(card)
        card_count += 1
        print(f"  ✅ Extracted {card['type']} card: {card['id']}")
    
    if card_count == 0:
        metadata = extract_metadata_from_body(body, pr_number)
        
        if metadata and metadata.get('is_bug_fix'):
            card = {
                'type': 'MISTAKE',
                'id': f"m.pr{pr_number}.{repo_name}",
                'repo': [repo_name],
                'symptom': title,
                'root_cause': metadata.get('root_cause', 'See PR for details'),
                'fix_steps': metadata.get('fix_steps', [f"See PR #{pr_number}"]),
                'evidence': {
                    'pr': pr_number,
                    'pr_title': title,
                    'author': author,
                    'merged_at': merged_at
                },
                'tags': labels + ['pr-generated']
            }
            emit(card)
            card_count += 1
            print(f"  ✅ Generated MISTAKE card from PR #{pr_number}")
        
        elif 'enhancement' in labels or 'feature' in labels:
            card = {
                'type': 'RUNBOOK',
                'id': f"rb.pr{pr_number}.{repo_name}",
                'repo': [repo_name],
                'title': title,
                'steps': [f"Implementation in PR #{pr_number}"],
                'evidence': {'pr': pr_number, 'merged_at': merged_at},
                'tags': labels + ['pr-generated']
            }
            emit(card)
            card_count += 1
            print(f"  ✅ Generated RUNBOOK card from PR #{pr_number}")
    
    return card_count


def get_repo_name() -> str:
    """Get current repo name from git"""
    try:
        result = subprocess.run(
            ["git", "remote", "get-url", "origin"],
            capture_output=True,
            text=True,
            check=True,
            cwd=ROOT
        )
        url = result.stdout.strip()
        match = re.search(r'/([^/]+?)(?:\.git)?$', url)
        if match:
            return match.group(1)
        return 'unknown-repo'
    except:
        return 'unknown-repo'


def main():
    parser = argparse.ArgumentParser(description='Extract knowledge from GitHub PRs')
    parser.add_argument('--limit', type=int, default=50, help='Number of PRs to fetch (default: 50)')
    parser.add_argument('--stdin', action='store_true', help='Read PR JSON from stdin instead of fetching')
    parser.add_argument('--repo', type=str, help='Repository name (auto-detected if not provided)')
    args = parser.parse_args()
    
    KB.parent.mkdir(parents=True, exist_ok=True)
    
    repo_name = args.repo or get_repo_name()
    print(f"📖 Extracting knowledge from PRs in {repo_name}...")
    
    if args.stdin:
        print("📥 Reading PR data from stdin...")
        pr_data = json.load(sys.stdin)
    else:
        print(f"📥 Fetching last {args.limit} merged PRs from GitHub...")
        output = run_gh_command([
            'pr', 'list',
            '--state', 'merged',
            '--limit', str(args.limit),
            '--json', 'number,title,author,body,labels,mergedAt,closedAt'
        ])
        pr_data = json.loads(output)
    
    total_prs = len(pr_data)
    total_cards = 0
    
    for pr in pr_data:
        cards = process_pr(pr, repo_name)
        total_cards += cards
    
    print(f"\n🎉 Extraction complete!")
    print(f"   PRs processed: {total_prs}")
    print(f"   Knowledge cards extracted: {total_cards}")
    print(f"   Knowledge base: {KB}")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n⚠️  Interrupted by user", file=sys.stderr)
        sys.exit(130)
    except Exception as e:
        print(f"❌ ERROR: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)

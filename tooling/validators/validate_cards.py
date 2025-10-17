#!/usr/bin/env python3
"""
PR Knowledge Cards Validator
Validates knowledge cards in PR bodies for CI/CD integration.

Usage:
    python3 ai_manual/tooling/validators/validate_cards.py --pr-body pr_body.txt
    
    export PR_BODY="..." 
    python3 ai_manual/tooling/validators/validate_cards.py --env PR_BODY
    
    echo "$PR_BODY" | python3 ai_manual/tooling/validators/validate_cards.py --stdin

Exit codes:
    0: Valid cards found
    1: No cards or invalid cards
    2: Error
"""

import json
import sys
import re
import argparse
import os
from typing import List, Dict, Tuple

GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'

RE_JSONL_BLOCK = re.compile(r'```(?:json|jsonl)\s*\n(.*?)\n```', re.DOTALL | re.I)

REQUIRED_FIELDS = {
    'MISTAKE': ['type', 'id', 'symptom', 'root_cause', 'fix_steps', 'tags'],
    'PATTERN': ['type', 'id', 'name', 'when', 'steps', 'tags'],
    'DECISION': ['type', 'id', 'question', 'decision', 'reason', 'tags'],
    'TOOL': ['type', 'id', 'name', 'tags'],
    'RUNBOOK': ['type', 'id', 'title', 'steps', 'tags'],
}


def extract_cards_from_text(text: str) -> List[str]:
    """Extract JSONL cards from markdown code blocks"""
    cards = []
    matches = RE_JSONL_BLOCK.findall(text)
    
    for block in matches:
        for line in block.split('\n'):
            line = line.strip()
            if not line or line.startswith('//') or line.startswith('#'):
                continue
            cards.append(line)
    
    return cards


def validate_card(card_json: str) -> Tuple[bool, str, Dict]:
    """Validate a single knowledge card"""
    try:
        card = json.loads(card_json)
    except json.JSONDecodeError as e:
        return False, f"Invalid JSON: {e.msg}", {}
    
    if 'type' not in card:
        return False, "Missing required field 'type'", card
    if 'id' not in card:
        return False, "Missing required field 'id'", card
    
    card_type = card['type']
    
    if card_type not in REQUIRED_FIELDS:
        return False, f"Unknown card type '{card_type}'", card
    
    missing = []
    for field in REQUIRED_FIELDS[card_type]:
        if field not in card:
            missing.append(field)
    
    if missing:
        return False, f"Missing required fields: {', '.join(missing)}", card
    
    if card_type in ['MISTAKE', 'PATTERN', 'RUNBOOK']:
        list_fields = {'MISTAKE': ['fix_steps'], 'PATTERN': ['steps'], 'RUNBOOK': ['steps']}
        for field in list_fields.get(card_type, []):
            if not isinstance(card.get(field), list):
                return False, f"Field '{field}' must be a list", card
    
    if not isinstance(card.get('tags'), list):
        return False, "Field 'tags' must be a list", card
    
    if 'repo' in card and not isinstance(card['repo'], list):
        return False, "Field 'repo' must be a list", card
    
    return True, "Valid", card


def main():
    parser = argparse.ArgumentParser(description='Validate knowledge cards in PR body')
    parser.add_argument('--pr-body', type=str, help='Path to file containing PR body')
    parser.add_argument('--env', type=str, help='Environment variable containing PR body')
    parser.add_argument('--stdin', action='store_true', help='Read PR body from stdin')
    parser.add_argument('--require-cards', action='store_true', help='Fail if no cards found')
    args = parser.parse_args()
    
    pr_body = None
    if args.stdin:
        pr_body = sys.stdin.read()
    elif args.env:
        pr_body = os.environ.get(args.env)
        if not pr_body:
            print(f"{RED}❌ Environment variable '{args.env}' not set{RESET}")
            sys.exit(2)
    elif args.pr_body:
        try:
            with open(args.pr_body, 'r') as f:
                pr_body = f.read()
        except FileNotFoundError:
            print(f"{RED}❌ File not found: {args.pr_body}{RESET}")
            sys.exit(2)
    else:
        print(f"{RED}❌ Must specify --pr-body, --env, or --stdin{RESET}")
        parser.print_help()
        sys.exit(2)
    
    print(f"{BLUE}🔍 Validating Knowledge Cards in PR{RESET}\n")
    
    card_lines = extract_cards_from_text(pr_body)
    
    if not card_lines:
        print(f"{YELLOW}⚠️  No knowledge cards found in PR body{RESET}")
        if args.require_cards:
            print(f"{RED}❌ At least one knowledge card is required{RESET}")
            print(f"\n{BLUE}Expected format:{RESET}")
            print("```json")
            print('{"type":"MISTAKE","id":"m.example","symptom":"...","root_cause":"...","fix_steps":["..."],"tags":["..."]}')
            print("```")
            sys.exit(1)
        else:
            print(f"{GREEN}✅ No cards required, passing{RESET}")
            sys.exit(0)
    
    print(f"📄 Found {len(card_lines)} potential card(s)\n")
    
    valid_count = 0
    invalid_count = 0
    
    for i, card_line in enumerate(card_lines, 1):
        is_valid, message, card = validate_card(card_line)
        
        if is_valid:
            card_type = card['type']
            card_id = card['id']
            print(f"{GREEN}✅ Card {i}: {card_type} - {card_id}{RESET}")
            valid_count += 1
        else:
            print(f"{RED}❌ Card {i}: {message}{RESET}")
            print(f"   {card_line[:100]}...")
            invalid_count += 1
    
    print(f"\n{BLUE}📊 Summary{RESET}")
    print(f"   Valid cards: {valid_count}")
    print(f"   Invalid cards: {invalid_count}")
    
    if invalid_count > 0:
        print(f"\n{RED}❌ Validation FAILED{RESET}")
        print(f"\n{BLUE}Card Templates:{RESET}")
        print("\nMISTAKE:")
        print('{"type":"MISTAKE","id":"m.<slug>","repo":["<repo>"],"symptom":"...","root_cause":"...","fix_steps":["..."],"tags":["..."]}')
        print("\nPATTERN:")
        print('{"type":"PATTERN","id":"pat.<slug>","repo":["<repo>"],"name":"...","when":"...","steps":["..."],"tags":["..."]}')
        print("\nDECISION:")
        print('{"type":"DECISION","id":"d.<slug>","repo":["<repo>"],"question":"...","decision":"...","reason":"...","tags":["..."]}')
        sys.exit(1)
    elif valid_count == 0 and args.require_cards:
        print(f"\n{RED}❌ No valid cards found (at least one required){RESET}")
        sys.exit(1)
    else:
        print(f"\n{GREEN}✅ All cards are valid{RESET}")
        sys.exit(0)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{YELLOW}⚠️  Interrupted by user{RESET}")
        sys.exit(130)
    except Exception as e:
        print(f"{RED}❌ ERROR: {e}{RESET}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(2)

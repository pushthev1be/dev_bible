#!/usr/bin/env python3
"""
Knowledge Base JSONL Validator
Validates syntax and structure of knowledge.jsonl file.

Usage:
    python3 ai_manual/tooling/validators/validate_kb.py
    
Exit codes:
    0: All valid
    1: Validation errors found
    2: File not found or other error
"""

import json
import sys
import pathlib
from typing import Dict, List, Tuple

ROOT = pathlib.Path(__file__).resolve().parents[3]
KB = ROOT / "ai_manual" / "kb" / "knowledge.jsonl"

GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'


def validate_jsonl_syntax(file_path: pathlib.Path) -> Tuple[bool, List[str]]:
    """Validate that each line is valid JSON"""
    errors = []
    line_num = 0
    
    try:
        with file_path.open('r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                if not line:
                    continue  # Empty lines are OK
                
                try:
                    json.loads(line)
                except json.JSONDecodeError as e:
                    errors.append(f"Line {line_num}: Invalid JSON - {e.msg}")
    except FileNotFoundError:
        errors.append(f"File not found: {file_path}")
        return False, errors
    
    return len(errors) == 0, errors


def validate_card_structure(card: Dict, line_num: int) -> List[str]:
    """Validate structure of a knowledge card"""
    errors = []
    
    if 'type' not in card:
        errors.append(f"Line {line_num}: Missing required field 'type'")
    if 'id' not in card:
        errors.append(f"Line {line_num}: Missing required field 'id'")
    
    card_type = card.get('type', '')
    
    if card_type == 'META':
        pass
    
    elif card_type == 'MISTAKE':
        required = ['symptom', 'root_cause', 'fix_steps', 'tags']
        for field in required:
            if field not in card:
                errors.append(f"Line {line_num}: MISTAKE card missing '{field}'")
        
        if 'fix_steps' in card and not isinstance(card['fix_steps'], list):
            errors.append(f"Line {line_num}: 'fix_steps' should be a list")
        
        if 'tags' in card and not isinstance(card['tags'], list):
            errors.append(f"Line {line_num}: 'tags' should be a list")
    
    elif card_type == 'PATTERN':
        required = ['name', 'when', 'steps', 'tags']
        for field in required:
            if field not in card:
                errors.append(f"Line {line_num}: PATTERN card missing '{field}'")
        
        if 'steps' in card and not isinstance(card['steps'], list):
            errors.append(f"Line {line_num}: 'steps' should be a list")
    
    elif card_type == 'DECISION':
        required = ['question', 'decision', 'reason', 'tags']
        for field in required:
            if field not in card:
                errors.append(f"Line {line_num}: DECISION card missing '{field}'")
    
    elif card_type == 'TOOL':
        required = ['name', 'tags']
        for field in required:
            if field not in card:
                errors.append(f"Line {line_num}: TOOL card missing '{field}'")
    
    elif card_type == 'RUNBOOK':
        required = ['title', 'steps', 'tags']
        for field in required:
            if field not in card:
                errors.append(f"Line {line_num}: RUNBOOK card missing '{field}'")
    
    else:
        errors.append(f"Line {line_num}: Unknown card type '{card_type}'")
    
    if 'repo' in card and not isinstance(card['repo'], list):
        errors.append(f"Line {line_num}: 'repo' should be a list")
    
    return errors


def validate_card_ids(cards: List[Tuple[int, Dict]]) -> List[str]:
    """Check for duplicate IDs"""
    errors = []
    seen_ids = {}
    
    for line_num, card in cards:
        card_id = card.get('id')
        if card_id:
            if card_id in seen_ids:
                errors.append(
                    f"Line {line_num}: Duplicate ID '{card_id}' "
                    f"(first seen on line {seen_ids[card_id]})"
                )
            else:
                seen_ids[card_id] = line_num
    
    return errors


def main():
    print(f"{BLUE}🔍 Validating Knowledge Base{RESET}")
    print(f"   File: {KB}\n")
    
    if not KB.exists():
        print(f"{RED}❌ File not found: {KB}{RESET}")
        sys.exit(2)
    
    all_errors = []
    cards = []
    
    print("1️⃣  Checking JSONL syntax...")
    is_valid, syntax_errors = validate_jsonl_syntax(KB)
    if syntax_errors:
        all_errors.extend(syntax_errors)
        print(f"{RED}   ❌ {len(syntax_errors)} syntax error(s) found{RESET}")
        for error in syntax_errors:
            print(f"      {error}")
    else:
        print(f"{GREEN}   ✅ All lines are valid JSON{RESET}")
    
    print("\n2️⃣  Checking card structure...")
    with KB.open('r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            
            try:
                card = json.loads(line)
                cards.append((line_num, card))
                
                card_errors = validate_card_structure(card, line_num)
                all_errors.extend(card_errors)
            except json.JSONDecodeError:
                pass
    
    if not all_errors:
        print(f"{GREEN}   ✅ All cards have valid structure{RESET}")
    else:
        structure_errors = [e for e in all_errors if e not in syntax_errors]
        if structure_errors:
            print(f"{RED}   ❌ {len(structure_errors)} structure error(s) found{RESET}")
            for error in structure_errors[:10]:  # Show first 10
                print(f"      {error}")
            if len(structure_errors) > 10:
                print(f"      ... and {len(structure_errors) - 10} more")
    
    print("\n3️⃣  Checking for duplicate IDs...")
    duplicate_errors = validate_card_ids(cards)
    if duplicate_errors:
        all_errors.extend(duplicate_errors)
        print(f"{YELLOW}   ⚠️  {len(duplicate_errors)} duplicate ID(s) found{RESET}")
        for error in duplicate_errors:
            print(f"      {error}")
    else:
        print(f"{GREEN}   ✅ All IDs are unique{RESET}")
    
    print(f"\n{BLUE}📊 Summary{RESET}")
    print(f"   Total cards: {len(cards)}")
    
    type_counts = {}
    for _, card in cards:
        card_type = card.get('type', 'UNKNOWN')
        type_counts[card_type] = type_counts.get(card_type, 0) + 1
    
    print(f"   By type:")
    for card_type, count in sorted(type_counts.items(), key=lambda x: -x[1]):
        print(f"     - {card_type}: {count}")
    
    print()
    if all_errors:
        print(f"{RED}❌ Validation FAILED with {len(all_errors)} error(s){RESET}")
        sys.exit(1)
    else:
        print(f"{GREEN}✅ All validations PASSED{RESET}")
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

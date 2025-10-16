#!/bin/bash
#
#
#

alias bibles='~/dev_bibles/bible-search --list'
alias bible-stats='~/dev_bibles/bible-search --stats'
alias bible='~/dev_bibles/bible-search'

alias bible-mistakes='~/dev_bibles/bible-search --mistakes'
alias bible-patterns='~/dev_bibles/bible-search --patterns'
alias bible-personal='~/dev_bibles/bible-search --personal'
alias bible-master='~/dev_bibles/bible-search --master'

alias bible-sync='~/dev_bibles/bible-sync'
alias bible-import='~/dev_bibles/bible-sync --import'
alias bible-discover='~/dev_bibles/bible-sync --discover'
alias bible-status='~/dev_bibles/bible-sync --status'

bible-add-mistake() {
    echo "Adding MISTAKE to Master Bible"
    echo -n "ID (e.g., m.personal.forgot_x): "
    read id
    echo -n "Symptom: "
    read symptom
    echo -n "Root cause: "
    read root_cause
    echo -n "Fix: "
    read fix
    echo -n "Tags (comma-separated): "
    read tags
    
    echo "{\"type\":\"MISTAKE\",\"id\":\"$id\",\"symptom\":\"$symptom\",\"root_cause\":\"$root_cause\",\"fix_steps\":[\"$fix\"],\"tags\":[\"${tags//,/\",\"}\"]}" >> ~/dev_bibles/_master/bible.jsonl
    echo "✓ Added to Master Bible"
}

bible-add-pattern() {
    echo "Adding PATTERN to Master Bible"
    echo -n "ID (e.g., pat.personal.my_pattern): "
    read id
    echo -n "Name: "
    read name
    echo -n "When to use: "
    read when
    echo -n "Step 1: "
    read step1
    echo -n "Step 2: "
    read step2
    echo -n "Tags (comma-separated): "
    read tags
    
    echo "{\"type\":\"PATTERN\",\"id\":\"$id\",\"name\":\"$name\",\"when\":\"$when\",\"steps\":[\"$step1\",\"$step2\"],\"tags\":[\"${tags//,/\",\"}\"]}" >> ~/dev_bibles/_master/bible.jsonl
    echo "✓ Added to Master Bible"
}

bible-add-principle() {
    echo "Adding PRINCIPLE to Master Bible"
    echo -n "ID (e.g., p.personal.my_rule): "
    read id
    echo -n "Principle: "
    read text
    echo -n "Tags (comma-separated): "
    read tags
    
    echo "{\"type\":\"PRINCIPLE\",\"id\":\"$id\",\"text\":\"$text\",\"tags\":[\"${tags//,/\",\"}\"]}" >> ~/dev_bibles/_master/bible.jsonl
    echo "✓ Added to Master Bible"
}

alias cdmaster='cd ~/dev_bibles/_master'
alias cdbibles='cd ~/dev_bibles'

bible-help() {
    echo "Bible Library Commands"
    echo "======================"
    echo ""
    echo "Searching:"
    echo "  bible <tag>              Search all Bibles"
    echo "  bible <tag> <project>    Search specific project"
    echo "  bible-mistakes <tag>     Find mistakes only"
    echo "  bible-patterns <tag>     Find patterns only"
    echo "  bible-personal           Show your personal flaws"
    echo "  bible-master <tag>       Search master Bible only"
    echo ""
    echo "Syncing:"
    echo "  bible-discover           Find projects with Bibles"
    echo "  bible-import             Import all project Bibles"
    echo "  bible-status             Show sync status"
    echo "  bible-sync --help        Full sync help"
    echo ""
    echo "Stats & Info:"
    echo "  bible-stats              Show all Bible stats"
    echo "  bibles                   List all projects"
    echo ""
    echo "Adding Lessons (to Master):"
    echo "  bible-add-mistake        Add personal mistake"
    echo "  bible-add-pattern        Add personal pattern"
    echo "  bible-add-principle      Add personal principle"
    echo ""
    echo "Navigation:"
    echo "  cdmaster                 Go to master Bible"
    echo "  cdbibles                 Go to library root"
    echo ""
    echo "Full help: bible --help"
}

echo "✓ Bible aliases loaded"
echo "  Type 'bible-help' for commands"

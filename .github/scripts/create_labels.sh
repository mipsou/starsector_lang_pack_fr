#!/bin/bash

# Configuration
REPO="mipsou/starsector_lang_pack_fr_private"
API="https://api.github.com/repos/$REPO/labels"

# Function to create or update a label
create_label() {
    NAME=$1
    COLOR=$2
    DESCRIPTION=$3
    
    echo "Creating label: $NAME"
    curl -X POST $API \
         -H "Accept: application/vnd.github.v3+json" \
         -d "{\"name\":\"$NAME\",\"color\":\"$COLOR\",\"description\":\"$DESCRIPTION\"}"
}

# Type labels
create_label "🐛 bug" "d73a4a" "Something isn't working"
create_label "✨ feature" "0075ca" "New feature or request"
create_label "📚 documentation" "0075ca" "Documentation improvements"
create_label "🌍 translation" "1d76db" "Translation related"
create_label "🔧 maintenance" "2a3f99" "Maintenance tasks"

# Status labels
create_label "👀 needs review" "fbca04" "Needs review from maintainers"
create_label "⌛ in progress" "fef2c0" "Work in progress"
create_label "✅ ready" "0e8a16" "Ready to merge"
create_label "🚫 blocked" "b60205" "Blocked or needs discussion"

# Priority labels
create_label "🔥 high" "d93f0b" "High priority"
create_label "🟡 medium" "fbca04" "Medium priority"
create_label "🟢 low" "0e8a16" "Low priority"

echo "Labels created successfully!"

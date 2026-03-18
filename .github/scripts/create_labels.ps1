# Configuration
$repo = "mipsou/starsector_lang_pack_fr"
$api = "https://api.github.com/repos/$repo/labels"

# Function to create or update a label
function Create-Label {
    param(
        [string]$name,
        [string]$color,
        [string]$description
    )
    
    Write-Host "Creating label: $name"
    $body = @{
        name = $name
        color = $color
        description = $description
    } | ConvertTo-Json

    Invoke-RestMethod -Uri $api -Method Post -Body $body -ContentType "application/json"
}

# Type labels
Create-Label "🐛 bug" "d73a4a" "Something isn't working"
Create-Label "✨ feature" "0075ca" "New feature or request"
Create-Label "📚 documentation" "0075ca" "Documentation improvements"
Create-Label "🌍 translation" "1d76db" "Translation related"
Create-Label "🔧 maintenance" "2a3f99" "Maintenance tasks"

# Status labels
Create-Label "👀 needs review" "fbca04" "Needs review from maintainers"
Create-Label "⌛ in progress" "fef2c0" "Work in progress"
Create-Label "✅ ready" "0e8a16" "Ready to merge"
Create-Label "🚫 blocked" "b60205" "Blocked or needs discussion"

# Priority labels
Create-Label "🔥 high" "d93f0b" "High priority"
Create-Label "🟡 medium" "fbca04" "Medium priority"
Create-Label "🟢 low" "0e8a16" "Low priority"

Write-Host "Labels created successfully!"

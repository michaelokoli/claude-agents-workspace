#!/bin/bash
# Update Architecture Documentation Script
# Run this after making changes to agents, scripts, or knowledge base

echo "🔍 Scanning workspace architecture..."
python scripts/architecture_scanner.py

echo ""
echo "📊 Architecture Summary:"
echo "─────────────────────"
grep "Total Agents" docs/architecture-overview.md
grep "Knowledge Base Entries" docs/architecture-overview.md
grep "Python Scripts" docs/architecture-overview.md
echo ""
echo "✅ Architecture documentation updated!"
echo "View at: docs/architecture-overview.md"
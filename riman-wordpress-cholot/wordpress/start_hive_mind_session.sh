#!/bin/bash

# Start Hive Mind Session für WordPress Processor
# ================================================

echo "🐝 Starting Hive Mind Session: hive-wordpress-processor"
echo "================================================"

# 1. Session wiederherstellen
echo "📂 Restoring session context..."
npx claude-flow@alpha hooks session-restore --session-id "hive-wordpress-processor"

# 2. Swarm Status prüfen
echo "🔍 Checking swarm status..."
npx claude-flow@alpha swarm status

# 3. Memory laden
echo "💾 Loading memory..."
npx claude-flow@alpha memory list --namespace "hive/wordpress-processor"

# 4. Claude mit Hive Mind Prompt starten
echo "🚀 Starting Claude with Hive Mind configuration..."
echo ""
echo "Option 1: Interactive Claude Session"
echo "======================================="
echo "claude < hive_mind_prompt.md"
echo ""
echo "Option 2: Direct Command with Context"
echo "======================================="
cat << 'EOF'
claude "$(cat hive_mind_prompt.md)

I am now resuming the hive-wordpress-processor session with:
- Swarm ID: swarm_1756407314892_gfkn8cryq  
- Session ID: hive-wordpress-processor

What aspect of the WordPress/Elementor processor should we coordinate today?"
EOF
echo ""
echo "Option 3: With Pre-loaded Context"
echo "======================================="
cat << 'EOF'
claude --context hive_mind_config.json --context hive_mind_prompt.md \
  "Resume the hive-wordpress-processor session. Analyze current state and ask what to coordinate."
EOF
echo ""
echo "Option 4: Using SPARC Swarm Mode"
echo "======================================="
echo 'npx claude-flow@alpha sparc swarm-coordinator "Resume hive-wordpress-processor session"'
echo ""

# Tatsächlich starten (wähle eine Option):
echo "🎯 Executing Option 2 (Direct Command with Context)..."
echo "================================================"

claude "$(cat hive_mind_prompt.md)

## Session Resume
I am now resuming the hive-wordpress-processor session with:
- Swarm ID: swarm_1756407314892_gfkn8cryq  
- Session ID: hive-wordpress-processor
- Working Directory: $(pwd)

## Current State Check
Let me first analyze the current project state:

1. **WordPress Status**: Page 3000 configured with Elementor
2. **Available Processors**: 
   - yaml_to_elementor.php
   - yaml_to_xml_generator.py
   - complete_xml_generator.py
3. **Test URLs**:
   - http://localhost:8081/?page_id=3000 (our generated page)
   - http://localhost:8080 (Cholot reference)

## Queen's Analysis
As the Queen Project Manager, I observe that:
- The Elementor error has been fixed
- We have working YAML to XML processors
- The design review verification loop is ready
- Image generation pipeline is configured

## Coordination Question
What specific aspect of the WordPress/Elementor processor should we coordinate today?

1. Should we focus on perfecting the service card generation?
2. Should we implement the image generation workflow?
3. Should we improve the YAML processor to better match Cholot theme?
4. Should we run a full design review verification loop?

I await your directive to delegate tasks to the appropriate specialist agents."
#!/bin/bash

# XML Generator Swarm Runner
# Referenziert die detaillierte Prompt-Datei

echo "🚀 Starting Cholot XML Generator Swarm..."

# Option 1: Datei direkt einlesen und als Prompt übergeben (EMPFOHLEN)
npx claude-flow@alpha swarm "$(cat swarm-prompt-xml-generator.md)" \
  --strategy content-transformation \
  --neural-patterns enabled \
  --memory-compression high

# Option 2: Kurzer Prompt mit Dateiverweis
# npx claude-flow@alpha swarm "Read and execute the detailed instructions in swarm-prompt-xml-generator.md. This file contains the complete specification for creating an intelligent WordPress XML generator from Cholot theme components. Follow all phases: Component Discovery, Pattern Recognition, and Generator Design. The main files to analyze are demo-data-fixed.xml and riman-content-structure.json in the current directory." \
#   --strategy engineering \
#   --neural-patterns enabled \
#   --agents 6

# Option 3: Kombination - Zusammenfassung + Details
# npx claude-flow@alpha swarm "Create an intelligent WordPress XML generator that understands Cholot theme components. IMPORTANT: Read swarm-prompt-xml-generator.md for complete specifications. Key tasks: 1) Parse demo-data-fixed.xml to extract all Elementor widgets as reusable components, 2) Design a system that accepts Markdown/YAML/JSON input, 3) Generate valid WordPress XML maintaining 100% Cholot theme compatibility. Use the detailed implementation strategy in the markdown file." \
#   --strategy engineering \
#   --neural-patterns enabled \
#   --memory-compression high
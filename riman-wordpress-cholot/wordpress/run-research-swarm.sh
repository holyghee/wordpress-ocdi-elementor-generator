#!/bin/bash

echo "🔬 Starting Research Swarm for Elementor JSON Generation"
echo "=================================================="

# Check if context package exists
if [ ! -f "swarm-context-package.md" ]; then
    echo "❌ Error: swarm-context-package.md not found!"
    echo "This file contains critical context for the research."
    exit 1
fi

echo "✅ Context package found - providing complete background to swarm"
echo ""

# Execute the research swarm with full context
npx claude-flow@alpha swarm "CONTEXT: We have a working WordPress XML generator (generate_wordpress_xml.py) that converts YAML to WordPress/Elementor sites. We have 7 real Elementor JSON templates from Cholot theme with 13 custom widgets. We've built adaptive layout engine, content-design separator, and block library system. HTML/CSS conversion proved too complex. Core challenge: Generate valid Elementor JSON (400+ parameters per widget) from simple user input (business name, 3-10 services). 

RESEARCH FOCUS: Test if LLMs can reliably generate valid Elementor JSON when given our complete templates as examples, widget documentation, and validation rules. Compare with fixed code patterns and hybrid approaches. Build on our existing working code, don't reinvent.

KEY FILES TO ANALYZE: generate_wordpress_xml.py (working), elementor-templates/*.json (real data), adaptive-layout-engine.py (layout logic), content-design-separator.py (core concept), block-library-system.py (template extraction).

DELIVERABLE: Definitive recommendation with working prototype - LLM vs Fixed Code vs Hybrid for production business website generator." \
  --strategy research \
  --neural-patterns enabled \
  --memory-compression high \
  --agents 4 \
  --topology hierarchical \
  --max-time 600 \
  --context-file swarm-context-package.md \
  --output-format detailed

echo ""
echo "Research areas to investigate:"
echo "✓ LLM reliability for complex JSON generation"
echo "✓ Fixed code patterns vs flexibility trade-offs" 
echo "✓ Hybrid architectures (LLM content + fixed structure)"
echo "✓ Template-based vs generative approaches"
echo "✓ Performance and cost analysis"
echo "✓ Maintenance and scalability considerations"
echo ""
echo "Expected deliverables:"
echo "• Technical benchmarks and comparisons"
echo "• Recommended architecture with justification"
echo "• Implementation roadmap and risk assessment"
echo "• Proof of concept code examples"
echo ""
echo "🚀 Research Swarm is now analyzing the problem..."
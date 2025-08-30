# Hive Mind Session Start Commands

## 🚀 Quick Start (Copy & Paste)

### Option 1: Direct Claude Command
```bash
claude "I need to resume the hive-wordpress-processor session (Swarm: swarm_1756407314892_gfkn8cryq). Load the configuration from hive_mind_config.json and act as the Queen Project Manager. First analyze the current state, then ask what should be coordinated today. Never code directly, only delegate to specialized agents."
```

### Option 2: With Full Context File
```bash
claude --context hive_mind_config.json --context hive_mind_prompt.md "Resume the hive-wordpress-processor session and analyze current project state"
```

### Option 3: Interactive Session with Script
```bash
./start_hive_mind_session.sh
```

### Option 4: Using SPARC Swarm Coordinator
```bash
npx claude-flow@alpha sparc swarm-coordinator "Resume hive-wordpress-processor session with Queen Project Manager role from hive_mind_config.json"
```

## 📋 Manual Session Restoration

If you want to manually set up the session:

```bash
# 1. Restore session
npx claude-flow@alpha hooks session-restore --session-id "hive-wordpress-processor"

# 2. Load memory
npx claude-flow@alpha memory usage --action retrieve --key "hive/wordpress-processor/config"

# 3. Start Claude with the role
claude "You are the Queen Project Manager for the WordPress/Elementor processor project. Your configuration is in hive_mind_config.json. Coordinate but never code directly."
```

## 🎯 What the Hive Mind Knows

The Queen has full knowledge of:
- **WordPress Cleanup**: `./wordpress-cleanup.sh`
- **Image Generation**: Midjourney server at `/Users/holgerbrandt/dev/claude-code/tools/midjourney-mcp-server`
- **Image Server**: Running on `http://localhost:3456`
- **XML Import**: Can import `riman_generated.xml` for testing
- **Design Verification**: Uses design-review agent iteratively (max 5 loops)
- **All Processors**: YAML to Elementor/XML converters
- **Agent Delegation Map**: Which agents to use for each task type

## 👑 Queen's Directive

"First analyze the current project state, then ask what should be coordinated today. Never code directly, only delegate."

## 🔄 Verification Loop Protocol

Every task follows this pattern:
1. Delegate to specialist agent
2. Run design-review verification
3. If failed, iterate with feedback (max 5 times)
4. Document results in memory

## 💾 Session IDs

- **Swarm ID**: `swarm_1756407314892_gfkn8cryq`
- **Session ID**: `hive-wordpress-processor`
- **Memory Namespace**: `hive/wordpress-processor/*`
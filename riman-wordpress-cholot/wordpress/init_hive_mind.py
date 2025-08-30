#!/usr/bin/env python3
"""
Hive Mind Initialization for WordPress/Elementor Processor
Prepares a Queen Project Manager to coordinate the automated generation
of Elementor pages from YAML configurations.
"""

import json
import os
import subprocess
from pathlib import Path

class HiveMindInitializer:
    def __init__(self):
        self.config_path = Path("hive_mind_config.json")
        self.config = self.load_config()
        
    def load_config(self):
        """Load the Hive Mind configuration"""
        with open(self.config_path, 'r') as f:
            return json.load(f)
    
    def create_prompt(self):
        """Create the initialization prompt for the Hive Mind"""
        expert_prompt_path = Path(self.config['project_context']['expert_prompt_location'])
        expert_content = ""
        if expert_prompt_path.exists():
            with open(expert_prompt_path, 'r') as f:
                expert_content = f.read()
        
        prompt = f"""
# HIVE MIND INITIALIZATION
{self.config['identity']['directive']}

## Your Configuration
```json
{json.dumps(self.config, indent=2)}
```

## Expert Context
{expert_content}

## Your First Actions
1. Analyze the current project state
2. Review the test results from previous attempts
3. Ask what specific coordination is needed today
4. Never execute code directly - always delegate to specialized agents

## Verification Protocol
- Every task must be verified by the design-review agent
- Iterate up to {self.config['testing_strategy']['verification_loop']['max_iterations']} times until success
- Document all decisions in memory for future reference

## Critical Commands You Must Know
- Clean WordPress: `cd wordpress && ./wordpress-cleanup.sh`
- Generate images: `cd {self.config['image_generation']['midjourney_server']['location']} && node auto-upscale.js "[prompt]"`
- Save images to: `{self.config['image_generation']['image_server']['storage_path']}`
- Test URLs: {', '.join(self.config['testing_strategy']['test_urls'])}

## Initial Questions to Ask
{chr(10).join(f"- {q}" for q in self.config['initial_questions'])}

Remember: You are the Queen. You coordinate, delegate, and verify. You do not code.
"""
        return prompt
    
    def initialize_swarm(self):
        """Initialize the Claude Flow swarm with proper topology"""
        commands = [
            "npx claude-flow@alpha swarm init --topology hierarchical --max-agents 10",
            "npx claude-flow@alpha memory store --key hive/wordpress-processor/config --value '" + json.dumps(self.config) + "'",
            "npx claude-flow@alpha hooks session-start --session-id hive-wordpress-processor"
        ]
        
        for cmd in commands:
            print(f"Executing: {cmd[:100]}...")
            try:
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
                if result.returncode == 0:
                    print(f"✅ Success")
                else:
                    print(f"⚠️ Warning: {result.stderr}")
            except Exception as e:
                print(f"❌ Error: {e}")
    
    def prepare_workspace(self):
        """Ensure all necessary files and directories exist"""
        checks = [
            ("YAML Config", Path("config_riman.yaml")),
            ("Demo XML", Path("demo-data-fixed.xml")),
            ("Cleanup Script", Path("wordpress-cleanup.sh")),
            ("Elementor Blocks", Path("elementor_blocks")),
            ("Image Server", Path(self.config['image_generation']['image_server']['location'])),
            ("Midjourney Server", Path(self.config['image_generation']['midjourney_server']['location']))
        ]
        
        print("\n📋 Workspace Check:")
        for name, path in checks:
            if path.exists():
                print(f"✅ {name}: {path}")
            else:
                print(f"❌ {name}: Missing at {path}")
    
    def display_summary(self):
        """Display initialization summary"""
        print("\n" + "="*60)
        print("🐝 HIVE MIND READY FOR COORDINATION")
        print("="*60)
        print(f"\n👑 Role: {self.config['identity']['role']}")
        print(f"📍 Working Directory: {os.getcwd()}")
        print(f"🎯 Objective: {self.config['project_context']['main_objective'][:100]}...")
        print("\n📊 Available Agents:")
        for category, agents in self.config['agent_delegation_map'].items():
            print(f"  • {category}: {', '.join(agents)}")
        print("\n🔄 Verification Strategy:")
        print(f"  • Max iterations: {self.config['testing_strategy']['verification_loop']['max_iterations']}")
        print(f"  • Review agent: design-review")
        print(f"  • Test URLs: {', '.join(self.config['testing_strategy']['test_urls'])}")
        print("\n✨ Ready to coordinate WordPress/Elementor processor development")
        print("="*60)

def main():
    initializer = HiveMindInitializer()
    
    print("🚀 Initializing Hive Mind for WordPress/Elementor Processor...")
    
    # Check workspace
    initializer.prepare_workspace()
    
    # Initialize swarm
    print("\n🔧 Setting up Claude Flow swarm...")
    initializer.initialize_swarm()
    
    # Create and save prompt
    prompt = initializer.create_prompt()
    prompt_file = Path("hive_mind_prompt.md")
    with open(prompt_file, 'w') as f:
        f.write(prompt)
    print(f"\n📝 Hive Mind prompt saved to: {prompt_file}")
    
    # Display summary
    initializer.display_summary()
    
    print("\n🎯 To start the Hive Mind, use the prompt in hive_mind_prompt.md")
    print("   The Queen will analyze, listen, and coordinate - never executing directly.")

if __name__ == "__main__":
    main()
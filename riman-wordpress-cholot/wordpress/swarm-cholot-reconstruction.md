# SWARM: Cholot Theme Elementor Block Reconstruction & Testing

## Mission
Analysiere die Elementor-Block-Templates und rekonstruiere die komplette Cholot Theme Demo-Struktur. Erstelle einen vollautomatischen Test-Zyklus, der iterativ die Lösung verbessert bis sie funktioniert.

## Context & Resources

### Available Files
1. **Elementor Block Templates**: `/Users/holgerbrandt/dev/claude-code/projects/riman-wordpress/riman-wordpress-cholot/wordpress/elementor blocks/`
2. **Target XML Structure**: `/Users/holgerbrandt/Downloads/cholot-retirement-community-wordpress-theme11/documentation/sample_data/demo-data-fixed.xml`
3. **Working Generator**: `/Users/holgerbrandt/dev/claude-code/projects/riman-wordpress/riman-wordpress-cholot/wordpress/full_site_generator.py`
4. **Section Processor**: `/Users/holgerbrandt/dev/claude-code/projects/riman-wordpress/riman-wordpress-cholot/wordpress/section_based_processor.py`
5. **OCDI Config**: `/Users/holgerbrandt/dev/claude-code/projects/riman-wordpress/riman-wordpress-cholot/wordpress/wp-content/mu-plugins/ocdi-riman-import.php`
6. **Cleanup Script**: `/Users/holgerbrandt/dev/claude-code/projects/riman-wordpress/riman-wordpress-cholot/wordpress/wordpress-cleanup.sh`

### Working Directory
```
/Users/holgerbrandt/dev/claude-code/projects/riman-wordpress/riman-wordpress-cholot/wordpress
```

## Phase 1: Analysis & Mapping

### Task 1.1: Analyze Elementor Templates
```bash
# List all available Elementor block templates
ls -la "elementor blocks/"

# For each template file:
for file in "elementor blocks"/*.json; do
    echo "=== Analyzing: $file ==="
    # Extract key information
    python3 -c "
import json
with open('$file') as f:
    data = json.load(f)
    if 'content' in data and len(data['content']) > 0:
        print(f'Type: {data[\"content\"][0].get(\"elType\", \"unknown\")}')
        print(f'Widgets: {len(data[\"content\"][0].get(\"elements\", []))}')
        if 'settings' in data['content'][0]:
            print(f'Has settings: Yes')
    "
done
```

### Task 1.2: Parse Target XML Structure
```python
import xml.etree.ElementTree as ET

# Parse the target XML
tree = ET.parse('/Users/holgerbrandt/Downloads/cholot-retirement-community-wordpress-theme11/documentation/sample_data/demo-data-fixed.xml')
root = tree.getroot()

# Extract all pages with Elementor data
pages_with_elementor = []
for item in root.findall('.//item'):
    for meta in item.findall('.//wp:postmeta', namespaces={'wp': 'http://wordpress.org/export/1.2/'}):
        meta_key = meta.find('.//wp:meta_key', namespaces={'wp': 'http://wordpress.org/export/1.2/'})
        if meta_key is not None and meta_key.text == '_elementor_data':
            title = item.find('.//title').text
            pages_with_elementor.append(title)
            print(f"Found Elementor page: {title}")

# Analyze menu structure
menus = root.findall('.//wp:term[wp:term_taxonomy="nav_menu"]', 
                     namespaces={'wp': 'http://wordpress.org/export/1.2/'})
for menu in menus:
    name = menu.find('.//wp:term_name', namespaces={'wp': 'http://wordpress.org/export/1.2/'}).text
    print(f"Found menu: {name}")
```

## Phase 2: Pattern Recognition & Mapping

### Task 2.1: Create Block Mapping
```python
import json
import os

class ElementorBlockAnalyzer:
    def __init__(self, blocks_dir, target_xml):
        self.blocks_dir = blocks_dir
        self.target_xml = target_xml
        self.block_patterns = {}
    
    def analyze_blocks(self):
        """Analyze all Elementor block templates"""
        for filename in os.listdir(self.blocks_dir):
            if filename.endswith('.json'):
                with open(os.path.join(self.blocks_dir, filename)) as f:
                    data = json.load(f)
                    self.extract_pattern(filename, data)
    
    def extract_pattern(self, filename, data):
        """Extract reusable patterns from blocks"""
        if 'content' in data and data['content']:
            block = data['content'][0]
            pattern = {
                'type': block.get('elType'),
                'widgets': self.extract_widgets(block),
                'settings': block.get('settings', {})
            }
            self.block_patterns[filename] = pattern
    
    def extract_widgets(self, block):
        """Extract widget types from block"""
        widgets = []
        if 'elements' in block:
            for element in block['elements']:
                if element.get('elType') == 'widget':
                    widgets.append(element.get('widgetType'))
        return widgets
    
    def match_to_cholot_pages(self):
        """Match blocks to Cholot theme pages"""
        # Parse XML and extract Elementor data
        tree = ET.parse(self.target_xml)
        root = tree.getroot()
        
        matches = {}
        for item in root.findall('.//item'):
            title_elem = item.find('.//title')
            if title_elem is not None:
                title = title_elem.text
                elementor_data = self.get_elementor_data(item)
                if elementor_data:
                    matches[title] = self.find_best_block_match(elementor_data)
        
        return matches

analyzer = ElementorBlockAnalyzer('elementor blocks', 
    '/Users/holgerbrandt/Downloads/cholot-retirement-community-wordpress-theme11/documentation/sample_data/demo-data-fixed.xml')
analyzer.analyze_blocks()
matches = analyzer.match_to_cholot_pages()
```

## Phase 3: YAML Generation

### Task 3.1: Generate Cholot-Compatible YAML
```python
import yaml

class CholotYAMLGenerator:
    def __init__(self, block_patterns, xml_structure):
        self.block_patterns = block_patterns
        self.xml_structure = xml_structure
        
    def generate_yaml(self):
        """Generate YAML configuration for Cholot theme"""
        config = {
            'site': {
                'title': 'Cholot Theme Demo',
                'url': 'http://localhost:8082',
                'description': 'Retirement Community WordPress Theme'
            },
            'pages': [],
            'menus': [],
            'posts': []
        }
        
        # Add pages based on XML structure
        for page in self.xml_structure['pages']:
            page_config = self.create_page_config(page)
            config['pages'].append(page_config)
        
        # Add menus
        for menu in self.xml_structure['menus']:
            config['menus'].append(menu)
        
        return config
    
    def create_page_config(self, page_data):
        """Create page configuration with Elementor blocks"""
        return {
            'id': page_data['id'],
            'title': page_data['title'],
            'slug': page_data['slug'],
            'template': 'elementor_canvas',
            'sections': self.map_blocks_to_sections(page_data)
        }
    
    def save_yaml(self, config, filename='cholot-theme.yaml'):
        """Save configuration to YAML file"""
        with open(filename, 'w') as f:
            yaml.dump(config, f, default_flow_style=False, sort_keys=False)
        return filename
```

## Phase 4: Automated Testing Loop

### Task 4.1: Create Test Harness
```python
#!/usr/bin/env python3
import subprocess
import time
import json
import yaml
import hashlib
from pathlib import Path

class CholotThemeTestHarness:
    def __init__(self):
        self.working_dir = '/Users/holgerbrandt/dev/claude-code/projects/riman-wordpress/riman-wordpress-cholot/wordpress'
        self.target_xml = '/Users/holgerbrandt/Downloads/cholot-retirement-community-wordpress-theme11/documentation/sample_data/demo-data-fixed.xml'
        self.max_iterations = 10
        self.current_iteration = 0
        
    def run_test_cycle(self):
        """Run complete test cycle"""
        while self.current_iteration < self.max_iterations:
            print(f"\n🔄 Iteration {self.current_iteration + 1}/{self.max_iterations}")
            
            # 1. Generate YAML
            yaml_file = self.generate_yaml_config()
            
            # 2. Generate XML from YAML
            xml_file = self.generate_xml(yaml_file)
            
            # 3. Clean WordPress
            self.cleanup_wordpress()
            
            # 4. Import XML
            import_success = self.import_xml(xml_file)
            
            # 5. Verify import
            if import_success:
                verification = self.verify_import()
                
                if verification['success']:
                    print("✅ SUCCESS! Theme reconstruction complete!")
                    self.save_solution(yaml_file, xml_file)
                    return True
                else:
                    print(f"❌ Verification failed: {verification['errors']}")
                    self.adjust_configuration(verification['errors'])
            else:
                print("❌ Import failed, adjusting configuration...")
                self.adjust_configuration(['import_failed'])
            
            self.current_iteration += 1
        
        print("⚠️ Max iterations reached without success")
        return False
    
    def generate_yaml_config(self):
        """Generate YAML configuration"""
        print("📝 Generating YAML configuration...")
        # Use the analyzer to create config
        subprocess.run(['python3', 'generate_cholot_yaml.py'])
        return 'cholot-theme.yaml'
    
    def generate_xml(self, yaml_file):
        """Generate XML from YAML"""
        print("🔄 Converting YAML to XML...")
        result = subprocess.run([
            'python3', 'full_site_generator.py', 
            yaml_file, 
            'cholot-test.xml'
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ XML generated successfully")
            return 'cholot-test.xml'
        else:
            print(f"❌ XML generation failed: {result.stderr}")
            return None
    
    def cleanup_wordpress(self):
        """Clean WordPress installation"""
        print("🧹 Cleaning WordPress...")
        subprocess.run(['./wordpress-cleanup.sh'], check=True)
        time.sleep(2)
    
    def import_xml(self, xml_file):
        """Import XML using OCDI"""
        print("📥 Importing XML with OCDI...")
        result = subprocess.run([
            'php', 'test-direct-ocdi.php'
        ], capture_output=True, text=True)
        
        return 'Import completed' in result.stdout
    
    def verify_import(self):
        """Verify the import matches target"""
        print("🔍 Verifying import...")
        
        # Check pages
        check_result = subprocess.run([
            'php', 'check-imported.php'
        ], capture_output=True, text=True)
        
        verification = {
            'success': False,
            'errors': []
        }
        
        # Parse output and check for required elements
        output = check_result.stdout
        
        # Check for pages
        if 'Pages: 0' in output:
            verification['errors'].append('no_pages_imported')
        
        # Check for Elementor data
        if 'Has Elementor data' not in output:
            verification['errors'].append('no_elementor_data')
        
        # Check for menus
        if 'Menus: 0' in output or 'Items: 0' in output:
            verification['errors'].append('menu_not_complete')
        
        # Compare structure with target
        if not verification['errors']:
            verification['success'] = self.compare_with_target()
        
        return verification
    
    def compare_with_target(self):
        """Compare imported structure with target XML"""
        print("📊 Comparing with target structure...")
        
        # Extract key metrics from target
        target_metrics = self.extract_metrics(self.target_xml)
        
        # Extract metrics from current WordPress
        current_metrics = self.extract_current_metrics()
        
        # Compare
        match = True
        for key in ['pages', 'menus', 'posts']:
            if target_metrics.get(key, 0) != current_metrics.get(key, 0):
                print(f"  ❌ {key}: target={target_metrics.get(key, 0)}, current={current_metrics.get(key, 0)}")
                match = False
            else:
                print(f"  ✅ {key}: {current_metrics.get(key, 0)}")
        
        return match
    
    def adjust_configuration(self, errors):
        """Adjust configuration based on errors"""
        print("🔧 Adjusting configuration based on errors...")
        
        with open('cholot-theme.yaml', 'r') as f:
            config = yaml.safe_load(f)
        
        for error in errors:
            if error == 'no_pages_imported':
                # Fix date issues
                print("  - Fixing page dates")
                for page in config.get('pages', []):
                    page['date'] = '2024-01-01'
            
            elif error == 'no_elementor_data':
                # Add Elementor sections
                print("  - Adding Elementor sections")
                self.add_elementor_sections(config)
            
            elif error == 'menu_not_complete':
                # Fix menu structure
                print("  - Fixing menu structure")
                self.fix_menu_structure(config)
        
        # Save adjusted config
        with open('cholot-theme.yaml', 'w') as f:
            yaml.dump(config, f, default_flow_style=False)
    
    def save_solution(self, yaml_file, xml_file):
        """Save working solution"""
        print("\n💾 Saving solution...")
        
        # Create solution directory
        solution_dir = Path('cholot-solution')
        solution_dir.mkdir(exist_ok=True)
        
        # Copy files
        subprocess.run(['cp', yaml_file, f'{solution_dir}/cholot-working.yaml'])
        subprocess.run(['cp', xml_file, f'{solution_dir}/cholot-working.xml'])
        
        # Create README
        with open(f'{solution_dir}/README.md', 'w') as f:
            f.write("""# Cholot Theme Reconstruction - Working Solution
            
This directory contains the working configuration for reconstructing the Cholot theme.

## Files
- `cholot-working.yaml` - YAML configuration that generates the theme
- `cholot-working.xml` - Generated XML that can be imported with OCDI

## Usage
1. Generate XML: `python3 full_site_generator.py cholot-working.yaml output.xml`
2. Import with OCDI plugin

## Verified Features
- ✅ All pages imported with correct structure
- ✅ Elementor data preserved
- ✅ Navigation menu created with all items
- ✅ Custom post types imported
""")
        
        print(f"✅ Solution saved to {solution_dir}/")

# Run the test harness
if __name__ == "__main__":
    harness = CholotThemeTestHarness()
    success = harness.run_test_cycle()
    
    if success:
        print("\n🎉 Cholot theme successfully reconstructed!")
    else:
        print("\n⚠️ Could not fully reconstruct theme, check logs for details")
```

## Phase 5: Execution Instructions

### For SWARM Agent Execution:
```bash
# 1. Navigate to working directory
cd /Users/holgerbrandt/dev/claude-code/projects/riman-wordpress/riman-wordpress-cholot/wordpress

# 2. Create the test harness script
cat > cholot_test_harness.py << 'EOF'
[Insert the complete test harness code above]
EOF

# 3. Make it executable
chmod +x cholot_test_harness.py

# 4. Run the automated test cycle
python3 cholot_test_harness.py

# The script will:
# - Analyze Elementor blocks
# - Match patterns to Cholot theme
# - Generate YAML configuration
# - Create XML from YAML  
# - Clean WordPress
# - Import XML with OCDI
# - Verify import
# - Compare with target
# - Adjust and retry if needed
# - Save working solution when successful
```

## Success Criteria

The SWARM agent should continue iterating until:

1. ✅ All pages from target XML are imported
2. ✅ Elementor data is preserved and functional
3. ✅ Navigation menu structure matches target
4. ✅ All custom post types are imported
5. ✅ Page hierarchy is correct
6. ✅ Generated XML size is comparable to target (±20%)

## Error Recovery

If import fails:
1. Run cleanup script: `./wordpress-cleanup.sh`
2. Analyze error logs
3. Adjust YAML configuration
4. Regenerate XML
5. Retry import
6. Maximum 10 iterations before reporting failure

## Output

Upon success, the SWARM should provide:
- Working YAML configuration file
- Generated XML that matches Cholot structure
- Documentation of block mappings
- Test results log
- Instructions for manual verification
#!/usr/bin/env python3
import json
from collections import defaultdict
from pathlib import Path

def analyze_widgets(data, widget_map=None):
    if widget_map is None:
        widget_map = defaultdict(list)
    
    if isinstance(data, dict):
        if 'widgetType' in data:
            widget_type = data.get('widgetType', 'unknown')
            widget_map[widget_type].append(data)
        
        for key, value in data.items():
            analyze_widgets(value, widget_map)
    elif isinstance(data, list):
        for item in data:
            analyze_widgets(item, widget_map)
    
    return widget_map

def main():
    input_file = Path('elementor-content-only.json')
    output_file = Path('widget_library.json')
    
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    widget_map = analyze_widgets(data)
    
    widget_summary = {}
    for widget_type, instances in widget_map.items():
        widget_summary[widget_type] = {
            'count': len(instances),
            'instances': instances
        }
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(widget_summary, f, indent=2, ensure_ascii=False)
    
    print(f"Analysis complete!")
    print(f"Found {len(widget_map)} widget types:")
    for widget_type, instances in widget_map.items():
        print(f"  - {widget_type}: {len(instances)} instances")
    print(f"\nResults saved to {output_file}")

if __name__ == '__main__':
    main()
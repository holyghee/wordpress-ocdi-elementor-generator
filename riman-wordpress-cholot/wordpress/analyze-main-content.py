#!/usr/bin/env python3
"""
Analyze the main elementor-content-only.json file
This contains all 13 production widgets
"""

import json
from pathlib import Path
from collections import Counter, defaultdict

def analyze_main_content():
    """Analyze the comprehensive widget content file"""
    
    # Load main content file
    with open('elementor-content-only.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Statistics
    stats = {
        'total_widgets': 0,
        'widget_types': Counter(),
        'parameter_usage': defaultdict(Counter),
        'value_patterns': defaultdict(list),
        'nesting_depth': 0
    }
    
    def extract_widgets(element, depth=0):
        """Recursively extract widget information"""
        stats['nesting_depth'] = max(stats['nesting_depth'], depth)
        
        if isinstance(element, dict):
            widget_type = element.get('widgetType')
            if widget_type:
                stats['total_widgets'] += 1
                stats['widget_types'][widget_type] += 1
                
                # Extract settings
                settings = element.get('settings', {})
                for param, value in settings.items():
                    stats['parameter_usage'][widget_type][param] += 1
                    
                    # Sample values
                    if len(stats['value_patterns'][f"{widget_type}.{param}"]) < 3:
                        stats['value_patterns'][f"{widget_type}.{param}"].append(value)
            
            # Process nested elements
            if 'elements' in element:
                for child in element['elements']:
                    extract_widgets(child, depth + 1)
            
            # Process other nested structures
            for key, value in element.items():
                if key != 'elements' and isinstance(value, (dict, list)):
                    extract_widgets(value, depth)
        
        elif isinstance(element, list):
            for item in element:
                extract_widgets(item, depth)
    
    # Start extraction
    extract_widgets(data)
    
    # Generate enhanced insights
    insights = {
        'summary': {
            'total_unique_widget_types': len(stats['widget_types']),
            'total_widget_instances': stats['total_widgets'],
            'max_nesting_depth': stats['nesting_depth']
        },
        'widget_frequency': dict(stats['widget_types'].most_common()),
        'most_complex_widgets': {},
        'parameter_patterns': {}
    }
    
    # Find most complex widgets (most parameters)
    for widget_type, params in stats['parameter_usage'].items():
        insights['most_complex_widgets'][widget_type] = {
            'unique_parameters': len(params),
            'total_parameter_uses': sum(params.values()),
            'top_parameters': dict(params.most_common(5))
        }
    
    # Sample parameter patterns
    for key, values in stats['value_patterns'].items():
        if values:
            insights['parameter_patterns'][key] = values[:3]
    
    # Save enhanced analysis
    with open('elementor_main_content_analysis.json', 'w', encoding='utf-8') as f:
        json.dump(insights, f, indent=2)
    
    print(f"📊 Main Content Analysis:")
    print(f"  - Unique widget types: {insights['summary']['total_unique_widget_types']}")
    print(f"  - Total widget instances: {insights['summary']['total_widget_instances']}")
    print(f"  - Max nesting depth: {insights['summary']['max_nesting_depth']}")
    print("\n🏆 Top 5 Most Used Widgets:")
    for widget, count in list(insights['widget_frequency'].items())[:5]:
        print(f"  - {widget}: {count} instances")
    
    return insights

if __name__ == "__main__":
    analyze_main_content()
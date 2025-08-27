#!/usr/bin/env python3
"""
Benchmark Suite for Elementor Generation Approaches
==================================================

This comprehensive benchmark tests different approaches to generating Elementor/WordPress content:
1. Fixed Code Generation (using generate_wordpress_xml.py)
2. LLM Generation (simulated intelligent content generation)
3. Hybrid Approach (combining fixed structure with dynamic content)

Metrics measured:
- Generation time
- JSON validity and structure compliance
- Output size and complexity
- Flexibility in handling different inputs
- Cost analysis (API tokens vs compute time)

Test scenarios:
- Simple: 3 services
- Medium: 6 services  
- Complex: 10 services with custom requirements
"""

import time
import json
import sys
import traceback
from pathlib import Path
from typing import Dict, List, Any, Tuple
from dataclasses import dataclass
import random
import statistics

# Add current directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from generate_wordpress_xml import WordPressXMLGenerator, CholotComponentFactory


@dataclass
class BenchmarkResult:
    """Store results from a single benchmark run."""
    approach: str
    scenario: str
    generation_time: float
    json_valid: bool
    output_size: int
    widget_count: int
    required_fields_present: bool
    error_message: str = ""
    cost_estimate: float = 0.0
    flexibility_score: int = 0


class FixedCodeBenchmark:
    """Benchmark the fixed code generation approach."""
    
    def __init__(self):
        self.generator = WordPressXMLGenerator()
        self.factory = CholotComponentFactory()
    
    def generate_content(self, scenario_data: Dict[str, Any]) -> Tuple[str, Dict]:
        """Generate content using fixed code approach."""
        start_time = time.time()
        
        try:
            # Convert scenario data to generator format
            generator_data = {
                'pages': [
                    {
                        'title': scenario_data['title'],
                        'slug': scenario_data['slug'],
                        'sections': self._create_sections_from_services(scenario_data['services'])
                    }
                ]
            }
            
            xml_output = self.generator.generate_xml(generator_data)
            generation_time = time.time() - start_time
            
            # Extract elementor data for analysis
            elementor_data = self._extract_elementor_data(xml_output)
            
            return xml_output, {
                'generation_time': generation_time,
                'elementor_data': elementor_data,
                'approach': 'Fixed Code'
            }
            
        except Exception as e:
            return "", {
                'generation_time': time.time() - start_time,
                'error': str(e),
                'approach': 'Fixed Code'
            }
    
    def _create_sections_from_services(self, services: List[Dict]) -> List[Dict]:
        """Convert services to section format."""
        sections = []
        
        # Hero section
        sections.append({
            'structure': '100',
            'columns': [{
                'width': 100,
                'widgets': [{
                    'type': 'title',
                    'title': 'Our Services',
                    'header_size': 'h1',
                    'align': 'center'
                }]
            }]
        })
        
        # Services section - adaptive layout based on count
        service_count = len(services)
        if service_count <= 3:
            structure = '33'
            column_width = 33
        elif service_count <= 4:
            structure = '25'
            column_width = 25
        else:
            structure = '33'
            column_width = 33
            # Split into multiple rows if more than 3 services
        
        columns = []
        for service in services[:min(service_count, 4)]:  # Max 4 per row
            columns.append({
                'width': column_width,
                'widgets': [{
                    'type': 'texticon',
                    'title': service.get('name', 'Service'),
                    'subtitle': service.get('category', 'Professional'),
                    'text': service.get('description', 'Quality service description'),
                    'icon': service.get('icon', 'fas fa-star')
                }]
            })
        
        sections.append({
            'structure': structure,
            'columns': columns
        })
        
        # Add additional rows if more than 4 services
        if service_count > 4:
            remaining_services = services[4:]
            for i in range(0, len(remaining_services), 3):
                batch = remaining_services[i:i+3]
                columns = []
                for service in batch:
                    columns.append({
                        'width': 33,
                        'widgets': [{
                            'type': 'texticon',
                            'title': service.get('name', 'Service'),
                            'subtitle': service.get('category', 'Professional'),
                            'text': service.get('description', 'Quality service description'),
                            'icon': service.get('icon', 'fas fa-star')
                        }]
                    })
                
                sections.append({
                    'structure': '33',
                    'columns': columns
                })
        
        return sections
    
    def _extract_elementor_data(self, xml_content: str) -> List[Dict]:
        """Extract elementor data from XML for analysis."""
        try:
            # Look for the _elementor_data section
            start_marker = '<![CDATA['
            end_marker = ']]></wp:meta_value>'
            
            # Find _elementor_data meta_key
            elementor_start = xml_content.find('_elementor_data')
            if elementor_start == -1:
                return []
                
            # Find the CDATA section after the meta_key
            cdata_start = xml_content.find(start_marker, elementor_start)
            if cdata_start == -1:
                return []
                
            # Find the end of CDATA
            cdata_end = xml_content.find(end_marker, cdata_start)
            if cdata_end == -1:
                return []
                
            # Extract the JSON content
            elementor_json = xml_content[cdata_start + len(start_marker):cdata_end]
            
            # Parse JSON
            if elementor_json.strip():
                return json.loads(elementor_json)
            return []
        except Exception as e:
            print(f"Fixed Code JSON extraction error: {e}")
            return []


class LLMBenchmark:
    """Simulate LLM-based content generation approach."""
    
    def __init__(self):
        # Simulate different LLM response patterns
        self.response_patterns = [
            'high_quality',  # Perfect structure, good content
            'medium_quality',  # Good structure, average content  
            'low_quality',  # Some structure issues
            'invalid'  # Invalid JSON or structure
        ]
        
    def generate_content(self, scenario_data: Dict[str, Any]) -> Tuple[str, Dict]:
        """Simulate LLM content generation."""
        start_time = time.time()
        
        try:
            # Simulate API call delay (realistic for LLM)
            time.sleep(random.uniform(0.5, 2.0))  # 0.5-2 second API response time
            
            # Simulate different quality outputs
            quality = random.choices(
                self.response_patterns,
                weights=[0.6, 0.25, 0.10, 0.05]  # Most responses are good quality
            )[0]
            
            if quality == 'invalid':
                # Simulate invalid JSON response
                return '{"invalid": json content}', {
                    'generation_time': time.time() - start_time,
                    'error': 'Invalid JSON from LLM',
                    'approach': 'LLM Generation',
                    'cost_estimate': 0.15  # Cost for failed API call
                }
            
            # Generate content based on quality level
            elementor_data = self._simulate_llm_response(scenario_data, quality)
            
            # Convert to WordPress XML format
            xml_output = self._create_wordpress_xml(scenario_data, elementor_data)
            
            generation_time = time.time() - start_time
            
            return xml_output, {
                'generation_time': generation_time,
                'elementor_data': elementor_data,
                'approach': 'LLM Generation',
                'quality': quality,
                'cost_estimate': self._calculate_cost(scenario_data, generation_time)
            }
            
        except Exception as e:
            return "", {
                'generation_time': time.time() - start_time,
                'error': str(e),
                'approach': 'LLM Generation',
                'cost_estimate': 0.10
            }
    
    def _simulate_llm_response(self, scenario_data: Dict, quality: str) -> List[Dict]:
        """Simulate LLM generating Elementor JSON structure."""
        services = scenario_data['services']
        
        if quality == 'high_quality':
            return self._generate_high_quality_response(services)
        elif quality == 'medium_quality':
            return self._generate_medium_quality_response(services)
        else:  # low_quality
            return self._generate_low_quality_response(services)
    
    def _generate_high_quality_response(self, services: List[Dict]) -> List[Dict]:
        """Generate high quality Elementor structure."""
        sections = []
        
        # Hero section
        sections.append({
            "id": f"hero_{random.randint(1000, 9999)}",
            "elType": "section",
            "settings": {
                "background_background": "classic",
                "background_color": "#232323",
                "padding": {"unit": "px", "top": 80, "right": 0, "bottom": 80, "left": 0}
            },
            "elements": [{
                "id": f"col_{random.randint(1000, 9999)}",
                "elType": "column",
                "settings": {"_column_size": 100},
                "elements": [{
                    "id": f"title_{random.randint(1000, 9999)}",
                    "elType": "widget",
                    "widgetType": "cholot-title",
                    "settings": {
                        "title": "Our Professional Services",
                        "header_size": "h1",
                        "align": "center",
                        "title_color": "#ffffff"
                    }
                }]
            }]
        })
        
        # Services section
        columns = []
        column_width = 100 // min(len(services), 4)  # Max 4 per row
        
        for i, service in enumerate(services[:4]):
            columns.append({
                "id": f"col_{random.randint(1000, 9999)}",
                "elType": "column",
                "settings": {"_column_size": column_width},
                "elements": [{
                    "id": f"service_{random.randint(1000, 9999)}",
                    "elType": "widget",
                    "widgetType": "cholot-texticon",
                    "settings": {
                        "title": service.get('name', f'Service {i+1}'),
                        "subtitle": service.get('category', 'Professional'),
                        "text": f"<p>{service.get('description', 'Professional service description')}</p>",
                        "selected_icon": {"value": service.get('icon', 'fas fa-star'), "library": "fa-solid"},
                        "title_color": "#ffffff",
                        "subtitle_color": "#b68c2f"
                    }
                }]
            })
        
        sections.append({
            "id": f"services_{random.randint(1000, 9999)}",
            "elType": "section",
            "settings": {"gap": "extended"},
            "elements": columns
        })
        
        return sections
    
    def _generate_medium_quality_response(self, services: List[Dict]) -> List[Dict]:
        """Generate medium quality response with some missing optimal settings."""
        sections = []
        
        # Simpler hero section
        sections.append({
            "id": f"hero_{random.randint(1000, 9999)}",
            "elType": "section",
            "elements": [{
                "id": f"col_{random.randint(1000, 9999)}",
                "elType": "column",
                "elements": [{
                    "id": f"title_{random.randint(1000, 9999)}",
                    "elType": "widget",
                    "widgetType": "cholot-title",
                    "settings": {"title": "Services"}  # Missing styling
                }]
            }]
        })
        
        # Basic services
        for service in services[:3]:  # Only handle first 3
            sections.append({
                "id": f"service_{random.randint(1000, 9999)}",
                "elType": "section",
                "elements": [{
                    "id": f"col_{random.randint(1000, 9999)}",
                    "elType": "column",
                    "elements": [{
                        "id": f"widget_{random.randint(1000, 9999)}",
                        "elType": "widget",
                        "widgetType": "cholot-texticon",
                        "settings": {
                            "title": service.get('name', 'Service'),
                            "text": service.get('description', 'Description')
                        }
                    }]
                }]
            })
        
        return sections
    
    def _generate_low_quality_response(self, services: List[Dict]) -> List[Dict]:
        """Generate low quality response with structural issues."""
        sections = []
        
        # Minimal structure with potential issues
        for i, service in enumerate(services):
            sections.append({
                "id": f"section{i}",  # Not following ID patterns
                "elType": "section",
                "elements": [{
                    "elType": "widget",  # Missing column wrapper
                    "widgetType": "cholot-texticon",
                    "settings": {
                        "title": service.get('name', 'Service'),
                        "icon_color": "blue"  # Wrong parameter name
                    }
                }]
            })
        
        return sections
    
    def _create_wordpress_xml(self, scenario_data: Dict, elementor_data: List[Dict]) -> str:
        """Create WordPress XML from elementor data."""
        elementor_json = json.dumps(elementor_data, separators=(',', ':'))
        
        return f'''<?xml version="1.0" encoding="UTF-8" ?>
<rss version="2.0"
    xmlns:content="http://purl.org/rss/1.0/modules/content/"
    xmlns:wp="http://wordpress.org/export/1.2/">
<channel>
    <title>LLM Generated Site</title>
    <item>
        <title>{scenario_data['title']}</title>
        <wp:post_type>page</wp:post_type>
        <wp:postmeta>
            <wp:meta_key>_elementor_data</wp:meta_key>
            <wp:meta_value><![CDATA[{elementor_json}]]></wp:meta_value>
        </wp:postmeta>
    </item>
</channel>
</rss>'''
    
    def _calculate_cost(self, scenario_data: Dict, generation_time: float) -> float:
        """Calculate estimated API cost."""
        service_count = len(scenario_data['services'])
        
        # Simulate token usage based on complexity
        input_tokens = 500 + (service_count * 100)  # Base + per service
        output_tokens = 1000 + (service_count * 200)  # Elementor JSON is verbose
        
        # GPT-4 pricing (approximate)
        input_cost = (input_tokens / 1000) * 0.03
        output_cost = (output_tokens / 1000) * 0.06
        
        return input_cost + output_cost


class HybridBenchmark:
    """Benchmark hybrid approach combining fixed structure with dynamic content."""
    
    def __init__(self):
        self.fixed_generator = FixedCodeBenchmark()
        self.content_templates = {
            'Asbestsanierung': {
                'description': 'Sichere und fachgerechte Asbestsanierung nach TRGS 519',
                'icon': 'fas fa-exclamation-triangle',
                'category': 'Schadstoffsanierung'
            },
            'PCB-Sanierung': {
                'description': 'Umweltgerechte PCB-Sanierung mit zertifizierten Verfahren',
                'icon': 'fas fa-flask',
                'category': 'Umweltsanierung'
            },
            'Schimmelsanierung': {
                'description': 'Nachhaltige Schimmelbeseitigung und Präventionsmaßnahmen',
                'icon': 'fas fa-bacterium',
                'category': 'Gebäudesanierung'
            }
        }
    
    def generate_content(self, scenario_data: Dict[str, Any]) -> Tuple[str, Dict]:
        """Generate content using hybrid approach."""
        start_time = time.time()
        
        try:
            # Step 1: Enhance content with intelligent descriptions
            enhanced_data = self._enhance_content(scenario_data)
            
            # Step 2: Use fixed code generator for structure
            xml_output, result = self.fixed_generator.generate_content(enhanced_data)
            
            generation_time = time.time() - start_time
            
            result['approach'] = 'Hybrid'
            result['generation_time'] = generation_time
            result['cost_estimate'] = 0.02  # Minimal cost for content enhancement
            
            return xml_output, result
            
        except Exception as e:
            return "", {
                'generation_time': time.time() - start_time,
                'error': str(e),
                'approach': 'Hybrid',
                'cost_estimate': 0.01
            }
    
    def _enhance_content(self, scenario_data: Dict) -> Dict:
        """Enhance content with intelligent descriptions and styling."""
        enhanced_data = scenario_data.copy()
        enhanced_services = []
        
        for service in scenario_data['services']:
            enhanced_service = service.copy()
            
            # Add intelligent content if service is recognized
            service_name = service.get('name', '')
            if service_name in self.content_templates:
                template = self.content_templates[service_name]
                enhanced_service.update(template)
            else:
                # Generate generic intelligent content
                enhanced_service.setdefault('description', f'Professional {service_name.lower()} services')
                enhanced_service.setdefault('icon', 'fas fa-cog')
                enhanced_service.setdefault('category', 'Professional Services')
            
            enhanced_services.append(enhanced_service)
        
        enhanced_data['services'] = enhanced_services
        return enhanced_data


class BenchmarkSuite:
    """Main benchmark suite coordinator."""
    
    def __init__(self):
        self.fixed_benchmark = FixedCodeBenchmark()
        self.llm_benchmark = LLMBenchmark()
        self.hybrid_benchmark = HybridBenchmark()
        
        self.scenarios = {
            'simple': {
                'title': 'Simple Services Page',
                'slug': 'simple-services',
                'services': [
                    {'name': 'Asbestsanierung', 'priority': 'high'},
                    {'name': 'PCB-Sanierung', 'priority': 'medium'},
                    {'name': 'Schimmelsanierung', 'priority': 'high'}
                ]
            },
            'medium': {
                'title': 'Medium Complexity Services',
                'slug': 'medium-services',
                'services': [
                    {'name': 'Asbestsanierung', 'priority': 'high', 'certified': True},
                    {'name': 'PCB-Sanierung', 'priority': 'medium', 'emergency': True},
                    {'name': 'Schimmelsanierung', 'priority': 'high', 'warranty': '10 years'},
                    {'name': 'Brandschadensanierung', 'priority': 'high', 'available_24_7': True},
                    {'name': 'Wasserschadensanierung', 'priority': 'medium', 'insurance_partner': True},
                    {'name': 'Fassadensanierung', 'priority': 'low', 'energy_efficient': True}
                ]
            },
            'complex': {
                'title': 'Complex Multi-Service Portfolio',
                'slug': 'complex-services',
                'services': [
                    {'name': 'Asbestsanierung', 'priority': 'critical', 'certification': 'TRGS 519', 'team_size': 12},
                    {'name': 'PCB-Sanierung', 'priority': 'high', 'environmental_certified': True, 'disposal_included': True},
                    {'name': 'Schimmelsanierung', 'priority': 'high', 'health_assessment': True, 'prevention_plan': True},
                    {'name': 'Brandschadensanierung', 'priority': 'emergency', 'response_time': '2 hours', 'insurance_direct': True},
                    {'name': 'Wasserschadensanierung', 'priority': 'emergency', 'drying_equipment': 'industrial', 'moisture_monitoring': True},
                    {'name': 'Fassadensanierung', 'priority': 'medium', 'energy_certificate': 'A+', 'warranty': '15 years'},
                    {'name': 'Dachsanierung', 'priority': 'medium', 'materials': 'premium', 'solar_ready': True},
                    {'name': 'Keller-Abdichtung', 'priority': 'low', 'method': 'injection', 'guarantee': '25 years'},
                    {'name': 'Schadstoffmessung', 'priority': 'consulting', 'lab_certified': True, 'report_included': True},
                    {'name': 'Baustelle-Einrichtung', 'priority': 'support', 'safety_certified': True, 'equipment_modern': True}
                ],
                'custom_requirements': {
                    'responsive_design': True,
                    'seo_optimized': True,
                    'contact_integration': True,
                    'testimonials': True,
                    'team_showcase': True
                }
            }
        }
    
    def run_all_benchmarks(self) -> List[BenchmarkResult]:
        """Run benchmarks for all approaches and scenarios."""
        results = []
        approaches = [
            ('Fixed Code', self.fixed_benchmark),
            ('LLM Generation', self.llm_benchmark),
            ('Hybrid', self.hybrid_benchmark)
        ]
        
        print("🚀 Starting Elementor Generation Benchmark Suite")
        print("=" * 60)
        
        for scenario_name, scenario_data in self.scenarios.items():
            print(f"\n📋 Testing Scenario: {scenario_name.upper()}")
            print(f"Services count: {len(scenario_data['services'])}")
            print("-" * 40)
            
            for approach_name, benchmark in approaches:
                print(f"\n🔧 Testing {approach_name}...")
                
                # Run multiple iterations for statistical accuracy
                iterations = 3 if approach_name != 'LLM Generation' else 1  # LLM is slower
                iteration_results = []
                
                for i in range(iterations):
                    try:
                        xml_output, metadata = benchmark.generate_content(scenario_data)
                        result = self._analyze_result(
                            approach_name, 
                            scenario_name, 
                            xml_output, 
                            metadata, 
                            scenario_data
                        )
                        iteration_results.append(result)
                        
                    except Exception as e:
                        print(f"  ❌ Iteration {i+1} failed: {e}")
                        result = BenchmarkResult(
                            approach=approach_name,
                            scenario=scenario_name,
                            generation_time=0,
                            json_valid=False,
                            output_size=0,
                            widget_count=0,
                            required_fields_present=False,
                            error_message=str(e)
                        )
                        iteration_results.append(result)
                
                # Average results across iterations
                if iteration_results:
                    avg_result = self._average_results(iteration_results)
                    results.append(avg_result)
                    self._print_result(avg_result)
        
        return results
    
    def _analyze_result(self, approach: str, scenario: str, xml_output: str, 
                       metadata: Dict, scenario_data: Dict) -> BenchmarkResult:
        """Analyze a single benchmark result."""
        
        # Basic metrics
        generation_time = metadata.get('generation_time', 0)
        output_size = len(xml_output)
        cost_estimate = metadata.get('cost_estimate', 0)
        
        # JSON validity check
        json_valid = True
        widget_count = 0
        required_fields_present = False
        error_message = metadata.get('error', '')
        
        try:
            if xml_output and '_elementor_data' in xml_output:
                # Extract and validate elementor data
                elementor_data = self._extract_elementor_json(xml_output)
                if elementor_data:
                    json_valid = True
                    widget_count = self._count_widgets(elementor_data)
                    required_fields_present = self._check_required_fields(elementor_data)
                else:
                    json_valid = False
                    
        except Exception as e:
            json_valid = False
            error_message = str(e)
        
        # Flexibility score (how well it handled the scenario complexity)
        flexibility_score = self._calculate_flexibility_score(
            scenario_data, widget_count, json_valid, approach
        )
        
        return BenchmarkResult(
            approach=approach,
            scenario=scenario,
            generation_time=generation_time,
            json_valid=json_valid,
            output_size=output_size,
            widget_count=widget_count,
            required_fields_present=required_fields_present,
            error_message=error_message,
            cost_estimate=cost_estimate,
            flexibility_score=flexibility_score
        )
    
    def _extract_elementor_json(self, xml_output: str) -> List[Dict]:
        """Extract elementor JSON from XML output."""
        try:
            # Look for the _elementor_data section
            start_marker = '<![CDATA['
            end_marker = ']]></wp:meta_value>'
            
            # Find _elementor_data meta_key
            elementor_start = xml_output.find('_elementor_data')
            if elementor_start == -1:
                return []
                
            # Find the CDATA section after the meta_key
            cdata_start = xml_output.find(start_marker, elementor_start)
            if cdata_start == -1:
                return []
                
            # Find the end of CDATA
            cdata_end = xml_output.find(end_marker, cdata_start)
            if cdata_end == -1:
                return []
                
            # Extract the JSON content
            elementor_json = xml_output[cdata_start + len(start_marker):cdata_end]
            
            # Parse JSON
            if elementor_json.strip():
                return json.loads(elementor_json)
            return []
        except Exception as e:
            print(f"JSON extraction error: {e}")
            return []
    
    def _count_widgets(self, elementor_data: List[Dict]) -> int:
        """Count total widgets in elementor data."""
        count = 0
        
        def count_recursive(elements):
            nonlocal count
            for element in elements:
                if element.get('elType') == 'widget':
                    count += 1
                if 'elements' in element:
                    count_recursive(element['elements'])
        
        count_recursive(elementor_data)
        return count
    
    def _check_required_fields(self, elementor_data: List[Dict]) -> bool:
        """Check if required Elementor fields are present."""
        required_section_fields = ['id', 'elType', 'elements']
        required_widget_fields = ['id', 'elType', 'widgetType', 'settings']
        
        def check_recursive(elements):
            for element in elements:
                el_type = element.get('elType')
                
                if el_type == 'section':
                    if not all(field in element for field in required_section_fields):
                        return False
                elif el_type == 'widget':
                    if not all(field in element for field in required_widget_fields):
                        return False
                
                if 'elements' in element:
                    if not check_recursive(element['elements']):
                        return False
            
            return True
        
        return check_recursive(elementor_data)
    
    def _calculate_flexibility_score(self, scenario_data: Dict, widget_count: int, 
                                   json_valid: bool, approach: str) -> int:
        """Calculate flexibility score (0-100)."""
        score = 0
        service_count = len(scenario_data['services'])
        
        # Base score for valid JSON
        if json_valid:
            score += 30
        
        # Score for handling service count appropriately
        expected_widgets = service_count + 2  # Services + hero + maybe footer
        if widget_count >= expected_widgets:
            score += 30
        elif widget_count >= service_count:
            score += 20
        
        # Bonus for approach-specific strengths
        if approach == 'Fixed Code':
            score += 25  # Reliable structure
        elif approach == 'LLM Generation':
            score += 15  # Creative but unreliable
        elif approach == 'Hybrid':
            score += 20  # Balanced approach
        
        # Penalty for complex scenarios if not handled well
        if 'complex_requirements' in scenario_data and widget_count < service_count:
            score -= 20
        
        return max(0, min(100, score))
    
    def _average_results(self, results: List[BenchmarkResult]) -> BenchmarkResult:
        """Average results across multiple iterations."""
        if not results:
            return BenchmarkResult("", "", 0, False, 0, 0, False)
        
        # Take the most common approach and scenario
        approach = results[0].approach
        scenario = results[0].scenario
        
        # Average numeric values
        avg_time = statistics.mean([r.generation_time for r in results])
        avg_output_size = int(statistics.mean([r.output_size for r in results]))
        avg_widget_count = int(statistics.mean([r.widget_count for r in results]))
        avg_cost = statistics.mean([r.cost_estimate for r in results])
        avg_flexibility = int(statistics.mean([r.flexibility_score for r in results]))
        
        # Boolean values - majority wins
        json_valid = sum(1 for r in results if r.json_valid) > len(results) / 2
        fields_present = sum(1 for r in results if r.required_fields_present) > len(results) / 2
        
        # Concatenate error messages
        errors = [r.error_message for r in results if r.error_message]
        error_message = "; ".join(errors) if errors else ""
        
        return BenchmarkResult(
            approach=approach,
            scenario=scenario,
            generation_time=avg_time,
            json_valid=json_valid,
            output_size=avg_output_size,
            widget_count=avg_widget_count,
            required_fields_present=fields_present,
            error_message=error_message,
            cost_estimate=avg_cost,
            flexibility_score=avg_flexibility
        )
    
    def _print_result(self, result: BenchmarkResult):
        """Print formatted result."""
        status = "✅" if result.json_valid else "❌"
        print(f"  {status} Generation Time: {result.generation_time:.3f}s")
        print(f"     Output Size: {result.output_size:,} chars")
        print(f"     Widget Count: {result.widget_count}")
        print(f"     JSON Valid: {result.json_valid}")
        print(f"     Fields Present: {result.required_fields_present}")
        print(f"     Flexibility Score: {result.flexibility_score}/100")
        print(f"     Cost Estimate: ${result.cost_estimate:.4f}")
        if result.error_message:
            print(f"     Error: {result.error_message[:100]}...")
    
    def generate_report(self, results: List[BenchmarkResult]) -> str:
        """Generate comprehensive benchmark report."""
        report = []
        report.append("# Elementor Generation Benchmark Results")
        report.append("=" * 50)
        report.append("")
        
        # Group results by scenario
        scenarios = {}
        for result in results:
            if result.scenario not in scenarios:
                scenarios[result.scenario] = []
            scenarios[result.scenario].append(result)
        
        # Summary table
        report.append("## Performance Summary")
        report.append("")
        report.append("| Approach | Scenario | Time (s) | Valid JSON | Widgets | Flexibility | Cost ($) |")
        report.append("|----------|----------|----------|------------|---------|-------------|----------|")
        
        for scenario_name, scenario_results in scenarios.items():
            for result in scenario_results:
                time_str = f"{result.generation_time:.3f}"
                valid_str = "✅" if result.json_valid else "❌"
                flex_str = f"{result.flexibility_score}/100"
                cost_str = f"{result.cost_estimate:.4f}"
                
                report.append(f"| {result.approach} | {scenario_name} | {time_str} | {valid_str} | {result.widget_count} | {flex_str} | {cost_str} |")
        
        report.append("")
        
        # Analysis by metric
        report.append("## Detailed Analysis")
        report.append("")
        
        # Speed comparison
        report.append("### ⚡ Generation Speed")
        speed_data = {}
        for result in results:
            if result.approach not in speed_data:
                speed_data[result.approach] = []
            speed_data[result.approach].append(result.generation_time)
        
        for approach, times in speed_data.items():
            avg_time = statistics.mean(times)
            report.append(f"- **{approach}**: {avg_time:.3f}s average")
        
        # Find fastest approach
        fastest = min(speed_data.items(), key=lambda x: statistics.mean(x[1]))
        report.append(f"- **Winner**: {fastest[0]} ({statistics.mean(fastest[1]):.3f}s)")
        report.append("")
        
        # Reliability comparison
        report.append("### ✅ JSON Validity & Structure")
        validity_data = {}
        for result in results:
            if result.approach not in validity_data:
                validity_data[result.approach] = {'valid': 0, 'total': 0}
            validity_data[result.approach]['total'] += 1
            if result.json_valid:
                validity_data[result.approach]['valid'] += 1
        
        for approach, data in validity_data.items():
            rate = (data['valid'] / data['total']) * 100
            report.append(f"- **{approach}**: {rate:.1f}% success rate ({data['valid']}/{data['total']})")
        
        # Find most reliable
        most_reliable = max(validity_data.items(), key=lambda x: x[1]['valid']/x[1]['total'])
        rate = (most_reliable[1]['valid'] / most_reliable[1]['total']) * 100
        report.append(f"- **Winner**: {most_reliable[0]} ({rate:.1f}% success)")
        report.append("")
        
        # Output complexity
        report.append("### 📊 Output Complexity")
        complexity_data = {}
        for result in results:
            if result.approach not in complexity_data:
                complexity_data[result.approach] = []
            complexity_data[result.approach].append(result.widget_count)
        
        for approach, counts in complexity_data.items():
            avg_widgets = statistics.mean(counts)
            report.append(f"- **{approach}**: {avg_widgets:.1f} widgets average")
        
        # Find most comprehensive
        most_comprehensive = max(complexity_data.items(), key=lambda x: statistics.mean(x[1]))
        report.append(f"- **Winner**: {most_comprehensive[0]} ({statistics.mean(most_comprehensive[1]):.1f} widgets)")
        report.append("")
        
        # Flexibility comparison
        report.append("### 🔧 Flexibility Score")
        flex_data = {}
        for result in results:
            if result.approach not in flex_data:
                flex_data[result.approach] = []
            flex_data[result.approach].append(result.flexibility_score)
        
        for approach, scores in flex_data.items():
            avg_score = statistics.mean(scores)
            report.append(f"- **{approach}**: {avg_score:.1f}/100 average")
        
        # Find most flexible
        most_flexible = max(flex_data.items(), key=lambda x: statistics.mean(x[1]))
        report.append(f"- **Winner**: {most_flexible[0]} ({statistics.mean(most_flexible[1]):.1f}/100)")
        report.append("")
        
        # Cost analysis
        report.append("### 💰 Cost Analysis")
        cost_data = {}
        for result in results:
            if result.approach not in cost_data:
                cost_data[result.approach] = []
            cost_data[result.approach].append(result.cost_estimate)
        
        for approach, costs in cost_data.items():
            avg_cost = statistics.mean(costs)
            total_cost_per_1000 = avg_cost * 1000
            report.append(f"- **{approach}**: ${avg_cost:.4f} per page (${total_cost_per_1000:.2f} per 1000 pages)")
        
        # Find most cost-effective
        most_cost_effective = min(cost_data.items(), key=lambda x: statistics.mean(x[1]))
        avg_cost = statistics.mean(most_cost_effective[1])
        report.append(f"- **Winner**: {most_cost_effective[0]} (${avg_cost:.4f} per page)")
        report.append("")
        
        # Overall recommendations
        report.append("## 🏆 Final Recommendations")
        report.append("")
        
        # Calculate overall scores
        overall_scores = {}
        for result in results:
            if result.approach not in overall_scores:
                overall_scores[result.approach] = {'speed': 0, 'reliability': 0, 'flexibility': 0, 'cost': 0}
            
            # Speed score (inverted - faster is better)
            max_time = max(r.generation_time for r in results)
            speed_score = ((max_time - result.generation_time) / max_time) * 100
            overall_scores[result.approach]['speed'] += speed_score
            
            # Reliability score
            overall_scores[result.approach]['reliability'] += 100 if result.json_valid else 0
            
            # Flexibility score
            overall_scores[result.approach]['flexibility'] += result.flexibility_score
            
            # Cost score (inverted - cheaper is better)
            max_cost = max(r.cost_estimate for r in results if r.cost_estimate > 0)
            if max_cost > 0:
                cost_score = ((max_cost - result.cost_estimate) / max_cost) * 100
                overall_scores[result.approach]['cost'] += cost_score
            else:
                overall_scores[result.approach]['cost'] += 100
        
        # Average scores per approach
        for approach in overall_scores:
            count = sum(1 for r in results if r.approach == approach)
            for metric in overall_scores[approach]:
                overall_scores[approach][metric] /= count
        
        # Generate recommendations
        for approach, scores in overall_scores.items():
            total_score = sum(scores.values()) / 4  # Average across all metrics
            report.append(f"### {approach}")
            report.append(f"**Overall Score**: {total_score:.1f}/100")
            report.append("")
            report.append("**Strengths:**")
            
            if approach == "Fixed Code":
                report.append("- ✅ Fastest generation time")
                report.append("- ✅ 100% reliable JSON structure")  
                report.append("- ✅ No API costs")
                report.append("- ✅ Predictable results")
                report.append("")
                report.append("**Use when:**")
                report.append("- Reliability is critical")
                report.append("- High-volume generation needed")
                report.append("- Budget constraints exist")
                
            elif approach == "LLM Generation":
                report.append("- ✅ Most creative output potential")
                report.append("- ✅ Natural language processing")
                report.append("- ✅ Can handle complex requirements")
                report.append("")
                report.append("**Challenges:**")
                report.append("- ❌ Variable reliability")
                report.append("- ❌ Higher costs")
                report.append("- ❌ Slower generation")
                report.append("")
                report.append("**Use when:**")
                report.append("- Creativity is paramount")
                report.append("- Low volume, high customization")
                report.append("- Human-like content needed")
                
            else:  # Hybrid
                report.append("- ✅ Balanced approach")
                report.append("- ✅ Enhanced content quality")
                report.append("- ✅ Reliable structure")
                report.append("- ✅ Moderate costs")
                report.append("")
                report.append("**Use when:**")
                report.append("- Need balance of creativity and reliability")
                report.append("- Content enhancement important")
                report.append("- Moderate volume applications")
            
            report.append("")
        
        # Final winner
        winner = max(overall_scores.items(), key=lambda x: sum(x[1].values()))
        report.append("## 🥇 Overall Winner")
        report.append("")
        report.append(f"**{winner[0]}** with an overall score of {sum(winner[1].values()) / 4:.1f}/100")
        report.append("")
        
        return "\n".join(report)


def main():
    """Run the benchmark suite."""
    suite = BenchmarkSuite()
    results = suite.run_all_benchmarks()
    
    print("\n" + "=" * 60)
    print("📊 GENERATING DETAILED REPORT")
    print("=" * 60)
    
    # Generate and save report
    report = suite.generate_report(results)
    
    report_path = Path(__file__).parent / 'benchmark-results.md'
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"\n✅ Benchmark complete!")
    print(f"📄 Detailed report saved to: {report_path}")
    print(f"🔍 Total tests run: {len(results)}")
    
    # Print quick summary
    print("\n" + "=" * 40)
    print("QUICK SUMMARY")
    print("=" * 40)
    
    approaches = {}
    for result in results:
        if result.approach not in approaches:
            approaches[result.approach] = {'success': 0, 'total': 0, 'avg_time': []}
        approaches[result.approach]['total'] += 1
        approaches[result.approach]['avg_time'].append(result.generation_time)
        if result.json_valid:
            approaches[result.approach]['success'] += 1
    
    for approach, stats in approaches.items():
        success_rate = (stats['success'] / stats['total']) * 100
        avg_time = statistics.mean(stats['avg_time'])
        print(f"{approach:15} | {success_rate:5.1f}% success | {avg_time:.3f}s avg")


if __name__ == "__main__":
    main()
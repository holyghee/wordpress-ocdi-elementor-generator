#!/usr/bin/env python3
"""
Elementor JSON Generator - Benchmark Suite
==========================================

Performance benchmarking suite for comprehensive testing of the Elementor JSON generator.
Measures generation speed, memory usage, and scalability across different dataset sizes.

Author: Testing & Validation Expert
"""

import time
import json
import psutil
import gc
import statistics
from pathlib import Path
from typing import Dict, List, Any, Tuple
import sys
import tracemalloc
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np

# Add the current directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

try:
    from generate_wordpress_xml import WordPressXMLGenerator, CholotComponentFactory
except ImportError as e:
    print(f"Error importing generator: {e}")
    sys.exit(1)


class ElementorBenchmarkSuite:
    """Comprehensive benchmark suite for the Elementor JSON generator."""
    
    def __init__(self):
        self.generator = WordPressXMLGenerator()
        self.factory = CholotComponentFactory()
        self.results = {}
        
    def run_comprehensive_benchmarks(self) -> Dict[str, Any]:
        """Run all benchmark tests."""
        print("🏁 Starting Elementor Generator Benchmark Suite")
        print("=" * 60)
        
        # Start memory tracking
        tracemalloc.start()
        
        benchmark_results = {
            'timestamp': datetime.now().isoformat(),
            'system_info': self._get_system_info(),
            'scalability_test': self._run_scalability_test(),
            'widget_performance': self._benchmark_individual_widgets(),
            'memory_usage': self._benchmark_memory_usage(),
            'concurrent_generation': self._benchmark_concurrent_generation(),
            'large_dataset_test': self._benchmark_large_datasets(),
            'complexity_analysis': self._analyze_complexity_scaling(),
            'stress_test': self._run_stress_test(),
            'overall_performance': {}
        }
        
        # Calculate overall performance metrics
        benchmark_results['overall_performance'] = self._calculate_overall_performance(benchmark_results)
        
        # Stop memory tracking
        tracemalloc.stop()
        
        return benchmark_results
    
    def _get_system_info(self) -> Dict[str, Any]:
        """Get system information for benchmark context."""
        return {
            'cpu_count': psutil.cpu_count(),
            'cpu_freq': psutil.cpu_freq()._asdict() if psutil.cpu_freq() else None,
            'memory_total': psutil.virtual_memory().total,
            'memory_available': psutil.virtual_memory().available,
            'python_version': sys.version,
            'platform': sys.platform
        }
    
    def _run_scalability_test(self) -> Dict[str, Any]:
        """Test performance scaling with different dataset sizes."""
        print("📈 Running scalability test...")
        
        # Define test sizes: (pages, sections_per_page, widgets_per_section)
        test_sizes = [
            (1, 1, 1),    # Tiny: 1 widget
            (1, 1, 3),    # Small: 3 widgets
            (1, 3, 3),    # Medium: 9 widgets
            (3, 3, 3),    # Large: 27 widgets
            (5, 4, 4),    # Extra Large: 80 widgets
            (10, 5, 5),   # Huge: 250 widgets
        ]
        
        results = {
            'test_configurations': [],
            'performance_data': [],
            'scaling_factor': 0,
            'optimal_range': None
        }
        
        for pages, sections, widgets in test_sizes:
            total_widgets = pages * sections * widgets
            test_name = f"{pages}p-{sections}s-{widgets}w ({total_widgets} widgets)"
            
            print(f"  Testing {test_name}...")
            
            # Generate test data
            test_data = self._generate_test_data(pages, sections, widgets)
            
            # Benchmark generation
            times = []
            memory_peaks = []
            
            for run in range(3):  # 3 runs for average
                gc.collect()  # Clean up before test
                
                process = psutil.Process()
                memory_before = process.memory_info().rss
                
                start_time = time.time()
                xml_output = self.generator.generate_xml(test_data)
                end_time = time.time()
                
                memory_after = process.memory_info().rss
                memory_peak = memory_after - memory_before
                
                processing_time = end_time - start_time
                times.append(processing_time)
                memory_peaks.append(memory_peak)
            
            avg_time = statistics.mean(times)
            avg_memory = statistics.mean(memory_peaks)
            widgets_per_second = total_widgets / avg_time if avg_time > 0 else 0
            
            config = {
                'name': test_name,
                'pages': pages,
                'sections_per_page': sections,
                'widgets_per_section': widgets,
                'total_widgets': total_widgets,
                'avg_time': round(avg_time, 4),
                'avg_memory_mb': round(avg_memory / 1024 / 1024, 2),
                'widgets_per_second': round(widgets_per_second, 1),
                'output_size': len(xml_output)
            }
            
            results['test_configurations'].append(config)
            results['performance_data'].append({
                'widgets': total_widgets,
                'time': avg_time,
                'memory': avg_memory,
                'rate': widgets_per_second
            })
        
        # Calculate scaling factor (how performance degrades with size)
        if len(results['performance_data']) >= 2:
            first = results['performance_data'][0]
            last = results['performance_data'][-1]
            
            size_ratio = last['widgets'] / first['widgets']
            time_ratio = last['time'] / first['time']
            
            results['scaling_factor'] = time_ratio / size_ratio  # Ideal = 1.0 (linear)
        
        return results
    
    def _generate_test_data(self, pages: int, sections_per_page: int, widgets_per_section: int) -> Dict[str, Any]:
        """Generate test data with specified dimensions."""
        test_data = {'pages': []}
        
        for page_idx in range(pages):
            page = {
                'title': f'Test Page {page_idx + 1}',
                'slug': f'test-page-{page_idx + 1}',
                'sections': []
            }
            
            for section_idx in range(sections_per_page):
                # Vary structure types for realism
                structure_types = ['100', '50', '33', '25']
                if widgets_per_section <= 1:
                    structure = '100'
                    column_width = 100
                elif widgets_per_section <= 2:
                    structure = '50'
                    column_width = 50
                elif widgets_per_section <= 3:
                    structure = '33'
                    column_width = 33.33
                else:
                    structure = '25'
                    column_width = 25
                
                section = {
                    'structure': structure,
                    'columns': []
                }
                
                for widget_idx in range(widgets_per_section):
                    column = {
                        'width': column_width,
                        'widgets': [{
                            'type': 'texticon',
                            'title': f'Widget P{page_idx+1}S{section_idx+1}W{widget_idx+1}',
                            'icon': 'fas fa-star',
                            'subtitle': f'Subtitle {widget_idx+1}',
                            'text': f'Content for widget {page_idx+1}-{section_idx+1}-{widget_idx+1}'
                        }]
                    }
                    section['columns'].append(column)
                
                page['sections'].append(section)
            
            test_data['pages'].append(page)
        
        return test_data
    
    def _benchmark_individual_widgets(self) -> Dict[str, Any]:
        """Benchmark individual widget type performance."""
        print("🎛️ Benchmarking individual widgets...")
        
        widget_configs = {
            'texticon': {
                'title': 'Benchmark TextIcon',
                'icon': 'fas fa-benchmark',
                'subtitle': 'Performance Test',
                'text': 'Testing widget generation performance with various content lengths and complexity.'
            },
            'title': {
                'title': 'Benchmark Title Widget<span>.</span>',
                'header_size': 'h1',
                'align': 'center'
            },
            'gallery': {
                'images': [f'http://localhost:8082/benchmark-{i}.jpg' for i in range(12)],
                'columns': 'col-md-4',
                'height': 250
            },
            'team': {
                'name': 'John Benchmark',
                'position': 'Performance Tester',
                'image_url': 'http://localhost:8082/team-benchmark.jpg',
                'social_links': [
                    {'icon': 'fab fa-linkedin', 'url': 'https://linkedin.com/benchmark'},
                    {'icon': 'fab fa-twitter', 'url': 'https://twitter.com/benchmark'},
                    {'icon': 'fab fa-github', 'url': 'https://github.com/benchmark'}
                ]
            },
            'testimonial': {
                'columns': 3,
                'testimonials': [
                    {
                        '_id': f'bench_{i}',
                        'name': f'Client {i}',
                        'position': f'Position {i}',
                        'testimonial': f'This is a benchmark testimonial number {i} with detailed content for performance testing.'
                    }
                    for i in range(6)
                ]
            },
            'post-three': {
                'post_count': 3,
                'column': 'one',
                'button_text': 'Read Benchmark Post',
                'categories': ['benchmark', 'performance', 'testing']
            },
            'post-four': {
                'post_count': 4,
                'column': 'two',
                'button_text': 'View Benchmark Article',
                'categories': ['benchmark', 'analysis', 'metrics', 'data']
            },
            'button-text': {
                'text': 'Benchmark Call to Action Button',
                'url': 'https://benchmark.example.com/action',
                'subtitle': 'Performance Testing CTA'
            },
            'text-line': {
                'title': 'Benchmark Text Line Widget Performance Test',
                'subtitle': 'Measuring generation speed and resource usage',
                'line_width': 75
            }
        }
        
        results = {
            'widget_benchmarks': {},
            'fastest_widget': None,
            'slowest_widget': None,
            'average_time': 0
        }
        
        all_times = []
        
        for widget_type, config in widget_configs.items():
            print(f"  Benchmarking {widget_type} widget...")
            
            times = []
            memory_usage = []
            
            for run in range(10):  # 10 runs for statistical significance
                gc.collect()
                
                process = psutil.Process()
                memory_before = process.memory_info().rss
                
                start_time = time.perf_counter()
                
                try:
                    if widget_type == 'texticon':
                        widget = self.factory.create_texticon_widget(config)
                    elif widget_type == 'title':
                        widget = self.factory.create_title_widget(config)
                    elif widget_type == 'gallery':
                        widget = self.factory.create_gallery_widget(config)
                    elif widget_type == 'team':
                        widget = self.factory.create_team_widget(config)
                    elif widget_type == 'testimonial':
                        widget = self.factory.create_testimonial_widget(config)
                    elif widget_type in ['post-three', 'post-four']:
                        post_type = widget_type.split('-')[1]
                        widget = self.factory.create_post_widget(config, post_type)
                    elif widget_type == 'button-text':
                        widget = self.factory.create_button_text_widget(config)
                    elif widget_type == 'text-line':
                        widget = self.factory.create_text_line_widget(config)
                    
                    end_time = time.perf_counter()
                    
                    memory_after = process.memory_info().rss
                    memory_used = memory_after - memory_before
                    
                    creation_time = end_time - start_time
                    times.append(creation_time)
                    memory_usage.append(memory_used)
                    
                except Exception as e:
                    print(f"    Error in {widget_type}: {e}")
                    continue
            
            if times:
                avg_time = statistics.mean(times)
                std_dev = statistics.stdev(times) if len(times) > 1 else 0
                avg_memory = statistics.mean(memory_usage)
                
                results['widget_benchmarks'][widget_type] = {
                    'avg_time_ms': round(avg_time * 1000, 3),
                    'std_dev_ms': round(std_dev * 1000, 3),
                    'avg_memory_bytes': int(avg_memory),
                    'runs': len(times),
                    'widgets_per_second': round(1 / avg_time, 1) if avg_time > 0 else 0
                }
                
                all_times.append((widget_type, avg_time))
        
        if all_times:
            all_times.sort(key=lambda x: x[1])
            results['fastest_widget'] = all_times[0][0]
            results['slowest_widget'] = all_times[-1][0]
            results['average_time'] = round(statistics.mean([t[1] for t in all_times]) * 1000, 3)
        
        return results
    
    def _benchmark_memory_usage(self) -> Dict[str, Any]:
        """Benchmark memory usage patterns."""
        print("🧠 Benchmarking memory usage...")
        
        # Test different memory scenarios
        test_scenarios = [
            ('Small Dataset', 1, 1, 3),
            ('Medium Dataset', 2, 3, 4),
            ('Large Dataset', 5, 4, 5),
            ('Memory Stress', 10, 6, 6)
        ]
        
        results = {
            'memory_tests': [],
            'peak_memory_mb': 0,
            'memory_efficiency': 'UNKNOWN'
        }
        
        for test_name, pages, sections, widgets in test_scenarios:
            print(f"  Testing {test_name}...")
            
            test_data = self._generate_test_data(pages, sections, widgets)
            total_widgets = pages * sections * widgets
            
            # Force garbage collection
            gc.collect()
            
            # Get baseline memory
            process = psutil.Process()
            baseline_memory = process.memory_info().rss
            
            # Enable memory tracing
            tracemalloc.start()
            
            try:
                # Generate XML
                xml_output = self.generator.generate_xml(test_data)
                
                # Get peak memory usage
                current_memory, peak_memory = tracemalloc.get_traced_memory()
                final_memory = process.memory_info().rss
                
                memory_used = final_memory - baseline_memory
                memory_per_widget = memory_used / total_widgets if total_widgets > 0 else 0
                
                test_result = {
                    'name': test_name,
                    'total_widgets': total_widgets,
                    'memory_used_mb': round(memory_used / 1024 / 1024, 2),
                    'peak_memory_mb': round(peak_memory / 1024 / 1024, 2),
                    'memory_per_widget_kb': round(memory_per_widget / 1024, 2),
                    'output_size_mb': round(len(xml_output) / 1024 / 1024, 2),
                    'memory_efficiency': round((len(xml_output) / memory_used) * 100, 2) if memory_used > 0 else 0
                }
                
                results['memory_tests'].append(test_result)
                
                if test_result['peak_memory_mb'] > results['peak_memory_mb']:
                    results['peak_memory_mb'] = test_result['peak_memory_mb']
                
            except Exception as e:
                print(f"    Memory test failed: {e}")
            
            finally:
                tracemalloc.stop()
        
        # Calculate overall memory efficiency
        if results['memory_tests']:
            avg_efficiency = statistics.mean([t['memory_efficiency'] for t in results['memory_tests']])
            if avg_efficiency > 50:
                results['memory_efficiency'] = 'EXCELLENT'
            elif avg_efficiency > 25:
                results['memory_efficiency'] = 'GOOD'
            elif avg_efficiency > 10:
                results['memory_efficiency'] = 'ACCEPTABLE'
            else:
                results['memory_efficiency'] = 'POOR'
        
        return results
    
    def _benchmark_concurrent_generation(self) -> Dict[str, Any]:
        """Benchmark concurrent generation scenarios."""
        print("🔄 Benchmarking concurrent generation...")
        
        # Simulate concurrent generation (sequential for now, could use threading)
        results = {
            'concurrent_tests': [],
            'throughput_pages_per_second': 0
        }
        
        # Test generating multiple pages sequentially (simulating concurrent requests)
        pages_to_generate = [
            {'title': f'Concurrent Page {i}', 'slug': f'concurrent-{i}', 'sections': [{
                'structure': '33',
                'columns': [
                    {'width': 33.33, 'widgets': [{'type': 'texticon', 'title': f'Widget {i}-1', 'icon': 'fas fa-1'}]},
                    {'width': 33.33, 'widgets': [{'type': 'texticon', 'title': f'Widget {i}-2', 'icon': 'fas fa-2'}]},
                    {'width': 33.33, 'widgets': [{'type': 'texticon', 'title': f'Widget {i}-3', 'icon': 'fas fa-3'}]}
                ]
            }]}
            for i in range(20)  # 20 pages
        ]
        
        start_time = time.time()
        successful_generations = 0
        
        for page_data in pages_to_generate:
            try:
                xml_output = self.generator.generate_xml({'pages': [page_data]})
                if xml_output and len(xml_output) > 1000:  # Basic validation
                    successful_generations += 1
            except Exception as e:
                print(f"    Generation failed: {e}")
        
        end_time = time.time()
        total_time = end_time - start_time
        
        results['concurrent_tests'].append({
            'total_pages': len(pages_to_generate),
            'successful_generations': successful_generations,
            'total_time': round(total_time, 2),
            'pages_per_second': round(successful_generations / total_time, 2) if total_time > 0 else 0,
            'success_rate': round((successful_generations / len(pages_to_generate)) * 100, 1)
        })
        
        results['throughput_pages_per_second'] = results['concurrent_tests'][0]['pages_per_second']
        
        return results
    
    def _benchmark_large_datasets(self) -> Dict[str, Any]:
        """Benchmark performance with very large datasets."""
        print("📊 Benchmarking large datasets...")
        
        # Test progressively larger datasets
        dataset_sizes = [
            ('Small Site', 5, 50),      # 5 pages, 50 widgets each
            ('Medium Site', 10, 100),   # 10 pages, 100 widgets each  
            ('Large Site', 20, 150),    # 20 pages, 150 widgets each
            ('Enterprise', 50, 200)     # 50 pages, 200 widgets each
        ]
        
        results = {
            'large_dataset_tests': [],
            'scalability_rating': 'UNKNOWN'
        }
        
        for test_name, num_pages, widgets_per_page in dataset_sizes:
            print(f"  Testing {test_name} ({num_pages} pages, {widgets_per_page} widgets each)...")
            
            # Generate large dataset
            large_data = {'pages': []}
            
            for page_idx in range(num_pages):
                page = {
                    'title': f'Large Test Page {page_idx + 1}',
                    'slug': f'large-page-{page_idx + 1}',
                    'sections': []
                }
                
                # Distribute widgets across sections
                widgets_added = 0
                section_idx = 0
                
                while widgets_added < widgets_per_page:
                    widgets_in_section = min(4, widgets_per_page - widgets_added)  # Max 4 per section
                    
                    section = {
                        'structure': '25' if widgets_in_section == 4 else '33' if widgets_in_section == 3 else '50' if widgets_in_section == 2 else '100',
                        'columns': []
                    }
                    
                    width = 100 / widgets_in_section
                    
                    for widget_idx in range(widgets_in_section):
                        column = {
                            'width': width,
                            'widgets': [{
                                'type': 'texticon',
                                'title': f'Large Widget P{page_idx+1}S{section_idx+1}W{widget_idx+1}',
                                'icon': 'fas fa-star',
                                'text': f'Content for large dataset widget {page_idx+1}-{section_idx+1}-{widget_idx+1}'
                            }]
                        }
                        section['columns'].append(column)
                    
                    page['sections'].append(section)
                    widgets_added += widgets_in_section
                    section_idx += 1
                
                large_data['pages'].append(page)
            
            try:
                # Benchmark generation
                gc.collect()
                process = psutil.Process()
                memory_before = process.memory_info().rss
                
                start_time = time.time()
                xml_output = self.generator.generate_xml(large_data)
                end_time = time.time()
                
                memory_after = process.memory_info().rss
                
                total_widgets = num_pages * widgets_per_page
                processing_time = end_time - start_time
                memory_used = memory_after - memory_before
                
                test_result = {
                    'name': test_name,
                    'pages': num_pages,
                    'widgets_per_page': widgets_per_page,
                    'total_widgets': total_widgets,
                    'processing_time': round(processing_time, 2),
                    'widgets_per_second': round(total_widgets / processing_time, 1) if processing_time > 0 else 0,
                    'memory_used_mb': round(memory_used / 1024 / 1024, 2),
                    'output_size_mb': round(len(xml_output) / 1024 / 1024, 2),
                    'success': True
                }
                
                results['large_dataset_tests'].append(test_result)
                
            except Exception as e:
                print(f"    Large dataset test failed: {e}")
                results['large_dataset_tests'].append({
                    'name': test_name,
                    'error': str(e),
                    'success': False
                })
        
        # Rate scalability
        successful_tests = [t for t in results['large_dataset_tests'] if t.get('success')]
        if len(successful_tests) >= 2:
            first_rate = successful_tests[0]['widgets_per_second']
            last_rate = successful_tests[-1]['widgets_per_second']
            
            if last_rate >= first_rate * 0.8:  # Less than 20% degradation
                results['scalability_rating'] = 'EXCELLENT'
            elif last_rate >= first_rate * 0.6:  # Less than 40% degradation
                results['scalability_rating'] = 'GOOD'
            elif last_rate >= first_rate * 0.4:  # Less than 60% degradation
                results['scalability_rating'] = 'ACCEPTABLE'
            else:
                results['scalability_rating'] = 'POOR'
        
        return results
    
    def _analyze_complexity_scaling(self) -> Dict[str, Any]:
        """Analyze how performance scales with complexity."""
        print("🔬 Analyzing complexity scaling...")
        
        # Test different complexity scenarios
        complexity_tests = [
            ('Simple Structure', 1, 1, 1, 'texticon'),        # 1 simple widget
            ('Medium Structure', 1, 3, 3, 'texticon'),        # 9 simple widgets
            ('Complex Structure', 1, 5, 5, 'texticon'),       # 25 simple widgets
            ('Mixed Widgets', 1, 1, 5, 'mixed'),              # 5 different widget types
            ('Rich Content', 1, 1, 3, 'rich')                 # 3 content-heavy widgets
        ]
        
        results = {
            'complexity_analysis': [],
            'complexity_factor': 0,
            'recommended_limits': {}
        }
        
        for test_name, pages, sections, widgets, widget_type in complexity_tests:
            print(f"  Analyzing {test_name}...")
            
            if widget_type == 'mixed':
                # Create mixed widget types
                widget_types = ['texticon', 'title', 'gallery', 'team', 'testimonial']
                test_widgets = []
                for i in range(widgets):
                    wtype = widget_types[i % len(widget_types)]
                    if wtype == 'texticon':
                        test_widgets.append({'type': 'texticon', 'title': f'Mixed {i}', 'icon': 'fas fa-star'})
                    elif wtype == 'title':
                        test_widgets.append({'type': 'title', 'title': f'Title {i}'})
                    elif wtype == 'gallery':
                        test_widgets.append({'type': 'gallery', 'images': [f'img{i}.jpg']})
                    elif wtype == 'team':
                        test_widgets.append({'type': 'team', 'name': f'Person {i}'})
                    elif wtype == 'testimonial':
                        test_widgets.append({'type': 'testimonial', 'columns': 1, 'testimonials': [{'_id': f'test{i}', 'name': f'Client {i}', 'testimonial': 'Great!'}]})
            
            elif widget_type == 'rich':
                # Create content-heavy widgets
                test_widgets = []
                for i in range(widgets):
                    test_widgets.append({
                        'type': 'texticon',
                        'title': f'Rich Content Widget {i+1}',
                        'icon': 'fas fa-star',
                        'subtitle': f'Detailed subtitle for widget {i+1} with extensive information',
                        'text': f'This is a very detailed text content for widget {i+1} ' * 20  # Long text
                    })
            else:
                # Simple texticon widgets
                test_widgets = [{'type': 'texticon', 'title': f'Simple {i}', 'icon': 'fas fa-star'} for i in range(widgets)]
            
            # Create test data
            test_data = {
                'pages': [{
                    'title': f'Complexity Test: {test_name}',
                    'slug': f'complexity-{test_name.lower().replace(" ", "-")}',
                    'sections': [{
                        'structure': '25' if widgets == 4 else '33' if widgets == 3 else '50' if widgets == 2 else '100',
                        'columns': [
                            {'width': 100/widgets, 'widgets': [test_widgets[i]]}
                            for i in range(widgets)
                        ]
                    }] * sections
                }] * pages
            }
            
            try:
                # Benchmark
                times = []
                memory_usage = []
                
                for run in range(5):
                    gc.collect()
                    process = psutil.Process()
                    memory_before = process.memory_info().rss
                    
                    start_time = time.perf_counter()
                    xml_output = self.generator.generate_xml(test_data)
                    end_time = time.perf_counter()
                    
                    memory_after = process.memory_info().rss
                    
                    times.append(end_time - start_time)
                    memory_usage.append(memory_after - memory_before)
                
                total_elements = pages * sections * widgets
                avg_time = statistics.mean(times)
                avg_memory = statistics.mean(memory_usage)
                
                complexity_result = {
                    'name': test_name,
                    'total_elements': total_elements,
                    'widget_type': widget_type,
                    'avg_time': round(avg_time, 4),
                    'avg_memory_mb': round(avg_memory / 1024 / 1024, 2),
                    'elements_per_second': round(total_elements / avg_time, 1) if avg_time > 0 else 0,
                    'time_per_element_ms': round((avg_time / total_elements) * 1000, 3) if total_elements > 0 else 0,
                    'memory_per_element_kb': round(avg_memory / total_elements / 1024, 2) if total_elements > 0 else 0
                }
                
                results['complexity_analysis'].append(complexity_result)
                
            except Exception as e:
                print(f"    Complexity test failed: {e}")
        
        # Calculate complexity factor
        if len(results['complexity_analysis']) >= 2:
            simple = results['complexity_analysis'][0]  # Simple structure
            complex = results['complexity_analysis'][2]  # Complex structure
            
            if simple['total_elements'] > 0 and complex['total_elements'] > 0:
                element_ratio = complex['total_elements'] / simple['total_elements']
                time_ratio = complex['avg_time'] / simple['avg_time']
                results['complexity_factor'] = round(time_ratio / element_ratio, 2)
        
        # Generate recommendations
        if results['complexity_analysis']:
            best_performance = min(results['complexity_analysis'], key=lambda x: x['time_per_element_ms'])
            results['recommended_limits'] = {
                'optimal_elements_per_page': best_performance['total_elements'],
                'max_recommended_widgets': best_performance['total_elements'] * 2,
                'performance_target_ms_per_element': best_performance['time_per_element_ms'] * 2
            }
        
        return results
    
    def _run_stress_test(self) -> Dict[str, Any]:
        """Run stress test to find performance limits."""
        print("💪 Running stress test...")
        
        results = {
            'stress_tests': [],
            'performance_limit': None,
            'stability_rating': 'UNKNOWN'
        }
        
        # Progressive stress test - increase load until failure or significant slowdown
        stress_levels = [
            (100, 'Light Load'),
            (500, 'Medium Load'), 
            (1000, 'Heavy Load'),
            (2000, 'Extreme Load'),
            (5000, 'Stress Limit')
        ]
        
        baseline_rate = None
        
        for widget_count, level_name in stress_levels:
            print(f"  Testing {level_name} ({widget_count} widgets)...")
            
            try:
                # Generate stress test data
                pages = max(1, widget_count // 100)  # At least 1 page
                widgets_per_page = widget_count // pages
                
                stress_data = self._generate_test_data(pages, 1, widgets_per_page)
                
                # Measure performance
                gc.collect()
                process = psutil.Process()
                memory_before = process.memory_info().rss
                
                start_time = time.time()
                xml_output = self.generator.generate_xml(stress_data)
                end_time = time.time()
                
                memory_after = process.memory_info().rss
                
                processing_time = end_time - start_time
                memory_used = memory_after - memory_before
                widgets_per_second = widget_count / processing_time if processing_time > 0 else 0
                
                # Check if we've hit a performance wall
                if baseline_rate is None:
                    baseline_rate = widgets_per_second
                
                performance_degradation = ((baseline_rate - widgets_per_second) / baseline_rate * 100) if baseline_rate > 0 else 0
                
                stress_result = {
                    'level': level_name,
                    'widget_count': widget_count,
                    'pages': pages,
                    'processing_time': round(processing_time, 2),
                    'widgets_per_second': round(widgets_per_second, 1),
                    'memory_used_mb': round(memory_used / 1024 / 1024, 2),
                    'output_size_mb': round(len(xml_output) / 1024 / 1024, 2),
                    'performance_degradation_percent': round(performance_degradation, 1),
                    'success': True
                }
                
                results['stress_tests'].append(stress_result)
                
                # Stop if performance has degraded significantly (>50%)
                if performance_degradation > 50:
                    results['performance_limit'] = widget_count
                    break
                    
                # Stop if processing takes too long (>30 seconds)
                if processing_time > 30:
                    results['performance_limit'] = widget_count
                    break
                
            except Exception as e:
                print(f"    Stress test failed at {level_name}: {e}")
                results['stress_tests'].append({
                    'level': level_name,
                    'widget_count': widget_count,
                    'error': str(e),
                    'success': False
                })
                results['performance_limit'] = widget_count
                break
        
        # Rate stability
        successful_tests = [t for t in results['stress_tests'] if t.get('success')]
        if successful_tests:
            max_degradation = max(t['performance_degradation_percent'] for t in successful_tests)
            
            if max_degradation <= 25:
                results['stability_rating'] = 'EXCELLENT'
            elif max_degradation <= 50:
                results['stability_rating'] = 'GOOD'
            elif max_degradation <= 75:
                results['stability_rating'] = 'ACCEPTABLE'
            else:
                results['stability_rating'] = 'POOR'
        
        return results
    
    def _calculate_overall_performance(self, benchmark_results: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate overall performance metrics."""
        overall = {
            'performance_score': 0,
            'performance_rating': 'UNKNOWN',
            'key_metrics': {},
            'bottlenecks': [],
            'recommendations': []
        }
        
        # Extract key metrics
        scalability = benchmark_results.get('scalability_test', {})
        if scalability.get('performance_data'):
            last_perf = scalability['performance_data'][-1]
            overall['key_metrics']['max_widgets_per_second'] = last_perf.get('rate', 0)
            overall['key_metrics']['scaling_factor'] = scalability.get('scaling_factor', 0)
        
        memory = benchmark_results.get('memory_usage', {})
        if memory.get('memory_tests'):
            overall['key_metrics']['peak_memory_mb'] = memory.get('peak_memory_mb', 0)
            overall['key_metrics']['memory_efficiency'] = memory.get('memory_efficiency', 'UNKNOWN')
        
        stress = benchmark_results.get('stress_test', {})
        if stress.get('performance_limit'):
            overall['key_metrics']['performance_limit_widgets'] = stress['performance_limit']
            overall['key_metrics']['stability_rating'] = stress.get('stability_rating', 'UNKNOWN')
        
        # Calculate performance score (0-100)
        score_factors = []
        
        # Widget generation speed (40% of score)
        max_rate = overall['key_metrics'].get('max_widgets_per_second', 0)
        if max_rate >= 50:
            score_factors.append(40)
        elif max_rate >= 25:
            score_factors.append(35)
        elif max_rate >= 10:
            score_factors.append(30)
        elif max_rate >= 5:
            score_factors.append(20)
        else:
            score_factors.append(10)
        
        # Memory efficiency (25% of score)
        memory_eff = overall['key_metrics'].get('memory_efficiency', 'UNKNOWN')
        if memory_eff == 'EXCELLENT':
            score_factors.append(25)
        elif memory_eff == 'GOOD':
            score_factors.append(20)
        elif memory_eff == 'ACCEPTABLE':
            score_factors.append(15)
        else:
            score_factors.append(5)
        
        # Scalability (20% of score)
        scaling = overall['key_metrics'].get('scaling_factor', 0)
        if scaling <= 1.2:  # Near-linear scaling
            score_factors.append(20)
        elif scaling <= 1.5:
            score_factors.append(15)
        elif scaling <= 2.0:
            score_factors.append(10)
        else:
            score_factors.append(5)
        
        # Stability (15% of score)
        stability = overall['key_metrics'].get('stability_rating', 'UNKNOWN')
        if stability == 'EXCELLENT':
            score_factors.append(15)
        elif stability == 'GOOD':
            score_factors.append(12)
        elif stability == 'ACCEPTABLE':
            score_factors.append(8)
        else:
            score_factors.append(3)
        
        overall['performance_score'] = sum(score_factors)
        
        # Determine rating
        if overall['performance_score'] >= 90:
            overall['performance_rating'] = 'EXCELLENT'
        elif overall['performance_score'] >= 75:
            overall['performance_rating'] = 'GOOD'
        elif overall['performance_score'] >= 60:
            overall['performance_rating'] = 'ACCEPTABLE'
        elif overall['performance_score'] >= 40:
            overall['performance_rating'] = 'NEEDS_IMPROVEMENT'
        else:
            overall['performance_rating'] = 'POOR'
        
        # Generate recommendations
        if max_rate < 10:
            overall['recommendations'].append("Optimize widget generation algorithms - current speed is below recommended minimum")
        
        if memory_eff in ['POOR', 'ACCEPTABLE']:
            overall['recommendations'].append("Improve memory efficiency - consider object pooling or memory optimization")
        
        if scaling > 2.0:
            overall['recommendations'].append("Address scalability issues - performance degrades significantly with dataset size")
        
        if stability in ['POOR', 'ACCEPTABLE']:
            overall['recommendations'].append("Improve stability under load - consider memory management and error handling")
        
        if not overall['recommendations']:
            overall['recommendations'].append("Excellent performance across all metrics!")
        
        return overall
    
    def save_benchmark_report(self, results: Dict[str, Any], output_file: Path = None) -> Path:
        """Save benchmark results to file."""
        if output_file is None:
            output_file = Path(__file__).parent / f"benchmark_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        return output_file
    
    def generate_performance_charts(self, results: Dict[str, Any], output_dir: Path = None):
        """Generate performance visualization charts."""
        if output_dir is None:
            output_dir = Path(__file__).parent / "benchmark_charts"
        
        output_dir.mkdir(exist_ok=True)
        
        try:
            import matplotlib.pyplot as plt
            
            # Scalability chart
            scalability = results.get('scalability_test', {})
            if scalability.get('performance_data'):
                data = scalability['performance_data']
                widgets = [d['widgets'] for d in data]
                rates = [d['rate'] for d in data]
                
                plt.figure(figsize=(10, 6))
                plt.plot(widgets, rates, 'b-o', linewidth=2, markersize=8)
                plt.xlabel('Total Widgets')
                plt.ylabel('Widgets per Second')
                plt.title('Generator Performance Scalability')
                plt.grid(True, alpha=0.3)
                plt.savefig(output_dir / 'scalability_chart.png', dpi=300, bbox_inches='tight')
                plt.close()
            
            # Memory usage chart
            memory = results.get('memory_usage', {})
            if memory.get('memory_tests'):
                tests = memory['memory_tests']
                test_names = [t['name'] for t in tests]
                memory_used = [t['memory_used_mb'] for t in tests]
                
                plt.figure(figsize=(12, 6))
                bars = plt.bar(test_names, memory_used, color='green', alpha=0.7)
                plt.xlabel('Test Scenario')
                plt.ylabel('Memory Used (MB)')
                plt.title('Memory Usage by Test Scenario')
                plt.xticks(rotation=45)
                
                # Add value labels on bars
                for bar, value in zip(bars, memory_used):
                    plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1, 
                            f'{value:.1f}MB', ha='center', va='bottom')
                
                plt.tight_layout()
                plt.savefig(output_dir / 'memory_usage_chart.png', dpi=300, bbox_inches='tight')
                plt.close()
            
            print(f"📈 Performance charts saved to {output_dir}")
            
        except ImportError:
            print("⚠️  matplotlib not available - skipping chart generation")
    
    def print_benchmark_summary(self, results: Dict[str, Any]):
        """Print benchmark results summary."""
        print("\n" + "=" * 70)
        print("🏁 BENCHMARK RESULTS SUMMARY")
        print("=" * 70)
        
        overall = results.get('overall_performance', {})
        print(f"Performance Score: {overall.get('performance_score', 0)}/100")
        print(f"Performance Rating: {overall.get('performance_rating', 'UNKNOWN')}")
        
        key_metrics = overall.get('key_metrics', {})
        if key_metrics:
            print(f"\n📊 Key Metrics:")
            if 'max_widgets_per_second' in key_metrics:
                print(f"  Max Generation Rate: {key_metrics['max_widgets_per_second']} widgets/second")
            if 'peak_memory_mb' in key_metrics:
                print(f"  Peak Memory Usage: {key_metrics['peak_memory_mb']} MB")
            if 'scaling_factor' in key_metrics:
                print(f"  Scaling Factor: {key_metrics['scaling_factor']:.2f} (1.0 = linear)")
            if 'performance_limit_widgets' in key_metrics:
                print(f"  Performance Limit: {key_metrics['performance_limit_widgets']} widgets")
        
        # Widget performance
        widget_perf = results.get('widget_performance', {})
        if widget_perf.get('fastest_widget'):
            print(f"\n⚡ Fastest Widget: {widget_perf['fastest_widget']}")
            print(f"   Slowest Widget: {widget_perf.get('slowest_widget', 'Unknown')}")
            print(f"   Average Time: {widget_perf.get('average_time', 0):.3f}ms")
        
        # Stress test results
        stress = results.get('stress_test', {})
        if stress.get('stability_rating'):
            print(f"\n💪 Stress Test: {stress['stability_rating']}")
            if stress.get('performance_limit'):
                print(f"   Performance Limit: {stress['performance_limit']} widgets")
        
        # Recommendations
        recommendations = overall.get('recommendations', [])
        if recommendations:
            print(f"\n💡 Recommendations:")
            for i, rec in enumerate(recommendations, 1):
                print(f"  {i}. {rec}")
        
        print(f"\n🎯 PERFORMANCE VERDICT: {overall.get('performance_rating', 'UNKNOWN')}")


def main():
    """Main function to run benchmark suite."""
    benchmark_suite = ElementorBenchmarkSuite()
    
    # Run comprehensive benchmarks
    results = benchmark_suite.run_comprehensive_benchmarks()
    
    # Save results
    report_file = benchmark_suite.save_benchmark_report(results)
    print(f"\n📄 Detailed benchmark report saved to: {report_file}")
    
    # Generate performance charts
    benchmark_suite.generate_performance_charts(results)
    
    # Print summary
    benchmark_suite.print_benchmark_summary(results)
    
    return 0


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
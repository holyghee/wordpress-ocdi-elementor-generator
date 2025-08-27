#!/usr/bin/env python3
"""
Test Scenarios for Elementor JSON Generator
==========================================

Pre-defined test scenarios for comprehensive validation of the generator.

Author: Testing & Validation Expert
"""

import json
from pathlib import Path
from typing import Dict, List, Any

class TestScenarioManager:
    """Manages pre-defined test scenarios for the Elementor JSON generator."""
    
    def __init__(self):
        self.scenarios = {}
        self._initialize_scenarios()
    
    def _initialize_scenarios(self):
        """Initialize all test scenarios."""
        self.scenarios = {
            'basic_page': self._create_basic_page_scenario(),
            'service_page_3': self._create_3_service_scenario(),
            'service_page_6': self._create_6_service_scenario(),
            'full_website': self._create_full_website_scenario(),
            'widget_showcase': self._create_widget_showcase_scenario(),
            'responsive_layout': self._create_responsive_layout_scenario(),
            'multi_language': self._create_multi_language_scenario(),
            'business_template': self._create_business_template_scenario(),
            'portfolio_template': self._create_portfolio_template_scenario(),
            'blog_template': self._create_blog_template_scenario(),
            'minimal_scenario': self._create_minimal_scenario(),
            'complex_hierarchy': self._create_complex_hierarchy_scenario()
        }
    
    def get_scenario(self, scenario_name: str) -> Dict[str, Any]:
        """Get a specific test scenario."""
        return self.scenarios.get(scenario_name, {})
    
    def get_all_scenarios(self) -> Dict[str, Dict[str, Any]]:
        """Get all test scenarios."""
        return self.scenarios
    
    def get_scenario_names(self) -> List[str]:
        """Get names of all available scenarios."""
        return list(self.scenarios.keys())
    
    def _create_basic_page_scenario(self) -> Dict[str, Any]:
        """Create a basic single-page scenario."""
        return {
            'name': 'Basic Single Page',
            'description': 'Simple page with title and text content',
            'data': {
                'pages': [{
                    'title': 'Welcome',
                    'slug': 'welcome',
                    'sections': [{
                        'structure': '100',
                        'columns': [{
                            'width': 100,
                            'widgets': [
                                {
                                    'type': 'title',
                                    'title': 'Welcome to Our Website<span>.</span>',
                                    'header_size': 'h1',
                                    'align': 'center'
                                },
                                {
                                    'type': 'texticon',
                                    'title': 'Professional Services',
                                    'icon': 'fas fa-star',
                                    'subtitle': 'Quality First',
                                    'text': 'We provide high-quality professional services to help your business grow.'
                                }
                            ]
                        }]
                    }]
                }]
            },
            'site_config': {
                'title': 'Basic Test Site',
                'description': 'A simple test website',
                'base_url': 'http://localhost:8082'
            },
            'expected_widgets': ['cholot-title', 'cholot-texticon'],
            'expected_pages': 1
        }
    
    def _create_3_service_scenario(self) -> Dict[str, Any]:
        """Create 3-service page scenario."""
        services = [
            {
                'title': 'Web Development',
                'icon': 'fas fa-code',
                'subtitle': 'Custom Solutions',
                'text': 'Professional web development with modern technologies and best practices.'
            },
            {
                'title': 'Mobile Applications',
                'icon': 'fas fa-mobile-alt',
                'subtitle': 'Cross Platform',
                'text': 'Native and cross-platform mobile apps for iOS and Android platforms.'
            },
            {
                'title': 'UI/UX Design',
                'icon': 'fas fa-paint-brush',
                'subtitle': 'User Centered',
                'text': 'Beautiful and intuitive user interfaces designed for optimal user experience.'
            }
        ]
        
        columns = []
        for service in services:
            columns.append({
                'width': 33.33,
                'widgets': [{
                    'type': 'texticon',
                    **service
                }]
            })
        
        return {
            'name': '3-Service Page',
            'description': 'Services page with exactly 3 service offerings',
            'data': {
                'pages': [{
                    'title': 'Our Services',
                    'slug': 'services',
                    'sections': [
                        {
                            'structure': '100',
                            'columns': [{
                                'width': 100,
                                'widgets': [{
                                    'type': 'title',
                                    'title': 'Our Professional Services<span>.</span>',
                                    'header_size': 'h1',
                                    'align': 'center'
                                }]
                            }]
                        },
                        {
                            'structure': '33',
                            'columns': columns
                        }
                    ]
                }]
            },
            'site_config': {
                'title': '3-Service Company',
                'description': 'Professional services company',
                'base_url': 'http://localhost:8082'
            },
            'expected_widgets': ['cholot-title', 'cholot-texticon'],
            'expected_texticon_count': 3,
            'expected_pages': 1
        }
    
    def _create_6_service_scenario(self) -> Dict[str, Any]:
        """Create 6-service page scenario."""
        services_row_1 = [
            {
                'title': 'Web Development',
                'icon': 'fas fa-code',
                'subtitle': 'Full Stack',
                'text': 'Complete web development solutions from frontend to backend.'
            },
            {
                'title': 'Mobile Apps',
                'icon': 'fas fa-mobile-alt',
                'subtitle': 'Native & Hybrid',
                'text': 'Mobile applications for iOS and Android with great performance.'
            },
            {
                'title': 'UI/UX Design',
                'icon': 'fas fa-paint-brush',
                'subtitle': 'User Focused',
                'text': 'Design that prioritizes user experience and conversion optimization.'
            }
        ]
        
        services_row_2 = [
            {
                'title': 'Digital Marketing',
                'icon': 'fas fa-bullhorn',
                'subtitle': 'Growth Driven',
                'text': 'Strategic digital marketing campaigns to grow your business online.'
            },
            {
                'title': 'Cloud Solutions',
                'icon': 'fas fa-cloud',
                'subtitle': 'Scalable Infrastructure',
                'text': 'Reliable and scalable cloud infrastructure solutions for modern businesses.'
            },
            {
                'title': 'Data Analytics',
                'icon': 'fas fa-chart-line',
                'subtitle': 'Business Intelligence',
                'text': 'Transform your data into actionable business insights and strategies.'
            }
        ]
        
        columns_row_1 = []
        for service in services_row_1:
            columns_row_1.append({
                'width': 33.33,
                'widgets': [{
                    'type': 'texticon',
                    **service
                }]
            })
        
        columns_row_2 = []
        for service in services_row_2:
            columns_row_2.append({
                'width': 33.33,
                'widgets': [{
                    'type': 'texticon',
                    **service
                }]
            })
        
        return {
            'name': '6-Service Page',
            'description': 'Services page with 6 service offerings in 2 rows',
            'data': {
                'pages': [{
                    'title': 'Complete Services',
                    'slug': 'complete-services',
                    'sections': [
                        {
                            'structure': '100',
                            'columns': [{
                                'width': 100,
                                'widgets': [{
                                    'type': 'title',
                                    'title': 'Complete Digital Solutions<span>.</span>',
                                    'header_size': 'h1',
                                    'align': 'center'
                                }]
                            }]
                        },
                        {
                            'structure': '33',
                            'columns': columns_row_1
                        },
                        {
                            'structure': '33', 
                            'columns': columns_row_2
                        }
                    ]
                }]
            },
            'site_config': {
                'title': 'Full Service Agency',
                'description': 'Complete digital solutions provider',
                'base_url': 'http://localhost:8082'
            },
            'expected_widgets': ['cholot-title', 'cholot-texticon'],
            'expected_texticon_count': 6,
            'expected_pages': 1
        }
    
    def _create_full_website_scenario(self) -> Dict[str, Any]:
        """Create a complete multi-page website scenario."""
        return {
            'name': 'Full Website',
            'description': 'Complete multi-page website with all common pages',
            'data': {
                'pages': [
                    {
                        'title': 'Home',
                        'slug': 'home',
                        'sections': [
                            {
                                'structure': '100',
                                'columns': [{
                                    'width': 100,
                                    'widgets': [
                                        {
                                            'type': 'title',
                                            'title': 'Welcome to Our Company<span>.</span>',
                                            'header_size': 'h1',
                                            'align': 'center'
                                        },
                                        {
                                            'type': 'texticon',
                                            'title': 'Professional Excellence',
                                            'icon': 'fas fa-star',
                                            'subtitle': 'Quality Service',
                                            'text': 'We deliver professional excellence in everything we do.'
                                        }
                                    ]
                                }]
                            }
                        ]
                    },
                    {
                        'title': 'About Us',
                        'slug': 'about',
                        'sections': [
                            {
                                'structure': '50',
                                'columns': [
                                    {
                                        'width': 50,
                                        'widgets': [{
                                            'type': 'title',
                                            'title': 'About Our Company',
                                            'header_size': 'h2'
                                        }]
                                    },
                                    {
                                        'width': 50,
                                        'widgets': [{
                                            'type': 'team',
                                            'name': 'John Smith',
                                            'position': 'CEO & Founder',
                                            'image_url': 'http://localhost:8082/team-ceo.jpg'
                                        }]
                                    }
                                ]
                            }
                        ]
                    },
                    {
                        'title': 'Services',
                        'slug': 'services',
                        'sections': [
                            {
                                'structure': '33',
                                'columns': [
                                    {
                                        'width': 33.33,
                                        'widgets': [{
                                            'type': 'texticon',
                                            'title': 'Consulting',
                                            'icon': 'fas fa-lightbulb'
                                        }]
                                    },
                                    {
                                        'width': 33.33,
                                        'widgets': [{
                                            'type': 'texticon',
                                            'title': 'Development',
                                            'icon': 'fas fa-code'
                                        }]
                                    },
                                    {
                                        'width': 33.33,
                                        'widgets': [{
                                            'type': 'texticon',
                                            'title': 'Support',
                                            'icon': 'fas fa-headset'
                                        }]
                                    }
                                ]
                            }
                        ]
                    },
                    {
                        'title': 'Contact',
                        'slug': 'contact',
                        'sections': [
                            {
                                'structure': '100',
                                'columns': [{
                                    'width': 100,
                                    'widgets': [
                                        {
                                            'type': 'title',
                                            'title': 'Get In Touch<span>.</span>',
                                            'header_size': 'h2',
                                            'align': 'center'
                                        },
                                        {
                                            'type': 'contact',
                                            'shortcode': '[contact-form-7 id="1" title="Contact form"]'
                                        }
                                    ]
                                }]
                            }
                        ]
                    }
                ]
            },
            'site_config': {
                'title': 'Full Website Demo',
                'description': 'Complete business website demonstration',
                'base_url': 'http://localhost:8082'
            },
            'expected_widgets': ['cholot-title', 'cholot-texticon', 'cholot-team', 'cholot-contact'],
            'expected_pages': 4
        }
    
    def _create_widget_showcase_scenario(self) -> Dict[str, Any]:
        """Create a scenario showcasing all 13 widget types."""
        return {
            'name': 'Widget Showcase',
            'description': 'Demonstrates all 13 Cholot widget types',
            'data': {
                'pages': [{
                    'title': 'Widget Showcase',
                    'slug': 'showcase',
                    'sections': [
                        # Header
                        {
                            'structure': '100',
                            'columns': [{
                                'width': 100,
                                'widgets': [{
                                    'type': 'title',
                                    'title': 'Widget Showcase<span>.</span>',
                                    'header_size': 'h1',
                                    'align': 'center'
                                }]
                            }]
                        },
                        # TextIcon widgets
                        {
                            'structure': '33',
                            'columns': [
                                {
                                    'width': 33.33,
                                    'widgets': [{
                                        'type': 'texticon',
                                        'title': 'TextIcon Widget',
                                        'icon': 'fas fa-star',
                                        'subtitle': 'Feature Rich',
                                        'text': 'Versatile widget for displaying icons with text content.'
                                    }]
                                },
                                {
                                    'width': 33.33,
                                    'widgets': [{
                                        'type': 'gallery',
                                        'images': [
                                            'http://localhost:8082/gallery-1.jpg',
                                            'http://localhost:8082/gallery-2.jpg',
                                            'http://localhost:8082/gallery-3.jpg'
                                        ],
                                        'columns': 'col-md-4',
                                        'height': 200
                                    }]
                                },
                                {
                                    'width': 33.33,
                                    'widgets': [{
                                        'type': 'logo',
                                        'url': 'http://localhost:8082/company-logo.svg',
                                        'height': '80px',
                                        'align': 'center'
                                    }]
                                }
                            ]
                        },
                        # Post and Navigation widgets
                        {
                            'structure': '33',
                            'columns': [
                                {
                                    'width': 33.33,
                                    'widgets': [{
                                        'type': 'post-three',
                                        'post_count': 3,
                                        'column': 'one',
                                        'button_text': 'Read More'
                                    }]
                                },
                                {
                                    'width': 33.33,
                                    'widgets': [{
                                        'type': 'post-four',
                                        'post_count': 4,
                                        'column': 'two',
                                        'categories': ['news', 'blog']
                                    }]
                                },
                                {
                                    'width': 33.33,
                                    'widgets': [{
                                        'type': 'menu',
                                        'menu_name': 'main-navigation',
                                        'align': 'center'
                                    }]
                                }
                            ]
                        },
                        # Interactive widgets
                        {
                            'structure': '33',
                            'columns': [
                                {
                                    'width': 33.33,
                                    'widgets': [{
                                        'type': 'button-text',
                                        'text': 'Call to Action',
                                        'url': 'https://example.com/cta',
                                        'subtitle': 'Get Started Today'
                                    }]
                                },
                                {
                                    'width': 33.33,
                                    'widgets': [{
                                        'type': 'team',
                                        'name': 'Sarah Johnson',
                                        'position': 'Lead Designer',
                                        'image_url': 'http://localhost:8082/team-sarah.jpg',
                                        'social_links': [
                                            {'icon': 'fab fa-linkedin', 'url': 'https://linkedin.com/in/sarah'},
                                            {'icon': 'fab fa-behance', 'url': 'https://behance.net/sarah'}
                                        ]
                                    }]
                                },
                                {
                                    'width': 33.33,
                                    'widgets': [{
                                        'type': 'testimonial',
                                        'columns': 1,
                                        'testimonials': [{
                                            '_id': 'testimonial_showcase',
                                            'name': 'Happy Client',
                                            'position': 'Business Owner',
                                            'testimonial': 'Excellent service and outstanding results!'
                                        }]
                                    }]
                                }
                            ]
                        },
                        # Content and Form widgets
                        {
                            'structure': '33',
                            'columns': [
                                {
                                    'width': 33.33,
                                    'widgets': [{
                                        'type': 'text-line',
                                        'title': 'Text Line Widget',
                                        'subtitle': 'Styled Text Display',
                                        'line_width': 50
                                    }]
                                },
                                {
                                    'width': 33.33,
                                    'widgets': [{
                                        'type': 'contact',
                                        'shortcode': '[contact-form-7 id="showcase" title="Showcase Contact Form"]'
                                    }]
                                },
                                {
                                    'width': 33.33,
                                    'widgets': [{
                                        'type': 'sidebar',
                                        'width': '300px'
                                    }]
                                }
                            ]
                        }
                    ]
                }]
            },
            'site_config': {
                'title': 'Widget Showcase Site',
                'description': 'Demonstration of all Cholot widgets',
                'base_url': 'http://localhost:8082'
            },
            'expected_widgets': [
                'cholot-title', 'cholot-texticon', 'cholot-gallery', 'cholot-logo',
                'cholot-post-three', 'cholot-post-four', 'cholot-menu', 'cholot-button-text',
                'cholot-team', 'cholot-testimonial', 'cholot-text-line', 'cholot-contact', 'cholot-sidebar'
            ],
            'expected_pages': 1,
            'expected_total_widgets': 13
        }
    
    def _create_responsive_layout_scenario(self) -> Dict[str, Any]:
        """Create a scenario testing responsive layouts."""
        return {
            'name': 'Responsive Layout Test',
            'description': 'Tests various responsive column layouts',
            'data': {
                'pages': [{
                    'title': 'Responsive Layout',
                    'slug': 'responsive',
                    'sections': [
                        # Single column
                        {
                            'structure': '100',
                            'columns': [{
                                'width': 100,
                                'widgets': [{
                                    'type': 'title',
                                    'title': '100% Width Layout',
                                    'header_size': 'h2'
                                }]
                            }]
                        },
                        # Two columns
                        {
                            'structure': '50',
                            'columns': [
                                {
                                    'width': 50,
                                    'widgets': [{
                                        'type': 'texticon',
                                        'title': '50% Column 1',
                                        'icon': 'fas fa-left'
                                    }]
                                },
                                {
                                    'width': 50,
                                    'widgets': [{
                                        'type': 'texticon',
                                        'title': '50% Column 2',
                                        'icon': 'fas fa-right'
                                    }]
                                }
                            ]
                        },
                        # Three columns
                        {
                            'structure': '33',
                            'columns': [
                                {
                                    'width': 33.33,
                                    'widgets': [{
                                        'type': 'texticon',
                                        'title': '33% Column 1',
                                        'icon': 'fas fa-1'
                                    }]
                                },
                                {
                                    'width': 33.33,
                                    'widgets': [{
                                        'type': 'texticon',
                                        'title': '33% Column 2',
                                        'icon': 'fas fa-2'
                                    }]
                                },
                                {
                                    'width': 33.33,
                                    'widgets': [{
                                        'type': 'texticon',
                                        'title': '33% Column 3',
                                        'icon': 'fas fa-3'
                                    }]
                                }
                            ]
                        },
                        # Four columns
                        {
                            'structure': '25',
                            'columns': [
                                {
                                    'width': 25,
                                    'widgets': [{
                                        'type': 'texticon',
                                        'title': '25% Col 1',
                                        'icon': 'fas fa-star'
                                    }]
                                },
                                {
                                    'width': 25,
                                    'widgets': [{
                                        'type': 'texticon',
                                        'title': '25% Col 2',
                                        'icon': 'fas fa-star'
                                    }]
                                },
                                {
                                    'width': 25,
                                    'widgets': [{
                                        'type': 'texticon',
                                        'title': '25% Col 3',
                                        'icon': 'fas fa-star'
                                    }]
                                },
                                {
                                    'width': 25,
                                    'widgets': [{
                                        'type': 'texticon',
                                        'title': '25% Col 4',
                                        'icon': 'fas fa-star'
                                    }]
                                }
                            ]
                        }
                    ]
                }]
            },
            'site_config': {
                'title': 'Responsive Test Site',
                'description': 'Testing responsive layouts',
                'base_url': 'http://localhost:8082'
            },
            'expected_widgets': ['cholot-title', 'cholot-texticon'],
            'expected_pages': 1
        }
    
    def _create_minimal_scenario(self) -> Dict[str, Any]:
        """Create minimal test scenario."""
        return {
            'name': 'Minimal Test',
            'description': 'Absolute minimal test with just one widget',
            'data': {
                'pages': [{
                    'title': 'Minimal',
                    'slug': 'minimal',
                    'sections': [{
                        'structure': '100',
                        'columns': [{
                            'width': 100,
                            'widgets': [{
                                'type': 'title',
                                'title': 'Minimal Test'
                            }]
                        }]
                    }]
                }]
            },
            'site_config': {
                'title': 'Minimal Site',
                'description': 'Minimal test site',
                'base_url': 'http://localhost:8082'
            },
            'expected_widgets': ['cholot-title'],
            'expected_pages': 1
        }
    
    def _create_complex_hierarchy_scenario(self) -> Dict[str, Any]:
        """Create complex nested structure scenario."""
        return {
            'name': 'Complex Hierarchy',
            'description': 'Complex nested structure with multiple sections and widgets',
            'data': {
                'pages': [{
                    'title': 'Complex Structure',
                    'slug': 'complex',
                    'sections': [
                        {
                            'structure': '100',
                            'columns': [{
                                'width': 100,
                                'widgets': [
                                    {
                                        'type': 'title',
                                        'title': 'Complex Hierarchy Test<span>.</span>',
                                        'header_size': 'h1'
                                    },
                                    {
                                        'type': 'texticon',
                                        'title': 'Introduction',
                                        'icon': 'fas fa-info-circle',
                                        'text': 'This page demonstrates complex nested structures.'
                                    }
                                ]
                            }]
                        },
                        {
                            'structure': '66',
                            'columns': [
                                {
                                    'width': 66.67,
                                    'widgets': [
                                        {
                                            'type': 'title',
                                            'title': 'Main Content Area',
                                            'header_size': 'h2'
                                        },
                                        {
                                            'type': 'gallery',
                                            'images': [
                                                'http://localhost:8082/gallery-1.jpg',
                                                'http://localhost:8082/gallery-2.jpg',
                                                'http://localhost:8082/gallery-3.jpg',
                                                'http://localhost:8082/gallery-4.jpg'
                                            ]
                                        },
                                        {
                                            'type': 'testimonial',
                                            'columns': 2,
                                            'testimonials': [
                                                {
                                                    '_id': 'test1',
                                                    'name': 'Client 1',
                                                    'testimonial': 'Great work!'
                                                },
                                                {
                                                    '_id': 'test2',
                                                    'name': 'Client 2',
                                                    'testimonial': 'Excellent service!'
                                                }
                                            ]
                                        }
                                    ]
                                },
                                {
                                    'width': 33.33,
                                    'widgets': [
                                        {
                                            'type': 'sidebar',
                                            'width': '300px'
                                        },
                                        {
                                            'type': 'team',
                                            'name': 'Team Lead',
                                            'position': 'Project Manager'
                                        },
                                        {
                                            'type': 'button-text',
                                            'text': 'Contact Us',
                                            'url': 'contact.html'
                                        }
                                    ]
                                }
                            ]
                        },
                        {
                            'structure': '25',
                            'columns': [
                                {
                                    'width': 25,
                                    'widgets': [{
                                        'type': 'texticon',
                                        'title': 'Service 1',
                                        'icon': 'fas fa-cog'
                                    }]
                                },
                                {
                                    'width': 25,
                                    'widgets': [{
                                        'type': 'texticon',
                                        'title': 'Service 2',
                                        'icon': 'fas fa-star'
                                    }]
                                },
                                {
                                    'width': 25,
                                    'widgets': [{
                                        'type': 'texticon',
                                        'title': 'Service 3',
                                        'icon': 'fas fa-crown'
                                    }]
                                },
                                {
                                    'width': 25,
                                    'widgets': [{
                                        'type': 'texticon',
                                        'title': 'Service 4',
                                        'icon': 'fas fa-gem'
                                    }]
                                }
                            ]
                        }
                    ]
                }]
            },
            'site_config': {
                'title': 'Complex Site',
                'description': 'Complex hierarchy demonstration',
                'base_url': 'http://localhost:8082'
            },
            'expected_widgets': [
                'cholot-title', 'cholot-texticon', 'cholot-gallery', 'cholot-testimonial',
                'cholot-sidebar', 'cholot-team', 'cholot-button-text'
            ],
            'expected_pages': 1
        }
    
    def _create_business_template_scenario(self) -> Dict[str, Any]:
        """Create realistic business template scenario."""
        return {
            'name': 'Business Template',
            'description': 'Realistic business website template',
            'data': {
                'pages': [
                    {
                        'title': 'Home - Business Solutions',
                        'slug': 'home',
                        'sections': [
                            {
                                'structure': '100',
                                'columns': [{
                                    'width': 100,
                                    'widgets': [
                                        {
                                            'type': 'title',
                                            'title': 'Professional Business Solutions<span>.</span>',
                                            'header_size': 'h1',
                                            'align': 'center'
                                        },
                                        {
                                            'type': 'texticon',
                                            'title': 'Excellence in Service',
                                            'icon': 'fas fa-award',
                                            'subtitle': 'Trusted Partner',
                                            'text': 'We deliver professional excellence and innovative solutions to help your business thrive in today\'s competitive market.'
                                        }
                                    ]
                                }]
                            },
                            {
                                'structure': '33',
                                'columns': [
                                    {
                                        'width': 33.33,
                                        'widgets': [{
                                            'type': 'texticon',
                                            'title': 'Strategic Consulting',
                                            'icon': 'fas fa-lightbulb',
                                            'subtitle': 'Expert Guidance',
                                            'text': 'Strategic business consulting to optimize operations and drive growth.'
                                        }]
                                    },
                                    {
                                        'width': 33.33,
                                        'widgets': [{
                                            'type': 'texticon',
                                            'title': 'Technology Solutions',
                                            'icon': 'fas fa-laptop-code',
                                            'subtitle': 'Modern Tech',
                                            'text': 'Cutting-edge technology solutions tailored to your business needs.'
                                        }]
                                    },
                                    {
                                        'width': 33.33,
                                        'widgets': [{
                                            'type': 'texticon',
                                            'title': '24/7 Support',
                                            'icon': 'fas fa-headset',
                                            'subtitle': 'Always Available',
                                            'text': 'Round-the-clock support to ensure your business operations run smoothly.'
                                        }]
                                    }
                                ]
                            }
                        ]
                    }
                ]
            },
            'site_config': {
                'title': 'Business Solutions Inc.',
                'description': 'Professional business solutions and consulting services',
                'base_url': 'http://localhost:8082'
            },
            'expected_widgets': ['cholot-title', 'cholot-texticon'],
            'expected_texticon_count': 4,
            'expected_pages': 1
        }
    
    def _create_portfolio_template_scenario(self) -> Dict[str, Any]:
        """Create portfolio template scenario."""
        return {
            'name': 'Portfolio Template',
            'description': 'Creative portfolio website template',
            'data': {
                'pages': [{
                    'title': 'Creative Portfolio',
                    'slug': 'portfolio',
                    'sections': [
                        {
                            'structure': '100',
                            'columns': [{
                                'width': 100,
                                'widgets': [
                                    {
                                        'type': 'title',
                                        'title': 'Creative Portfolio<span>.</span>',
                                        'header_size': 'h1',
                                        'align': 'center'
                                    },
                                    {
                                        'type': 'text-line',
                                        'title': 'Showcasing Creative Excellence',
                                        'subtitle': 'Design • Development • Innovation',
                                        'line_width': 80
                                    }
                                ]
                            }]
                        },
                        {
                            'structure': '50',
                            'columns': [
                                {
                                    'width': 50,
                                    'widgets': [{
                                        'type': 'gallery',
                                        'images': [
                                            'http://localhost:8082/portfolio-1.jpg',
                                            'http://localhost:8082/portfolio-2.jpg',
                                            'http://localhost:8082/portfolio-3.jpg',
                                            'http://localhost:8082/portfolio-4.jpg'
                                        ],
                                        'columns': 'col-md-6',
                                        'height': 300
                                    }]
                                },
                                {
                                    'width': 50,
                                    'widgets': [
                                        {
                                            'type': 'team',
                                            'name': 'Alex Designer',
                                            'position': 'Creative Director',
                                            'image_url': 'http://localhost:8082/alex-portrait.jpg',
                                            'social_links': [
                                                {'icon': 'fab fa-behance', 'url': 'https://behance.net/alex'},
                                                {'icon': 'fab fa-dribbble', 'url': 'https://dribbble.com/alex'},
                                                {'icon': 'fab fa-instagram', 'url': 'https://instagram.com/alex'}
                                            ]
                                        },
                                        {
                                            'type': 'button-text',
                                            'text': 'View Full Portfolio',
                                            'url': 'https://portfolio.example.com',
                                            'subtitle': 'See All Projects'
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                }]
            },
            'site_config': {
                'title': 'Alex Designer Portfolio',
                'description': 'Creative design portfolio showcasing innovative work',
                'base_url': 'http://localhost:8082'
            },
            'expected_widgets': ['cholot-title', 'cholot-text-line', 'cholot-gallery', 'cholot-team', 'cholot-button-text'],
            'expected_pages': 1
        }
    
    def _create_blog_template_scenario(self) -> Dict[str, Any]:
        """Create blog template scenario."""
        return {
            'name': 'Blog Template',
            'description': 'Blog website template with post listings',
            'data': {
                'pages': [{
                    'title': 'Tech Blog',
                    'slug': 'blog',
                    'sections': [
                        {
                            'structure': '100',
                            'columns': [{
                                'width': 100,
                                'widgets': [{
                                    'type': 'title',
                                    'title': 'Technology Blog<span>.</span>',
                                    'header_size': 'h1',
                                    'align': 'center'
                                }]
                            }]
                        },
                        {
                            'structure': '66',
                            'columns': [
                                {
                                    'width': 66.67,
                                    'widgets': [
                                        {
                                            'type': 'post-four',
                                            'post_count': 4,
                                            'column': 'two',
                                            'button_text': 'Read Full Article',
                                            'categories': ['technology', 'innovation', 'tutorials']
                                        },
                                        {
                                            'type': 'post-three',
                                            'post_count': 3,
                                            'column': 'one',
                                            'button_text': 'Continue Reading',
                                            'categories': ['news', 'updates']
                                        }
                                    ]
                                },
                                {
                                    'width': 33.33,
                                    'widgets': [
                                        {
                                            'type': 'sidebar',
                                            'width': '320px'
                                        },
                                        {
                                            'type': 'texticon',
                                            'title': 'About This Blog',
                                            'icon': 'fas fa-info-circle',
                                            'subtitle': 'Tech Insights',
                                            'text': 'Stay updated with the latest technology trends, tutorials, and industry insights.'
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                }]
            },
            'site_config': {
                'title': 'Tech Insights Blog',
                'description': 'Technology news, tutorials, and industry insights',
                'base_url': 'http://localhost:8082'
            },
            'expected_widgets': ['cholot-title', 'cholot-post-four', 'cholot-post-three', 'cholot-sidebar', 'cholot-texticon'],
            'expected_pages': 1
        }
    
    def _create_multi_language_scenario(self) -> Dict[str, Any]:
        """Create multi-language scenario."""
        return {
            'name': 'Multi-Language Test',
            'description': 'Tests handling of multi-language content',
            'data': {
                'pages': [{
                    'title': 'Multilingual Site - Mehrsprachige Website',
                    'slug': 'multilingual',
                    'sections': [
                        {
                            'structure': '50',
                            'columns': [
                                {
                                    'width': 50,
                                    'widgets': [{
                                        'type': 'texticon',
                                        'title': 'English Services',
                                        'icon': 'fas fa-flag-usa',
                                        'subtitle': 'Professional Services',
                                        'text': 'We provide professional services in English for international clients.'
                                    }]
                                },
                                {
                                    'width': 50,
                                    'widgets': [{
                                        'type': 'texticon',
                                        'title': 'Deutsche Dienstleistungen',
                                        'icon': 'fas fa-flag-germany',
                                        'subtitle': 'Professionelle Services',
                                        'text': 'Wir bieten professionelle Dienstleistungen auf Deutsch für unsere Kunden.'
                                    }]
                                }
                            ]
                        }
                    ]
                }]
            },
            'site_config': {
                'title': 'Multilingual Business',
                'description': 'International business services in multiple languages',
                'base_url': 'http://localhost:8082'
            },
            'expected_widgets': ['cholot-texticon'],
            'expected_pages': 1
        }

    def save_scenarios_to_files(self, output_dir: Path):
        """Save all scenarios to individual JSON files."""
        output_dir.mkdir(exist_ok=True)
        
        for scenario_name, scenario_data in self.scenarios.items():
            file_path = output_dir / f"scenario_{scenario_name}.json"
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(scenario_data, f, indent=2, ensure_ascii=False)
        
        print(f"Saved {len(self.scenarios)} scenarios to {output_dir}")


if __name__ == "__main__":
    manager = TestScenarioManager()
    
    print("Available Test Scenarios:")
    print("=" * 50)
    
    for name in manager.get_scenario_names():
        scenario = manager.get_scenario(name)
        print(f"• {scenario['name']}: {scenario['description']}")
    
    # Save scenarios to files
    output_dir = Path(__file__).parent / "test_scenarios"
    manager.save_scenarios_to_files(output_dir)
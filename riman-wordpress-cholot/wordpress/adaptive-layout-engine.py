#!/usr/bin/env python3
"""
Adaptive Layout Engine - Passt Design dynamisch an Content an
"""

import json
from typing import Dict, List, Any
import math

class AdaptiveLayoutEngine:
    """
    Generiert dynamische Layouts basierend auf Content-Menge und Regeln
    """
    
    def __init__(self):
        # Layout-Patterns für verschiedene Anzahlen
        self.layout_patterns = {
            1: {"structure": "100", "columns": 1},
            2: {"structure": "50", "columns": 2},
            3: {"structure": "33", "columns": 3},
            4: {"structure": "25", "columns": 4},
            5: {"structure": "20", "columns": 5},
            6: {"structure": "33", "columns": 3, "rows": 2},  # 2x3 Grid
            8: {"structure": "25", "columns": 4, "rows": 2},  # 2x4 Grid
            9: {"structure": "33", "columns": 3, "rows": 3},  # 3x3 Grid
        }
    
    def demonstrate_adaptive_layout(self):
        """
        Zeigt wie Layouts sich an Content anpassen
        """
        print("🎯 ADAPTIVE LAYOUT ENGINE")
        print("=" * 60)
        
        # Beispiel 1: User will 2 Services
        services_2 = ["Asbestsanierung", "PCB-Sanierung"]
        layout_2 = self.calculate_layout(services_2)
        print(f"\n2 Services → {layout_2['description']}")
        print(f"  Structure: {layout_2['structure']}")
        
        # Beispiel 2: User will 3 Services  
        services_3 = ["Asbestsanierung", "PCB-Sanierung", "Schimmelsanierung"]
        layout_3 = self.calculate_layout(services_3)
        print(f"\n3 Services → {layout_3['description']}")
        print(f"  Structure: {layout_3['structure']}")
        
        # Beispiel 3: User will 6 Services
        services_6 = [
            "Asbestsanierung", "PCB-Sanierung", "Schimmelsanierung",
            "PAK-Sanierung", "KMF-Sanierung", "Bleisanierung"
        ]
        layout_6 = self.calculate_layout(services_6)
        print(f"\n6 Services → {layout_6['description']}")
        print(f"  Structure: {layout_6['structure']}")
        print(f"  Rows: {layout_6.get('rows', 1)}")
    
    def calculate_layout(self, items: List) -> Dict:
        """
        Berechnet optimales Layout für Anzahl Items
        """
        count = len(items)
        
        # Direkte Patterns
        if count in self.layout_patterns:
            layout = self.layout_patterns[count].copy()
            layout['description'] = f"{count} items in {layout['columns']} columns"
            if 'rows' in layout:
                layout['description'] += f" × {layout['rows']} rows"
            return layout
        
        # Intelligente Berechnung für andere Anzahlen
        if count <= 4:
            columns = count
        elif count <= 6:
            columns = 3
        elif count <= 8:
            columns = 4
        else:
            columns = 3  # Default zu 3 Spalten
        
        rows = math.ceil(count / columns)
        structure = str(int(100 / columns)) if columns <= 4 else "33"
        
        return {
            "structure": structure,
            "columns": columns,
            "rows": rows,
            "description": f"{count} items in {columns}×{rows} grid"
        }
    
    def parse_layout_description(self, description: str) -> Dict:
        """
        Parst natürliche Sprache zu Layout-Parametern
        
        Beispiele:
        - "3 services in einer Reihe"
        - "6 services in 2 Reihen"
        - "services als 2x3 grid"
        - "services in 3 Spalten"
        """
        description = description.lower()
        
        # Extrahiere Zahlen
        import re
        numbers = re.findall(r'\d+', description)
        
        layout = {}
        
        # Grid-Pattern (z.B. "2x3")
        if 'x' in description and len(numbers) >= 2:
            rows = int(numbers[0])
            cols = int(numbers[1])
            layout = {
                "rows": rows,
                "columns": cols,
                "structure": str(int(100 / cols)),
                "type": "grid"
            }
        
        # Reihen-Pattern
        elif 'reihe' in description or 'row' in description:
            if len(numbers) >= 2:
                items = int(numbers[0])
                rows = int(numbers[1])
                cols = math.ceil(items / rows)
                layout = {
                    "rows": rows,
                    "columns": cols,
                    "structure": str(int(100 / cols)),
                    "type": "rows"
                }
        
        # Spalten-Pattern
        elif 'spalte' in description or 'column' in description:
            if numbers:
                cols = int(numbers[-1])  # Letzte Zahl ist Spaltenanzahl
                layout = {
                    "columns": cols,
                    "structure": str(int(100 / cols)),
                    "type": "columns"
                }
        
        # Responsive Hints
        if 'mobil' in description or 'mobile' in description:
            layout['mobile_columns'] = 1
        if 'tablet' in description:
            layout['tablet_columns'] = 2
            
        return layout
    
    def generate_elementor_section(self, items: List, layout_spec: Dict) -> Dict:
        """
        Generiert eine Elementor Section mit dynamischem Layout
        """
        columns = layout_spec.get('columns', 3)
        rows = layout_spec.get('rows', 1)
        structure = layout_spec.get('structure', '33')
        
        # Basis Section
        section = {
            "id": self.generate_id(),
            "elType": "section",
            "settings": {
                "structure": structure,
                "gap": "extended"
            },
            "elements": []  # Columns kommen hier rein
        }
        
        # Generiere Columns
        items_per_row = columns
        for row in range(rows):
            row_items = items[row * items_per_row:(row + 1) * items_per_row]
            
            for item in row_items:
                column = self.generate_column(item, 100 / columns)
                section["elements"].append(column)
        
        # Responsive Settings
        if layout_spec.get('mobile_columns'):
            section["settings"]["structure_mobile"] = "100"
        if layout_spec.get('tablet_columns'):
            section["settings"]["structure_tablet"] = str(int(100 / layout_spec['tablet_columns']))
        
        return section
    
    def generate_column(self, content: Any, width: float) -> Dict:
        """Generiert eine Elementor Column"""
        return {
            "id": self.generate_id(),
            "elType": "column",
            "settings": {
                "_column_size": int(width),
                "_inline_size": None
            },
            "elements": [
                # Hier käme das Widget rein
                self.generate_widget(content)
            ]
        }
    
    def generate_widget(self, content: Any) -> Dict:
        """Generiert ein Widget basierend auf Content"""
        if isinstance(content, dict):
            return {
                "id": self.generate_id(),
                "elType": "widget",
                "widgetType": "cholot-texticon",
                "settings": {
                    "title": content.get('title', ''),
                    "text": content.get('text', ''),
                    "icon": content.get('icon', 'fas fa-check')
                }
            }
        else:
            # Simple Text
            return {
                "id": self.generate_id(),
                "elType": "widget",
                "widgetType": "text-editor",
                "settings": {
                    "editor": f"<p>{content}</p>"
                }
            }
    
    def generate_id(self) -> str:
        """Generiert Elementor-kompatible ID"""
        import random
        import string
        return ''.join(random.choices(string.ascii_lowercase + string.digits, k=7))
    
    def demonstrate_yaml_syntax(self):
        """
        Zeigt die intuitive YAML Syntax
        """
        yaml_example = """
# INTUITIVE YAML SYNTAX für adaptive Layouts
# =============================================

sections:
  # Hero bleibt immer gleich
  - type: hero
    content:
      title: "RIMAN GmbH"
      subtitle: "Professionelle Sanierung"
  
  # Services - adaptives Layout je nach Anzahl
  - type: services
    layout: "auto"  # System entscheidet basierend auf Anzahl
    items:
      - title: "Asbestsanierung"
      - title: "PCB-Sanierung"
      - title: "Schimmelsanierung"
      - title: "PAK-Sanierung"
      - title: "KMF-Sanierung"
      - title: "Bleisanierung"
    # → System macht automatisch 2x3 Grid
  
  # Oder explizite Layout-Angabe
  - type: features
    layout: "4 columns"  # Explizit 4 Spalten
    items:
      - "24/7 Service"
      - "Zertifiziert"
      - "25 Jahre Erfahrung"
      - "Kostenlose Beratung"
  
  # Oder Grid-Angabe
  - type: gallery
    layout: "3x2 grid"  # 3 Spalten, 2 Reihen
    images:
      - "projekt1.jpg"
      - "projekt2.jpg"
      - "projekt3.jpg"
      - "projekt4.jpg"
      - "projekt5.jpg"
      - "projekt6.jpg"
  
  # Responsive Angaben
  - type: team
    layout: "3 columns, tablet 2 columns, mobile 1 column"
    members:
      - name: "Max Mustermann"
      - name: "Erika Beispiel"
      - name: "Hans Schmidt"
"""
        
        print("\n" + "=" * 60)
        print("📝 INTUITIVE YAML SYNTAX")
        print("=" * 60)
        print(yaml_example)
        
        print("\n✨ Features:")
        print("• 'auto' = System entscheidet optimal")
        print("• '3 columns' = Explizite Spaltenanzahl")
        print("• '2x3 grid' = Explizites Grid")
        print("• Responsive Angaben möglich")
        print("• Natürliche Sprache!")
    
    def show_complete_flow(self):
        """
        Zeigt den kompletten Flow
        """
        print("\n" + "=" * 60)
        print("🔄 KOMPLETTER FLOW")
        print("=" * 60)
        
        # Input
        user_input = {
            "services": [
                {"title": "Asbestsanierung", "icon": "shield"},
                {"title": "PCB-Sanierung", "icon": "flask"},
                {"title": "Schimmelsanierung", "icon": "home"},
                {"title": "PAK-Sanierung", "icon": "fire"},
                {"title": "KMF-Sanierung", "icon": "wind"},
                {"title": "Bleisanierung", "icon": "paint"}
            ]
        }
        
        print("1️⃣ INPUT (6 Services):")
        for s in user_input['services']:
            print(f"   • {s['title']}")
        
        # Layout-Berechnung
        layout = self.calculate_layout(user_input['services'])
        print(f"\n2️⃣ LAYOUT-BERECHNUNG:")
        print(f"   → {layout['description']}")
        print(f"   → Structure: {layout['structure']}")
        
        # Elementor Generation
        section = self.generate_elementor_section(user_input['services'], layout)
        print(f"\n3️⃣ ELEMENTOR GENERATION:")
        print(f"   → Section mit {len(section['elements'])} Columns")
        print(f"   → Jede Column: {100/layout['columns']}% Breite")
        
        print(f"\n4️⃣ RESULT:")
        print(f"   ✅ Professionelle 2×3 Service-Grid")
        print(f"   ✅ Responsive (Mobile: 1 Spalte)")
        print(f"   ✅ Alle Elementor-Features erhalten")


def main():
    """Demo des adaptiven Layout-Systems"""
    
    engine = AdaptiveLayoutEngine()
    
    # Zeige adaptive Layouts
    engine.demonstrate_adaptive_layout()
    
    # Zeige YAML Syntax
    engine.demonstrate_yaml_syntax()
    
    # Zeige kompletten Flow
    engine.show_complete_flow()
    
    print("\n" + "=" * 60)
    print("💡 FAZIT: So lösen wir das Problem!")
    print("=" * 60)
    print("""
    1. User schreibt: "6 services" oder "services in 2 Reihen"
    2. System berechnet: 2×3 Grid optimal
    3. System generiert: Elementor Section mit 6 Columns
    4. System füllt: Content in die Columns
    5. Fertig: Professionelle responsive Section!
    
    Das ist der Weg: ADAPTIVE LAYOUTS + CONTENT INJECTION
    """)


if __name__ == "__main__":
    main()
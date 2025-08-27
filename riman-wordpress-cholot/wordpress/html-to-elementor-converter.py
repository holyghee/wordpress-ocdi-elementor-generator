#!/usr/bin/env python3
"""
HTML/CSS to Elementor JSON Converter - Zeigt die Herausforderungen und Möglichkeiten
"""

from bs4 import BeautifulSoup
import cssutils
import json
import re

class HTMLToElementorConverter:
    """
    Konvertiert HTML+CSS zu Elementor JSON
    """
    
    def show_the_challenge(self):
        """
        Zeigt warum HTML→Elementor schwierig ist
        """
        print("🎯 HTML/CSS → ELEMENTOR JSON CONVERSION")
        print("=" * 60)
        
        # Simples HTML Beispiel
        simple_html = """
        <section class="hero" style="background: #232323; padding: 60px 0;">
            <div class="container">
                <h1 style="font-size: 45px; color: white;">RIMAN GmbH</h1>
                <p style="font-size: 18px; color: #b68c2f;">Professionelle Sanierung</p>
                <button style="background: #b68c2f; color: white; padding: 15px 30px;">
                    Kontakt
                </button>
            </div>
        </section>
        """
        
        print("📝 SIMPLES HTML:")
        print(simple_html)
        
        # Was Elementor daraus macht
        elementor_json = {
            "id": "abc123",
            "elType": "section",
            "settings": {
                "background_background": "classic",
                "background_color": "#232323",
                "padding": {
                    "unit": "px",
                    "top": 60,
                    "right": 0,
                    "bottom": 60,
                    "left": 0,
                    "isLinked": False
                },
                "padding_tablet": {
                    "unit": "px",
                    "top": 40,
                    "right": 0,
                    "bottom": 40,
                    "left": 0
                },
                "padding_mobile": {
                    "unit": "px",
                    "top": 30,
                    "right": 0,
                    "bottom": 30,
                    "left": 0
                }
            },
            "elements": [
                {
                    "id": "def456",
                    "elType": "column",
                    "settings": {
                        "_column_size": 100,
                        "_inline_size": None
                    },
                    "elements": [
                        {
                            "id": "ghi789",
                            "elType": "widget",
                            "widgetType": "heading",
                            "settings": {
                                "title": "RIMAN GmbH",
                                "header_size": "h1",
                                "title_color": "#ffffff",
                                "typography_typography": "custom",
                                "typography_font_size": {
                                    "unit": "px",
                                    "size": 45,
                                    "sizes": []
                                },
                                "typography_font_size_tablet": {
                                    "unit": "px",
                                    "size": 35
                                },
                                "typography_font_size_mobile": {
                                    "unit": "px",
                                    "size": 28
                                }
                            }
                        }
                        # ... weitere Widgets
                    ]
                }
            ]
        }
        
        print("\n🔄 ELEMENTOR JSON (nur Auszug!):")
        print(json.dumps(elementor_json, indent=2)[:500] + "...")
        
        print("\n⚠️  DIE PROBLEME:")
        print("1. HTML: 'padding: 60px 0' → Elementor: komplexes Object mit top/right/bottom/left")
        print("2. HTML: eine font-size → Elementor: Desktop + Tablet + Mobile Versionen")
        print("3. HTML: keine IDs → Elementor: Unique IDs für alles")
        print("4. HTML: keine Widget-Types → Elementor: spezifische Widget-Typen")
        print("5. HTML: simple styles → Elementor: 50+ Settings pro Element")
    
    def convert_html_to_elementor(self, html: str, css: str = "") -> Dict:
        """
        Basis-Converter für HTML zu Elementor
        """
        soup = BeautifulSoup(html, 'html.parser')
        
        # Parse CSS wenn vorhanden
        styles = self.parse_css(css) if css else {}
        
        # Konvertiere HTML Structure
        elementor_data = []
        
        for section in soup.find_all(['section', 'div'], class_=lambda x: x and 'section' in x):
            elementor_section = self.convert_section(section, styles)
            elementor_data.append(elementor_section)
        
        return elementor_data
    
    def convert_section(self, section_element, styles: Dict) -> Dict:
        """
        Konvertiert HTML Section zu Elementor Section
        """
        section_id = self.generate_id()
        
        # Extrahiere Styles
        section_styles = self.extract_styles(section_element)
        
        # Basis Section Structure
        section = {
            "id": section_id,
            "elType": "section",
            "settings": {},
            "elements": []  # Columns
        }
        
        # Konvertiere Background
        if 'background' in section_styles or 'background-color' in section_styles:
            bg_color = section_styles.get('background-color', section_styles.get('background', ''))
            if bg_color:
                section['settings']['background_background'] = 'classic'
                section['settings']['background_color'] = bg_color
        
        # Konvertiere Padding
        if 'padding' in section_styles:
            section['settings']['padding'] = self.parse_spacing(section_styles['padding'])
        
        # Finde Columns (divs innerhalb der Section)
        columns = section_element.find_all('div', recursive=False)
        if not columns:
            # Wenn keine Columns, mache eine 100% Column
            columns = [section_element]
        
        # Konvertiere Columns
        for col in columns:
            column = self.convert_column(col)
            section['elements'].append(column)
        
        return section
    
    def convert_column(self, column_element) -> Dict:
        """
        Konvertiert HTML Div zu Elementor Column
        """
        column = {
            "id": self.generate_id(),
            "elType": "column",
            "settings": {
                "_column_size": 100,  # Default 100%
                "_inline_size": None
            },
            "elements": []  # Widgets
        }
        
        # Finde Widgets (h1, h2, p, button, img, etc.)
        for element in column_element.find_all(['h1', 'h2', 'h3', 'p', 'button', 'img', 'a']):
            widget = self.convert_to_widget(element)
            if widget:
                column['elements'].append(widget)
        
        return column
    
    def convert_to_widget(self, element) -> Dict:
        """
        Konvertiert HTML Element zu Elementor Widget
        """
        tag = element.name
        styles = self.extract_styles(element)
        
        widget = {
            "id": self.generate_id(),
            "elType": "widget",
            "settings": {}
        }
        
        # Heading Widget
        if tag in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
            widget['widgetType'] = 'heading'
            widget['settings']['title'] = element.get_text(strip=True)
            widget['settings']['header_size'] = tag
            
            if 'color' in styles:
                widget['settings']['title_color'] = styles['color']
            if 'font-size' in styles:
                widget['settings']['typography_typography'] = 'custom'
                widget['settings']['typography_font_size'] = {
                    "unit": "px",
                    "size": int(re.findall(r'\d+', styles['font-size'])[0]) if re.findall(r'\d+', styles['font-size']) else 16
                }
        
        # Text Widget
        elif tag == 'p':
            widget['widgetType'] = 'text-editor'
            widget['settings']['editor'] = f"<p>{element.get_text(strip=True)}</p>"
        
        # Button Widget
        elif tag in ['button', 'a']:
            widget['widgetType'] = 'button'
            widget['settings']['text'] = element.get_text(strip=True)
            
            if 'href' in element.attrs:
                widget['settings']['link'] = {
                    "url": element['href'],
                    "is_external": "",
                    "nofollow": ""
                }
            
            if 'background' in styles or 'background-color' in styles:
                widget['settings']['background_color'] = styles.get('background-color', styles.get('background'))
        
        # Image Widget
        elif tag == 'img':
            widget['widgetType'] = 'image'
            widget['settings']['image'] = {
                "url": element.get('src', ''),
                "id": "",
                "alt": element.get('alt', '')
            }
        
        return widget
    
    def extract_styles(self, element) -> Dict:
        """
        Extrahiert inline styles aus HTML Element
        """
        styles = {}
        if element.has_attr('style'):
            style_str = element['style']
            # Parse inline styles
            for rule in style_str.split(';'):
                if ':' in rule:
                    prop, value = rule.split(':', 1)
                    styles[prop.strip()] = value.strip()
        return styles
    
    def parse_spacing(self, spacing_value: str) -> Dict:
        """
        Parst CSS spacing zu Elementor Format
        """
        values = spacing_value.split()
        
        if len(values) == 1:
            # Alle Seiten gleich
            size = int(re.findall(r'\d+', values[0])[0]) if re.findall(r'\d+', values[0]) else 0
            return {
                "unit": "px",
                "top": size,
                "right": size,
                "bottom": size,
                "left": size,
                "isLinked": True
            }
        elif len(values) == 2:
            # Vertikal Horizontal
            v = int(re.findall(r'\d+', values[0])[0]) if re.findall(r'\d+', values[0]) else 0
            h = int(re.findall(r'\d+', values[1])[0]) if re.findall(r'\d+', values[1]) else 0
            return {
                "unit": "px",
                "top": v,
                "right": h,
                "bottom": v,
                "left": h,
                "isLinked": False
            }
        elif len(values) == 4:
            # Top Right Bottom Left
            return {
                "unit": "px",
                "top": int(re.findall(r'\d+', values[0])[0]) if re.findall(r'\d+', values[0]) else 0,
                "right": int(re.findall(r'\d+', values[1])[0]) if re.findall(r'\d+', values[1]) else 0,
                "bottom": int(re.findall(r'\d+', values[2])[0]) if re.findall(r'\d+', values[2]) else 0,
                "left": int(re.findall(r'\d+', values[3])[0]) if re.findall(r'\d+', values[3]) else 0,
                "isLinked": False
            }
        
        return {"unit": "px", "top": 0, "right": 0, "bottom": 0, "left": 0, "isLinked": False}
    
    def parse_css(self, css: str) -> Dict:
        """
        Parst CSS zu Dictionary
        """
        # Vereinfacht - würde cssutils oder ähnliches nutzen
        return {}
    
    def generate_id(self) -> str:
        """Generiert Elementor ID"""
        import random
        import string
        return ''.join(random.choices(string.ascii_lowercase + string.digits, k=7))
    
    def demonstrate_better_approach(self):
        """
        Zeigt einen besseren Ansatz
        """
        print("\n" + "=" * 60)
        print("💡 BESSERER ANSATZ: Semantic HTML + Templates")
        print("=" * 60)
        
        semantic_html = """
<!-- Semantic HTML mit data-attributes -->
<section data-element="hero" data-layout="centered" data-theme="dark">
    <h1 data-animate="fadeIn">RIMAN GmbH</h1>
    <p data-style="subtitle">Professionelle Sanierung seit 1998</p>
    <button data-action="cta" data-style="primary">Kontakt aufnehmen</button>
</section>

<section data-element="services" data-columns="3">
    <div data-service="asbestos">
        <h3>Asbestsanierung</h3>
        <p>Sichere und zertifizierte Entfernung</p>
    </div>
    <div data-service="pcb">
        <h3>PCB-Sanierung</h3>
        <p>Umweltgerechte Entsorgung</p>
    </div>
    <div data-service="mold">
        <h3>Schimmelsanierung</h3>
        <p>Nachhaltige Beseitigung</p>
    </div>
</section>
        """
        
        print("📝 SEMANTIC HTML mit data-attributes:")
        print(semantic_html)
        
        print("\n✨ VORTEILE:")
        print("1. HTML bleibt lesbar und einfach")
        print("2. data-attributes geben Kontext")
        print("3. System mapped zu vordefinierten Elementor-Templates")
        print("4. CSS-Classes triggern Template-Varianten")
        
        print("\n🔄 MAPPING:")
        print('data-element="hero" → Elementor Hero Template')
        print('data-columns="3" → 3-Column Section')
        print('data-theme="dark" → Dark Background Settings')
        print('data-animate="fadeIn" → Animation Settings')
        
        return semantic_html
    
    def show_realistic_solution(self):
        """
        Zeigt realistische Lösung
        """
        print("\n" + "=" * 60)
        print("🎯 REALISTISCHE LÖSUNG")
        print("=" * 60)
        
        print("""
        NICHT: Beliebiges HTML → Elementor ❌
        (zu komplex, zu viele Edge Cases)
        
        SONDERN: Strukturiertes HTML → Elementor ✅
        
        1. DEFINIERE HTML-Komponenten:
           <article class="riman-service">
             <h3>{{title}}</h3>
             <p>{{description}}</p>
           </article>
        
        2. MAPPE zu Elementor-Widgets:
           .riman-service → cholot-texticon Widget
        
        3. STYLE mit Template-Presets:
           class="style-modern" → Modern Template Settings
           class="style-classic" → Classic Template Settings
        
        4. NUTZE data-attributes für Optionen:
           data-icon="shield" → Icon Setting
           data-color="primary" → Color Scheme
        
        Das ist machbar und praktisch!
        """)


def main():
    """Demo HTML zu Elementor Conversion"""
    
    converter = HTMLToElementorConverter()
    
    # Zeige die Herausforderung
    converter.show_the_challenge()
    
    # Zeige besseren Ansatz
    converter.demonstrate_better_approach()
    
    # Zeige realistische Lösung
    converter.show_realistic_solution()
    
    print("\n" + "=" * 60)
    print("📌 FAZIT")
    print("=" * 60)
    print("""
    HTML → Elementor ist MÖGLICH aber:
    
    ❌ Nicht für beliebiges HTML
    ❌ Verliert viele Elementor-Features
    ❌ Keine responsive Settings
    ❌ Keine Animationen
    
    ✅ BESSER: Strukturiertes Semantic HTML
    ✅ Mit data-attributes für Mapping
    ✅ Vordefinierte Component-Library
    ✅ Template-basiertes Styling
    
    Der Weg: HTML als CONTENT-DEFINITION,
    nicht als DESIGN-DEFINITION!
    """)


if __name__ == "__main__":
    main()
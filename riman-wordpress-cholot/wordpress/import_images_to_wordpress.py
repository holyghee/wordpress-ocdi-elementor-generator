#!/usr/bin/env python3
"""
Importiert Bilder vom lokalen Image-Server in die WordPress Media Library
"""

import os
import subprocess
import json
from pathlib import Path

class WordPressImageImporter:
    def __init__(self):
        self.image_server_dir = Path("/Users/holgerbrandt/dev/claude-code/projects/riman-wordpress/image-server")
        self.image_mapping = {}
        
    def import_images(self):
        """Importiere alle relevanten Bilder in WordPress"""
        print("🖼️  Importiere Bilder in WordPress Media Library...")
        
        # Liste der wichtigsten Bilder für RIMAN
        priority_images = [
            "systematischer-gebaeuderueckbau-kreislaufwirtschaft.jpg",
            "asbestsanierung-schutzausruestung-fachpersonal.jpg",
            "schadstoffsanierung-industrieanlage-riman-gmbh.jpg",
            "dr-michael-riman-geschaeftsfuehrer.jpg",
            "sabine-weber-projektleitung.jpg",
            "thomas-mueller-technische-leitung.jpg",
            "sicherheitsvorbereitung-schutzausruestung-schritt-3.jpg",
            "sanierung-durchfuehrung-fachgerecht-schritt-4.jpg",
            "luftqualitaet-monitoring-echtzeitdaten-schritt-5.jpg",
            "materialverarbeitung-entsorgung-vorschriften-schritt-6.jpg",
            "qualitaetskontrolle-abnahme-pruefung-schritt-7.jpg",
            "zertifizierung-dokumentation-abschluss-schritt-8.jpg",
            "nachhaltiger-rueckbau-baustelle-recycling.jpg",
            "altlastensanierung-grundwasser-bodenschutz.jpg",
            "umweltingenieur-bodenproben-analyse-labor.jpg",
            "riman-gmbh-logo.png"
        ]
        
        for image_name in priority_images:
            image_path = self.image_server_dir / image_name
            if image_path.exists():
                # Importiere mit WP-CLI
                cmd = [
                    "php", "wp-cli.phar", "media", "import",
                    str(image_path),
                    "--title=" + image_name.replace("-", " ").replace(".jpg", "").replace(".png", "").title(),
                    "--alt=" + image_name.replace("-", " ").replace(".jpg", "").replace(".png", ""),
                    "--porcelain"  # Gibt nur die ID zurück
                ]
                
                try:
                    result = subprocess.run(cmd, capture_output=True, text=True, check=True)
                    media_id = result.stdout.strip()
                    
                    # Hole die URL des importierten Bildes
                    url_cmd = ["php", "wp-cli.phar", "post", "get", media_id, "--field=guid"]
                    url_result = subprocess.run(url_cmd, capture_output=True, text=True, check=True)
                    media_url = url_result.stdout.strip()
                    
                    self.image_mapping[f"http://localhost:8082/{image_name}"] = {
                        "id": media_id,
                        "url": media_url,
                        "title": image_name.replace("-", " ").replace(".jpg", "").replace(".png", "").title()
                    }
                    
                    print(f"  ✅ {image_name} -> ID: {media_id}")
                    
                except subprocess.CalledProcessError as e:
                    print(f"  ❌ Fehler bei {image_name}: {e.stderr}")
        
        # Speichere Mapping für späteren Gebrauch
        with open("image_mapping.json", "w") as f:
            json.dump(self.image_mapping, f, indent=2, ensure_ascii=False)
        
        print(f"\n✅ {len(self.image_mapping)} Bilder importiert")
        print(f"   Mapping gespeichert in: image_mapping.json")
        
        return self.image_mapping

if __name__ == "__main__":
    importer = WordPressImageImporter()
    importer.import_images()
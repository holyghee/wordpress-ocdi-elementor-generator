/**
 * Service Cards Comparison Script
 * Compares Service Cards sections between Cholot Original and RIMAN Implementation
 * 
 * Usage:
 * 1. Install Playwright: npm install playwright
 * 2. Run: node service-cards-comparison.js
 */

const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

class ServiceCardsComparator {
    constructor() {
        this.results = {
            cholot: {
                url: 'http://localhost:8080',
                serviceCards: [],
                layout: {},
                colors: {},
                icons: [],
                errors: []
            },
            riman: {
                url: 'http://localhost:8081/?page_id=3000',
                serviceCards: [],
                layout: {},
                colors: {},
                icons: [],
                errors: []
            },
            comparison: {
                cardCount: {},
                layoutDifferences: [],
                colorDifferences: [],
                iconDifferences: [],
                overallMatch: 0
            }
        };
    }

    async analyzeSite(page, site) {
        try {
            console.log(`🔍 Analyzing ${site} site...`);
            
            // Navigate to site
            await page.goto(this.results[site].url, { waitUntil: 'networkidle' });
            
            // Wait a bit for dynamic content to load
            await page.waitForTimeout(3000);
            
            // Take initial screenshot
            await page.screenshot({
                path: `${site}-full-page.png`,
                fullPage: true
            });
            
            // Look for Service Cards sections with multiple selectors
            const serviceCardSelectors = [
                '.elementor-widget-cholot-texticon', // Cholot texticon widgets
                '.service-card',
                '.cholot-texticon',
                '[class*="service"]',
                '[class*="card"]',
                '.elementor-section [class*="service"]',
                '.elementor-column [class*="service"]'
            ];
            
            let serviceCards = [];
            
            for (const selector of serviceCardSelectors) {
                try {
                    const elements = await page.$$(selector);
                    if (elements.length > 0) {
                        console.log(`Found ${elements.length} elements with selector: ${selector}`);
                        
                        for (const element of elements) {
                            const cardData = await this.analyzeServiceCard(page, element);
                            if (cardData) {
                                cardData.selector = selector;
                                serviceCards.push(cardData);
                            }
                        }
                    }
                } catch (error) {
                    console.log(`Error with selector ${selector}:`, error.message);
                }
            }
            
            // Analyze page structure
            const pageStructure = await page.evaluate(() => {
                const sections = document.querySelectorAll('.elementor-section');
                const serviceElements = document.querySelectorAll('[class*="service"], [class*="card"]');
                const backgroundElements = document.querySelectorAll('[style*="background"]');
                
                return {
                    totalSections: sections.length,
                    serviceElements: serviceElements.length,
                    backgroundElements: backgroundElements.length,
                    title: document.title
                };
            });
            
            // Look for specific Service Card indicators
            const serviceCardIndicators = await page.evaluate(() => {
                const results = {
                    cholotTexticon: document.querySelectorAll('.cholot-texticon, .elementor-widget-cholot-texticon').length,
                    iconsWithGoldenColor: 0,
                    cardsWithBorders: 0,
                    cardsWithGoldenAccents: 0
                };
                
                // Check for golden color (#b68c2f)
                const allElements = document.querySelectorAll('*');
                allElements.forEach(el => {
                    const styles = getComputedStyle(el);
                    if (styles.color.includes('b68c2f') || 
                        styles.backgroundColor.includes('b68c2f') || 
                        styles.borderColor.includes('b68c2f')) {
                        results.iconsWithGoldenColor++;
                    }
                    
                    if (styles.border !== 'none' && styles.border !== '') {
                        results.cardsWithBorders++;
                    }
                });
                
                return results;
            });
            
            // Store results
            this.results[site].serviceCards = serviceCards;
            this.results[site].layout = {
                ...pageStructure,
                ...serviceCardIndicators
            };
            
            // Take screenshot of service cards area if found
            if (serviceCards.length > 0) {
                try {
                    const firstCard = await page.$(serviceCardSelectors.find(sel => 
                        serviceCards.some(card => card.selector === sel)
                    ));
                    if (firstCard) {
                        const box = await firstCard.boundingBox();
                        if (box) {
                            await page.screenshot({
                                path: `${site}-service-cards-area.png`,
                                clip: {
                                    x: Math.max(0, box.x - 50),
                                    y: Math.max(0, box.y - 50),
                                    width: Math.min(1200, box.width + 100),
                                    height: Math.min(800, box.height + 100)
                                }
                            });
                        }
                    }
                } catch (error) {
                    console.log('Could not take service cards screenshot:', error.message);
                }
            }
            
            console.log(`✅ Found ${serviceCards.length} service cards on ${site} site`);
            
        } catch (error) {
            console.error(`❌ Error analyzing ${site} site:`, error.message);
            this.results[site].errors.push(error.message);
        }
    }
    
    async analyzeServiceCard(page, element) {
        try {
            const cardData = await element.evaluate((el) => {
                const rect = el.getBoundingClientRect();
                const styles = getComputedStyle(el);
                
                // Extract text content
                const title = el.querySelector('[class*="title"]')?.textContent?.trim() || 
                             el.querySelector('h1, h2, h3, h4, h5, h6')?.textContent?.trim() ||
                             '';
                
                const subtitle = el.querySelector('[class*="subtitle"]')?.textContent?.trim() || '';
                const description = el.querySelector('[class*="text"], p')?.textContent?.trim() || '';
                
                // Check for icons
                const iconElement = el.querySelector('i[class*="fa-"], .fas, .far, .fab');
                const iconClass = iconElement ? iconElement.className : '';
                
                // Check colors
                const hasGoldenColor = styles.color.includes('b68c2f') || 
                                     styles.backgroundColor.includes('b68c2f') ||
                                     styles.borderColor.includes('b68c2f');
                
                return {
                    title,
                    subtitle,
                    description,
                    iconClass,
                    hasGoldenColor,
                    backgroundColor: styles.backgroundColor,
                    borderColor: styles.borderColor,
                    color: styles.color,
                    position: {
                        x: rect.x,
                        y: rect.y,
                        width: rect.width,
                        height: rect.height
                    }
                };
            });
            
            return cardData;
        } catch (error) {
            console.log('Error analyzing service card:', error.message);
            return null;
        }
    }
    
    generateComparison() {
        console.log('\n📊 Generating comparison...');
        
        // Card count comparison
        this.results.comparison.cardCount = {
            cholot: this.results.cholot.serviceCards.length,
            riman: this.results.riman.serviceCards.length,
            match: this.results.cholot.serviceCards.length === this.results.riman.serviceCards.length
        };
        
        // Layout comparison
        this.results.comparison.layoutDifferences = [];
        if (this.results.cholot.layout.cholotTexticon !== this.results.riman.layout.cholotTexticon) {
            this.results.comparison.layoutDifferences.push(
                `Cholot texticon widgets: Cholot has ${this.results.cholot.layout.cholotTexticon}, RIMAN has ${this.results.riman.layout.cholotTexticon}`
            );
        }
        
        // Calculate overall match percentage
        let matchPoints = 0;
        let totalPoints = 5;
        
        if (this.results.comparison.cardCount.match) matchPoints++;
        if (Math.abs(this.results.cholot.layout.serviceElements - this.results.riman.layout.serviceElements) <= 2) matchPoints++;
        if (this.results.cholot.layout.iconsWithGoldenColor > 0 && this.results.riman.layout.iconsWithGoldenColor > 0) matchPoints++;
        if (this.results.cholot.serviceCards.length > 0 && this.results.riman.serviceCards.length > 0) matchPoints++;
        if (this.results.comparison.layoutDifferences.length <= 2) matchPoints++;
        
        this.results.comparison.overallMatch = Math.round((matchPoints / totalPoints) * 100);
    }
    
    generateReport() {
        const report = `# Service Cards Comparison Report
Generated: ${new Date().toLocaleString()}

## Sites Analyzed
- **Original Cholot Theme**: ${this.results.cholot.url}
- **RIMAN Implementation**: ${this.results.riman.url}

## Service Cards Analysis

### Card Count Comparison
- **Cholot Original**: ${this.results.comparison.cardCount.cholot} service cards found
- **RIMAN Implementation**: ${this.results.comparison.cardCount.riman} service cards found
- **Match**: ${this.results.comparison.cardCount.match ? '✅ YES' : '❌ NO'}

### Detailed Findings

#### Original Cholot Theme (${this.results.cholot.url})
- **Total Sections**: ${this.results.cholot.layout.totalSections}
- **Service Elements**: ${this.results.cholot.layout.serviceElements}
- **Cholot Texticon Widgets**: ${this.results.cholot.layout.cholotTexticon}
- **Icons with Golden Color**: ${this.results.cholot.layout.iconsWithGoldenColor}
- **Cards with Borders**: ${this.results.cholot.layout.cardsWithBorders}
- **Page Title**: ${this.results.cholot.layout.title}

${this.results.cholot.serviceCards.length > 0 ? `
**Service Cards Found:**
${this.results.cholot.serviceCards.map((card, i) => `
${i + 1}. **${card.title || 'Untitled Card'}**
   - Subtitle: ${card.subtitle || 'None'}
   - Description: ${card.description ? card.description.substring(0, 100) + '...' : 'None'}
   - Icon: ${card.iconClass || 'None'}
   - Has Golden Color (#b68c2f): ${card.hasGoldenColor ? '✅' : '❌'}
   - Selector: ${card.selector}
`).join('')}` : 'No service cards detected'}

#### RIMAN Implementation (${this.results.riman.url})
- **Total Sections**: ${this.results.riman.layout.totalSections}
- **Service Elements**: ${this.results.riman.layout.serviceElements}
- **Cholot Texticon Widgets**: ${this.results.riman.layout.cholotTexticon}
- **Icons with Golden Color**: ${this.results.riman.layout.iconsWithGoldenColor}
- **Cards with Borders**: ${this.results.riman.layout.cardsWithBorders}
- **Page Title**: ${this.results.riman.layout.title}

${this.results.riman.serviceCards.length > 0 ? `
**Service Cards Found:**
${this.results.riman.serviceCards.map((card, i) => `
${i + 1}. **${card.title || 'Untitled Card'}**
   - Subtitle: ${card.subtitle || 'None'}
   - Description: ${card.description ? card.description.substring(0, 100) + '...' : 'None'}
   - Icon: ${card.iconClass || 'None'}
   - Has Golden Color (#b68c2f): ${card.hasGoldenColor ? '✅' : '❌'}
   - Selector: ${card.selector}
`).join('')}` : 'No service cards detected'}

### Key Differences
${this.results.comparison.layoutDifferences.length > 0 ? 
this.results.comparison.layoutDifferences.map(diff => `- ${diff}`).join('\n') : 
'No major layout differences detected'}

### Critical Issues
${this.results.comparison.cardCount.cholot === 0 && this.results.comparison.cardCount.riman === 0 ? 
'🚨 **CRITICAL**: No Service Cards found on either site!' :
this.results.comparison.cardCount.riman === 0 ?
'🚨 **CRITICAL**: Service Cards missing from RIMAN implementation!' :
this.results.comparison.cardCount.cholot > this.results.comparison.cardCount.riman ?
'⚠️ **WARNING**: RIMAN has fewer Service Cards than original' :
'✅ Service Cards appear to be implemented'}

### Screenshots Generated
- cholot-full-page.png - Full page screenshot of original
- riman-full-page.png - Full page screenshot of RIMAN
${this.results.cholot.serviceCards.length > 0 ? '- cholot-service-cards-area.png - Service Cards area (original)' : ''}
${this.results.riman.serviceCards.length > 0 ? '- riman-service-cards-area.png - Service Cards area (RIMAN)' : ''}

### Overall Match Score: ${this.results.comparison.overallMatch}%

### Recommendations
${this.results.comparison.overallMatch < 70 ? `
🚨 **Immediate Action Required**:
1. Verify Service Cards implementation in RIMAN
2. Check if Cholot texticon widgets are properly loaded
3. Ensure golden color (#b68c2f) is applied to icons and accents
4. Review card layout and styling
` : this.results.comparison.overallMatch < 85 ? `
⚠️ **Improvements Needed**:
1. Fine-tune Service Cards styling
2. Verify icon consistency
3. Check color scheme alignment
` : `
✅ **Good Implementation**:
Service Cards appear to be properly implemented with minor differences.
`}

### Errors Encountered
${this.results.cholot.errors.length > 0 ? `**Cholot Site**: ${this.results.cholot.errors.join(', ')}` : ''}
${this.results.riman.errors.length > 0 ? `**RIMAN Site**: ${this.results.riman.errors.join(', ')}` : ''}
${this.results.cholot.errors.length === 0 && this.results.riman.errors.length === 0 ? 'No errors encountered during analysis' : ''}

---
Generated by Service Cards Comparison Tool
`;

        return report;
    }
    
    async run() {
        console.log('🚀 Starting Service Cards Comparison...\n');
        
        const browser = await chromium.launch({
            headless: true, // Set to false to see browser in action
            args: ['--no-sandbox', '--disable-dev-shm-usage']
        });
        
        try {
            const page = await browser.newPage();
            await page.setViewportSize({ width: 1440, height: 900 });
            
            // Analyze both sites
            await this.analyzeSite(page, 'cholot');
            await this.analyzeSite(page, 'riman');
            
            // Generate comparison
            this.generateComparison();
            
            // Generate and save report
            const report = this.generateReport();
            const reportPath = path.join(__dirname, 'service-cards-comparison-report.md');
            fs.writeFileSync(reportPath, report);
            
            // Save raw data for further analysis
            const dataPath = path.join(__dirname, 'service-cards-comparison-data.json');
            fs.writeFileSync(dataPath, JSON.stringify(this.results, null, 2));
            
            console.log('\n📄 Reports generated:');
            console.log(`- ${reportPath}`);
            console.log(`- ${dataPath}`);
            console.log('\n📸 Screenshots saved in current directory');
            
            console.log('\n🎯 Summary:');
            console.log(`Match Score: ${this.results.comparison.overallMatch}%`);
            console.log(`Cholot Cards: ${this.results.comparison.cardCount.cholot}`);
            console.log(`RIMAN Cards: ${this.results.comparison.cardCount.riman}`);
            
        } finally {
            await browser.close();
        }
    }
}

// Run the comparison if called directly
if (require.main === module) {
    const comparator = new ServiceCardsComparator();
    comparator.run().catch(console.error);
}

module.exports = ServiceCardsComparator;
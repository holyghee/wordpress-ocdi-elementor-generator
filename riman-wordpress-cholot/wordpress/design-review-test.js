const { chromium } = require('playwright');

async function conductDesignReview() {
    const browser = await chromium.launch({ headless: false });
    const context = await browser.newContext({
        viewport: { width: 1440, height: 900 }
    });
    
    const page = await context.newPage();
    
    console.log('🔍 Starting comprehensive design review...');
    
    try {
        // Phase 0: Navigate to the page
        console.log('📍 Navigating to RIMAN website...');
        await page.goto('http://localhost:8081/?page_id=3000', { waitUntil: 'networkidle' });
        await page.waitForTimeout(3000); // Wait for any dynamic content
        
        // Phase 1: Check for JavaScript errors
        console.log('🔧 Checking console for JavaScript errors...');
        const consoleMessages = [];
        page.on('console', msg => {
            if (msg.type() === 'error') {
                consoleMessages.push(`ERROR: ${msg.text()}`);
            } else if (msg.type() === 'warning') {
                consoleMessages.push(`WARNING: ${msg.text()}`);
            }
        });
        
        // Phase 2: Take desktop screenshot
        console.log('📸 Taking desktop screenshot...');
        await page.screenshot({ 
            path: 'desktop-view.png', 
            fullPage: true,
            type: 'png'
        });
        
        // Phase 3: Check hero slider functionality
        console.log('🎠 Testing hero slider...');
        const sliderExists = await page.locator('.hero-slider, .slider, .slick-slider').count() > 0;
        console.log(`Slider element found: ${sliderExists}`);
        
        if (sliderExists) {
            // Check if slick is initialized
            const slickInitialized = await page.evaluate(() => {
                const sliders = document.querySelectorAll('.hero-slider, .slider, .slick-slider');
                for (let slider of sliders) {
                    if (slider.classList.contains('slick-initialized')) {
                        return true;
                    }
                }
                return false;
            });
            console.log(`Slick slider initialized: ${slickInitialized}`);
            
            // Check for slide images
            const slideImages = await page.locator('.hero-slider img, .slider img, .slick-slide img').count();
            console.log(`Number of slider images found: ${slideImages}`);
        }
        
        // Phase 4: Check service cards
        console.log('💼 Testing service cards...');
        const serviceCards = await page.locator('.service-card, .services .card, .service-item').count();
        console.log(`Service cards found: ${serviceCards}`);
        
        // Phase 5: Check contact form
        console.log('📝 Testing contact form...');
        const contactForm = await page.locator('form, .wpcf7-form, [role="form"]').count();
        console.log(`Contact forms found: ${contactForm}`);
        
        if (contactForm > 0) {
            const formErrors = await page.locator('.wpcf7-not-valid, .error, .alert-danger').count();
            console.log(`Form errors visible: ${formErrors}`);
        }
        
        // Phase 6: Check testimonials
        console.log('💬 Testing testimonials...');
        const testimonials = await page.locator('.testimonial, .review, .testimonials .item').count();
        console.log(`Testimonials found: ${testimonials}`);
        
        // Phase 7: Mobile responsiveness test
        console.log('📱 Testing mobile view...');
        await page.setViewportSize({ width: 375, height: 667 });
        await page.waitForTimeout(1000);
        
        await page.screenshot({ 
            path: 'mobile-view.png', 
            fullPage: true,
            type: 'png'
        });
        
        // Phase 8: Check for horizontal scrolling on mobile
        const hasHorizontalScroll = await page.evaluate(() => {
            return document.documentElement.scrollWidth > document.documentElement.clientWidth;
        });
        console.log(`Mobile horizontal scrolling detected: ${hasHorizontalScroll}`);
        
        // Phase 9: Generate final report
        console.log('\n📊 FINAL DESIGN REVIEW REPORT');
        console.log('=====================================');
        
        if (consoleMessages.length > 0) {
            console.log('❌ CONSOLE ERRORS/WARNINGS:');
            consoleMessages.forEach(msg => console.log(`  ${msg}`));
        } else {
            console.log('✅ No console errors detected');
        }
        
        console.log(`\n✅ Hero Slider: ${sliderExists ? 'Present' : 'Missing'}`);
        console.log(`✅ Service Cards: ${serviceCards} found`);
        console.log(`✅ Contact Form: ${contactForm > 0 ? 'Present' : 'Missing'}`);
        console.log(`✅ Testimonials: ${testimonials} found`);
        console.log(`✅ Mobile Layout: ${hasHorizontalScroll ? 'Issues detected' : 'No horizontal scroll'}`);
        
    } catch (error) {
        console.error('❌ Error during design review:', error.message);
    } finally {
        await browser.close();
    }
}

conductDesignReview();
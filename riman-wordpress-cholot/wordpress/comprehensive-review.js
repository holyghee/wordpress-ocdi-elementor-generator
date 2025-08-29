const { chromium } = require('playwright');

async function comprehensiveReview() {
    const browser = await chromium.launch({ headless: false });
    const context = await browser.newContext({
        viewport: { width: 1440, height: 900 }
    });
    
    const page = await context.newPage();
    let consoleErrors = [];
    let consoleWarnings = [];
    
    // Capture console messages
    page.on('console', msg => {
        if (msg.type() === 'error') {
            consoleErrors.push(msg.text());
            console.log('❌ Console Error:', msg.text());
        } else if (msg.type() === 'warning') {
            consoleWarnings.push(msg.text());
            console.log('⚠️  Console Warning:', msg.text());
        }
    });
    
    // Capture network failures
    page.on('response', response => {
        if (response.status() >= 400) {
            console.log('🌐 Network Error:', response.url(), 'Status:', response.status());
        }
    });
    
    try {
        console.log('🚀 Starting comprehensive RIMAN website review...\n');
        
        // Navigate to the page
        await page.goto('http://localhost:8081/?page_id=3000', { 
            waitUntil: 'networkidle',
            timeout: 30000 
        });
        
        // Wait for dynamic content
        await page.waitForTimeout(5000);
        
        // 1. CHECK HERO SLIDER
        console.log('🎠 TESTING HERO SLIDER');
        console.log('========================');
        
        const sliderContainer = await page.locator('.slider, .hero-slider, .rdn-slider').first();
        const sliderExists = await sliderContainer.count() > 0;
        console.log(`✅ Slider container found: ${sliderExists}`);
        
        if (sliderExists) {
            // Check if slick is initialized
            const slickInitialized = await page.evaluate(() => {
                const sliders = document.querySelectorAll('.slider, .hero-slider, .slick-slider');
                for (let slider of sliders) {
                    if (slider.classList.contains('slick-initialized') || 
                        slider.querySelector('.slick-dots') || 
                        slider.querySelector('.slick-arrow')) {
                        return true;
                    }
                }
                return false;
            });
            console.log(`✅ Slick functionality active: ${slickInitialized}`);
            
            // Check for slides
            const slides = await page.locator('.slider .slider-img-bg, .slick-slide, .slide').count();
            console.log(`✅ Number of slides: ${slides}`);
            
            // Check for navigation elements
            const hasNavigation = await page.locator('.slick-dots, .slick-arrow, .slider-nav').count() > 0;
            console.log(`✅ Navigation elements: ${hasNavigation ? 'Present' : 'Missing'}`);
        }
        
        // 2. CHECK SERVICE CARDS
        console.log('\n💼 TESTING SERVICE CARDS');
        console.log('==========================');
        
        const serviceCards = await page.locator('.service-card, .service-item, [data-widget_type*="service"]').count();
        console.log(`✅ Service cards found: ${serviceCards}`);
        
        if (serviceCards > 0) {
            const serviceIcons = await page.locator('.service-card i, .service-item i, .fa').count();
            console.log(`✅ Service icons: ${serviceIcons}`);
            
            const serviceText = await page.locator('.service-card h3, .service-item h3').count();
            console.log(`✅ Service headings: ${serviceText}`);
        }
        
        // 3. CHECK CONTACT FORM
        console.log('\n📝 TESTING CONTACT FORM');
        console.log('=========================');
        
        const contactForms = await page.locator('form, .wpcf7-form, [role="form"]').count();
        console.log(`✅ Contact forms found: ${contactForms}`);
        
        if (contactForms > 0) {
            // Check for form fields
            const nameFields = await page.locator('input[name*="name"], input[type="text"]').count();
            const emailFields = await page.locator('input[name*="email"], input[type="email"]').count();
            const messageFields = await page.locator('textarea[name*="message"], textarea').count();
            
            console.log(`✅ Name fields: ${nameFields}`);
            console.log(`✅ Email fields: ${emailFields}`);
            console.log(`✅ Message fields: ${messageFields}`);
            
            // Check for form errors
            const formErrors = await page.locator('.wpcf7-not-valid, .error, .alert-danger, .form-error').count();
            console.log(`✅ Form errors visible: ${formErrors === 0 ? 'None (Good!)' : formErrors}`);
        }
        
        // 4. CHECK TESTIMONIALS
        console.log('\n💬 TESTING TESTIMONIALS');
        console.log('=========================');
        
        const testimonials = await page.locator('.testimonial, .review, [data-widget_type*="testimonial"]').count();
        console.log(`✅ Testimonials found: ${testimonials}`);
        
        if (testimonials > 0) {
            const testimonialText = await page.locator('.testimonial-content, .testimonial-text, .review-text').count();
            const testimonialAuthors = await page.locator('.testimonial-author, .review-author').count();
            
            console.log(`✅ Testimonial content: ${testimonialText}`);
            console.log(`✅ Testimonial authors: ${testimonialAuthors}`);
        }
        
        // 5. RESPONSIVENESS TEST
        console.log('\n📱 TESTING RESPONSIVENESS');
        console.log('===========================');
        
        // Test mobile view
        await page.setViewportSize({ width: 375, height: 667 });
        await page.waitForTimeout(2000);
        
        const hasHorizontalScroll = await page.evaluate(() => {
            return document.documentElement.scrollWidth > document.documentElement.clientWidth;
        });
        console.log(`✅ Mobile horizontal scroll: ${hasHorizontalScroll ? '❌ ISSUE DETECTED' : '✅ Clean'}`);
        
        // Check mobile menu
        const mobileMenuButton = await page.locator('.mobile-menu-toggle, .navbar-toggle, .menu-toggle').count() > 0;
        console.log(`✅ Mobile menu button: ${mobileMenuButton ? 'Present' : 'Missing'}`);
        
        // Test tablet view
        await page.setViewportSize({ width: 768, height: 1024 });
        await page.waitForTimeout(1000);
        
        // Back to desktop
        await page.setViewportSize({ width: 1440, height: 900 });
        await page.waitForTimeout(1000);
        
        // 6. PERFORMANCE CHECK
        console.log('\n⚡ PERFORMANCE CHECK');
        console.log('=====================');
        
        const imageCount = await page.locator('img').count();
        const brokenImages = await page.evaluate(() => {
            const images = Array.from(document.querySelectorAll('img'));
            return images.filter(img => !img.complete || img.naturalHeight === 0).length;
        });
        
        console.log(`✅ Total images: ${imageCount}`);
        console.log(`✅ Broken images: ${brokenImages === 0 ? 'None (Good!)' : brokenImages}`);
        
        // Check CSS and JS loading
        const cssCount = await page.locator('link[rel="stylesheet"]').count();
        const jsCount = await page.locator('script[src]').count();
        
        console.log(`✅ CSS files loaded: ${cssCount}`);
        console.log(`✅ JS files loaded: ${jsCount}`);
        
        // 7. FINAL ASSESSMENT
        console.log('\n📊 FINAL ASSESSMENT');
        console.log('====================');
        
        let score = 0;
        let maxScore = 0;
        const issues = [];
        
        // Hero Slider Assessment
        maxScore += 20;
        if (sliderExists) score += 10;
        if (sliderExists && await page.evaluate(() => document.querySelector('.slider, .hero-slider'))) score += 10;
        else if (!sliderExists) issues.push('Hero slider not found or not working');
        
        // Service Cards Assessment
        maxScore += 15;
        if (serviceCards >= 3) score += 15;
        else if (serviceCards > 0) score += 10;
        else issues.push('Service cards missing or insufficient');
        
        // Contact Form Assessment
        maxScore += 20;
        if (contactForms > 0) score += 20;
        else issues.push('Contact form missing');
        
        // Mobile Responsiveness Assessment
        maxScore += 15;
        if (!hasHorizontalScroll) score += 15;
        else issues.push('Mobile layout has horizontal scrolling');
        
        // Performance Assessment
        maxScore += 15;
        if (brokenImages === 0) score += 10;
        if (consoleErrors.length === 0) score += 5;
        else issues.push(`${consoleErrors.length} JavaScript errors detected`);
        
        // Console Errors Assessment
        maxScore += 15;
        if (consoleErrors.length === 0) score += 15;
        else if (consoleErrors.length <= 2) score += 10;
        else if (consoleErrors.length <= 5) score += 5;
        
        const percentage = Math.round((score / maxScore) * 100);
        
        console.log(`\n🎯 OVERALL SCORE: ${score}/${maxScore} (${percentage}%)`);
        
        if (percentage >= 90) {
            console.log('🎉 SUCCESS: Website is performing excellently!');
        } else if (percentage >= 75) {
            console.log('✅ GOOD: Website is performing well with minor issues');
        } else if (percentage >= 60) {
            console.log('⚠️  ACCEPTABLE: Website has some issues that should be addressed');
        } else {
            console.log('❌ FAILURE: Website has significant issues requiring attention');
        }
        
        if (issues.length > 0) {
            console.log('\n🔧 ISSUES TO ADDRESS:');
            issues.forEach((issue, index) => {
                console.log(`${index + 1}. ${issue}`);
            });
        }
        
        console.log('\n🐛 CONSOLE SUMMARY:');
        console.log(`Errors: ${consoleErrors.length}`);
        console.log(`Warnings: ${consoleWarnings.length}`);
        
        if (consoleErrors.length > 0) {
            console.log('\n❌ Console Errors:');
            consoleErrors.forEach((error, index) => {
                console.log(`${index + 1}. ${error}`);
            });
        }
        
        return {
            score: percentage,
            issues: issues,
            consoleErrors: consoleErrors.length,
            consoleWarnings: consoleWarnings.length
        };
        
    } catch (error) {
        console.error('❌ Test failed:', error.message);
        return { score: 0, issues: ['Test execution failed'], consoleErrors: 999, consoleWarnings: 0 };
    } finally {
        await browser.close();
    }
}

comprehensiveReview().then(result => {
    process.exit(result.score >= 75 ? 0 : 1);
});
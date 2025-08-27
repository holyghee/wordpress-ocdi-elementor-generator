/**
 * RIMAN Modern Theme JavaScript
 */

document.addEventListener('DOMContentLoaded', function() {
    // Smooth scrolling for anchor links
    const smoothScroll = () => {
        const links = document.querySelectorAll('a[href^="#"]');
        
        links.forEach(link => {
            link.addEventListener('click', function(e) {
                e.preventDefault();
                
                const targetId = this.getAttribute('href');
                if (targetId === '#') return;
                
                const targetElement = document.querySelector(targetId);
                
                if (targetElement) {
                    const offset = 80; // Header height
                    const targetPosition = targetElement.getBoundingClientRect().top + window.pageYOffset - offset;
                    
                    window.scrollTo({
                        top: targetPosition,
                        behavior: 'smooth'
                    });
                }
            });
        });
    };
    
    // Header scroll effect
    const headerScroll = () => {
        const header = document.querySelector('.site-header');
        
        window.addEventListener('scroll', () => {
            if (window.scrollY > 100) {
                header.classList.add('scrolled');
            } else {
                header.classList.remove('scrolled');
            }
        });
    };
    
    // Mobile menu toggle
    const mobileMenu = () => {
        const menuButton = document.createElement('button');
        menuButton.className = 'mobile-menu-toggle';
        menuButton.innerHTML = '<span></span><span></span><span></span>';
        menuButton.setAttribute('aria-label', 'Toggle Menu');
        
        const navigation = document.querySelector('.main-navigation');
        const header = document.querySelector('.header-container');
        
        if (window.innerWidth <= 768) {
            if (!document.querySelector('.mobile-menu-toggle')) {
                header.appendChild(menuButton);
            }
            
            menuButton.addEventListener('click', () => {
                navigation.classList.toggle('active');
                menuButton.classList.toggle('active');
            });
        }
    };
    
    // Service cards animation on scroll
    const animateCards = () => {
        const cards = document.querySelectorAll('.service-card');
        
        const observer = new IntersectionObserver((entries) => {
            entries.forEach((entry, index) => {
                if (entry.isIntersecting) {
                    setTimeout(() => {
                        entry.target.classList.add('animated');
                    }, index * 100);
                }
            });
        }, {
            threshold: 0.1
        });
        
        cards.forEach(card => {
            observer.observe(card);
        });
    };
    
    // Initialize all functions
    smoothScroll();
    headerScroll();
    mobileMenu();
    animateCards();
    
    // Handle window resize
    let resizeTimer;
    window.addEventListener('resize', () => {
        clearTimeout(resizeTimer);
        resizeTimer = setTimeout(() => {
            mobileMenu();
        }, 250);
    });
});

// Add CSS class for JS enabled
document.documentElement.classList.add('js');
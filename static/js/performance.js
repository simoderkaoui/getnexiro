/**
 * getNexiro Performance Optimizations
 * - Pause off-screen glow orb animations via IntersectionObserver
 * - Lazy initialize heavy animations only when visible
 */
(function() {
    'use strict';

    // Pause glow orbs when off-screen
    if ('IntersectionObserver' in window) {
        var glowOrbs = document.querySelectorAll('.ambient-glow, .glow-orb-1, .glow-orb-2');
        if (glowOrbs.length > 0) {
            var observer = new IntersectionObserver(function(entries) {
                entries.forEach(function(entry) {
                    if (entry.isIntersecting) {
                        entry.target.style.animationPlayState = 'running';
                    } else {
                        entry.target.style.animationPlayState = 'paused';
                    }
                });
            }, { rootMargin: '100px' });

            glowOrbs.forEach(function(orb) {
                observer.observe(orb);
            });
        }

        // Pause logo carousel animation when off-screen
        var carousels = document.querySelectorAll('.logo-carousel-track, .client-logos-row');
        if (carousels.length > 0) {
            var carouselObserver = new IntersectionObserver(function(entries) {
                entries.forEach(function(entry) {
                    if (entry.isIntersecting) {
                        entry.target.style.animationPlayState = 'running';
                    } else {
                        entry.target.style.animationPlayState = 'paused';
                    }
                });
            }, { rootMargin: '50px' });

            carousels.forEach(function(el) {
                carouselObserver.observe(el);
            });
        }
    }
})();

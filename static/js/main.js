/**
 * ═══════════════════════════════════════════════════
 * getNexiro — Modern B2B Studio JavaScript
 * Handles navigation, interactive filters, counters,
 * and micro-interactions.
 * ═══════════════════════════════════════════════════
 */

document.addEventListener('DOMContentLoaded', () => {

    // ── 1. Mobile Navigation Drawer ────────────────
    const navToggle = document.getElementById('navToggle');
    const navLinks  = document.getElementById('navLinks');

    if (navToggle && navLinks) {
        navToggle.addEventListener('click', (e) => {
            e.stopPropagation();
            const isActive = navLinks.classList.toggle('active');
            navToggle.classList.toggle('active');
            navToggle.setAttribute('aria-expanded', isActive ? 'true' : 'false');
        });

        // Close when clicking nav links
        navLinks.querySelectorAll('.nav-link, .btn').forEach(link => {
            link.addEventListener('click', () => {
                navLinks.classList.remove('active');
                navToggle.classList.remove('active');
                navToggle.setAttribute('aria-expanded', 'false');
            });
        });

        // Close when clicking anywhere outside
        document.addEventListener('click', (e) => {
            if (!navLinks.contains(e.target) && !navToggle.contains(e.target)) {
                navLinks.classList.remove('active');
                navToggle.classList.remove('active');
                navToggle.setAttribute('aria-expanded', 'false');
            }
        });
    }

    // ── 2. Floating Navbar Scroll Blur ────────────
    const navbar = document.getElementById('navbar');
    if (navbar) {
        const updateNavbar = () => {
            if (window.scrollY > 25) {
                navbar.classList.add('scrolled');
            } else {
                navbar.classList.remove('scrolled');
            }
        };
        window.addEventListener('scroll', updateNavbar, { passive: true });
        updateNavbar();
    }

    // ── 3. Interactive Projects Category Filter ────
    const filterButtons = document.querySelectorAll('.filter-btn');
    const projectCards  = document.querySelectorAll('.project-card');

    if (filterButtons.length > 0 && projectCards.length > 0) {
        filterButtons.forEach(btn => {
            btn.addEventListener('click', () => {
                filterButtons.forEach(b => b.classList.remove('active'));
                btn.classList.add('active');

                const filter = btn.dataset.filter;

                projectCards.forEach(card => {
                    const cardCat = card.dataset.category;
                    if (filter === 'all' || cardCat === filter) {
                        card.style.display = '';
                        setTimeout(() => {
                            card.style.opacity = '1';
                            card.style.transform = 'translateY(0)';
                        }, 50);
                    } else {
                        card.style.opacity = '0';
                        card.style.transform = 'translateY(10px)';
                        setTimeout(() => {
                            card.style.display = 'none';
                        }, 250);
                    }
                });
            });
        });
    }

    // ── 4. Stats Counter Animation ────────────────
    const counters = document.querySelectorAll('.counter[data-target]');
    if (counters.length > 0 && 'IntersectionObserver' in window) {
        let hasAnimated = false;

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting && !hasAnimated) {
                    hasAnimated = true;
                    counters.forEach(counter => {
                        const target = parseFloat(counter.getAttribute('data-target'));
                        const isDecimal = target % 1 !== 0;
                        const duration = 1600; // ms
                        const startTime = performance.now();

                        const updateCount = (currentTime) => {
                            const elapsed = currentTime - startTime;
                            const progress = Math.min(elapsed / duration, 1);
                            // Ease out quad
                            const easeProgress = 1 - (1 - progress) * (1 - progress);
                            const currentVal = easeProgress * target;

                            if (isDecimal) {
                                counter.textContent = currentVal.toFixed(2);
                            } else {
                                counter.textContent = Math.floor(currentVal);
                            }

                            if (progress < 1) {
                                requestAnimationFrame(updateCount);
                            } else {
                                counter.textContent = target;
                            }
                        };
                        requestAnimationFrame(updateCount);
                    });
                }
            });
        }, { threshold: 0.3 });

        const statsSection = document.querySelector('.stats-strip');
        if (statsSection) {
            observer.observe(statsSection);
        }
    }

    // ── 5. Smooth Scroll for internal hash links ──
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            const targetId = this.getAttribute('href');
            if (targetId.length > 1) {
                const target = document.querySelector(targetId);
                if (target) {
                    e.preventDefault();
                    target.scrollIntoView({ behavior: 'smooth', block: 'start' });
                }
            }
        });
    });

});

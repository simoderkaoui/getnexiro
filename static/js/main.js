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
        const setMenuState = (isActive) => {
            navLinks.classList.toggle('active', isActive);
            navToggle.classList.toggle('active', isActive);
            navToggle.setAttribute('aria-expanded', isActive ? 'true' : 'false');
            document.body.classList.toggle('menu-open', isActive);
        };

        navToggle.addEventListener('click', (e) => {
            e.stopPropagation();
            const isActive = !navLinks.classList.contains('active');
            setMenuState(isActive);
        });

        // Close when clicking nav links
        navLinks.querySelectorAll('.nav-link, .btn').forEach(link => {
            link.addEventListener('click', () => {
                setMenuState(false);
            });
        });

        // Close when clicking anywhere outside
        document.addEventListener('click', (e) => {
            if (!navLinks.contains(e.target) && !navToggle.contains(e.target)) {
                setMenuState(false);
            }
        });

        // Close on Escape key
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && navLinks.classList.contains('active')) {
                setMenuState(false);
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
    const counters = document.querySelectorAll('.counter[data-target], .counter[data-value]');
    if (counters.length > 0 && 'IntersectionObserver' in window) {
        let hasAnimated = false;

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting && !hasAnimated) {
                    hasAnimated = true;
                    counters.forEach(counter => {
                        const raw = counter.getAttribute('data-value') || counter.getAttribute('data-target') || counter.textContent;
                        // Extract numbers and suffix
                        const match = raw.match(/([\d\.]+)(.*)/);
                        if (!match) return;

                        const target = parseFloat(match[1]);
                        const suffix = match[2] || '';
                        const isDecimal = match[1].includes('.');
                        const duration = 1600; // ms
                        const startTime = performance.now();

                        const updateCount = (currentTime) => {
                            const elapsed = currentTime - startTime;
                            const progress = Math.min(elapsed / duration, 1);
                            const easeProgress = 1 - (1 - progress) * (1 - progress);
                            const currentVal = easeProgress * target;

                            if (isDecimal) {
                                counter.textContent = currentVal.toFixed(1) + suffix;
                            } else {
                                counter.textContent = Math.floor(currentVal) + suffix;
                            }

                            if (progress < 1) {
                                requestAnimationFrame(updateCount);
                            } else {
                                counter.textContent = raw;
                            }
                        };
                        requestAnimationFrame(updateCount);
                    });
                }
            });
        }, { threshold: 0.25 });

        const statsSection = document.querySelector('.stats-strip');
        if (statsSection) {
            observer.observe(statsSection);
        }
    }

    // ── 5. Smooth Scroll for internal hash links ──
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            const targetId = this.getAttribute('href');
            if (targetId && targetId.length > 1) {
                const target = document.querySelector(targetId);
                if (target) {
                    e.preventDefault();
                    target.scrollIntoView({ behavior: 'smooth', block: 'start' });
                }
            }
        });
    });

    // ── 6. Scroll Reveal Animations ──────────────
    const revealElements = document.querySelectorAll('.reveal, .reveal-stagger');
    if (revealElements.length > 0 && 'IntersectionObserver' in window) {
        const revealObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('revealed');
                    revealObserver.unobserve(entry.target);
                }
            });
        }, { threshold: 0.1, rootMargin: '0px 0px -50px 0px' });

        revealElements.forEach(el => revealObserver.observe(el));
    }

    // ── 7. Back to Top Button ────────────────────
    const backToTop = document.getElementById('backToTop');
    if (backToTop) {
        const toggleBackToTop = () => {
            if (window.scrollY > 600) {
                backToTop.classList.add('visible');
            } else {
                backToTop.classList.remove('visible');
            }
        };
        window.addEventListener('scroll', toggleBackToTop, { passive: true });
        backToTop.addEventListener('click', () => {
            window.scrollTo({ top: 0, behavior: 'smooth' });
        });
    }

    // ── 8. Spotlight Command Palette (Ctrl+K / ⌘K) ──
    const spotlightModal = document.getElementById('spotlightModal');
    const spotlightTrigger = document.getElementById('spotlightTrigger');
    const mobileSpotlightTrigger = document.getElementById('mobileSpotlightTrigger');
    const spotlightCloseBtn = document.getElementById('spotlightCloseBtn');
    const spotlightBackdrop = document.getElementById('spotlightBackdrop');
    const spotlightInput = document.getElementById('spotlightInput');
    const spotlightItems = document.querySelectorAll('.spotlight-item');
    const spotlightGroups = document.querySelectorAll('.spotlight-group');

    if (spotlightModal && spotlightInput) {
        let focusedIndex = -1;

        const getVisibleItems = () => {
            return Array.from(spotlightItems).filter(item => item.style.display !== 'none');
        };

        const updateFocus = (items) => {
            items.forEach((item, idx) => {
                item.classList.toggle('focused', idx === focusedIndex);
            });
            if (focusedIndex >= 0 && items[focusedIndex]) {
                items[focusedIndex].scrollIntoView({ block: 'nearest', behavior: 'smooth' });
            }
        };

        const openSpotlight = () => {
            spotlightModal.classList.add('active');
            spotlightModal.setAttribute('aria-hidden', 'false');
            document.body.style.overflow = 'hidden';
            setTimeout(() => {
                spotlightInput.focus();
                spotlightInput.select();
            }, 50);
            focusedIndex = -1;
            updateFocus(getVisibleItems());
        };

        const closeSpotlight = () => {
            spotlightModal.classList.remove('active');
            spotlightModal.setAttribute('aria-hidden', 'true');
            document.body.style.overflow = '';
            spotlightInput.value = '';
            // Restore visibility of all items & groups
            spotlightItems.forEach(item => item.style.display = '');
            spotlightGroups.forEach(grp => grp.style.display = '');
        };

        if (spotlightTrigger) spotlightTrigger.addEventListener('click', openSpotlight);
        if (mobileSpotlightTrigger) mobileSpotlightTrigger.addEventListener('click', openSpotlight);
        if (spotlightCloseBtn) spotlightCloseBtn.addEventListener('click', closeSpotlight);
        if (spotlightBackdrop) spotlightBackdrop.addEventListener('click', closeSpotlight);

        // Global Keyboard Shortcut: Ctrl+K / ⌘K / "/"
        document.addEventListener('keydown', (e) => {
            const isTyping = ['INPUT', 'TEXTAREA'].includes(document.activeElement?.tagName);

            if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === 'k') {
                e.preventDefault();
                if (spotlightModal.classList.contains('active')) {
                    closeSpotlight();
                } else {
                    openSpotlight();
                }
            } else if (e.key === '/' && !isTyping && !spotlightModal.classList.contains('active')) {
                e.preventDefault();
                openSpotlight();
            } else if (e.key === 'Escape' && spotlightModal.classList.contains('active')) {
                e.preventDefault();
                closeSpotlight();
            }
        });

        // Real-Time Search Filter
        spotlightInput.addEventListener('input', () => {
            const query = spotlightInput.value.trim().toLowerCase();
            focusedIndex = -1;

            if (!query) {
                spotlightItems.forEach(item => item.style.display = '');
                spotlightGroups.forEach(grp => grp.style.display = '');
                return;
            }

            spotlightGroups.forEach(group => {
                let groupHasVisible = false;
                const itemsInGroup = group.querySelectorAll('.spotlight-item');

                itemsInGroup.forEach(item => {
                    const text = (item.textContent + ' ' + (item.dataset.keywords || '')).toLowerCase();
                    const matches = text.includes(query);
                    item.style.display = matches ? '' : 'none';
                    if (matches) groupHasVisible = true;
                });

                group.style.display = groupHasVisible ? '' : 'none';
            });

            const visibleItems = getVisibleItems();
            if (visibleItems.length > 0) {
                focusedIndex = 0;
                updateFocus(visibleItems);
            }
        });

        // Arrow Key & Enter Navigation
        spotlightInput.addEventListener('keydown', (e) => {
            const visibleItems = getVisibleItems();
            if (visibleItems.length === 0) return;

            if (e.key === 'ArrowDown') {
                e.preventDefault();
                focusedIndex = (focusedIndex + 1) % visibleItems.length;
                updateFocus(visibleItems);
            } else if (e.key === 'ArrowUp') {
                e.preventDefault();
                focusedIndex = (focusedIndex - 1 + visibleItems.length) % visibleItems.length;
                updateFocus(visibleItems);
            } else if (e.key === 'Enter') {
                e.preventDefault();
                if (focusedIndex >= 0 && visibleItems[focusedIndex]) {
                    visibleItems[focusedIndex].click();
                } else if (visibleItems.length > 0) {
                    visibleItems[0].click();
                }
            }
        });
    }

    // ── 9. Hero Console Interactive Tabs ──────────
    const consoleTabButtons = document.querySelectorAll('.console-tab-btn[data-console-tab]');
    const paneArchitecture = document.getElementById('consolePaneArchitecture');
    const paneTelemetry = document.getElementById('consolePaneTelemetry');
    const paneRadar = document.getElementById('consolePaneRadar');

    if (consoleTabButtons.length > 0) {
        const panes = {
            architecture: paneArchitecture,
            telemetry: paneTelemetry,
            radar: paneRadar
        };

        consoleTabButtons.forEach(btn => {
            btn.addEventListener('click', () => {
                const tabKey = btn.dataset.consoleTab;

                consoleTabButtons.forEach(b => {
                    b.classList.remove('active');
                    b.setAttribute('aria-selected', 'false');
                });
                btn.classList.add('active');
                btn.setAttribute('aria-selected', 'true');

                Object.keys(panes).forEach(key => {
                    if (panes[key]) {
                        panes[key].classList.toggle('active', key === tabKey);
                    }
                });
            });
        });
    }

    // ── 10. Interactive Project Estimator Teaser ──
    const estTabBtns = document.querySelectorAll('.estimator-tab-btn[data-type]');
    const estDelivery = document.getElementById('estDelivery');
    const estSprints = document.getElementById('estSprints');
    const estOwnership = document.getElementById('estOwnership');
    const estWarranty = document.getElementById('estWarranty');
    const estBlueprint = document.getElementById('estBlueprint');
    const estCta = document.getElementById('estCta');

    if (estTabBtns.length > 0 && estDelivery) {
        const estData = {
            web: {
                delivery: '4 – 8 Weeks',
                sprints: '2 – 4 Agile Sprints',
                ownership: '100% Full IP Transfer',
                warranty: '30 Days Included',
                blueprint: 'Custom Django 5.1 engine + PostgreSQL database, responsive component system, multilingual routing (EN/FR/AR), and Dockerized automated CI/CD pipeline.',
                ctaParam: 'web'
            },
            mobile: {
                delivery: '6 – 10 Weeks',
                sprints: '3 – 5 Agile Sprints',
                ownership: '100% Full IP Transfer',
                warranty: '60 Days Included',
                blueprint: 'Cross-platform Flutter mobile app (iOS & Android) with unified codebase, offline-first SQLite sync, push notifications, and App Store / Google Play deployment.',
                ctaParam: 'mobile'
            },
            backend: {
                delivery: '3 – 6 Weeks',
                sprints: '2 – 3 Agile Sprints',
                ownership: '100% Full IP Transfer',
                warranty: '30 Days Included',
                blueprint: 'High-throughput RESTful & GraphQL microservices with JWT/OAuth2 authentication, PostgreSQL schema design, Redis caching layer, and automated API documentation.',
                ctaParam: 'backend'
            },
            design: {
                delivery: '2 – 4 Weeks',
                sprints: '1 – 2 Design Sprints',
                ownership: '100% Figma & Tokens',
                warranty: 'Styleguide Handoff',
                blueprint: 'Complete B2B UX audit, clickable high-fidelity Figma prototypes, comprehensive design tokens (dark/light, typography, spacing), and accessible component library.',
                ctaParam: 'design'
            }
        };

        estTabBtns.forEach(btn => {
            btn.addEventListener('click', () => {
                const type = btn.dataset.type;
                if (!estData[type]) return;

                estTabBtns.forEach(b => {
                    b.classList.remove('active');
                    b.setAttribute('aria-selected', 'false');
                });
                btn.classList.add('active');
                btn.setAttribute('aria-selected', 'true');

                const data = estData[type];
                estDelivery.textContent = data.delivery;
                estSprints.textContent = data.sprints;
                estOwnership.textContent = data.ownership;
                estWarranty.textContent = data.warranty;
                estBlueprint.textContent = data.blueprint;
                if (estCta) {
                    const currentHref = estCta.getAttribute('href').split('?')[0];
                    estCta.setAttribute('href', `${currentHref}?type=${data.ctaParam}`);
                }
            });
        });
    }

    // ── 11. Dynamic Mouse Spotlight Radial Highlight ──
    const spotlightCards = document.querySelectorAll(
        '.glass-card, .service-preview-card, .project-preview-card, .bento-card, .estimator-teaser-card, .hub-card'
    );
    const isFinePointer = window.matchMedia('(hover: hover) and (pointer: fine)').matches;

    spotlightCards.forEach(card => {
        card.addEventListener('mousemove', (e) => {
            const rect = card.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            card.style.setProperty('--mouse-x', `${x}px`);
            card.style.setProperty('--mouse-y', `${y}px`);

            if (isFinePointer && !card.classList.contains('no-tilt') && card.classList.contains('bento-card')) {
                const centerX = rect.width / 2;
                const centerY = rect.height / 2;
                const rotateX = ((y - centerY) / centerY) * -2.5;
                const rotateY = ((x - centerX) / centerX) * 2.5;
                card.style.transform = `perspective(1000px) rotateX(${rotateX.toFixed(2)}deg) rotateY(${rotateY.toFixed(2)}deg) translateY(-2px)`;
            }
        });

        card.addEventListener('mouseleave', () => {
            card.style.removeProperty('--mouse-x');
            card.style.removeProperty('--mouse-y');
            if (isFinePointer && card.classList.contains('bento-card')) {
                card.style.transform = '';
            }
        });
    });
});

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

    // ── 8. Upgraded Spotlight Command Palette (Ctrl+K / ⌘K) ──
    const spotlightModal = document.getElementById('spotlightModal');
    const spotlightTrigger = document.getElementById('spotlightTrigger');
    const mobileSpotlightTrigger = document.getElementById('mobileSpotlightTrigger');
    const spotlightCloseBtn = document.getElementById('spotlightCloseBtn');
    const spotlightBackdrop = document.getElementById('spotlightBackdrop');
    const spotlightInput = document.getElementById('spotlightInput');
    const spotlightResults = document.getElementById('spotlightResults');
    const spotlightDefaultResults = document.getElementById('spotlightDefaultResults');
    const spotlightDynamicResults = document.getElementById('spotlightDynamicResults');

    if (spotlightModal && spotlightInput) {
        let focusedIndex = -1;
        let searchDebounceTimer = null;
        let activeAbortController = null;
        const searchApiUrl = spotlightResults?.dataset?.searchUrl || '/en/search/';

        // Escape HTML to prevent XSS
        const escapeHtml = (str) => {
            if (!str) return '';
            return String(str).replace(/[&<>"']/g, (m) => ({
                '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#039;'
            }[m]));
        };

        // Safe substring highlight
        const highlightMatch = (text, query) => {
            if (!text || !query) return escapeHtml(text);
            const escapedText = escapeHtml(text);
            const escapedQuery = query.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
            const regex = new RegExp(`(${escapedQuery})`, 'gi');
            return escapedText.replace(regex, '<mark class="spotlight-match">$1</mark>');
        };

        const getVisibleItems = () => {
            return Array.from(spotlightModal.querySelectorAll('.spotlight-item')).filter(item => {
                return item.offsetParent !== null && item.style.display !== 'none';
            });
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
            if (activeAbortController) {
                activeAbortController.abort();
            }
            if (spotlightDynamicResults) {
                spotlightDynamicResults.style.display = 'none';
                spotlightDynamicResults.innerHTML = '';
            }
            if (spotlightDefaultResults) {
                spotlightDefaultResults.style.display = '';
                const defaultItems = spotlightDefaultResults.querySelectorAll('.spotlight-item');
                const defaultGroups = spotlightDefaultResults.querySelectorAll('.spotlight-group');
                defaultItems.forEach(item => item.style.display = '');
                defaultGroups.forEach(grp => grp.style.display = '');
            }
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

        // Live Asynchronous Search with 200ms debounce
        spotlightInput.addEventListener('input', () => {
            const query = spotlightInput.value.trim();
            focusedIndex = -1;
            clearTimeout(searchDebounceTimer);

            if (query.length < 2) {
                if (activeAbortController) activeAbortController.abort();
                if (spotlightDynamicResults) {
                    spotlightDynamicResults.style.display = 'none';
                    spotlightDynamicResults.innerHTML = '';
                }
                if (spotlightDefaultResults) {
                    spotlightDefaultResults.style.display = '';
                    const defaultItems = spotlightDefaultResults.querySelectorAll('.spotlight-item');
                    const defaultGroups = spotlightDefaultResults.querySelectorAll('.spotlight-group');
                    defaultItems.forEach(item => item.style.display = '');
                    defaultGroups.forEach(grp => grp.style.display = '');
                }
                const visible = getVisibleItems();
                if (visible.length > 0) {
                    focusedIndex = 0;
                    updateFocus(visible);
                }
                return;
            }

            searchDebounceTimer = setTimeout(() => {
                if (activeAbortController) activeAbortController.abort();
                activeAbortController = new AbortController();

                const currentLang = document.documentElement.lang || 'en';
                const i18n = {
                    loading: currentLang === 'ar' ? 'جاري البحث في الخدمات، المشاريع، المدونة والمراكز...' :
                             (currentLang === 'fr' ? 'Recherche dans les services, projets, blog et hubs...' :
                             'Searching across services, projects, blog & hubs...'),
                    noMatch: currentLang === 'ar' ? `لا توجد نتائج مطابقة لـ "${escapeHtml(query)}"` :
                             (currentLang === 'fr' ? `Aucun résultat direct pour « ${escapeHtml(query)} »` :
                             `No direct matches for "${escapeHtml(query)}"`),
                    noMatchSub: currentLang === 'ar' ? 'تبحث عن هندسة نظام مخصص لمشروعك؟ مهندسو جيت نكسيرو بطنجة في خدمتك.' :
                                (currentLang === 'fr' ? 'Vous souhaitez développer un système sur mesure ? Nos architectes logiciels à Tanger sont à votre écoute.' :
                                'Looking to engineer a custom system? Our Tangier software architects can help.'),
                    ctaText: currentLang === 'ar' ? 'احسب تكلفة مشروعك فوراً ←' :
                             (currentLang === 'fr' ? 'Calculer un devis instantané →' :
                             'Calculate Instant Project Quote →'),
                    searchError: currentLang === 'ar' ? 'خدمة البحث غير متاحة مؤقتاً.' :
                                 (currentLang === 'fr' ? 'La recherche est temporairement indisponible.' :
                                 'Search is temporarily unavailable.')
                };

                if (spotlightDefaultResults) spotlightDefaultResults.style.display = 'none';
                if (spotlightDynamicResults) {
                    spotlightDynamicResults.style.display = 'block';
                    spotlightDynamicResults.innerHTML = `<div class="spotlight-loading-spinner"><span>⚡</span> <span>${i18n.loading}</span></div>`;
                }

                fetch(`${searchApiUrl}?q=${encodeURIComponent(query)}`, {
                    signal: activeAbortController.signal,
                    headers: { 'X-Requested-With': 'XMLHttpRequest' }
                })
                .then(res => res.json())
                .then(data => {
                    if (!spotlightDynamicResults) return;

                    if (!data.groups || data.groups.length === 0 || data.total === 0) {
                        const quoteUrl = `/${currentLang}/quote/`;
                        spotlightDynamicResults.innerHTML = `
                            <div class="spotlight-empty-state">
                                <span class="spotlight-empty-icon">🔍</span>
                                <p class="spotlight-empty-title">${i18n.noMatch}</p>
                                <p class="spotlight-empty-sub">${i18n.noMatchSub}</p>
                                <a href="${quoteUrl}" class="btn btn-primary btn-sm spotlight-empty-cta spotlight-item">
                                    <span>${i18n.ctaText}</span>
                                </a>
                            </div>
                        `;
                    } else {
                        let html = '';
                        data.groups.forEach(group => {
                            html += `
                                <div class="spotlight-group" data-group="${escapeHtml(group.type)}">
                                    <div class="spotlight-group-title">${escapeHtml(group.title)}</div>
                            `;
                            group.items.forEach(item => {
                                const highlightedTitle = highlightMatch(item.title, query);
                                const highlightedDesc = highlightMatch(item.desc, query);
                                html += `
                                    <a href="${escapeHtml(item.url)}" class="spotlight-item">
                                        <span class="spotlight-item-icon">${escapeHtml(item.icon || '📄')}</span>
                                        <div class="spotlight-item-text">
                                            <span class="spotlight-item-title">${highlightedTitle}</span>
                                            <span class="spotlight-item-desc">${highlightedDesc}</span>
                                        </div>
                                        <span class="spotlight-item-badge">${escapeHtml(item.badge || '')}</span>
                                    </a>
                                `;
                            });
                            html += `</div>`;
                        });
                        spotlightDynamicResults.innerHTML = html;
                    }

                    const visible = getVisibleItems();
                    if (visible.length > 0) {
                        focusedIndex = 0;
                        updateFocus(visible);
                    }
                })
                .catch(err => {
                    if (err.name === 'AbortError') return;
                    if (spotlightDynamicResults) {
                        spotlightDynamicResults.innerHTML = `
                            <div class="spotlight-empty-state">
                                <p class="spotlight-empty-title">${i18n.searchError}</p>
                            </div>
                        `;
                    }
                });
            }, 200);
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

                const data = estData[type] || {};
                estDelivery.textContent = btn.dataset.delivery || data.delivery || '';
                estSprints.textContent = btn.dataset.sprints || data.sprints || '';
                estOwnership.textContent = btn.dataset.ownership || data.ownership || '';
                estWarranty.textContent = btn.dataset.warranty || data.warranty || '';
                estBlueprint.textContent = btn.dataset.blueprint || data.blueprint || '';
                if (estCta) {
                    const ctaParam = btn.dataset.cta || data.ctaParam || type;
                    const currentHref = estCta.getAttribute('href').split('?')[0];
                    estCta.setAttribute('href', `${currentHref}?type=${ctaParam}`);
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

    // ── 12. Feature 2: Sticky Mini-CTA Bar ──────────
    const stickyMiniCta = document.getElementById('stickyMiniCta');
    const stickyCtaClose = document.getElementById('stickyCtaClose');

    if (stickyMiniCta) {
        let ctaTicking = false;
        const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

        const checkCtaScroll = () => {
            if (sessionStorage.getItem('nexiro_sticky_cta_dismissed') === '1') {
                return;
            }
            const docHeight = document.documentElement.scrollHeight - window.innerHeight;
            if (docHeight <= 350) return;

            const scrollPercent = (window.scrollY / docHeight) * 100;
            if (scrollPercent >= 40) {
                if (!stickyMiniCta.classList.contains('active')) {
                    stickyMiniCta.classList.add('active');
                    stickyMiniCta.setAttribute('aria-hidden', 'false');
                    document.body.classList.add('sticky-cta-active');
                }
            } else if (scrollPercent < 15) {
                if (stickyMiniCta.classList.contains('active')) {
                    stickyMiniCta.classList.remove('active');
                    stickyMiniCta.setAttribute('aria-hidden', 'true');
                    document.body.classList.remove('sticky-cta-active');
                }
            }
        };

        window.addEventListener('scroll', () => {
            if (!ctaTicking) {
                window.requestAnimationFrame(() => {
                    checkCtaScroll();
                    ctaTicking = false;
                });
                ctaTicking = true;
            }
        }, { passive: true });

        // Initial check in case of mid-page reload
        setTimeout(checkCtaScroll, 100);

        if (stickyCtaClose) {
            stickyCtaClose.addEventListener('click', () => {
                stickyMiniCta.classList.remove('active');
                stickyMiniCta.setAttribute('aria-hidden', 'true');
                document.body.classList.remove('sticky-cta-active');
                try {
                    sessionStorage.setItem('nexiro_sticky_cta_dismissed', '1');
                } catch (e) {}
            });
        }
    }

    // ── 13. Feature 3: Newsletter 'Morocco Web Tips' AJAX ──
    const newsletterForms = document.querySelectorAll('.newsletter-form-ajax');
    newsletterForms.forEach(form => {
        form.addEventListener('submit', (e) => {
            e.preventDefault();
            const emailInput = form.querySelector('input[name="email"]');
            const submitBtn = form.querySelector('.newsletter-submit-btn');
            const feedback = form.querySelector('.newsletter-feedback');
            const btnText = submitBtn?.querySelector('.btn-text');
            const btnSpinner = submitBtn?.querySelector('.btn-spinner');

            if (!emailInput || !emailInput.value.trim()) return;

            const originalBtnText = btnText ? btnText.textContent : '';
            if (btnText && btnSpinner) {
                btnText.style.display = 'none';
                btnSpinner.style.display = 'inline-block';
            }
            if (submitBtn) submitBtn.disabled = true;
            if (feedback) {
                feedback.className = 'newsletter-feedback';
                feedback.textContent = '';
            }

            const formData = new FormData(form);
            const csrfToken = form.querySelector('input[name="csrfmiddlewaretoken"]')?.value || '';

            fetch(form.action, {
                method: 'POST',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': csrfToken
                },
                body: formData
            })
            .then(res => res.json().then(data => ({ status: res.status, data })))
            .then(({ status, data }) => {
                if (feedback) {
                    feedback.textContent = data.message || 'Subscription processed.';
                    if (data.status === 'success') {
                        feedback.classList.add('success');
                        form.reset();
                    } else if (data.status === 'info') {
                        feedback.classList.add('info');
                    } else {
                        feedback.classList.add('error');
                    }
                }
            })
            .catch(() => {
                if (feedback) {
                    feedback.className = 'newsletter-feedback error';
                    const currentLang = document.documentElement.lang || 'en';
                    feedback.textContent = currentLang === 'ar' ? 'خطأ في الاتصال بالشبكة. يرجى المحاولة مرة أخرى.' :
                                          (currentLang === 'fr' ? 'Erreur de connexion. Veuillez réessayer.' :
                                          'Network error. Please try again.');
                }
            })
            .finally(() => {
                if (btnText && btnSpinner) {
                    btnText.style.display = '';
                    btnSpinner.style.display = 'none';
                }
                if (submitBtn) submitBtn.disabled = false;
            });
        });
    });

    // ── 14. Feature 4: Animated Process Timeline ────
    const processSection = document.getElementById('ourProcessTimeline');
    const stepNodes = document.querySelectorAll('.process-step-node');
    const trackFill = document.getElementById('timelineProgressFill');

    if (processSection && stepNodes.length > 0) {
        const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

        if (prefersReducedMotion) {
            stepNodes.forEach(node => node.classList.add('is-visible'));
            if (trackFill) {
                trackFill.style.width = '100%';
                trackFill.style.height = '100%';
            }
        } else if ('IntersectionObserver' in window) {
            let maxActiveStep = 0;
            const isHorizontal = window.innerWidth > 960;

            const observer = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        const stepNum = parseInt(entry.target.dataset.step, 10) || 1;
                        entry.target.classList.add('is-visible');
                        if (stepNum > maxActiveStep) {
                            maxActiveStep = stepNum;
                            const progressPercent = Math.min(100, Math.round(((maxActiveStep - 1) / (stepNodes.length - 1)) * 100));
                            if (trackFill) {
                                if (window.innerWidth > 960) {
                                    trackFill.style.width = `${progressPercent}%`;
                                } else {
                                    trackFill.style.height = `${progressPercent}%`;
                                }
                            }
                        }
                    }
                });
            }, {
                threshold: 0.25,
                rootMargin: '0px 0px -10% 0px'
            });

            stepNodes.forEach(node => observer.observe(node));
        } else {
            stepNodes.forEach(node => node.classList.add('is-visible'));
        }
    }

    // ── 15. Feature 5: Client Dashboard Demo ────────
    const demoTabBtns = document.querySelectorAll('.demo-tab-btn[data-tab]');
    const demoPanes = document.querySelectorAll('.demo-tab-pane');
    const filterBtns = document.querySelectorAll('.ticket-filter-bar .btn-filter');
    const ticketCards = document.querySelectorAll('.ticket-item-card[data-ticket-status]');

    if (demoTabBtns.length > 0) {
        demoTabBtns.forEach(btn => {
            btn.addEventListener('click', () => {
                const targetTab = btn.dataset.tab;

                demoTabBtns.forEach(b => {
                    b.classList.remove('active');
                    b.setAttribute('aria-selected', 'false');
                });
                btn.classList.add('active');
                btn.setAttribute('aria-selected', 'true');

                demoPanes.forEach(pane => {
                    pane.classList.remove('active');
                });

                const targetPane = document.getElementById(`demoPane${targetTab.charAt(0).toUpperCase() + targetTab.slice(1)}`);
                if (targetPane) {
                    targetPane.classList.add('active');
                }
            });
        });
    }

    if (filterBtns.length > 0 && ticketCards.length > 0) {
        filterBtns.forEach(btn => {
            btn.addEventListener('click', () => {
                const filter = btn.dataset.filter;

                filterBtns.forEach(b => b.classList.remove('active'));
                btn.classList.add('active');

                ticketCards.forEach(card => {
                    const status = card.dataset.ticketStatus;
                    if (filter === 'all' || status === filter) {
                        card.style.display = '';
                    } else {
                        card.style.display = 'none';
                    }
                });
            });
        });
    }
});

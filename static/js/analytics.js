/**
 * getNexiro Analytics Event Tracking Helper
 *
 * Usage: trackEvent('event_name', { key: 'value' })
 *
 * Safely does nothing when:
 * - Cookie consent has not been given
 * - No analytics provider is configured
 * - Analytics script has not loaded yet
 */
(function(window) {
    'use strict';

    window.trackEvent = function(eventName, params) {
        // Check cookie consent
        if (localStorage.getItem('cookie_consent') !== 'accepted') {
            return;
        }

        params = params || {};

        // GA4 (gtag)
        if (typeof window.gtag === 'function') {
            window.gtag('event', eventName, params);
            return;
        }

        // Plausible
        if (typeof window.plausible === 'function') {
            window.plausible(eventName, { props: params });
            return;
        }

        // Analytics not loaded yet — no-op
    };
})(window);

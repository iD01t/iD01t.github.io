// Performance monitoring and optimization script
(function() {
  'use strict';

  // Performance metrics collection
  const performanceData = {
    loadTime: 0,
    domContentLoaded: 0,
    firstPaint: 0,
    firstContentfulPaint: 0,
    largestContentfulPaint: 0,
    cumulativeLayoutShift: 0,
    firstInputDelay: 0
  };

  // Collect Core Web Vitals
  function collectWebVitals() {
    // Largest Contentful Paint
    if ('PerformanceObserver' in window) {
      const lcpObserver = new PerformanceObserver((list) => {
        const entries = list.getEntries();
        const lastEntry = entries[entries.length - 1];
        performanceData.largestContentfulPaint = lastEntry.startTime;
      });
      lcpObserver.observe({ entryTypes: ['largest-contentful-paint'] });

      // Cumulative Layout Shift
      const clsObserver = new PerformanceObserver((list) => {
        for (const entry of list.getEntries()) {
          if (!entry.hadRecentInput) {
            performanceData.cumulativeLayoutShift += entry.value;
          }
        }
      });
      clsObserver.observe({ entryTypes: ['layout-shift'] });

      // First Input Delay
      const fidObserver = new PerformanceObserver((list) => {
        for (const entry of list.getEntries()) {
          performanceData.firstInputDelay = entry.processingStart - entry.startTime;
        }
      });
      fidObserver.observe({ entryTypes: ['first-input'] });
    }
  }

  // Collect basic performance metrics
  function collectBasicMetrics() {
    window.addEventListener('load', () => {
      const navigation = performance.getEntriesByType('navigation')[0];
      if (navigation) {
        performanceData.loadTime = navigation.loadEventEnd - navigation.loadEventStart;
        performanceData.domContentLoaded = navigation.domContentLoadedEventEnd - navigation.domContentLoadedEventStart;
      }

      // First Paint
      const paintEntries = performance.getEntriesByType('paint');
      paintEntries.forEach(entry => {
        if (entry.name === 'first-paint') {
          performanceData.firstPaint = entry.startTime;
        } else if (entry.name === 'first-contentful-paint') {
          performanceData.firstContentfulPaint = entry.startTime;
        }
      });

      // Send to analytics if available
      if (typeof gtag !== 'undefined') {
        gtag('event', 'performance_metrics', {
          'custom_parameter_1': performanceData.loadTime,
          'custom_parameter_2': performanceData.firstContentfulPaint,
          'custom_parameter_3': performanceData.largestContentfulPaint,
          'custom_parameter_4': performanceData.cumulativeLayoutShift,
          'custom_parameter_5': performanceData.firstInputDelay
        });
      }

      // Log performance issues
      if (performanceData.loadTime > 3000) {
        console.warn('Slow page load detected:', performanceData.loadTime + 'ms');
      }
      if (performanceData.firstContentfulPaint > 1500) {
        console.warn('Slow first contentful paint:', performanceData.firstContentfulPaint + 'ms');
      }
      if (performanceData.cumulativeLayoutShift > 0.1) {
        console.warn('High cumulative layout shift:', performanceData.cumulativeLayoutShift);
      }
    });
  }

  // Image optimization
  function optimizeImages() {
    const images = document.querySelectorAll('img');
    images.forEach(img => {
      // Add loading="lazy" if not present
      if (!img.hasAttribute('loading')) {
        img.setAttribute('loading', 'lazy');
      }
      
      // Add decoding="async" if not present
      if (!img.hasAttribute('decoding')) {
        img.setAttribute('decoding', 'async');
      }

      // Add error handling
      img.addEventListener('error', function() {
        this.src = '/assets/placeholder-cover.svg';
        this.alt = 'Image not available';
      });
    });
  }

  // Preload critical resources
  function preloadCriticalResources() {
    const criticalResources = [
      '/assets/site.css',
      '/assets/site.js'
    ];

    criticalResources.forEach(resource => {
      const link = document.createElement('link');
      link.rel = 'preload';
      link.href = resource;
      link.as = resource.endsWith('.css') ? 'style' : 'script';
      document.head.appendChild(link);
    });
  }

  // Optimize third-party scripts
  function optimizeThirdPartyScripts() {
    // Defer non-critical scripts
    const scripts = document.querySelectorAll('script[src]');
    scripts.forEach(script => {
      if (script.src.includes('googletagmanager.com') || 
          script.src.includes('google-analytics.com')) {
        script.async = true;
        script.defer = true;
      }
    });
  }

  // Monitor resource loading
  function monitorResourceLoading() {
    if ('PerformanceObserver' in window) {
      const resourceObserver = new PerformanceObserver((list) => {
        list.getEntries().forEach(entry => {
          if (entry.duration > 1000) {
            console.warn('Slow resource loading:', entry.name, entry.duration + 'ms');
          }
        });
      });
      resourceObserver.observe({ entryTypes: ['resource'] });
    }
  }

  // Initialize performance monitoring
  function init() {
    collectWebVitals();
    collectBasicMetrics();
    optimizeImages();
    preloadCriticalResources();
    optimizeThirdPartyScripts();
    monitorResourceLoading();
  }

  // Run when DOM is ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

  // Expose performance data globally for debugging
  window.performanceData = performanceData;

})();

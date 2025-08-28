// iD01t Productions - Shared JavaScript Utilities
// No build step required - vanilla JS for GitHub Pages

// Theme management
export function toggleTheme() {
  const root = document.documentElement;
  const dark = root.classList.toggle('dark');
  localStorage.setItem('theme', dark ? 'dark' : 'light');
  
  // Update button text
  const themeBtn = document.getElementById('themeToggle');
  if (themeBtn) {
    themeBtn.textContent = dark ? 'Light' : 'Dark';
  }
}

// Mobile menu management
export function toggleMobileMenu() {
  const mobileMenu = document.getElementById('mobileMenu');
  const mobileBtn = document.getElementById('mobileMenuBtn');
  
  if (mobileMenu && mobileBtn) {
    const isHidden = mobileMenu.classList.contains('hidden');
    mobileMenu.classList.toggle('hidden');
    
    // Update button aria-expanded
    mobileBtn.setAttribute('aria-expanded', !isHidden);
    
    // Update button icon
    const icon = mobileBtn.querySelector('svg');
    if (icon) {
      if (isHidden) {
        icon.innerHTML = '<path d="M6 18L18 6M6 6l12 12"/>'; // X icon
      } else {
        icon.innerHTML = '<path d="M3 6h18M3 12h18M3 18h18"/>'; // Menu icon
      }
    }
  }
}

// Active navigation highlighting
export function initActiveNav() {
  const currentPath = window.location.pathname;
  const navLinks = document.querySelectorAll('nav a[href]');
  
  navLinks.forEach(link => {
    const href = link.getAttribute('href');
    if (href === currentPath || (currentPath === '/' && href === '/index.html')) {
      link.setAttribute('aria-current', 'page');
      link.classList.add('text-brand-600', 'dark:text-brand-400');
    } else {
      link.removeAttribute('aria-current');
      link.classList.remove('text-brand-600', 'dark:text-brand-400');
    }
  });
}

// Accordion functionality
export function initAccordions() {
  const accordionButtons = document.querySelectorAll('[data-accordion]');
  
  accordionButtons.forEach(button => {
    button.addEventListener('click', () => {
      const content = button.nextElementSibling;
      const isExpanded = button.getAttribute('aria-expanded') === 'true';
      
      button.setAttribute('aria-expanded', !isExpanded);
      content.classList.toggle('hidden');
      
      // Update icon if present
      const icon = button.querySelector('[data-accordion-icon]');
      if (icon) {
        icon.classList.toggle('rotate-180');
      }
    });
  });
}

// Modal management
export function initModal() {
  const modalTriggers = document.querySelectorAll('[data-modal]');
  const modals = document.querySelectorAll('[data-modal-content]');
  
  modalTriggers.forEach(trigger => {
    trigger.addEventListener('click', (e) => {
      e.preventDefault();
      const modalId = trigger.getAttribute('data-modal');
      const modal = document.querySelector(`[data-modal-content="${modalId}"]`);
      
      if (modal) {
        modal.classList.remove('hidden');
        modal.setAttribute('aria-hidden', 'false');
        
        // Focus management
        const focusableElements = modal.querySelectorAll('button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])');
        if (focusableElements.length > 0) {
          focusableElements[0].focus();
        }
        
        // Trap focus
        trapFocus(modal);
      }
    });
  });
  
  // Close modal on backdrop click or escape key
  modals.forEach(modal => {
    modal.addEventListener('click', (e) => {
      if (e.target === modal) {
        closeModal(modal);
      }
    });
    
    const closeBtn = modal.querySelector('[data-modal-close]');
    if (closeBtn) {
      closeBtn.addEventListener('click', () => closeModal(modal));
    }
  });
  
  // Escape key to close modal
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
      const openModal = document.querySelector('[data-modal-content]:not(.hidden)');
      if (openModal) {
        closeModal(openModal);
      }
    }
  });
}

// Close modal helper
function closeModal(modal) {
  modal.classList.add('hidden');
  modal.setAttribute('aria-hidden', 'true');
  
  // Return focus to trigger
  const trigger = document.querySelector(`[data-modal="${modal.getAttribute('data-modal-content')}"]`);
  if (trigger) {
    trigger.focus();
  }
}

// Focus trap for modals
function trapFocus(modal) {
  const focusableElements = modal.querySelectorAll('button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])');
  const firstElement = focusableElements[0];
  const lastElement = focusableElements[focusableElements.length - 1];
  
  modal.addEventListener('keydown', (e) => {
    if (e.key === 'Tab') {
      if (e.shiftKey) {
        if (document.activeElement === firstElement) {
          e.preventDefault();
          lastElement.focus();
        }
      } else {
        if (document.activeElement === lastElement) {
          e.preventDefault();
          firstElement.focus();
        }
      }
    }
  });
}

// Form helpers
export function initForms() {
  const forms = document.querySelectorAll('form[data-netlify="true"]');
  
  forms.forEach(form => {
    form.addEventListener('submit', (e) => {
      // Basic spam protection
      const honeypot = form.querySelector('[name="bot-field"]');
      if (honeypot && honeypot.value) {
        e.preventDefault();
        return;
      }
      
      // Show success message if form has success handling
      const successAnchor = form.getAttribute('data-success');
      if (successAnchor) {
        setTimeout(() => {
          window.location.hash = successAnchor;
        }, 100);
      }
    });
  });
}

// Initialize everything when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
  // Set initial theme
  const storage = localStorage.getItem('theme');
  const preferDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
  if (storage === 'dark' || (!storage && preferDark)) {
    document.documentElement.classList.add('dark');
  }
  
  // Update theme button text
  const themeBtn = document.getElementById('themeToggle');
  if (themeBtn) {
    themeBtn.textContent = document.documentElement.classList.contains('dark') ? 'Light' : 'Dark';
  }
  
  // Initialize theme toggle
  themeBtn?.addEventListener('click', toggleTheme);
  
  // Initialize mobile menu
  const mobileBtn = document.getElementById('mobileMenuBtn');
  mobileBtn?.addEventListener('click', toggleMobileMenu);
  
  // Initialize active navigation
  initActiveNav();
  
  // Initialize accordions
  initAccordions();
  
  // Initialize modals
  initModal();
  
  // Initialize forms
  initForms();
  
  // Set dynamic year in footer
  const yearElement = document.getElementById('year');
  if (yearElement) {
    yearElement.textContent = new Date().getFullYear();
  }
  
  // Add loading states to buttons
  const buttons = document.querySelectorAll('button[type="submit"]');
  buttons.forEach(button => {
    button.addEventListener('click', () => {
      if (button.form && button.form.checkValidity()) {
        button.disabled = true;
        button.innerHTML = '<svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path></svg>Sending...';
        
        // Re-enable after form submission
        setTimeout(() => {
          button.disabled = false;
          button.innerHTML = 'Send';
        }, 3000);
      }
    });
  });
});

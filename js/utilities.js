// iD01t Productions Website Utilities
// Theme toggle, mobile menu, navigation, and modal functionality

// Theme management
export function toggleTheme() {
  const html = document.documentElement;
  const currentTheme = html.getAttribute('data-theme');
  const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
  
  html.setAttribute('data-theme', newTheme);
  localStorage.setItem('theme', newTheme);
  
  // Update theme toggle button text
  const themeToggle = document.getElementById('themeToggle');
  if (themeToggle) {
    themeToggle.textContent = newTheme === 'dark' ? 'Light' : 'Dark';
  }
}

// Mobile menu management
export function toggleMobileMenu() {
  const mobileMenu = document.getElementById('mobileMenu');
  const mobileMenuBtn = document.getElementById('mobileMenuBtn');
  
  if (mobileMenu && mobileMenuBtn) {
    const isHidden = mobileMenu.classList.contains('hidden');
    
    if (isHidden) {
      mobileMenu.classList.remove('hidden');
      mobileMenuBtn.setAttribute('aria-expanded', 'true');
    } else {
      mobileMenu.classList.add('hidden');
      mobileMenuBtn.setAttribute('aria-expanded', 'false');
    }
  }
}

// Initialize active navigation
export function initActiveNav() {
  const currentPath = window.location.pathname;
  const navLinks = document.querySelectorAll('nav a[href]');
  
  navLinks.forEach(link => {
    const href = link.getAttribute('href');
    if (href === currentPath || (currentPath === '/' && href === '/index.html')) {
      link.classList.add('text-brand-600', 'dark:text-brand-400');
      link.setAttribute('aria-current', 'page');
    } else {
      link.classList.remove('text-brand-600', 'dark:text-brand-400');
      link.removeAttribute('aria-current');
    }
  });
}

// Accordion functionality
export function initAccordions() {
  const accordionButtons = document.querySelectorAll('[data-accordion]');
  
  accordionButtons.forEach(button => {
    button.addEventListener('click', () => {
      const target = button.getAttribute('data-accordion');
      const content = document.getElementById(target);
      const isExpanded = button.getAttribute('aria-expanded') === 'true';
      
      // Toggle expanded state
      button.setAttribute('aria-expanded', !isExpanded);
      
      // Toggle content visibility
      if (content) {
        if (isExpanded) {
          content.classList.add('hidden');
        } else {
          content.classList.remove('hidden');
        }
      }
    });
  });
}

// Modal functionality
export function initModal() {
  const modalTriggers = document.querySelectorAll('[data-modal]');
  
  modalTriggers.forEach(trigger => {
    trigger.addEventListener('click', (e) => {
      e.preventDefault();
      const modalId = trigger.getAttribute('data-modal');
      const modal = document.getElementById(modalId);
      
      if (modal) {
        modal.classList.remove('hidden');
        modal.setAttribute('aria-hidden', 'false');
        
        // Focus management
        const focusableElements = modal.querySelectorAll(
          'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
        );
        
        if (focusableElements.length > 0) {
          focusableElements[0].focus();
        }
        
        // Trap focus
        trapFocus(modal);
      }
    });
  });
  
  // Close modal on backdrop click or escape key
  document.addEventListener('click', (e) => {
    if (e.target.classList.contains('modal-backdrop')) {
      const modal = e.target.closest('[id$="-modal"]');
      if (modal) {
        closeModal(modal);
      }
    }
  });
  
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
      const openModal = document.querySelector('[aria-hidden="false"]');
      if (openModal) {
        closeModal(openModal);
      }
    }
  });
}

// Focus trap for modals
export function trapFocus(element) {
  const focusableElements = element.querySelectorAll(
    'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
  );
  
  const firstElement = focusableElements[0];
  const lastElement = focusableElements[focusableElements.length - 1];
  
  element.addEventListener('keydown', (e) => {
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

// Close modal helper
function closeModal(modal) {
  modal.classList.add('hidden');
  modal.setAttribute('aria-hidden', 'true');
  
  // Return focus to trigger element
  const trigger = document.querySelector(`[data-modal="${modal.id}"]`);
  if (trigger) {
    trigger.focus();
  }
}

// Dynamic footer year
function updateFooterYear() {
  const yearElement = document.getElementById('year');
  if (yearElement) {
    yearElement.textContent = new Date().getFullYear();
  }
}

// Initialize everything when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
  // Initialize theme
  const savedTheme = localStorage.getItem('theme') || 
    (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
  document.documentElement.setAttribute('data-theme', savedTheme);
  
  // Set theme toggle button text
  const themeToggle = document.getElementById('themeToggle');
  if (themeToggle) {
    themeToggle.textContent = savedTheme === 'dark' ? 'Light' : 'Dark';
  }
  
  // Theme toggle event listener
  if (themeToggle) {
    themeToggle.addEventListener('click', toggleTheme);
  }
  
  // Mobile menu event listener
  const mobileMenuBtn = document.getElementById('mobileMenuBtn');
  if (mobileMenuBtn) {
    mobileMenuBtn.addEventListener('click', toggleMobileMenu);
  }
  
  // Initialize navigation
  initActiveNav();
  
  // Initialize accordions
  initAccordions();
  
  // Initialize modals
  initModal();
  
  // Update footer year
  updateFooterYear();
  
  // Form success handling
  const urlParams = new URLSearchParams(window.location.search);
  if (urlParams.get('success') === 'true') {
    const successModal = document.getElementById('success');
    if (successModal) {
      successModal.classList.remove('hidden');
    }
  }
});

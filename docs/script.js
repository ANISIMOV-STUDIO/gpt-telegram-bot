// === DOM Elements ===
const hero = document.getElementById('hero');
const highlight = document.getElementById('highlight');

// === Parallax Hero Tilt ===
let isMouseInWindow = true;

document.addEventListener('mousemove', (e) => {
  if (!isMouseInWindow) return;
  
  const { innerWidth: w, innerHeight: h } = window;
  
  // Hero tilt effect
  const rotY = ((e.clientX - w/2) / w) * 12; // ±12deg range
  const rotX = -((e.clientY - h/2) / h) * 8;  // ±8deg range
  
  hero.style.transform = `rotateX(${rotX}deg) rotateY(${rotY}deg)`;
  
  // Dynamic highlight following cursor
  const x = (e.clientX / w) * 100 + '%';
  const y = (e.clientY / h) * 100 + '%';
  
  highlight.style.setProperty('--mx', x);
  highlight.style.setProperty('--my', y);
});

// === Mouse enter/leave window tracking ===
window.addEventListener('mouseenter', () => {
  isMouseInWindow = true;
});

window.addEventListener('mouseleave', () => {
  isMouseInWindow = false;
  // Reset hero tilt
  hero.style.transform = '';
  // Reset highlight to center
  highlight.style.setProperty('--mx', '50%');
  highlight.style.setProperty('--my', '50%');
});

// === Scroll-based hero fade ===
window.addEventListener('scroll', () => {
  const scrolled = window.scrollY;
  const fadeStart = 100;
  const fadeEnd = 400;
  
  if (scrolled <= fadeStart) {
    hero.style.opacity = '1';
  } else if (scrolled >= fadeEnd) {
    hero.style.opacity = '0.2';
  } else {
    const fadeProgress = (scrolled - fadeStart) / (fadeEnd - fadeStart);
    hero.style.opacity = 1 - (fadeProgress * 0.8);
  }
});

// === Card stagger animation on load ===
document.addEventListener('DOMContentLoaded', () => {
  const cards = document.querySelectorAll('.card');
  const infoCards = document.querySelectorAll('.info-card');
  
  cards.forEach((card, index) => {
    card.style.opacity = '0';
    card.style.transform = 'translateY(30px)';
    
    setTimeout(() => {
      card.style.transition = 'all 0.6s cubic-bezier(0.25, 0.46, 0.45, 0.94)';
      card.style.opacity = '1';
      card.style.transform = 'translateY(0)';
    }, 800 + (index * 150)); // Stagger by 150ms
  });
  
  // Animate info cards
  infoCards.forEach((card, index) => {
    card.style.opacity = '0';
    card.style.transform = 'translateY(40px) scale(0.95)';
    
    setTimeout(() => {
      card.style.transition = 'all 0.8s cubic-bezier(0.25, 0.46, 0.45, 0.94)';
      card.style.opacity = '1';
      card.style.transform = 'translateY(0) scale(1)';
    }, 300 + (index * 200)); // Stagger info cards
  });
});

// === Enhanced card hover effects ===
document.querySelectorAll('.card').forEach(card => {
  card.addEventListener('mouseenter', (e) => {
    // Add golden glow overlay
    const rect = card.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;
    
    card.style.setProperty('--hover-x', `${x}px`);
    card.style.setProperty('--hover-y', `${y}px`);
  });
  
  card.addEventListener('mousemove', (e) => {
    const rect = card.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;
    
    card.style.setProperty('--hover-x', `${x}px`);
    card.style.setProperty('--hover-y', `${y}px`);
  });
});

// === Smooth scroll for any internal links ===
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
  anchor.addEventListener('click', function (e) {
    e.preventDefault();
    const target = document.querySelector(this.getAttribute('href'));
    if (target) {
      target.scrollIntoView({
        behavior: 'smooth',
        block: 'start'
      });
    }
  });
});

// === Performance optimization: throttle scroll events ===
let scrollTimeout;
const originalScrollHandler = window.onscroll;

window.addEventListener('scroll', () => {
  if (scrollTimeout) {
    clearTimeout(scrollTimeout);
  }
  
  scrollTimeout = setTimeout(() => {
    // Scroll handler logic here
  }, 16); // ~60fps
}); 
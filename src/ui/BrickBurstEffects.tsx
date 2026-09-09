import { useEffect } from 'react';

const burstTargets = [
  'button:not([disabled]):not([role="tab"])',
  'a.primary-button',
  'a.primary-link',
  '.hero-actions a',
  '.story-copy > a',
].join(',');

const colors = ['#e23b34', '#f2c230', '#2f6fce', '#22a7b8', '#d7559b', '#7654c6'];

export function BrickBurstEffects() {
  useEffect(() => {
    const reducedMotion = matchMedia('(prefers-reduced-motion: reduce)');

    const burst = (event: MouseEvent) => {
      if (reducedMotion.matches || event.button !== 0 || !(event.target instanceof Element)) return;
      const target = event.target.closest<HTMLElement>(burstTargets);
      if (!target || target.matches(':disabled')) return;

      const rect = target.getBoundingClientRect();
      const originX = event.detail ? event.clientX : rect.left + rect.width / 2;
      const originY = event.detail ? event.clientY : rect.top + rect.height / 2;
      target.animate([
        { transform: 'translateY(0) scale(1)' },
        { transform: 'translateY(2px) scale(.96)', offset: 0.35 },
        { transform: 'translateY(-1px) scale(1.015)', offset: 0.72 },
        { transform: 'translateY(0) scale(1)' },
      ], { duration: 360, easing: 'cubic-bezier(.22, 1, .36, 1)' });

      for (let index = 0; index < 10; index++) {
        const angle = -Math.PI * 0.95 + index / 9 * Math.PI * 1.9;
        const distance = 24 + index % 3 * 9;
        const piece = document.createElement('i');
        piece.className = 'brick-burst-piece';
        piece.setAttribute('aria-hidden', 'true');
        piece.style.left = `${originX - 4 + Math.cos(angle) * 5}px`;
        piece.style.top = `${originY - 3 + Math.sin(angle) * 3}px`;
        piece.style.width = `${6 + index % 3 * 2}px`;
        piece.style.height = `${5 + (index + 1) % 2 * 2}px`;
        piece.style.background = colors[index % colors.length];
        piece.style.setProperty('--burst-x', `${Math.cos(angle) * distance}px`);
        piece.style.setProperty('--burst-y', `${Math.sin(angle) * distance - 12}px`);
        piece.style.setProperty('--burst-spin', `${index % 2 ? 150 : -150}deg`);
        document.body.appendChild(piece);
        piece.addEventListener('animationend', () => piece.remove(), { once: true });
      }
    };

    document.addEventListener('click', burst);
    return () => document.removeEventListener('click', burst);
  }, []);

  return null;
}

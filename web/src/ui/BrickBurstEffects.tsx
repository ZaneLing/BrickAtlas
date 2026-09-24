import { useEffect } from 'react';

const burstTargets = [
  'button:not([disabled]):not([role="tab"])',
  'a.primary-button',
  'a.primary-link',
  '.hero-actions a',
  '.story-copy > a',
].join(',');

const colors = ['#e23b34', '#f2c230', '#2f6fce', '#22a7b8', '#d7559b', '#7654c6'];
const shatterTargets = [
  '[data-brick-effect="shatter"]',
  '.primary-button',
  '.hero-primary',
  '.model-card-actions .primary-link',
].join(',');

export function BrickBurstEffects() {
  useEffect(() => {
    const reducedMotion = matchMedia('(prefers-reduced-motion: reduce)');

    const particles = (originX: number, originY: number, target?: HTMLElement, shatter = false) => {
      const rect = target?.getBoundingClientRect();
      const count = shatter ? 14 : 10;
      for (let index = 0; index < count; index++) {
        const angle = -Math.PI * 0.95 + index / Math.max(1, count - 1) * Math.PI * 1.9;
        const distance = (shatter ? 38 : 24) + index % 3 * 9;
        const piece = document.createElement('i');
        piece.className = `brick-burst-piece ${shatter ? 'brick-shatter-piece' : ''}`;
        piece.setAttribute('aria-hidden', 'true');
        const column = index % 4, row = Math.floor(index / 4);
        piece.style.left = `${shatter && rect ? rect.left + (column + .5) / 4 * rect.width - 5 : originX - 4 + Math.cos(angle) * 5}px`;
        piece.style.top = `${shatter && rect ? rect.top + (row + .5) / 4 * Math.min(rect.height, 56) - 4 : originY - 3 + Math.sin(angle) * 3}px`;
        piece.style.width = `${shatter && rect ? Math.max(7, Math.min(18, rect.width / 5)) : 6 + index % 3 * 2}px`;
        piece.style.height = `${shatter ? Math.max(6, Math.min(11, (rect?.height ?? 30) / 4)) : 5 + (index + 1) % 2 * 2}px`;
        piece.style.background = shatter && target ? getComputedStyle(target).backgroundColor : colors[index % colors.length];
        piece.style.setProperty('--burst-x', `${Math.cos(angle) * distance}px`);
        piece.style.setProperty('--burst-y', `${Math.sin(angle) * distance - (shatter ? 20 : 12)}px`);
        piece.style.setProperty('--burst-spin', `${index % 2 ? 150 + index * 12 : -150 - index * 12}deg`);
        document.body.appendChild(piece);
        piece.addEventListener('animationend', () => piece.remove(), { once: true });
      }
    };

    const burst = (event: MouseEvent) => {
      if (reducedMotion.matches || event.button !== 0 || !(event.target instanceof Element)) return;
      const target = event.target.closest<HTMLElement>(burstTargets);
      if (!target || target.matches(':disabled')) return;

      const rect = target.getBoundingClientRect();
      const originX = event.detail ? event.clientX : rect.left + rect.width / 2;
      const originY = event.detail ? event.clientY : rect.top + rect.height / 2;
      const shatter = target.matches(shatterTargets);
      const quiet = !!target.closest('.diy-categories, .diy-swatches, .diy-view-navigation, .color-palette');
      target.animate([
        { transform: 'translateY(0) scale(1)', filter: 'brightness(1)' },
        { transform: `translateY(2px) scale(${shatter ? .91 : .96})`, filter: 'brightness(.92)', offset: 0.34 },
        { transform: 'translateY(-1px) scale(1.015)', filter: 'brightness(1.06)', offset: 0.72 },
        { transform: 'translateY(0) scale(1)', filter: 'brightness(1)' },
      ], { duration: shatter ? 480 : 360, easing: 'cubic-bezier(.22, 1, .36, 1)' });
      if (!quiet) particles(originX, originY, target, shatter);
    };

    const placement = (event: Event) => {
      if (reducedMotion.matches) return;
      const detail = (event as CustomEvent<{ x: number; y: number; color: string }>).detail;
      const ring = document.createElement('i');
      ring.className = 'brick-placement-ring';
      ring.style.left = `${detail.x}px`;
      ring.style.top = `${detail.y}px`;
      ring.style.borderColor = detail.color;
      document.body.appendChild(ring);
      ring.addEventListener('animationend', () => ring.remove(), { once: true });
      particles(detail.x, detail.y, undefined, false);
    };
    document.addEventListener('click', burst);
    document.addEventListener('brick-atlas:placement', placement);
    return () => {
      document.removeEventListener('click', burst);
      document.removeEventListener('brick-atlas:placement', placement);
    };
  }, []);

  return null;
}

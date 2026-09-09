export function readLocal(key: string): string | null {
  try { return localStorage.getItem(key); } catch { return null; }
}

export function writeLocal(key: string, value: string): boolean {
  try { localStorage.setItem(key, value); return true; } catch { return false; }
}

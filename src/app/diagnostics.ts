interface DiagnosticEvent { at: string; type: string; data: Record<string, unknown> }
const events: DiagnosticEvent[] = [];

export function recordDiagnostic(type: string, data: Record<string, unknown>) {
  events.push({ at: new Date().toISOString(), type, data });
  if (events.length > 50) events.shift();
}

export function diagnosticsReport() {
  return {
    version: '1.0.0',
    browser: navigator.userAgent,
    viewport: { width: innerWidth, height: innerHeight, devicePixelRatio },
    events: [...events],
    metrics: window.__atlas?.(),
  };
}

export function installDiagnostics() {
  const onError = (event: ErrorEvent) => recordDiagnostic('window-error', { message: event.message });
  const onRejection = (event: PromiseRejectionEvent) => recordDiagnostic('unhandled-rejection', { message: String(event.reason) });
  window.addEventListener('error', onError);
  window.addEventListener('unhandledrejection', onRejection);
  return () => {
    window.removeEventListener('error', onError);
    window.removeEventListener('unhandledrejection', onRejection);
  };
}

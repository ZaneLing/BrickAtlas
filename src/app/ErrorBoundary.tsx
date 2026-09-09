import { Component, type ErrorInfo, type ReactNode } from 'react';
import { recordDiagnostic } from './diagnostics';

export class ErrorBoundary extends Component<{ children: ReactNode }, { error: string | null }> {
  state = { error: null as string | null };
  static getDerivedStateFromError(error: Error) { return { error: error.message }; }
  componentDidCatch(error: Error, info: ErrorInfo) {
    recordDiagnostic('react-error', { message: error.message, componentStack: info.componentStack });
  }
  render() {
    if (this.state.error) return <main className="app"><div className="loading-state error-state" role="alert"><h1>Brick Atlas</h1><p>应用出现异常：{this.state.error}</p><button className="primary-button" onClick={() => location.reload()}>重新加载</button></div></main>;
    return this.props.children;
  }
}

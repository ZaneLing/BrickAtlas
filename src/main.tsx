import { createRoot } from 'react-dom/client';
import App from './app/App';
import { ErrorBoundary } from './app/ErrorBoundary';
import './app/styles.css';

createRoot(document.getElementById('root')!).render(<ErrorBoundary><App /></ErrorBoundary>);

import { createRoot } from 'react-dom/client';
import App from './app/App';
import { ErrorBoundary } from './app/ErrorBoundary';
import { BrickBurstEffects } from './ui/BrickBurstEffects';
import './app/styles.css';
import './app/workspaces.css';

createRoot(document.getElementById('root')!).render(
  <ErrorBoundary>
    <BrickBurstEffects />
    <App />
  </ErrorBoundary>,
);

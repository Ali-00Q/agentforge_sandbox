import React, { useEffect } from 'react';
import LoginForm from './components/LoginForm';
import ThemeToggle from './components/ThemeToggle';

function App() {
  useEffect(() => {
    try {
      const stored = localStorage.getItem('theme:v1');
      if (stored === 'dark') {
        document.documentElement.classList.add('dark');
      } else if (stored === 'light') {
        document.documentElement.classList.remove('dark');
      }
    } catch {}
  }, []);

  const handleLogin = (credentials) => {
    console.log('Logging in with:', credentials);
    alert(`Logged in successfully as ${credentials.email}`);
  };

  return (
    <div className="App min-h-screen bg-white dark:bg-gray-950 text-gray-900 dark:text-gray-100 transition-colors">
      <header className="flex flex-col sm:flex-row items-center justify-between p-4 border-b border-gray-200 dark:border-gray-800 max-w-4xl mx-auto gap-4">
        <h1 className="text-xl font-bold">App Navigation</h1>
        <nav className="flex items-center justify-between w-full sm:w-auto space-x-4">
          <div className="flex items-center space-x-2">
            <ThemeToggle />
          </div>
          <div className="flex items-center space-x-2">
            {/* User profile icon placeholder next to theme toggle */}
            <div className="w-8 h-8 rounded-full bg-gray-200 dark:bg-gray-800 flex items-center justify-center text-xs font-semibold" aria-label="User Profile">
              UP
            </div>
          </div>
        </nav>
      </header>
      <main className="p-4">
        <LoginForm onLogin={handleLogin} />
      </main>
    </div>
  );
}

export default App;
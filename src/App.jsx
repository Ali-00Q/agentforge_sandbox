import React from 'react';
import LoginForm from './components/LoginForm';
import ThemeToggle from './components/ThemeToggle';

function App() {
  const handleLogin = (credentials) => {
    console.log('Logging in with:', credentials);
    alert(`Logged in successfully as ${credentials.email}`);
  };

  return (
    <div className="App min-h-screen bg-white dark:bg-gray-950 text-gray-900 dark:text-gray-100 transition-colors">
      <header className="flex items-center justify-between p-4 border-b border-gray-200 dark:border-gray-800 max-w-4xl mx-auto">
        <h1 className="text-xl font-bold">App Navigation</h1>
        <ThemeToggle />
      </header>
      <main className="p-4">
        <LoginForm onLogin={handleLogin} />
      </main>
    </div>
  );
}

export default App;
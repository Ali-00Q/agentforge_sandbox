import React from 'react';
import LoginForm from './components/LoginForm';

function App() {
  const handleLogin = (credentials) => {
    console.log('Logging in with:', credentials);
    alert(`Logged in successfully as ${credentials.email}`);
  };

  return (
    <div className="App">
      <LoginForm onLogin={handleLogin} />
    </div>
  );
}

export default App;
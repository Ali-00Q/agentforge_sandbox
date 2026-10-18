import React from 'react';

export default function HomePage({ user, onLogout }) {
  return (
    <div className="max-w-2xl mx-auto mt-8 p-6 bg-white dark:bg-gray-900 rounded-xl shadow-md border border-gray-100 dark:border-gray-800 text-center">
      <h2 className="text-2xl font-bold mb-4">Welcome, {user?.email || 'User'}!</h2>
      <p className="text-gray-600 dark:text-gray-400 mb-6">You have successfully logged into the home page.</p>
      <button
        onClick={onLogout}
        className="px-4 py-2 bg-red-600 hover:bg-red-700 text-white rounded-lg transition-colors"
      >
        Logout
      </button>
    </div>
  );
}

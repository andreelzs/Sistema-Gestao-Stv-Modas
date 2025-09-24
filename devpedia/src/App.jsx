import React from 'react';
import { BrowserRouter as Router, Routes, Route, NavLink } from 'react-router-dom';
import { ProfileProvider } from './context/ProfileContext';
import { FavoritesProvider } from './context/FavoritesContext';
import HomePage from './pages/HomePage';
import FavoritesPage from './pages/FavoritesPage';
import './App.css';

function App() {
  return (
    <ProfileProvider>
      <FavoritesProvider>
        <Router>
          <nav className="navbar">
            <NavLink to="/" className="nav-logo">DevPedia</NavLink>
            <div className="nav-links">
              <NavLink to="/" className={({ isActive }) => (isActive ? 'nav-link active' : 'nav-link')}>
                Busca
              </NavLink>
              <NavLink to="/favorites" className={({ isActive }) => (isActive ? 'nav-link active' : 'nav-link')}>
                Favoritos
              </NavLink>
            </div>
          </nav>
          <main className="container">
            <Routes>
              <Route path="/" element={<HomePage />} />
              <Route path="/favorites" element={<FavoritesPage />} />
            </Routes>
          </main>
        </Router>
      </FavoritesProvider>
    </ProfileProvider>
  );
}

export default App;

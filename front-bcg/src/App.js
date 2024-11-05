// src/App.js
import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Register from './components/Register';
import Login from './components/Login';
import Home from './components/Home';
import '@fortawesome/fontawesome-free/css/all.min.css';

import './App.css';

// Função para verificar se o usuário está autenticado
const isAuthenticated = () => {
  return localStorage.getItem("authToken") !== null;
};

// Componente PrivateRoute para proteger rotas privadas
const PrivateRoute = ({ element, ...rest }) => {
  return isAuthenticated() ? element : <Navigate to="/login" />;
};

function App() {
  return (
    <Router>
      <div className="App">
        <Routes>
          <Route path="/" element={<PrivateRoute element={<Home />} />} />
          <Route path="/register" element={<Register />} />
          <Route path="/login" element={<Login />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;

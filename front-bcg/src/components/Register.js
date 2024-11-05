// src/components/Register.js
import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { FaUser, FaEnvelope, FaEye, FaEyeSlash } from 'react-icons/fa';
import Logo from './Logo';
import './Register.css';

function Register() {
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleRegister = async (e) => {
    e.preventDefault();

    try {
      const response = await fetch('http://localhost:5000/register', { // Altere a URL se necessário
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          name: username,
          email: email,
          password: password,
        }),
      });

      const data = await response.json();

      if (response.ok) {
        // Redireciona para a página inicial após o registro bem-sucedido
        navigate('/');
      } else {
        // Exibe mensagem de erro
        setError(data.error || 'Erro no registro');
      }
    } catch (err) {
      console.error('Erro:', err);
      setError('Erro ao se conectar ao servidor');
    }
  };

  return (
    <div className="container">
      <div className="form register-form">
        <Logo />
        <h2>Registro</h2>
        <form onSubmit={handleRegister}>
          <div className="input-container">
            <FaUser className="input-icon" />
            <input
              type="text"
              placeholder="Nome de usuário"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
            />
          </div>
          <div className="input-container">
            <FaEnvelope className="input-icon" />
            <input
              type="email"
              placeholder="Email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </div>
          <div className="input-container">
            <input
              type={showPassword ? "text" : "password"}
              placeholder="Senha"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
            <div className="toggle-password" onClick={() => setShowPassword(!showPassword)}>
              {showPassword ? <FaEyeSlash /> : <FaEye />}
            </div>
          </div>
          {error && <p className="error-message">{error}</p>}
          <button className="form-button register-button">Registrar</button>
        </form>
        <p>Já tem uma conta? <Link to="/login" className="form-link">Faça login aqui</Link></p>
      </div>
      <div className="image-container" />
    </div>
  );
}

export default Register;

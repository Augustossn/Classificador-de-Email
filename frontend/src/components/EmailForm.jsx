import React, { useState } from 'react';
import axios from 'axios';
import '../styles/EmailForm.css';

function EmailForm({ onResult, onLoading }) {
  const [emailText, setEmailText] = useState('');
  const [file, setFile] = useState(null);
  const [activeTab, setActiveTab] = useState('text');
  const [error, setError] = useState('');

  const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';

  const handleTextChange = (e) => {
    setEmailText(e.target.value);
    setError('');
  };

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile) {
      if (!['text/plain', 'application/pdf'].includes(selectedFile.type)) {
        setError('Por favor, selecione um arquivo .txt ou .pdf');
        setFile(null);
        return;
      }
      if (selectedFile.size > 5 * 1024 * 1024) {
        setError('Arquivo deve ter menos de 5MB');
        setFile(null);
        return;
      }
      setFile(selectedFile);
      setError('');
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (activeTab === 'text' && !emailText.trim()) {
      setError('Por favor, insira o conteúdo do email');
      return;
    }

    if (activeTab === 'file' && !file) {
      setError('Por favor, selecione um arquivo');
      return;
    }

    try {
      onLoading(true);
      setError('');

      let response;

      if (activeTab === 'text') {
        response = await axios.post(
          `${API_URL}/classify`,
          { email_content: emailText },
          { headers: { 'Content-Type': 'application/json' } }
        );
      } else {
        const formData = new FormData();
        formData.append('file', file);
        response = await axios.post(
          `${API_URL}/classify`,
          formData,
          { headers: { 'Content-Type': 'multipart/form-data' } }
        );
      }

      if (response.data.sucesso) {
        onResult(response.data);
        setEmailText('');
        setFile(null);
      } else {
        setError(response.data.erro || 'Erro ao processar email');
      }
    } catch (err) {
      console.error('Erro:', err);
      setError(
        err.response?.data?.erro ||
        'Erro ao conectar com o servidor. Verifique se o backend está rodando.'
      );
    } finally {
      onLoading(false);
    }
  };

  return (
    <div className="email-form-container">
      <div className="form-header">
        <h2>Classificador de Emails</h2>
        <p>Insira um email para classificação automática e sugestão de resposta</p>
      </div>

      <form onSubmit={handleSubmit}>
        <div className="tabs">
          <button
            type="button"
            className={`tab ${activeTab === 'text' ? 'active' : ''}`}
            onClick={() => {
              setActiveTab('text');
              setError('');
            }}
          >
            Texto Direto
          </button>
          <button
            type="button"
            className={`tab ${activeTab === 'file' ? 'active' : ''}`}
            onClick={() => {
              setActiveTab('file');
              setError('');
            }}
          >
            Upload de Arquivo
          </button>
        </div>

        <div className="tab-content">
          {activeTab === 'text' && (
            <div className="form-group">
              <label htmlFor="email-text">Cole o conteúdo do email aqui:</label>
              <textarea
                id="email-text"
                value={emailText}
                onChange={handleTextChange}
                placeholder="Exemplo: Olá, gostaria de saber o status da minha requisição..."
                rows="8"
                className="email-textarea"
              />
              <small className="char-count">
                {emailText.length} caracteres
              </small>
            </div>
          )}

          {activeTab === 'file' && (
            <div className="form-group">
              <label htmlFor="file-input" className="file-label">
                <input
                  id="file-input"
                  type="file"
                  accept=".txt,.pdf"
                  onChange={handleFileChange}
                  className="file-input"
                />
                <span className="file-button">
                  Selecione um arquivo (.txt ou .pdf)
                </span>
              </label>
              {file && (
                <div className="file-info">
                  ✓ Arquivo selecionado: <strong>{file.name}</strong>
                </div>
              )}
            </div>
          )}
        </div>

        {error && <div className="error-message">{error}</div>}

        <button type="submit" className="submit-button">
          Classificar Email
        </button>
      </form>
    </div>
  );
}

export default EmailForm;

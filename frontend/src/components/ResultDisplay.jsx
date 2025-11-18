import React, { useState } from 'react';
import '../styles/ResultDisplay.css';

function ResultDisplay({ result, onClear }) {
  const [copied, setCopied] = useState(false);

  if (!result) {
    return (
      <div className="result-container empty">
        <div className="empty-state">
          <p>Nenhum resultado ainda. Classifique um email para começar</p>
        </div>
      </div>
    );
  }

  const copyToClipboard = (text) => {
    navigator.clipboard.writeText(text);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const getCategoryColor = (categoria) => {
    return categoria === 'Produtivo' ? 'productive' : 'unproductive';
  };

  const getConfidenceColor = (confianca) => {
    switch (confianca) {
      case 'Alta':
        return 'high';
      case 'Média':
        return 'medium';
      case 'Baixa':
        return 'low';
      default:
        return 'medium';
    }
  };

  return (
    <div className="result-container">
      <div className="result-header">
        <h2>Resultado da Classificação</h2>
        <button className="clear-button" onClick={onClear}>
          Novo Email
        </button>
      </div>

      <div className="result-section classification-section">
        <h3>Classificação</h3>
        <div className={`category-badge ${getCategoryColor(result.categoria)}`}>
          <span className="category-text">{result.categoria}</span>
        </div>

        <div className="classification-details">
          <div className="detail-item">
            <label>Confiança:</label>
            <div className={`confidence-badge ${getConfidenceColor(result.confianca)}`}>
              {result.confianca}
            </div>
          </div>

          <div className="detail-item">
            <label>Motivo:</label>
            <p className="reason-text">{result.motivo}</p>
          </div>
        </div>
      </div>

      <div className="result-section response-section">
        <h3>Resposta Sugerida</h3>
        <div className="response-box">
          <p>{result.resposta_sugerida}</p>
        </div>

        <button
          className={`copy-button ${copied ? 'copied' : ''}`}
          onClick={() => copyToClipboard(result.resposta_sugerida)}
        >
          {copied ? 'Copiado!' : 'Copiar Resposta'}
        </button>
      </div>

      <div className="result-section info-section">
        <h3>Como Usar</h3>
        <ul>
          <li>
            <strong>Se Produtivo:</strong> A resposta sugere ação. Use para responder
            solicitações de suporte ou atualizações.
          </li>
          <li>
            <strong>Se Improdutivo:</strong> A resposta é um agradecimento educado.
            Use para responder felicitações ou mensagens não urgentes.
          </li>
          <li>
            <strong>Copie a resposta:</strong> Clique no botão acima para copiar
            e colar em seu cliente de email.
          </li>
        </ul>
      </div>
    </div>
  );
}

export default ResultDisplay;

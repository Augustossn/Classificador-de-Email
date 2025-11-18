import React, { useState } from 'react';
import EmailForm from './components/EmailForm';
import ResultDisplay from './components/ResultDisplay';
import './App.css';

function App() {
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleResult = (data) => {
    setResult(data);
  };

  const handleClear = () => {
    setResult(null);
  };

  return (
    <div className="app-container">
      <header className="app-header">
        <div className="header-content">
          <h1>Classificador Inteligente de Emails</h1>
          <p>
            Classifique automaticamente seus emails como Produtivos ou Improdutivos
            e receba sugestões de respostas automáticas
          </p>
        </div>
      </header>

      <main className="app-main">
        <div className="container">
          <div className="content-grid">
            <div className="form-column">
              <EmailForm onResult={handleResult} onLoading={setLoading} />
            </div>

            <div className="result-column">
              {loading ? (
                <div className="loading-container">
                  <div className="spinner"></div>
                  <p>Processando email...</p>
                </div>
              ) : (
                <ResultDisplay result={result} onClear={handleClear} />
              )}
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}

export default App;

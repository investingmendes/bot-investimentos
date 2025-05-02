import yfinance as yf
import time

def analisar_fundamentalista(ticker):
    try:
        time.sleep(2)  # Espera 2 segundos
        
        if not ticker.endswith('.SA'):
            ticker += '.SA'
        
        acao = yf.Ticker(ticker)
        info = acao.info
        
        if not info:
            return "❌ Não foi possível obter dados para este ativo."
        
        # Restante do seu código aqui...
        # (mantenha o que já tinha de análise)
        
    except Exception as e:
        return f"❌ Erro ao analisar: {str(e)}"
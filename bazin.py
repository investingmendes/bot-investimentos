import yfinance as yf
import time

# Configuração simplificada (sem cache)
def calcular_bazin(ticker, anos=5, taxa_minima=0.06):
    try:
        time.sleep(2)  # Espera 2 segundos entre requisições
        if not ticker.endswith('.SA'):
            ticker += '.SA'
        
        # Restante do seu código aqui...
        # (mantenha o cálculo do método Bazin)
        
    except Exception as e:
        return f"❌ Erro no cálculo: {str(e)}"
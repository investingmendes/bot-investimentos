import yfinance as yf
import time
import random
from datetime import timedelta
import os

# Mesmo cache do fundamentalista.py
cache_dir = "cache_dir"
os.makedirs(cache_dir, exist_ok=True)
yf.set_tz_cache_location(cache_dir)
yf.set_tz_cache_duration(timedelta(hours=6))

def calcular_bazin(ticker, anos=5, taxa_minima=0.06):
    try:
        # Espera 2-4 segundos entre requisições
        time.sleep(random.uniform(2, 4))
        
        if not ticker.endswith('.SA'):
            ticker += '.SA'
        
        # Restante do seu código aqui...
        # (mantenha o cálculo do método Bazin)
        
    except Exception as e:
        return f"❌ Erro no cálculo: {str(e)}"
import yfinance as yf
import pandas as pd
from bs4 import BeautifulSoup
import requests

def analisar_fundamentalista(ticker):
    try:
        # Adiciona .SA para ações brasileiras no yfinance
        if not ticker.endswith('.SA'):
            ticker += '.SA'
        
        # Obtém dados do Yahoo Finance
        acao = yf.Ticker(ticker)
        info = acao.info
        
        # Verifica se temos dados suficientes
        if not info:
            return "❌ Não foi possível obter dados para este ativo."
        
        # Coleta dados fundamentais
        empresa = info.get('longName', 'N/A')
        setor = info.get('sector', 'N/A')
        cotacao = info.get('currentPrice', 'N/A')
        pl = info.get('trailingPE', 'N/A')
        roe = info.get('returnOnEquity', 'N/A')
        roic = info.get('returnOnInvestedCapital', 'N/A')
        div_yield = info.get('dividendYield', 'N/A')
        if div_yield != 'N/A':
            div_yield = f"{div_yield * 100:.2f}%"
        
        # Coleta dados de proventos
        dividends = acao.dividends
        if not dividends.empty:
            ult_prov = dividends[-1]
            media_prov = dividends.mean()
        else:
            ult_prov = 'N/A'
            media_prov = 'N/A'
        
        # Análise qualitativa (raspagem de notícias)
        noticias = raspar_noticias(empresa)
        
        # Monta resposta
        resposta = f"""
📈 *ANÁLISE FUNDAMENTALISTA* 📉

*Empresa:* {empresa}
*Setor:* {setor}
*Cotação:* R$ {cotacao if isinstance(cotacao, str) else f"{cotacao:.2f}"}

📊 *Indicadores Chave:*
- P/L: {pl if isinstance(pl, str) else f"{pl:.2f}"}
- ROE: {roe if isinstance(roe, str) else f"{roe*100:.2f}%"}
- ROIC: {roic if isinstance(roic, str) else f"{roic*100:.2f}%"}
- Dividend Yield: {div_yield}

💰 *Proventos:*
- Último: R$ {ult_prov if isinstance(ult_prov, str) else f"{ult_prov:.2f}"}
- Média: R$ {media_prov if isinstance(media_prov, str) else f"{media_prov:.2f}"}

📰 *Últimas Notícias:*
{noticias if noticias else "Nenhuma notícia relevante encontrada."}

⚠️ *Disclaimer:* Esta análise é automatizada e não constitui recomendação de investimento.
"""
        return resposta
    
    except Exception as e:
        return f"❌ Erro ao analisar o ativo: {str(e)}"

def raspar_noticias(empresa):
    try:
        # Exemplo de raspagem de notícias (adaptar conforme necessário)
        url = f"https://www.google.com/search?q={empresa.replace(' ', '+')}+site:valor.com.br&tbm=nws"
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        noticias = []
        for item in soup.select('.dbsr')[:3]:  # Limita a 3 notícias
            titulo = item.select_one('.nDgy9d').text
            link = item.a['href']
            noticias.append(f"• {titulo} - [Ler mais]({link})")
        
        return "\n".join(noticias)
    except:
        return ""
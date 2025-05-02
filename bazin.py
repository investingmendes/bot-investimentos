import yfinance as yf

def calcular_bazin(ticker, anos=5, taxa_minima=0.06):
    try:
        # Adiciona .SA para ações brasileiras no yfinance
        if not ticker.endswith('.SA'):
            ticker += '.SA'
        
        # Obtém dados históricos de dividendos
        acao = yf.Ticker(ticker)
        dividends = acao.dividends
        
        if dividends.empty:
            return "❌ Não há dados de dividendos suficientes para este ativo."
        
        # Filtra os últimos X anos
        ultimos_anos = dividends.last(f'{anos}Y')
        if len(ultimos_anos) < 1:
            return f"❌ Não há dados de dividendos nos últimos {anos} anos."
        
        # Calcula a média dos dividendos
        media_dividendos = ultimos_anos.mean()
        
        # Calcula o preço justo pelo Método Bazin
        preco_justo = media_dividendos / taxa_minima
        
        # Obtém a cotação atual
        info = acao.info
        cotacao = info.get('currentPrice', None)
        
        if cotacao is None:
            comparacao = ""
        else:
            diferenca = preco_justo - cotacao
            percentual = (diferenca / cotacao) * 100
            if diferenca > 0:
                comparacao = f"💰 *Subvalorizado:* {percentual:.2f}% abaixo do preço justo"
            else:
                comparacao = f"⚠️ *Sobrevalorizado:* {abs(percentual):.2f}% acima do preço justo"
        
        # Monta resposta
        resposta = f"""
🧮 *MÉTODO BAZIN* 🧮

*Ativo:* {ticker.replace('.SA', '')}
*Período analisado:* Últimos {anos} anos
*Taxa mínima de retorno:* {taxa_minima*100:.0f}% a.a.

📊 *Resultados:*
- Média de dividendos: R$ {media_dividendos:.2f}
- Preço justo calculado: R$ {preco_justo:.2f}
- Cotação atual: {'R$ ' + f"{cotacao:.2f}" if cotacao else "N/A"}

{comparacao if cotacao else ""}

📌 *Interpretação:*
O Método Bazin sugere que o preço justo é o valor que, ao receber a média histórica de dividendos, proporcionaria um retorno mínimo de {taxa_minima*100:.0f}% ao ano.

⚠️ *Limitações:*
- Não considera crescimento futuro dos dividendos
- Sensível à taxa de retorno mínima escolhida
- Baseado apenas em dados históricos
"""
        return resposta
    
    except Exception as e:
        return f"❌ Erro ao calcular pelo Método Bazin: {str(e)}"
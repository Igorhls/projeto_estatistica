import pandas as pd

# Dados do Igor (Source 1)
dados_igor = {
    "Item": ["Arroz", "Feijão", "Carne", "Leite", "Farinha", "Açúcar", "Oleo", "Pão", "Café", "Ovo", "Frango", "Bolacha", "Vitamilho", "Banana", "Maça", "Tomate", "Cebola"],
    "Semana 1": [4.99, 2.19, 39.90, 5.98, 5.00, 4.49, 9.08, 6.19, 16.63, 19.11, 16.90, 3.99, 2.19, 5.50, 8.99, 4.50, 4.00],
    "Semana 2": [5.10, 7.29, 41.50, 5.90, 5.00, 4.49, 8.80, 5.99, 16.00, 18.50, 17.50, 3.99, 2.19, 5.80, 9.50, 4.80, 4.50],
    "Semana 3": [5.15, 7.45, 44.90, 5.85, 4.95, 4.59, 8.20, 6.29, 15.00, 18.00, 18.00, 4.19, 2.29, 6.00, 9.50, 5.50, 5.00],
    "Semana 4": [4.15, 7.59, 39.90, 5.80, 4.24, 3.99, 2.79, 5.55, 14.29, 17.73, 18.50, 4.19, 2.29, 6.40, 9.80, 6.00, 5.50]
}

# Dados do Gladson (Source 2)
dados_gladson = {
    "Item": ["Arroz", "Feijão", "Carne", "Leite", "Farinha", "Açúcar", "Oleo", "Pão", "Café", "Ovo", "Frango", "Bolacha", "Vitamilho", "Banana", "Maça", "Tomate", "Cebola"],
    "Semana 1": [3.99, 6.39, 42.90, 3.99, 4.59, 4.49, 8.99, 8.99, 15.39, 18.00, 19.90, 3.99, 1.39, 4.00, 8.00, 4.59, 3.89],
    "Semana 2": [4.79, 6.39, 37.90, 5.29, 4.79, 4.89, 8.25, 4.99, 16.49, 13.99, 18.99, 4.39, 1.89, 3.99, 9.70, 3.99, 3.85],
    "Semana 3": [2.99, 4.69, 42.89, 4.05, 4.59, 4.49, 7.99, 8.99, 14.99, 17.99, 18.99, 3.99, 1.29, 4.00, 11.25, 4.29, 3.79],
    "Semana 4": [4.35, 6.99, 42.99, 5.20, 4.89, 4.89, 9.25, 7.99, 15.89, 19.90, 21.99, 5.25, 2.39, 5.09, 0.00, 5.29, 4.99]
}

pd.DataFrame(dados_igor).to_csv("tabela_igor.csv", index=False)
pd.DataFrame(dados_gladson).to_csv("tabela_gladson.csv", index=False)
print("Arquivos CSV criados com sucesso!")


# Dados do IBGE
dados_ibge = {
    "Municipio": [
        "Acari", "Açu", "Afonso Bezerra", "Alexandria", "Alto do Rodrigues", 
        "Caicó", "Currais Novos", "Guamaré", "Mossoró", "Natal", 
        "Parnamirim", "Pau dos Ferros", "Santa Cruz", "São Gonçalo do Amarante",
        "São José de Mipibu", "Tangará", "Touros"
    ],
    "PIB_Per_Capita": [
        12785.32, 24982.91, 12542.16, 11145.72, 41300.47, 
        20295.80, 17863.07, 125585.40, 26570.03, 26972.28, 
        25121.67, 23028.80, 15382.76, 18157.09, 
        23357.80, 12505.26, 24167.89
    ],
    "Salario_Medio": [
        1.4, 1.8, 1.7, 1.4, 2.1, 1.7, 1.7, 3.0, 2.2, 3.0, 
        1.7, 1.7, 1.7, 1.8, 1.7, 1.9, 1.9
    ],
    "Comprometimento_Renda": [
        7.85, 6.11, 6.46, 7.85, 5.23, 8.46, 6.46, 3.66, 5.00, 3.66, 
        6.46, 6.46, 6.46, 6.11, 6.46, 5.78, 5.78
    ]
}

df_ibge = pd.DataFrame(dados_ibge)
df_ibge["Custo_Cesta"] = 165.83 # Valor fixo conforme o documento
df_ibge.to_csv("tabela_ibge.csv", index=False)
print("Base IBGE atualizada!")
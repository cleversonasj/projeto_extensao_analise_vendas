import pandas as pd
import plotly.express as px
from format_brl import format_brl

# Carregar a planilha de vendas.
file_path = './assets/rel_vendas_por_itens.xlsx'
df = pd.read_excel(file_path)

# Como essas colunas podem ter dados com valores nulos, fiz o preenchiemento com o valor 0.
df['Preço custo'] = df['Preço custo'].fillna(0)
df['Total custo'] = df['Total custo'].fillna(0)
df['Desconto'] = df['Desconto'].fillna(0)
df['Acréscimo'] = df['Acréscimo'].fillna(0)

# Busca por todas as colunas que possuem valores númericos para converter em números.
cols_to_convert = ['Preço custo', 'Preço venda', 'Quantidade', 'Total custo', 'Desconto', 'Acréscimo', 
                   'Líquido item', 'Bruto item', 'Lucro', 'Total Venda']
df[cols_to_convert] = df[cols_to_convert].apply(pd.to_numeric, errors='coerce')

# Convertendo a coluna 'Data' para datetime e extraindo apenas a parte da data (sem horário).
df['Data'] = pd.to_datetime(df['Data'], errors='coerce')
df['Data'] = df['Data'].dt.date

# Produtos mais vendidos.
quantidade_vendida_total = df.groupby(['Código', 'Descrição'])['Quantidade'].sum().sort_values(ascending=False).head(10).reset_index()
quantidade_vendida_total['Rótulo'] = quantidade_vendida_total['Código'].astype(str) + ' - ' + quantidade_vendida_total['Descrição']
fig_produtos_vendidos = px.pie(
    quantidade_vendida_total,
    names='Rótulo', 
    values='Quantidade',
    title='Produtos Mais Vendidos',
    labels={'Rótulo': 'Produto', 'Quantidade': 'Quantidade Vendida'},
    hole=0.3
)

# Produtos com o menor valor de custo.
produtos_menor_custo = df[df['Preço custo'] > 0].groupby(['Código', 'Descrição']).agg({'Preço custo': 'min'}).nsmallest(5, 'Preço custo').reset_index()
produtos_menor_custo['Rótulo'] = produtos_menor_custo['Código'].astype(str) + ' - ' + produtos_menor_custo['Descrição']
fig_menor_custo = px.pie(
    produtos_menor_custo,
    names='Rótulo',
    values='Preço custo',
    title='Produtos com o Menor Valor de Custo',
    labels={'Rótulo': 'Produto', 'Preço custo': 'Preço Custo'},
    hole=0.3
)

# Produtos com o maior valor de lucro.
produtos_maior_lucro = df[df['Preço custo'] > 0].groupby(['Código', 'Descrição']).agg({'Lucro': 'max'}).nlargest(5, 'Lucro').reset_index()
produtos_maior_lucro['Rótulo'] = produtos_maior_lucro['Código'].astype(str) + ' - ' + produtos_maior_lucro['Descrição']
fig_maior_lucro = px.bar(
    produtos_maior_lucro,
    x='Rótulo',
    y='Lucro',
    title='Produtos com o Maior Valor de Lucro',
    labels={'Rótulo': 'Produto', 'Lucro': 'Lucro'},
    text='Lucro'
)

# Quantidade vendida por item.
quantidade_vendida_por_item = df.groupby(['Código', 'Descrição'])['Quantidade'].sum().reset_index()
quantidade_vendida_por_item['Rótulo'] = quantidade_vendida_por_item['Código'].astype(str) + ' - ' + quantidade_vendida_por_item['Descrição']
fig_quantidade_vendida = px.scatter(
    quantidade_vendida_por_item,
    x='Rótulo', 
    y='Quantidade',
    title='Quantidade Vendida por Item',
    labels={'Rótulo': 'Produto', 'Quantidade': 'Quantidade Vendida'},
)

# Produtos com o maior custo de venda.
produtos_maior_custo_venda = df.groupby(['Código', 'Descrição']).agg({'Preço venda': 'max'}).nlargest(5, 'Preço venda').reset_index()
produtos_maior_custo_venda['Rótulo'] = produtos_maior_custo_venda['Código'].astype(str) + ' - ' + produtos_maior_custo_venda['Descrição']
fig_maior_custo_venda = px.scatter(
    produtos_maior_custo_venda,
    x='Rótulo', 
    y='Preço venda',
    title='Produtos com o Maior Custo de Venda',
    labels={'Rótulo': 'Produto', 'Preço venda': 'Preço Venda'},
)

# Busca dos valores de descontos e acréscimos.
total_desconto = df['Desconto'].sum()
maior_desconto = df['Desconto'].max()
menor_desconto = df[df['Desconto'] > 0]['Desconto'].min()
total_acrescimo = df['Acréscimo'].sum()
maior_acrescimo = df['Acréscimo'].max()
menor_acrescimo = df[df['Acréscimo'] > 0]['Acréscimo'].min()
total_quantidade_vendida = int(df['Quantidade'].sum())

menor_acrescimo = 0 if pd.isna(menor_acrescimo) else menor_acrescimo
menor_desconto = 0 if pd.isna(menor_desconto) else menor_desconto

# DataFrame para o relatório com a quantidade de itens vendidos.
relatorio_financeiro = pd.DataFrame({
    'Métrica': ['Total de Desconto', 'Maior Desconto', 'Menor Desconto',  'Total de Acréscimo',
                'Maior Acréscimo', 'Menor Acréscimo', 'Total de Itens Vendidos'],
    '(R$)': [format_brl(total_desconto), format_brl(maior_desconto), 
                format_brl(menor_desconto), format_brl(total_acrescimo),
                format_brl(maior_acrescimo), format_brl(menor_acrescimo),
                total_quantidade_vendida]
})

# Exibindo o relatório financeiro.
print("-------------------------------")
print("Relatório Financeiro")
print("-------------------------------")
print(relatorio_financeiro.to_string(index=False, formatters={'R$': format_brl}))
print("-------------------------------")

# Valor total das vendas.
df['Valor Total Venda'] = df.groupby('Nº venda')['Total Venda'].transform('max')
vendas_valor_total = df.drop_duplicates(subset='Nº venda').groupby('Nº venda')['Valor Total Venda'].sum()
vendas_maior_valor = vendas_valor_total.nlargest(5)
fig_maior_valor_vendas = px.scatter(
    vendas_maior_valor.reset_index(),
    x='Nº venda', 
    y='Valor Total Venda',
    title='Vendas com o Maior Valor Total',
    labels={'Nº venda': 'Número da Venda', 'Valor Total Venda': 'Total Venda'}
)

# Quantidade de vendas realizadas por data.
vendas_por_data = df.groupby('Data')['Nº venda'].nunique()
fig_datas_vendas = px.line(
    vendas_por_data.reset_index(),
    x='Data', 
    y='Nº venda',
    title='Distribuição das Vendas por Data',
    labels={'Data': 'Data', 'Nº venda': 'Número de Vendas'}
)

# Quantidade de vendas realizadas por cada vendedor.
vendas_por_vendedor = df.groupby('Vendedor')['Nº venda'].nunique().reset_index()
fig_vendas_por_vendedor = px.pie(
    vendas_por_vendedor,
    names='Vendedor',
    values='Nº venda',
    title='Quantidade de Vendas por Vendedor',
    labels={'Vendedor': 'Vendedor', 'Nº venda': 'Número de Vendas'},
    hole=0.3
)

# Formas de pagamento.
formas_pagamento_por_venda = df.drop_duplicates(subset='Nº venda')[['Forma de Pagamento']].value_counts().reset_index()
formas_pagamento_por_venda.columns = ['Forma de Pagamento', 'Número de Vendas']
fig_formas_pagamento = px.pie(
    formas_pagamento_por_venda,
    names='Forma de Pagamento',
    values='Número de Vendas',
    title='Formas de Pagamento Utilizadas',
    labels={'Forma de Pagamento': 'Forma de Pagamento', 'Número de Vendas': 'Número de Vendas'},
    hole=0.3
)

# Exibir os gráficos.
fig_produtos_vendidos.show()
fig_menor_custo.show()
fig_maior_lucro.show()
fig_quantidade_vendida.show()
fig_maior_custo_venda.show()
fig_maior_valor_vendas.show()
fig_datas_vendas.show()
fig_vendas_por_vendedor.show()
fig_formas_pagamento.show()
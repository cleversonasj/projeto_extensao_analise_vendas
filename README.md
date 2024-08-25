# Projeto de Análise de Dados com Pandas e Plotly

Este projeto realiza análises de dados usando Python com as bibliotecas Pandas e Plotly em um Jupyter Notebook. O objetivo é analisar dados de vendas e criar visualizações interativas baseadas em uma planilha de dados para a empresa selecionada neste Projeto de Extensão.

## Requisitos

Ter o Python instalado e os seguintes pacotes: Jupyter, Pandas e Plotly.

Você pode instalar esses pacotes usando o comando:

```bash
pip install pandas plotly jupyter
```

## Estrutura do Projeto

O projeto possui a seguinte estrutura:

- **main.py**: O script principal que carrega a planilha, realiza as análises e gera as visualizações. 

- **assets/rel_vendas_por_itens.xlsx**: Planilha de exemplo no formato esperado. Esta planilha contém os dados que serão analisados. Para usar outra planilha, certifique-se de que ela tenha o mesmo formato, esteja dentro da pasta 'assets' e altere no arquivo 'main.py' o nome da planilha incluindo a extensão.

## Executando o Script no Jupyter Notebook

Para rodar o script `main.py` no Jupyter Notebook, siga estes passos:

1. **Abrir o Jupyter Notebook**: Inicie o Jupyter Notebook na pasta do projeto com o comando:

    ```bash
    jupyter notebook
    ```

    Isso abrirá a interface do Jupyter Notebook no seu navegador.

2. **Navegar até o Diretório**: No Jupyter Notebook, navegue até o diretório onde o projeto está localizado. Você pode criar um novo notebook ou abrir um existente.

3. **Executar o Script**: Clique em "File" > "New" > "Console" > Use "Python 3" ao Selecionar o Kernel.

    No console use o comando:

    `%run main.py` e pressione "Shift" + "Enter" para executar o comando.

4. **Verificar Saídas e Visualizações**: Após a execução, os resultados das análises e os gráficos gerados serão exibidos diretamente no Jupyter Notebook.


#### Desenvolvido por Cleverson Alves da Silva Junior.

# Trabalho-Prático-1-PAA
# 📊 Projeto: Análise Experimental do Quicksort

## 🎯 Objetivo
O objetivo deste trabalho é realizar um **estudo comparativo de diversas implementações do algoritmo Quicksort**.  

Foram implementadas três versões do algoritmo:
1. **Quicksort recursivo**: implementação padrão utilizando partição de Lomuto.
2. **Quicksort híbrido**: versão recursiva em que a partição é interrompida para sub-vetores com menos de `M` elementos, que são ordenados com Insertion Sort. O valor de `M` é determinado empiricamente através de experimentos com vetores de 1000 elementos aleatórios.
3. **Quicksort híbrido com mediana-de-três**: melhoria da versão híbrida utilizando a técnica de mediana-de-três para escolha do pivô, reduzindo a chance de casos degenerados.

---

## 🧪 Testes Realizados
Para comparar os algoritmos, foram geradas diferentes **massas de teste**:
- Vetores **aleatórios**.
- Vetores **ordenados**.
- Vetores **ordenados de forma inversa**.
- Vetores com **muitos elementos repetidos**.
- Vetores que **forçam explicitamente o pior caso do Quicksort** (vetores ordenados crescentes para partição de Lomuto).

Cada teste foi executado **várias vezes** para obter resultados consistentes, registrando **tempo médio de execução, número médio de comparações e número médio de trocas**.

---

## 📄 Relatório
O relatório foi produzido em **LaTeX (via Overleaf)** e contém:
- **Introdução**: contextualização do trabalho, importância do tema e objetivos.
- **Referencial Teórico**: explicação sobre algoritmos de ordenação, com foco em Insertion Sort e Quicksort, análise de complexidade e discussão sobre o pior caso do Quicksort, incluindo referências clássicas e recentes.
- **Metodologia**: descrição detalhada dos experimentos, tamanhos e tipos de vetores utilizados, além da busca empírica do parâmetro `M`.
- **Resultados e Análises**: tabelas e gráficos comparando desempenho, incluindo análise crítica sobre o impacto do parâmetro `M`.
- **Conclusão**: principais achados do estudo.
- **Referências Bibliográficas**: autores clássicos e artigos recentes.

---

## ⚙️ Implementação

### Requisitos
- Python 3.9+
- Dependências: `pandas`, `matplotlib`

Instalação das dependências:
```bash
pip install pandas matplotlib

Estrutura do Projeto
quicksort-project/
├── src/                     
│   ├── quicksort.py         # Implementações do Quicksort
│   ├── utils.py             # Funções auxiliares (contadores, geradores, swaps)
│   └── experiments.py       # Execução dos experimentos
├── main.py                  # Script principal
├── results/                 # CSVs e gráficos gerados
├── docs/                    # Relatório (PDF exportado do Overleaf)
├── requirements.txt         # Dependências
└── README.md                # Este documento

Referências

Cormen, T. H.; Leiserson, C. E.; Rivest, R. L.; Stein, C. Algoritmos: Teoria e Prática. 3ª ed. Elsevier, 2012.

Sedgewick, R.; Wayne, K. Algorithms. 4ª ed. Addison-Wesley, 2011.

Hoare, C. A. R. (1962). Quicksort. The Computer Journal, 5(1), 10–16.

Weiss, M. A. Data Structures and Algorithm Analysis in C++. 4ª ed. Pearson, 2014.
👨‍💻 Autor

Fábio Wnuk Hollerbach Klier
Engenharia da Computação – PUC Minas (2025)

# Trabalho-Prático-1-PAA
# 📊 Projeto: Análise Experimental do Quicksort  

## 🎯 Objetivo  
O objetivo deste trabalho é realizar um **estudo comparativo de diversas implementações do algoritmo Quicksort**.  

As versões implementadas foram:  
- **(a) Quicksort recursivo**: implementação padrão utilizando partição de Lomuto.  
- **(b) Quicksort híbrido**: versão recursiva em que a partição é interrompida para sub-vetores com menos de `M` elementos, que são ordenados com Insertion Sort. O valor de `M` é determinado **empiricamente** por meio de experimentos com vetores de 1000 elementos aleatórios.  
- **(c) Quicksort híbrido com mediana-de-três**: melhoria da versão híbrida utilizando a técnica de mediana-de-três para escolha do pivô, reduzindo os casos degenerados.  

---

## 🧪 Testes Realizados  
Foram geradas diferentes **massas de teste** para comparar os algoritmos:  
- Vetores **aleatórios**.  
- Vetores **já ordenados**.  
- Vetores **ordenados de forma inversa**.  
- Vetores com **muitos elementos repetidos**.  
- Vetores que **forçam explicitamente o pior caso do Quicksort** (ordenados crescentes para partição de Lomuto).  

Cada teste foi executado **várias vezes** para obter resultados consistentes, registrando **tempo médio de execução, número médio de comparações e número médio de trocas**.  

---

## 📄 Relatório (Overleaf)  
O relatório foi desenvolvido em **LaTeX (via Overleaf)** e contém:  
1. **Introdução** – contextualização do trabalho, importância do tema e objetivos.  
2. **Referencial Teórico** – explicação sobre algoritmos de ordenação, com foco em Insertion Sort e Quicksort, análise de complexidade e discussão sobre o pior caso do Quicksort.  
3. **Metodologia** – descrição dos experimentos, tamanhos e tipos de vetores utilizados, além da busca empírica do parâmetro `M`.  
4. **Resultados e Análises** – tabelas e gráficos comparando desempenho, incluindo análise crítica sobre o impacto do parâmetro `M`.  
5. **Conclusão** – principais achados do estudo.  
6. **Referências Bibliográficas** – autores clássicos e artigos recentes.  

---

## ⚙️ Implementação  

### Requisitos
- Python 3.9+  
- Dependências listadas em `requirements.txt`  

Instalação das dependências:  
```bash
pip install -r requirements.txt

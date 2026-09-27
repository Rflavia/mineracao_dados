# Mineração de Dados Eleitorais 2026 — Grupo 3

Projeto desenvolvido na disciplina de **Mineração de Dados**, utilizando dados públicos do TSE referentes às Eleições 2026.

## 📌 Recorte do grupo

**Cargo:** Deputado Federal
**Região:** Sul
**Estados:** Paraná (PR), Rio Grande do Sul (RS) e Santa Catarina (SC)


## 🎯 Objetivo

Identificar os perfis dos 1.117 candidatos a Deputado Federal no Sul nas Eleições 2026 a partir de quatro variáveis — **idade, anos de estudo, patrimônio declarado e gasto de campanha** —, entender o que caracteriza cada perfil (regras de associação) e quem foge do padrão da base e do próprio grupo (detecção de anomalias).

## 📓 Notebooks

| Notebook | Conteúdo |
|---|---|
| `00_preparacao_dados` | Leitura e junção das bases do TSE (candidatos e bens) |
| `01_analise_descritiva` | Análise descritiva, incluindo as 4 variáveis do projeto |
| `02_clusterizacao` | K-Means e Bisecting K-Means com 3 variáveis (versão exploratória) |
| `02_clusterizacao_com_despesa` | Gasto de campanha, faixas por quartil e o **Bisecting K-Means oficial com as 4 variáveis (k=4)** |
| `03_regras_associacao` | Apriori com as faixas por quartil e o cluster no antecedente e no consequente |
| `04_deteccao_anomalias` | Isolation Forest global e por cluster, e as conclusões do grupo |

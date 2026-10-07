# Mineração de Dados Eleitorais 2026 — Grupo 3

Projeto desenvolvido na disciplina de **Aprendizagem de máquina não supervisionado**, da Pós-graduação em Data Science e Inteligência Artificial do SENAC DF. 

Nesse projeto foram utilizados dados públicos disponíveis nos portais do TSE referentes às Eleições 2026.

## Alunos
[![GitHub](https://badgen.net/badge/GitHub/Rflavia/black?icon=github)](https://github.com/Rflavia) 
[![GitHub](https://badgen.net/badge/GitHub/clara_cecilia/black?icon=github)](https://github.com/clara-cecilia) 
[![GitHub](https://badgen.net/badge/GitHub/itagibanetos/black?icon=github)](https://github.com/itagibanetos) 
[![GitHub](https://badgen.net/badge/GitHub/presley-rocha/black?icon=github)](https://github.com/presley-rocha) 
[![GitHub](https://badgen.net/badge/GitHub/theminas/black?icon=github)](https://github.com/theminas)

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
| `05_eleicoes` | Analise exploratoria sobre os resultados das eleições por perfil |

##  📊​ Infográfico | Raio X dos candidatos a Deputado Federal em 2026 na região Sul

<img width="2752" height="1536" alt="Raio-X Candidatos Sul Eleições 2026" src="https://github.com/user-attachments/assets/4b547635-0fa6-4b9d-9a5f-cf9f25676377" />


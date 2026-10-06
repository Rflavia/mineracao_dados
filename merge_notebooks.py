#!/usr/bin/env python3
"""
Junta os notebooks do projeto, na ordem, em um único arquivo .ipynb.

Uso (na pasta do projeto, onde estão os notebooks):

    python merge_notebooks.py

Opções úteis:

    python merge_notebooks.py --pasta caminho/da/pasta
    python merge_notebooks.py --saida meu_notebook_unico.ipynb
    python merge_notebooks.py --limpar-outputs        # arquivo bem menor, sem gráficos/saídas
    python merge_notebooks.py --sem-indice            # não cria o índice no topo
    python merge_notebooks.py --ignorar-ausentes      # pula notebooks que não existirem

Para mudar a ordem, incluir ou tirar notebooks, edite a lista NOTEBOOKS abaixo.

O script usa só a biblioteca padrão do Python (não precisa instalar nada).
"""

import argparse
import json
import re
import sys
import uuid
from pathlib import Path

# ---------------------------------------------------------------------------
# Ordem dos notebooks: (arquivo, título que aparece no índice e no cabeçalho)
# Para deixar um notebook de fora, apague ou comente a linha dele.
# ---------------------------------------------------------------------------
NOTEBOOKS = [
    ("00_preparacao_dados.ipynb", "Preparação de dados"),
    ("01_analise_descritiva.ipynb", "Análise descritiva"),
    ("02_clusterizacao.ipynb", "Clusterização exploratória (K-Means e Bisecting, 3 variáveis)"),
    ("02_clusterizacao_com_despesa.ipynb", "Clusterização com gasto de campanha (resultado oficial)"),
    ("03_regras_associacao.ipynb", "Regras de associação"),
    ("04_deteccao_anomalias.ipynb", "Detecção de anomalias"),
    ("05_eleitos.ipynb", "Resultado nas urnas × clusters"),
]

TITULO_GERAL = "Mineração de Dados Eleitorais 2026 — notebook único"

# Cada notebook costuma abrir com um selo "Open in Colab" que aponta para ele mesmo;
# no arquivo único esses selos ficam sem sentido, então são removidos.
REMOVER_SELO_COLAB = True


def ler_notebook(caminho: Path) -> dict:
    with open(caminho, encoding="utf-8") as f:
        nb = json.load(f)
    if nb.get("nbformat") != 4:
        raise ValueError(f"{caminho.name}: só há suporte para nbformat 4 (encontrado: {nb.get('nbformat')}).")
    return nb


def texto(fonte) -> str:
    """O campo 'source' de uma célula pode ser texto ou lista de linhas."""
    return "".join(fonte) if isinstance(fonte, list) else fonte


def eh_selo_colab(celula: dict) -> bool:
    return (
        celula.get("cell_type") == "markdown"
        and "colab.research.google.com/assets/colab-badge" in texto(celula.get("source", ""))
    )


def limpar_outputs(celula: dict) -> None:
    if celula.get("cell_type") == "code":
        celula["outputs"] = []
        celula["execution_count"] = None


def novo_id(usados: set) -> str:
    while True:
        cid = uuid.uuid4().hex[:8]
        if cid not in usados:
            usados.add(cid)
            return cid


def ancora(indice: int, arquivo: str) -> str:
    base = re.sub(r"[^a-z0-9]+", "-", Path(arquivo).stem.lower()).strip("-")
    return f"parte-{base}"


def celula_markdown(conteudo: str) -> dict:
    return {"cell_type": "markdown", "metadata": {}, "source": conteudo}


def montar_indice(itens) -> dict:
    linhas = [f"# {TITULO_GERAL}", "",
              "Junção, na ordem, dos notebooks do projeto. Cada parte abaixo corresponde a um notebook original.", "",
              "## Índice", ""]
    for i, (arquivo, titulo, ancora_id) in enumerate(itens, start=1):
        linhas.append(f"{i}. [{titulo}](#{ancora_id}) — `{arquivo}`")
    return celula_markdown("\n".join(linhas))


def montar_cabecalho(arquivo: str, titulo: str, ancora_id: str) -> dict:
    return celula_markdown(
        f'<a id="{ancora_id}"></a>\n\n---\n\n# {titulo}\n\n'
        f"> Origem: `{arquivo}`"
    )


def nome_saida_padrao(arquivos) -> str:
    """Ex.: 00_05_notebook_unico.ipynb (usa o prefixo numérico do primeiro e do último arquivo)."""
    def prefixo(nome):
        m = re.match(r"(\d+)", nome)
        return m.group(1) if m else None

    p0, p1 = prefixo(arquivos[0]), prefixo(arquivos[-1])
    if p0 and p1:
        return f"{p0}_{p1}_notebook_unico.ipynb"
    return "notebook_unico.ipynb"


def mesclar(pasta: Path, saida: Path, limpar: bool, com_indice: bool, ignorar_ausentes: bool) -> None:
    existentes, ausentes = [], []
    for arquivo, titulo in NOTEBOOKS:
        (existentes if (pasta / arquivo).exists() else ausentes).append((arquivo, titulo))

    if ausentes and not ignorar_ausentes:
        print("Não encontrei estes notebooks em", pasta.resolve(), file=sys.stderr)
        for arquivo, _ in ausentes:
            print(f"  - {arquivo}", file=sys.stderr)
        print("\nCorrija o caminho (--pasta), ajuste a lista NOTEBOOKS ou use --ignorar-ausentes.", file=sys.stderr)
        sys.exit(1)
    if not existentes:
        print("Nenhum notebook encontrado.", file=sys.stderr)
        sys.exit(1)

    itens = [(arq, tit, ancora(i, arq)) for i, (arq, tit) in enumerate(existentes)]

    celulas = []
    if com_indice:
        celulas.append(montar_indice(itens))

    metadata = None
    minor = 0
    resumo = []

    for (arquivo, titulo, ancora_id) in itens:
        nb = ler_notebook(pasta / arquivo)
        if metadata is None:
            metadata = nb.get("metadata", {})        # kernel e linguagem do primeiro notebook
        minor = max(minor, nb.get("nbformat_minor", 0))

        celulas.append(montar_cabecalho(arquivo, titulo, ancora_id))

        usadas = 0
        for celula in nb["cells"]:
            if REMOVER_SELO_COLAB and eh_selo_colab(celula):
                continue
            if limpar:
                limpar_outputs(celula)
            celulas.append(celula)
            usadas += 1
        resumo.append((arquivo, usadas))

    # A partir do nbformat 4.5 cada célula precisa de um id único no arquivo inteiro.
    # Como cada notebook tinha seus próprios ids, geramos ids novos para evitar colisões.
    if minor >= 5:
        usados = set()
        for c in celulas:
            c["id"] = novo_id(usados)
    else:
        for c in celulas:
            c.pop("id", None)

    resultado = {
        "cells": celulas,
        "metadata": metadata or {},
        "nbformat": 4,
        "nbformat_minor": minor,
    }

    with open(saida, "w", encoding="utf-8") as f:
        json.dump(resultado, f, ensure_ascii=False, indent=1)
        f.write("\n")

    print(f"Notebook único salvo em: {saida}")
    print("-" * 60)
    for arquivo, n in resumo:
        print(f"  {arquivo:<42} {n:>4} células")
    extras = len(celulas) - sum(n for _, n in resumo)
    print("-" * 60)
    print(f"  {'cabeçalhos' + (' + índice' if com_indice else ''):<42} {extras:>4} células")
    print(f"  {'TOTAL':<42} {len(celulas):>4} células")
    if ausentes:
        print("\nIgnorados (não encontrados):", ", ".join(a for a, _ in ausentes))
    if limpar:
        print("\nOutputs removidos (--limpar-outputs): rode o notebook para gerá-los de novo.")


def main() -> None:
    parser = argparse.ArgumentParser(description="Junta os notebooks do projeto em um único .ipynb")
    parser.add_argument("--pasta", default=".", help="pasta onde estão os notebooks (padrão: pasta atual)")
    parser.add_argument("--saida", default=None, help="arquivo de saída (padrão: ex. 00_05_notebook_unico.ipynb)")
    parser.add_argument("--limpar-outputs", action="store_true", help="remove as saídas e gráficos das células")
    parser.add_argument("--sem-indice", action="store_true", help="não cria o índice no início")
    parser.add_argument("--ignorar-ausentes", action="store_true", help="pula notebooks que não existirem")
    args = parser.parse_args()

    pasta = Path(args.pasta)
    saida = Path(args.saida) if args.saida else pasta / nome_saida_padrao([a for a, _ in NOTEBOOKS])

    mesclar(pasta, saida, limpar=False, com_indice=not args.sem_indice, ignorar_ausentes=args.ignorar_ausentes)


if __name__ == "__main__":
    main()

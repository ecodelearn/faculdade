#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para organizar automaticamente arquivos baixados do portal do aluno
(localizados em ~/Downloads) e movê-los para as pastas corretas de cada aula.
Utiliza o mapeamento exato do HTML extraído da faculdade.
"""

import os
import re
import sys
import shutil
from pathlib import Path

# Adiciona o diretório do script ao sys.path
SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.append(str(SCRIPT_DIR))

from gerar_estrutura import parse_html_aluno

BASE_DIR = SCRIPT_DIR / "Modelagem e Segurança da Informação"
HTML_FILE = SCRIPT_DIR / "inner-html-box-aluno.html"
DOWNLOADS_DIR = Path.home() / "Downloads"

def norm(s: str) -> str:
    """Normaliza texto removendo acentos e caracteres especiais para comparação flexível."""
    s = s.lower()
    s = re.sub(r'[àáâãä]', 'a', s)
    s = re.sub(r'[èéêë]', 'e', s)
    s = re.sub(r'[ìíîï]', 'i', s)
    s = re.sub(r'[òóôõö]', 'o', s)
    s = re.sub(r'[ùúûü]', 'u', s)
    s = re.sub(r'[ç]', 'c', s)
    s = re.sub(r'[^a-z0-9]', '', s)
    return s

def construir_mapeamento_completo():
    """Constrói um dicionário com base no HTML ligando cada título de aula, PDF e vídeo à sua pasta."""
    dados = parse_html_aluno(str(HTML_FILE))
    mapping = {}

    for disc in dados['disciplinas']:
        disc_folder = BASE_DIR / disc['pasta']
        for ua in disc['unidades']:
            ua_folder = disc_folder / ua['pasta_ua'] if ua['pasta_ua'] else disc_folder
            for aula in ua['aulas']:
                aula_folder = ua_folder / aula['pasta_aula']
                
                # Mapeia título da aula
                mapping[norm(aula['titulo_original'])] = aula_folder
                
                # Mapeia todos os títulos de PDFs vinculados à aula
                for p in aula['pdfs']:
                    mapping[norm(p)] = aula_folder
                    
                # Mapeia todos os títulos de blocos de vídeo
                for v in aula['videos']:
                    mapping[norm(v['titulo'])] = aula_folder

    return mapping

def organizar():
    if not DOWNLOADS_DIR.exists():
        print(f"Diretório de Downloads não encontrado: {DOWNLOADS_DIR}")
        return

    print("Construindo mapeamento com base no plano de aulas...")
    mapping = construir_mapeamento_completo()
    print(f"Total de chaves mapeadas: {len(mapping)}")
    print(f"Varrendo arquivos em: {DOWNLOADS_DIR} ...\n")

    arquivos_movidos = 0
    nao_identificados = []

    for arquivo in sorted(DOWNLOADS_DIR.iterdir()):
        if not arquivo.is_file():
            continue

        nome = arquivo.name
        # Filtrar apenas arquivos acadêmicos do portal
        if not any(nome.startswith(p) for p in ['Legenda', 'Slide', 'Apostila', 'Aula PDF', 'Audioaula', 'Anotações']):
            continue

        # Limpar prefixos e extensão para buscar no mapa
        clean_name = nome
        for prefix in ['Legenda - ', 'Slide - ', 'Apostila - ', 'Aula PDF - ', 'Audioaula - ', 'Anotações - ']:
            if clean_name.startswith(prefix):
                clean_name = clean_name[len(prefix):]
                break

        # Remove sufixos numéricos de duplicatas (ex: "-1.pdf") e extensão
        clean_name = re.sub(r'-\d+\.[a-zA-Z0-9]+$', '', clean_name)
        clean_name = re.sub(r'\.[a-zA-Z0-9]+$', '', clean_name)
        clean_norm = norm(clean_name)

        # 1. Correspondência direta no dicionário
        target_folder = mapping.get(clean_norm)

        # 2. Correspondência por melhor substring se não for exata
        if not target_folder:
            best_score = 0
            for k, folder in mapping.items():
                if k in clean_norm or clean_norm in k:
                    score = len(k)
                    if score > best_score:
                        best_score = score
                        target_folder = folder

        if target_folder:
            target_folder.mkdir(parents=True, exist_ok=True)
            destino = target_folder / nome
            print(f"[MOVIDO] {nome} \n   ↳ Para: {target_folder.relative_to(BASE_DIR)}\n")
            shutil.move(str(arquivo), str(destino))
            arquivos_movidos += 1
        else:
            nao_identificados.append(nome)

    print(f"==================================================")
    print(f"✅ Total de arquivos organizados com sucesso: {arquivos_movidos}")
    if nao_identificados:
        print(f"⚠️ Arquivos não identificados ({len(nao_identificados)}):")
        for f in nao_identificados:
            print(f"   - {f}")
    print(f"==================================================")

if __name__ == '__main__':
    organizar()

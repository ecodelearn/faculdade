#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para converter todas as legendas (.srt) em arquivos de texto (.txt)
limpos e contínuos, otimizados para consumo no NotebookLM e Gemini.
Também gera um arquivo consolidado de transcrição completa por aula.
"""

import os
import re
from pathlib import Path

BASE_DIR = Path("/home/ecode/projects/faculdade/3o-periodo/Modelagem e Segurança da Informação")

def srt_para_texto_limpo(srt_content: str) -> str:
    """Remove numerações de linhas e timestamps do SRT, retornando texto contínuo e fluído."""
    lines = srt_content.splitlines()
    text_lines = []
    for line in lines:
        line = line.strip()
        if not line or line.isdigit() or '-->' in line:
            continue
        text_lines.append(line)

    # Junta linhas preservando espaçamento e pontuação natural
    clean_text = ' '.join(text_lines)
    clean_text = re.sub(r'\s+', ' ', clean_text).strip()
    clean_text = re.sub(r' ([.,!?;:])', r'\1', clean_text)
    return clean_text

def converter_todas_legendas():
    print(f"Buscando arquivos .srt em: {BASE_DIR} ...")
    
    total_convertidos = 0
    total_aulas_consolidadas = 0

    for root, dirs, files in os.walk(BASE_DIR):
        r_path = Path(root)
        if not r_path.name.startswith("Aula "):
            continue

        srt_files = sorted([f for f in files if f.endswith(".srt")])
        if not srt_files:
            continue

        transcricoes_aula = []

        for srt_name in srt_files:
            srt_path = r_path / srt_name
            conteudo_srt = srt_path.read_text(encoding='utf-8', errors='ignore')
            texto_limpo = srt_para_texto_limpo(conteudo_srt)

            # 1. Cria a versão .txt direta (com o nome Legenda - *.txt)
            txt_legenda_name = srt_name.replace(".srt", ".txt")
            txt_legenda_path = r_path / txt_legenda_name
            txt_legenda_path.write_text(texto_limpo, encoding='utf-8')

            # 2. Cria a versão Transcrição - *.txt
            transcricao_name = srt_name.replace("Legenda - ", "Transcrição - ").replace(".srt", ".txt")
            transcricao_path = r_path / transcricao_name
            transcricao_path.write_text(texto_limpo, encoding='utf-8')

            total_convertidos += 1
            
            # Guarda para o consolidado da aula
            parte_titulo = srt_name.replace("Legenda - ", "").replace(".srt", "")
            transcricoes_aula.append((parte_titulo, texto_limpo))

        # 3. Gerar Transcrição Completa da Aula (se houver múltiplas partes ou aula)
        aula_titulo = r_path.name.split(" - ", 1)[-1]
        consolidado_name = f"Transcrição Completa - {aula_titulo}.txt"
        consolidado_path = r_path / consolidado_name

        texto_consolidado = f"# Transcrição Completa da Aula: {aula_titulo}\n\n"
        for parte_nome, txt_parte in transcricoes_aula:
            texto_consolidado += f"## 🎬 Bloco: {parte_nome}\n\n{txt_parte}\n\n---\n\n"

        consolidado_path.write_text(texto_consolidado, encoding='utf-8')
        total_aulas_consolidadas += 1

    print(f"==================================================")
    print(f"✅ Total de legendas convertidas em .txt limpos: {total_convertidos}")
    print(f"✅ Total de Transcrições Completas por Aula: {total_aulas_consolidadas}")
    print(f"==================================================")

if __name__ == '__main__':
    converter_todas_legendas()

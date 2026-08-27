#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Agente Automatizado de Resumos e Quizzes Acadêmicos (Gran Faculdade)
Utiliza a API do Gemini para ler os materiais locais (Apostilas e Transcrições)
e gerar resumos padronizados para a área de anotações do portal do aluno.
"""

import os
import re
import sys
import json
import time
import argparse
import subprocess
import urllib.request
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent / "Modelagem e Segurança da Informação"

SYSTEM_PROMPT = """Atue como o 'Estudo Gran Resumo de Aulas', um assistente educacional especializado em transformar conteúdos brutos de graduação em materiais de estudo estruturados e auxiliar na resolução de exercícios baseados estritamente no conteúdo fornecido.

Objetivos e Metas:
* Produzir resumos detalhados e checklists de aprendizagem a partir de materiais de aula (PDFs, transcrições, slides).
* Resolver questões de múltipla escolha (quizzes) fundamentando as respostas exclusivamente no conteúdo estudado.
* Garantir a compreensão da lógica por trás das respostas através de análises técnicas e debates simulados.

Comportamentos e Regras Gerais:

1) Fidelidade ao Material:
- Utilize apenas o conteúdo fornecido. Não utilize conhecimentos externos, não invente informações e não traga exemplos que não constem no material original.
- Se o material for vago ou ambíguo, descreva apenas o que está escrito sem preencher lacunas com suposições.

2) Idioma e Terminologia:
- Responda sempre em português.
- Preserve e utilize corretamente todos os termos técnicos presentes no material original.

3) Modos de Operação:

a) MODO RESUMO:
Formato de saída estrito:
Linha 1: Disciplina: [Nome da Disciplina]
Linha 2: Aula: [Nome da Aula]
[Linha em branco]
1. [Nome do Tópico Principal]
[Texto detalhado, estruturado porém corrido, cobrindo conceitos, definições e exemplos do material]

2. [Nome do Segundo Tópico Principal]
[Texto detalhado do segundo tópico]

3. [Nome do Terceiro Tópico Principal (se houver)]
[Texto detalhado do terceiro tópico]

Checklist de Aprendizagem:
- [Palavra-chave 1]: [1 parágrafo de justificativa conectando-a ao texto]
- [Palavra-chave 2]: [1 parágrafo de justificativa conectando-a ao texto]
- [Palavra-chave 3]: [1 parágrafo de justificativa conectando-a ao texto]

b) MODO QUIZ (Ativado quando fornecida uma Questão e Alternativas):
- Análise da questão: Explique o que é cobrado e relacione com o material. Analise individualmente cada alternativa.
- Alternativa correta: Indique claramente a opção correta.
- Debate entre especialistas: Simule 3 rodadas de diálogo entre dois especialistas. O Especialista 1 defende a resposta; o Especialista 2 questiona com base no material. Confirme o consenso após a 3ª rodada.

Tom de Voz:
* Profissional, educacional e rigoroso quanto ao uso das fontes.
* Objetivo e direto, evitando comentários irrelevantes fora do escopo do material.
"""

def carregar_env():
    """Carrega variáveis de arquivo .env se existir."""
    for p in [Path(__file__).resolve().parent / ".env", Path(__file__).resolve().parent.parent / ".env"]:
        if p.exists():
            for line in p.read_text(encoding="utf-8").splitlines():
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    k = k.strip()
                    v = v.strip().strip("'").strip('"')
                    if k and not os.environ.get(k):
                        os.environ[k] = v

def extrair_texto_pdf(pdf_path: Path) -> str:
    """Extrai texto do PDF usando pdftotext ou pypdf."""
    try:
        res = subprocess.run(['pdftotext', str(pdf_path), '-'], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
        if res.returncode == 0 and res.stdout.strip():
            return res.stdout.strip()
    except Exception:
        pass
    return ""

def chamar_gemini(prompt: str, api_key: str) -> str:
    """Chama a API oficial do Google Gemini com fallback automático entre modelos disponíveis."""
    modelos_candidatos = ["gemini-3.5-flash", "gemini-3.1-flash-lite", "gemini-3-flash-preview"]
    
    ultimo_erro = None
    for model in modelos_candidatos:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
        
        payload = {
            "contents": [
                {
                    "role": "user",
                    "parts": [{"text": prompt}]
                }
            ],
            "systemInstruction": {
                "parts": [{"text": SYSTEM_PROMPT}]
            },
            "generationConfig": {
                "temperature": 0.2,
                "maxOutputTokens": 8192
            }
        }
        
        data_bytes = json.dumps(payload).encode('utf-8')
        req = urllib.request.Request(url, data=data_bytes, headers={'Content-Type': 'application/json'})
        
        try:
            with urllib.request.urlopen(req, timeout=120) as resp:
                res_json = json.loads(resp.read().decode('utf-8'))
                candidates = res_json.get('candidates', [])
                if candidates:
                    parts = candidates[0].get('content', {}).get('parts', [])
                    if parts:
                        return parts[0].get('text', '').strip()
                return ""
        except urllib.error.HTTPError as e:
            error_body = e.read().decode('utf-8')
            ultimo_erro = f"{model} ({e.code}): {error_body}"
            # Se for 503 ou 429, tenta o próximo modelo
            if e.code in [503, 429, 404]:
                time.sleep(1)
                continue
            raise RuntimeError(f"Erro na API do Gemini: {ultimo_erro}")
        except Exception as e:
            ultimo_erro = f"{model}: {e}"
            continue

    raise RuntimeError(f"Todos os modelos falharam. Último erro: {ultimo_erro}")

def processar_aula(aula_dir: Path, api_key: str, disciplina_nome: str, sobrescrever: bool = False):
    """Lê as fontes da aula, envia para o Gemini e salva o resumo pronto para o portal."""
    aula_nome = aula_dir.name.split(" - ", 1)[-1]
    saida_portal = aula_dir / f"Anotação Portal - {aula_nome}.txt"

    if saida_portal.exists() and not sobrescrever:
        print(f"⏩ Pulando (já existe): {aula_dir.name}")
        return

    print(f"\n📖 Processando: {disciplina_nome} -> {aula_dir.name}")

    # 1. Ler Transcrição Completa
    transcricao_file = aula_dir / f"Transcrição Completa - {aula_nome}.txt"
    texto_transcricao = ""
    if transcricao_file.exists():
        texto_transcricao = transcricao_file.read_text(encoding='utf-8', errors='ignore')

    # 2. Ler PDF da Matéria / Apostila
    texto_apostila = ""
    apostilas = list(aula_dir.glob("Apostila - *.pdf")) + list(aula_dir.glob("Aula PDF - *.pdf"))
    if apostilas:
        texto_apostila = extrair_texto_pdf(apostilas[0])

    if not texto_transcricao and not texto_apostila:
        print(f"⚠️  Nenhuma fonte encontrada em: {aula_dir.name}")
        return

    # 3. Montar Prompt
    prompt_usuario = f"""Disciplina: {disciplina_nome}
Aula: {aula_nome}

--- CONTEÚDO BRUTO DAS FONTES ---

[TRANSCRIÇÃO DAS VIDEOAULAS]:
{texto_transcricao}

[LIVRO / APOSTILA DA MATÉRIA]:
{texto_apostila[:30000]}

---
Gere o Resumo no MODO RESUMO conforme suas instruções do sistema.
"""

    print("🤖 Gerando resumo com Gemini...")
    resumo_gerado = chamar_gemini(prompt_usuario, api_key)

    if not resumo_gerado:
        print("❌ Falha ao obter resposta do modelo.")
        return

    # 4. Salvar arquivo pronto para o Portal do Aluno
    saida_portal.write_text(resumo_gerado, encoding='utf-8')
    print(f"✅ Salvo para o Portal: {saida_portal.name} ({len(resumo_gerado)} caracteres)")

    # 5. Atualizar Resumo.md se existir
    resumo_md = aula_dir / f"Resumo - {aula_nome}.md"
    if resumo_md.exists():
        conteudo_antigo = resumo_md.read_text(encoding='utf-8')
        if "### 1. Visão Geral e Conceitos Fundamentais" in conteudo_antigo:
            partes = conteudo_antigo.split("### 1. Visão Geral e Conceitos Fundamentais")
            cabecalho = partes[0]
            resto = partes[1].split("## 🧠 Mapa Mental")[1] if "## 🧠 Mapa Mental" in partes[1] else ""
            novo_conteudo = f"{cabecalho}### 1. Resumo Consolidado (Gerado por IA)\n\n```text\n{resumo_gerado}\n```\n\n## 🧠 Mapa Mental{resto}"
            resumo_md.write_text(novo_conteudo, encoding='utf-8')

def main():
    carregar_env()
    
    parser = argparse.ArgumentParser(description="Agente de Estudos e Resumos para Graduação")
    parser.add_argument("--key", help="Chave da API do Google Gemini (ou configure GEMINI_API_KEY no ambiente)")
    parser.add_argument("--disciplina", help="Filtrar por nome da disciplina (ex: 'Redes')")
    parser.add_argument("--ua", help="Filtrar por número da UA (ex: '01')")
    parser.add_argument("--aula", help="Filtrar por número da aula (ex: '01')")
    parser.add_argument("--todas", action="store_true", help="Processar todas as aulas encontradas")
    parser.add_argument("--sobrescrever", action="store_true", help="Sobrescrever resumos existentes")
    parser.add_argument("--quiz", help="Texto da questão e alternativas para resolver no MODO QUIZ")
    args = parser.parse_args()

    api_key = args.key or os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        print("❌ Chave da API do Gemini não informada.")
        print("   👉 Use: python agente_resumos.py --key AIzaSy... ou configure no arquivo .env")
        print("   Obtenha sua chave gratuita em: https://aistudio.google.com")
        sys.exit(1)

    if args.quiz:
        print("🧠 Resolvendo Questão no MODO QUIZ...")
        resposta = chamar_gemini(f"Resolva a seguinte questão no MODO QUIZ:\n\n{args.quiz}", api_key)
        print("\n" + "="*60)
        print(resposta)
        print("="*60)
        return

    # Buscar aulas para processar
    aulas_encontradas = []
    for root, dirs, files in os.walk(BASE_DIR):
        r_path = Path(root)
        if r_path.name.startswith("Aula "):
            disc_nome = r_path.parents[1].name if "UA " in r_path.parent.name else r_path.parent.name
            ua_nome = r_path.parent.name if "UA " in r_path.parent.name else ""

            if args.disciplina and args.disciplina.lower() not in disc_nome.lower():
                continue
            if args.ua and args.ua not in ua_nome:
                continue
            if args.aula and not r_path.name.startswith(f"Aula {int(args.aula):02d}"):
                continue

            aulas_encontradas.append((r_path, disc_nome))

    print(f"🎯 Total de aulas selecionadas para processamento: {len(aulas_encontradas)}")
    if not aulas_encontradas:
        print("Nenhuma aula correspondeu aos filtros aplicados.")
        return

    for aula_path, disc_nome in aulas_encontradas:
        processar_aula(aula_path, api_key, disc_nome, sobrescrever=args.sobrescrever)

    print("\n🎉 Todas as aulas selecionadas foram processadas!")

if __name__ == '__main__':
    main()

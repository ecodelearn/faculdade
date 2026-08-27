#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para organizar o material da faculdade por:
Módulo / Área -> Disciplina / Matéria -> Unidade de Aprendizagem (UA) -> Aulas

Lê o HTML exportado do portal da faculdade (inner-html-box-aluno.html)
e cria toda a árvore de diretórios compatível com Linux e Google Drive,
além de arquivos template de resumo prontos para NotebookLM e Gemini.
"""

import os
import re
import sys
import json
from pathlib import Path

def sanitize_filename(name: str) -> str:
    """Remove ou substitui caracteres problemáticos para sistemas de arquivos Linux/Google Drive."""
    name = name.replace('/', '-').replace('\\', '-').replace(':', ' -')
    name = name.replace('–', '-').replace('—', '-').replace('|', '-')
    name = re.sub(r'[\*\?\"<>\|]', '', name)
    name = re.sub(r'\s+', ' ', name).strip()
    return name

def format_ua_folder(ua_title: str) -> str:
    """Padroniza o nome da pasta da UA (ex: 'UA 1 - Acesso à Rede' -> 'UA 01 - Acesso à Rede')."""
    match = re.match(r'UA\s*(\d+)\s*[-–—]\s*(.*)', ua_title, re.IGNORECASE)
    if match:
        num = int(match.group(1))
        title = match.group(2).strip()
        return f"UA {num:02d} - {sanitize_filename(title)}"
    return sanitize_filename(ua_title)

def parse_html_aluno(html_path: str):
    with open(html_path, 'r', encoding='utf-8') as f:
        text = f.read()

    # 1. Identificar Curso e Período
    curso_m = re.search(r'data-preset=\"Headline1\"[^>]*>([^<]+)</p>', text)
    curso = curso_m.group(1).strip() if curso_m else "Gestão da TI"

    periodo = "3º Período"
    for p in ["1° período", "2° período", "3° período"]:
        if 'color-accent-500' in text and p in text:
            periodo = p.replace('°', 'º')

    # Identificar Módulo / Grande Área
    h2_matches = re.findall(r'data-preset=\"Headline2\"[^>]*>([^<]+)</p>', text)
    modulo = "Modelagem e Segurança da Informação"
    for h2 in h2_matches:
        if h2.strip() != "Continue de onde parou":
            modulo = h2.strip()
            break

    # 2. Identificar todas as disciplinas
    disc_splits = list(re.finditer(r'<p data-accent-color=\"gray\" data-preset=\"Headline3\"[^>]*>([^<]+)</p>', text))

    disciplinas = []
    for i, dm in enumerate(disc_splits):
        disc_name = dm.group(1).strip()
        start_pos = dm.end()
        end_pos = disc_splits[i+1].start() if i+1 < len(disc_splits) else len(text)
        disc_chunk = text[start_pos:end_pos]

        disc_obj = {
            'nome': disc_name,
            'pasta': sanitize_filename(disc_name),
            'unidades': []
        }

        # Verificar se tem UAs (Headline4)
        ua_splits = list(re.finditer(r'<p data-accent-color=\"gray\" data-preset=\"Headline4\"[^>]*>([^<]+)</p>', disc_chunk))

        if ua_splits:
            for u_idx, um in enumerate(ua_splits):
                ua_raw = um.group(1).strip()
                u_start = um.end()
                u_end = ua_splits[u_idx+1].start() if u_idx+1 < len(ua_splits) else len(disc_chunk)
                ua_chunk = disc_chunk[u_start:u_end]

                ua_obj = {
                    'titulo_original': ua_raw,
                    'pasta_ua': format_ua_folder(ua_raw),
                    'aulas': []
                }

                aula_splits = list(re.finditer(r'<p data-accent-color=\"gray\" data-preset=\"Body2\"[^>]*>([^<]+)</p>', ua_chunk))
                for a_idx, am in enumerate(aula_splits):
                    a_raw = am.group(1).strip()
                    a_start = am.end()
                    a_end = aula_splits[a_idx+1].start() if a_idx+1 < len(aula_splits) else len(ua_chunk)
                    a_chunk = ua_chunk[a_start:a_end]

                    pdfs = re.findall(r'Aula PDF - ([^<]+)', a_chunk)
                    video_blocks = re.findall(r'<div class=\"styles_accordionVideoItem[^\"]*\".*?</div>\s*</div>\s*</div>', a_chunk, re.DOTALL)
                    videos = []
                    for vb in video_blocks:
                        v_title_m = re.search(r'data-preset=\"Body3\"[^>]*>([^<]+)</p>', vb)
                        prof_m = re.search(r'<i class=\"fal fa-user[^\"]*\"></i>\s*([^<]+)</p>', vb)
                        dur_m = re.search(r'data-preset=\"Body3\"[^>]*>(\d{2}:\d{2})</p>', vb)
                        url_m = re.search(r'href=\"(/graduacao/curso/[^\"]+)\"', vb)

                        v_title = v_title_m.group(1).strip() if v_title_m else 'Vídeo'
                        prof = prof_m.group(1).strip() if prof_m else 'Professor do Curso'
                        dur = dur_m.group(1).strip() if dur_m else 'N/D'
                        v_url = url_m.group(1).strip() if url_m else ''

                        videos.append({
                            'titulo': v_title,
                            'professor': prof,
                            'duracao': dur,
                            'url': v_url
                        })

                    ua_obj['aulas'].append({
                        'numero': a_idx + 1,
                        'titulo_original': a_raw,
                        'pasta_aula': f"Aula {a_idx+1:02d} - {sanitize_filename(a_raw)}",
                        'pdfs': pdfs if pdfs else [a_raw],
                        'videos': videos
                    })

                disc_obj['unidades'].append(ua_obj)
        else:
            # Disciplinas sem UAs explícitas (ex: Projeto Integrador, Atividade Extensionista)
            aula_splits = list(re.finditer(r'<p data-accent-color=\"gray\" data-preset=\"Body2\"[^>]*>([^<]+)</p>', disc_chunk))
            ua_obj = {
                'titulo_original': 'Conteúdo Geral',
                'pasta_ua': '',  # Sem subpasta de UA para não criar níveis desnecessários
                'aulas': []
            }

            for a_idx, am in enumerate(aula_splits):
                a_raw = am.group(1).strip()
                a_start = am.end()
                a_end = aula_splits[a_idx+1].start() if a_idx+1 < len(aula_splits) else len(disc_chunk)
                a_chunk = disc_chunk[a_start:a_end]

                pdfs = re.findall(r'Aula PDF - ([^<]+)', a_chunk)
                video_blocks = re.findall(r'<div class=\"styles_accordionVideoItem[^\"]*\".*?</div>\s*</div>\s*</div>', a_chunk, re.DOTALL)
                videos = []
                for vb in video_blocks:
                    v_title_m = re.search(r'data-preset=\"Body3\"[^>]*>([^<]+)</p>', vb)
                    prof_m = re.search(r'<i class=\"fal fa-user[^\"]*\"></i>\s*([^<]+)</p>', vb)
                    dur_m = re.search(r'data-preset=\"Body3\"[^>]*>(\d{2}:\d{2})</p>', vb)
                    url_m = re.search(r'href=\"(/graduacao/curso/[^\"]+)\"', vb)

                    v_title = v_title_m.group(1).strip() if v_title_m else 'Vídeo'
                    prof = prof_m.group(1).strip() if prof_m else 'Professor do Curso'
                    dur = dur_m.group(1).strip() if dur_m else 'N/D'
                    v_url = url_m.group(1).strip() if url_m else ''

                    videos.append({
                        'titulo': v_title,
                        'professor': prof,
                        'duracao': dur,
                        'url': v_url
                    })

                ua_obj['aulas'].append({
                    'numero': a_idx + 1,
                    'titulo_original': a_raw,
                    'pasta_aula': f"Aula {a_idx+1:02d} - {sanitize_filename(a_raw)}",
                    'pdfs': pdfs if pdfs else [a_raw],
                    'videos': videos
                })

            disc_obj['unidades'].append(ua_obj)

        disciplinas.append(disc_obj)

    return {
        'curso': curso,
        'periodo': periodo,
        'modulo': modulo,
        'disciplinas': disciplinas
    }

def gerar_template_resumo(curso: str, modulo: str, disciplina: str, ua_data: dict, aula_data: dict) -> str:
    """Gera um arquivo de resumo Markdown formatado e otimizado para NotebookLM e Gemini."""
    videos_md = ""
    duracao_total_min = 0
    duracao_total_sec = 0

    for i, v in enumerate(aula_data['videos'], 1):
        videos_md += f"- **Parte {i:02d}:** {v['titulo']} ({v['duracao']}) - *{v['professor']}*\n"
        if ':' in v['duracao']:
            try:
                m, s = map(int, v['duracao'].split(':'))
                duracao_total_min += m
                duracao_total_sec += s
            except ValueError:
                pass

    duracao_total_min += duracao_total_sec // 60
    duracao_total_sec = duracao_total_sec % 60
    tempo_formatado = f"{duracao_total_min} min {duracao_total_sec:02d} s" if aula_data['videos'] else "N/D"

    pdfs_md = ""
    for pdf_nome in aula_data['pdfs']:
        pdfs_md += f"- [ ] `PDF da Matéria`: `{pdf_nome}.pdf`\n"

    ua_titulo = ua_data['titulo_original']
    ua_header = f"## {ua_titulo} - Aula {aula_data['numero']:02d}: {aula_data['titulo_original']}" if ua_titulo != 'Conteúdo Geral' else f"## Aula {aula_data['numero']:02d}: {aula_data['titulo_original']}"

    content = f"""# Resumo da Matéria: {disciplina}
{ua_header}

> **Curso:** {curso} | **Período:** 3º Período  
> **Módulo:** {modulo}  
> **Disciplina:** {disciplina}  
> **Unidade:** {ua_titulo}  
> **Aula:** {aula_data['numero']:02d} - {aula_data['titulo_original']}  
> **Carga de Vídeo:** ~{tempo_formatado} ({len(aula_data['videos'])} bloco{'s' if len(aula_data['videos']) != 1 else ''} de vídeo)

---

## 📂 Checklist de Materiais Baixados
{pdfs_md}- [ ] `PDF de Slides`: `Slides - {sanitize_filename(aula_data['titulo_original'])}.pdf`
- [ ] `Áudios`: MP3 das videoaulas
- [ ] `Legendas/Transcrições`: VTT / SRT / TXT
- [ ] `Resumo Gerado`: Markdown pronto para revisão

---

## 🎬 Blocos de Videoaulas
{videos_md if videos_md else "_Nenhum vídeo registrado para esta aula._\n"}
---

## 🎯 Objetivos de Aprendizagem
- [ ] Compreender os conceitos principais de **{aula_data['titulo_original']}**.
- [ ] Conectar os fundamentos com as aplicações práticas em **{disciplina}**.
- [ ] Consolidar pontos críticos para exames e questionários (Quiz / Check de Aprendizagem).

---

## 📝 Resumo Consolidado (Para NotebookLM / Gemini)

### 1. Visão Geral e Conceitos Fundamentais
*Insira aqui o resumo gerado pelo Gemini / NotebookLM ou suas anotações principais.*

- **Conceito Chave 1:** 
- **Conceito Chave 2:** 
- **Conceito Chave 3:** 

### 2. Tópicos Abordados
*Resumo detalhado dos blocos de vídeo e do livro-texto.*

### 3. Tabela de Termos Técnicos, Siglas e Protocolos
| Termo / Sigla | Definição / Significado | Aplicação Prática |
| :--- | :--- | :--- |
| | | |
| | | |

---

## 🧠 Mapa Mental / Diagrama de Fluxo (Mermaid)
```mermaid
flowchart TD
    A["{aula_data['titulo_original']}"] --> B["Conceito Principal"]
    A --> C["Tecnologias / Modelos"]
    B --> D["Funcionamento Prático"]
    C --> E["Boas Práticas & Segurança"]
```

---

## ❓ Perguntas de Fixação & Flashcards (Estudo Ativo)
1. **Pergunta:** 
   - **Resposta:** 
2. **Pergunta:** 
   - **Resposta:** 

---

## 💡 Dicas de Estudo
- Faça o **Check de Aprendizagem** e o **Quiz da UA** após revisar este resumo.
- Para gerar novas perguntas e simular testes, carregue este arquivo + o PDF da matéria no **NotebookLM** ou **Gemini**.
"""
    return content

def criar_estrutura_diretorios(base_dir: Path, data: dict):
    """Cria a estrutura de pastas e arquivos no diretório alvo para todas as disciplinas."""
    modulo_dir = base_dir / sanitize_filename(data['modulo'])
    modulo_dir.mkdir(parents=True, exist_ok=True)

    # README Geral do Módulo
    readme_modulo = modulo_dir / "README.md"
    readme_modulo_content = f"# Módulo: {data['modulo']}\n\n"
    readme_modulo_content += f"> **Curso:** {data['curso']} | **Período:** {data['periodo']}\n\n"
    readme_modulo_content += "## 📚 Disciplinas do Módulo\n\n"

    for disc in data['disciplinas']:
        disc_dir = modulo_dir / disc['pasta']
        disc_dir.mkdir(parents=True, exist_ok=True)

        total_aulas_disc = sum(len(u['aulas']) for u in disc['unidades'])
        total_videos_disc = sum(sum(len(a['videos']) for a in u['aulas']) for u in disc['unidades'])
        readme_modulo_content += f"- **[{disc['nome']}](./{disc['pasta']})** ({len(disc['unidades'])} UAs, {total_aulas_disc} Aulas, {total_videos_disc} Vídeos)\n"

        # README da Disciplina
        readme_disc = disc_dir / "README.md"
        readme_disc_content = f"# {disc['nome']}\n\n"
        readme_disc_content += f"> **Curso:** {data['curso']} | **Período:** {data['periodo']} | **Módulo:** {data['modulo']}\n\n"
        readme_disc_content += "## 📚 Unidades e Aulas\n\n"

        for ua in disc['unidades']:
            if ua['pasta_ua']:
                ua_dir = disc_dir / ua['pasta_ua']
                ua_dir.mkdir(parents=True, exist_ok=True)
                readme_disc_content += f"### 📁 {ua['pasta_ua']}\n"
                ua_prefix = f"./{ua['pasta_ua']}"
            else:
                ua_dir = disc_dir
                readme_disc_content += f"### 📁 Conteúdo Geral\n"
                ua_prefix = "."

            for aula in ua['aulas']:
                aula_dir = ua_dir / aula['pasta_aula']
                aula_dir.mkdir(parents=True, exist_ok=True)

                link_path = f"{ua_prefix}/{aula['pasta_aula']}" if ua['pasta_ua'] else f"./{aula['pasta_aula']}"
                qtd_vids = len(aula['videos'])
                readme_disc_content += f"- **[{aula['pasta_aula']}]({link_path})** ({qtd_vids} vídeo{'s' if qtd_vids != 1 else ''} + PDF)\n"

                # Criar arquivo de Resumo Template se não existir
                resumo_file = aula_dir / f"Resumo - {sanitize_filename(aula['titulo_original'])}.md"
                if not resumo_file.exists():
                    conteudo_resumo = gerar_template_resumo(
                        curso=data['curso'],
                        modulo=data['modulo'],
                        disciplina=disc['nome'],
                        ua_data=ua,
                        aula_data=aula
                    )
                    resumo_file.write_text(conteudo_resumo, encoding='utf-8')

            readme_disc_content += "\n"

        readme_disc.write_text(readme_disc_content, encoding='utf-8')

    readme_modulo.write_text(readme_modulo_content, encoding='utf-8')
    print(f"[OK] Toda a estrutura foi gerada com sucesso em: {modulo_dir}")

def main():
    base_path = Path("/home/ecode/projects/faculdade/3o-periodo")
    html_file = base_path / "inner-html-box-aluno.html"

    if not html_file.exists():
        print(f"Erro: Arquivo {html_file} não encontrado.")
        sys.exit(1)

    print("Analisando o HTML expandido do portal do aluno...")
    dados = parse_html_aluno(str(html_file))

    print(f"Curso: {dados['curso']}")
    print(f"Período: {dados['periodo']}")
    print(f"Módulo: {dados['modulo']}")
    print(f"Total de Disciplinas: {len(dados['disciplinas'])}")
    
    total_uas = sum(len(d['unidades']) for d in dados['disciplinas'])
    total_aulas = sum(sum(len(u['aulas']) for u in d['unidades']) for d in dados['disciplinas'])
    total_videos = sum(sum(sum(len(a['videos']) for a in u['aulas']) for u in d['unidades']) for d in dados['disciplinas'])

    print(f"Total de UAs mapeadas: {total_uas}")
    print(f"Total de Aulas mapeadas: {total_aulas}")
    print(f"Total de Vídeos mapeados: {total_videos}")

    print("\nCriando pastas, subpastas e templates de resumo...")
    criar_estrutura_diretorios(base_path, dados)

if __name__ == '__main__':
    main()

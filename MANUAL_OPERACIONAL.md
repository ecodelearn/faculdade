# Manual Operacional e Roadmap de Estudos com IA
## Gestão da TI - Guia Definitivo de Execução e Evolução

Este documento é o guia definitivo para replicar o fluxo de organização acadêmica em novos períodos/semestres com máxima fidelidade e detalha o roadmap para evolução do nosso **Agente Multimodal de Estudos (Áudio, Diagramas e Slides Mira)**.

---

## 🧭 PARTE 1: Fluxo Operacional Passo a Passo (Para Novos Semestres)

Quando iniciar um novo período da faculdade (ex: 4º Período), siga rigorosamente estas 5 etapas:

```
[1. Extrair HTML do AVA] ➔ [2. Gerar Estrutura] ➔ [3. Download & Organização] ➔ [4. Limpeza SRT/TXT] ➔ [5. Agente de IA & Resumos]
```

### 1️⃣ Etapa 1: Extrair o Plano do AVA
1. Acesse o portal do aluno da faculdade no Firefox.
2. Abra o módulo do novo semestre e expanda todas as disciplinas, UAs e blocos de aula.
3. Abra as ferramentas de desenvolvedor (`F12`), inspecione o contêiner principal das aulas e copie o elemento HTML.
4. Crie a pasta do período (ex: `faculdade/4o-periodo/`) e salve o conteúdo em `inner-html-box-aluno.html`.

### 2️⃣ Etapa 2: Gerar a Hierarquia de Pastas e Templates
Copie o script `gerar_estrutura.py` para a pasta do novo período e execute:
```bash
python3 gerar_estrutura.py
```
**O que o script faz:**
- Faz o parsing completo do HTML do AVA.
- Cria a hierarquia padronizada: `Módulo / Disciplina / UA XX - Nome / Aula XX - Nome`.
- Cria os templates de resumo `Resumo - <Aula>.md` pré-preenchidos com metadados (professores, duração dos vídeos, checklist de PDFs e espaço para flashcards).
- Cria os arquivos `README.md` com índices navegáveis.

### 3️⃣ Etapa 3: Baixar e Organizar as Fontes
1. No portal do aluno, execute o script de download no console (`download-manterial-script.js`) ou baixe os materiais (Apostilas `.pdf`, Slides `.pdf` e Legendas `.srt`).
2. *Nota de decisão:* **Descartamos o download de vídeos/áudios brutos** para economizar dezenas de gigabytes, pois as legendas textuais (`.srt`) e PDFs contêm 100% do conteúdo conceitual.
3. Com os arquivos baixados em `~/Downloads`, execute:
```bash
python3 organizar_downloads.py
```
**O que o script faz:**
- Constrói o mapa de chaves normalizadas a partir da grade curricular.
- Identifica cada apostila, slide e legenda baixada e move automaticamente para a pasta exata da aula correspondente.

### 4️⃣ Etapa 4: Limpar e Consolidar as Transcrições
Execute:
```bash
python3 converter_legendas.py
```
**O que o script faz:**
- Remove números de linha e timestamps repetitivos dos arquivos `.srt`.
- Cria arquivos de texto fluido e pontuado: `Transcrição - <Nome>.txt`.
- Gera um arquivo consolidado **`Transcrição Completa - <Nome da Aula>.txt`** por aula, unificando todos os blocos de vídeo em sequência.

### 5️⃣ Etapa 5: Executar o Agente de IA para Resumos e Quizzes
Configure o `.env` com a `GEMINI_API_KEY` e execute:
```bash
# Gerar resumos de uma disciplina inteira:
python3 agente_resumos.py --disciplina "NomeDaMateria"

# Ou gerar para todo o semestre em lote:
python3 agente_resumos.py --todas

# Resolver questões de prova no Modo Quiz (com 3 rodadas de debate de especialistas):
python3 agente_resumos.py --quiz "Questão da prova com alternativas..."
```
**Resultado:**
- Cria o arquivo `Anotação Portal - <Aula>.txt` pronto para colar na caixinha de anotações do AVA.
- Atualiza a seção de Resumo Consolidado no arquivo local `Resumo - <Aula>.md`.

---

## 🚀 PARTE 2: Sincronização e Estudo Ativo

### ☁️ Google Drive
Para manter o material acessível na nuvem e no celular:
- Execute `./subir_drive.sh` ou faça o upload da pasta direto pelo Google Drive web.

### 🧠 NotebookLM (Google)
1. Crie cadernos temáticos por Disciplina ou UA.
2. Adicione como fonte a **Apostila (`.pdf`)**, os **Slides (`.pdf`)** e a **`Transcrição Completa - <Aula>.txt`**.
3. Use o *Audio Overview* para gerar podcasts de estudo e tire dúvidas conceituais diretamente com a IA baseando-se estritamente nas fontes da faculdade.

---

## 🔮 PARTE 3: Roadmap de Evolução (Agente Multimodal e Slides Mira)

Para os próximos períodos e aprofundamento das matérias atuais, expandiremos a automação para um **Agente de Ensino Multimodal**:

```
                              ┌──> Resumos Narrados em Áudio (TTS / Podcasts)
                              │
[Fontes da Aula] ──> [Agente] ├──> Diagramas Conceituais (Mermaid / Imagens)
                              │
                              └──> Decks Interativos 3D com MIRA (Prof. Sandeco)
```

### 1. Resumos Narrados em Áudio (TTS Local e Gemini Audio)
- **Objetivo:** Criar podcasts didáticos e áudios de revisão rápida (3 a 5 minutos) por aula para escutar no transporte ou intervalos.
- **Implementação:**
  - Integrar ferramentas de TTS de alta qualidade e baixa latência (como `Edge-TTS`, `Kokoro` ou a API nativa de áudio do Gemini).
  - Gerar roteiros de diálogo entre dois apresentadores (estilo NotebookLM Audio Overview) sintetizando os pontos-chave de cada UA.

### 2. Geração de Diagramas Visuais e Imagens Explicativas
- **Objetivo:** Transformar conceitos abstratos de infraestrutura, segurança e arquitetura em mapas visuais claros.
- **Implementação:**
  - Geração automática de fluxos **Mermaid** (arquiteturas cliente-servidor, topologias lógicas de rede, fluxos BPMN, pipelines CI/CD).
  - Renderização de diagramas conceituais e infográficos didáticos usando ferramentas locais ou APIs generativas.

### 3. Decks de Slides Interativos e 3D com MIRA (Prof. Sandeco)
- **Objetivo:** Criar apresentações web interativas, modernas e altamente visuais para tópicos densos de TI (ex: Criptografia Assimétrica, Modelo OSI, Microsserviços, Algoritmos de Roteamento).
- **Implementação:**
  - Conectar o ecossistema local do **Mira** (`/home/ecode/projects/slides`) com o nosso agente acadêmico.
  - O agente seleciona os conceitos centrais da aula e gera a estrutura do deck no padrão Mira (`aula-capitulo` / temas personalizados).
  - Inclusão de elementos visuais dinâmicos em **Three.js** e **D3.js** (gráficos interativos, visualizações 3D de pacotes de rede e estruturas de dados).

### 4. Videoaulas Sintetizadas (Slides + TTS + Animações)
- **Objetivo:** Unificar os slides animados do Mira com o áudio narrado do TTS para gerar mini-videoaulas de revisão rápida por aula.

---

## 📋 Checklist Rápido de Início de Semestre

- [ ] Criar diretório `faculdade/Xo-periodo/`
- [ ] Extrair `inner-html-box-aluno.html` do portal
- [ ] Executar `gerar_estrutura.py`
- [ ] Baixar PDFs e legendas do portal
- [ ] Executar `organizar_downloads.py`
- [ ] Executar `converter_legendas.py`
- [ ] Executar `agente_resumos.py --todas`
- [ ] Colar anotações no portal do aluno
- [ ] Sincronizar com Google Drive e NotebookLM
- [ ] Git commit e push para o repositório privado

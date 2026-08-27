# Faculdade - Gestão da TI (3º Período)
## Módulo: Modelagem e Segurança da Informação

Estrutura automatizada de estudos com suporte para **Google Drive**, **NotebookLM** e **Gemini**.

---

### 📊 Visão Geral do Período
- **6 Disciplinas Mapeadas:**
  1. `Redes e Segurança da Informação` (4 UAs, 20 Aulas, 65 Vídeos)
  2. `Gestão da Segurança e Continuidade` (4 UAs, 20 Aulas, 60 Vídeos)
  3. `Desenvolvimento Back-end` (4 UAs, 20 Aulas, 76 Vídeos)
  4. `Modelagem e Gerenciamento de Processos de Negócio` (4 UAs, 20 Aulas, 60 Vídeos)
  5. `Projeto Integrador: Profissional de TI – Empregabilidade e Portfólio` (1 Aula)
  6. `Atividade Extensionista 3 - TI` (1 Aula)
- **Total:** 18 UAs | 82 Aulas | 263 Blocos de Vídeo

---

### 🛠️ Scripts e Comandos Disponíveis

#### 1. Gerar / Atualizar Estrutura de Pastas e Resumos
```bash
python3 gerar_estrutura.py
```
Lê `inner-html-box-aluno.html` e cria todas as pastas, índices `README.md` e arquivos de template `Resumo - <Aula>.md` preenchidos com metadados dos vídeos e planos de estudo.

#### 2. Organizar Arquivos Baixados do Portal
```bash
python3 organizar_downloads.py
```
Varre a pasta `~/Downloads`, identifica apostilas, slides, legendas e anotações PDF baixadas no portal e move cada arquivo automaticamente para a pasta exata da sua aula.

#### 3. Converter e Limpar Legendas (SRT -> TXT)
```bash
python3 converter_legendas.py
```
Converte todos os arquivos `.srt` em arquivos de texto contínuos `.txt` (removendo índices e timestamps) e gera um arquivo consolidado `Transcrição Completa - <Aula>.txt` por aula.

#### 4. Agente de IA para Geração de Resumos e Quizzes (Gemini)
```bash
# Gerar resumo de uma aula específica
python3 agente_resumos.py --disciplina "Redes" --ua 01 --aula 01

# Gerar resumo para todas as aulas de uma disciplina
python3 agente_resumos.py --disciplina "Back-end"

# Gerar resumo para todas as 82 aulas do período
python3 agente_resumos.py --todas

# Resolver questão no MODO QUIZ (com debate de especialistas)
python3 agente_resumos.py --quiz "Texto da questão com alternativas A, B, C, D..."
```

---

### ☁️ Sincronização com Google Drive (Rclone)
```bash
./subir_drive.sh
```

---

### 📂 Formato de Cada Pasta de Aula
- `Apostila - <Nome>.pdf`: Livro/apostila da matéria
- `Slide - <Nome> [I, II...].pdf`: Slides da aula
- `Transcrição - <Nome> [I, II...].txt`: Transcrição limpa por bloco de vídeo
- `Transcrição Completa - <Nome da Aula>.txt`: Transcrição completa da aula (todos os blocos unidos)
- `Anotação Portal - <Nome da Aula>.txt`: Resumo gerado pelo Agente Gemini pronto para colar no portal
- `Resumo - <Nome da Aula>.md`: Template estruturado para estudo ativo e notas locais

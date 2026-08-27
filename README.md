# Faculdade - Gestão da TI
Repositório central de materiais de estudo, scripts de automação e agentes de IA (Google Gemini / NotebookLM / Mira).

---

## 📖 Guia de Operação e Roadmap
- Consulte o **[Manual Operacional e Roadmap de Estudos](file:///home/ecode/projects/faculdade/MANUAL_OPERACIONAL.md)** para o passo a passo completo de execução em novos semestres e a arquitetura planejada para o Agente Multimodal (Áudio, Diagramas e Slides 3D com Mira).

---

## 📂 Estrutura do Repositório

- **`3o-periodo/`**: Conteúdo completo do 3º Período (Módulo: *Modelagem e Segurança da Informação*)
  - `Modelagem e Segurança da Informação/`: 6 disciplinas, 18 UAs e 82 Aulas organizadas com Apostilas (`.pdf`), Slides (`.pdf`), Transcrições limpas (`.txt`), Resumos Markdown (`.md`) e Anotações do Portal.
  - `gerar_estrutura.py`: Gerador da árvore de pastas e templates.
  - `organizar_downloads.py`: Organizador automático de downloads do portal do aluno.
  - `converter_legendas.py`: Conversor e unificador de legendas SRT em transcrições contínuas TXT.
  - `agente_resumos.py`: Agente inteligente com Gemini para geração automatizada de resumos para o portal e resolução de Quizzes.
  - `subir_drive.sh`: Script de sincronização com o Google Drive via Rclone.
- **`MANUAL_OPERACIONAL.md`**: Runbook completo para novos períodos e especificações do roadmap multimodal.

---

## 🔒 Segurança e Privacidade
Este repositório é privado (`ecodelearn/faculdade`) e configurado via `.gitignore` para nunca versionar tokens, chaves de API (`.env`) ou credenciais.

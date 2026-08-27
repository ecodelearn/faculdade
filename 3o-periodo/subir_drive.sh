#!/usr/bin/env bash
# Script para sincronizar todo o material do 3º Período com o Google Drive
set -e

SOURCE_DIR="/home/ecode/projects/faculdade/3o-periodo/Modelagem e Segurança da Informação"
REMOTE_DEST="gdrive:Faculdade/3o-periodo/Modelagem e Segurança da Informação"

if ! command -v rclone &> /dev/null; then
    echo "❌ Rclone não encontrado. Instale com: sudo pacman -S rclone"
    exit 1
fi

echo "🚀 Iniciando sincronização com o Google Drive..."
echo "📂 Origem:  $SOURCE_DIR"
echo "☁️  Destino: $REMOTE_DEST"
echo "--------------------------------------------------------"

rclone sync "$SOURCE_DIR" "$REMOTE_DEST" -P --transfers 8 --checkers 16

echo "--------------------------------------------------------"
echo "✅ Sincronização concluída com sucesso!"
echo "👉 Abra o NotebookLM (https://notebooklm.google.com) e adicione as fontes direto do Google Drive."

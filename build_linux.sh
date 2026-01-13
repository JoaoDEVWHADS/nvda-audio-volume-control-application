#!/bin/bash
set -e

echo "========================================="
echo "  BUILD NVDA ADD-ON: AudioVolumeControl"
echo "  (Com Dependency Shading)"
echo "========================================="

BASE_DIR="/root/AddonTemplate-master"
TARGET_DIR="$BASE_DIR/addon/globalPlugins/audioVolumeControl"

cd "$BASE_DIR"

echo "1. Limpando ambiente e instalando ferramentas de build..."
if command -v apt-get &> /dev/null; then
    apt-get update && apt-get install -y gettext zip unzip
elif command -v dnf &> /dev/null; then
    dnf install -y gettext zip unzip
fi

scons -c > /dev/null 2>&1 || true
rm -rf addon/locale
rm -rf "$TARGET_DIR/pycaw"*
rm -rf "$TARGET_DIR/dep_pycaw"*
rm -rf "$TARGET_DIR/comtypes"*
rm -rf "$TARGET_DIR/psutil"*
rm -rf "$TARGET_DIR/__pycache__"
rm -f *.nvda-addon
echo "   OK"

echo "2. Instalando dependências..."
echo "2. Baixando dependências Windows (32-bit) para cross-compile..."
mkdir -p temp_wheels
pip3 download \
    --dest temp_wheels \
    --platform win32 \
    --python-version 3.11 \
    --only-binary=:all: \
    --no-deps \
    pycaw comtypes psutil

echo "   Extraindo wheels..."
for wheel in temp_wheels/*.whl; do
    python3 -c "import zipfile, sys; zipfile.ZipFile(sys.argv[1]).extractall(sys.argv[2])" "$wheel" "$TARGET_DIR/"
done
rm -rf temp_wheels
echo "   OK"

echo "3. Aplicando 'Shading' no pycaw (Renomeando para dep_pycaw)..."
if [ -d "$TARGET_DIR/pycaw" ]; then
    mv "$TARGET_DIR/pycaw" "$TARGET_DIR/dep_pycaw"
    
    find "$TARGET_DIR/dep_pycaw" -name "*.py" -exec sed -i 's/from pycaw/from dep_pycaw/g' {} +
    find "$TARGET_DIR/dep_pycaw" -name "*.py" -exec sed -i 's/import pycaw/import dep_pycaw/g' {} +
    
    echo "   ✓ Renomeado pycaw -> dep_pycaw e corrigido imports internos"
else
    echo "❌ FALHA: Pasta pycaw não encontrada após extração!"
    exit 1
fi

echo "4. Limpando lixo..."
rm -rf "$TARGET_DIR/"*.dist-info
rm -rf "$TARGET_DIR/"bin
echo "   OK"

echo "5. Compilando o arquivo .nvda-addon..."
scons
echo "   OK"

echo "6. Verificando resultado..."
FILE_NAME=$(ls *.nvda-addon 2>/dev/null | head -n 1)

if [ -z "$FILE_NAME" ]; then
    echo "❌ FALHA: Arquivo não foi criado!"
    exit 1
fi

SIZE_BYTES=$(stat -c%s "$FILE_NAME")
SIZE_MB=$(echo "scale=2; $SIZE_BYTES/1024/1024" | bc 2>/dev/null || echo "N/A")

if [ "$SIZE_BYTES" -lt 1000000 ]; then
    echo "⚠️  ALERTA: Arquivo muito pequeno ($SIZE_MB MB). Dependências podem estar faltando!"
else
    echo "✅ SUCESSO! Arquivo criado:"
    echo "   Nome: $FILE_NAME"
    echo "   Tamanho: ~$SIZE_MB MB"
fi

echo ""
echo "========================================="
echo "Para baixar no Windows:"
echo "python3 -m http.server 8000"
echo "========================================="

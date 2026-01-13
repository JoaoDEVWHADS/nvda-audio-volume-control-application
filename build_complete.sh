#!/bin/bash
# Script Final - Compilação Completa do Add-on NVDA
# Autor: NVDA Community
# Data: 2026-01-12

set -e  # Parar em caso de erro

echo "========================================="
echo "  NVDA Audio Volume Control - Build"
echo "========================================="
echo ""

cd /root/AddonTemplate-master

echo "1. Limpando builds anteriores..."
scons -c 2>/dev/null || true
rm -rf addon/locale
rm -rf addon/globalPlugins/audioVolumeControl/pycaw*
rm -rf addon/globalPlugins/audioVolumeControl/comtypes*
rm -rf addon/globalPlugins/audioVolumeControl/psutil*
rm -rf addon/globalPlugins/audioVolumeControl/bin
rm -f *.nvda-addon
echo "   ✓ Limpeza concluída"
echo ""

echo "2. Instalando dependências Python..."
pip3 install pycaw comtypes psutil \
    --target addon/globalPlugins/audioVolumeControl/ \
    --upgrade \
    --quiet
echo "   ✓ Dependências instaladas"
echo ""

echo "3. Verificando dependências..."
if [ -d "addon/globalPlugins/audioVolumeControl/pycaw" ]; then
    echo "   ✓ pycaw encontrado"
else
    echo "   ✗ pycaw NÃO encontrado!"
    exit 1
fi

if [ -d "addon/globalPlugins/audioVolumeControl/comtypes" ]; then
    echo "   ✓ comtypes encontrado"
else
    echo "   ✗ comtypes NÃO encontrado!"
    exit 1
fi

if [ -d "addon/globalPlugins/audioVolumeControl/psutil" ]; then
    echo "   ✓ psutil encontrado"
else
    echo "   ✗ psutil NÃO encontrado!"
    exit 1
fi
echo ""

echo "4. Compilando add-on..."
scons
echo "   ✓ Compilação concluída"
echo ""

echo "5. Verificando arquivo gerado..."
if [ -f "audioVolumeControl-1.0.0.nvda-addon" ]; then
    SIZE=$(ls -lh audioVolumeControl-1.0.0.nvda-addon | awk '{print $5}')
    echo "   ✓ Arquivo criado: audioVolumeControl-1.0.0.nvda-addon"
    echo "   ✓ Tamanho: $SIZE"
else
    echo "   ✗ Arquivo NÃO foi gerado!"
    exit 1
fi
echo ""

echo "========================================="
echo "  ✓ BUILD CONCLUÍDO COM SUCESSO!"
echo "========================================="
echo ""
echo "Próximos passos:"
echo "1. Transfira o arquivo para o Windows"
echo "2. Desinstale o add-on antigo no NVDA"
echo "3. Feche o NVDA completamente"
echo "4. Delete: C:\\Users\\Noah\\AppData\\Roaming\\nvda\\addons\\audioVolumeControl"
echo "5. Abra o NVDA"
echo "6. Instale o novo .nvda-addon"
echo "7. Reinicie o NVDA"
echo "8. Teste com Ctrl+NVDA+Y"
echo ""
echo "Para transferir via HTTP:"
echo "  python3 -m http.server 8000"
echo "  Acesse: http://$(hostname -I | awk '{print $1}'):8000/"
echo ""

#!/bin/bash
# Script Final - Build Completo do Add-on NVDA
# Resolve TODOS os problemas de dependências

set -e

echo "================================================"
echo "  NVDA Audio Volume Control - Build Final"
echo "================================================"
echo ""

cd /root/AddonTemplate-master

echo "1. Limpando completamente..."
scons -c 2>/dev/null || true
rm -rf addon/locale
rm -rf addon/lib
rm -rf addon/globalPlugins/audioVolumeControl/{pycaw*,comtypes*,psutil*,bin}
rm -f *.nvda-addon
echo "   ✓ Limpeza concluída"
echo ""

echo "2. Criando estrutura de diretórios..."
mkdir -p addon/lib
echo "   ✓ Diretórios criados"
echo ""

echo "3. Instalando dependências em addon/lib/..."
pip3 install pycaw comtypes psutil \
    --target addon/lib/ \
    --upgrade \
    --no-warn-script-location \
    2>&1 | grep -E "(Successfully|Collecting|Installing)" || true
echo "   ✓ Dependências instaladas"
echo ""

echo "4. Verificando dependências instaladas..."
DEPS_OK=true

if [ -d "addon/lib/pycaw" ]; then
    echo "   ✓ pycaw instalado"
else
    echo "   ✗ pycaw FALTANDO!"
    DEPS_OK=false
fi

if [ -d "addon/lib/comtypes" ]; then
    echo "   ✓ comtypes instalado"
else
    echo "   ✗ comtypes FALTANDO!"
    DEPS_OK=false
fi

if [ -d "addon/lib/psutil" ]; then
    echo "   ✓ psutil instalado"
else
    echo "   ✗ psutil FALTANDO!"
    DEPS_OK=false
fi

if [ "$DEPS_OK" = false ]; then
    echo ""
    echo "ERRO: Dependências não foram instaladas corretamente!"
    exit 1
fi
echo ""

echo "5. Contando arquivos em addon/lib/..."
FILE_COUNT=$(find addon/lib/ -type f | wc -l)
echo "   ✓ Total de arquivos: $FILE_COUNT"
echo ""

echo "6. Compilando add-on..."
scons 2>&1 | grep -E "(Building|Generating|done)" || true
echo "   ✓ Compilação concluída"
echo ""

echo "7. Verificando pacote gerado..."
if [ -f "audioVolumeControl-1.0.0.nvda-addon" ]; then
    SIZE_BYTES=$(stat -f%z "audioVolumeControl-1.0.0.nvda-addon" 2>/dev/null || stat -c%s "audioVolumeControl-1.0.0.nvda-addon")
    SIZE_KB=$((SIZE_BYTES / 1024))
    SIZE_MB=$((SIZE_BYTES / 1048576))
    
    echo "   ✓ Arquivo: audioVolumeControl-1.0.0.nvda-addon"
    echo "   ✓ Tamanho: ${SIZE_KB}KB (${SIZE_MB}MB)"
    
    if [ $SIZE_KB -lt 2000 ]; then
        echo ""
        echo "   ⚠ AVISO: Arquivo muito pequeno (< 2MB)!"
        echo "   ⚠ As dependências podem não estar incluídas!"
        echo ""
        echo "   Verificando conteúdo do pacote..."
        if command -v unzip &> /dev/null; then
            unzip -l audioVolumeControl-1.0.0.nvda-addon | grep -E "lib/(pycaw|comtypes|psutil)" | head -5
        else
            echo "   (unzip não disponível para verificar)"
        fi
    else
        echo "   ✓ Tamanho adequado - dependências provavelmente incluídas"
    fi
else
    echo "   ✗ ERRO: Arquivo não foi gerado!"
    exit 1
fi
echo ""

echo "================================================"
echo "  ✓ BUILD CONCLUÍDO!"
echo "================================================"
echo ""
echo "Próximos passos no Windows:"
echo "1. Transfira o arquivo .nvda-addon"
echo "2. Desinstale add-on antigo"
echo "3. Delete: C:\\Users\\Noah\\AppData\\Roaming\\nvda\\addons\\audioVolumeControl"
echo "4. Instale o novo .nvda-addon"
echo "5. Reinicie NVDA"
echo "6. Teste: Ctrl+NVDA+Y"
echo ""

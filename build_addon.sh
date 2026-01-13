#!/bin/bash
# Script completo para compilar o add-on NVDA com dependências

echo "=== Compilação do Add-on NVDA: Audio Volume Control ==="
echo ""

cd /root/AddonTemplate-master

echo "1. Limpando builds anteriores..."
scons -c
rm -rf addon/locale
rm -rf addon/lib
rm -f *.nvda-addon

echo ""
echo "2. Instalando dependências Python..."
pip3 install pycaw comtypes psutil --target addon/globalPlugins/audioVolumeControl/ --upgrade

echo ""
echo "3. Compilando add-on..."
scons

echo ""
echo "4. Verificando arquivo gerado..."
if [ -f "audioVolumeControl-1.0.0.nvda-addon" ]; then
    ls -lh audioVolumeControl-1.0.0.nvda-addon
    echo ""
    echo "✓ Add-on compilado com sucesso!"
    echo ""
    echo "Próximos passos:"
    echo "1. Transfira o arquivo para o Windows"
    echo "2. Desinstale o add-on antigo no NVDA"
    echo "3. Feche o NVDA completamente"
    echo "4. Instale o novo .nvda-addon"
    echo "5. Abra o NVDA"
    echo "6. Teste com Ctrl+NVDA+Y"
else
    echo "✗ Erro: Arquivo não foi gerado!"
fi

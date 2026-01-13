#!/bin/bash
# Script para instalar dependências corretamente no add-on

cd /root/AddonTemplate-master

echo "Instalando dependências no local correto..."

# Criar pasta lib se não existir
mkdir -p addon/lib

# Instalar dependências na pasta lib
pip3 install pycaw comtypes psutil --target addon/lib/ --upgrade --quiet

echo "Dependências instaladas em addon/lib/"
ls -la addon/lib/ | grep -E "pycaw|comtypes|psutil"

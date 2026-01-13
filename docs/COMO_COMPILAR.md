# 🔧 Como Compilar o Add-on NVDA - Audio Volume Control

## 📋 Pré-requisitos no Linux

```bash
# Instalar dependências do sistema
apt-get update
apt-get install -y python3 python3-pip scons gettext

# Verificar instalação
python3 --version
scons --version
```

---

## 🚀 Compilação Completa (Método Recomendado)

### **Opção 1: Script Automático**

```bash
cd /root/AddonTemplate-master
chmod +x build_complete.sh
./build_complete.sh
```

### **Opção 2: Comandos Manuais**

```bash
# 1. Ir para o diretório do projeto
cd /root/AddonTemplate-master

# 2. Limpar builds anteriores
scons -c
rm -rf addon/locale
rm -rf addon/globalPlugins/audioVolumeControl/pycaw*
rm -rf addon/globalPlugins/audioVolumeControl/comtypes*
rm -rf addon/globalPlugins/audioVolumeControl/psutil*
rm -f *.nvda-addon

# 3. Instalar dependências Python DENTRO do add-on
pip3 install pycaw comtypes psutil \
    --target addon/globalPlugins/audioVolumeControl/ \
    --upgrade

# 4. Verificar se as dependências foram instaladas
ls -la addon/globalPlugins/audioVolumeControl/ | grep -E "pycaw|comtypes|psutil"

# 5. Compilar o add-on
scons

# 6. Verificar arquivo gerado
ls -lh audioVolumeControl-1.0.0.nvda-addon
```

**✅ O arquivo deve ter mais de 1MB** (aproximadamente 1.5-2MB com todas as dependências)

---

## 📦 Transferir para Windows

### **Método 1: Servidor HTTP (Mais Fácil)**

No Linux:
```bash
cd /root/AddonTemplate-master
python3 -m http.server 8000
```

No Windows, abra o navegador:
```
http://IP_DO_LINUX:8000/
```
Baixe: `audioVolumeControl-1.0.0.nvda-addon`

### **Método 2: SCP/SFTP**
Use WinSCP, FileZilla ou similar para baixar:
```
/root/AddonTemplate-master/audioVolumeControl-1.0.0.nvda-addon
```

---

## 🔧 Instalar no NVDA (Windows)

### **Passo 1: Desinstalar Versão Antiga**

1. Abra o NVDA
2. Pressione: `NVDA + N` (menu NVDA)
3. Vá em: `Ferramentas → Gerenciar Complementos`
4. Selecione "Audio Volume Control" (se existir)
5. Clique em "Remover"

### **Passo 2: Limpar Cache (CRÍTICO!)**

1. **Feche o NVDA completamente**: `Ctrl + NVDA + Q`
2. Abra o Explorador de Arquivos (`Win + E`)
3. Cole na barra de endereços:
   ```
   %APPDATA%\nvda\addons
   ```
4. **Delete a pasta** `audioVolumeControl` (se existir)

### **Passo 3: Instalar Novo Add-on**

1. Abra o NVDA novamente
2. Dê **duplo clique** no arquivo `audioVolumeControl-1.0.0.nvda-addon`
3. Confirme a instalação quando solicitado
4. **Reinicie o NVDA** quando solicitado

### **Passo 4: Testar**

Pressione: **`Ctrl + NVDA + Y`**

Deve abrir o diálogo "Controle de Volume de Aplicativos"

---

## ✅ Verificação de Sucesso

### **Checklist:**

- [ ] Arquivo `.nvda-addon` tem **mais de 1MB**
- [ ] Pasta antiga foi deletada de `%APPDATA%\nvda\addons`
- [ ] NVDA foi reiniciado após instalação
- [ ] Atalho `Ctrl + NVDA + Y` abre o diálogo
- [ ] Aplicativos com áudio aparecem na lista

---

## 🐛 Solução de Problemas

### **Problema 1: "No module named 'pycaw'"**

**Causa:** Dependências não foram incluídas no build

**Solução:**
```bash
# No Linux, recompilar com verificação:
cd /root/AddonTemplate-master
rm -f *.nvda-addon
pip3 install pycaw comtypes psutil \
    --target addon/globalPlugins/audioVolumeControl/ \
    --upgrade --force-reinstall
scons
ls -lh audioVolumeControl-1.0.0.nvda-addon  # Deve ter > 1MB
```

### **Problema 2: Atalho não funciona**

**Verificar:**
1. Abra NVDA
2. Vá em: `NVDA → Preferências → Definir Comandos`
3. Procure por "Audio Volume Control"
4. Se não aparecer, o add-on não carregou

**Solução:**
- Veja o log: `%APPDATA%\nvda\nvda.log`
- Procure por erros relacionados a "audioVolumeControl"

### **Problema 3: Arquivo muito pequeno (< 100KB)**

**Causa:** Dependências não foram empacotadas

**Solução:**
```bash
# Verificar estrutura do pacote:
cd /root/AddonTemplate-master
unzip -l audioVolumeControl-1.0.0.nvda-addon | grep -E "pycaw|comtypes|psutil"
```

Deve mostrar centenas de arquivos dessas bibliotecas.

---

## 📝 Estrutura Esperada do Pacote

Dentro do `.nvda-addon` deve conter:

```
globalPlugins/audioVolumeControl/
├── __init__.py
├── audioSessionManager.py
├── volumeController.py
├── volumeControlDialog.py
├── pycaw/                    ← Biblioteca completa
├── comtypes/                 ← Biblioteca completa
└── psutil/                   ← Biblioteca completa
```

---

## 🔍 Logs e Diagnóstico

### **Ver log do NVDA:**
```
%APPDATA%\nvda\nvda.log
```

### **Procurar erros específicos:**
```
Ctrl + F → "audioVolumeControl"
Ctrl + F → "ERROR"
```

---

## 📞 Comandos Rápidos de Referência

```bash
# Compilar tudo de uma vez (Linux)
cd /root/AddonTemplate-master && ./build_complete.sh

# Servir arquivo via HTTP (Linux)
python3 -m http.server 8000

# Limpar cache NVDA (Windows - PowerShell)
Remove-Item "$env:APPDATA\nvda\addons\audioVolumeControl" -Recurse -Force

# Ver tamanho do arquivo (Linux)
ls -lh audioVolumeControl-1.0.0.nvda-addon

# Listar conteúdo do pacote (Linux)
unzip -l audioVolumeControl-1.0.0.nvda-addon
```

---

## ✨ Atalhos do Add-on

| Atalho | Função |
|--------|--------|
| `Ctrl + NVDA + Y` | Abrir diálogo de controle de volume |
| `Seta Cima/Baixo` | Navegar entre aplicativos |
| `Seta Esquerda/Direita` | Ajustar volume (-5% / +5%) |
| `Home` | Volume 0% |
| `End` | Volume 100% |
| `Espaço` | Mute/Unmute |
| `Escape` | Fechar diálogo |

---

**Última atualização:** 2026-01-12

# ✅ COMANDOS FINAIS - Compilar e Instalar

## 🚀 NO LINUX (Compilar)

```bash
# 1. Ir para o diretório
cd /root/AddonTemplate-master

# 2. Limpar tudo
rm -f *.nvda-addon
scons -c
rm -rf addon/globalPlugins/audioVolumeControl/pycaw*
rm -rf addon/globalPlugins/audioVolumeControl/comtypes*
rm -rf addon/globalPlugins/audioVolumeControl/psutil*

# 3. Instalar dependências
pip3 install pycaw comtypes psutil \
    --target addon/globalPlugins/audioVolumeControl/ \
    --upgrade --force-reinstall

# 4. Compilar
scons

# 5. Verificar (deve ter > 1MB)
ls -lh audioVolumeControl-1.0.0.nvda-addon

# 6. Servir via HTTP
python3 -m http.server 8000
```

---

## 💻 NO WINDOWS (Instalar)

### **1. Baixar o arquivo**
Abra navegador: `http://IP_DO_LINUX:8000/`
Baixe: `audioVolumeControl-1.0.0.nvda-addon`

### **2. Fechar NVDA**
```
Ctrl + NVDA + Q
```
Aguarde 10 segundos

### **3. Limpar instalação antiga**

**Opção A - Explorador:**
1. `Win + R`
2. Digite: `%APPDATA%\nvda\addons`
3. Delete:
   - `audioVolumeControl`
   - `audioVolumeControl.pendingInstall`
   - Arquivos `.delete`

**Opção B - PowerShell (como Admin):**
```powershell
Stop-Process -Name nvda -Force -ErrorAction SilentlyContinue
Start-Sleep -Seconds 2
Remove-Item "$env:APPDATA\nvda\addons\audioVolumeControl*" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item "$env:APPDATA\nvda\addons\*.delete" -Recurse -Force -ErrorAction SilentlyContinue
```

### **4. Instalar**
1. Abra o NVDA
2. Duplo clique em `audioVolumeControl-1.0.0.nvda-addon`
3. Confirme instalação
4. Reinicie o NVDA

### **5. Verificar**

**Opção 1 - Testar atalho:**
```
Ctrl + NVDA + Y
```

**Opção 2 - Ver em Definir Comandos:**
1. `NVDA + N`
2. `Preferências → Definir Comandos`
3. Procure: "Audio Volume Control"
4. Deve aparecer: "Show the per-application volume control dialog"

---

## 🎯 O que foi corrigido:

1. ✅ Import do pycaw (`from pycaw import` em vez de `from pycaw.pycaw import`)
2. ✅ Categoria do script com tradução (`scriptCategory = _("Audio Volume Control")`)
3. ✅ Descrição do script traduzível

---

## 📋 Checklist Final:

- [ ] Código corrigido no Linux
- [ ] Recompilado com `scons`
- [ ] Arquivo > 1MB
- [ ] Transferido para Windows
- [ ] NVDA fechado
- [ ] Pasta antiga deletada
- [ ] Novo add-on instalado
- [ ] NVDA reiniciado
- [ ] Aparece em "Definir Comandos"
- [ ] Atalho `Ctrl+NVDA+Y` funciona

---

**Agora deve funcionar! 🎉**

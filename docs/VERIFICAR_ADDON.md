# 🔍 Verificação: Por que o Add-on Não Aparece

## ⚠️ IMPORTANTE: Você recompilou?

As correções que fiz foram no **código fonte**. Se você não recompilou no Linux, ainda está usando a versão antiga!

---

## 📋 Checklist de Verificação

### **1. Você recompilou no Linux após as correções?**
- [ ] Sim, recompilei com `scons`
- [ ] Não, ainda estou usando o arquivo antigo

**Se NÃO recompilou, PARE AQUI e recompile primeiro!**

---

## 🔎 Verificações no Windows

### **Verificação 1: Add-on está instalado?**

1. Abra NVDA
2. `NVDA + N` → `Ferramentas → Gerenciar Complementos`
3. Procure "Audio Volume Control"

**Resultado esperado:**
- ✅ Aparece na lista como "Ativado"
- ❌ Não aparece = não está instalado

---

### **Verificação 2: Add-on carregou sem erros?**

Abra o arquivo de log:
```
%APPDATA%\nvda\nvda.log
```

Procure por (Ctrl+F):
```
Audio Volume Control add-on initialized
```

**Resultados possíveis:**

✅ **Aparece "INFO - Audio Volume Control add-on initialized"**
   → Add-on carregou corretamente

❌ **Aparece "ERROR" antes dessa linha**
   → Houve erro no carregamento, copie o erro completo

❌ **Não aparece nada sobre "Audio Volume Control"**
   → Add-on não foi carregado

---

### **Verificação 3: Estrutura do add-on instalado**

Abra no Explorador:
```
%APPDATA%\nvda\addons\audioVolumeControl\globalPlugins\audioVolumeControl
```

**Deve conter:**
- [ ] `__init__.py`
- [ ] `audioSessionManager.py`
- [ ] `volumeController.py`
- [ ] `volumeControlDialog.py`
- [ ] Pasta `pycaw/`
- [ ] Pasta `comtypes/`
- [ ] Pasta `psutil/`

**Se faltam as pastas pycaw/comtypes/psutil:**
→ Problema na compilação, dependências não foram incluídas

---

### **Verificação 4: Arquivo compilado tem o tamanho correto?**

O arquivo `.nvda-addon` deve ter **mais de 1MB** (aproximadamente 1.5-2MB).

Se for menor que 100KB, as dependências não foram incluídas.

---

## 🛠️ Soluções por Problema

### **Problema A: "Add-on não aparece em Gerenciar Complementos"**

**Solução:**
1. Feche NVDA
2. Delete: `%APPDATA%\nvda\addons\audioVolumeControl`
3. Reinstale o `.nvda-addon`
4. Reinicie NVDA

---

### **Problema B: "Add-on aparece em Gerenciar Complementos mas não em Definir Comandos"**

**Causa:** Erro no carregamento do plugin

**Solução:**
1. Veja o log (`nvda.log`)
2. Procure por erros relacionados a "audioVolumeControl"
3. Copie o erro completo e me envie

---

### **Problema C: "Erro no log: No module named 'pycaw'"**

**Causa:** Dependências não foram incluídas na compilação

**Solução:** Recompilar no Linux:
```bash
cd /root/AddonTemplate-master
rm -f *.nvda-addon
pip3 install pycaw comtypes psutil \
    --target addon/globalPlugins/audioVolumeControl/ \
    --upgrade --force-reinstall
scons
```

---

## 🎯 Teste Definitivo

Execute este comando no PowerShell:

```powershell
# Ver se o add-on está instalado
Test-Path "$env:APPDATA\nvda\addons\audioVolumeControl\globalPlugins\audioVolumeControl\__init__.py"

# Ver últimas linhas do log relacionadas ao add-on
Get-Content "$env:APPDATA\nvda\nvda.log" | Select-String "audioVolumeControl" | Select-Object -Last 10
```

**Me envie o resultado desses comandos!**

---

## 📝 O que preciso saber:

1. **Você recompilou no Linux após as correções?**
2. **O add-on aparece em "Gerenciar Complementos"?**
3. **Qual é a última linha do log relacionada a "audioVolumeControl"?**

Com essas informações, posso identificar o problema exato! 🔍

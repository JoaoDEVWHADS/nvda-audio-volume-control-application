# 🔍 Diagnóstico - Add-on Não Aparece em "Definir Comandos"

## ❌ Problema
O add-on foi instalado, mas **não aparece** na lista de comandos do NVDA (NVDA → Preferências → Definir Comandos).

---

## 🔎 Possíveis Causas

### **1. Add-on Não Carregou (Erro no Import)**
O log anterior mostrou:
```
ERROR - external:globalPlugins.audioVolumeControl.audioSessionManager (20:04:17.608):
Failed to import dependencies: No module named 'pycaw.pycaw'
```

**Já corrigimos isso**, mas você precisa **recompilar** no Linux!

---

## ✅ Solução Completa

### **PASSO 1: Recompilar no Linux (OBRIGATÓRIO)**

O código foi corrigido, mas você ainda está usando a versão antiga compilada. Precisa recompilar:

```bash
# No Linux
cd /root/AddonTemplate-master

# Limpar tudo
rm -f *.nvda-addon
rm -rf addon/globalPlugins/audioVolumeControl/pycaw*
rm -rf addon/globalPlugins/audioVolumeControl/comtypes*
rm -rf addon/globalPlugins/audioVolumeControl/psutil*

# Reinstalar dependências
pip3 install pycaw comtypes psutil \
    --target addon/globalPlugins/audioVolumeControl/ \
    --upgrade --force-reinstall

# Compilar
scons

# Verificar tamanho (deve ter > 1MB)
ls -lh audioVolumeControl-1.0.0.nvda-addon
```

### **PASSO 2: Transferir Novo Arquivo**

```bash
# Servir via HTTP
python3 -m http.server 8000
```

No Windows, baixe o **NOVO** arquivo.

### **PASSO 3: Limpar Instalação Antiga no Windows**

1. **Fechar NVDA:** `Ctrl + NVDA + Q`
2. **Aguardar 10 segundos**
3. **Abrir pasta:** `Win + R` → `%APPDATA%\nvda\addons` → `Enter`
4. **Deletar:**
   - `audioVolumeControl`
   - `audioVolumeControl.pendingInstall`
   - Arquivos `.delete`

### **PASSO 4: Instalar Novo Add-on**

1. Abrir NVDA
2. Duplo clique no **NOVO** `.nvda-addon`
3. Reiniciar NVDA

### **PASSO 5: Verificar se Carregou**

Abra o log do NVDA:
```
%APPDATA%\nvda\nvda.log
```

Procure por:
```
INFO - Audio Volume Control add-on initialized
```

Se aparecer **ERROR** em vez de **INFO**, o add-on não carregou.

---

## 🧪 Teste Rápido

### **Verificar se o Add-on Está Instalado:**

1. Abra NVDA
2. `NVDA + N` (menu NVDA)
3. `Ferramentas → Gerenciar Complementos`
4. Procure por "Audio Volume Control"
5. Deve aparecer como **"Ativado"**

### **Verificar se Aparece em Definir Comandos:**

1. `NVDA + N`
2. `Preferências → Definir Comandos`
3. Procure por "Per-Application Volume Control" ou "Audio Volume"
4. Deve aparecer com o comando `Ctrl + NVDA + Y`

---

## 🐛 Se Ainda Não Funcionar

### **Verificar Log Detalhado:**

Abra: `%APPDATA%\nvda\nvda.log`

Procure por linhas com:
- `audioVolumeControl`
- `ERROR`
- `Failed to import`

### **Comandos de Diagnóstico (PowerShell):**

```powershell
# Ver se o add-on está instalado
Get-ChildItem "$env:APPDATA\nvda\addons\audioVolumeControl"

# Ver últimas linhas do log
Get-Content "$env:APPDATA\nvda\nvda.log" -Tail 50 | Select-String "audioVolumeControl"
```

### **Verificar Estrutura do Add-on Instalado:**

```
%APPDATA%\nvda\addons\audioVolumeControl\
├── manifest.ini                          ← Deve existir
├── globalPlugins\
│   └── audioVolumeControl\
│       ├── __init__.py                   ← Código principal
│       ├── pycaw\                        ← Dependência
│       ├── comtypes\                     ← Dependência
│       └── psutil\                       ← Dependência
```

Se as pastas `pycaw`, `comtypes` ou `psutil` **NÃO existirem**, o problema é na compilação.

---

## 📋 Checklist de Verificação

- [ ] Código foi corrigido (import de `pycaw`)
- [ ] Recompilou no Linux com o código corrigido
- [ ] Arquivo `.nvda-addon` tem mais de 1MB
- [ ] Limpou instalação antiga no Windows
- [ ] Instalou o novo `.nvda-addon`
- [ ] Reiniciou o NVDA
- [ ] Verificou o log (`nvda.log`) sem erros
- [ ] Add-on aparece em "Gerenciar Complementos" como "Ativado"
- [ ] Add-on aparece em "Definir Comandos"

---

## 🎯 Resumo do Problema

**Você ainda está usando a versão ANTIGA compilada antes da correção!**

A correção que fiz foi no **código fonte**, mas você precisa:
1. **Recompilar** no Linux
2. **Transferir** o novo arquivo
3. **Reinstalar** no Windows

Só assim a correção vai funcionar! 🚀

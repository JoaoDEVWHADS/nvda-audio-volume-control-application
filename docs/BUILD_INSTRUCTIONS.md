# 🚀 Instruções de Build - Add-on NVDA

## Passo a Passo para Construir o Add-on

### 1️⃣ Instalar Dependências (Opcional mas Recomendado)

As dependências podem ser bundled (incluídas) no add-on ou instaladas no ambiente Python do NVDA.

#### Opção A: Bundling (Recomendado para Distribuição)

**No Windows:**
```powershell
cd c:\Users\Noah\Documents\joao\AddonTemplate-master
.\install_dependencies.ps1
```

**No Linux:**
```bash
cd /c/Users/Noah/Documents/joao/AddonTemplate-master
chmod +x install_dependencies.sh
./install_dependencies.sh
```

Isso criará a pasta `addon/lib/` com:
- pycaw
- comtypes
- psutil

#### Opção B: Instalação no NVDA (Para Desenvolvimento)

```bash
# Encontre o Python do NVDA (geralmente em C:\Program Files (x86)\NVDA\)
cd "C:\Program Files (x86)\NVDA"
python -m pip install pycaw comtypes psutil
```

### 2️⃣ Construir o Pacote .nvda-addon

```bash
cd c:\Users\Noah\Documents\joao\AddonTemplate-master
scons
```

**Saída esperada:**
```
Compiling...
Creating manifest...
Building add-on package...
audioVolumeControl-1.0.0.nvda-addon created successfully!
```

**Arquivo gerado:** `audioVolumeControl-1.0.0.nvda-addon`

### 3️⃣ Verificar o Pacote

```bash
# Listar conteúdo do pacote (é um arquivo ZIP)
unzip -l audioVolumeControl-1.0.0.nvda-addon
```

**Conteúdo esperado:**
```
manifest.ini
addon/
  globalPlugins/
    audioVolumeControl/
      __init__.py
      audioSessionManager.py
      volumeController.py
      volumeControlDialog.py
  doc/
    en/
      readme.html
  locale/
    en/
      LC_MESSAGES/
```

### 4️⃣ Instalar no NVDA (Windows)

#### Método 1: Duplo Clique
1. Navegue até `audioVolumeControl-1.0.0.nvda-addon`
2. Pressione Enter ou duplo clique
3. NVDA perguntará se deseja instalar
4. Clique "Sim"
5. Reinicie o NVDA quando solicitado

#### Método 2: Via Menu NVDA
1. Abra NVDA
2. NVDA Menu → Ferramentas → Gerenciar complementos
3. Clique "Instalar"
4. Navegue até o arquivo `.nvda-addon`
5. Selecione e abra
6. Reinicie o NVDA

### 5️⃣ Verificar Instalação

Após reiniciar o NVDA:

1. Pressione **Ctrl+NVDA+Y**
2. O diálogo deve abrir
3. Se houver apps com áudio, eles aparecerão na lista

### 6️⃣ Testar Funcionalidade

**Teste Básico:**
1. Abra YouTube no navegador
2. Inicie um vídeo
3. Pressione Ctrl+NVDA+Y
4. Navegue até o navegador na lista
5. Teste ajustar volume com setas

**Teste Completo:**
- [ ] Abrir diálogo (Ctrl+NVDA+Y)
- [ ] Listar múltiplos apps
- [ ] Verificar ordenação alfabética
- [ ] Testar seleção automática
- [ ] Ajustar volume +1% (Seta Direita)
- [ ] Ajustar volume -1% (Seta Esquerda)
- [ ] Ajustar volume +5% (Seta Cima)
- [ ] Ajustar volume -5% (Seta Baixo)
- [ ] Ajustar volume +10% (Page Up)
- [ ] Ajustar volume -10% (Page Down)
- [ ] Volume 0% (Home)
- [ ] Volume 100% (End)
- [ ] Mute/Unmute (M)
- [ ] Refresh lista (R)
- [ ] Verificar anúncios NVDA

---

## 🔧 Troubleshooting

### Problema: "scons: command not found"

**Solução:**
```bash
pip install scons
```

### Problema: "Dependencies not available"

**Causa:** pycaw, comtypes ou psutil não instalados.

**Solução:**
```bash
# Opção 1: Bundle com add-on
.\install_dependencies.ps1

# Opção 2: Instalar no NVDA
cd "C:\Program Files (x86)\NVDA"
python -m pip install pycaw comtypes psutil
```

### Problema: "No active audio sessions found"

**Causa:** Nenhum aplicativo está tocando áudio.

**Solução:**
1. Abra YouTube, Spotify, ou qualquer player
2. Inicie reprodução de áudio
3. Pressione R no diálogo para refresh

### Problema: "Error loading audio sessions"

**Possíveis causas:**
- Serviço de áudio do Windows não está rodando
- Permissões insuficientes
- Conflito com outro software de áudio

**Soluções:**
1. Reinicie o serviço de áudio do Windows
2. Execute NVDA como administrador
3. Verifique logs do NVDA (NVDA+F1)

### Problema: Build falha com erro de encoding

**Solução:**
```bash
# Defina encoding UTF-8
set PYTHONIOENCODING=utf-8
scons
```

---

## 📦 Distribuição

### Criar Release

1. **Build do pacote:**
   ```bash
   scons
   ```

2. **Testar instalação:**
   - Instale em máquina limpa
   - Teste todas as funcionalidades
   - Verifique compatibilidade

3. **Criar release no GitHub:**
   ```bash
   git tag v1.0.0
   git push origin v1.0.0
   ```

4. **Upload do arquivo:**
   - Faça upload de `audioVolumeControl-1.0.0.nvda-addon`
   - Adicione notas de release do `changelog.md`

### Submeter para NVDA Add-on Store

1. Crie conta no [NVDA Add-on Store](https://github.com/nvaccess/addon-datastore)
2. Fork do repositório addon-datastore
3. Adicione seu add-on seguindo as diretrizes
4. Crie pull request
5. Aguarde revisão da comunidade

---

## 🔄 Desenvolvimento Contínuo

### Fazer Alterações

1. **Edite os arquivos Python:**
   ```bash
   cd addon/globalPlugins/audioVolumeControl
   # Edite __init__.py, volumeController.py, etc.
   ```

2. **Rebuild:**
   ```bash
   scons
   ```

3. **Reinstale no NVDA:**
   - Desinstale versão antiga
   - Instale nova versão
   - Reinicie NVDA

### Atualizar Versão

1. **Edite `buildVars.py`:**
   ```python
   addon_version="1.1.0"
   ```

2. **Atualize `changelog.md`:**
   ```markdown
   ## Version 1.1.0
   - Nova funcionalidade X
   - Correção de bug Y
   ```

3. **Rebuild:**
   ```bash
   scons
   ```

---

## 📊 Checklist de Release

Antes de distribuir:

- [ ] Todas as funcionalidades testadas
- [ ] Documentação atualizada
- [ ] Changelog atualizado
- [ ] Versão incrementada em buildVars.py
- [ ] Build sem erros
- [ ] Instalação testada em máquina limpa
- [ ] Compatibilidade verificada (Windows 10/11)
- [ ] NVDA versões testadas (2019.3 - 2024.4)
- [ ] Dependências incluídas ou documentadas
- [ ] Licença GPL v2 incluída

---

## 🎯 Comandos Rápidos

```bash
# Build
scons

# Build com versão customizada
scons version=1.1.0

# Build de desenvolvimento (usa data atual)
scons dev=1

# Gerar template de tradução
scons pot

# Limpar build
scons -c

# Instalar dependências
.\install_dependencies.ps1  # Windows
./install_dependencies.sh   # Linux
```

---

## 📝 Notas Finais

- ✅ O add-on está pronto para build
- ✅ Todas as dependências estão documentadas
- ✅ Scripts de instalação criados
- ✅ Documentação completa
- ⏳ Aguardando teste no Windows com NVDA

**Próxima ação:** Execute `scons` para criar o pacote!

---

**Boa sorte com o build! 🚀**

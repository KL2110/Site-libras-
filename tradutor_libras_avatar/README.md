# Assistente de Acessibilidade: Tradutor de Voz para Libras (SENAI) 🤟

Este projeto é um MVP (Mínimo Produto Viável) de um **Tradutor de Voz (Português Falado) para Libras Visual** em tempo real, projetado para inclusão de alunos surdos ou com deficiência auditiva em aulas práticas e oficinas do ecossistema **SENAI**.

O sistema captura o áudio do instrutor, transcreve em texto de forma local usando Inteligência Artificial (OpenAI Whisper / Google Speech API) e mapeia as palavras-chave para uma sequência de sinais de Libras reproduzidos por um avatar (com suporte a soletrar em alfabeto datilológico caso a palavra seja nova).

---

## 🛠️ Tecnologias Utilizadas

- **Python 3.10+** (Linguagem do Backend)
- **Streamlit** (Interface Web leve, interativa e de rápida implementação)
- **SpeechRecognition & OpenAI Whisper** (Modelos de IA para Speech-to-Text rodando offline/local)
- **HTML5 & Custom CSS** (Estilização premium, com alto contraste e acessibilidade visual)

---

## 📁 Estrutura do Projeto

```text
tradutor_libras_avatar/
│
├── assets/
│   └── sinais/          # Pasta onde você deve colar seus arquivos de vídeo/GIF do avatar
│       ├── perigo.gif   # Exemplo: Sinal de perigo animado
│       ├── atencao.gif  # Exemplo: Sinal de atenção animado
│       └── [outros]
│
├── app.py               # Arquivo principal do aplicativo Streamlit
├── requirements.txt     # Dependências do Python
└── README.md            # Documentação e instruções de configuração
```

---

## 🚀 Como Executar o Projeto Localmente

Siga o passo a passo abaixo para rodar o projeto na sua máquina:

### 1. Criar e Ativar Ambiente Virtual (Recomendado)
No terminal do seu editor (VS Code), navegue até a pasta do projeto e execute:

```bash
# Criar ambiente virtual python
python -m venv venv

# Ativar no Windows (PowerShell)
.\venv\Scripts\Activate.ps1

# Ou ativar no Windows (Prompt de Comando CMD)
.\venv\Scripts\activate.bat
```

### 2. Instalar as Dependências
Com o ambiente virtual ativado, instale as bibliotecas necessárias:

```bash
pip install -r requirements.txt
```

> **Nota sobre Áudio no Windows:** O aplicativo utiliza o componente nativo `st.audio_input` do Streamlit, eliminando a necessidade de compilar o `pyaudio` na máquina local, o que evita 90% dos erros comuns de instalação em sistemas Windows.

### 3. Rodar a Interface Web (Streamlit)
Execute o comando abaixo para iniciar o servidor local:

```bash
streamlit run app.py
```

O aplicativo será aberto automaticamente no seu navegador padrão no endereço `http://localhost:8501`.

---

## 🎨 Como Alimentar o Avatar (GIFs e Vídeos)

Para o MVP rodar imediatamente, criamos um **sistema de Fallback inteligente com emojis e descrições textuais dos movimentos**.

Para colocar o seu próprio avatar 3D ou animação real:
1. Grave ou renderize o sinal (usando Blender, Unity ou gravando de fontes públicas como o VLibras).
2. Salve o arquivo no formato `.gif` (ou `.png` / `.jpg`).
3. Cole o arquivo dentro da pasta `assets/sinais/`.
4. Garanta que o nome do arquivo seja exatamente igual à palavra-chave cadastrada em minúsculas (exemplo: `assets/sinais/perigo.gif` ou `assets/sinais/martelo.gif`).
5. Ao reproduzir, o Streamlit automaticamente detectará a existência do arquivo físico e renderizará o vídeo do seu avatar no lugar do emoji!

---

## 🎯 Apresentação para a Banca do SENAI

### Argumentos de Inovação Industrial (Pitch)
1. **Segurança Aumentada (EHS):** O instrutor pode alertar sobre riscos no chassi ou na máquina elétrica e o aluno surdo recebe o aviso visual na tela instantaneamente, evitando acidentes industriais.
2. **Custo Zero de Infraestrutura (Edge-First):** Roda localmente em computadores normais das escolas do SENAI. Não requer internet rápida ou placas de vídeo caras (GPUs).
3. **Escalabilidade Educacional:** O mesmo código pode ser replicado em qualquer oficina mecânica, de soldagem, panificação ou eletrônica do ecossistema SENAI nacional.

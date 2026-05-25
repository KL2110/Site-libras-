import streamlit as st
import speech_recognition as sr
import time
import os
import re
import requests
import unicodedata
from io import BytesIO
import streamlit.components.v1 as components
from utils import transcrever_audio
from pathlib import Path

# --------- FUNÇÃO AUXILIAR ---------
def remover_acentos(texto):
    """Remove acentuações de um texto usando normalização Unicode"""
    nfd = unicodedata.normalize('NFD', texto)
    return ''.join(char for char in nfd if unicodedata.category(char) != 'Mn')

# --------- CONFIGURAÇÃO DE HEADERS ---------
HEADERS_NAVEGADOR = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

# Configuração da Página do Streamlit com tema premium e acessível
st.set_page_config(
    page_title="Tradutor de Voz para Libras (SENAI)",
    page_icon="🤟",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Carrega estilos a partir do arquivo CSS separado para organização
css_path = Path(__file__).parent / "assets" / "frontend.css"
try:
    css = css_path.read_text(encoding='utf-8')
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
except Exception:
    # Fallback mínimo caso o arquivo não exista
    st.markdown("""
        <style>
            .main-title{ color:#3b82f6 }
        </style>
    """, unsafe_allow_html=True)

# Transcrição: agora delegada para `utils.transcrever_audio` para melhor organização

# ----------------- INTERFACE DO USUÁRIO (UI) -----------------

# Cabeçalho Principal
st.markdown("""
    <div class="title-container">
        <h1 class="main-title">Tradutor de Voz para Libras 🤟</h1>
        <p class="subtitle">Assistente de Acessibilidade 3D em Tempo Real para Aulas Práticas do SENAI</p>
    </div>
""", unsafe_allow_html=True)

# Layout em duas colunas (Esquerda: Entrada de Áudio e Controles | Direita: Visualizador do Avatar)
col1, col2 = st.columns([1, 1])

# Inicialização de Variáveis de Estado
if "transcricao" not in st.session_state:
    st.session_state.transcricao = ""
if "history" not in st.session_state:
    st.session_state.history = []
if "translations_count" not in st.session_state:
    st.session_state.translations_count = 0
if "mic_status" not in st.session_state:
    st.session_state.mic_status = "idle"  # idle, listening, translating
if "last_rendered_transcricao" not in st.session_state:
    st.session_state.last_rendered_transcricao = ""

# --- COLUNA 1: ENTRADA E CONTROLES ---
with col1:
    st.markdown("### 🎙️ Captura de Voz do Instrutor")
    
    st.markdown("""
    <div class="glass-card">
        <strong>Instruções de Uso:</strong><br>
        1. Fale a sua instrução no microfone abaixo.<br>
        2. Clique em "Traduzir Fala ➔ Libras" para processar a frase.<br>
        3. O sistema exibirá as letras em Libras uma a uma no painel da direita.
    </div>
    """, unsafe_allow_html=True)
    
    # Componente de gravação nativo do Streamlit
    audio_capturado = st.audio_input("Grave a instrução da aula:")
    
    # Processar áudio se gravado
    if audio_capturado is not None:
        if st.button("Traduzir Fala ➔ Libras", type="primary", use_container_width=True):
            st.session_state.mic_status = "translating"
            with st.spinner("IA processando áudio..."):
                texto_transcrito = transcrever_audio(audio_capturado)
                st.session_state.transcricao = texto_transcrito
                # Atualiza histórico e contador
                if texto_transcrito:
                    st.session_state.history.insert(0, texto_transcrito)
                    st.session_state.translations_count += 1
            st.session_state.mic_status = "idle"
    
    # Exibir Legenda Transcrita
    st.markdown("### 📝 Legenda em Tempo Real")
    if st.session_state.transcricao:
        st.markdown(f"""
        <div class="glass-card" style="font-size: 1.3rem; border-left: 5px solid #3b82f6;">
            "{st.session_state.transcricao}"
        </div>
        """, unsafe_allow_html=True)
    else:
        st.info("Aguardando áudio do instrutor. Fale no microfone acima.")

# --- SIDEBAR (CONFIGURAÇÕES DO SISTEMA) ---
with st.sidebar:
    st.markdown("""
        <div class="logo-container">
            <h2 class="logo-text">SENAI</h2>
            <p class="logo-sub">Tecnologia da Informação</p>
        </div>
    """, unsafe_allow_html=True)
    st.markdown("---")
    
    st.markdown("### ℹ️ Sobre o Assistente de Libras")
    st.write(
        "Este MVP integra o reconhecimento de voz local (Python) com uma visualização local do alfabeto manual em Libras. "
        "A cada frase reconhecida, o sistema mostra as letras correspondentes em sequência." 
    )
    
    st.markdown("---")
    st.markdown("### 💡 Dica para a Apresentação")
    st.info(
        "Ao falar termos técnicos de oficina (ex: Torno, Fresa, Calibrador), "
        "o sistema exibirá as letras em Libras correspondentes ao texto transcrito."
    )
    
    st.markdown("---")
    st.caption("Desenvolvido para o TCC da Turma de TI - SENAI 2026. Foco em Acessibilidade e Inclusão Industrial.")
    st.markdown("---")
    st.markdown("### 🔢 Estatísticas")
    st.markdown(f"- **Traduções realizadas:** {st.session_state.translations_count}")
    mic_label = "🔴 Desativado" if st.session_state.mic_status == 'idle' else ("🟡 Traduzindo" if st.session_state.mic_status=='translating' else "🟢 Ouvindo")
    st.markdown(f"- **Microfone:** {mic_label}")
    st.markdown("---")
    st.markdown("### 🕘 Histórico de Transcrições")
    if st.session_state.history:
        for i, item in enumerate(st.session_state.history[:8]):
            st.markdown(f"- {item}")
        if st.button("Limpar Histórico"):
            st.session_state.history = []
    else:
        st.info("Nenhuma transcrição ainda.")

# --- COLUNA 2: PAINEL DO AVATAR ---
with col2:
    st.markdown("### 🤟 Avatar 3D Tradutor de Libras")

    # Div de Status com feedback de UX
    if st.session_state.mic_status == 'translating':
        status_html = '<span class="status-badge status-active">TRADUZINDO...</span>'
    elif st.session_state.mic_status == 'listening':
        status_html = '<span class="status-badge status-active">OUVINDO</span>'
    elif st.session_state.transcricao:
        status_html = '<span class="status-badge status-active">AVATAR SINALIZANDO</span>'
    else:
        status_html = '<span class="status-badge status-idle">PRONTO / AGUARDANDO VOZ</span>'

    st.markdown(status_html, unsafe_allow_html=True)

    # Configura diretórios de assets com criação automática
    PASTA_ALFABETO = Path(__file__).parent / "assets" / "alfabeto"
    PASTA_DICIONARIO_LOCAL = Path(__file__).parent / "assets" / "dicionario_local"
    
    PASTA_ALFABETO.mkdir(parents=True, exist_ok=True)
    PASTA_DICIONARIO_LOCAL.mkdir(parents=True, exist_ok=True)

    # Carrega lookup de imagens locais para fallback (datilologia)
    image_lookup = {}
    if PASTA_ALFABETO.exists():
        for imagem in PASTA_ALFABETO.rglob("*.png"):
            nome = imagem.stem.lower().replace(" ", "").replace("letra", "").strip()
            if len(nome) == 1 and nome.isalpha():
                image_lookup[nome] = imagem

    with st.container(border=True):
        st.markdown("#### 🎬 Dicionário de Libras (3 Planos)")

        if st.session_state.transcricao:
            # Limpa a transcrição: remove pontuações e converte para minúsculas
            texto_limpo = re.sub(r"[^a-z0-9\s]", "", st.session_state.transcricao.lower(), flags=re.UNICODE)
            texto_limpo = texto_limpo.strip()
            palavras = texto_limpo.split()

            if palavras:
                # Cria placeholders fixos ANTES do loop para evitar empilhamento
                placeholder_texto = st.empty()
                placeholder_video = st.empty()
                
                for palavra in palavras:
                    primeira_letra = palavra[0]
                    palavra_limpa = remover_acentos(palavra)
                    video_encontrado = False
                    
                    # --------- PLANO DE CONTINGÊNCIA LOCAL (Prioridade 1) ---------
                    # Verifica se a palavra existe localmente (ex: "torno.mp4" ou "torno.gif")
                    for extensao in ['.mp4', '.gif', '.webm']:
                        arquivo_local = PASTA_DICIONARIO_LOCAL / f"{palavra_limpa}{extensao}"
                        if arquivo_local.exists():
                            video_encontrado = True
                            placeholder_texto.markdown(f"**Termo técnico: {palavra.upper()}** (Local)")
                            if extensao in ['.mp4', '.webm']:
                                placeholder_video.video(str(arquivo_local), autoplay=True, loop=True, muted=True)
                            else:
                                # GIF renderizado como imagem
                                placeholder_video.image(str(arquivo_local))
                            time.sleep(4.0)
                            break
                    
                    # --------- PLANO A: INES COM HEADERS (Prioridade 2) ---------
                    if not video_encontrado:
                        urls_para_tentar = [
                            f"https://www.ines.gov.br/dicionario-de-libras/videos/{primeira_letra}/{palavra_limpa}.mp4",
                            f"http://www.ines.gov.br/dicionario-de-libras/videos/{primeira_letra}/{palavra_limpa}.mp4"
                        ]
                        
                        for url_ines in urls_para_tentar:
                            if video_encontrado:
                                break
                            try:
                                resposta = requests.get(
                                    url_ines, 
                                    timeout=2.5, 
                                    stream=True, 
                                    allow_redirects=True,
                                    headers=HEADERS_NAVEGADOR
                                )
                                if resposta.status_code == 200:
                                    video_encontrado = True
                                    placeholder_texto.markdown(f"**Palavra: {palavra.upper()}** (INES)")
                                    placeholder_video.video(url_ines, autoplay=True, loop=True, muted=True)
                                    time.sleep(4.0)
                            except Exception:
                                pass
                    
                    # --------- PLANO B: DATILOLOGIA LOCAL (Prioridade 3) ---------
                    if not video_encontrado:
                        placeholder_texto.markdown(f"**Datilologia: {palavra.upper()}**")
                        for letra in palavra:
                            if letra == " ":
                                placeholder_video.markdown(
                                    "<div style='height:280px; display:flex; align-items:center; justify-content:center; color:#64748b; font-size:1.1rem;'>Espaço</div>",
                                    unsafe_allow_html=True
                                )
                            else:
                                imagem_path = image_lookup.get(letra)
                                if imagem_path and imagem_path.exists():
                                    placeholder_texto.markdown(f"**Soletrado: {letra.upper()}**")
                                    placeholder_video.image(str(imagem_path), width=280)
                                else:
                                    placeholder_video.markdown(
                                        f"<div style='height:280px; display:flex; align-items:center; justify-content:center; color:#f97316; font-size:1rem;'>Letra '{letra}' não encontrada</div>",
                                        unsafe_allow_html=True
                                    )
                            time.sleep(0.8)
            else:
                st.info("Aguardando voz...")
        else:
            st.markdown("""
            <div style='height:300px; display:flex; flex-direction:column; align-items:center; justify-content:center; color:#94a3b8; text-align:center;'>
                <div style='font-size:2.5rem; margin-bottom:16px;'>🎤</div>
                <div style='font-size:1.1rem; font-weight:500;'>Sistema Pronto</div>
                <div style='font-size:0.95rem; margin-top:8px;'>Fale no microfone para traduzir em Libras</div>
            </div>
            """, unsafe_allow_html=True)


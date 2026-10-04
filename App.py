import streamlit as st

# Configuração inicial da página
st.set_page_config(
    page_title="QG das Batidas - Cardápio Oficial",
    page_icon="🍸",
    layout="wide"
)

# --- FUNÇÃO DO EFEITO MATRIX NO PLANO DE FUNDO ---
def adicionar_efeito_matrix():
    st.markdown("""
        <style>
        /* Garante que o fundo geral do app fique totalmente escuro */
        .stApp {
            background-color: #0d0d0d;
        }
        /* Estilo do canvas do Matrix cobrindo toda a tela ao fundo */
        #matrix-canvas {
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw;
            height: 100vh;
            z-index: 0;
            pointer-events: none;
            opacity: 0.22; /* Suave para não atrapalhar a leitura dos produtos */
        }
        /* Mantém o conteúdo e os cartões do Streamlit acima do fundo Matrix */
        .main .block-container {
            position: relative;
            z-index: 1;
        }
        </style>

        <canvas id="matrix-canvas"></canvas>

        <script>
        const canvas = document.getElementById('matrix-canvas');
        const ctx = canvas.getContext('2d');

        function resizeCanvas() {
            canvas.width = window.innerWidth;
            canvas.height = window.innerHeight;
        }
        resizeCanvas();
        window.addEventListener('resize', resizeCanvas);

        const katakana = 'アァカサタナハマヤャラワガザダバパイィキシチニヒミリヰギジヂビピウゥクスツヌフムユュルグズブヅプエェケセテネヘメレヱゲゼデベペオォコソトノホモヨョロヲゴゾドボポヴッン';
        const numbers = '0123456789';
        const alphabet = katakana + numbers;

        const fontSize = 16;
        let columns = Math.floor(canvas.width / fontSize);

        const rainDrops = [];
        for (let x = 0; x < columns; x++) {
            rainDrops[x] = 1;
        }

        function drawMatrix() {
            ctx.fillStyle = 'rgba(13, 13, 13, 0.05)';
            ctx.fillRect(0, 0, canvas.width, canvas.height);

            ctx.fillStyle = '#00FF7F'; // Verde neon característico
            ctx.font = fontSize + 'px monospace';

            for (let i = 0; i < rainDrops.length; i++) {
                const text = alphabet.charAt(Math.floor(Math.random() * alphabet.length));
                ctx.fillText(text, i * fontSize, rainDrops[i] * fontSize);

                ifMestre Sidney, aqui está o **código completo** do seu arquivo principal (`app.py`), já unindo a configuração do sistema, o fundo com o **efeito Matrix**, o menu de navegação e as páginas da sua aplicação (incluindo o cardápio e a gestão). 

Basta copiar este bloco inteiro e substituir no seu arquivo principal (`app.py`):

```python
import streamlit as st

# Configuração da página principal (deve ser a primeira chamada do Streamlit)
st.set_page_config(
    page_title="QG das Batidas",
    page_icon="🍸",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- FUNÇÃO DO EFEITO MATRIX NO FUNDO ---
def adicionar_efeito_matrix():
    st.markdown("""
        <style>
        /* Garante que o fundo geral do app fique totalmente escuro */
        .stApp {
            background-color: #0d0d0d;
            color: #ffffff;
        }
        /* Estilo do canvas do Matrix cobrindo toda a tela ao fundo */
        #matrix-canvas {
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw;
            height: 100vh;
            z-index: 0;
            pointer-events: none;
            opacity: 0.20; /* Fundo suave para não atrapalhar a leitura */
        }
        /* Mantém todo o conteúdo do Streamlit acima do fundo Matrix */
        .main .block-container {
            position: relative;
            z-index: 1;
        }
        </style>

        <canvas id="matrix-canvas"></canvas>

        <script>
        const canvas = document.getElementById('matrix-canvas');
        const ctx = canvas.getContext('2d');

        function resizeCanvas() {
            canvas.width = window.innerWidth;
            canvas.height = window.innerHeight;
        }
        resizeCanvas();
        window.addEventListener('resize', resizeCanvas);

        const katakana = 'アァカサタナハマヤャラワガザダバパイィキシチニヒミリヰギジヂビピウゥクスツヌフムユュルグズブヅプエェケセテネヘメレヱゲゼデベペオォコソトノホモヨョロヲゴゾドボポヴッン';
        const numbers = '0123456789';
        const alphabet = katakana + numbers;

        const fontSize = 16;
        let columns = Math.floor(canvas.width / fontSize);

        const rainDrops = [];
        for (let x = 0; x < columns; x++) {
            rainDrops[x] = 1;
        }

        function drawMatrix() {
            ctx.fillStyle = 'rgba(13, 13, 13, 0.05)';
            ctx.fillRect(0, 0, canvas.width, canvas.height);

            ctx.fillStyle = '#00FF7F'; // Verde neon estilo QG das Batidas
            ctx.font = fontSize + 'px monospace';

            for (let i = 0; i < rainDrops.length; i++) {
                const text = alphabet.charAt(Math.floor(Math.random() * alphabet.length));
                ctx.fillText(text, i * fontSize, rainDrops[i] * fontSize);

                if (rainDrops[i] * fontSize > canvas.height && Math.random() > 0.975) {
                    rainDrops[i] = 0;
                }
                rainDrops[i]++;
            }
        }

        setInterval(drawMatrix, 30);
        </script>
    """, unsafe_allow_html=True)

# Ativa o efeito Matrix no fundo de todas as telas
adicionar_efeito_matrix()

# --- IMPORTAÇÃO DAS VIEWS/PÁGINAS DO SISTEMA ---
from views import vitrine_cardapio, pedidos_admin

# Menu de navegação lateral
st.sidebar.markdown("### 🍸 QG das Batidas")
st.sidebar.markdown("Painel de Controle e Vendas")

pagina = st.sidebar.radio(
    "Navegação:",
    ["🛒 Cardápio (Vitrine do Cliente)", "📊 Painel de Pedidos (Admin)"]
)

st.sidebar.markdown("---")
st.sidebar.info("💡 **Dica:** O sistema está integrado com salvamento de pedidos e CEP automático.")

# --- ROTEAMENTO DAS PÁGINAS ---
if pagina == "🛒 Cardápio (Vitrine do Cliente)":
    try:
        vitrine_cardapio.render()
    except Exception as e:
        st.error(f"Erro ao carregar a vitrine do cardápio: {e}")

elif pagina == "📊 Painel de Pedidos (Admin)":
    try:
        pedidos_admin.render()
    except Exception as e:
        st.error(f"Erro ao carregar o painel administrativo: {e}")
    

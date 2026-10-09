import streamlit as st
import json
import os
import random
import datetime
import sqlite3

st.set_page_config(
    page_title="QG das Batidas",
    page_icon="🍸",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- CONFIGURAÇÃO DO BANCO DE DADOS SQLITE ---
def init_db():
    conn = sqlite3.connect("qg_batidas.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS produtos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            categoria TEXT,
            preco_base REAL,
            descricao TEXT,
            status TEXT DEFAULT 'Disponível'
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pedidos (
            pedido_id TEXT PRIMARY KEY,
            timestamp TEXT,
            data_hora TEXT,
            cliente TEXT,
            whatsapp TEXT,
            nascimento TEXT,
            endereco TEXT,
            pagamento TEXT,
            status TEXT,
            total REAL
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS caixa (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data_hora TEXT,
            tipo TEXT,
            descricao TEXT,
            valor REAL
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS crm_clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            whatsapp TEXT,
            preferencia TEXT,
            compras_totais INTEGER DEFAULT 0
        )
    """)
    conn.commit()
    conn.close()

init_db()

def adicionar_estilo_moderno():
    st.markdown("""
        <style>
        .stApp {
            background-color: #0b0b0b;
            color: #ffffff;
        }
        #matrix-canvas {
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw;
            height: 100vh;
            z-index: 0;
            pointer-events: none;
            opacity: 0.12;
        }
        .main .block-container {
            position: relative;
            z-index: 1;
            padding-top: 1.5rem;
            padding-bottom: 5rem;
        }
        .hero-banner {
            background: linear-gradient(135deg, rgba(0, 255, 127, 0.15) 0%, rgba(255, 184, 0, 0.1) 100%);
            border: 1px solid rgba(0, 255, 127, 0.3);
            border-radius: 16px;
            padding: 24px;
            text-align: center;
            margin-bottom: 20px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.4);
        }
        .badge-loja {
            background: rgba(0, 255, 127, 0.2);
            color: #00FF7F;
            border: 1px solid rgba(0, 255, 127, 0.5);
            border-radius: 30px;
            padding: 5px 15px;
            font-size: 0.8rem;
            font-weight: 700;
            display: inline-block;
            letter-spacing: 0.5px;
            margin-bottom: 10px;
        }
                .detalhe-batida {
            color: #e0e0e0 !important;
            font-size: 1.1rem !important;
            line-height: 1.5 !important;
            font-weight: 400 !important;
            display: block;
            margin-bottom: 14px;
        }
        .preco-destaque {
            color: #FFB800;
            font-size: 1.45rem;
            font-weight: 850;
        }
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
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
            ctx.fillStyle = 'rgba(11, 11, 11, 0.05)';
            ctx.fillRect(0, 0, canvas.width, canvas.height);

            ctx.fillStyle = '#00FF7F';
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

adicionar_estilo_moderno()

if "carrinho" not in st.session_state:
    st.session_state.carrinho = []
if "pagina_atual" not in st.session_state:
    st.session_state.pagina_atual = "🛒 Cardápio"
if "ultimo_pedido" not in st.session_state:
    st.session_state.ultimo_pedido = None
if "categoria_ativa" not in st.session_state:
    st.session_state.categoria_ativa = "⭐ Especiais da Casa"

col_nav1, col_nav2, col_nav3 = st.columns([2, 2, 2])
with col_nav1:
    if st.button("🛒 Cardápio (Vitrine)", use_container_width=True):
        st.session_state.pagina_atual = "🛒 Cardápio"
        st.rerun()
with col_nav2:
    if st.button("🛍 Ver Carrinho & Checkout", use_container_width=True):
        st.session_state.pagina_atual = "🛍 Carrinho"
        st.rerun()
with col_nav3:
    if st.button("📊 Painel Admin", use_container_width=True):
        st.session_state.pagina_atual = "📊 Admin"
        st.rerun()

st.markdown("---")
        cardapio_detalhado = [
    {"id": 1, "nome": "Batida Tropical de Morango", "categoria": "⭐ Especiais da Casa", "preco_base": 32.00, "desc": "Morangos frescos selecionados, xarope de açúcar, vodka premium e gelo triturado."},
    {"id": 2, "nome": "Batida de Maracujá Clássica", "categoria": "⭐ Especiais da Casa", "preco_base": 32.00, "desc": "Polpa de maracujá azedo natural, leite condensado, cachaça branca e gelo."},
    {"id": 3, "nome": "Batida de Ninho com Nutella", "categoria": "⭐ Especiais da Casa", "preco_base": 38.00, "desc": "Creme cremoso de Leite Ninho, toque generoso de Nutella original e vodka."},
    {"id": 4, "nome": "Batida de Maracujá com Leite Condensado", "categoria": "⭐ Especiais da Casa", "preco_base": 32.00, "desc": "A clássica acidez do maracujá equilibrada com a doçura do leite condensado."},
    {"id": 5, "nome": "Batida de Morango com Leite Condensado", "categoria": "⭐ Especiais da Casa", "preco_base": 32.00, "desc": "Morangos frescos batidos na hora com leite condensado e vodka."},
    {"id": 6, "nome": "Batida de Abacaxi com Hortelã", "categoria": "⭐ Especiais da Casa", "preco_base": 32.00, "desc": "Abacaxi fresco, folhas de hortelã batidas, rum branco e gelo."},
    {"id": 7, "nome": "Batida de Limão com Leite Condensado", "categoria": "⭐ Especiais da Casa", "preco_base": 30.00, "desc": "Limão tahiti fresco, leite condensado e cachaça artesanal."},

    {"id": 8, "nome": "Batida Cocadinha Tropical", "categoria": "🥥 Clássicas & Tropicais", "preco_base": 30.00, "desc": "Leite de coco concentrado, rum branco, leite condensado e coco ralado."},
    {"id": 9, "nome": "Batida de Coco Cremoso", "categoria": "🥥 Clássicas & Tropicais", "preco_base": 30.00, "desc": "Cachaça Artesanal, Leite de Coco Integral, Leite Condensado e Coco Ralado."},
    {"id": 10, "nome": "Batida de Manga com Maracujá", "categoria": "🥥 Clássicas & Tropicais", "preco_base": 32.00, "desc": "Polpa de manga doce combinada com o toque cítrico do maracujá."},
    {"id": 11, "nome": "Batida de Melancia com Hortelã", "categoria": "🥥 Clássicas & Tropicais", "preco_base": 30.00, "desc": "Melancia suculenta batida com folhas frescas de hortelã e vodka."},
    {"id": 12, "nome": "Batida de Frutas Vermelhas", "categoria": "🥥 Clássicas & Tropicais", "preco_base": 35.00, "desc": "Amora, framboesa e morango batidos com vodka e leite condensado."},
    {"id": 13, "nome": "Batida de Banana com Canela", "categoria": "🥥 Clássicas & Tropicais", "preco_base": 30.00, "desc": "Banana nanica madura, pitada de canela em pó, leite condensado e rum."},
    {"id": 14, "nome": "Batida de Maracujá com Pimenta", "categoria": "🥥 Clássicas & Tropicais", "preco_base": 34.00, "desc": "Maracujá natural com um toque leve de pimenta dedo-de-moça."},

    {"id": 15, "nome": "Batida de Vinho Tinto Suave", "categoria": "🍷 Vinhos & Especiais", "preco_base": 35.00, "desc": "Vinho Tinto Suave selecionado, Cachaça Artesanal e Leite Condensado."},
    {"id": 16, "nome": "Batida de Vinho com Morango", "categoria": "🍷 Vinhos & Especiais", "preco_base": 36.00, "desc": "Vinho tinto suave batido com morangos frescos e leite condensado."},
    {"id": 17, "nome": "Batida de Amarula Caseira", "categoria": "🍷 Vinhos & Especiais", "preco_base": 40.00, "desc": "Creme cremoso sabor marula, conhaque, leite condensado e toque de chocolate."},
    {"id": 18, "nome": "Batida de Chocolate Cremoso", "categoria": "🍷 Vinhos & Especiais", "preco_base": 35.00, "desc": "Chocolate meio amargo derretido, leite condensado, vodka e creme de leite."},
    {"id": 19, "nome": "Batida de Doce de Leite com Coco", "categoria": "🍷 Vinhos & Especiais", "preco_base": 36.00, "desc": "Doce de leite argentino puro batido com leite de coco e cachaça."},
    {"id": 20, "nome": "Batida de Paçoca", "categoria": "🍷 Vinhos & Especiais", "preco_base": 34.00, "desc": "Paçoca de amendoim artesanal triturada, leite condensado e vodka."},
    {"id": 21, "nome": "Batida de Ovomaltine", "categoria": "🍷 Vinhos & Especiais", "preco_base": 36.00, "desc": "Crocante Ovomaltine misturado com creme de leite, leite condensado e vodka."},

    {"id": 22, "nome": "Batida de Gengibre com Mel", "categoria": "🌶️ Exóticas & Potentes", "preco_base": 35.00, "desc": "Gengibre fresco ralado, limão tahiti, mel silvestre puro e Cachaça Envelhecida."},
    {"id": 23, "nome": "Batida de Catuaba com Açaí", "categoria": "🌶️ Exóticas & Potentes", "preco_base": 34.00, "desc": "Açaí na polpa batido com Catuaba selvagem e leite condensado."},
    {"id": 24, "nome": "Batida de Limão Siciliano com Capim-Santo", "categoria": "🌶 Exóticas & Potentes", "preco_base": 33.00, "desc": "Infusão aromática de capim-santo com limão siciliano e vodka."},
    {"id": 25, "nome": "Batida de Kiwi com Hortelã", "categoria": "🌶️ Exóticas & Potentes", "preco_base": 32.00, "desc": "Kiwi verde fresco, folhas de hortelã, vodka premium e xarope de açúcar."},
    {"id": 26, "nome": "Batida de Tangerina com Pimenta", "categoria": "🌶️ Exóticas & Potentes", "preco_base": 33.00, "desc": "Suco natural de tangerina poncã com um toque exótico de pimenta rosa."},
    {"id": 27, "nome": "Batida de Café Expresso com Licor", "categoria": "🌶 Exóticas & Potentes", "preco_base": 36.00, "desc": "Café expresso forte, licor de cacau, leite condensado e vodka."},
    {"id": 28, "nome": "Batida de Acerola com Laranja", "categoria": "🌶️ Exóticas & Potentes", "preco_base": 30.00, "desc": "Acerola rica em vitamina C combinada com suco de laranja natural e cachaça."},
    {"id": 29, "nome": "Batida de Cajá Tropical", "categoria": "🌶️ Exóticas & Potentes", "preco_base": 32.00, "desc": "Polpa selecionada de cajá com acidez marcante, leite condensado e rum."},
    {"id": 30, "nome": "Batida Tropical de Pitaya", "categoria": "🌶️ Exóticas & Potentes", "preco_base": 38.00, "desc": "Pitaya vermelha fresca batida com vodka premium, limão e xarope leve."}
]
if st.session_state.pagina_atual == "🛒 Cardápio":
    st.markdown("""
        <div class="hero-banner">
            <span class="badge-loja">🟢 LOJA ABERTA • DAS 14H ÀS 03H</span>
            <h1 style="color: #ffffff; font-weight: 900; font-size: 2.2rem; margin: 5px 0;">QG DAS <span style="color: #FFB800;">BATIDAS</span></h1>
            <p style="color: #bbbbbb; font-size: 0.95rem; margin: 0;">As melhores batidas artesanais da região entregues trincando na sua casa</p>
        </div>
    """, unsafe_allow_html=True)

    col_c1, col_c2 = st.columns([2, 2])
    with col_c1:
        if st.button("⭐ Especiais da Casa", use_container_width=True):
            st.session_state.categoria_ativa = "⭐ Especiais da Casa"
        if st.button("🍷 Vinhos & Especiais", use_container_width=True):
            st.session_state.categoria_ativa = "🍷 Vinhos & Especiais"
    with col_c2:
        if st.button("🥥 Clássicas & Tropicais", use_container_width=True):
            st.session_state.categoria_ativa = "🥥 Clássicas & Tropicais"
        if st.button("🌶️ Exóticas & Potentes", use_container_width=True):
            st.session_state.categoria_ativa = "🌶️ Exóticas & Potentes"

    st.markdown("---")
    st.markdown(f"## {st.session_state.categoria_ativa}")

    itens_filtrados = [item for item in cardapio_detalhado if item["categoria"] == st.session_state.categoria_ativa]

    for item in itens_filtrados:
        with st.container(border=True):
            st.markdown(f"### {item['nome']}")
            st.markdown(f"<span class='detalhe-batida'>{item['desc']}</span>", unsafe_allow_html=True)
            
            st.markdown("**Tamanho:**")
            tamanho = st.radio("Tamanho:", ["300ml", "500ml", "1 Litro"], horizontal=True, key=f"tam_{item['id']}", label_visibility="collapsed")
            
            if tamanho == "300ml":
                preco_final = 12.00 if item['preco_base'] >= 32.00 else 11.00
            elif tamanho == "500ml":
                preco_final = 18.00 if item['preco_base'] >= 32.00 else 17.00
            else:
                preco_final = item['preco_base']
                
            st.markdown(f"<div style='margin: 12px 0;'><span class='preco-destaque'>R$ {preco_final:.2f}</span></div>", unsafe_allow_html=True)
            
            if st.button("🛒 Adicionar", key=f"add_{item['id']}", use_container_width=True):
                st.session_state.carrinho.append({"nome": f"{item['nome']} ({tamanho})", "preco": preco_final})
                st.success("Adicionado ao carrinho com sucesso!")

    total_itens = len(st.session_state.carrinho)
    valor_total_carrinho = sum(item['preco'] for item in st.session_state.carrinho)
    
    if total_itens > 0:
        st.markdown("---")
        st.markdown(f"""
            <div style="background: rgba(0, 255, 127, 0.15); border: 1px solid #00FF7F; padding: 15px; border-radius: 12px; text-align: center; margin-top: 20px;">
                <h3 style="color: #00FF7F; margin: 0 0 5px 0;">🛍 Seu Carrinho tem {total_itens} ite(ns) • R$ {valor_total_carrinho:.2f}</h3>
            </div>
        """, unsafe_allow_html=True)
        if st.button("🚀 Ir para o Checkout / Finalizar Pedido", use_container_width=True):
            st.session_state.pagina_atual = "🛍 Carrinho"
            st.rerun()

elif st.session_state.pagina_atual == "🛍 Carrinho":
    st.markdown("<h2>🛍 Seu Carrinho de Compras</h2>", unsafe_allow_html=True)
    st.markdown("---")

    if st.session_state.get("ultimo_pedido"):
        st.markdown(f"""
            <div style="background: rgba(255, 184, 0, 0.15); border: 1px solid #FFB800; padding: 15px; border-radius: 12px; text-align: center; margin-bottom: 20px;">
                <h3 style="color: #FFB800; margin: 0 0 5px 0;">🎫 Último Pedido Confirmado: {st.session_state.ultimo_pedido}</h3>
                <p style="color: #dddddd; margin: 0; font-size: 0.9rem;">Guarde este ID para acompanhar o status na Central Administrativa.</p>
            </div>
        """, unsafe_allow_html=True)

    if len(st.session_state.carrinho) == 0:
        st.info("Seu carrinho está vazio no momento. Volte ao cardápio e escolha suas batidas!")
        if st.button("⬅️ Voltar ao Cardápio"):
            st.session_state.pagina_atual = "🛒 Cardápio"
            st.rerun()
    else:
        total_carrinho = 0
        for idx, prod in enumerate(st.session_state.carrinho):
            col_i1, col_i2 = st.columns([3, 1])
            with col_i1:
                st.markdown(f"• **{prod['nome']}** — R$ {prod['preco']:.2f}")
            with col_i2:
                if st.button("Remover", key=f"del_{idx}"):
                    st.session_state.carrinho.pop(idx)
                    st.rerun()
            total_carrinho += prod['preco']
        
        st.markdown("---")
        st.markdown(f"### **Total a Pagar: R$ {total_carrinho:.2f}**")
        
        if st.button("🗑 Limpar Carrinho Inteiro"):
            st.session_state.carrinho = []
            st.rerun()

        st.markdown("---")
        st.markdown("### 📝 Dados de Entrega e Pagamento")
        
        if "rua_val" not in st.session_state:
            st.session_state.rua_val = ""
        if "bairro_val" not in st.session_state:
            st.session_state.bairro_val = ""
        if "cidade_val" not in st.session_state:
            st.session_state.cidade_val = "Taboão da Serra"

        with st.form("form_checkout_principal"):
            nome_cliente = st.text_input("Seu Nome Completo:")
            whatsapp = st.text_input("WhatsApp / Telefone:")
            data_nascimento = st.text_input("Data de Nascimento (DD/MM/AAAA):", placeholder="Ex: 12/10/1985")
            
            st.markdown("---")
            st.markdown("📍 **Endereço**")
            cep_input = st.text_input("CEP:", max_chars=8)
            buscar_cep_btn = st.form_submit_button("🔍 Buscar CEP Automático")
            
            if buscar_cep_btn:
                clean_cep = "".join(filter(str.isdigit, cep_input))
                base_ceps = {
                    "06783100": {"rua": "Rua André da Silva Pina", "bairro": "Jardim Record", "cidade": "Taboão da Serra"},
                    "06765000": {"rua": "Estrada Kizaemon Takeuti", "bairro": "Parque Pinheiros", "cidade": "Taboão da Serra"},
                    "06753000": {"rua": "Rodovia Régis Bittencourt", "bairro": "Centro", "cidade": "Taboão da Serra"}
                }
                if clean_cep in base_ceps:
                    info = base_ceps[clean_cep]
                    st.session_state.rua_val = info["rua"]
                    st.session_state.bairro_val = info["bairro"]
                    st.session_state.cidade_val = info["cidade"]
                    st.success("✅ Endereço carregado com sucesso!")

            rua = st.text_input("Rua:", value=st.session_state.rua_val)
            numero = st.text_input("Número:")
            bairro = st.text_input("Bairro:", value=st.session_state.bairro_val)
            cidade = st.text_input("Cidade:", value=st.session_state.cidade_val)
            
            st.markdown("---")
            pagamento = st.selectbox("Forma de Pagamento:", ["Pix", "Cartão de Crédito", "Cartão de Débito", "Dinheiro"])
            
            enviar_pedido = st.form_submit_button("🚀 Confirmar e Enviar Pedido")
                            if enviar_pedido:
                if not nome_cliente or not whatsapp or not rua or not numero:
                    st.error("Preencha Nome, WhatsApp, Rua e Número para prosseguir.")
                else:
                    numero_pedido = f"QG-2026-{random.randint(1000, 9999)}"
                    timestamp_criacao = datetime.datetime.now().isoformat()
                    data_hora_atual = datetime.datetime.now().strftime("%d/%m/%Y às %H:%M")
                    endereco_completo = f"{rua}, nº {numero} - {bairro}, {cidade}"
                    
                    conn = sqlite3.connect("qg_batidas.db")
                    cursor = conn.cursor()
                    cursor.execute("""
                        INSERT INTO pedidos (pedido_id, timestamp, data_hora, cliente, whatsapp, nascimento, endereco, pagamento, status, total)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (numero_pedido, timestamp_criacao, data_hora_atual, nome_cliente, whatsapp, data_nascimento, endereco_completo, pagamento, "Recebido", total_carrinho))
                    
                    cursor.execute("""
                        INSERT INTO caixa (data_hora, tipo, descricao, valor)
                        VALUES (?, ?, ?, ?)
                    """, (data_hora_atual, "Entrada", f"Venda Pedido {numero_pedido} - {nome_cliente}", total_carrinho))
                    
                    cursor.execute("SELECT id, compras_totais FROM crm_clientes WHERE whatsapp = ?", (whatsapp,))
                    cli_existente = cursor.fetchone()
                    if cli_existente:
                        cursor.execute("UPDATE crm_clientes SET compras_totais = compras_totais + 1 WHERE whatsapp = ?", (whatsapp,))
                    else:
                        cursor.execute("INSERT INTO crm_clientes (nome, whatsapp, preferencia, compras_totais) VALUES (?, ?, ?, ?)", (nome_cliente, whatsapp, "Geral", 1))
                    
                    conn.commit()
                    conn.close()

                    st.session_state.ultimo_pedido = numero_pedido
                    st.session_state.carrinho = []
                    st.success(f"🎉 Pedido gerado com sucesso! ID de Rastreio: {numero_pedido}")
                    st.balloons()

    if st.session_state.get("ultimo_pedido"):
        st.markdown("---")
        if st.button("🔄 Fazer Novo Pedido"):
            st.session_state.pagina_atual = "🛒 Cardápio"
            st.rerun()

elif st.session_state.pagina_atual == "📊 Admin":
    st.markdown("<h2>📊 Painel Administrativo do QG</h2>", unsafe_allow_html=True)
    st.markdown("---")
    
    tab_adm1, tab_adm2, tab_adm3, tab_adm4 = st.tabs(["📦 Gestão de Pedidos", "💰 Caixa & Sangrias", "👥 CRM & Clientes", "🚀 Marketing & Ações"])
    
    with tab_adm1:
        st.markdown("### Pedidos Registrados no Banco de Dados")
        conn = sqlite3.connect("qg_batidas.db")
        cursor = conn.cursor()
        cursor.execute("SELECT pedido_id, data_hora, cliente, whatsapp, pagamento, status, total FROM pedidos ORDER BY timestamp DESC")
        todos_pedidos = cursor.fetchall()
        conn.close()
        
        if not todos_pedidos:
            st.info("Nenhum pedido registado até o momento.")
        else:
            for p in todos_pedidos:
                with st.container(border=True):
                    st.markdown(f"**ID:** `{p[0]}` | **Data:** {p[1]} | **Status:** `{p[5]}`")
                    st.markdown(f"**Cliente:** {p[2]} ({p[3]}) | **Pagamento:** {p[4]} | **Total:** R$ {p[6]:.2f}")
    
    with tab_adm2:
        st.markdown("### 💰 Controle de Caixa e Sangrias")
        conn = sqlite3.connect("qg_batidas.db")
        cursor = conn.cursor()
        cursor.execute("SELECT data_hora, tipo, descricao, valor FROM caixa ORDER BY id DESC")
        lancamentos = cursor.fetchall()
        
        total_entradas = sum(l[3] for l in lancamentos if l[1] == "Entrada")
        total_saidas = sum(l[3] for l in lancamentos if l[1] == "Saída / Sangria")
        saldo_liquido = total_entradas - total_saidas
        
        col_m1, col_m2, col_m3 = st.columns(3)
        col_m1.metric("Entradas Totais", f"R$ {total_entradas:.2f}")
        col_m2.metric("Saídas / Sangrias", f"R$ {total_saidas:.2f}")
        col_m3.metric("Saldo Líquido", f"R$ {saldo_liquido:.2f}")
        
        st.markdown("---")
        st.markdown("#### Registar Nova Sangria / Retirada")
        with st.form("form_sangria"):
            desc_sangria = st.text_input("Motivo da Sangria (ex: Pagamento de Insumos / Gelo):")
            valor_sangria = st.number_input("Valor (R$):", min_value=0.0, step=10.0)
            btn_salvar_sangria = st.form_submit_button("🚨 Registar Sangria")
            
            if btn_salvar_sangria:
                if desc_sangria and valor_sangria > 0:
                    data_hora_atual = datetime.datetime.now().strftime("%d/%m/%Y às %H:%M")
                    cursor.execute("INSERT INTO caixa (data_hora, tipo, descricao, valor) VALUES (?, ?, ?, ?)", (data_hora_atual, "Saída / Sangria", desc_sangria, valor_sangria))
                    conn.commit()
                    st.success("Sangria registada com sucesso!")
                    st.rerun()
                else:
                    st.error("Preencha a descrição e um valor válido.")
        conn.close()
        
    with tab_adm3:
        st.markdown("### 👥 Relacionamento com Clientes (CRM)")
        conn = sqlite3.connect("qg_batidas.db")
        cursor = conn.cursor()
        cursor.execute("SELECT nome, whatsapp, preferencia, compras_totais FROM crm_clientes")
        clientes = cursor.fetchall()
        conn.close()
        
        if not clientes:
            st.info("Nenhum cliente registado no CRM ainda.")
        else:
            for c in clientes:
                with st.container(border=True):
                    st.markdown(f"**Cliente:** {c[0]} | **WhatsApp:** {c[1]}")
                    st.markdown(f"**Preferência:** {c[2]} | **Total de Compras:** {c[3]} pedido(s)")
                    
    with tab_adm4:
        st.markdown("### 🚀 Central de Marketing & Ações")
        st.markdown("Gere copys rápidas e links de atendimento para impulsionar suas vendas no WhatsApp:")
        
        campanha_tipo = st.selectbox("Escolha a Ação de Marketing:", [
            "Happy Hour do QG (Desconto em 300ml)", 
            "Fim de Semana com Batida Dobrada", 
            "Recuperação de Cliente Sumido"
        ])
        
        if campanha_tipo == "Happy Hour do QG (Desconto em 300ml)":
            texto_copy = "🔥 Fala, mestre! Passando para avisar que o Happy Hour do QG das Batidas tá ativado! Garanta sua batida de 300ml trincando por apenas R$ 11,00 hoje. Clica aqui e pede a sua!"
        elif campanha_tipo == "Fim de Semana com Batida Dobrada":
            texto_copy = "🍸 Fim de semana chegou e o QG preparou lotes frescos das nossas batidas artesanais! Peça sua garrafa de 1L e garanta a resenha com os melhores sabores da região."
        else:
            texto_copy = "👋 E aí, sumido! Sentiu falta das nossas batidas? Hoje temos lote especial saindo do forno. Vem conferir o cardápio atualizado!"
            
        st.text_area("Sugestão de Copy Pronta para Copiar:", value=texto_copy, height=100)
        st.success("Copie o texto acima e cole direto nas suas transmissões do WhatsApp ou Status!")
    

import streamlit as st
import random
import datetime
import sqlite3

# Inicialização direta do banco de dados para evitar erros de importação
def init_db():
    conn = sqlite3.connect("qg_batidas.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pedidos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pedido_id TEXT,
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
            compras_totais INTEGER
        )
    """)
    conn.commit()
    conn.close()

init_db()

# Importação segura do cardápio e módulos do painel
try:
    from produtos import cardapio_detalhado
except ImportError:
    cardapio_detalhado = [
        {"id": 1, "nome": "Batida de Coco com Leite Condensado", "desc": "Cremosa, refrescante e tradicional.", "preco_base": 32.00, "categoria": "⭐ Especiais da Casa"},
        {"id": 2, "nome": "Batida de Vinho com Morango", "desc": "A fusão perfeita entre a doçura e a potência.", "preco_base": 35.00, "categoria": "🍷 Vinhos & Especiais"}
    ]

try:
    from pedidos import exibir_pedidos
except ImportError:
    exibir_pedidos = None

try:
    from caixa import exibir_caixa
except ImportError:
    exibir_caixa = None

try:
    from crm import exibir_crm
except ImportError:
    exibir_crm = None

st.set_page_config(
    page_title="QG das Batidas",
    page_icon="🍸",
    layout="wide",
    initial_sidebar_state="collapsed"
)

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

if st.session_state.pagina_atual == "🛒 Cardápio":
    st.markdown("""
        <div style="background: linear-gradient(135deg, rgba(0, 255, 127, 0.15) 0%, rgba(255, 184, 0, 0.1) 100%); border: 1px solid rgba(0, 255, 127, 0.3); border-radius: 16px; padding: 24px; text-align: center; margin-bottom: 20px;">
            <span style="background: rgba(0, 255, 127, 0.2); color: #00FF7F; border: 1px solid rgba(0, 255, 127, 0.5); border-radius: 30px; padding: 5px 15px; font-size: 0.8rem; font-weight: 700;">🟢 LOJA ABERTA • DAS 14H ÀS 03H</span>
            <h1 style="color: #ffffff; font-weight: 900; font-size: 2.2rem; margin: 10px 0 5px 0;">QG DAS <span style="color: #FFB800;">BATIDAS</span></h1>
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
            st.markdown(f"<span style='color: #e0e0e0; font-size: 1.1rem; display: block; margin-bottom: 14px;'>{item['desc']}</span>", unsafe_allow_html=True)
            
            tamanho = st.radio("Tamanho:", ["300ml", "500ml", "1 Litro"], horizontal=True, key=f"tam_{item['id']}", label_visibility="collapsed")
            
            if tamanho == "300ml":
                preco_final = 12.00 if item['preco_base'] >= 32.00 else 11.00
            elif tamanho == "500ml":
                preco_final = 18.00 if item['preco_base'] >= 32.00 else 17.00
            else:
                preco_final = item['preco_base']
                
            st.markdown(f"<div style='margin: 12px 0;'><span style='color: #FFB800; font-size: 1.45rem; font-weight: 850;'>R$ {preco_final:.2f}</span></div>", unsafe_allow_html=True)
            
            if st.button("🛒 Adicionar", key=f"add_{item['id']}", use_container_width=True):
                st.session_state.carrinho.append({"nome": f"{item['nome']} ({tamanho})", "preco": preco_final})
                st.success("Adicionado ao carrinho com sucesso!")

    if len(st.session_state.carrinho) > 0:
        st.markdown("---")
        st.markdown(f"""
            <div style="background: rgba(0, 255, 127, 0.15); border: 1px solid #00FF7F; padding: 15px; border-radius: 12px; text-align: center; margin-top: 20px;">
                <h3 style="color: #00FF7F; margin: 0 0 5px 0;">🛍 Seu Carrinho tem {len(st.session_state.carrinho)} ite(ns) • R$ {sum(i['preco'] for i in st.session_state.carrinho):.2f}</h3>
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
            </div>
        """, unsafe_allow_html=True)

    if len(st.session_state.carrinho) == 0:
        st.info("Seu carrinho está vazio no momento.")
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
        st.markdown("### 📝 Dados de Entrega")
        with st.form("form_checkout_principal"):
            nome_cliente = st.text_input("Seu Nome Completo:")
            whatsapp = st.text_input("WhatsApp:")
            rua = st.text_input("Rua:")
            numero = st.text_input("Número:")
            bairro = st.text_input("Bairro:")
            cidade = st.text_input("Cidade:", value="Taboão da Serra")
            pagamento = st.selectbox("Forma de Pagamento:", ["Pix", "Cartão de Crédito", "Dinheiro"])
            
            enviar_pedido = st.form_submit_button("🚀 Confirmar e Enviar Pedido")
            
            if enviar_pedido:
                if not nome_cliente or not whatsapp or not rua or not numero:
                    st.error("Preencha Nome, WhatsApp, Rua e Número.")
                else:
                    numero_pedido = f"QG-2026-{random.randint(1000, 9999)}"
                    dha = datetime.datetime.now().strftime("%d/%m/%Y às %H:%M")
                    
                    conn = sqlite3.connect("qg_batidas.db")
                    cursor = conn.cursor()
                    cursor.execute("""
                        INSERT INTO pedidos (pedido_id, timestamp, data_hora, cliente, whatsapp, nascimento, endereco, pagamento, status, total)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (numero_pedido, datetime.datetime.now().isoformat(), dha, nome_cliente, whatsapp, "", f"{rua}, nº {numero} - {bairro}, {cidade}", pagamento, "Recebido", total_carrinho))
                    
                    cursor.execute("""
                        INSERT INTO caixa (data_hora, tipo, descricao, valor)
                        VALUES (?, ?, ?, ?)
                    """, (dha, "Entrada", f"Venda Pedido {numero_pedido} - {nome_cliente}", total_carrinho))
                    
                    cursor.execute("SELECT id FROM crm_clientes WHERE whatsapp = ?", (whatsapp,))
                    if cursor.fetchone():
                        cursor.execute("UPDATE crm_clientes SET compras_totais = compras_totais + 1 WHERE whatsapp = ?", (whatsapp,))
                    else:
                        cursor.execute("INSERT INTO crm_clientes (nome, whatsapp, preferencia, compras_totais) VALUES (?, ?, ?, 1)", (nome_cliente, whatsapp, "Geral"))
                    
                    conn.commit()
                    conn.close()

                    st.session_state.ultimo_pedido = numero_pedido
                    st.session_state.carrinho = []
                    st.success(f"🎉 Pedido gerado com sucesso! ID: {numero_pedido}")
                    st.balloons()

elif st.session_state.pagina_atual == "📊 Admin":
    st.markdown("<h2>📊 Painel Administrativo</h2>", unsafe_allow_html=True)
    st.markdown("---")
    
    t1, t2, t3 = st.tabs(["📦 Pedidos", "💰 Caixa & Sangrias", "👥 CRM & Clientes"])
    
    with t1:
        if exibir_pedidos:
            exibir_pedidos()
        else:
            st.info("Módulo pedidos em carregamento...")
            
    with t2:
        if exibir_caixa:
            exibir_caixa()
        else:
            st.info("Módulo caixa em carregamento...")
            
    with t3:
        if exibir_crm:
            exibir_crm()
        else:
            st.info("Módulo crm em carregamento...")
            

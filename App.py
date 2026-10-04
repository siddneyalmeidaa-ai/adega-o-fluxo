import streamlit as st
import json
import os
import random
import datetime

# Configuração da página principal
st.set_page_config(
    page_title="QG das Batidas",
    page_icon="🍸",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- ESTILIZAÇÃO CSS AVANÇADA (MODO APP DELIVERY PREMIUM) ---
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
            opacity: 0.15;
        }
        .main .block-container {
            position: relative;
            z-index: 1;
            padding-top: 2rem;
        }
        /* Cartão de Produto Estilo Glassmorphism */
        .card-produto {
            background: linear-gradient(145deg, #161616, #111111);
            border: 1px solid #262626;
            border-radius: 18px;
            padding: 18px;
            margin-bottom: 15px;
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.6);
            transition: all 0.3s ease;
        }
        .card-produto:hover {
            border-color: #00FF7F;
            box-shadow: 0 8px 25px rgba(0, 255, 127, 0.15);
        }
        /* Badge de Status da Loja */
        .badge-loja {
            background: rgba(0, 255, 127, 0.1);
            color: #00FF7F;
            border: 1px solid rgba(0, 255, 127, 0.4);
            border-radius: 30px;
            padding: 6px 18px;
            font-size: 0.85rem;
            font-weight: 700;
            display: inline-block;
            letter-spacing: 0.5px;
        }
        /* Preço Dourado Destacado */
        .preco-destaque {
            color: #FFB800;
            font-size: 1.35rem;
            font-weight: 800;
        }
        /* Ajuste de fontes e títulos */
        h1, h2, h3 {
            font-family: 'Inter', sans-serif;
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

# --- MENU LATERAL ---
st.sidebar.markdown("### 🍸 QG das Batidas")
st.sidebar.markdown("Painel de Controle e Vendas")

pagina = st.sidebar.radio(
    "Navegação:",
    ["🛒 Cardápio (Vitrine do Cliente)", "📊 Painel de Pedidos (Admin)"]
)

st.sidebar.markdown("---")

# --- MÓDULO 1: VITRINE DO CLIENTE ---
if pagina == "🛒 Cardápio (Vitrine do Cliente)":
    st.markdown('<div style="text-align: center; margin-bottom: 10px;"><span class="badge-loja">🟢 LOJA ABERTA • DAS 14H ÀS 03H</span></div>', unsafe_allow_html=True)
    st.markdown('<h1 style="text-align: center; color: #ffffff; font-weight: 900; font-size: 2.2rem; margin-bottom: 0px;">QG DAS <span style="color: #FFB800;">BATIDAS</span></h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; color: #888888; font-size: 0.95rem; margin-bottom: 25px;">As 30 melhores batidas artesanais da região direto na sua casa</p>', unsafe_allow_html=True)

    if "carrinho" not in st.session_state:
        st.session_state.carrinho = []

    # Lista completa das 30 Batidas
    cardapio_detalhado = [
        # ⭐ Batidas Especiais da Casa
        {"id": 1, "nome": "Batida Tropical de Morango", "categoria": "⭐ Especiais da Casa", "preco_base": 32.00, "desc": "Morangos frescos selecionados, xarope de açúcar, vodka premium e gelo triturado."},
        {"id": 2, "nome": "Batida de Maracujá Clássica", "categoria": "⭐ Especiais da Casa", "preco_base": 32.00, "desc": "Polpa de maracujá azedo natural, leite condensado, cachaça branca e gelo."},
        {"id": 3, "nome": "Batida de Ninho com Nutella", "categoria": "⭐ Especiais da Casa", "preco_base": 38.00, "desc": "Creme cremoso de Leite Ninho, toque generoso de Nutella original e vodka."},
        {"id": 4, "nome": "Batida de Maracujá com Leite Condensado", "categoria": "⭐ Especiais da Casa", "preco_base": 32.00, "desc": "A clássica acidez do maracujá equilibrada com a doçura do leite condensado."},
        {"id": 5, "nome": "Batida de Morango com Leite Condensado", "categoria": "⭐ Especiais da Casa", "preco_base": 32.00, "desc": "Morangos frescos batidos na hora com leite condensado e vodka."},
        {"id": 6, "nome": "Batida de Abacaxi com Hortelã", "categoria": "⭐ Especiais da Casa", "preco_base": 32.00, "desc": "Abacaxi fresco, folhas de hortelã batidas, rum branco e gelo."},
        {"id": 7, "nome": "Batida de Limão com Leite Condensado", "categoria": "⭐ Especiais da Casa", "preco_base": 30.00, "desc": "Limão tahiti fresco, leite condensado e cachaça artesanal."},

        # 🥥 Clássicas & Tropicais
        {"id": 8, "nome": "Batida Cocadinha Tropical", "categoria": "🥥 Clássicas & Tropicais", "preco_base": 30.00, "desc": "Leite de coco concentrado, rum branco, leite condensado e coco ralado."},
        {"id": 9, "nome": "Batida de Coco Cremoso", "categoria": "🥥 Clássicas & Tropicais", "preco_base": 30.00, "desc": "Cachaça Artesanal, Leite de Coco Integral, Leite Condensado e Coco Ralado."},
        {"id": 10, "nome": "Batida de Manga com Maracujá", "categoria": "🥥 Clássicas & Tropicais", "preco_base": 32.00, "desc": "Polpa de manga doce combinada com o toque cítrico do maracujá."},
        {"id": 11, "nome": "Batida de Melancia com Hortelã", "categoria": "🥥 Clássicas & Tropicais", "preco_base": 30.00, "desc": "Melancia suculenta batida com folhas frescas de hortelã e vodka."},
        {"id": 12, "nome": "Batida de Frutas Vermelhas", "categoria": "🥥 Clássicas & Tropicais", "preco_base": 35.00, "desc": "Amora, framboesa e morango batidos com vodka e leite condensado."},
        {"id": 13, "nome": "Batida de Banana com Canela", "categoria": "🥥 Clássicas & Tropicais", "preco_base": 30.00, "desc": "Banana nanica madura, pitada de canela em pó, leite condensado e rum."},
        {"id": 14, "nome": "Batida de Maracujá com Pimenta", "categoria": "🥥 Clássicas & Tropicais", "preco_base": 34.00, "desc": "Maracujá natural com um toque leve de pimenta dedo-de-moça."},

        # 🍷 Vinhos & Especiais
        {"id": 15, "nome": "Batida de Vinho Tinto Suave", "categoria": "🍷 Vinhos & Especiais", "preco_base": 35.00, "desc": "Vinho Tinto Suave selecionado, Cachaça Artesanal e Leite Condensado."},
        {"id": 16, "nome": "Batida de Vinho com Morango", "categoria": "🍷 Vinhos & Especiais", "preco_base": 36.00, "desc": "Vinho tinto suave batido com morangos frescos e leite condensado."},
        {"id": 17, "nome": "Batida de Amarula Caseira", "categoria": "🍷 Vinhos & Especiais", "preco_base": 40.00, "desc": "Creme cremoso sabor marula, conhaque, leite condensado e toque de chocolate."},
        {"id": 18, "nome": "Batida de Chocolate Cremoso", "categoria": "🍷 Vinhos & Especiais", "preco_base": 35.00, "desc": "Chocolate meio amargo derretido, leite condensado, vodka e creme de leite."},
        {"id": 19, "nome": "Batida de Doce de Leite com Coco", "categoria": "🍷 Vinhos & Especiais", "preco_base": 36.00, "desc": "Doce de leite argentino puro batido com leite de coco e cachaça."},
        {"id": 20, "nome": "Batida de Paçoca", "categoria": "🍷 Vinhos & Especiais", "preco_base": 34.00, "desc": "Paçoca de amendoim artesanal triturada, leite condensado e vodka."},
        {"id": 21, "nome": "Batida de Ovomaltine", "categoria": "🍷 Vinhos & Especiais", "preco_base": 36.00, "desc": "Crocante Ovomaltine misturado com creme de leite, leite condensado e vodka."},

        # 🌶️ Exóticas, Potentes & Cítricas
        {"id": 22, "nome": "Batida de Gengibre com Mel", "categoria": "🌶️ Exóticas & Potentes", "preco_base": 35.00, "desc": "Gengibre fresco ralado, limão tahiti, mel silvestre puro e Cachaça Envelhecida."},
        {"id": 23, "nome": "Batida de Catuaba com Açaí", "categoria": "🌶️ Exóticas & Potentes", "preco_base": 34.00, "desc": "Açaí na polpa batido com Catuaba selvagem e leite condensado."},
        {"id": 24, "nome": "Batida de Limão Siciliano com Capim-Santo", "categoria": "🌶️️ Exóticas & Potentes", "preco_base": 33.00, "desc": "Infusão aromática de capim-santo com limão siciliano e vodka."},
        {"id": 25, "nome": "Batida de Kiwi com Hortelã", "categoria": "🌶️ Exóticas & Potentes", "preco_base": 32.00, "desc": "Kiwi verde fresco, folhas de hortelã, vodka premium e xarope de açúcar."},
        {"id": 26, "nome": "Batida de Tangerina com Pimenta", "categoria": "🌶️ Exóticas & Potentes", "preco_base": 33.00, "desc": "Suco natural de tangerina poncã com um toque exótico de pimenta rosa."},
        {"id": 27, "nome": "Batida de Café Expresso com Licor", "categoria": "🌶️ Exóticas & Potentes", "preco_base": 36.00, "desc": "Café expresso forte, licor de cacau, leite condensado e vodka."},
        {"id": 28, "nome": "Batida de Acerola com Laranja", "categoria": "🌶️ Exóticas & Potentes", "preco_base": 30.00, "desc": "Acerola rica em vitamina C combinada com suco de laranja natural e cachaça."},
        {"id": 29, "nome": "Batida de Cajá Tropical", "categoria": "🌶️ Exóticas & Potentes", "preco_base": 32.00, "desc": "Polpa selecionada de cajá com acidez marcante, leite condensado e rum."},
        {"id": 30, "nome": "Batida Tropical de Pitaya", "categoria": "🌶️ Exóticas & Potentes", "preco_base": 38.00, "desc": "Pitaya vermelha fresca batida com vodka premium, limão e xarope leve."}
    ]

    categorias_disponiveis = [
        "⭐ Especiais da Casa", 
        "🥥 Clássicas & Tropicais", 
        "🍷 Vinhos & Especiais", 
        "🌶️ Exóticas & Potentes"
    ]
    
    cat_selecionada = st.selectbox("📂 Filtrar Categoria do Cardápio:", categorias_disponiveis)

    itens_filtrados = [item for item in cardapio_detalhado if item["categoria"] == cat_selecionada]

    st.markdown("---")
    st.markdown(f"### {cat_selecionada}")

    # Exibição em grade de 2 colunas para ficar com cara de aplicativo profissional
    for i in range(0, len(itens_filtrados), 2):
        cols = st.columns(2)
        for j in range(2):
            if i + j < len(itens_filtrados):
                item = itens_filtrados[i + j]
                with cols[j]:
                    with st.container():
                        st.markdown(f"""
                            <div class="card-produto">
                                <h4 style="color: #ffffff; margin-bottom: 6px; font-size: 1.1rem; font-weight: 700;">{item['nome']}</h4>
                                <p style="color: #999999; font-size: 0.82rem; margin-bottom: 12px; line-height: 1.4; min-height: 38px;">{item['desc']}</p>
                            </div>
                        """, unsafe_allow_html=True)
                        
                        tamanho = st.radio(
                            f"Tamanho ({item['nome']}):",
                            ["300ml", "500ml", "1 Litro"],
                            horizontal=True,
                            key=f"tam_{item['id']}",
                            label_visibility="collapsed"
                        )
                        
                        if tamanho == "300ml":
                            preco_final = 12.00 if item['preco_base'] >= 32.00 else 11.00
                        elif tamanho == "500ml":
                            preco_final = 18.00 if item['preco_base'] >= 32.00 else 17.00
                        else:
                            preco_final = item['preco_base']
                            
                        col_p, col_b = st.columns([1.1, 1])
                        with col_p:
                            st.markdown(f"<span class='preco-destaque'>R$ {preco_final:.2f}</span>", unsafe_allow_html=True)
                        with col_b:
                            if st.button("🛒 Adicionar", key=f"add_{item['id']}", use_container_width=True):
                                item_carrinho = {
                                    "nome": f"{item['nome']} ({tamanho})",
                                    "preco": preco_final
                                }
                                st.session_state.carrinho.append(item_carrinho)
                                st.success("Adicionado!")
                        
                        st.markdown("<br>", unsafe_allow_html=True)

    # Carrinho Lateral
    st.sidebar.markdown("### 🛍 Seu Carrinho")
    if len(st.session_state.carrinho) == 0:
        st.sidebar.info("O carrinho está vazio. Escolha suas batidas!")
    else:
        total_carrinho = 0
        for prod in st.session_state.carrinho:
            st.sidebar.markdown(f"- {prod['nome']} (R$ {prod['preco']:.2f})")
            total_carrinho += prod['preco']
        
        st.sidebar.markdown(f"**Total a Pagar: R$ {total_carrinho:.2f}**")
        
        if st.sidebar.button("🗑 Limpar Carrinho"):
            st.session_state.carrinho = []
            st.rerun()

        st.sidebar.markdown("---")
        st.sidebar.markdown("### 📝 Dados de Entrega")
        
        if "rua_val" not in st.session_state:
            st.session_state.rua_val = ""
        if "bairro_val" not in st.session_state:
            st.session_state.bairro_val = ""
        if "cidade_val" not in st.session_state:
            st.session_state.cidade_val = "Taboão da Serra"

        with st.sidebar.form("form_checkout"):
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
                    st.success("✅ Endereço carregado!")

            rua = st.text_input("Rua:", value=st.session_state.rua_val)
            numero = st.text_input("Número:")
            bairro = st.text_input("Bairro:", value=st.session_state.bairro_val)
            cidade = st.text_input("Cidade:", value=st.session_state.cidade_val)
            
            st.markdown("---")
            pagamento = st.selectbox("Forma de Pagamento:", ["Pix", "Cartão de Crédito", "Cartão de Débito", "Dinheiro"])
            
            enviar_pedido = st.form_submit_button("🚀 Finalizar Pedido")
            
            if enviar_pedido:
                if not nome_cliente or not whatsapp or not rua or not numero:
                    st.error("Preencha Nome, WhatsApp, Rua e Número.")
                else:
                    numero_pedido = f"QG-2026-{random.randint(1000, 9999)}"
                    data_hora_atual = datetime.datetime.now().strftime("%d/%m/%Y às %H:%M")
                    endereco_completo = f"{rua}, nº {numero} - {bairro}, {cidade}"
                    
                    novo_registro = {
                        "pedido_id": numero_pedido,
                        "data_hora": data_hora_atual,
                        "cliente": nome_cliente,
                        "whatsapp": whatsapp,
                        "nascimento": data_nascimento,
                        "endereco": endereco_completo,
                        "pagamento": pagamento,
                        "itens": st.session_state.carrinho,
                        "total": total_carrinho
                    }
                    
                    arquivo_pedidos = "pedidos_qg.json"
                    lista_pedidos = []
                    if os.path.exists(arquivo_pedidos):
                        try:
                            with open(arquivo_pedidos, "r", encoding="utf-8") as f:
                                lista_pedidos = json.load(f)
                        except:
                            lista_pedidos = []
                    
                    lista_pedidos.append(novo_registro)
                    
                    with open(arquivo_pedidos, "w", encoding="utf-8") as f:
                        json.dump(lista_pedidos, f, ensure_ascii=False, indent=4)

                    st.session_state.ultimo_pedido = numero_pedido
                    st.session_state.carrinho = []
                    st.rerun()

    if "ultimo_pedido" in st.session_state and st.session_state.ultimo_pedido:
        st.success(f"🎉 Pedido **{st.session_state.ultimo_pedido}** finalizado com sucesso!")
        st.balloons()
        if st.button("🔄 Fazer Novo Pedido"):
            st.session_state.ultimo_pedido = None
            st.rerun()

# --- MÓDULO 2: PAINEL ADMINISTRATIVO DE PEDIDOS ---
elif pagina == "📊 Painel de Pedidos (Admin)":
    st.markdown("<h2>📦 Acompanhamento de Pedidos em Tempo Real</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color: #888888;'>Gerencie os pedidos que chegam da vitrine do cardápio.</p>", unsafe_allow_html=True)
    st.markdown("---")

    arquivo_pedidos = "pedidos_qg.json"
    
    if not os.path.exists(arquivo_pedidos):
        st.info("Nenhum pedido registrado até o momento.")
    else:
        try:
            with open(arquivo_pedidos, "r", encoding="utf-8") as f:
                pedidos = json.load(f)
        except:
            pedidos = []

        if not pedidos:
            st.info("A base de pedidos está vazia no momento.")
        else:
            st.markdown(f"**Total de Pedidos na Base: {len(pedidos)}**")
            st.markdown("---")

            for p in reversed(pedidos):
                with st.container():
                    st.markdown(f"""
                        <div class="card-produto">
                            <h3>🛒 Pedido <span style="color: #00FF7F;">{p.get('pedido_id')}</span> - <b>{p.get('cliente')}</b></h3>
                            <p style="m

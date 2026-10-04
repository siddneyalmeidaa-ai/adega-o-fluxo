import streamlit as st
import json
import os
import random
import datetime

def render():
    # Injetar CSS customizado para estilizar os cartões escuros exatos da sua imagem de referência
    st.markdown("""
        <style>
        .stApp {
            background-color: #121212;
            color: #ffffff;
        }
        .card-produto {
            background-color: #1a1a1a;
            border: 1px solid #333333;
            border-radius: 16px;
            padding: 20px;
            margin-bottom: 20px;
            box-shadow: 0 4px 10px rgba(0,0,0,0.5);
        }
        .badge-loja {
            background-color: rgba(0, 255, 127, 0.15);
            color: #00FF7F;
            border: 1px solid #00FF7F;
            border-radius: 20px;
            padding: 6px 16px;
            font-size: 0.9rem;
            font-weight: bold;
            display: inline-block;
            text-align: center;
            margin-bottom: 10px;
        }
        </style>
    """, unsafe_allow_html=True)

    # Topo igualzinho à sua referência
    st.markdown('<div style="text-align: center;"><span class="badge-loja">🟢 LOJA ABERTA - DAS 14H ÀS 03H</span></div>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; color: #aaaaaa; font-size: 0.85rem; letter-spacing: 1px; margin-bottom: 0px;">ARTESANAIS & EXCLUSIVAS</p>', unsafe_allow_html=True)
    st.markdown('<h1 style="text-align: center; color: #ffffff; font-weight: 800; margin-top: 0px;">QG DAS <span style="color: #FFB800;">BATIDAS</span></h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; color: #cccccc; margin-bottom: 25px;">As melhores batidas da região na sua casa</p>', unsafe_allow_html=True)

    # Inicializar o carrinho na sessão se não existir
    if "carrinho" not in st.session_state:
        st.session_state.carrinho = []

    # Lista completa de produtos com preços base proporcional para os tamanhos
    cardapio_detalhado = [
        {
            "id": 1, 
            "nome": "Batida Tropical de Morango", 
            "categoria": "⭐ Batidas Especiais da Casa", 
            "preco_base": 32.00, # Preço de referencia para 1L
            "desc": "Morangos frescos selecionados, xarope de açúcar, vodka premium e gelo triturado."
        },
        {
            "id": 2, 
            "nome": "Batida de Maracujá Clássica", 
            "categoria": "⭐ Batidas Especiais da Casa", 
            "preco_base": 32.00, 
            "desc": "Polpa de maracujá azedo natural, leite condensado, cachaça branca e gelo."
        },
        {
            "id": 3, 
            "nome": "Batida Cocadinha Tropical", 
            "categoria": "🥥 Clássicas & Tropicais", 
            "preco_base": 30.00, 
            "desc": "Leite de coco concentrado, rum branco, leite condensado e coco ralado."
        },
        {
            "id": 4, 
            "nome": "Batida de Coco Cremoso", 
            "categoria": "🥥 Clássicas & Tropicais", 
            "preco_base": 30.00, 
            "desc": "Cachaça Artesanal, Leite de Coco Integral, Leite Condensado e Coco Ralado."
        },
        {
            "id": 5, 
            "nome": "Batida de Vinho Tinto Suave", 
            "categoria": "🍷 Vinhos & Especiais", 
            "preco_base": 35.00, 
            "desc": "Vinho Tinto Suave selecionado, Cachaça Artesanal e Leite Condensado."
        },
        {
            "id": 6, 
            "nome": "Batida de Gengibre com Mel", 
            "categoria": "🌶️ Exóticas & Potentes", 
            "preco_base": 35.00, 
            "desc": "Gengibre fresco ralado, limão tahiti, mel silvestre puro e Cachaça Envelhecida."
        }
    ]

    # Menu de categorias em abas/filtros
    categorias_disponiveis = ["⭐ Batidas Especiais da Casa", "🥥 Clássicas & Tropicais", "🍷 Vinhos & Especiais", "🌶️ Exóticas & Potentes"]
    cat_selecionada = st.selectbox("Filtrar Categoria:", categorias_disponiveis)

    itens_filtrados = [item for item in cardapio_detalhado if item["categoria"] == cat_selecionada]

    st.markdown("---")
    st.markdown(f"### {cat_selecionada}")

    # Exibição em formato de cards idêntico ao modelo da imagem
    for item in itens_filtrados:
        with st.container():
            st.markdown(f"""
                <div class="card-produto">
                    <h3 style="color: #ffffff; margin-bottom: 5px; font-size: 1.25rem;">{item['nome']}</h3>
                    <p style="color: #aaaaaa; font-size: 0.9rem; margin-bottom: 15px;">{item['desc']}</p>
                </div>
            """, unsafe_allow_html=True)
            
            # Seletor de Tamanhos (Simulando os botões da imagem)
            tamanho = st.radio(
                f"Escolha o tamanho para {item['nome']}:",
                ["300ml", "500ml", "1 Litro"],
                horizontal=True,
                key=f"tam_{item['id']}"
            )
            
            # Cálculo proporcional dos preços baseado no padrão da imagem (300ml=R$12, 500ml=R$18, 1L=R$32)
            if tamanho == "300ml":
                preco_final = 12.00 if item['preco_base'] == 32.00 else 11.00
            elif tamanho == "500ml":
                preco_final = 18.00 if item['preco_base'] == 32.00 else 17.00
            else:
                preco_final = item['preco_base']
                
            c_preco, c_botao = st.columns([1.5, 1])
            with c_preco:
                st.markdown(f"<h3 style='color: #FFB800; margin-top: 10px;'>R$ {preco_final:.2f}</h3>", unsafe_allow_html=True)
            with c_botao:
                if st.button("+ ADICIONAR", key=f"add_{item['id']}", use_container_width=True):
                    item_carrinho = {
                        "nome": f"{item['nome']} ({tamanho})",
                        "preco": preco_final
                    }
                    st.session_state.carrinho.append(item_carrinho)
                    st.success("Adicionado! ✅")
            
            st.markdown("<br>", unsafe_allow_html=True)

    # --- CARRINHO E CHECKOUT NA SIDEBAR ---
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
        
        if "cep_val" not in st.session_state:
            st.session_state.cep_val = ""
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
                    

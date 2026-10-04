import streamlit as st
import json
import os
import random
import datetime

def render():
    # Injetar CSS customizado para estilizar os cartões e deixar a interface com cara de app mobile
    st.markdown("""
        <style>
        .card-produto {
            background-color: #1e1e1e;
            border: 1px solid #333333;
            border-radius: 12px;
            padding: 15px;
            margin-bottom: 20px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.3);
        }
        .preco-destaque {
            color: #00FF7F;
            font-size: 1.2rem;
            font-weight: bold;
        }
        </style>
    """, unsafe_allow_html=True)

    st.title("🍸 QG das Batidas")
    st.markdown("Selecione sua garrafa artesanal favorita, escolha o tamanho e faça o seu pedido rápido!")

    # Inicializar o carrinho na sessão se não existir
    if "carrinho" not in st.session_state:
        st.session_state.carrinho = []

    # Lista completa de produtos com fotos e preços base para 1L
    cardapio_detalhado = [
        {
            "id": 1, 
            "nome": "Batida de Coco Cremoso", 
            "categoria": "🥥 Clássicas & Frutas Tropicais", 
            "preco_1l": 45.00, 
            "desc": "Suave, cremosa e marcante.",
            "ingredientes": "Cachaça Artesanal, Leite de Coco Integral, Leite Condensado, Coco Ralado em Flocos e Leite em Pó.",
            "foto": "https://images.unsplash.com/photo-1551024709-8f23befc6f87?auto=format&fit=crop&w=600&q=80"
        },
        {
            "id": 2, 
            "nome": "Batida de Maracujá", 
            "categoria": "🥥 Clássicas & Frutas Tropicais", 
            "preco_1l": 48.00, 
            "desc": "Equilíbrio perfeito entre o azedinho e o doce.",
            "ingredientes": "Polpa de Maracujá in natura, Cachaça Selecionada e Leite Condensado cremoso.",
            "foto": "https://images.unsplash.com/photo-1536935338788-846bb9981813?auto=format&fit=crop&w=600&q=80"
        },
        {
            "id": 3, 
            "nome": "Batida de Morango Silvestre", 
            "categoria": "🥥 Clássicas & Frutas Tropicais", 
            "preco_1l": 50.00, 
            "desc": "Feita com frutas frescas selecionadas.",
            "ingredientes": "Morangos frescos, Cachaça Artesanal, Leite Condensado e calda artesanal.",
            "foto": "https://images.unsplash.com/photo-1541544741938-0af808871cc0?auto=format&fit=crop&w=600&q=80"
        },
        {
            "id": 4, 
            "nome": "Batida de Abacaxi com Hortelã", 
            "categoria": "🥥 Clássicas & Frutas Tropicais", 
            "preco_1l": 46.00, 
            "desc": "Refrescante e revigorante.",
            "ingredientes": "Abacaxi suculento, folhas de hortelã orgânica, Cachaça Premium e açúcar refinado.",
            "foto": "https://images.unsplash.com/photo-1514362545857-3bc16c4c7d1b?auto=format&fit=crop&w=600&q=80"
        },
        {
            "id": 5, 
            "nome": "Batida de Manga com Maracujá", 
            "categoria": "🥥 Clássicas & Frutas Tropicais", 
            "preco_1l": 49.00, 
            "desc": "Toque tropical irresistível.",
            "ingredientes": "Manga Palmer madura, polpa de maracujá e Cachaça Artesanal.",
            "foto": "https://images.unsplash.com/photo-1556679343-c7306c1976bc?auto=format&fit=crop&w=600&q=80"
        },
        {
            "id": 6, 
            "nome": "Batida de Limão Siciliano", 
            "categoria": "🥥 Clássicas & Frutas Tropicais", 
            "preco_1l": 47.00, 
            "desc": "Cítrico na medida certa com elegância.",
            "ingredientes": "Sumo de Limão Siciliano, raspas aromáticas, Cachaça Especial e Leite Condensado.",
            "foto": "https://images.unsplash.com/photo-1621263764928-df1444c5e859?auto=format&fit=crop&w=600&q=80"
        },
        {
            "id": 7, 
            "nome": "Batida de Goiaba Vermelha", 
            "categoria": "🥥 Clássicas & Frutas Tropicais", 
            "preco_1l": 45.00, 
            "desc": "Sabor autêntico e encorpado da fruta.",
            "ingredientes": "Goiabada cascão artesanal, Cachaça Selecionada e creme de leite leve.",
            "foto": "https://images.unsplash.com/photo-1575444758702-4a6b9222336e?auto=format&fit=crop&w=600&q=80"
        },
        {
            "id": 8, 
            "nome": "Batida de Caju com Pitada de Sal", 
            "categoria": "🥥 Clássicas & Frutas Tropicais", 
            "preco_1l": 48.00, 
            "desc": "O clássico reinventado com personalidade.",
            "ingredientes": "Caju fresco, Cachaça Branca, Leite Condensado e pitada de sal marinho.",
            "foto": "https://images.unsplash.com/photo-1506806732259-39c2d0268443?auto=format&fit=crop&w=600&q=80"
        },
        {
            "id": 9, 
            "nome": "Batida de Vinho Tinto Suave", 
            "categoria": "🍷 Vinhos & Especiais", 
            "preco_1l": 52.00, 
            "desc": "Encorpada e aconchegante.",
            "ingredientes": "Vinho Tinto Suave selecionado, Cachaça Artesanal e Leite Condensado.",
            "foto": "https://images.unsplash.com/photo-1510812431401-41d2bd2722f3?auto=format&fit=crop&w=600&q=80"
        },
        {
            "id": 10, 
            "nome": "Batida de Vinho com Canela e Cravo", 
            "categoria": "🍷 Vinhos & Especiais", 
            "preco_1l": 55.00, 
            "desc": "Aromatizada com especiarias finas.",
            "ingredientes": "Vinho Tinto, infusão de cravo, canela em pau fresca e Cachaça Premium.",
            "foto": "https://images.unsplash.com/photo-1543747579-795b9c2c3ada?auto=format&fit=crop&w=600&q=80"
        },
        {
            "id": 23, 
            "nome": "Batida de Gengibre com Mel", 
            "categoria": "🌶️ Exóticas & Potentes", 
            "preco_1l": 52.00, 
            "desc": "Picante na medida certa e revigorante.",
            "ingredientes": "Gengibre fresco ralado, limão tahiti, mel silvestre puro e Cachaça Envelhecida.",
            "foto": "https://images.unsplash.com/photo-1582106245687-cbb46679fdbb?auto=format&fit=crop&w=600&q=80"
        },
        {
            "id": 24, 
            "nome": "Batida de Pimenta Rosa com Abacaxi", 
            "categoria": "🌶️ Exóticas & Potentes", 
            "preco_1l": 54.00, 
            "desc": "Sofisticação e ardência leve.",
            "ingredientes": "Abacaxi fresco, grãos de pimenta rosa, Cachaça Artesanal e Leite Condensado.",
            "foto": "https://images.unsplash.com/photo-1563227812-0ea4c22e6cc8?auto=format&fit=crop&w=600&q=80"
        }
    ]

    # Filtro por Categoria em abas visuais ou selectbox limpo
    cat_cols = st.selectbox("Filtrar Categoria:", ["⭐ Todas as Batidas", "🥥 Clássicas & Frutas Tropicais", "🍷 Vinhos & Especiais", "🌶️ Exóticas & Potentes"])

    if cat_cols == "⭐ Todas as Batidas":
        itens_filtrados = cardapio_detalhado
    else:
        itens_filtrados = [item for item in cardapio_detalhado if item["categoria"] == cat_cols]

    st.markdown("---")

    # Exibição em grade otimizada para mobile
    for item in itens_filtrados:
        with st.container():
            st.markdown(f"### 🍸 {item['nome']}")
            
            c_foto, c_detalhes = st.columns([1.2, 2])
            
            with c_foto:
                st.image(item['foto'], use_container_width=True)
                
            with c_detalhes:
                st.markdown(f"*{item['desc']}*")
                st.markdown(f"📝 **Ingredientes:** _{item['ingredientes']}_")
                
                # Seletor de Tamanho
                tamanho = st.selectbox("Tamanho da Garrafa:", ["300ml", "500ml", "1 Litro"], key=f"tam_{item['id']}")
                
                # Cálculo de preço proporcional
                if tamanho == "300ml":
                    preco_final = item['preco_1l'] * 0.38
                elif tamanho == "500ml":
                    preco_final = item['preco_1l'] * 0.60
                else:
                    preco_final = item['preco_1l']
                
                st.markdown(f"💰 **R$ {preco_final:.2f}**")
                
                if st.button("🛒 Adicionar ao Carrinho", key=f"add_{item['id']}"):
                    item_carrinho = {
                        "nome": f"{item['nome']} ({tamanho})",
                        "preco": preco_final
                    }
                    st.session_state.carrinho.append(item_carrinho)
                    st.success("Adicionado com sucesso! ✅")

            st.markdown("---")

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
        st.success(f"🎉 Pedido **{st.session_state.ultimo_pedido}** finalizado com sucesso e salvo com data e hora!")
        st.balloons()
        if st.button("🔄 Fazer Novo Pedido"):
            st.session_state.ultimo_pedido = None
            st.rerun()
    

import streamlit as st
import database as db
import requests

def render():
    st.title("🍸 QG das Batidas - Cardápio Oficial")
    st.markdown("Escolha entre as nossas **30 batidas artesanais exclusivas** preparadas pelo Mestre Sidney e faça o seu pedido direto!")

    # Inicializar o carrinho na sessão se não existir
    if "carrinho" not in st.session_state:
        st.session_state.carrinho = []

    # Lista completa das 30 batidas organizadas por categoria
    cardapio_30 = [
        {"id": 1, "nome": "1. Batida de Coco Cremoso 1L", "categoria": "🥥 Clássicas & Frutas Tropicais", "preco": 45.00, "desc": "Suave, cremosa e marcante."},
        {"id": 2, "nome": "2. Batida de Maracujá com Leite Condensado 1L", "categoria": "🥥 Clássicas & Frutas Tropicais", "preco": 48.00, "desc": "Equilíbrio perfeito entre o azedinho e o doce."},
        {"id": 3, "nome": "3. Batida de Morango Silvestre 1L", "categoria": "🥥 Clássicas & Frutas Tropicais", "preco": 50.00, "desc": "Feita com frutas frescas selecionadas."},
        {"id": 4, "nome": "4. Batida de Abacaxi com Hortelã 1L", "categoria": "🥥 Clássicas & Frutas Tropicais", "preco": 46.00, "desc": "Refrescante e revigorante."},
        {"id": 5, "nome": "5. Batida de Manga com Maracujá 1L", "categoria": "🥥 Clássicas & Frutas Tropicais", "preco": 49.00, "desc": "Toque tropical irresistível."},
        {"id": 6, "nome": "6. Batida de Limão Siciliano 1L", "categoria": "🥥 Clássicas & Frutas Tropicais", "preco": 47.00, "desc": "Citrico na medida certa."},
        {"id": 7, "nome": "7. Batida de Goiaba Vermelha 1L", "categoria": "🥥 Clássicas & Frutas Tropicais", "preco": 45.00, "desc": "Sabor autêntico da fruta."},
        {"id": 8, "nome": "8. Batida de Caju com Pitada de Sal 1L", "categoria": "🥥 Clássicas & Frutas Tropicais", "preco": 48.00, "desc": "O clássico reinventado."},
        {"id": 9, "nome": "9. Batida de Vinho Tinto Suave 1L", "categoria": "🍷 Vinhos & Especiais de Inverno", "preco": 52.00, "desc": "Encorpada e aconchegante."},
        {"id": 10, "nome": "10. Batida de Vinho com Canela e Cravo 1L", "categoria": "🍷 Vinhos & Especiais de Inverno", "preco": 55.00, "desc": "Aromatizada com especiarias finas."},
        {"id": 23, "nome": "23. Batida de Gengibre com Limão e Mel 1L", "categoria": "🌶️ Exóticas & Potentes (Pimenta / Gengibre / Ervas)", "preco": 52.00, "desc": "Picante na medida certa."},
        {"id": 24, "nome": "24. Batida de Pimenta Rosa com Abacaxi 1L", "categoria": "🌶️ Exóticas & Potentes (Pimenta / Gengibre / Ervas)", "preco": 54.00, "desc": "Sofisticação e ardência leve."},
        {"id": 25, "nome": "25. Batida de Capim-Santo com Limão 1L", "categoria": "🌶️ Exóticas & Potentes (Pimenta / Gengibre / Ervas)", "preco": 48.00, "desc": "Herbal e extremamente refrescante."}
    ]

    # Filtro por Categoria
    categorias_disponiveis = ["⭐ Todas as 30 Batidas", "🥥 Clássicas & Frutas Tropicais", "🍷 Vinhos & Especiais de Inverno", "🌶️ Exóticas & Potentes (Pimenta / Gengibre / Ervas)"]
    categoria_selecionada = st.selectbox("Filtrar por Categoria:", categorias_disponiveis)

    if categoria_selecionada == "⭐ Todas as 30 Batidas":
        itens_filtrados = cardapio_30
    else:
        itens_filtrados = [item for item in cardapio_30 if item["categoria"] == categoria_selecionada]

    st.markdown(f"**Exibindo {len(itens_filtrados)} item(ns)**")
    st.markdown("---")

    for item in itens_filtrados:
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"### {item['nome']}")
            st.markdown(f"💰 **R$ {item['preco']:.2f}** | *{item['desc']}*")
        with col2:
            if st.button("🛒 Adicionar", key=f"add_{item['id']}"):
                st.session_state.carrinho.append(item)
                st.success("Adicionado!")
        st.markdown("---")

    # --- CARRINHO E CHECKOUT ---
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🛍 Seu Carrinho")
    
    if len(st.session_state.carrinho) == 0:
        st.sidebar.info("O carrinho está vazio.")
    else:
        total_carrinho = 0
        for prod in st.session_state.carrinho:
            st.sidebar.markdown(f"- {prod['nome']} (R$ {prod['preco']:.2f})")
            total_carrinho += prod['preco']
        
        st.sidebar.markdown(f"**Total a Pagar: R$ {total_carrinho:.2f}**")
        
        if st.sidebar.button("🗑️️ Limpar Carrinho"):
            st.session_state.carrinho = []
            st.rerun()

        st.sidebar.markdown("---")
        st.sidebar.markdown("### 📝 Cadastro & Endereço")
        
        # Variáveis de sessão para preenchimento
        if "rua_val" not in st.session_state:
            st.session_state.rua_val = ""
        if "bairro_val" not in st.session_state:
            st.session_state.bairro_val = ""
        if "cidade_val" not in st.session_state:
            st.session_state.cidade_val = "Taboão da Serra"

        # Campo de CEP fora do form principal para consulta instantânea
        cep = st.sidebar.text_input("CEP (Apenas números):", max_chars=8, key="input_cep")
        
        if len(cep) == 8:
            try:
                res = requests.get(f"https://viacep.com.br/ws/{cep}/json/")
                data_cep = res.json()
                if "erro" not in data_cep:
                    st.session_state.rua_val = data_cep.get("logradouro", "")
                    st.session_state.bairro_val = data_cep.get("bairro", "")
                    st.session_state.cidade_val = data_cep.get("localidade", "")
            except:
                pass

        with st.sidebar.form("form_checkout"):
            nome_cliente = st.text_input("Seu Nome Completo:")
            whatsapp = st.text_input("WhatsApp / Telefone:")
            data_nascimento = st.text_input("Data de Nascimento (DD/MM/AAAA):", placeholder="Ex: 12/10/1985")
            
            st.markdown("---")
            st.markdown("📍 **Confirme os Dados de Endereço**")
            
            rua = st.text_input("Rua / Logradouro:", value=st.session_state.rua_val)
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
                    endereco_completo = f"{rua}, nº {numero} - {bairro}, {cidade} (CEP: {cep})"
                    
                    novo_registro = {
                        "cliente": nome_cliente,
                        "whatsapp": whatsapp,
                        "nascimento": data_nascimento,
                        "endereco": endereco_completo,
                        "pagamento": pagamento,
                        "itens": st.session_state.carrinho,
                        "total": total_carrinho
                    }
                    db.salvar_cliente(novo_registro)
                    
                    st.success("🎉 Pedido registado com sucesso!")
                    st.balloons()
                    st.session_state.carrinho = []
        

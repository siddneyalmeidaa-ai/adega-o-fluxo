import streamlit as st

def render():
    st.title("🍸 QG das Batidas - Cardápio Oficial")
    st.markdown("Escolha entre as nossas **30 batidas artesanais exclusivas** preparadas pelo Mestre Sidney e peça direto pelo WhatsApp!")

    # Filtro por Categoria
    categoria = st.selectbox("Filtrar por Categoria:", [
        "🌟 Todas as 30 Batidas",
        "🥥 Clássicas & Frutas Tropicais",
        "🍷 Vinhos & Especiais de Inverno",
        "🍫 Cremosas & Doces (Leite Condensado / Chocolate)",
        "🌶️ Exóticas & Potentes (Pimenta / Gengibre / Ervas)",
        "💎 Linha Premium & Dry Martini"
    ])

    # Lista completa das 30 batidas
    cardapio_30 = [
        # Clássicas e Frutas Tropicais (1 a 8)
        {"id": 1, "nome": "1. Batida de Coco Cremoso 1L", "cat": "🥥 Clássicas & Frutas Tropicais", "preco": 45.0, "desc": "O clássico supremo, super cremoso e refrescante."},
        {"id": 2, "nome": "2. Batida de Maracujá com Leite 1L", "cat": "🥥 Clássicas & Frutas Tropicais", "preco": 48.0, "desc": "O equilíbrio perfeito entre o azedinho e o doce."},
        {"id": 3, "nome": "3. Batida de Morango Silvestre 1L", "cat": "🥥 Clássicas & Frutas Tropicais", "preco": 50.0, "desc": "Feita com morangos frescos selecionados."},
        {"id": 4, "nome": "4. Batida de Abacaxi com Hortelã 1L", "cat": "🥥 Clássicas & Frutas Tropicais", "preco": 46.0, "desc": "Refrescância extrema para dias quentes."},
        {"id": 5, "nome": "5. Batida de Manga com Maracujá 1L", "cat": "🥥 Clássicas & Frutas Tropicais", "preco": 48.0, "desc": "Mix tropical de respeito."},
        {"id": 6, "nome": "6. Batida de Limão Siciliano 1L", "cat": "🥥 Clássicas & Frutas Tropicais", "preco": 46.0, "desc": "Cítrica, leve e sofisticada."},
        {"id": 7, "nome": "7. Batida de Goiaba Vermelha 1L", "cat": "🥥 Clássicas & Frutas Tropicais", "preco": 45.0, "desc": "Sabor marcante e textura aveludada."},
        {"id": 8, "nome": "8. Batida de Caju com Pitada de Sal 1L", "cat": "🥥 Clássicas & Frutas Tropicais", "preco": 48.0, "desc": "A verdadeira essência brasileira."},

        # Vinhos e Especiais (9 a 15)
        {"id": 9, "nome": "9. Batida de Vinho Tinto com Morango 1L", "cat": "🍷 Vinhos & Especiais de Inverno", "preco": 58.0, "desc": "Lote exclusivo e amado pela galera."},
        {"id": 10, "nome": "10. Batida de Vinho Bordô Suave 1L", "cat": "🍷 Vinhos & Especiais de Inverno", "preco": 55.0, "desc": "Doce na medida certa."},
        {"id": 11, "nome": "11. Batida de Vinho com Canela e Cravo 1L", "cat": "🍷 Vinhos & Especiais de Inverno", "preco": 56.0, "desc": "Toque especial de especiarias."},
        {"id": 12, "nome": "12. Batida de Jabuticaba Artesanal 1L", "cat": "🍷 Vinhos & Especiais de Inverno", "preco": 60.0, "desc": "Fruta colhida e batida na hora."},
        {"id": 13, "nome": "13. Batida de Amora Silvestre 1L", "cat": "🍷 Vinhos & Especiais de Inverno", "preco": 58.0, "desc": "Rica em sabor e antioxidantes."},
        {"id": 14, "nome": "14. Batida de Frutas Vermelhas 1L", "cat": "🍷 Vinhos & Especiais de Inverno", "preco": 60.0, "desc": "Mix de mirtilo, framboesa e morango."},
        {"id": 15, "nome": "15. Batida de Figo com Mel 1L", "cat": "🍷 Vinhos & Especiais de Inverno", "preco": 62.0, "desc": "Combinação nobre e elegante."},

        # Cremosas e Doces (16 a 22)
        {"id": 16, "nome": "16. Batida de Chocolate Cremoso 1L", "cat": "🍫 Cremosas & Doces (Leite Condensado / Chocolate)", "preco": 50.0, "desc": "Para os formigões de plantão."},
        {"id": 17, "nome": "17. Batida de Doce de Leite com Paçoca 1L", "cat": "🍫 Cremosas & Doces (Leite Condensado / Chocolate)", "preco": 52.0, "desc": "Uma explosão de sabor mineiro."},
        {"id": 18, "nome": "18. Batida de Nutella com Avelã 1L", "cat": "🍫 Cremosas & Doces (Leite Condensado / Chocolate)", "preco": 65.0, "desc": "O ápice da indulgência e luxo."},
        {"id": 19, "nome": "19. Batida de Leite Ninho Trufado 1L", "cat": "🍫 Cremosas & Doces (Leite Condensado / Chocolate)", "preco": 55.0, "desc": "Cremoso demais, impossível tomar um só."},
        {"id": 20, "nome": "20. Batida de Ovomaltine Crocante 1L", "cat": "🍫 Cremosas & Doces (Leite Condensado / Chocolate)", "preco": 54.0, "desc": "Aqueles floquinhos crocantes que fazem a diferença."},
        {"id": 21, "nome": "21. Batida de Marula Artesanal 1L", "cat": "🍫 Cremosas & Doces (Leite Condensado / Chocolate)", "preco": 60.0, "desc": "Inspirada no famoso licor africano."},
        {"id": 22, "nome": "22. Batida de Café Expresso com Chocolate 1L", "cat": "🍫 Cremosas & Doces (Leite Condensado / Chocolate)", "preco": 50.0, "desc": "Energia e sabor na mesma garrafa."},

        # Exóticas e Potentes (23 a 26)
        {"id": 23, "nome": "23. Batida de Gengibre com Limão e Mel 1L", "cat": "🌶️ Exóticas & Potentes (Pimenta / Gengibre / Ervas)", "preco": 52.0, "desc": "Picante na medida certa."},
        {"id": 24, "nome": "24. Batida de Pimenta Rosa com Abacaxi 1L", "cat": "🌶️ Exóticas & Potentes (Pimenta / Gengibre / Ervas)", "preco": 54.0, "desc": "Sofisticação e ardência leve."},
        {"id": 25, "nome": "25. Batida de Capim-Santo com Limão 1L", "cat": "🌶️ Exóticas & Potentes (Pimenta / Gengibre / Ervas)", "preco": 48.0, "desc": "Herbal, relaxante e super refrescante."},
        {"id": 26, "nome": "26. Batida de Catuaba com Açaí 1L", "cat": "🌶️ Exóticas & Potentes (Pimenta / Gengibre / Ervas)", "preco": 50.0, "desc": "Para dar aquela energia extra no rolê."},

        # Premium e Dry Martini (27 a 30)
        {"id": 27, "nome": "27. Dry Martini Artesanal QG 750ml", "cat": "💎 Linha Premium & Dry Martini", "preco": 65.0, "desc": "O clássico dos clássicos preparado com maestria."},
        {"id": 28, "nome": "28. Batida Premium de Coco com Baunilha Fava 1L", "cat": "💎 Linha Premium & Dry Martini", "preco": 70.0, "desc": "Feita com favas de baunilha de verdade."},
        {"id": 29, "nome": "29. Batida de Frutas Vermelhas com Espumante 750ml", "cat": "💎 Linha Premium & Dry Martini", "preco": 75.0, "desc": "Elegância pura para comemorações."},
        {"id": 30, "nome": "30. O Elixir do Mestre (Segredo da Casa) 1L", "cat": "💎 Linha Premium & Dry Martini", "preco": 85.0, "desc": "A receita secreta e mais potente do QG!"}
    ]

    # Filtragem na tela
    if categoria == "🌟 Todas as 30 Batidas":
        itens_filtrados = cardapio_30
    else:
        itens_filtrados = [item for item in cardapio_30 if item["cat"] == categoria]

    st.markdown(f"### Exibindo {len(itens_filtrados)} item(ns)")

    # Exibição em cards usando colunas
    for i in range(0, len(itens_filtrados), 3):
        cols = st.columns(3)
        for j in range(3):
            if i + j < len(itens_filtrados):
                batida = itens_filtrados[i + j]
                with cols[j]:
                    st.markdown(f"**{batida['nome']}**")
                    st.write(f"💰 **R$ {batida['preco']:.2f}**")
                    st.write(batida['desc'])
                    if st.button(f"🛒 Pedir", key=f"ped_batida_{batida['id']}"):
                        st.success(f"{batida['nome']} adicionada ao pedido!")
                    st.markdown("---")
                  

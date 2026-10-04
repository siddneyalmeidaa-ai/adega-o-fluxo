import streamlit as st
import json
import os

def render():
    st.subheader("🚀 Central de CRM & Gestão de Pedidos")
    
    # Abas internas do Centro de Comando
    aba_crm, aba_pedidos = st.tabs(["📢 Campanhas de WhatsApp", "📦 Pedidos & Clientes da Vitrine"])

    # Carregar pedidos do arquivo JSON local de backup
    pedidos = []
    arquivo_pedidos = "pedidos_qg.json"
    
    if os.path.exists(arquivo_pedidos):
        try:
            with open(arquivo_pedidos, "r", encoding="utf-8") as f:
                pedidos = json.load(f)
        except:
            pedidos = []

    with aba_crm:
        st.markdown("Selecione a campanha estratégica para conversão e retenção da base:")

        tipo_campanha = st.selectbox("Escolha a Campanha Estratégica:", [
            "🎉 Aniversariantes do Mês",
            "⚡ Promoção Relâmpago",
            "💤 Clientes Inativos (+30 dias)",
            "🧊 Esquenta de Sexta / Fim de Semana (Antecipação)",
            "🛒 Recuperação de Carrinho / Pedido Não Concluído",
            "🎁 Programa VIP 'Clube do Mestre' (Indicação)",
            "⭐ Pesquisa de Satisfação Pós-Compra",
            "💰 Saldo de Cashback Disponível",
            "🚨 Alerta de Fim de Estoque / Lote Limitado",
            "🍸 Sugestão de Combo / Acompanhamento Automático (Cross-selling)",
            "🎁 Reativação 'Cliente Sumido há 60 Dias' com Brinde",
            "🧠 Abordagem VIP Baseada no Histórico de Compra Anterior"
        ], key="select_campanha_crm")

        # Dicionário com os textos de cada campanha
        textos_campanhas = {
            "🎉 Aniversariantes do Mês": "Fala, [Nome]! Parabéns pelo seu dia! 🥂 Para comemorar em grande estilo, o QG das Batidas te dá um presente especial na sua próxima garrafa. Me chama aqui para resgatar!",
            "⚡ Promoção Relâmpago": "Atenção, [Nome]! ⚡ Promoção relâmpago nas próximas 2 horas: Batida artesanal com frete grátis e preço especial. Vai perder essa?",
            "💤 Clientes Inativos (+30 dias)": "Oi, [Nome]! Sentimos sua falta por aqui. 🍹 Passando para avisar que temos sabores novos geladinhos te esperando. Bora pedir uma hoje?",
            "🧊 Esquenta de Sexta / Fim de Semana (Antecipação)": "Fala, [Nome]! O fim de semana está batendo na porta. 🧊 Garanta já a sua batida artesanal geladinha para o rolê de hoje e evite a espera. Vai de Coco, Maracujá ou Vinho? 🍹🔥",
            "🛒 Recuperação de Carrinho / Pedido Não Concluído": "E aí, [Nome], tudo bem? Vi aqui que você montou sua batida no QG mas acabou não finalizando. Ficou alguma dúvida sobre os sabores ou os tamanhos? Me avisa aqui que eu te ajudo a liberar a entrega! 🚀",
            "🎁 Programa VIP 'Clube do Mestre' (Indicação)": "Salve, [Nome]! Quer ganhar R$ 15 de desconto na sua próxima garrafa? Indique um amigo para conhecer o QG das Batidas. Assim que ele fizer o primeiro pedido, o seu bônus é liberado automaticamente! 🎁✨",
            "⭐ Pesquisa de Satisfação Pós-Compra": "Fala, [Nome]! Curtiu a batida de ontem? 🍸 Seu feedback é sagrado para o nosso padrão. Para agradecer a moral, deixei um cupom de 10% OFF garantido para a sua próxima recarga. É só me chamar por aqui! 👊",
            "💰 Saldo de Cashback Disponível": "Fala, [Nome]! Você tem R$ 12,50 de cashback acumulado no QG das Batidas esperando por você. Quer resgatar hoje no seu pedido? 💰🚀",
            "🚨 Alerta de Fim de Estoque / Lote Limitado": "Atenção, [Nome]! 🚨 Nosso lote exclusivo de Batida de Vinho com Morango está na reta final (restam apenas 3 garrafas). Garanta a sua antes que esgote! 🍷🔥",
            "🍸 Sugestão de Combo / Acompanhamento Automático (Cross-selling)": "Boa escolha, [Nome]! Vai levar a batida de Coco? Que tal turbinar o rolê com o nosso kit com Gelo de Água de Coco e Copos Térmicos por apenas +R$ 15? 🧊✨",
            "🎁 Reativação 'Cliente Sumido há 60 Dias' com Brinde": "Sumido nada, [Nome]! 👊 Para celebrar o seu retorno ao QG das Batidas, na compra de qualquer 500ml hoje, você leva um copo exclusivo de cortesia. Vamos nessa? 🍹🎁",
            "🧠 Abordagem VIP Baseada no Histórico de Compra Anterior": "Fala, [Nome]! Tudo certo? A batida de Maracujá que você pediu da última vez fez sucesso? Preparei um lote fresquinho aqui, quer repetir a dose hoje? 🍸🔥"
        }

        # Atualizar a caixa de texto automaticamente quando a campanha mudar
        msg_padrao = textos_campanhas.get(tipo_campanha, "Fala, [Nome]! Tudo bem?")
        
        if "ultima_campanha_selecionada" not in st.session_state:
            st.session_state.ultima_campanha_selecionada = tipo_campanha
            st.session_state.txt_msg_crm = msg_padrao
        elif st.session_state.ultima_campanha_selecionada != tipo_campanha:
            st.session_state.ultima_campanha_selecionada = tipo_campanha
            st.session_state.txt_msg_crm = msg_padrao

        texto_msg = st.text_area("Texto da Mensagem (Editável - Use [Nome] para personalizar):", height=120, key="txt_msg_crm")

        total_clientes = len(pedidos)
        col_zap1, col_zap2 = st.columns(2)
        with col_zap1:
            st.metric(label="Público-Alvo Estimado", value=f"{total_clientes} Cliente(s) na Base")
        with col_zap2:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🚀 Disparar Campanha via WhatsApp", key="btn_disparar_crm"):
                st.success(f"Campanha disparada para {total_clientes} cliente(s) com sucesso!")

        st.markdown("---")
        st.markdown("### 📋 Lista de Clientes Capturados para Disparo Direto")
        if not pedidos:
            st.info("Nenhum cliente cadastrado via pedidos ainda.")
        else:
            for p in pedidos:
                c_nome = p.get("cliente", "Cliente")
                c_whats = p.get("whatsapp", "")
                c_nasc = p.get("nascimento", "Não informada")
                whats_clean = "".join(filter(str.isdigit, str(c_whats)))
                
                st.markdown(f"👤 **{c_nome}** | 🎂 Nasc: `{c_nasc}` | 📱 WhatsApp: `{c_whats}`")
                if whats_clean:
                    msg_personalizada = texto_msg.replace("[Nome]", c_nome)
                    st.markdown(f"[💬 Enviar WhatsApp Direto](https://wa.me/55{whats_clean}?text={msg_personalizada.replace(' ', '%20')})", unsafe_allow_html=True)
                st.markdown("---")

    with aba_pedidos:
        st.markdown("### 📦 Acompanhamento de Pedidos em Tempo Real")
        st.markdown("Aqui aparecem automaticamente todos os pedidos finalizados pelos clientes na vitrine com data, horário, nomes, telefones e datas de nascimento.")

        if not pedidos:
            st.info("📭 Nenhum pedido registado até o momento. Faça um teste simulando um pedido na vitrine do cardápio!")
        else:
            st.markdown(f"**Total de Pedidos na Base:** {len(pedidos)}")
            st.markdown("---")

            for idx, pedido in enumerate(reversed(pedidos)):
                if isinstance(pedido, dict):
                    num_ped = pedido.get("pedido_id", f"QG-#{len(pedidos) - idx}")
                    data_hora_ped = pedido.get("data_hora", "Data não registrada")
                    cliente = pedido.get("cliente", "Cliente Anônimo")
                    whatsapp = pedido.get("whatsapp", "Não informado")
                    nascimento = pedido.get("nascimento", "Não informada")
                    endereco = pedido.get("endereco", "Endereço não informado")
                    pagamento = pedido.get("pagamento", "Dinheiro")
                    total = pedido.get("total", 0.0)
                    itens = pedido.get("itens", [])

                    with st.container():
                        st.markdown(f"### 🛒 Pedido `{num_ped}` - {cliente}")
                        st.markdown(f"🕒 **Data e Horário:** `{data_hora_ped}`")
                        
                        c1, c2 = st.columns(2)
                        with c1:
                            st.markdown(f"📱 **WhatsApp:** `{whatsapp}`")
                            st.markdown(f"🎂 **Data de Nascimento:** `{nascimento}`")
                            st.markdown(f"💳 **Forma de Pagamento:** `{pagamento}`")
                        with c2:
                            st.markdown(f"📍 **Endereço:** {endereco}")
                            st.markdown(f"💰 **Total:** **R$ {total:.2f}**")

                        st.markdown("**Itens do Pedido:**")
                        for item in itens:
                            st.markdown(f"- {item.get('nome', 'Item')} (R$ {item.get('preco', 0.0):.2f})")

                        whatsapp_clean = "".join(filter(str.isdigit, str(whatsapp)))
                        if whatsapp_clean:
                            msg_w = f"Olá {cliente}! Aqui é do QG das Batidas. Recebemos o seu pedido {num_ped} no valor de R$ {total:.2f} às {data_hora_ped}. Estamos a preparar tudo com carinho!"
                            st.markdown(f"[💬 Falar com o Cliente no WhatsApp](https://wa.me/55{whatsapp_clean}?text={msg_w.replace(' ', '%20')})", unsafe_allow_html=True)

                        st.markdown("---")
        

import streamlit as st
from datetime import datetime

# Importando os módulos da pasta views
from views import vitrine_cardapio, produtos, caixa, crm, metricas

st.set_page_config(
    page_title="QG das Batidas - Sistema Operacional",
    page_icon="🍸",
    layout="wide"
)

# Carimbo de data e hora no sidebar
st.sidebar.markdown(f"📅 **Data:** 03/10/2026")
st.sidebar.markdown(f"🕒 **Hora:** 23:45 -03")
st.sidebar.markdown(f"📍 **Local:** Taboão da Serra, SP")
st.sidebar.markdown("---")

menu_principal = st.sidebar.selectbox("Navegação do Sistema:", [
    "🏠 Vitrine & Cardápio (30 Batidas)", 
    "⚙️ Painel Administrativo / Centro de Comando"
])

if menu_principal == "🏠 Vitrine & Cardápio (30 Batidas)":
    vitrine_cardapio.render()

elif menu_principal == "⚙️ Painel Administrativo / Centro de Comando":
    pin_input = st.text_input("Digite o PIN Administrativo:", type="password", key="admin_pin")
    
    if pin_input != "5120":
        if pin_input != "":
            st.error("PIN incorreto. Acesso restrito.")
        st.warning("Insira o PIN correto para gerenciar o painel.")
        st.stop()

    st.success("Acesso Liberado ao Centro de Comando pelo Mestre Sidney!")

    tab_op, tab_caixa, tab_crm, tab_metricas = st.tabs([
        "🛒 Gestão de Produtos & Estoque", 
        "💰 Caixa & Sangrias", 
        "🚀 Automação & CRM (12 Campanhas)", 
        "📊 Métricas & Desempenho"
    ])

    with tab_op:
        produtos.render()
    with tab_caixa:
        caixa.render()
    with tab_crm:
        crm.render()
    with tab_metricas:
        metricas.render()
      

import streamlit as st
from datetime import datetime
import database as db

# Importação segura dos módulos estruturados na pasta views
try:
    from views import vitrine_cardapio, produtos, caixa, crm, metricas
except ImportError:
    import vitrine_cardapio, produtos, caixa, crm, metricas

# Configuração da Página
st.set_page_config(
    page_title="QG das Batidas - Sistema Operacional",
    page_icon="🍸",
    layout="wide"
)

# Sidebar Informativa & Operacional
st.sidebar.markdown(f"📅 **Data:** 04/10/2026")
st.sidebar.markdown(f"🕒 **Hora:** 00:21 -03")
st.sidebar.markdown(f"📍 **Local:** Taboão da Serra, SP")
st.sidebar.markdown("---")

st.sidebar.markdown("### 🧭 Navegação Principal")
menu_principal = st.sidebar.selectbox("Escolha a Tela:", [
    "🏠 Vitrine & Cardápio (30 Batidas)", 
    "⚙️ Painel Administrativo / Centro de Comando"
])

# Roteamento das Telas
if menu_principal == "🏠 Vitrine & Cardápio (30 Batidas)":
    vitrine_cardapio.render()

elif menu_principal == "⚙️ Painel Administrativo / Centro de Comando":
    st.sidebar.markdown("---")
    pin_input = st.sidebar.text_input("PIN de Acesso Restrito:", type="password", key="admin_pin")
    
    if pin_input != "5120":
        if pin_input != "":
            st.sidebar.error("PIN incorreto.")
        st.warning("🔒 Insira o PIN correto na barra lateral para desbloquear o Centro de Comando.")
        st.stop()

    st.sidebar.success("Acesso Autorizado!")
    st.title("⚙️ Centro de Comando Operacional")
    st.markdown("Gestão unificada de estoque, fluxo de caixa, campanhas de CRM e métricas de desempenho.")

    # Abas do Painel Administrativo
    tab_op, tab_caixa, tab_crm, tab_metricas = st.tabs([
        "🛒 Produtos & Estoque", 
        "💰 Caixa & Sangrias", 
        "🚀 Automação & CRM", 
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
        

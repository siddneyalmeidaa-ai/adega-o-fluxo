import streamlit as st
from datetime import datetime

# Configuração Inicial da Página
st.set_page_config(
    page_title="QG das Batidas - Sistema Operacional",
    page_icon="🍸",
    layout="wide"
)

# Tentativa segura de importação individual de cada módulo
try:
    from views import vitrine_cardapio
except ImportError:
    import vitrine_cardapio

try:
    from views import produtos
except ImportError:
    try:
        import produtos
    except ImportError:
        produtos = None

try:
    from views import caixa
except ImportError:
    try:
        import caixa
    except ImportError:
        caixa = None

try:
    from views import crm
except ImportError:
    try:
        import crm
    except ImportError:
        crm = None

try:
    from views import metricas
except ImportError:
    try:
        import metricas
    except ImportError:
        metricas = None

# Sidebar Informativa & Operacional
st.sidebar.markdown(f"📅 **Data:** 04/10/2026")
st.sidebar.markdown(f"🕒 **Hora:** 00:22 -03")
st.sidebar.markdown(f"📍 **Local:** Taboão da Serra, SP")
st.sidebar.markdown("---")

st.sidebar.markdown("### 🧭 Navegação Principal")
menu_principal = st.sidebar.selectbox("Escolha a Tela:", [
    "🏠 Vitrine & Cardápio (30 Batidas)", 
    "⚙️ Painel Administrativo / Centro de Comando"
])

# Roteamento das Telas
if menu_principal == "🏠 Vitrine & Cardápio (30 Batidas)":
    if vitrine_cardapio and hasattr(vitrine_cardapio, 'render'):
        vitrine_cardapio.render()
    else:
        st.error("Módulo de vitrine não encontrado.")

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
        if produtos and hasattr(produtos, 'render'):
            produtos.render()
        else:
            st.info("Módulo de produtos em carregamento.")

    with tab_caixa:
        if caixa and hasattr(caixa, 'render'):
            caixa.render()
        else:
            st.info("Módulo de caixa em carregamento.")

    with tab_crm:
        if crm and hasattr(crm, 'render'):
            crm.render()
        else:
            st.info("Módulo de CRM em carregamento.")

    with tab_metricas:
        if metricas and hasattr(metricas, 'render'):
            metricas.render()
        else:
            st.info("Módulo de métricas em carregamento.")
            

import streamlit as st

def render():
    st.subheader("💰 Caixa & Sangrias")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="Caixa Atual em Dinheiro", value="R$ 380,00")
        valor_sangria = st.number_input("Valor da Sangria (R$)", min_value=0.0, step=10.0, key="val_sangria")
        st.text_input("Motivo da Retirada (Ex: Gelo e Frutas)", key="motivo_sangria")
        if st.button("🚨 Registrar Sangria", key="btn_exec_sangria"):
            st.success(f"Sangria de R$ {valor_sangria:.2f} registrada com sucesso!")

    with col2:
        st.metric(label="Faturamento Total do Dia", value="R$ 1.450,00")
        if st.button("🔒 Realizar Fechamento de Caixa", key="btn_fechar_caixa"):
            st.success("Caixa fechado e relatório enviado para auditoria com sucesso!")
          

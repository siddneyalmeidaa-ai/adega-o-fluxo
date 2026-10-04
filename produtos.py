import streamlit as st
import pandas as pd

def render():
    st.subheader("🛒 Gestão de Produtos & Estoque")
    st.info("Controle em tempo real dos lotes e status de disponibilidade na vitrine.")
    
    produtos_df = pd.DataFrame({
        "Produto": ["Batida de Coco 1L", "Batida de Maracujá 1L", "Batida de Vinho com Morango", "Dry Martini Artesanal"],
        "Preço (R$)": [45.00, 48.00, 58.00, 60.00],
        "Status": ["Disponível", "Disponível", "Poucas Unidades (Escassez)", "Disponível"],
        "Estoque Atual (L)": [8.5, 4.0, 1.5, 6.0]
    })

    st.data_editor(produtos_df, key="editor_produtos_status", use_container_width=True)
    
    col_est1, col_est2 = st.columns(2)
    with col_est1:
        if st.button("💾 Salvar Alterações de Estoque", key="btn_salvar_estoque"):
            st.success("Estoque atualizado e sincronizado com a vitrine com sucesso!")
    with col_est2:
        if st.button("🚨 Ativar Alerta de Lote Limitado (WhatsApp)", key="btn_alerta_lote"):
            st.success("Disparo de escassez de lote ativado para a base!")
          

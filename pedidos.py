import streamlit as st
import sqlite3

def exibir_pedidos():
    st.markdown("### 📦 Gestão de Pedidos Registrados")
    conn = sqlite3.connect("qg_batidas.db")
    cursor = conn.cursor()
    cursor.execute("SELECT pedido_id, data_hora, cliente, whatsapp, pagamento, status, total FROM pedidos ORDER BY timestamp DESC")
    todos_pedidos = cursor.fetchall()
    conn.close()
    
    if not todos_pedidos:
        st.info("Nenhum pedido registado até o momento.")
    else:
        for p in todos_pedidos:
            with st.container(border=True):
                st.markdown(f"**ID do Pedido:** `{p[0]}` | **Data:** {p[1]} | **Status:** `{p[5]}`")
                st.markdown(f"**Cliente:** {p[2]} ({p[3]}) | **Pagamento:** {p[4]} | **Total:** R$ {p[6]:.2f}")
              

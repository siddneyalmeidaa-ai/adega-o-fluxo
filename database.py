import sqlite3

def init_db():
    conn = sqlite3.connect("qg_batidas.db")
    cursor = conn.cursor()
    
    # Tabela de Pedidos
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pedidos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pedido_id TEXT,
            timestamp TEXT,
            data_hora TEXT,
            cliente TEXT,
            whatsapp TEXT,
            nascimento TEXT,
            endereco TEXT,
            pagamento TEXT,
            status TEXT,
            total REAL
        )
    """)
    
    # Tabela de Caixa
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS caixa (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data_hora TEXT,
            tipo TEXT,
            descricao TEXT,
            valor REAL
        )
    """)
    
    # Tabela de CRM / Clientes
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS crm_clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            whatsapp TEXT,
            preferencia TEXT,
            compras_totais INTEGER
        )
    """)
    
    conn.commit()
    conn.close()
    

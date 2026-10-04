import json
import os
from datetime import datetime

DB_FILE = "clientes_db.json"

def carregar_clientes():
    if not os.path.exists(DB_FILE):
        # Base inicial com alguns clientes de exemplo do Mestre Sidney
        dados_iniciais = [
            {"id": 1, "nome": "Marcus", "telefone": "11999991111", "total_compras": 320.0, "cashback": 25.0, "ultima_compra": "2026-09-28", "status": "Ativo"},
            {"id": 2, "nome": "Beatriz", "telefone": "11988882222", "total_compras": 180.0, "cashback": 12.5, "ultima_compra": "2026-09-15", "status": "Ativo"},
            {"id": 3, "nome": "Carlos Silva", "telefone": "11977773333", "total_compras": 90.0, "cashback": 5.0, "ultima_compra": "2026-08-10", "status": "Inativo (+30 dias)"}
        ]
        salvar_clientes(dados_iniciais)
        return dados_iniciais
    
    with open(DB_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def salvar_clientes(lista_clientes):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(lista_clientes, f, ensure_ascii=False, indent=4)

def adicionar_cliente(nome, telefone, valor_compra=0.0):
    clientes = carregar_clientes()
    novo_id = max([c["id"] for c in clientes], default=0) + 1
    cashback_gerado = valor_compra * 0.10 # 10% de cashback
    
    novo_cliente = {
        "id": novo_id,
        "nome": nome,
        "telefone": telefone,
        "total_compras": valor_compra,
        "cashback": cashback_gerado,
        "ultima_compra": datetime.now().strftime("%Y-%m-%d"),
        "status": "Ativo"
    }
    clientes.append(novo_cliente)
    salvar_clientes(clientes)
    return novo_cliente
  

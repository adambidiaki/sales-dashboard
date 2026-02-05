import streamlit as st
import sqlite3

conn = sqlite3.connect('data.db', check_same_thread=False) # Conectar ao banco de dados (ou criar um novo se ele não existir)

cursor = conn.cursor() # Criar um cursor

# Consulta
def view_all_data(): 
    cursor.execute("SELECT * FROM insurance order by id asc") # Realizar uma consulta
    results = cursor.fetchall() # Buscar todos os resultados
    return results

# # Imprimir os resultados
# for row in results:
#     print(row)

# # Fechar a conexão
# cursor.close()
# conn.close()

import sqlite3
from langchain_ollama import OllamaLLM  # Az új, ajánlott import

# 1. Adatbázis inicializálása (maradt a régi)
def init_db():
    conn = sqlite3.connect('bolt.db')
    cursor = conn.cursor()
    
    # Vevők tábla
    cursor.execute('''CREATE TABLE IF NOT EXISTS vevok 
                      (vevo_id INTEGER PRIMARY KEY, nev TEXT, varos TEXT)''')
    
    # Eladások tábla (vevo_id-val kiegészítve)
    cursor.execute('''CREATE TABLE IF NOT EXISTS eladasok 
                      (id INTEGER PRIMARY KEY, termek TEXT, ar INTEGER, 
                       datum DATE, vevo_id INTEGER,
                       FOREIGN KEY(vevo_id) REFERENCES vevok(vevo_id))''')

    # Adatok feltöltése (töröljük a régit, hogy tiszta legyen)
    cursor.execute("DELETE FROM eladasok")
    cursor.execute("DELETE FROM vevok")

    # Minta vevők
    vevok = [(1, 'Kovács János', 'Budapest'), (2, 'Nagy Anna', 'Debrecen'), (3, 'Szabó Béla', 'Szeged')]
    cursor.executemany("INSERT INTO vevok VALUES (?,?,?)", vevok)

    # Minta eladások
    eladasok = [
        (101, 'Laptop', 350000, '2023-10-01', 1),
        (102, 'Eger', 5000, '2023-10-05', 1),
        (103, 'Monitor', 80000, '2023-10-10', 2),
        (104, 'Billentyűzet', 12000, '2023-10-12', 3),
        (105, 'Laptop', 350000, '2023-10-15', 2)
    ]
    cursor.executemany("INSERT INTO eladasok VALUES (?,?,?,?,?)", eladasok)
    
    conn.commit()
    conn.close()

init_db()

# 2. Az új LLM osztály használata
# Ha a géped lassabb, cseréld le a "llama3"-at "phi3"-ra!
llm = OllamaLLM(model="llama3") 

def sql_agent(question):
    schema = """
    Tábla: vevok | Oszlopok: vevo_id, nev, varos
    Tábla: eladasok | Oszlopok: id, termek, ar, datum, vevo_id
    Kapcsolat: eladasok.vevo_id = vevok.vevo_id
    """
    max_attempts = 3
    current_attempt = 0
    feedback = ""

    while current_attempt < max_attempts:
        prompt = f"""
        SQL szakértő vagy. Az adatbázis sémája: {schema}
        Kérdés: {question}
        {f"AZ ELŐZŐ KÓD HIBÁS VOLT: {feedback}. Kérlek javítsd ki!" if feedback else ""}
        Csak a nyers SQL kódot add meg, markdown kódblokk és magyarázat nélkül!
        Példa: SELECT SUM(ar) FROM eladasok
        """
        
        # Generálás
        response = llm.invoke(prompt).strip()
        
        # Tisztítás (néha a modellek betesznek ```sql blokkokat, azt vegyük le)
        sql_query = response.replace("```sql", "").replace("```", "").strip()
        
        print(f"--- {current_attempt+1}. próbálkozás SQL kódja: {sql_query}")

        try:
            conn = sqlite3.connect('bolt.db')
            res = conn.execute(sql_query).fetchall()
            conn.close()
            return f"Siker! Eredmény: {res}"
        
        except Exception as e:
            feedback = str(e)
            current_attempt += 1
            print(f"Hiba történt: {feedback}")

    return "Sajnos 3 próbálkozásból sem sikerült érvényes SQL-t írnom."

# 3. Teszt
print("\nÜgynök indul...")
#print(sql_agent("Mennyi volt az összes bevétel?"))
print(sql_agent("Mennyi bevételünk származott Laptop eladásból?"))
#print(sql_agent("Milyen termékeket vásárolt Kovács János?"))
#print(sql_agent("Városonként mennyi volt a teljes bevétel?"))
#print(sql_agent("Ki a legtöbbet költő vásárlónk és mennyit fizetett összesen?"))
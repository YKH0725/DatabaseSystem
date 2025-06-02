from db.db_config import conn, cursor

hospitalization_id = 'H001'
discharge_date = '2025-06-01'

cursor.execute("CALL update_discharge(%s, %s)", (hospitalization_id, discharge_date))
conn.commit()
print("出院成功，床位已释放。")
conn.close()

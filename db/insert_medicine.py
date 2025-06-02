from db.db_config import conn, cursor

cursor.execute("""
INSERT INTO Medicine (medicine_id, name, specification, unit_price, manufacturer, stock_quantity)
VALUES (%s, %s, %s, %s, %s, %s)
""", ('M005', '阿莫西林', '250mg*10粒', 9.8, '华北制药', 5))

conn.commit()
print("药品添加成功，触发器已检查库存")
conn.close()

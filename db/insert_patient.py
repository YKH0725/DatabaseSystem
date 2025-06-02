
from db_config import conn, cursor

cursor.execute("""
INSERT INTO Patient VALUES
('P003', '小二', 'M', '1990-01-01', '13800001111', '北京市朝阳区', '123456789')
""")
conn.commit()
print("插入成功！")
conn.close()

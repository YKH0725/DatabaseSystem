from db_config import conn, cursor

try:
    conn.begin()
    patient_id = 'P001'
    cursor.execute("""
        DELETE FROM PrescriptionDetail 
        WHERE record_id IN (
            SELECT record_id FROM MedicalRecord WHERE patient_id = %s
        )
    """, (patient_id,))
    cursor.execute("DELETE FROM MedicalRecord WHERE patient_id = %s", (patient_id,))
    conn.commit()
    print("删除成功！")
except Exception as e:
    conn.rollback()
    print("删除失败：", e)
finally:
    conn.close()


from flask import Flask, render_template, request
import pymysql

app = Flask(__name__)

def get_db():
    return pymysql.connect(
        host='localhost',
        user='root',
        password='YKHykh0725',
        database='hospital_system',
        port=3306,
        cursorclass=pymysql.cursors.DictCursor
    )

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/patients')
def patients():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Patient")
    data = cursor.fetchall()
    conn.close()
    return render_template('patients.html', patients=data)

@app.route('/add_patient', methods=['GET', 'POST'])
def add_patient():
    if request.method == 'POST':
        pid = request.form['patient_id']
        name = request.form['name']
        gender = request.form['gender']
        phone = request.form['phone']
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Patient (patient_id, name, gender, phone) VALUES (%s, %s, %s, %s)",
                       (pid, name, gender, phone))
        conn.commit()
        conn.close()
        return '添加成功！<a href="/patients">返回列表</a>'
    return render_template('add_patient.html')

@app.route('/doctors')
def doctors():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Doctor")
    doctors = cursor.fetchall()
    conn.close()
    return render_template('doctors.html', doctors=doctors)

@app.route('/medicines')
def medicines():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Medicine")
    medicines = cursor.fetchall()
    conn.close()
    return render_template('medicines.html', medicines=medicines)

@app.route('/appointments')
def appointments():
    return render_template('appointments.html')

@app.route('/medical_records')
def medical_records():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
            mr.record_id,
            mr.visit_date,
            mr.symptoms,
            mr.diagnosis,
            mr.patient_id,
            p.name AS patient_name,
            mr.doctor_id,
            d.name AS doctor_name
        FROM MedicalRecord mr
        JOIN Patient p ON mr.patient_id = p.patient_id
        JOIN Doctor d ON mr.doctor_id = d.doctor_id
    """)
    records = cursor.fetchall()
    conn.close()
    return render_template('medical_records.html', records=records)

@app.route('/hospitalizations')
def hospitalizations():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Hospitalization")
    hospitalizations = cursor.fetchall()
    conn.close()
    return render_template('hospitalizations.html', hospitalizations=hospitalizations)

@app.route('/discharge', methods=['GET', 'POST'])
def discharge():
    if request.method == 'POST':
        hosp_id = request.form['hosp_id']
        ddate = request.form['discharge_date']
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("CALL update_discharge(%s, %s)", (hosp_id, ddate))
        conn.commit()
        conn.close()
        return "出院完成，床位已释放。"
    return render_template('discharge_patient.html')

@app.route('/delete_invalid', methods=['POST'])
def delete_invalid_patient():
    conn = get_db()
    cursor = conn.cursor()
    try:
        conn.begin()
        patient_id = 'INVALID'  # 硬编码无效ID
        
        # 首先检查患者是否存在
        cursor.execute("SELECT 1 FROM Patient WHERE patient_id = %s", (patient_id,))
        if not cursor.fetchone():
            raise ValueError(f"患者ID {patient_id} 不存在")
        
        # 尝试删除不存在的患者记录
        cursor.execute("""
            DELETE FROM PrescriptionDetail 
            WHERE record_id IN (
                SELECT record_id FROM MedicalRecord WHERE patient_id = %s
            )
        """, (patient_id,))
        
        deleted_prescriptions = cursor.rowcount
        
        cursor.execute("DELETE FROM MedicalRecord WHERE patient_id = %s", (patient_id,))
        deleted_records = cursor.rowcount
        
        # 如果什么都没删除，也视为错误
        if deleted_prescriptions == 0 and deleted_records == 0:
            raise ValueError("没有找到任何记录可删除")
            
        conn.commit()
        return f"删除了 {deleted_records} 条就诊记录和 {deleted_prescriptions} 条处方明细"
        
    except Exception as e:
        conn.rollback()
        # 记录错误到日志
        app.logger.error(f"删除患者失败: {str(e)}")
        return f"事务已回滚，删除失败：{str(e)}"
    finally:
        conn.close()

@app.route('/prescription/<record_id>')
def prescription(record_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
            pd.medicine_id,
            m.name AS medicine_name,
            pd.quantity,
            pd.dosage,
            pd.frequency
        FROM PrescriptionDetail pd
        JOIN Medicine m ON pd.medicine_id = m.medicine_id
        WHERE pd.record_id = %s
    """, (record_id,))
    prescriptions = cursor.fetchall()
    conn.close()
    return render_template('prescription.html', prescriptions=prescriptions, record_id=record_id)

# 事务删除操作
@app.route('/delete_records', methods=['POST'])
def delete_records():
    patient_id = request.form['patient_id']
    try:
        conn = get_db()
        cursor = conn.cursor()
        conn.begin()
        
        cursor.execute("""
            DELETE FROM PrescriptionDetail 
            WHERE record_id IN (
                SELECT record_id FROM MedicalRecord WHERE patient_id = %s
            )
        """, (patient_id,))
        
        cursor.execute("DELETE FROM MedicalRecord WHERE patient_id = %s", (patient_id,))
        conn.commit()
        
        return '''
            <script>
                alert("事务删除成功！");
                window.location.href = "/";
            </script>
        '''
    except Exception as e:
        conn.rollback()
        return f'''
            <script>
                alert("删除失败：{str(e)}");
                window.location.href = "/";
            </script>
        '''
    finally:
        conn.close()

# 触发器测试操作
@app.route('/add_medicine', methods=['POST'])
def add_medicine():
    medicine_data = (
        request.form['medicine_id'],
        request.form['name'],
        request.form['spec'],
        request.form['price'],
        request.form['manufacturer'],
        request.form['stock']
    )
    
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Medicine (medicine_id, name, specification, 
                                unit_price, manufacturer, stock_quantity)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, medicine_data)
        conn.commit()
        
        return '''
            <script>
                alert("药品添加成功(未触发限制)");
                window.location.href = "/";
            </script>
        '''
    except Exception as e:
        return f'''
            <script>
                alert("触发器拦截：{str(e)}");
                window.location.href = "/";
            </script>
        '''
    finally:
        conn.close()

# 视图查询操作
@app.route('/view_records')
def view_records():
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM PatientVisitView LIMIT 10")
        records = cursor.fetchall()
        
        # 简单展示结果
        result = "<h2>患者就诊记录视图(最近10条)</h2><table border='1'>"
        result += "<tr><th>患者姓名</th><th>就诊日期</th><th>诊断结果</th><th>医生</th></tr>"
        
        for r in records:
            result += f"<tr><td>{r['patient_name']}</td><td>{r['visit_date']}</td>"
            result += f"<td>{r['diagnosis']}</td><td>{r['doctor_name']}</td></tr>"
            
        result += "</table><br><a href='/'>返回首页</a>"
        return result
    except Exception as e:
        return f"查询失败: {str(e)}"
    finally:
        conn.close()

@app.route('/reset_test_data', methods=['POST'])
def reset_test_data():
    conn = None
    try:
        conn = get_db()
        cursor = conn.cursor()
        
        # 1. 终止所有可能冲突的事务
        cursor.execute("""
            SELECT trx_mysql_thread_id 
            FROM information_schema.INNODB_TRX
            WHERE trx_state = 'RUNNING'
        """)
        running_trxs = cursor.fetchall()
        for trx in running_trxs:
            try:
                cursor.execute(f"KILL {trx['trx_mysql_thread_id']}")
            except:
                pass
        
        # 2. 分阶段重置数据
        conn.begin()
        
        # 2.1 禁用外键检查
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
        
        # 2.2 按依赖顺序清空表
        tables = [
            'PrescriptionDetail', 'MedicalRecord', 
            'Hospitalization', 'Patient',
            'Doctor', 'Ward', 'Department',
            'Medicine'
        ]
        
        for table in tables:
            try:
                cursor.execute(f"TRUNCATE TABLE {table}")
                print(f"已清空表: {table}")
            except Exception as e:
                print(f"清空{table}失败:", e)
                conn.rollback()
                return f"重置失败: 无法清空{table}", 500        
        
        
        # 2. 重新插入基础测试数据
        # 2.1 插入科室
        departments = [
            ('D001', '内科', '门诊楼3层', '010-12345671', 'DOC001'),
            ('D002', '外科', '门诊楼2层', '010-12345672', 'DOC005'),
            ('D003', '儿科', '门诊楼1层', '010-12345673', 'DOC008'),
            ('D004', '妇产科', '住院部5层', '010-12345674', 'DOC010'),
            ('D005', '急诊科', '急诊楼1层', '010-12345675', 'DOC003')
        ]
        cursor.executemany(
            "INSERT INTO Department VALUES (%s, %s, %s, %s, %s)",
            departments
        )
        
        # 2.2 插入医生
        doctors = [
            ('DOC001', '张医生', 'M', '主任医师', '心血管疾病', '15011112222', 'D001'),
            ('DOC002', '李医生', 'F', '副主任医师', '呼吸内科', '15011113333', 'D001'),
            ('DOC003', '王医生', 'M', '主治医师', '急诊医学', '15011114444', 'D005'),
            ('DOC004', '赵医生', 'F', '住院医师', '消化内科', '15011115555', 'D001'),
            ('DOC005', '刘医生', 'M', '主任医师', '普通外科', '15011116666', 'D002'),
            ('DOC006', '陈医生', 'F', '副主任医师', '神经外科', '15011117777', 'D002'),
            ('DOC007', '杨医生', 'M', '主治医师', '骨科', '15011118888', 'D002'),
            ('DOC008', '周医生', 'F', '主任医师', '儿科', '15011119999', 'D003'),
            ('DOC009', '吴医生', 'M', '住院医师', '新生儿科', '15011110000', 'D003'),
            ('DOC010', '黄医生', 'F', '主任医师', '妇产科', '15011111234', 'D004')
        ]
        cursor.executemany(
            "INSERT INTO Doctor VALUES (%s, %s, %s, %s, %s, %s, %s)",
            doctors
        )
        
        # 更新科室主任
        cursor.execute("UPDATE Department SET director_id='DOC001' WHERE dept_id='D001'")
        cursor.execute("UPDATE Department SET director_id='DOC005' WHERE dept_id='D002'")
        cursor.execute("UPDATE Department SET director_id='DOC008' WHERE dept_id='D003'")
        cursor.execute("UPDATE Department SET director_id='DOC010' WHERE dept_id='D004'")
        cursor.execute("UPDATE Department SET director_id='DOC003' WHERE dept_id='D005'")
        
        # 2.3 插入患者
        patients = [
            ('P001', '张三', 'M', '1980-05-15', '13800138001', '北京市海淀区', 'INS123456789'),
            ('P002', '李四', 'F', '1992-08-22', '13900139002', '上海市浦东新区', 'INS987654321'),
            ('P003', '王五', 'M', '1975-11-30', '13600136003', '广州市天河区', 'INS456789123'),
            ('P004', '赵六', 'F', '1988-03-10', '13500135004', '深圳市南山区', 'INS789123456'),
            ('P005', '钱七', 'M', '1995-07-18', '13700137005', '成都市武侯区', 'INS321654987')
        ]
        cursor.executemany(
            "INSERT INTO Patient VALUES (%s, %s, %s, %s, %s, %s, %s)",
            patients
        )
        
        # 2.4 插入药品
        medicines = [
            ('M001', '阿司匹林', '100mg*30片', 15.80, '华北制药', 120),
            ('M002', '头孢克肟', '50mg*12粒', 28.50, '上海制药', 85),
            ('M003', '布洛芬', '200mg*20片', 12.90, '广州药业', 45),
            ('M004', '胰岛素', '300单位/支', 65.00, '诺和诺德', 30),
            ('M005', '奥美拉唑', '20mg*14粒', 32.80, '阿斯利康', 60),
            ('M006', '氨氯地平', '5mg*28片', 18.50, '辉瑞制药', 8), 
            ('M007', '阿莫西林', '250mg*10粒', 9.80, '华北制药', 25),
            ('M008', '蒙脱石散', '3g*10袋', 22.00, '博福-益普生', 40),
            ('M009', '维生素C', '100mg*60片', 8.50, '养生堂', 200),
            ('M010', '葡萄糖注射液', '5% 250ml', 3.50, '科伦药业', 150)
        ]
        cursor.executemany(
            "INSERT INTO Medicine VALUES (%s, %s, %s, %s, %s, %s)",
            medicines
        )
        
        # 2.5 插入病房数据（确保住院记录有对应的病房）
        wards = [
            ('W001', '101', 20, '内科一病区', 'D001'),
            ('W002', '201', 10, '内科二病区', 'D001'),
            ('W003', '301', 15, '外科一病区', 'D002'),
            ('W004', '401', 10, '外科二病区', 'D002'),
            ('W005', '501', 5, '妇产科病区', 'D004')  # 修正为妇产科
        ]
        cursor.executemany(
            "INSERT INTO Ward (ward_id, ward_number, bed_count, type, dept_id) VALUES (%s, %s, %s, %s, %s)",
            wards
        )
        
        # 2.6 插入住院记录（确保数据完整）
        hospitalizations = [
            ('H001', 'P001', '2025-01-11', None, 'W001', 'DOC001', '高血压危象'),
            ('H002', 'P003', '2025-01-16', '2025-01-25', 'W003', 'DOC007', '骨折术后'),
            ('H003', 'P004', '2025-01-20', None, 'W005', 'DOC010', '待产'),
            ('H004', 'P002', '2025-02-06', '2025-02-10', 'W001', 'DOC002', '重症肺炎'),
            ('H005', 'P005', '2025-02-21', None, 'W002', 'DOC001', '糖尿病酮症')
        ]
        cursor.executemany(
            """INSERT INTO Hospitalization 
            (hospitalization_id, patient_id, admission_date, discharge_date, ward_id, attending_doctor_id, diagnosis) 
            VALUES (%s, %s, %s, %s, %s, %s, %s)""",
            hospitalizations
        )
        
        # 2.7 插入就诊记录
        medical_records = [
            ('MR001', '2025-01-10', '头痛发热', '上呼吸道感染', 'P001', 'DOC001'),
            ('MR002', '2025-01-12', '腹痛腹泻', '急性肠胃炎', 'P002', 'DOC004'),
            ('MR003', '2025-01-15', '骨折', '右臂桡骨骨折', 'P003', 'DOC007'),
            ('MR004', '2025-01-18', '妊娠检查', '孕12周', 'P004', 'DOC010'),
            ('MR005', '2025-01-20', '高烧39℃', '扁桃体炎', 'P005', 'DOC008'),
            ('MR006', '2025-02-01', '胸闷气短', '高血压', 'P001', 'DOC001'),
            ('MR007', '2025-02-05', '皮肤擦伤', '表皮擦伤', 'P002', 'DOC003'),
            ('MR008', '2025-02-10', '糖尿病复查', 'II型糖尿病', 'P003', 'DOC002'),
            ('MR009', '2025-02-15', '产后复查', '产后恢复良好', 'P004', 'DOC010'),
            ('MR010', '2025-02-20', '疫苗接种', '乙肝疫苗', 'P005', 'DOC008')
        ]
        cursor.executemany(
            "INSERT INTO MedicalRecord VALUES (%s, %s, %s, %s, %s, %s)",
            medical_records
        )
        
        # 2.8 插入处方明细
        prescriptions = [
            ('MR001', 'M001', 1, '1片', '每日3次'),
            ('MR001', 'M003', 2, '1片', '每日2次'),
            ('MR002', 'M005', 1, '1粒', '每日1次'),
            ('MR003', 'M002', 2, '1粒', '每日2次'),
            ('MR003', 'M003', 1, '1片', '每日3次'),
            ('MR004', 'M004', 1, '10单位', '每日注射'),
            ('MR005', 'M001', 1, '1片', '每日3次'),
            ('MR006', 'M006', 1, '1片', '每日1次'),
            ('MR007', 'M008', 1, '1袋', '每日3次'),
            ('MR008', 'M004', 1, '15单位', '每日注射'),
            ('MR009', 'M009', 2, '1片', '每日1次'),
            ('MR010', 'M010', 1, '250ml', '静脉滴注')
        ]
        cursor.executemany(
            "INSERT INTO PrescriptionDetail VALUES (%s, %s, %s, %s, %s)",
            prescriptions
        )
        
# 重新启用外键检查
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
        # 提交事务
        conn.commit()
        
        # 验证住院记录是否成功插入
        cursor.execute("SELECT COUNT(*) AS count FROM Hospitalization")
        hosp_count = cursor.fetchone()['count']
        
        return f'''
            <script>
                alert("测试数据重置成功！共插入{hosp_count}条住院记录");
                window.location.href = "/hospitalizations";
            </script>
        '''
    
    except Exception as e:
        conn.rollback()
        return f'''
            <script>
                alert("重置失败: {str(e)}");
                window.location.href = "/";
            </script>
        '''
    
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == '__main__':
    app.run(debug=True)

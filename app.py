from flask import Flask, render_template, request, redirect, send_file
import sqlite3
from fpdf import FPDF
import os

app = Flask(__name__)

def connect_db():
    return sqlite3.connect('student_data.db')

def create_directories():
    os.makedirs('id_cards', exist_ok=True)
    os.makedirs('receipts', exist_ok=True)

create_directories()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_student', methods=['POST'])
def add_student():
    class_num = request.form['class_num']
    name = request.form['name']
    email = request.form['email']
    phone = request.form['phone']
    course = request.form['course']
    fee_paid = request.form['fee_paid']
    fee_due = request.form['fee_due']

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(f'''INSERT INTO class_{class_num} (name, email, phone, course, fee_paid, fee_due) 
                      VALUES (?, ?, ?, ?, ?, ?)''', (name, email, phone, course, fee_paid, fee_due))
    conn.commit()
    conn.close()

    return redirect(f'/students/{class_num}')

@app.route('/students', methods=['GET'])
def students_redirect():
    class_num = request.args.get('class_num')
    if class_num:
        return redirect(f'/students/{class_num}')
    return redirect('/')

@app.route('/students/<int:class_num>')
def students(class_num):
    search_query = request.args.get('q')
    conn = connect_db()
    cursor = conn.cursor()

    if search_query:
        cursor.execute(
            f'''SELECT * FROM class_{class_num} WHERE name LIKE ? OR email LIKE ? OR course LIKE ?''',
            ('%' + search_query + '%', '%' + search_query + '%', '%' + search_query + '%')
        )
    else:
        cursor.execute(f"SELECT * FROM class_{class_num}")

    students_data = cursor.fetchall()
    conn.close()

    return render_template('students.html', students=students_data, class_num=class_num, search_query=search_query)

@app.route('/generate_id/<int:class_num>/<int:student_id>')
def generate_id(class_num, student_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(f'SELECT * FROM class_{class_num} WHERE id = ?', (student_id,))
    student = cursor.fetchone()
    conn.close()

    id_card_filename = f"id_cards/class_{class_num}_id_card_{student[0]}.pdf"
    
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"ID Card for {student[1]}", ln=True, align="L")
    pdf.cell(200, 10, txt=f"Email: {student[2]}", ln=True, align="L")
    pdf.cell(200, 10, txt=f"Phone: {student[3]}", ln=True, align="L")
    pdf.cell(200, 10, txt=f"Course: {student[4]}", ln=True, align="L")
    
    os.makedirs(os.path.dirname(id_card_filename), exist_ok=True)
    pdf.output(id_card_filename)

    return send_file(id_card_filename, as_attachment=True)

@app.route('/generate_receipt/<int:class_num>/<int:student_id>')
def generate_receipt(class_num, student_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(f'SELECT * FROM class_{class_num} WHERE id = ?', (student_id,))
    student = cursor.fetchone()
    conn.close()

    receipt_filename = f"receipts/class_{class_num}_fee_receipt_{student[0]}.pdf"
    
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"Fee Receipt for {student[1]}", ln=True, align="L")
    pdf.cell(200, 10, txt=f"Fee Paid: {student[5]}", ln=True, align="L")
    pdf.cell(200, 10, txt=f"Fee Due: {student[6]}", ln=True, align="L")
    
    os.makedirs(os.path.dirname(receipt_filename), exist_ok=True)
    pdf.output(receipt_filename)

    return send_file(receipt_filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)

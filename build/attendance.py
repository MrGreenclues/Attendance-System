from pathlib import Path
from tkinter import Tk, Canvas, Entry, Button, PhotoImage, ttk, messagebox
import mysql.connector
import subprocess

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\xampp\htdocs\attendance\build\assets\frame3")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

# Establish connection
connection = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    database='attendance'
)

def open_dashboard():
    window.destroy()
    script_dir = Path(__file__).resolve().parent
    addpet_path = script_dir / "dashboard.py"
    subprocess.run(["python", str(addpet_path)])
# Create cursor
cursor = connection.cursor()

# Function to fetch and populate data
def populate_student_tree():
    # Execute a query to fetch the data
    cursor.execute("SELECT * FROM students")

    # Clear previous data in the tree
    for record in student_tree.get_children():
        student_tree.delete(record)

    # Insert fetched data into the tree
    for row in cursor.fetchall():
        student_tree.insert("", "end", values=row)

def clear_entries():
    for entry in (entry_1, entry_2, entry_3, entry_4, entry_5):
        entry.delete(0, 'end')

def populate_entry_fields(event):
    selected_item = student_tree.selection()
    if selected_item:
        student = student_tree.item(selected_item, 'values')
        for i, entry in enumerate((entry_1, entry_2, entry_3, entry_4, entry_5)):
            entry.delete(0, 'end')
            entry.insert(0, student[i])

def mark_present():
    # Get the selected student's ID from the Treeview
    selected_item = student_tree.selection()
    if selected_item:
        student_id = student_tree.item(selected_item, "values")[0]  # Assuming the student_id is the first column
        # Fetch student details
        cursor.execute("SELECT * FROM students WHERE student_id = %s", (student_id,))
        student_details = cursor.fetchone()
        if student_details:
            # Insert into the mark_present table
            messagebox.showinfo("Success", f"{student_details[1]} marked as present")
            cursor.execute("INSERT INTO mark_present (student_id, name, age, gender, course, status) VALUES (%s, %s, %s, %s, %s, %s)",
                           student_details)
            # Delete the student from the students table
            cursor.execute("DELETE FROM students WHERE student_id = %s", (student_id,))
            connection.commit()  # Commit the transaction
            # Refresh the student tree
            populate_student_tree()
            clear_entries()
            populate_present_tree()
            populate_absent_tree()


def mark_absent():
    # Get the selected student's ID from the Treeview
    selected_item = student_tree.selection()
    if selected_item:
        student_id = student_tree.item(selected_item, "values")[0]  # Assuming the student_id is the first column
        # Fetch student details
        cursor.execute("SELECT * FROM students WHERE student_id = %s", (student_id,))
        student_details = cursor.fetchone()
        if student_details:
            # Insert into the mark_absent table
            messagebox.showinfo("Success", f"{student_details[1]} marked as absent")  # Assuming name is the second column
            cursor.execute("INSERT INTO mark_absent (student_id, name, age, gender, course, status) VALUES (%s, %s, %s, %s, %s, %s)",
                           student_details)
            connection.commit()  # Commit the transaction
            # Delete the student from the students table
            cursor.execute("DELETE FROM students WHERE student_id = %s", (student_id,))
            connection.commit()  # Commit the transaction
            # Refresh the student tree
            populate_student_tree()
            populate_present_tree()
            clear_entries()
            populate_absent_tree()



def populate_present_tree():
    # Clear previous data in the tree
    for record in present_tree.get_children():
        present_tree.delete(record)

    # Fetch data from mark_present table
    cursor.execute("SELECT name, course, status FROM mark_present")
    # Insert fetched data into the tree
    for row in cursor.fetchall():
        present_tree.insert("", "end", values=row)

def populate_absent_tree():
    # Clear previous data in the tree
    for record in absent_tree.get_children():
        absent_tree.delete(record)

    # Fetch data from mark_absent table
    cursor.execute("SELECT name, course, status FROM mark_absent")
    # Insert fetched data into the tree
    for row in cursor.fetchall():
        absent_tree.insert("", "end", values=row)



window = Tk()
window.geometry("1235x933")
window.configure(bg="#6E6A7C")

canvas = Canvas(
    window,
    bg="#6E6A7C",
    height=933,
    width=1235,
    bd=0,
    highlightthickness=0,
    relief="ridge"
)
canvas.place(x=0, y=0)
canvas.create_rectangle(
    5.0,
    0.0,
    1240.0,
    125.0,
    fill="#007527",
    outline=""
)
canvas.create_text(
    798.0,
    33.0,
    anchor="nw",
    text="Attendance",
    fill="#FFFFFF",
    font=("Inter ExtraBold", 36 * -1)
)

button_image_1 = PhotoImage(file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=open_dashboard,
    relief="flat"
)
button_1.place(x=18.0, y=27.0, width=122.0, height=76.0)

entry_image_1 = PhotoImage(file=relative_to_assets("entry_1.png"))
entry_bg_1 = canvas.create_image(233.0, 253.0, image=entry_image_1)
entry_1 = Entry(bd=0, bg="#FDF2F2", fg="#000716", highlightthickness=0)
entry_1.place(x=86.0, y=223.0, width=294.0, height=58.0)

entry_image_2 = PhotoImage(file=relative_to_assets("entry_2.png"))
entry_bg_2 = canvas.create_image(236.0, 354.0, image=entry_image_2)
entry_2 = Entry(bd=0, bg="#FDF2F2", fg="#000716", highlightthickness=0)
entry_2.place(x=89.0, y=324.0, width=294.0, height=58.0)

entry_image_3 = PhotoImage(file=relative_to_assets("entry_3.png"))
entry_bg_3 = canvas.create_image(236.0, 455.0, image=entry_image_3)
entry_3 = Entry(bd=0, bg="#FDF2F2", fg="#000716", highlightthickness=0)
entry_3.place(x=89.0, y=425.0, width=294.0, height=58.0)

entry_image_4 = PhotoImage(file=relative_to_assets("entry_4.png"))
entry_bg_4 = canvas.create_image(236.0, 566.0, image=entry_image_4)
entry_4 = Entry(bd=0, bg="#FDF2F2", fg="#000716", highlightthickness=0)
entry_4.place(x=89.0, y=536.0, width=294.0, height=58.0)

entry_image_5 = PhotoImage(file=relative_to_assets("entry_5.png"))
entry_bg_5 = canvas.create_image(236.0, 667.0, image=entry_image_5)
entry_5 = Entry(bd=0, bg="#FDF2F2", fg="#000716", highlightthickness=0)
entry_5.place(x=89.0, y=637.0, width=294.0, height=58.0)

image_image_1 = PhotoImage(file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(140.0, 202.0, image=image_image_1)

image_image_2 = PhotoImage(file=relative_to_assets("image_2.png"))
image_2 = canvas.create_image(158.0, 303.0, image=image_image_2)

image_image_3 = PhotoImage(file=relative_to_assets("image_3.png"))
image_3 = canvas.create_image(522.0, 491.0, image=image_image_3)

image_image_4 = PhotoImage(file=relative_to_assets("image_4.png"))
image_4 = canvas.create_image(158.0, 410.0, image=image_image_4)

image_image_5 = PhotoImage(file=relative_to_assets("image_5.png"))
image_5 = canvas.create_image(163.0, 521.0, image=image_image_5)

image_image_6 = PhotoImage(file=relative_to_assets("image_6.png"))
image_6 = canvas.create_image(163.0, 622.0, image=image_image_6)

canvas.create_rectangle(
    438.0,
    182.0,
    1158.0,
    425.0,
    fill="#D9D9D9",
    outline=""
)
canvas.create_rectangle(
    807.0,
    506.0,
    1158.0,
    783.0,
    fill="#D9D9D9",
    outline=""
)
canvas.create_rectangle(
    438.0,
    507.5,
    789.0,
    784.5,
    fill="#D9D9D9",
    outline=""
)

# Create Treeview for displaying student information
student_tree = ttk.Treeview(window, columns=("student_id", "name", "age", "gender", "course","status"), show='headings')
student_tree.heading("student_id", text="ID Number")
student_tree.heading("name", text="Name")
student_tree.heading("age", text="Age")
student_tree.heading("gender", text="Gender")
student_tree.heading("course", text="Course")
student_tree.heading("status", text="Status")
student_tree.column("student_id", width=70, anchor="center")
student_tree.column("name", width=100, anchor="center")
student_tree.column("age", width=50, anchor="center")
student_tree.column("gender", width=100, anchor="center")
student_tree.column("course", width=100, anchor="center")
student_tree.column("status", width=100, anchor="center")
student_tree.place(x=448, y=192, width=700, height=220)
student_tree.bind("<ButtonRelease-1>", populate_entry_fields)
populate_student_tree()

# Create Treeview for displaying absent students
present_tree = ttk.Treeview(window, columns=("name","course","status"), show='headings')
present_tree.heading("name", text="Name")
present_tree.heading("course", text="Course")
present_tree.heading("status", text="Status")

present_tree.place(x=448, y=517.5, width=340, height=260)





# Create Treeview for displaying present students
absent_tree = ttk.Treeview(window, columns=("name", "course","status"), show='headings')
absent_tree.heading("name", text="Name")
absent_tree.heading("course", text="Course")
absent_tree.heading("status", text="Status")
absent_tree.place(x=817, y=516, width=340, height=260)


populate_present_tree()
populate_absent_tree()
# Call the function after defining it


##present button
button_image_2 = PhotoImage(file=relative_to_assets("button_2.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=mark_present,
    relief="flat"
)
button_2.place(x=117.0, y=738.0, width=238.99935913085938, height=48.0)

#absent button
button_image_3 = PhotoImage(file=relative_to_assets("button_3.png"))
button_3 = Button(
    image=button_image_3,
    borderwidth=0,
    highlightthickness=0,
    command=mark_absent,
    relief="flat"
)
button_3.place(x=117.0, y=807.0, width=238.99935913085938, height=48.0)

window.resizable(False, False)

# Initialize display of students, present, and absent tables

window.mainloop()

from pathlib import Path
import mysql.connector  # Import MySQL connector
from tkinter import Tk, Canvas, Button, PhotoImage
import subprocess

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\xampp\htdocs\attendance\build\assets\frame0")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

# Function to get the number of students from the database
def get_student_count():
    try:
        # Connect to the MySQL database
        connection = mysql.connector.connect(
            host='localhost',        # Replace with your MySQL server host
            user='root',             # Replace with your MySQL username
            password='',             # Replace with your MySQL password
            database='attendance' # Replace with your database name
        )

        cursor = connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM mark_present")
        result = cursor.fetchone()
        return result[0] if result else 0

    except mysql.connector.Error as error:
        print(f"Error: {error}")
        return 0

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def get_absent_student_count():
    try:
        # Connect to the MySQL database
        connection = mysql.connector.connect(
            host='localhost',        # Replace with your MySQL server host
            user='root',             # Replace with your MySQL username
            password='',             # Replace with your MySQL password
            database='attendance' # Replace with your database name
        )

        cursor = connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM mark_absent")
        result = cursor.fetchone()
        return result[0] if result else 0

    except mysql.connector.Error as error:
        print(f"Error: {error}")
        return 0

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()




def open_manage():
    window.destroy()
    script_dir = Path(__file__).resolve().parent
    addpet_path = script_dir / "manage.py"
    subprocess.run(["python", str(addpet_path)])

def open_attendance():
    window.destroy()
    script_dir = Path(__file__).resolve().parent
    addpet_path = script_dir / "attendance.py"
    subprocess.run(["python", str(addpet_path)])

window = Tk()
window.geometry("1235x933")
window.configure(bg = "#6E6A7C")

canvas = Canvas(
    window,
    bg = "#6E6A7C",
    height = 933,
    width = 1235,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
canvas.create_rectangle(
    61.0,
    166.0,
    614.0,
    813.0,
    fill="#000000",
    outline="")
# ------------------------------------------------------------------------
canvas.create_rectangle(
    766.0,
    173.0,
    1174.0,
    467.0,
    fill="#D9D9D9",
    outline="")

canvas.create_rectangle(
    321.0,
    173.0,
    729.0,
    467.0,
    fill="#D9D9D9",
    outline="")

canvas.create_rectangle(
    88.0,
    0.0,
    1323.0,
    125.0,
    fill="#000000",
    outline="")

canvas.create_rectangle(
    0.0,
    0.0,
    1235.0,
    125.0,
    fill="#007527",
    outline="")

canvas.create_text(
    927.0,
    33.0,
    anchor="nw",
    text="Dashboard",
    fill="#FFFFFF",
    font=("Inter ExtraBold", 36 * -1)
)

image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    449.0,
    209.0,
    image=image_image_1
)

image_image_2 = PhotoImage(
    file=relative_to_assets("image_2.png"))
image_2 = canvas.create_image(
    894.0,
    209.0,
    image=image_image_2
)

canvas.create_rectangle(
    0.0,
    0.0,
    285.0,
    933.0,
    fill="#007528",
    outline="")

button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=open_manage,
    relief="flat"
)
button_1.place(
    x=23.0,
    y=130.0,
    width=238.99923706054688,
    height=72.00001525878906
)

button_image_2 = PhotoImage(
    file=relative_to_assets("button_2.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=open_attendance,
    relief="flat"
)
button_2.place(
    x=22.0,
    y=233.0,
    width=238.99923706054688,
    height=72.00001525878906
)

# Get the student count and display it on the canvas=---------------------------------------------------
student_count = get_student_count()
canvas.create_text(
    650.0,
    200.0,
    anchor="nw",
    text=f" {student_count}",
    fill="black",
    font=("Inter ExtraBold", 60 * -1)
)

absent_students = get_absent_student_count()
canvas.create_text(
    1100.0,
    200.0,
    anchor="nw",
     text=f"{absent_students}",
    fill="black",
    font=("Inter ExtraBold", 60 * -1)
)


window.resizable(False, False)
window.mainloop()

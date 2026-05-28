import tkinter as tk 
from tkinter import ttk
import pandas as pd
import csv
import os


if not os.path.exists("student.csv"):
    df = pd.DataFrame(columns=["Roll", "Name", "Course", "Marks"])
    df.to_csv("student.csv", index=False)

root = tk.Tk()

tk.Label(root, text = "Student Name: ").grid(row = 0, column = 0)
name_entry = tk.Entry(root)
name_entry.grid(row = 0, column = 1)
tk.Label(root, text = "Roll number: ").grid(row = 1, column = 0)
roll_entry= tk.Entry(root)
roll_entry.grid(row = 1, column = 1)
tk.Label(root, text = "Course: ").grid(row = 2, column = 0)
course_entry = tk.Entry(root)
course_entry.grid(row = 2, column = 1)
tk.Label(root, text = "Marks: ",).grid(row = 3, column = 0)
marks_entry = tk.Entry(root)
marks_entry.grid(row = 3, column = 1)

tree = ttk.Treeview(root, columns = ["Roll number", "Name", "Course", "Marks"], show = "headings")
tree.heading("Roll number", text="Roll number")
tree.heading("Name", text="Name")
tree.heading("Course", text="Course")
tree.heading("Marks", text="Marks")
tree.grid(row=10, column=4, columnspan=8, pady=40)

def load_data():

    # Clear old data
    for row in tree.get_children():
        tree.delete(row)

    df = pd.read_csv("student.csv")

    for index, row in df.iterrows():
        tree.insert("", tk.END, values=list(row))
 

def std():

    roll = roll_entry.get()
    name = name_entry.get()
    course = course_entry.get()
    marks = marks_entry.get()
    
    new_student = {
        "Roll": roll,
        "Name": name,
        "Course": course,
        "Marks": marks
    }

    df = pd.read_csv("student.csv")

    df.loc[len(df)] = new_student
    df.to_csv("student.csv", index = False)

    load_data()

    roll_entry.delete(0, tk.END)
    name_entry.delete(0, tk.END)
    marks_entry.delete(0, tk.END)
    course_entry.delete(0, tk.END)

def select_record(event):

    selected = tree.selection()

    if selected:

        item = selected[0]

        values = tree.item(item, "values")

        # Clear old data
        roll_entry.delete(0, tk.END)
        name_entry.delete(0, tk.END)
        course_entry.delete(0, tk.END)
        marks_entry.delete(0, tk.END)

        # Insert selected row data
        roll_entry.insert(0, values[0])
        name_entry.insert(0, values[1])
        course_entry.insert(0, values[2])
        marks_entry.insert(0, values[3])

tree.bind("<<TreeviewSelect>>", select_record)    

def up():
    select = tree.selection()
    if select:
        item = select[0]
        new_data = ( roll_entry.get(),
                    name_entry.get(),
                    course_entry.get(),
                    marks_entry.get()) 
        tree.item(item, values = new_data)
        all_data = []

        for row in tree.get_children():

            data = tree.item(row, "values")

            all_data.append(data)

        df = pd.DataFrame(
            all_data,
            columns=["Roll number", "Name", "Course", "Marks"]
        )

        df.to_csv("student.csv", index=False)


menu = tk.Menu(root)
m1 = tk.Menu(menu, tearoff = 0)
menu.add_cascade(label = "File", menu = m1)
m1.add_command(label = "Add", command = std)
m1.add_command(label = "exit", command = root.destroy)
m1.add_command(label = "Update", command = up)
root.config(menu=menu)

load_data()


root.mainloop()
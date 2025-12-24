import tkinter as tk
from tkinter import messagebox
import mysql.connector

# -------------------- MySQL CONFIG --------------------
DB_HOST = "localhost"
DB_USER = "root"
DB_PASS = "nice"
DB_NAME = "ojas"
TABLE_NAME = "studdd"

class MySQLTodoApp:
    def __init__(self, root):
        self.root = root
        root.title("MySQL Notes / To-Do App")
        root.geometry("550x520")
        root.resizable(True, True)

        self.db_connect()
        self.ensure_table()

        # ------------------- UI -------------------
        top = tk.Frame(root, pady=10)
        top.pack(fill=tk.X)
        form = tk.Frame(top)
        form.pack()

        self.task_var = tk.StringVar()
        self.city_var = tk.StringVar()
        self.country_var = tk.StringVar()
        
        tk.Label(top, text="Name").pack(side=tk.LEFT)
        tk.Entry(top, textvariable=self.task_var, width=20).pack(side=tk.LEFT, padx=5)

        tk.Label(top, text="City").pack(side=tk.LEFT)
        tk.Entry(top, textvariable=self.city_var, width=15).pack(side=tk.LEFT, padx=5)

        tk.Label(top, text="Country").pack(side=tk.LEFT)
        tk.Entry(top, textvariable=self.country_var, width=15).pack(side=tk.LEFT, padx=5)

        tk.Button(top, text="Add", command=self.add_task).pack(side=tk.LEFT, padx=5)

        mid = tk.Frame(root)
        mid.pack(fill=tk.BOTH, expand=True, padx=10)

        self.listbox = tk.Listbox(mid, font=(None, 11))
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(mid, command=self.listbox.yview)
        scrollbar.pack(side=tk.LEFT, fill=tk.Y)
        self.listbox.config(yscrollcommand=scrollbar.set)

        bottom = tk.Frame(root, pady=10)
        bottom.pack()

        tk.Button(bottom, text="Delete Selected", command=self.delete_task).pack(side=tk.LEFT, padx=5)
        tk.Button(bottom, text="Refresh", command=self.load_tasks).pack(side=tk.LEFT)

        self.status = tk.Label(root, text="0 records")
        self.status.pack(pady=5)

        self.load_tasks()

    # ------------------- DB -------------------
    def db_connect(self):
        self.conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASS
        )
        self.cursor = self.conn.cursor()
        self.cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
        self.conn.database = DB_NAME

    def ensure_table(self):
        query = f"""
        CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
            id INT AUTO_INCREMENT PRIMARY KEY,
            task TEXT NOT NULL,
            city TEXT NOT NULL,
            country TEXT NOT NULL
        )
        """
        self.cursor.execute(query)
        self.conn.commit()

    # ------------------- FUNCTIONS -------------------
    def add_task(self):
        task = self.task_var.get().strip()
        city = self.city_var.get().strip()
        country = self.country_var.get().strip()

        if not task or not city or not country:
            messagebox.showwarning("Empty", "Fill all fields")
            return

        query = f"INSERT INTO {TABLE_NAME} (task, city, country) VALUES (%s, %s, %s)"
        self.cursor.execute(query, (task, city, country))
        self.conn.commit()

        self.task_var.set("")
        self.city_var.set("")
        self.country_var.set("")
        self.load_tasks()

    def load_tasks(self):
        self.listbox.delete(0, tk.END)
        self.cursor.execute(f"SELECT id, task, city, country FROM {TABLE_NAME}")
        self.tasks = self.cursor.fetchall()

        for row in self.tasks:
            self.listbox.insert(tk.END, f"{row[1]} | {row[2]} | {row[3]}")

        self.status.config(text=f"{len(self.tasks)} records")

    def delete_task(self):
        if not self.listbox.curselection():
            return

        idx = self.listbox.curselection()[0]
        task_id = self.tasks[idx][0]

        self.cursor.execute(f"DELETE FROM {TABLE_NAME} WHERE id=%s", (task_id,))
        self.conn.commit()
        self.load_tasks()

# ------------------- RUN -------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = MySQLTodoApp(root)
    root.mainloop()

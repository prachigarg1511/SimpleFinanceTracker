"""
login.py
---------
Login & Signup Window
"""

import tkinter as tk
from tkinter import ttk, messagebox

from helpers import (
    get_theme,
    TITLE_FONT,
    HEADER_FONT,
    NORMAL_FONT,
    USERS_FILE,
    read_json,
    write_json
)


class LoginWindow:

    def __init__(self):

        self.theme = get_theme()

        self.root = tk.Tk()
        self.root.title("Simple Finance Tracker")
        self.root.geometry("500x600")
        self.root.resizable(False, False)
        self.root.configure(bg=self.theme["bg"])

        self.center_window()

        self.show_password = False

        self.create_widgets()

        self.root.mainloop()

    # ----------------------------

    def center_window(self):

        width = 500
        height = 600

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)

        self.root.geometry(f"{width}x{height}+{x}+{y}")

    # ----------------------------

    def create_widgets(self):

        card = tk.Frame(
            self.root,
            bg=self.theme["card"],
            padx=30,
            pady=30
        )

        card.place(relx=.5, rely=.5, anchor="center")

        title = tk.Label(
            card,
            text="💰 Finance Tracker",
            font=TITLE_FONT,
            bg=self.theme["card"],
            fg=self.theme["primary"]
        )

        title.pack(pady=(0, 25))

        login_label = tk.Label(
            card,
            text="Login",
            font=HEADER_FONT,
            bg=self.theme["card"]
        )

        login_label.pack(pady=10)

        # Username

        tk.Label(
            card,
            text="Username",
            bg=self.theme["card"],
            font=NORMAL_FONT
        ).pack(anchor="w")

        self.username = ttk.Entry(
            card,
            width=35
        )

        self.username.pack(pady=8)

        # Password

        tk.Label(
            card,
            text="Password",
            bg=self.theme["card"],
            font=NORMAL_FONT
        ).pack(anchor="w")

        self.password = ttk.Entry(
            card,
            width=35,
            show="*"
        )

        self.password.pack(pady=8)

        self.show_btn = ttk.Button(
            card,
            text="Show Password",
            command=self.toggle_password
        )

        self.show_btn.pack()

        ttk.Button(
            card,
            text="Login",
            command=self.login,
            width=25
        ).pack(pady=20)

        ttk.Separator(card).pack(fill="x", pady=15)

        tk.Label(
            card,
            text="Create New Account",
            bg=self.theme["card"],
            font=("Segoe UI", 11, "bold")
        ).pack()

        self.new_user = ttk.Entry(card, width=35)
        self.new_user.pack(pady=5)

        self.new_pass = ttk.Entry(card, width=35, show="*")
        self.new_pass.pack(pady=5)

        ttk.Button(
            card,
            text="Create Account",
            command=self.signup
        ).pack(pady=10)

    # ----------------------------

    def toggle_password(self):

        if self.show_password:

            self.password.config(show="*")
            self.show_btn.config(text="Show Password")

        else:

            self.password.config(show="")
            self.show_btn.config(text="Hide Password")

        self.show_password = not self.show_password

    # ----------------------------

    def login(self):

        username = self.username.get().strip()
        password = self.password.get().strip()

        users = read_json(USERS_FILE)

        if username in users and users[username] == password:

            messagebox.showinfo(
                "Success",
                f"Welcome {username}!"
            )

            self.root.destroy()

            from dashboard import Dashboard

            Dashboard(username)

        else:

            messagebox.showerror(
                "Error",
                "Invalid Username or Password"
            )

    # ----------------------------

    def signup(self):

        username = self.new_user.get().strip()
        password = self.new_pass.get().strip()

        if username == "" or password == "":

            messagebox.showwarning(
                "Warning",
                "Fill all fields."
            )

            return

        users = read_json(USERS_FILE)

        if username in users:

            messagebox.showerror(
                "Error",
                "Username already exists."
            )

            return

        users[username] = password

        write_json(
            USERS_FILE,
            users
        )

        messagebox.showinfo(
            "Success",
            "Account Created Successfully!"
        )

        self.new_user.delete(0, tk.END)
        self.new_pass.delete(0, tk.END)
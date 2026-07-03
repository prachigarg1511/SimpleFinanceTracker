"""
settings.py
-----------
Settings Window
- Toggle Light / Dark theme
- Change password
- View app info
"""

import tkinter as tk
from tkinter import ttk, messagebox

from helpers import (
    get_theme,
    TITLE_FONT,
    HEADER_FONT,
    NORMAL_FONT,
    SMALL_FONT,
    SETTINGS_FILE,
    USERS_FILE,
    read_json,
    write_json
)


class SettingsWindow:

    def __init__(self, parent, username, on_theme_change=None):

        self.theme = get_theme()
        self.username = username
        self.on_theme_change = on_theme_change

        self.window = tk.Toplevel(parent)
        self.window.title("Settings")
        self.window.geometry("520x560")
        self.window.resizable(False, False)
        self.window.configure(bg=self.theme["bg"])

        self._center_window()
        self._create_ui()

    # --------------------------------------------------

    def _center_window(self):

        w, h = 520, 560
        sw = self.window.winfo_screenwidth()
        sh = self.window.winfo_screenheight()
        x = (sw // 2) - (w // 2)
        y = (sh // 2) - (h // 2)
        self.window.geometry(f"{w}x{h}+{x}+{y}")

    # --------------------------------------------------

    def _create_ui(self):

        # ---- Header ----
        header = tk.Frame(self.window, bg=self.theme["primary"], height=60)
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(
            header,
            text="⚙  Settings",
            font=TITLE_FONT,
            bg=self.theme["primary"],
            fg="white"
        ).pack(side="left", padx=20, pady=12)

        # ---- Content ----
        content = tk.Frame(self.window, bg=self.theme["bg"])
        content.pack(fill="both", expand=True, padx=25, pady=15)

        # ===== Theme Section =====
        self._section_label(content, "🎨  Appearance")

        theme_card = tk.Frame(content, bg="white", bd=1, relief="solid")
        theme_card.pack(fill="x", pady=(0, 15))

        tk.Label(
            theme_card,
            text="Theme",
            font=NORMAL_FONT,
            bg="white"
        ).pack(anchor="w", padx=15, pady=(12, 4))

        settings = read_json(SETTINGS_FILE)
        current_theme = settings.get("theme", "light")

        self.theme_var = tk.StringVar(value=current_theme)

        row = tk.Frame(theme_card, bg="white")
        row.pack(anchor="w", padx=15, pady=(0, 12))

        ttk.Radiobutton(
            row,
            text="☀️  Light Mode",
            variable=self.theme_var,
            value="light"
        ).pack(side="left", padx=(0, 20))

        ttk.Radiobutton(
            row,
            text="🌙  Dark Mode",
            variable=self.theme_var,
            value="dark"
        ).pack(side="left")

        ttk.Button(
            theme_card,
            text="Apply Theme",
            command=self._apply_theme
        ).pack(anchor="e", padx=15, pady=(0, 12))

        # ===== Password Section =====
        self._section_label(content, "🔒  Change Password")

        pwd_card = tk.Frame(content, bg="white", bd=1, relief="solid")
        pwd_card.pack(fill="x", pady=(0, 15))

        fields = tk.Frame(pwd_card, bg="white")
        fields.pack(padx=15, pady=12, fill="x")

        # Current password
        tk.Label(
            fields, text="Current Password",
            font=NORMAL_FONT, bg="white"
        ).grid(row=0, column=0, sticky="w", pady=5)

        self.current_pwd = ttk.Entry(fields, width=25, show="*")
        self.current_pwd.grid(row=0, column=1, padx=10)

        # New password
        tk.Label(
            fields, text="New Password",
            font=NORMAL_FONT, bg="white"
        ).grid(row=1, column=0, sticky="w", pady=5)

        self.new_pwd = ttk.Entry(fields, width=25, show="*")
        self.new_pwd.grid(row=1, column=1, padx=10)

        # Confirm password
        tk.Label(
            fields, text="Confirm Password",
            font=NORMAL_FONT, bg="white"
        ).grid(row=2, column=0, sticky="w", pady=5)

        self.confirm_pwd = ttk.Entry(fields, width=25, show="*")
        self.confirm_pwd.grid(row=2, column=1, padx=10)

        ttk.Button(
            pwd_card,
            text="Change Password",
            command=self._change_password
        ).pack(anchor="e", padx=15, pady=(0, 12))

        # ===== About Section =====
        self._section_label(content, "ℹ️  About")

        about_card = tk.Frame(content, bg="white", bd=1, relief="solid")
        about_card.pack(fill="x")

        about_text = (
            "Simple Finance Tracker\n"
            "Version 1.0.0\n\n"
            "Built with Python, Tkinter, Pandas,\n"
            "NumPy & Matplotlib.\n\n"
            f"Logged in as:  {self.username}"
        )

        tk.Label(
            about_card,
            text=about_text,
            font=SMALL_FONT,
            bg="white",
            fg="#6B7280",
            justify="left"
        ).pack(anchor="w", padx=15, pady=12)

    # --------------------------------------------------

    def _section_label(self, parent, text):

        tk.Label(
            parent,
            text=text,
            font=("Segoe UI", 12, "bold"),
            bg=self.theme["bg"],
            fg=self.theme["text"]
        ).pack(anchor="w", pady=(5, 4))

    # --------------------------------------------------

    def _apply_theme(self):

        chosen = self.theme_var.get()

        write_json(SETTINGS_FILE, {"theme": chosen})

        messagebox.showinfo(
            "Theme Applied",
            f"Theme set to {'Light' if chosen == 'light' else 'Dark'} mode.\n"
            "Please restart the application to see full effect.",
            parent=self.window
        )

        if self.on_theme_change:
            self.on_theme_change()

    # --------------------------------------------------

    def _change_password(self):

        current = self.current_pwd.get()
        new = self.new_pwd.get()
        confirm = self.confirm_pwd.get()

        if not current or not new or not confirm:
            messagebox.showwarning(
                "Warning",
                "Please fill all password fields.",
                parent=self.window
            )
            return

        users = read_json(USERS_FILE)

        if users.get(self.username) != current:
            messagebox.showerror(
                "Error",
                "Current password is incorrect.",
                parent=self.window
            )
            return

        if new != confirm:
            messagebox.showerror(
                "Error",
                "New passwords do not match.",
                parent=self.window
            )
            return

        if len(new) < 4:
            messagebox.showwarning(
                "Warning",
                "Password must be at least 4 characters.",
                parent=self.window
            )
            return

        users[self.username] = new
        write_json(USERS_FILE, users)

        messagebox.showinfo(
            "Success",
            "Password changed successfully!",
            parent=self.window
        )

        self.current_pwd.delete(0, tk.END)
        self.new_pwd.delete(0, tk.END)
        self.confirm_pwd.delete(0, tk.END)

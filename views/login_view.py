# views/login_view.py

import tkinter as tk
from tkinter import ttk, messagebox
import logging
from views.register_view import RegisterWindow

logger = logging.getLogger(__name__)

class LoginWindow:
    def __init__(self, parent, model, on_success):
        """
        Khởi tạo cửa sổ đăng nhập.

        :param parent: Cửa sổ cha.
        :param model: Đối tượng model.
        :param on_success: Hàm callback khi đăng nhập thành công.
        """
        self.model = model
        self.on_success = on_success
        self.window = tk.Toplevel(parent)
        self.window.title("Đăng Nhập")
        self.window.geometry("350x400")
        self.window.resizable(False, False)
        self.window.grab_set()

        # Tiêu đề
        title_label = ttk.Label(self.window, text="Đăng Nhập", font=("Helvetica", 16, "bold"))
        title_label.pack(pady=20)

        # Tên đăng nhập
        username_label = ttk.Label(self.window, text="Tên đăng nhập:")
        username_label.pack(pady=(10, 5))
        self.username_var = tk.StringVar()
        username_entry = ttk.Entry(self.window, textvariable=self.username_var)
        username_entry.pack(pady=5)

        # Mật khẩu
        password_label = ttk.Label(self.window, text="Mật khẩu:")
        password_label.pack(pady=(10, 5))
        self.password_var = tk.StringVar()
        password_entry = ttk.Entry(self.window, textvariable=self.password_var, show="*")
        password_entry.pack(pady=5)

        # Nút Đăng Nhập
        login_button = ttk.Button(self.window, text="Đăng Nhập", command=self.login)
        login_button.pack(pady=20)

        # Nút Đăng Ký
        register_button = ttk.Button(self.window, text="Đăng Ký", command=self.show_register)
        register_button.pack(pady=5)

    def login(self):
        """
        Xử lý đăng nhập.
        """
        username = self.username_var.get().strip()
        password = self.password_var.get().strip()

        if not username or not password:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập tên đăng nhập và mật khẩu.")
            return

        success, user_id, user_name, role = self.model.login_user(username, password)
        if success:
            messagebox.showinfo("Thành công", f"Đăng nhập thành công!")
            self.window.destroy()
            self.on_success(user_id, user_name, role)
        else:
            messagebox.showerror("Lỗi", "Tên đăng nhập hoặc mật khẩu không đúng.")
    

    def show_register(self):
        """
        Mở cửa sổ đăng ký.
        """
        RegisterWindow(self.window, self.model, self.on_register_success)

    def on_register_success(self):
        """
        Xử lý sau khi đăng ký thành công.
        """
        messagebox.showinfo("Thành công", "Bạn đã đăng ký thành công. Vui lòng đăng nhập.")


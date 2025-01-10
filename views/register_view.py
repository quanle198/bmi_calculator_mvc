# views/register_view.py

import tkinter as tk
from tkinter import ttk, messagebox
import logging

logger = logging.getLogger(__name__)

class RegisterWindow:
    def __init__(self, parent, model, on_success):
        """
        Khởi tạo cửa sổ đăng ký.

        :param parent: Cửa sổ cha.
        :param model: Đối tượng model.
        :param on_success: Hàm callback khi đăng ký thành công.
        """
        self.model = model
        self.on_success = on_success
        self.window = tk.Toplevel(parent)
        self.window.title("Đăng Ký")
        self.window.geometry("350x400")
        self.window.resizable(False, False)
        self.window.grab_set()

        # Tiêu đề
        title_label = ttk.Label(self.window, text="Đăng Ký", font=("Helvetica", 16, "bold"))
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

        # Xác nhận mật khẩu
        confirm_label = ttk.Label(self.window, text="Xác nhận mật khẩu:")
        confirm_label.pack(pady=(10, 5))
        self.confirm_var = tk.StringVar()
        confirm_entry = ttk.Entry(self.window, textvariable=self.confirm_var, show="*")
        confirm_entry.pack(pady=5)

        # Nút Đăng Ký
        register_button = ttk.Button(self.window, text="Đăng Ký", command=self.register)
        register_button.pack(pady=20)

    def register(self):
        """
        Xử lý đăng ký.
        """
        username = self.username_var.get().strip()
        password = self.password_var.get().strip()
        confirm_password = self.confirm_var.get().strip()

        if not username or not password or not confirm_password:
            messagebox.showwarning("Cảnh báo", "Vui lòng điền đầy đủ thông tin.")
            return

        if password != confirm_password:
            messagebox.showerror("Lỗi", "Mật khẩu không khớp.")
            return

        if len(password) < 6:
            messagebox.showwarning("Cảnh báo", "Mật khẩu phải ít nhất 6 ký tự.")
            return

        success = self.model.register_user(username, password, "user")
        if success:
            self.window.destroy()
            self.on_success()
        else:
            messagebox.showerror("Lỗi", "Tên đăng nhập đã tồn tại. Vui lòng chọn tên khác.")

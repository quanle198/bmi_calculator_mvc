# views/faq_view.py
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

class FAQWindow:
    def __init__(self, parent, model):
        self.parent = parent
        self.window = tk.Toplevel(parent)
        self.window.title("FAQ - Câu hỏi thường gặp")
        self.window.geometry("700x700")
        self.window.configure(bg="#ffffff")
        self.window.resizable(False, False)

        # Tải biểu tượng nếu có (tùy chọn)
        try:
            faq_icon = Image.open("Assets/img/bmi-icon.png")
            faq_icon = faq_icon.resize((30, 30))
            faq_photo = ImageTk.PhotoImage(faq_icon)
            self.window.iconphoto(False, faq_photo)
            self.icon_photo = faq_photo  # Lưu giữ reference
        except Exception as e:
            print(f"Lỗi khi tải icon FAQ: {e}")

        # Tiêu đề
        title = tk.Label(self.window, text="Câu hỏi thường gặp (FAQ)", font=("Helvetica", 20, "bold"), bg="#ffffff", pady=20)
        title.pack()

        # Tạo Scrollable Frame
        canvas = tk.Canvas(self.window, borderwidth=0, background="#ffffff")
        frame = tk.Frame(canvas, background="#ffffff")
        scrollbar = ttk.Scrollbar(self.window, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)
        canvas.create_window((0, 0), window=frame, anchor="nw")

        def on_frame_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))

        frame.bind("<Configure>", on_frame_configure)

        faqs = model.load_faq()

        # Tạo các Accordion cho từng câu hỏi
        for faq in faqs:
            accordion = Accordion(frame, title=faq['question'], content=faq['answer'])
            accordion.pack(fill='x', pady=5, padx=20, anchor="n")


class Accordion(tk.Frame):
    def __init__(self, parent, title="", content="", *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        
        self.is_expanded = False
        self.configure(bg="#ffffff")
        
        # Tải biểu tượng
        try:
            self.plus_image = ImageTk.PhotoImage(Image.open("Assets/img/plus.jpg").resize((20, 20)))
            self.minus_image = ImageTk.PhotoImage(Image.open("Assets/img/minus.jpg").resize((20, 20)))
        except Exception as e:
            print(f"Lỗi khi tải icon Accordion: {e}")
            # Sử dụng ký hiệu Unicode nếu không tải được hình ảnh
            self.plus_image = None
            self.minus_image = None

        # Header frame
        self.header = tk.Frame(self, bg="#f0f0f0", pady=10)
        self.header.pack(fill='x')

        # Nút tiêu đề
        self.toggle_button = tk.Button(
            self.header, 
            text=title, 
            font=("Helvetica", 14, "bold"), 
            bg="#f0f0f0",
            bd=0, 
            relief="flat",
            anchor="w",
            command=self.toggle
        )
        self.toggle_button.pack(side="left", fill='x', expand=True)

        # Biểu tượng
        if self.plus_image and self.minus_image:
            self.icon_label = tk.Label(self.header, image=self.plus_image, bg="#f0f0f0")
            self.icon_label.pack(side="right")
        else:
            # Sử dụng ký hiệu Unicode nếu không có hình ảnh
            self.icon_label = tk.Label(self.header, text="➕", font=("Helvetica", 12), bg="#f0f0f0")
            self.icon_label.pack(side="right")

        # Content frame (initially hidden)
        self.content_frame = tk.Frame(self, bg="#ffffff")
        self.content_label = tk.Label(
            self.content_frame, 
            text=content, 
            font=("Helvetica", 12), 
            wraplength=550, 
            justify='left',
            bg="#ffffff",
            padx=10,
            pady=10
        )
        self.content_label.pack(fill='x')

        # Hiệu ứng hover cho header
        self.header.bind("<Enter>", self.on_enter)
        self.header.bind("<Leave>", self.on_leave)
        self.toggle_button.bind("<Enter>", self.on_enter)
        self.toggle_button.bind("<Leave>", self.on_leave)
        self.icon_label.bind("<Enter>", self.on_enter)
        self.icon_label.bind("<Leave>", self.on_leave)
    
    def toggle(self):
        if self.is_expanded:
            self.content_frame.pack_forget()
            if self.plus_image and self.minus_image:
                self.icon_label.config(image=self.plus_image)
            else:
                self.icon_label.config(text="➕")
            self.is_expanded = False
        else:
            self.content_frame.pack(fill='x')
            if self.plus_image and self.minus_image:
                self.icon_label.config(image=self.minus_image)
            else:
                self.icon_label.config(text="➖")
            self.is_expanded = True
    
    def on_enter(self, event):
        self.header.config(bg="#e0e0e0")
        self.toggle_button.config(bg="#e0e0e0")
        self.icon_label.config(bg="#e0e0e0")
    
    def on_leave(self, event):
        self.header.config(bg="#f0f0f0")
        self.toggle_button.config(bg="#f0f0f0")
        self.icon_label.config(bg="#f0f0f0")

import tkinter as tk
from tkinter import ttk
import html

class HealthDetailView:
    def __init__(self, parent, bmi_category_id, model):
        self.parent = parent
        self.bmi_category_id = bmi_category_id
        self.window = tk.Toplevel(parent)
        self.window.title("Chi tiết đánh giá sức khỏe")
        self.window.geometry("400x400")
        self.window.resizable(False, False)
        self.window.configure(bg="#F0F4F7")
        self.model = model

        self.center_window()

        # Main Frame
        main_frame = ttk.Frame(self.window, padding=20)
        main_frame.pack(expand=True, fill='both')

        # Title
        title_label = ttk.Label(main_frame, text="Đánh Giá Sức Khỏe", font=("Helvetica", 18, "bold"), foreground="#333333")
        title_label.pack(pady=(0, 10))

        # Category Description
        description = self.get_description()
        description_label = ttk.Label(main_frame, text=description, font=("Helvetica", 12), wraplength=360, foreground="#555555", justify="left")
        description_label.pack(pady=10)

        # Recommendations
        recommendations = self.get_recommendations()
        recommendations_label = ttk.Label(main_frame, text="Khuyến nghị:", font=("Helvetica", 14, "bold"), foreground="#333333")
        recommendations_label.pack(anchor='w', pady=(10, 0))

        recommendations_text = ttk.Label(main_frame, text=recommendations, font=("Helvetica", 12), wraplength=360, foreground="#555555", justify="left")
        recommendations_text.pack(pady=5)

        # Close Button
        close_button = ttk.Button(main_frame, text="Đóng", command=self.window.destroy, style="Accent.TButton")
        close_button.pack(pady=20, ipadx=10, ipady=5)

        # Styling
        style = ttk.Style()
        style.configure("Accent.TButton",
                        foreground="#8ab4f8",
                        background="#8ab4f8",
                        font=("Helvetica", 10, "bold"),
                        padding=1,
                        borderwidth=0,
                        focusthickness=0)
        style.map("Accent.TButton",
                  background=[('active', '#6c99e8')],
                  foreground=[('active', '#8ab4f8')])

    def center_window(self):
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f"+{x}+{y}")

    def get_description(self):
        result = self.model.get_health_detail_by_categoryid(self.bmi_category_id)

        return result.HealthAssessment

    def get_recommendations(self):
        result = self.model.get_health_detail_by_categoryid(self.bmi_category_id)

        return result.Recommendation.replace("\\n", "\n")
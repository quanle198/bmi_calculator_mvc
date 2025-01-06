import tkinter as tk
from tkinter import ttk

class HistoryWindow:
    def __init__(self, parent, history):
        self.window = tk.Toplevel(parent)
        self.window.title("Lịch Sử BMI")
        self.window.geometry("400x400")
        self.window.resizable(False, False)
        self.window.configure(bg="#F0F4F7")

        main_frame = ttk.Frame(self.window, padding=20)
        main_frame.pack(expand=True, fill='both')

        title_label = ttk.Label(main_frame, text="Lịch Sử BMI", font=("Helvetica", 18, "bold"), foreground="#333333")
        title_label.pack(pady=(0, 10))

        # Danh sách lịch sử
        for entry in history:
            entry_label = ttk.Label(
                main_frame,
                text=f"{entry['date']}: BMI={entry['bmi']} ({entry['category']})",
                font=("Helvetica", 12),
                foreground="#555555",
                wraplength=360,
                justify="left"
            )
            entry_label.pack(anchor='w', pady=2)
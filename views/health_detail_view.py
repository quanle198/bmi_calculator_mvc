import tkinter as tk
from tkinter import ttk

class HealthDetailView:
    def __init__(self, parent, bmi_category):
        self.parent = parent
        self.bmi_category = bmi_category
        self.window = tk.Toplevel(parent)
        self.window.title("Chi tiết đánh giá sức khỏe")
        self.window.geometry("400x400")
        self.window.resizable(False, False)
        self.window.configure(bg="#F0F4F7")

        # Center the window relative to parent
        self.center_window()

        # Main Frame
        main_frame = ttk.Frame(self.window, padding=20)
        main_frame.pack(expand=True, fill='both')

        # Title
        title_label = ttk.Label(main_frame, text="Đánh Giá Sức Khỏe", font=("Helvetica", 18, "bold"), foreground="#333333")
        title_label.pack(pady=(0, 10))

        # Image (Optional: Add relevant images for each category)
        # For demonstration, we'll skip image implementation

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
                        font=("Helvetica", 12, "bold"),
                        padding=10,
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
        descriptions = {
            "Thiếu cân": "Chỉ số BMI của bạn cho thấy bạn đang thiếu cân. Thiếu cân có thể dẫn đến các vấn đề sức khỏe như suy giảm miễn dịch, loãng xương và mệt mỏi.",
            "Bình thường": "Chỉ số BMI của bạn trong khoảng bình thường, điều này cho thấy bạn có cơ thể khỏe mạnh. Hãy tiếp tục duy trì chế độ ăn uống và lối sống lành mạnh.",
            "Thừa cân": "Chỉ số BMI của bạn cho thấy bạn đang thừa cân. Thừa cân có thể tăng nguy cơ mắc các bệnh như tiểu đường, cao huyết áp và các vấn đề về tim mạch.",
            "Béo phì": "Chỉ số BMI của bạn cho thấy bạn đang béo phì. Béo phì là yếu tố nguy cơ chính cho nhiều bệnh nghiêm trọng như bệnh tim, đột quỵ, và một số loại ung thư."
        }
        return descriptions.get(self.bmi_category, "Không có thông tin chi tiết.")

    def get_recommendations(self):
        recommendations = {
            "Thiếu cân": "• Tăng cường ăn thực phẩm giàu dinh dưỡng như ngũ cốc nguyên hạt, protein, và chất béo lành mạnh.\n• Tập luyện thể dục thường xuyên để tăng cường sức mạnh cơ bắp.\n• Tham khảo ý kiến bác sĩ hoặc chuyên gia dinh dưỡng.",
            "Bình thường": "• Tiếp tục duy trì chế độ ăn uống cân đối.\n• Vận động thường xuyên để giữ gìn sức khỏe.\n• Theo dõi cân nặng định kỳ để đảm bảo không tăng thêm.",
            "Thừa cân": "• Giảm lượng calo tiêu thụ bằng cách hạn chế thực phẩm giàu đường và chất béo.\n• Tăng cường hoạt động thể chất như đi bộ, chạy bộ hoặc bơi lội.\n• Xem xét tư vấn với chuyên gia dinh dưỡng.",
            "Béo phì": "• Thực hiện chế độ ăn kiêng nghiêm ngặt dưới sự giám sát của bác sĩ.\n• Tăng cường vận động thể chất.\n• Cân nhắc các phương pháp điều trị y tế hoặc phẫu thuật nếu cần thiết."
        }
        return recommendations.get(self.bmi_category, "Không có khuyến nghị cụ thể.")

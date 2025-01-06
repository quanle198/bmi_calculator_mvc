import os
from datetime import datetime
import json

# --------------------- Model --------------------- #
class BMIModel:
    def __init__(self):
        self.height = 0.0  # in centimeters
        self.weight = 0.0  # in kilograms
        self.history_file = "bmi_history.json"
        self.history = self.load_history()
    
    def load_history(self):
        if os.path.exists(self.history_file):
            with open(self.history_file, 'r') as file:
                return json.load(file)
        return []

    def save_history(self, bmi, category):
        entry = {
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "bmi": bmi,
            "category": category
        }
        self.history.append(entry)
        with open(self.history_file, 'w') as file:
            json.dump(self.history, file, indent=4)

    def set_height(self, height):
        self.height = height

    def set_weight(self, weight):
        self.weight = weight

    def calculate_bmi(self):
        if self.height <= 0 or self.weight <= 0:
            raise ValueError("Height and weight must be positive numbers.")
        height_in_meters = self.height / 100
        bmi = round(self.weight / (height_in_meters ** 2), 1)
        return bmi

    def get_bmi_category(self, bmi):
        if bmi < 18.5:
            return "Thiếu cân", "Bạn đang thiếu cân.\nBổ sung thực phẩm dinh dưỡng."
        elif 18.5 <= bmi < 24.9:
            return "Bình thường", "Cân nặng hợp lý.\nDuy trì chế độ ăn và tập luyện."
        elif 24.9 <= bmi < 29.9:
            return "Thừa cân", "Bạn đang thừa cân.\nTăng cường vận động."
        else:
            return "Béo phì", "Bạn đang béo phì.\nTham khảo ý kiến bác sĩ."
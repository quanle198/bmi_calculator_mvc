import os
from datetime import datetime
import json
from database.connect import MSSQLConnection

# --------------------- Model --------------------- #
class BMIModel:
    def __init__(self):
        self.db = MSSQLConnection()
        self.height = 0.0  # in centimeters
        self.weight = 0.0  # in kilograms
        self.history_file = "bmi_history.json"
        self.history = self.load_history()
    
    def load_history(self):
        history = self.db.query('SELECT * FROM HISTORY')
        category = self.get_all_category()
        result = []
        for h in history:
            result.append({
                "id": h.Id,
                "date": h.Date,
                "bmi": h.BMI,
                "categoryName": next((c for c in category if c.Id == h.CategoryId), None).Name,
                "note": h.Note
            })
        return result
    
    def get_all_category(self):
        return self.db.query('SELECT * FROM CATEGORY')
    
    def get_health_detail_by_categoryid(self, categoryId):
        return self.db.query_one(f'SELECT * FROM HEALTH_DETAIL WHERE CategoryId={categoryId}')

    def save_history(self, bmi, categoryId):
        entry = {
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "bmi": bmi,
            "categoryId": categoryId,
            "note": None
        }
        return self.db.insert(f"INSERT INTO HISTORY (Date, BMI, CategoryId) VALUES ('{entry['date']}', {entry['bmi']}, {entry['categoryId']})")

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
        result = self.db.query(f"SELECT * FROM CATEGORY")

        for r in result:
            if r.MaxOfBMI is None:
                return r.Id, r.Name, r.Description
            elif  r.MinOfBMI <= bmi < r.MaxOfBMI:
                return r.Id, r.Name, r.Description


            
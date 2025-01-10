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
        self.current_user_id = None
        self.history = self.load_history()
    
    def login_user(self, username, password):
        user = self.db.query_one(f"SELECT * FROM USERS WHERE Username='{username}' AND Password='{password}'")
        if user:
            self.current_user_id = user.Id
            return True, user.Id, user.Username, user.Role
        return False, None, None
    
    def register_user(self, username, password, role):
        try:
            query = "INSERT INTO USERS (Username, Password, Role) VALUES (?, ?, ?)"
            params = (username, password, role)
            self.db.insert(query, params)
            return True
        except:
            return False
    
    def load_history(self):
        if self.current_user_id is None:
            return []
        query = "SELECT * FROM HISTORY WHERE UserId = ?"
        params = (self.current_user_id)
        history = self.db.query(query, params)
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
    
    def load_faq(self):
        faq = self.db.query('SELECT * FROM FAQ')
        result = []
        for item in faq:
            result.append({
                "id": item.Id,
                "question": item.Question,
                "answer": item.Answer
            })
        return result
    
    def get_all_category(self):
        return self.db.query('SELECT * FROM CATEGORY')
    
    def get_health_detail_by_categoryid(self, categoryId):
        return self.db.query_one(f'SELECT * FROM HEALTH_DETAIL WHERE CategoryId={categoryId}')

    def save_history(self, bmi, userId, categoryId):
        entry = {
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "bmi": bmi,
            "userId": userId,
            "categoryId": categoryId,
            "note": "---"
        }
        return self.db.insert(f"INSERT INTO HISTORY (Date, BMI, UserId, CategoryId, Note) VALUES ('{entry['date']}', {entry['bmi']}, {entry['userId']}, {entry['categoryId']}, '{entry['note']}')")
    
    def delete_history_entry(self, entry_id):
        return self.db.delete(f"DELETE FROM HISTORY WHERE Id={entry_id}")
    
    def update_history_note(self, entry_id, note):
        query = "UPDATE HISTORY SET Note = ? WHERE Id = ?"
        params = (note, entry_id)
        return self.db.update(query, params)

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


            
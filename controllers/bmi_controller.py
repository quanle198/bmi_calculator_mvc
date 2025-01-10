from models.bmi_model import BMIModel
from views.bmi_view import BMIView
from views.health_detail_view import HealthDetailView

# --------------------- Controller --------------------- #
class BMIController:
    def __init__(self, root):
        self.model = BMIModel()
        self.view = BMIView(root, self.model)
        self.setup()
        self.last_valid_height = 0.0  # To keep track of the last valid height
        self.last_valid_weight = 0.0  # To keep track of the last valid weight
        self.categoryId = None

    def setup(self):
        # Initialize entries with slider values
        self.view.height_var.set("0.00")
        self.view.weight_var.set("0.00")

        # Bind slider movements to controller methods
        self.view.set_height_slider_command(self.on_height_slider_changed)
        self.view.set_weight_slider_command(self.on_weight_slider_changed)

        # Bind calculate button
        self.view.set_calculate_command(self.calculate_bmi)

        # Bind view details button
        self.view.set_view_details_command(self.open_health_detail)

        # Bind entry changes
        self.view.height_var.trace_add("write", self.on_height_entry_changed)
        self.view.weight_var.trace_add("write", self.on_weight_entry_changed)

    def on_height_slider_changed(self, value):
        try:
            height = float(float(value))
            self.model.set_height(height)
            self.view.update_height(height)
            self.last_valid_height = height  # Update last valid height
            # Enable view details button if BMI is calculated
            if self.is_bmi_calculated():
                self.view.enable_view_details()
            else:
                self.view.disable_view_details()
        except ValueError:
            pass

    def on_weight_slider_changed(self, value):
        try:
            weight = float(float(value))
            self.model.set_weight(weight)
            self.view.update_weight(weight)
            self.last_valid_weight = weight  # Update last valid weight
            # Enable view details button if BMI is calculated
            if self.is_bmi_calculated():
                self.view.enable_view_details()
            else:
                self.view.disable_view_details()
        except ValueError:
            pass

    def on_height_entry_changed(self, *args):
        height_str = self.view.height_var.get()
        try:
            # Attempt to convert the entry to a float
            height = float(height_str)
            if height < 0 or height > 220:
                raise ValueError("Height out of valid range (0-220 cm).")
            self.model.set_height(height)
            self.view.update_height(height)
            self.view.height_slider.set(height)  # Update slider position
            self.last_valid_height = height  # Update last valid height
            # Enable view details button if BMI is calculated
            if self.is_bmi_calculated():
                self.view.enable_view_details()
            else:
                self.view.disable_view_details()
        except ValueError:
            # If invalid, revert to the last valid height and notify the user
            self.view.height_var.set(f"{self.last_valid_height:.2f}")
            self.view.update_advice("Chiều cao không hợp lệ. Vui lòng nhập số từ 0 đến 220.")
            self.view.disable_view_details()
            print(f"Invalid height input: '{height_str}'")

    def on_weight_entry_changed(self, *args):
        weight_str = self.view.weight_var.get()
        try:
            # Attempt to convert the entry to a float
            weight = float(weight_str)
            if weight < 0 or weight > 200:
                raise ValueError("Weight out of valid range (0-200 kg).")
            self.model.set_weight(weight)
            self.view.update_weight(weight)
            self.view.weight_slider.set(weight)  # Update slider position
            self.last_valid_weight = weight  # Update last valid weight
            # Enable view details button if BMI is calculated
            if self.is_bmi_calculated():
                self.view.enable_view_details()
            else:
                self.view.disable_view_details()
        except ValueError:
            # If invalid, revert to the last valid weight and notify the user
            self.view.weight_var.set(f"{self.last_valid_weight:.2f}")
            self.view.update_advice("Cân nặng không hợp lệ. Vui lòng nhập số từ 0 đến 200.")
            self.view.disable_view_details()
            print(f"Invalid weight input: '{weight_str}'")

    def is_bmi_calculated(self):
        """
        Check if BMI has been calculated and is valid.
        """
        bmi = self.view.bmi_var.get()
        return bmi != "--" and bmi != "Lỗi"

    def calculate_bmi(self):
        try:
            bmi = self.model.calculate_bmi()
            categoryId, category, advice = self.model.get_bmi_category(bmi)
            self.categoryId = categoryId
            self.view.update_bmi(bmi)
            self.view.update_category(category)
            self.view.update_advice(advice)
            if self.view.is_logged_in:
                self.model.save_history(bmi, self.view.userId, categoryId)
            # Enable view details button
            self.view.enable_view_details()
        except ValueError as e:
            self.view.update_bmi("--")
            self.view.update_category("Lỗi")
            self.view.update_advice("Hãy nhập số hợp lệ.")
            self.view.disable_view_details()
            print(f"Error calculating BMI: {e}")

    def open_health_detail(self):
        """
        Open the Health Detail window with the current BMI category.
        """
        category = self.view.category_var.get()
        if category not in ["--", "Lỗi"]:
            HealthDetailView(self.view.root, self.categoryId, self.model)
        else:
            self.view.update_advice("Không có dữ liệu để hiển thị chi tiết.")
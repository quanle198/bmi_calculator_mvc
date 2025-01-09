import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from views.history_view import HistoryWindow
from views.faq_view import FAQWindow
from views.login_view import LoginWindow

# --------------------- View --------------------- #
class BMIView:
    def __init__(self, root, model):
        self.root = root
        self.root.title("BMI Calculator")
        self.root.geometry("500x800")  # Increased height to accommodate the new button
        self.root.resizable(True, True)
        self.root.configure(bg="#8ab4f8")  # Light background color
        self.model = model
        self.is_logged_in = False  # Track login state

        #icon
        image_icon=tk.PhotoImage(file="Assets/img/bmi-icon.png")
        self.root.iconphoto(False,image_icon)

        # Configure grid layout
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        # Main Frame
        main_frame = ttk.Frame(self.root, padding=20)
        main_frame.grid(sticky="NSEW")

        # Configure grid in main_frame
        for i in range(14):  # Increased range to accommodate new widgets
            main_frame.rowconfigure(i, weight=1)
        for i in range(2):
            main_frame.columnconfigure(i, weight=1)

        # Title Label
        # Load the icon image
        icon_image = Image.open("Assets/img/bmi-icon.png")
        icon_image = icon_image.resize((30, 30))
        icon_photo = ImageTk.PhotoImage(icon_image)

        # Create a label with the icon and text
        title_label = ttk.Label(main_frame, text=" BMI Calculator", font=("Helvetica", 24, "bold"), foreground="#333333", image=icon_photo, compound="left")
        title_label.image = icon_photo  # Keep a reference to avoid garbage collection
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))

        # Height Section
        height_label = ttk.Label(main_frame, text="Chiều cao (cm)", font=("Helvetica", 14), foreground="#555555")
        height_label.grid(row=1, column=0, sticky="W", padx=10)

        self.height_var = tk.StringVar(value="0.00")

        # Register validation command for height_entry
        vcmd = (self.root.register(self.validate_float), '%P')
        height_entry = ttk.Entry(
            main_frame,
            textvariable=self.height_var,
            font=("Helvetica", 14),
            justify="center",
            validate='key',
            validatecommand=vcmd
        )
        height_entry.grid(row=1, column=1, sticky="E", padx=10)
        height_entry.config(width=10)

        self.height_slider = ttk.Scale(main_frame, from_=0, to=220, orient=tk.HORIZONTAL, style="TScale")
        self.height_slider.grid(row=2, column=0, columnspan=2, sticky="EW", padx=10, pady=(5, 15))

        # Weight Section
        weight_label = ttk.Label(main_frame, text="Cân nặng (kg)", font=("Helvetica", 14), foreground="#555555")
        weight_label.grid(row=3, column=0, sticky="W", padx=10)

        self.weight_var = tk.StringVar(value="0.00")

        # Register validation command for weight_entry
        vcmd_weight = (self.root.register(self.validate_float), '%P')
        weight_entry = ttk.Entry(
            main_frame,
            textvariable=self.weight_var,
            font=("Helvetica", 14),
            justify="center",
            validate='key',
            validatecommand=vcmd_weight
        )
        weight_entry.grid(row=3, column=1, sticky="E", padx=10)
        weight_entry.config(width=10)

        self.weight_slider = ttk.Scale(main_frame, from_=0, to=200, orient=tk.HORIZONTAL, style="TScale")
        self.weight_slider.grid(row=4, column=0, columnspan=2, sticky="EW", padx=10, pady=(5, 20))

        # Calculate Button with Enhanced Style
        self.style = ttk.Style()
        self.style.configure("Accent.TButton",
                             foreground="#8ab4f8",
                             background="#8ab4f8",
                             font=("Helvetica", 10, "bold"),
                             padding=1,
                             borderwidth=0,  # Flat design
                             focusthickness=0)  # Remove focus border

        self.style.map("Accent.TButton",
                       background=[('active', '#6c99e8')],  # Darker blue on hover
                       foreground=[('active', '#8ab4f8')])

        self.calculate_button = ttk.Button(main_frame, text="Xem kết quả", style="Accent.TButton")
        self.calculate_button.grid(row=5, column=0, columnspan=2, pady=10, ipadx=10, ipady=10)

        # New: View Details Button
        self.view_details_button = ttk.Button(main_frame, text="Xem chi tiết", style="Accent.TButton")
        self.view_details_button.grid(row=13, column=0, columnspan=2, pady=10, ipadx=10, ipady=10)
        self.view_details_button.grid_remove()  # Disabled by default

        # Thêm nút "Xem Lịch Sử"
        self.view_history_button = ttk.Button(main_frame, text="Xem Lịch Sử", style="Accent.TButton")
        self.view_history_button.grid(row=6, column=0, columnspan=2, pady=10, ipadx=10, ipady=10)
        self.view_history_button.config(command=self.show_history)
        self.view_history_button.grid_remove()  # Disable history button

        # Thêm nút "Xem FAQ"
        self.view_faq_button = ttk.Button(main_frame, text="Xem FAQ", style="Accent.TButton", command=self.show_faq)
        self.view_faq_button.grid(row=7, column=0, columnspan=2, pady=10, ipadx=10, ipady=10)

        # New: Login Button
        self.login_button = ttk.Button(main_frame, text="Login", style="Accent.TButton", command=self.open_login)
        self.login_button.grid(row=8, column=0, columnspan=2, pady=10, ipadx=10, ipady=10)

        # Separator
        separator = ttk.Separator(main_frame, orient='horizontal')
        separator.grid(row=9, column=0, columnspan=2, sticky="EW", pady=20)

        # Result Section
        self.bmi_var = tk.StringVar(value="--")
        bmi_label_title = ttk.Label(main_frame, text="BMI", font=("Helvetica", 16), foreground="#555555")
        bmi_label_title.grid(row=10, column=0, sticky="E", padx=10)
        self.bmi_label = ttk.Label(main_frame, textvariable=self.bmi_var, font=("Helvetica", 16, "bold"), foreground="#000000")
        self.bmi_label.grid(row=10, column=1, sticky="W", padx=10)

        self.category_var = tk.StringVar(value="--")
        category_label_title = ttk.Label(main_frame, text="Thể loại", font=("Helvetica", 16), foreground="#555555")
        category_label_title.grid(row=11, column=0, sticky="E", padx=10)
        self.category_label = ttk.Label(main_frame, textvariable=self.category_var, font=("Helvetica", 16, "bold"), foreground="#000000")
        self.category_label.grid(row=11, column=1, sticky="W", padx=10)

        self.advice_var = tk.StringVar(value="Nhập chiều cao và cân nặng để tính BMI.")
        advice_label = ttk.Label(main_frame, textvariable=self.advice_var, font=("Helvetica", 12), wraplength=400, foreground="#777777", justify="center")
        advice_label.grid(row=12, column=0, columnspan=2, pady=10)

        # Additional Styling for Other Widgets (Optional)
        self.style.configure("TScale", troughcolor="#D3D3D3", background="#F0F4F7")

    def open_login(self):
        """Open the login window."""
        LoginWindow(self.root, self.model, self.on_login_success)

    def on_login_success(self):
        """Handle actions after successful login."""
        self.is_logged_in = True
        self.view_history_button.grid()  # Show history button
        self.login_button.config(text="Logout", command=self.logout)
  

    def logout(self):
        """Handle user logout."""
        self.is_logged_in = False
        self.view_history_button.grid_remove()  # Disable history button
        self.login_button.config(text="Login", command=self.open_login)
 

    def show_history(self):
        HistoryWindow(self.root, self.model)

    def show_faq(self):
        FAQWindow(self.root, self.model)  # Mở cửa sổ FAQ

    def validate_float(self, P):
        """
        Validate that the input is a valid float or empty string.
        P: the new value of the entry
        """
        if P == "":
            return True
        try:
            float(P)
            return True
        except ValueError:
            return False

    def update_height(self, height):
        self.height_var.set(f"{height:.2f}")

    def update_weight(self, weight):
        self.weight_var.set(f"{weight:.2f}")

    def update_bmi(self, bmi):
        self.bmi_var.set(str(bmi))

    def update_category(self, category):
        self.category_var.set(category)

    def update_advice(self, advice):
        self.advice_var.set(advice)

    def set_calculate_command(self, command):
        self.calculate_button.config(command=command)

    def set_view_details_command(self, command):
        self.view_details_button.config(command=command)

    def set_height_slider_command(self, command):
        self.height_slider.config(command=command)

    def set_weight_slider_command(self, command):
        self.weight_slider.config(command=command)

    def enable_view_details(self):
        self.view_details_button.grid()

    def disable_view_details(self):
        self.view_details_button.grid_remove()
import tkinter as tk
from controllers.bmi_controller import BMIController

# --------------------- Main Application --------------------- #
def main():
    root = tk.Tk()
    app = BMIController(root)
    root.mainloop()

if __name__ == "__main__":
    main()
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox


class HistoryWindow:
    def __init__(self, parent, model):
        self.model = model  # Store the model to allow deletion and updates
        self.window = tk.Toplevel(parent)
        self.window.title("Lịch Sử BMI")
        self.window.geometry("800x600")  # Increased width to accommodate the new column
        self.window.resizable(False, False)
        self.window.configure(bg="#F0F4F7")

        main_frame = ttk.Frame(self.window, padding=20)
        main_frame.pack(expand=True, fill='both')

        title_label = ttk.Label(main_frame, text="Lịch Sử BMI", font=("Helvetica", 18, "bold"), foreground="#333333")
        title_label.pack(pady=(0, 10))

        # Define Treeview columns
        columns = ("ID", "Date", "BMI", "Category", "Note")
        self.tree = ttk.Treeview(main_frame, columns=columns, show="headings", height=15)

        # Define headings
        self.tree.heading("ID", text="ID")
        self.tree.heading("Date", text="Date")
        self.tree.heading("BMI", text="BMI")
        self.tree.heading("Category", text="Category")
        self.tree.heading("Note", text="Note")

        # Define column widths
        self.tree.column("ID", width=50, anchor="center")
        self.tree.column("Date", width=150, anchor="center")
        self.tree.column("BMI", width=100, anchor="center")
        self.tree.column("Category", width=150, anchor="center")
        self.tree.column("Note", width=300, anchor="w", stretch=True)  # Wider column for notes

        # Insert data into Treeview
        history = self.model.load_history()
        for entry in history:
            self.tree.insert("", "end", values=(
                entry['id'],
                entry['date'],
                entry['bmi'],
                entry['categoryName'],
                entry.get('note', "")  # Ensure 'note' exists
            ))

        self.tree.pack(expand=True, fill='both', pady=10)

        # Add scrollbar
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        # Add Delete button
        style = ttk.Style()
        style.configure("Red.TButton", background="red", foreground="red")  # Changed foreground to white for visibility
        delete_button = ttk.Button(main_frame, text="Xóa dòng dữ liệu", command=self.delete_selected, style="Red.TButton")
        delete_button.pack(pady=(10, 0))

        # Bind double-click event for editing
        self.tree.bind("<Double-1>", self.on_double_click)

        # Initialize editing widgets
        self.editing_entry = None

    def delete_selected(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("No Selection", "Vui lòng chọn một dòng để xoá.")
            return

        # Get the first selected item
        row_id = selected_item[0]
        values = self.tree.item(row_id, "values")
        entry_id = values[0]

        # Confirm deletion
        confirm = messagebox.askyesno("Confirm Delete", "Bạn có chắc chắn muốn xoá dòng này không?")
        if confirm:
            try:
                # Delete from Treeview
                self.tree.delete(row_id)
                # Delete from data source
                self.model.delete_history_entry(entry_id)
                messagebox.showinfo("Deleted", "Dòng đã được xoá thành công.")
            except Exception as e:
                messagebox.showerror("Error", f"Đã xảy ra lỗi khi xoá: {e}")

    def on_double_click(self, event):
        # Identify the row and column under cursor
        region = self.tree.identify("region", event.x, event.y)
        if region != "cell":
            return

        row_id = self.tree.identify_row(event.y)
        column = self.tree.identify_column(event.x)

        if column != '#5':  # Assuming 'Note' is the 5th column
            return

        # Get the column index
        col_index = int(column.replace('#', '')) - 1

        # Get current value
        item = self.tree.item(row_id)
        current_value = item['values'][col_index]

        # Get column bbox
        x, y, width, height = self.tree.bbox(row_id, column)

        # Create Entry widget
        self.editing_entry = tk.Entry(self.tree)
        self.editing_entry.place(x=x, y=y, width=width, height=height)
        self.editing_entry.insert(0, current_value)
        self.editing_entry.focus()

        # Bind events to handle editing
        self.editing_entry.bind("<Return>", lambda e: self.save_edit(row_id, col_index))
        self.editing_entry.bind("<FocusOut>", lambda e: self.cancel_edit())

    def save_edit(self, row_id, col_index):
        new_value = self.editing_entry.get()
        self.editing_entry.destroy()
        self.editing_entry = None

        # Update Treeview
        current_values = list(self.tree.item(row_id, "values"))
        current_values[col_index] = new_value
        self.tree.item(row_id, values=current_values)

        # Update model
        entry_id = current_values[0]
        try:
            self.model.update_history_note(entry_id, new_value)
            messagebox.showinfo("Success", "Ghi chú đã được cập nhật.")
        except Exception as e:
            messagebox.showerror("Error", f"Đã xảy ra lỗi khi cập nhật ghi chú: {e}")

    def cancel_edit(self):
        if self.editing_entry:
            self.editing_entry.destroy()
            self.editing_entry = None

# Example Model Implementation
class Model:
    def __init__(self):
        # This is a mock implementation. Replace with actual data handling.
        self.history = [
            {'id': '1', 'date': '2024-12-01', 'bmi': '22.5', 'categoryName': 'Normal', 'note': 'Feeling good'},
            {'id': '2', 'date': '2024-12-15', 'bmi': '24.3', 'categoryName': 'Overweight', 'note': ''},
            # Add more entries as needed
        ]

    def load_history(self):
        return self.history

    def delete_history_entry(self, entry_id):
        self.history = [entry for entry in self.history if entry['id'] != entry_id]

    def update_history_note(self, entry_id, new_note):
        for entry in self.history:
            if entry['id'] == entry_id:
                entry['note'] = new_note
                break
        else:
            raise ValueError("Entry ID not found")



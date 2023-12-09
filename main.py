# main.py
import tkinter as tk
from app import FacialRecognitionApp
from database import DatabaseManager

if __name__ == "__main__":
    root = tk.Tk()
    db_manager = DatabaseManager()
    app = FacialRecognitionApp(root, db_manager)
    root.mainloop()
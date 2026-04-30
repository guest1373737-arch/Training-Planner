import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime

class TrainingPlanner:
    def __init__(self, root):
        self.root = root
        self.root.title("Training Planner - Dautov Edgar")
        self.root.geometry("600x500")
        
        self.file_path = 'trainings.json'
        self.trainings = self.load_data()

        # Поля ввода
        frame_input = tk.LabelFrame(root, text="Добавить тренировку", padx=10, pady=10)
        frame_input.pack(fill="x", padx=10, pady=5)

        tk.Label(frame_input, text="Дата (ДД.ММ.ГГГГ):").grid(row=0, column=0)
        self.entry_date = tk.Entry(frame_input)
        self.entry_date.insert(0, datetime.now().strftime("%d.%m.%Y"))
        self.entry_date.grid(row=0, column=1)

        tk.Label(frame_input, text="Тип:").grid(row=0, column=2)
        self.combo_type = ttk.Combobox(frame_input, values=["Силовая", "Кардио", "Йога", "Плавание"])
        self.combo_type.grid(row=0, column=3)

        tk.Label(frame_input, text="Мин:").grid(row=1, column=0)
        self.entry_duration = tk.Entry(frame_input)
        self.entry_duration.grid(row=1, column=1)

        btn_add = tk.Button(frame_input, text="Добавить", command=self.add_training, bg="green", fg="white")
        btn_add.grid(row=1, column=2, columnspan=2, sticky="we", padx=5)

        # Фильтрация
        frame_filter = tk.Frame(root, padx=10, pady=5)
        frame_filter.pack(fill="x")
        tk.Label(frame_filter, text="Фильтр по типу:").pack(side="left")
        self.filter_type = ttk.Combobox(frame_filter, values=["Все", "Силовая", "Кардио", "Йога", "Плавание"])
        self.filter_type.set("Все")
        self.filter_type.pack(side="left", padx=5)
        btn_filter = tk.Button(frame_filter, text="Применить", command=self.update_table)
        btn_filter.pack(side="left")

        # Таблица
        self.tree = ttk.Treeview(root, columns=("Date", "Type", "Duration"), show='headings')
        self.tree.heading("Date", text="Дата")
        self.tree.heading("Type", text="Тип")
        self.tree.heading("Duration", text="Длительность (мин)")
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        self.update_table()

    def add_training(self):
        date = self.entry_date.get()
        t_type = self.combo_type.get()
        duration = self.entry_duration.get()

        try:
            datetime.strptime(date, "%d.%m.%Y")
            if int(duration) <= 0: raise ValueError
        except ValueError:
            messagebox.showerror("Ошибка", "Проверьте формат даты (ДД.ММ.ГГГГ) и длительность (>0)")
            return

        self.trainings.append({"date": date, "type": t_type, "duration": duration})
        self.save_data()
        self.update_table()
        self.entry_duration.delete(0, tk.END)

    def update_table(self):
        for i in self.tree.get_children(): self.tree.delete(i)
        f_type = self.filter_type.get()
        
        for t in self.trainings:
            if f_type == "Все" or t["type"] == f_type:
                self.tree.insert("", "end", values=(t["date"], t["type"], t["duration"]))

    def save_data(self):
        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump(self.trainings, f, ensure_ascii=False, indent=4)

    def load_data(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []

if __name__ == "__main__":
    root = tk.Tk()
    app = TrainingPlanner(root)
    root.mainloop()
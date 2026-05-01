import tkinter as tk
from tkinter import ttk, messagebox
import json

class MovieLibrary:
    def __init__(self, root):
        self.root = root
        self.root.title("Movie Library")
        self.movies = []
        self.create_widgets()
        self.load_data()

    def create_widgets(self):
        # Поля ввода
        tk.Label(self.root, text="Название:").grid(row=0, column=0, sticky="w")
        self.title_entry = tk.Entry(self.root, width=30)
        self.title_entry.grid(row=0, column=1)

        tk.Label(self.root, text="Жанр:").grid(row=1, column=0, sticky="w")
        self.genre_var = tk.StringVar(value="Драма")
        genres = ["Драма", "Комедия", "Ужасы", "Фантастика", "Боевик", "Триллер", "Мелодрама"]
        self.genre_combo = ttk.Combobox(self.root, textvariable=self.genre_var, values=genres, state="readonly")
        self.genre_combo.grid(row=1, column=1)

        tk.Label(self.root, text="Год выпуска:").grid(row=2, column=0, sticky="w")
        self.year_entry = tk.Entry(self.root)
        self.year_entry.grid(row=2, column=1)

        tk.Label(self.root, text="Рейтинг (0-10):").grid(row=3, column=0, sticky="w")
        self.rating_entry = tk.Entry(self.root)
        self.rating_entry.grid(row=3, column=1)

        # Кнопки
        tk.Button(self.root, text="Добавить фильм", command=self.add_movie).grid(row=4, column=0, pady=10)
        tk.Button(self.root, text="Удалить фильм", command=self.delete_movie).grid(row=4, column=1, pady=10)

        # Таблица
        self.tree = ttk.Treeview(self.root, columns=("Title", "Genre", "Year", "Rating"), show="headings")
        self.tree.heading("Title", text="Название")
        self.tree.heading("Genre", text="Жанр")
        self.tree.heading("Year", text="Год")
        self.tree.heading("Rating", text="Рейтинг")
        self.tree.column("Title", width=200)
        self.tree.column("Genre", width=120)
        self.tree.column("Year", width=80)
        self.tree.column("Rating", width=80)
        self.tree.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

        # Фильтры
        tk.Label(self.root, text="Фильтр по жанру:").grid(row=6, column=0, sticky="w")
        self.filter_genre_var = tk.StringVar(value="Все")
        filter_genres = ["Все"] + genres
        self.filter_genre_combo = ttk.Combobox(self.root, textvariable=self.filter_genre_var, values=filter_genres, state="readonly")
        self.filter_genre_combo.grid(row=6, column=1)
        tk.Button(self.root, text="Применить фильтр", command=self.apply_filter).grid(row=6, column=2)

        tk.Label(self.root, text="Фильтр по году:").grid(row=7, column=0, sticky="w")
        self.filter_year_entry = tk.Entry(self.root)
        self.filter_year_entry.grid(row=7, column=1)
        tk.Button(self.root, text="Сбросить фильтры", command=self.reset_filter).grid(row=7, column=2)

        # Сохранение и загрузка
        tk.Button(self.root, text="Сохранить в JSON", command=self.save_data).grid(row=8, column=0, pady=10)
        tk.Button(self.root, text="Загрузить из JSON", command=self.load_data).grid(row=8, column=1, pady=10)

    def validate_input(self):
        if not self.title_entry.get():
            messagebox.showerror("Ошибка", "Название не может быть пустым.")
            return False

        try:
            year = int(self.year_entry.get())
            if year < 1888 or year > 2026:
                messagebox.showerror("Ошибка", "Год должен быть от 1888 до 2026.")
                return False
        except ValueError:
            messagebox.showerror("Ошибка", "Год должен быть числом.")
            return False

        try:
            rating = float(self.rating_entry.get())
            if rating < 0 or rating > 10:
                messagebox.showerror("Ошибка", "Рейтинг должен быть от 0 до 10.")
                return False
        except ValueError:
            messagebox.showerror("Ошибка", "Рейтинг должен быть числом.")
            return False

        return True

    def add_movie(self):
        if self.validate_input():
            movie = {
                "title": self.title_entry.get(),
                "genre": self.genre_var.get(),
                "year": int(self.year_entry.get()),
                "rating": float(self.rating_entry.get())
            }
            self.movies.append(movie)
            self.update_table()
            self.clear_inputs()

    def delete_movie(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Предупреждение", "Выберите фильм для удаления")
            return
        index = self.tree.index(selected[0])
        del self.movies[index]
        self.update_table()

    def update_table(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for movie in self.movies:
            self.tree.insert("", "end", values=(movie["title"], movie["genre"], movie["year"], movie["rating"]))

    def clear_inputs(self):
        self.title_entry.delete(0, tk.END)
        self.year_entry.delete(0, tk.END)
        self.rating_entry.delete(0, tk.END)
        self.genre_var.set("Драма")

    def save_data(self):
        with open("movies_data.json", "w", encoding="utf-8") as f:
            json.dump(self.movies, f, ensure_ascii=False, indent=4)
        messagebox.showinfo("Успех", "Данные сохранены в movies_data.json")

    def load_data(self):
        try:
            with open("movies_data.json", "r", encoding="utf-8") as f:
                self.movies = json.load(f)
            self.update_table()
        except FileNotFoundError:
            self.movies = []
        except json.JSONDecodeError:
            self.movies = []
            messagebox.showwarning("Предупреждение", "Файл JSON повреждён")

    def apply_filter(self):
        filtered = self.movies
        genre_filter = self.filter_genre_var.get()
        year_filter = self.filter_year_entry.get()

        if genre_filter != "Все":
            filtered = [m for m in filtered if m["genre"] == genre_filter]
        if year_filter:
            try:
                year_filter = int(year_filter)
                filtered = [m for m in filtered if m["year"] == year_filter]
            except ValueError:
                messagebox.showerror("Ошибка", "Год фильтра должен быть числом.")
                return

        for item in self.tree.get_children():
            self.tree.delete(item)
        for movie in filtered:
            self.tree.insert("", "end", values=(movie["title"], movie["genre"], movie["year"], movie["rating"]))

    def reset_filter(self):
        self.filter_genre_var.set("Все")
        self.filter_year_entry.delete(0, tk.END)
        self.update_table()

if __name__ == "__main__":
    root = tk.Tk()
    app = MovieLibrary(root)
    root.mainloop()
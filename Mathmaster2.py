import tkinter as tk
from tkinter import messagebox
import random
import datetime
import os

student_name = ""
current_a = 0
current_b = 0
correct_answer = 0
log_file = "log.csv"

if not os.path.exists(log_file):
    with open(log_file, 'w', encoding='utf-8') as f:
        f.write("Дата;Время;ФИО;Пример;Ответ;Результат\n")

def log_action(example, answer, result):
    """Запись в лог"""
    with open(log_file, 'a', encoding='utf-8') as f:
        now = datetime.datetime.now()
        date = now.strftime("%Y-%m-%d")
        time = now.strftime("%H:%M:%S")
        f.write(f"{date};{time};{student_name};{example};{answer};{result}\n")

def show_menu():
    """Окно меню"""
    global menu_window
    menu_window = tk.Tk()
    menu_window.title("Меню")
    menu_window.geometry("400x300")
    menu_window.configure(bg="white")
    
    tk.Label(menu_window, text=f"Здравствуйте, {student_name}", 
             font=("Arial", 12), bg="white", fg="#0066CC").pack(pady=20)
    
    tk.Label(menu_window, text="Выберите действие:", 
             font=("Arial", 11), bg="white").pack(pady=10)
    
    tk.Button(menu_window, text="Начать тренировку", command=start_training,
              bg="#0066CC", fg="white", font=("Arial", 11), width=20, height=2).pack(pady=5)
    
    tk.Button(menu_window, text="Статистика", command=show_stats,
              bg="#0066CC", fg="white", font=("Arial", 11), width=20, height=2).pack(pady=5)
    
    tk.Button(menu_window, text="Выход", command=exit_app,
              bg="#0066CC", fg="white", font=("Arial", 11), width=20, height=2).pack(pady=5)
    
    menu_window.protocol("WM_DELETE_WINDOW", exit_app)
    menu_window.mainloop()

def generate_example():
    """Генерация нового примера"""
    global current_a, current_b, correct_answer
    current_a = random.randint(2, 9)
    current_b = random.randint(2, 9)
    correct_answer = current_a * current_b
    label_example.config(text=f"{current_a} × {current_b} = ?")

def check_answer():
    """Проверка ответа"""
    user_input = entry_answer.get().strip()
    
    if user_input == "":
        messagebox.showwarning("Внимание", "Введите ответ!")
        return
    try:
        user_answer = int(user_input)
    except ValueError:
        messagebox.showerror("Ошибка", "Введите число, а не буквы")
        log_action(f"{current_a}×{current_b}", user_input, "Ошибка ввода")
        entry_answer.delete(0, tk.END)
        entry_answer.focus()
        return

    if user_answer == correct_answer:
        log_action(f"{current_a}×{current_b}", user_answer, "Верно")
        messagebox.showinfo("Правильно", f"{current_a} × {current_b} = {correct_answer}")
        entry_answer.delete(0, tk.END)
        generate_example()
    else:
        log_action(f"{current_a}×{current_b}", user_answer, "Ошибка")
        messagebox.showerror("Неверно", f"Попробуйте еще раз")
        entry_answer.delete(0, tk.END)
        entry_answer.focus()

def start_training():
    """Запуск тренировки"""
    menu_window.destroy()
    
    global train_window, label_example, entry_answer
    train_window = tk.Tk()
    train_window.title("Тренировка")
    train_window.geometry("400x300")
    train_window.configure(bg="white")
    
    tk.Label(train_window, text="Решите пример:", 
             font=("Arial", 12), bg="white", fg="#0066CC").pack(pady=10)
    
    label_example = tk.Label(train_window, text="", 
                             font=("Arial", 28, "bold"), bg="white", fg="#0066CC")
    label_example.pack(pady=20)
    
    entry_answer = tk.Entry(train_window, width=10, font=("Arial", 14), 
                            justify="center")
    entry_answer.pack(pady=10)
    entry_answer.focus()
    entry_answer.bind('<Return>', lambda event: check_answer())

    tk.Button(train_window, text="Проверить", command=check_answer,
              bg="#0066CC", fg="white", font=("Arial", 11), width=15).pack(pady=10)
    
    frame = tk.Frame(train_window, bg="white")
    frame.pack(pady=20)
    
    tk.Button(frame, text="Новый пример", command=generate_example,
              bg="#0066CC", fg="white", font=("Arial", 10), width=12).pack(side=tk.LEFT, padx=5)
    
    tk.Button(frame, text="Статистика", command=show_stats_from_train,
              bg="#0066CC", fg="white", font=("Arial", 10), width=12).pack(side=tk.LEFT, padx=5)
    
    tk.Button(frame, text="В меню", command=back_to_menu,
              bg="#0066CC", fg="white", font=("Arial", 10), width=12).pack(side=tk.LEFT, padx=5)
    
    generate_example()
    
    train_window.protocol("WM_DELETE_WINDOW", back_to_menu)
    train_window.mainloop()

def show_stats():
    """Статистика из меню"""
    show_stats_window(menu_window)

def show_stats_from_train():
    """Статистика из тренировки"""
    show_stats_window(train_window)

def show_stats_window(parent):
    """Окно статистики"""
    stats_window = tk.Toplevel(parent)
    stats_window.title("Статистика")
    stats_window.geometry("600x400")
    stats_window.configure(bg="white")
    
    tk.Label(stats_window, text="История тренировок", 
             font=("Arial", 14, "bold"), bg="white", fg="#0066CC").pack(pady=10)
    
    text_frame = tk.Frame(stats_window)
    text_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    scrollbar = tk.Scrollbar(text_frame)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    text_widget = tk.Text(text_frame, yscrollcommand=scrollbar.set, 
                          font=("Courier", 10), bg="#F0F8FF")
    text_widget.pack(fill=tk.BOTH, expand=True)
    
    scrollbar.config(command=text_widget.yview)
    
    try:
        with open(log_file, 'r', encoding='utf-8') as f:
            text_widget.insert(tk.END, f.read())
    except:
        text_widget.insert(tk.END, "Файл статистики не найден")
    
    text_widget.config(state=tk.DISABLED)

    tk.Button(stats_window, text="Обновить", 
              command=lambda: refresh_stats(text_widget),
              bg="#0066CC", fg="white", font=("Arial", 10)).pack(pady=5)

def refresh_stats(text_widget):
    """Обновление статистики"""
    text_widget.config(state=tk.NORMAL)
    text_widget.delete(1.0, tk.END)
    try:
        with open(log_file, 'r', encoding='utf-8') as f:
            text_widget.insert(tk.END, f.read())
    except:
        text_widget.insert(tk.END, "Файл статистики не найден")
    text_widget.config(state=tk.DISABLED)

def back_to_menu():
    """Возврат в меню"""
    train_window.destroy()
    show_menu()

def exit_app():
    """Выход из приложения"""
    if messagebox.askyesno("Выход", "Завершить работу?"):
        log_action("Выход", "-", "Завершение")
        if 'menu_window' in globals():
            menu_window.quit()
            menu_window.destroy()
        if 'train_window' in globals():
            train_window.quit()
            train_window.destroy()

def login():
    """Обработка входа"""
    global student_name
    name = entry_name.get().strip()
    if name == "":
        messagebox.showerror("Ошибка", "Введите ФИО")
        return
    student_name = name
    log_action("Вход", "-", "Успешно")
    root.destroy()
    show_menu() 
root = tk.Tk()
root.title("Вход")
root.geometry("400x200")
root.configure(bg="white")

tk.Label(root, text="Тренажер таблицы умножения", 
         font=("Arial", 14, "bold"), bg="white", fg="#0066CC").pack(pady=20)

tk.Label(root, text="Введите ФИО:", bg="white", font=("Arial", 10)).pack()

entry_name = tk.Entry(root, width=30, font=("Arial", 10))
entry_name.pack(pady=10)
entry_name.focus()
entry_name.bind('<Return>', lambda event: login())

tk.Button(root, text="Войти", command=login, 
          bg="#0066CC", fg="white", font=("Arial", 10), width=15).pack(pady=10)

root.mainloop()
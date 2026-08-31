import tkinter as tk
from tkinter import messagebox
from sympy import symbols, sympify, diff, solve


# Переменные SymPy
x = symbols("x")
y = symbols("y")


def calculate():
    try:
        # Получаем данные из полей
        W = int(entry_W.get())
        L = int(entry_L.get())
        P = float(entry_P.get())
        InP = float(entry_InP.get())
        function_text = entry_function.get()

        # Проверка введённых данных
        if W < 0:
            raise ValueError("Богатство не может быть отрицательным.")

        if L < 0 or L > W:
            raise ValueError(
                f"Потери должны находиться в диапазоне от 0 до {W}."
            )

        if not 0 <= P <= 1:
            raise ValueError(
                "Вероятность должна находиться в диапазоне от 0 до 1."
            )

        if InP < 0:
            raise ValueError(
                "Цена страхового покрытия не может быть отрицательной."
            )

        if not function_text:
            raise ValueError("Введите функцию полезности.")

        # Создаём функцию полезности
        func = sympify(function_text)

        # Ожидаемая полезность
        EU = (
            P * func.subs(x, W - L + y - InP * y)
            + (1 - P) * func.subs(x, W - InP * y)
        )

        # Значения при y = 0 и y = L
        EU_0 = EU.subs(y, 0).evalf()
        EU_L = EU.subs(y, L).evalf()

        # Производная
        dEU = diff(EU, y)

        # Критические точки
        try:
            critical_points = solve(dEU, y)
        except Exception:
            critical_points = []

        # Кандидаты на максимум
        candidates = [0, L]

        for point in critical_points:
            try:
                point_float = float(point.evalf())

                if 0 <= point_float <= L:
                    candidates.append(point)

            except (TypeError, ValueError):
                continue

        # Ищем максимум
        best_y = None
        best_EU = None

        for point in candidates:
            try:
                value = EU.subs(y, point).evalf()

                # Отбрасываем комплексные значения
                if not value.is_real:
                    continue

                value = float(value)

                if best_EU is None or value > best_EU:
                    best_EU = value
                    best_y = point

            except Exception:
                continue

        # Если допустимого решения нет
        if best_y is None:
            messagebox.showerror(
                "Ошибка",
                "Не удалось найти допустимое значение y."
            )
            return

        # Формируем результат
        result = (
            f"Функция полезности:\n"
            f"U(x) = {func}\n\n"

            f"Ожидаемая полезность:\n"
            f"EU(y) = {EU}\n\n"

            f"EU(0) = {EU_0}\n"
            f"EU(L) = {EU_L}\n\n"

            f"Производная:\n"
            f"EU'(y) = {dEU}\n\n"

            f"Критические точки:\n"
            f"{critical_points}\n\n"

            f"Оптимальное страховое покрытие:\n"
            f"y* = {best_y}\n\n"

            f"Максимальная ожидаемая полезность:\n"
            f"EU(y*) = {best_EU}"
        )

        show_result(result)

    except ValueError as error:
        messagebox.showerror("Ошибка ввода", str(error))

    except Exception as error:
        messagebox.showerror(
            "Ошибка",
            f"Не удалось выполнить расчёт:\n\n{error}"
        )


def show_result(result):
    # Окно результатов
    result_window = tk.Toplevel(root)
    result_window.title("Результат")
    result_window.geometry("750x550")
    result_window.resizable(True, True)

    text = tk.Text(
        result_window,
        font=("Consolas", 11),
        wrap="word"
    )
    text.pack(
        fill="both",
        expand=True,
        padx=15,
        pady=15
    )

    text.insert("1.0", result)
    text.config(state="disabled")


# ==============================
# ОСНОВНОЕ ОКНО
# ==============================

root = tk.Tk()
root.title("Модель страхования")
root.geometry("600x450")
root.resizable(False, False)


# Заголовок
title = tk.Label(
    root,
    text="Модель страхования",
    font=("Arial", 20, "bold")
)
title.pack(pady=20)


# Контейнер для полей
frame = tk.Frame(root)
frame.pack()


# Богатство
tk.Label(
    frame,
    text="Богатство W:",
    font=("Arial", 11)
).grid(row=0, column=0, sticky="w", pady=8)

entry_W = tk.Entry(
    frame,
    width=30,
    font=("Arial", 11)
)
entry_W.grid(row=0, column=1, padx=15, pady=8)


# Потери
tk.Label(
    frame,
    text="Потери L:",
    font=("Arial", 11)
).grid(row=1, column=0, sticky="w", pady=8)

entry_L = tk.Entry(
    frame,
    width=30,
    font=("Arial", 11)
)
entry_L.grid(row=1, column=1, padx=15, pady=8)


# Вероятность
tk.Label(
    frame,
    text="Вероятность P:",
    font=("Arial", 11)
).grid(row=2, column=0, sticky="w", pady=8)

entry_P = tk.Entry(
    frame,
    width=30,
    font=("Arial", 11)
)
entry_P.grid(row=2, column=1, padx=15, pady=8)


# Цена страхования
tk.Label(
    frame,
    text="Цена покрытия:",
    font=("Arial", 11)
).grid(row=3, column=0, sticky="w", pady=8)

entry_InP = tk.Entry(
    frame,
    width=30,
    font=("Arial", 11)
)
entry_InP.grid(row=3, column=1, padx=15, pady=8)


# Функция полезности
tk.Label(
    frame,
    text="Функция U(x):",
    font=("Arial", 11)
).grid(row=4, column=0, sticky="w", pady=8)

entry_function = tk.Entry(
    frame,
    width=30,
    font=("Arial", 11)
)
entry_function.grid(row=4, column=1, padx=15, pady=8)


# Подсказка
tk.Label(
    root,
    text="Примеры:  log(x)    sqrt(x)    x**0.5    x**2",
    font=("Arial", 9),
    fg="gray"
).pack(pady=10)


# Кнопка
calculate_button = tk.Button(
    root,
    text="Рассчитать",
    command=calculate,
    font=("Arial", 12, "bold"),
    width=20,
    height=2
)
calculate_button.pack(pady=20)


# Запуск
root.mainloop()
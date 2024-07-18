LOW = "1"
MEDIUM = "2"
HIGH = "3"
PRIORITY = {LOW: "низкий", MEDIUM: "средний", HIGH: "высокий"}

NEW = "1"
IN_PROGRESS = "2"
DONE = "3"
STATUS = {NEW: "новая", IN_PROGRESS: "в процессе", DONE: "завершена"}

tasks = {}
data_file = "tasks.txt"


def load_tasks():
    global tasks
    tasks = {}
    try:
        with open(data_file, "r", encoding="utf-8") as file:
            for line in file:
                task_id, title, description, priority, status = line.strip().split("|")
                tasks[task_id] = {
                    "title": title,
                    "description": description,
                    "priority": priority,
                    "status": status,
                }
    except FileNotFoundError:
        tasks = {}


def save_tasks():
    with open(data_file, "w", encoding="utf-8") as file:
        for task_id, task in tasks.items():
            line = f"{task_id}|{task['title']}|{task['description']}|{task['priority']}|{task['status']}\n"
            file.write(line)


def generate_id():
    return str(max([int(k) for k in tasks.keys()] + [0]) + 1)


def create_task():
    title = input("Введите название задачи: ")
    description = input("Введите описание задачи: ")

    while True:
        priority = input("Выберите приоритет (1 - низкий, 2 - средний, 3 - высокий): ")
        if priority in PRIORITY:
            break
        print("Некорректный ввод. Пожалуйста, введите 1, 2 или 3.")

    while True:
        status = input("Выберите статус (1 - новая, 2 - в процессе, 3 - завершена): ")
        if status in STATUS:
            break
        print("Некорректный ввод. Пожалуйста, введите 1, 2 или 3.")

    task_id = generate_id()
    tasks[task_id] = {
        "title": title,
        "description": description,
        "priority": PRIORITY[priority],
        "status": STATUS[status],
    }
    save_tasks()
    print("Задача добавлена.")


def update_task():
    task_id = input("Введите ID задачи, которую хотите обновить: ")
    if task_id not in tasks:
        print("Задача с таким ID не найдена.")
        return

    print("Что вы хотите обновить?")
    print("1 - Название")
    print("2 - Описание")
    print("3 - Приоритет")
    print("4 - Статус")

    choice = input("Введите номер поля: ")
    if choice == "1":
        tasks[task_id]["title"] = input("Введите новое название: ")
    elif choice == "2":
        tasks[task_id]["description"] = input("Введите новое описание: ")
    elif choice == "3":
        while True:
            priority = input(
                "Выберите новый приоритет (1 - низкий, 2 - средний, 3 - высокий): "
            )
            if priority in PRIORITY:
                tasks[task_id]["priority"] = PRIORITY[priority]
                break
            print("Некорректный ввод. Пожалуйста, введите 1, 2 или 3.")
    elif choice == "4":
        while True:
            status = input(
                "Выберите новый статус (1 - новая, 2 - в процессе, 3 - завершена): "
            )
            if status in STATUS:
                tasks[task_id]["status"] = STATUS[status]
                break
            print("Некорректный ввод. Пожалуйста, введите 1, 2 или 3.")
    else:
        print("Некорректный выбор.")

    save_tasks()
    print("Задача обновлена.")


def delete_task():
    task_id = input("Введите ID задачи, которую хотите удалить: ")
    if task_id not in tasks:
        print("Задача с таким ID не найдена.")
        return

    del tasks[task_id]
    save_tasks()
    print("Задача удалена.")


def list_tasks():
    if not tasks:
        print("Нет задач для отображения.")
        return

    print("1 - Отобразить задачи в изначальном виде")
    print("2 - Отсортировать по статусу")
    print("3 - Отсортировать по приоритету")
    print("4 - Осуществить поиск по названию или описанию")

    choice = input("Введите номер действия: ")

    if choice == "1":
        sorted_tasks = tasks.items()
    elif choice == "2":
        sorted_tasks = sorted(
            tasks.items(), key=lambda x: list(STATUS.values()).index(x[1]["status"])
        )
    elif choice == "3":
        sorted_tasks = sorted(
            tasks.items(), key=lambda x: list(PRIORITY.values()).index(x[1]["priority"])
        )
    elif choice == "4":
        search_term = input("Введите строку для поиска: ").lower()
        sorted_tasks = filter(
            lambda x: search_term in x[1]["title"].lower()
            or search_term in x[1]["description"].lower(),
            tasks.items(),
        )
    else:
        print("Некорректный выбор.")
        return

    for task_id, task in sorted_tasks:
        print(f"ID: {task_id}")
        print(f"Название: {task['title']}")
        print(f"Описание: {task['description']}")
        print(f"Приоритет: {task['priority']}")
        print(f"Статус: {task['status']}")
        print()


def main_menu():
    load_tasks()

    while True:
        print("1 - Создать новую задачу")
        print("2 - Просмотреть задачи")
        print("3 - Обновить задачу")
        print("4 - Удалить задачу")
        print("0 - Выйти из программы")

        choice = input("Введите номер действия: ")
        if choice == "1":
            create_task()
        elif choice == "2":
            list_tasks()
        elif choice == "3":
            update_task()
        elif choice == "4":
            delete_task()
        elif choice == "0":
            break
        else:
            print("Некорректный ввод. Пожалуйста, введите 0, 1, 2, 3 или 4.")


main_menu()

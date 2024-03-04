import os
import shutil
from threading import Thread, Lock

lock = Lock()  # Створення об'єкту блокування

def process_file(file_path):
    _, file_extension = os.path.splitext(file_path)
    extension_folder = os.path.join(target_folder, file_extension[1:])
    
    # Блокування доступу до створення папки та переміщення файлу для уникнення конфліктів
    with lock:
        # Перевірка, чи папка існує перед спробою її створення
        if not os.path.exists(extension_folder):
            os.makedirs(extension_folder)

        # Перевірка, чи файл існує перед спробою перемістити його
        if not os.path.exists(os.path.join(extension_folder, os.path.basename(file_path))):
            shutil.move(file_path, extension_folder)

def process_directory(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            thread = Thread(target=process_file, args=(file_path,))
            thread.start()
            thread.join()  # Очікуємо завершення потока перед переходом до наступного файлу
        for dir in dirs:
            dir_path = os.path.join(root, dir)
            thread = Thread(target=process_directory, args=(dir_path,))
            thread.start()
            thread.join()  # Очікуємо завершення потока перед переходом до наступної папки

def remove_empty_directories(directory):
    for root, dirs, files in os.walk(directory, topdown=False):
        for dir in dirs:
            dir_path = os.path.join(root, dir)
            if not os.listdir(dir_path):  # Перевірка, чи папка порожня
                os.rmdir(dir_path)  # Видалення порожньої папки

# Введення шляху до цільової папки
target_folder = input("Введіть шлях до папки для обробки: ")

# Перевірка наявності папки за введеним шляхом
if not os.path.isdir(target_folder):
    print("Папку за вказаним шляхом не знайдено.")
else:
    # Обробка цільової папки
    process_directory(target_folder)
    # Видалення порожніх папок після обробки всіх файлів
    remove_empty_directories(target_folder)

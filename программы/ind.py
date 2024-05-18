import json
import os
import sys
from jsonschema import validate, ValidationError

def get_zodiac():
    """
    Запросить данные о списке
    """
    start = input("Ведите фамилию, имя ")
    finish = input("Введите знак Зодиака ")
    zodiac = (input("Введите дату рождения "))

    return {
        'start': start,
        'finish': finish,
        'zodiac': zodiac,
    }


def display_zodiac(zodiacs):
    """
    Отобразить список
    """
    if zodiacs:
        line = '+-{}-+-{}-+-{}-+-{}-+'.format(
            '-' * 4,
            '-' * 30,
            '-' * 20,
            '-' * 14
        )
        print(line)
        print(
            '| {:^4} | {:^30} | {:^20} | {:^14} |'.format(
                "№",
                "Фамилия, имя",
                "Знак Зодиака",
                "Дата рождения"
            )
        )
        print(line)

        for idx, worker in enumerate(zodiacs, 1):
            print(
                '| {:>4} | {:<30} | {:<20} | {:>14} |'.format(
                    idx,
                    worker.get('start', ''),
                    worker.get('finish', ''),
                    worker.get('zodiac', '')
                )
            )
        print(line)
    else:
        print("Список пуст")


def select_zodiacs(zodiacs, period):
    """
    Выбрать зодиак
    """
    result = []
    for employee in zodiacs:
        if employee.get('finish') == period:
            result.append(employee)

    return result


def save_zodiacs(file_name, staff):
    """
    Сохранить данные в файл JSON
    """
    with open(file_name, "w", encoding="utf-8") as fout:
        json.dump(staff, fout, ensure_ascii=False, indent=4)


def load_zodiacs(file_name=None):
    """
    Загрузить данные из файла JSON
    """
    if file_name is None:
        file_name = os.environ.get('data_individ.json')  # Get file name from environment variable

    if file_name is None:
        print("Файл не указан. Укажите имя файла или установите переменную окружения ZODIAC_FILE.", file=sys.stderr)
        return []

    schema = {
        "type": "array",
        "items": {
            "type": "object",
            "properties": {
                "start": {"type": "string"},
                "finish": {"type": "string"},
                "zodiac": {"type": "string"},
            },
            "required": [
                "start",
                "finish",
                "zodiac",
            ],
        },
    }
    # Открыть файл с заданным именем и прочитать его содержимое.
    with open(file_name, "r") as file_in:
        data = json.load(file_in)  # Прочитать данные из файла

    try:
        # Валидация
        validate(instance=data, schema=schema)
        print("JSON валиден по схеме.")
    except ValidationError as e:
        print(f"Ошибка валидации: {e.message}")

    return data  # Вернуть загруженные и проверенные данные


def main():
    """
    Главная функция программы
    """
    zodiacs = []

    while True:
        command = input(">>> ").lower()
        if command == 'exit':
            break

        elif command == 'add':
            zodiac = get_zodiac()
            zodiacs.append(zodiac)
            zodiacs.sort(key=lambda item: int(item.get('zodiac', '').split('.')[2]))

        elif command == 'list':
            display_zodiac(zodiacs)

        elif command.startswith('select'):
            parts = command.split(' ', maxsplit=1)
            period = parts[1].strip()  # Получаем название знака Зодиака
            selected = select_zodiacs(zodiacs, period)
            if selected:
                display_zodiac(selected)
            else:
                print("Нет людей с таким знаком Зодиака.")

        elif command.startswith("save "):
            parts = command.split(maxsplit=1)
            file_name = parts[1]
            save_zodiacs(file_name, zodiacs)

        elif command.startswith("load "):
            parts = command.split(maxsplit=1)
            file_name = parts[1]
            zodiacs = load_zodiacs(file_name)

        elif command == 'help':
            print("Список команд:\n")
            print("add - добавить знак зодиака;")
            print("list - вывести список;")
            print("select <список знаков зодиака> - запросить данные о зодиаке;")
            print("help - отобразить справку;")
            print("load - загрузить данные из файла;")
            print("save - сохранить данные в файл;")
            print("exit - завершить работу с программой.")
        else:
            print(f"Неизвестная команда {command}", file=sys.stderr)


if __name__ == '__main__':
    main()
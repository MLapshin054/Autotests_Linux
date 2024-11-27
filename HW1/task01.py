'''
Задание 1.

Условие:
Написать функцию на Python, которой передаются в качестве параметров команда и текст. Функция должна возвращать True,
если команда успешно выполнена и текст найден в её выводе и False в противном случае. Передаваться должна только одна
строка, разбиение вывода использовать не нужно.
'''

import subprocess


def check_command(command: str, text: str) -> bool:
    """
    Функция выполняет команду и проверяет, содержится ли текст в её выводе.
    :param command: echo Hello, world!
    :param text: Hello
    :return: True
    """
    try:
        result = subprocess.run(command, shell=True, text=True, stdout=subprocess.PIPE, encoding='UTF-8')
        if result.returncode == 0:
            return text in result.stdout
        else:
            return False
    except Exception as e:
        print(f'An error occurred: {e}')
        return False


if __name__ == '__main__':
    command = 'echo Hello, World!'
    text = 'Hello'
    print(check_command(command, text))

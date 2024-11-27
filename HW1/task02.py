'''
Задание 2.

Доработать функцию из предыдущего задания таким образом, чтобы у неё появился дополнительный режим работы,
в котором вывод разбивается на слова с удалением всех знаков пунктуации (их можно взять из списка string.punctuation
модуля string). В этом режиме должно проверяться наличие слова в выводе.
'''

import subprocess
import string


def check_command(command: str, text: str, mode: str = 'text') -> bool:
    """
    Функция выполняет команду и проверяет, содержится ли текст в её выводе.
    :param command: echo Hello, world!
    :param text: Hello
    :param mode: word
    :return: True
    """
    try:
        result = subprocess.run(command, shell=True, text=True, stdout=subprocess.PIPE, encoding='UTF-8')
        if result.returncode != 0:
            return False

        output = result.stdout
        if mode == 'word':
            words = output.translate(str.maketrans('', '', string.punctuation)).split()
            return text in words
        elif mode == 'text':
            return text in output

        raise ValueError('Invalid mode. Use "text" or "word".')

    except Exception as e:
        print(f'An error occurred: {e}')
        return False


if __name__ == '__main__':
    command = 'echo Hello, World!'
    text = 'World'
    mode = 'word'
    print(check_command(command, text, mode))

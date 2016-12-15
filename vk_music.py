import vk
import urllib.request
import os
import sys
from getpass import getpass

'Можно подсказывать какой твой id'

APP_ID = '5727039'


def get_user_login():
    return input('Введите ваш логин:')


def get_user_password():
    'Работает только в терминале\консоле'
    return getpass('Введите ваш пароль:')


def get_music(login, password, quantity, my_id):
    session = vk.AuthSession(
        app_id = APP_ID,
        user_login = login,
        user_password = password,
        scope = 'audio'
    )
    api = vk.API(session)
    audios = (api.audio.get(
        owner_id = my_id,
        count = quantity,
        version = '5.60' ))
    return audios


def get_folder(direction):
    if os.path.exists(direction):
        return direction
    else:
        return None


def get_answer():
    try:
        answer = int(input('Указанной папки не существует,создать ее?\n'\
                        '1-Yes, 0-No\n'))
        return answer
    except ValueError:
        return None


def create_folder(answer, exist_direction):
    if answer == 0:
        return 0
    elif answer == 1:
        try:
            os.makedirs(exist_direction)
            return True
        except TypeError:
            return 2
    else:
        return None
                

def download_music(audios, final_direction):
    p = 1
    Filenotfound_error = []
    file_exists = []
    while p != len(audios):
        name_of_song = '{}\\{}-{}.mp3'.format(final_direction, \
                audios[p]['title'], audios[p]['artist'])
        if not os.path.exists(name_of_song):
            try:
                urllib.request.urlretrieve(audios[p]['url'], name_of_song)
            except FileNotFoundError:
                Filenotfound_error.append(audios[p]['title'])
                pass
            except OSError:
                pass
        else:
            file_exists.append(audios[p]['title'])
        p+=1
    return Filenotfound_error, file_exists
        

if __name__ == '__main__':
    while True:
        login = get_user_login()
        password = get_user_password()
        try:
            quantity = int(input('Введите число последних аудиозаписей: '))
            my_id = int(input('Введите ваш id: '))
        except ValueError:
            print('Неправильно введено число аудиозаисей или id')
            break
        audios = get_music(login, password, quantity, my_id)
        direction = input('Укажите путь до папки, в которую будут сохраняться песни: ')
        exist_direction = get_folder(direction)
        if exist_direction is not None:
            Filenotfound_error, file_exists = download_music(audios, exist_direction)
        else:
            created_folder = create_folder(get_answer(), direction)
            if created_folder is None:
                print('Введено непраивльное число')
                break
            if created_folder == 0:
                break
            if created_folder == 2:
                print('Не удалось создать папку')
                break
            Filenotfound_error, file_exists = download_music(audios, direction)
        print('Файлы не скачались: "{}"'.format(Filenotfound_error))
        print('Файлы сущетсвуют: {}'.format(file_exists))
            
        break
    
    

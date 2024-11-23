import time
import os
import telebot
from dannye import tokenchik
bot = telebot.TeleBot(token=tokenchik)
RAM = [[0 for _ in range(16)] for _ in range(16)]
startprog = '00110001 01110101 00001111 11100110 01010001 11110010 10010000 11110111'
startprog = startprog.split(' ')
abchhh = []
A = 0
B = 0
N = 0
X = 0
Y = 0
output = 0
Z = 0
C = 0
PCL = 0
PCH = 0
PC = 0
try:
    os.mkdir('user_documents')
except FileExistsError:
    print(1)

commands = {
    '0000': 'ADD, A,Im',
    '00010000': 'MOV A,B',
    '0001': 'ADD A,B,N',
    '00100000': 'IN A',
    '0010': 'IN A+N',
    '0011': 'MOV A,Im',
    '01000000': 'MOV B,A',
    '0100': 'ADD B,A,N',
    '0101': 'ADD B,Im',
    '01100000': 'IN B',
    '0110': 'IN B+N',
    '0111': 'MOV B,Im',
    '10000000': 'ADD A,B',
    '10000001': 'NEG A',
    '10000010': 'NOT A',
    '10000011': 'OR A,B',
    '10000100': 'AND A,B',
    '10000101': 'XOR A,B',
    '10000110': 'SUB A,B',
    '10000111': 'OUT A',
    '10001000': 'LD A',
    '10001001': 'ST A',
    '10001010': 'LD B',
    '10001011': 'ST B',
    '10001100': 'MOV X,A',
    '10001101': 'MOV Y,A',
    '10001110': 'INC XY',
    '10001111': 'JMP XY',
    '10010000': 'OUT B',
    '1001': 'OUT B+N',
    '1010': 'JZ Im',
    '1011': 'OUT Im',
    '1100': 'MOV Y, Im',
    '1101': 'MOV X, Im',
    '1110': 'JNC Im',
    '1111': 'JMP Im'
}


def read_binfile():
    res = []
    with open('mainbytes.bin', 'rb') as file:
        binarydata = file.read()
        for byte in binarydata:
            res.append(bin(byte)[2:].zfill(8))
        return res


def read_binfile_user(username):
    res = []
    with open(f'user_documents/{username}.bin', 'rb') as file:
        binarydata = file.read()
        for byte in binarydata:
            res.append(bin(byte)[2:].zfill(8))
        return res


def write_binfile(array):
    with open('mainbytes.bin', 'wb') as file:
        for i in array:
            bindata = i.to_bytes(1, 'little')
            file.write(bindata)


def obrabotka(command, peremennaya=None):
    global A, B, X, Y, output, Z, C, PC, PCH, PCL
    if command == 'ADD, A,Im':
        if A + peremennaya > 15:
            A = (A + peremennaya) % 16
            C = 1
            if A == 0:
                Z = 1
        else:
            A += peremennaya
    elif command == 'MOV A,B':
        A = B
        C = 0
        Z = 0
    elif command == 'ADD A,B,N':
        if B + peremennaya > 15:
            A = (B + peremennaya) % 16
            C = 1
            if A == 0:
                Z = 1
        else:
            A = (B + peremennaya)
    elif command == 'IN A':
        C = 0
        Z = 0
        A = peremennaya
    elif command == 'IN A+N':
        if peremennaya + N > 15:
            A = (peremennaya + N) % 16
            C = 1
            if A == 0:
                Z = 1
        else:
            A = (peremennaya + N)
    elif command == 'MOV A,Im':
        A = peremennaya
        Z = 0
        C = 0
    elif command == 'MOV B,A':
        B = A
        Z = 0
        C = 0
    elif command == 'ADD B,A,N':
        B = A + N
        if B > 15:
            B = B % 16
            C = 1
            if B == 0:
                Z = 1
    elif command == 'ADD B,Im':
        B += peremennaya
        if B > 15:
            B = B % 16
            C = 1
            if B == 0:
                Z = 1
    elif command == 'IN B':
        B = peremennaya
        Z = 0
        C = 0
    elif command == 'IN B+N':
        B = peremennaya + N
        if B > 15:
            B = B % 16
            C = 1
            if B == 0:
                Z = 1
    elif command == 'MOV B, Im':
        B = peremennaya
        Z = 0
        C = 0
    elif command == 'ADD A,B':
        A += B
        if A > 15:
            A = A % 16
            C = 1
            if A == 0:
                Z = 1
    elif command == 'NEG A':
        A = 15 - A + 1
        if A == 0 or A == 16:
            A = 0
            Z = 1
    elif command == 'NOT A':
        tr = vyravnivaniye(A)
        tr = tr.replace('0', '2')
        tr = tr.replace('1', '0')
        tr = tr.replace('2', '1')
        A = int(tr, 2)
        if A == 0:
            Z = 1
        C = 0
    elif command == 'OR A,B':
        A = vyravnivaniye(A)
        B = vyravnivaniye(B)
        orab = ''
        for i in range(len(A)):
            if int(A[i]) >= int(B[i]):
                orab += A[i]
            else:
                orab += B[i]
        A = int(orab, 2)
        if A == 0:
            Z = 1
        C = 0
    elif command == 'AND A,B':
        A = vyravnivaniye(A)
        B = vyravnivaniye(B)
        anab = ''
        for i in range(len(A)):
            if int(A[i]) <= int(B[i]):
                anab += A[i]
            else:
                anab += B[i]
        A = int(anab, 2)
        if A == 0:
            Z = 1
        C = 0
    elif command == 'XOR A,B':
        C = 0
        A = vyravnivaniye(A)
        B = vyravnivaniye(B)
        xoab = ''
        for i in range(len(A)):
            if int(A[i]) == int(B[i]):
                xoab += '1'
            else:
                xoab += '0'
        A = int(xoab, 2)
        if A == 0:
            Z = 1
    elif command == 'SUB A,B':
        A = A - B
        if A < 0:
            A = A + 16
            C = 1
        if A == 0:
            Z = 1
    elif command == 'OUT A':
        output = A
        C = 0
        Z = 0
    elif command == 'LD A':
        A = int(str(RAM[X][Y]), 2)
        C = 0
        Z = 0
    elif command == 'ST A':
        RAM[X][Y] = vyravnivaniye(A)
        C = 0
        Z = 0
    elif command == 'LD B':
        B = int(str(RAM[X][Y]), 2)
        C = 0
        Z = 0
    elif command == 'ST B':
        RAM[X][Y] = vyravnivaniye(B)
        C = 0
        Z = 0
    elif command == 'MOV X,A':
        X = A
        C = 0
        Z = 0
    elif command == 'MOV Y,A':
        Y = A
        C = 0
        Z = 0
    elif command == 'INC XY':
        X += 1
        Y += 1
        C = 0
        Z = 0
    elif command == 'JMP XY':
        PC = int(vyravnivaniye(X) + vyravnivaniye(Y), 2)
        C = 0
        Z = 0
    elif command == 'OUT B':
        output = B
        C = 0
        Z = 0
    elif command == 'OUT B+N':
        output = B + N
        if output > 15:
            output = output % 16
            C = 1
        if output == 0:
            Z = 1
    elif command == 'JZ Im':
        if Z == 1:
            PCL = peremennaya
            PC = int(vyravnivaniye(PCH) + vyravnivaniye(PCL), 2)
        C = 0
        Z = 0
    elif command == 'OUT Im':
        output = peremennaya
        C = 0
        Z = 0
    elif command == 'MOV Y, Im':
        Y = peremennaya
        C = 0
        Z = 0
    elif command == 'MOV X, Im':
        X = peremennaya
        C = 0
        Z = 0
    elif command == 'JNC Im':
        if C == 0:
            PCL = peremennaya
            PC = int(vyravnivaniye(PCH) + vyravnivaniye(PCL), 2)
    elif command == 'JMP Im':
        PCL = peremennaya
        PC = int(vyravnivaniye(PCH) + vyravnivaniye(PCL), 2)
    return f"A = {A}, B = {B}, Out = {output}, N = {N}, X = {X}, Y = {Y}, PC = {PC}"


def vyravnivaniye(bin_numb):
    bin_numb = bin(bin_numb)[2:]
    while len(bin_numb) < 4:
        bin_numb = '0' + bin_numb
    return bin_numb


preres = read_binfile()
abchhh = []
for i in preres:
    if i in commands:
        abchhh.append(commands[i])
    else:
        abchhh.append([commands[i[:4]], int(i[4:], 2)])


@bot.message_handler(commands=['start'])
def welcomemsg(message):
    print(f'{message.chat.username} запускает бота впервые')
    bot.send_message(message.chat.id, 'Добро пожаловать в эмулятор td4m.\nЧтоб ознакомиться с командами, введите /help')


@bot.message_handler(commands=['help'])
def helpmessage(message):
    print(f'{message.chat.username} прописал команду /help')
    bot.send_message(message.chat.id, '/help - помощь по всем командам\n'
                                      '/start_td4_demo - запустить тд4 в демо-режиме\n'
                                      '/change_scr - задать бинарный файл для эмуляции\n'
                                      '/delete_scr - удаление бинарного скрипта для тд4м\n'
                                      '/start_td4m - запустить эмуляцию тд4\n'
                                      '/reset - сбросить все переменные')


@bot.message_handler(commands=['change_scr'])
def changescr(message):
    print(f'{message.chat.username} загружает скрипт')
    bot.send_message(message.chat.id, 'Пришлите сюда ваш bin файл в качестве документа.')
    @bot.message_handler(content_types=['document'])
    def changingscr(message):
        file_bin = bot.get_file(message.document.file_id)
        download_document = bot.download_file(file_bin.file_path)
        with open(f'user_documents/{message.chat.username}.bin', 'wb') as new_file:
            new_file.write(download_document)
        bot.send_message(message.chat.id, 'Документ сохранен')


@bot.message_handler(commands=['start_td4_demo'])
def start_td4(message):
    print(f'{message.chat.username} запускает тд4 демо')
    textbot = ''
    bot.send_message(message.chat.id, 'Идет запуск подгруженного скрипта. Если хотите поменять: введите /change_scr')
    for i in range(len(abchhh)):
        if len(abchhh[i]) > 2:
            textbot += f'{abchhh[i]}\n'
        else:
            textbot += f'{abchhh[i][0]} {vyravnivaniye(abchhh[i][1])}\n'
    print(abchhh)
    msg = bot.send_message(message.chat.id, textbot)
    for i in range(len(abchhh)):
        textbotforedit = textbot.split('\n')
        if len(abchhh[i]) > 2:
            textbotforedit[i] = textbotforedit[i] + f' ---  {obrabotka(command=abchhh[i])}'
        else:
            textbotforedit[i] = textbotforedit[i] + f' ---  {obrabotka(command=abchhh[i][0], peremennaya=abchhh[i][1])}'
        rezultat = ''
        for t in textbotforedit:
            rezultat += f'{t}\n'
        bot.edit_message_text(chat_id=message.chat.id, message_id=msg.message_id, text=rezultat)
        time.sleep(1)


@bot.message_handler(commands=['delete_scr'])
def deletebin(message):
    print(f'{message.chat.username} удаляет скрипт')
    msg = bot.send_message(message.chat.id, 'Файл удаляется.')
    try:
        os.remove(f'user_documents/{message.chat.username}.bin')
        time.sleep(1)
        bot.edit_message_text(chat_id=message.chat.id, message_id=msg.message_id, text='Файл удален.')
    except FileNotFoundError:
        bot.edit_message_text(chat_id=message.chat.id, message_id=msg.message_id, text='Ошибка удаления файла. Попробуйте сначала его установить /change_scr')


@bot.message_handler(commands=['reset'])
def reset(message):
    global A, B, X, Y, N, output, Z, C, PCL, PCH, PC
    A = 0
    B = 0
    X = 0
    Y = 0
    N = 0
    output = 0
    Z = 0
    C = 0
    PCL = 0
    PCH = 0
    PC = 0
    bot.send_message(message.chat.id, 'Переменные сброшены')


@bot.message_handler(commands=['start_td4m'])
def start_td4m(message):
    print(f'{message.chat.username} запускает тд4м')
    bot.send_message(message.chat.id, 'Выберите режим, в котором вы хотите исполнять код.\n'
                                      '/manual - ручной\n'
                                      '/auto - автоматический')

    @bot.message_handler(commands=['auto'])
    def automat(message):
        bot.delete_message(message.chat.id, message.message_id)
        bot.send_message(message.chat.id, 'Введите частоту Тд4м, рекомендуется не больше 5Гц.')

        @bot.message_handler(content_types=['text'])
        def chastota(message):
            try:
                ghz = float(message.text)
                ghz = 1 / ghz
                bot.send_message(message.chat.id, f'Была применена частота {message.text} Гц')
                time.sleep(0.5)
                try:
                    strttd4m = read_binfile_user(message.chat.username)
                    workingtd4m = []
                    for i in strttd4m:
                        if i in commands:
                            workingtd4m.append(commands[i])
                        else:
                            workingtd4m.append([commands[i[:4]], int(i[4:], 2)])
                    textbot = ''
                    bot.send_message(message.chat.id,'Идет запуск td4m с вашими настройками.')
                    time.sleep(0.5)
                    for i in range(len(workingtd4m)):
                        if len(workingtd4m[i]) > 2:
                            textbot += f'{workingtd4m[i]}\n'
                        else:
                            textbot += f'{workingtd4m[i][0]} {vyravnivaniye(workingtd4m[i][1])}\n'
                    msg = bot.send_message(message.chat.id, textbot)
                    for i in range(len(workingtd4m)):
                        textbotforedit = textbot.split('\n')
                        if len(workingtd4m[i]) > 2:
                            textbotforedit[i] = textbotforedit[i] + f' ---  {obrabotka(command=workingtd4m[i])}'
                        else:
                            textbotforedit[i] = textbotforedit[i] + f' ---  {obrabotka(command=workingtd4m[i][0], peremennaya=workingtd4m[i][1])}'
                        rezultat = ''
                        for t in textbotforedit:
                            rezultat += f'{t}\n'
                        bot.edit_message_text(chat_id=message.chat.id, message_id=msg.message_id, text=rezultat)
                        time.sleep(ghz)
                    time.sleep(0.5)
                    helpmessage(message)
                except FileNotFoundError:
                    bot.send_message(message.chat.id, 'Для начала нужно загрузить бинарный файл командой /change_scr')
            except ValueError:
                bot.send_message(message.chat.id, 'Введите заново команду и укажите число без лишних символов')

    @bot.message_handler(commands=['manual'])
    def manual_td4m(message):
        try:
            strttd4m = read_binfile_user(message.chat.username)
            workingtd4m = []
            for i in strttd4m:
                if i in commands:
                    workingtd4m.append(commands[i])
                else:
                    workingtd4m.append([commands[i[:4]], int(i[4:], 2)])
            textbot = ''
            bot.send_message(message.chat.id, 'Идет запуск td4m с вашими настройками.')
            for i in range(len(workingtd4m)):
                if len(workingtd4m[i]) > 2:
                    textbot += f'{workingtd4m[i]}\n'
                else:
                    textbot += f'{workingtd4m[i][0]} {vyravnivaniye(workingtd4m[i][1])}\n'
            msg = bot.send_message(message.chat.id, textbot)
            for i in range(len(workingtd4m)):
                textbotforedit = textbot.split('\n')
                if len(workingtd4m[i]) > 2:
                    textbotforedit[i] = textbotforedit[i] + f' ---  {obrabotka(command=workingtd4m[i])}'
                else:
                    textbotforedit[i] = textbotforedit[i] + f' ---  {obrabotka(command=workingtd4m[i][0], peremennaya=workingtd4m[i][1])}'
                rezultat = ''
                for t in textbotforedit:
                    rezultat += f'{t}\n'
                bot.edit_message_text(chat_id=message.chat.id, message_id=msg.message_id, text=rezultat)
                input()
        except FileNotFoundError:
            bot.send_message(message.chat.id, 'Для начала нужно загрузить бинарный файл командой /change_scr')


bot.polling(none_stop=True)
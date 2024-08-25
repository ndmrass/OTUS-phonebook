import csv

def input_to_bool(question='Введите 1 если да, 0 если нет: '):
    """
    Задает вопрос пользователю пока не будут введены 0 или 1, возвращает на основе ответа True или False
    """
    while True:
        u_input = input(question)
        if u_input == '1':
            return True
        elif u_input == '0':
            return False
        else:
            print('Некорректные данные')


def input_to_valid_int(leftborder, rightborder):
    """
    На основе левой и правой границы (включительно) зацикленно спрашивает у пользователя число, пока оно не удовлетворит
        условию. Возвращает введенный int.
    :param leftborder: int
    :param rightborder: int
    :return: int
    """
    while True:
        my_int = input('Введите номер пункта: ')
        if my_int.isdigit() and leftborder <= int(my_int) <= rightborder:
            my_int = int(my_int)
            return my_int
        else:
            print('\nВведенные данные не являются номером пункта.')


def edit_contact(contact_as_list):
    """
    Принимает информацию о контакте, зацикленно спрашивает у пользователя, какие данные он хочет изменить, изменяет
        данные пока пользователь не сохранит изменения или не отменит их.
    :param contact_as_list: list of str
    :return: list of str or False
    """
    contact_as_list = list(contact_as_list)
    while True:
        for n in range(6):
            print(f'\t{fields[n]}: {contact_as_list[n]}')
        for k in fields[6:]:
            print(f'\t{k}')
        chosen_field = input_to_valid_int(1, 8)
        if 1 <= chosen_field <= 6:
            contact_as_list[int(fields[chosen_field - 1][0]) - 1] = input(
                f'Введите {fields[chosen_field - 1][3:].lower()}: ')
        elif chosen_field == 7:
            print('\nПросмотрите введенные данные.')
            for place, info in enumerate(contact_as_list, start=1):
                print(f'\t{place}. {info}')
            if input_to_bool('Если вас все устраивает, введите 1, если хотите редактировать, введите 0: '):
                return contact_as_list
            else:
                continue
        elif chosen_field == 8:
            if input_to_bool('Вы действительно хотите выйти, не сохранив изменения? (1 если да, 0 если нет): '):
                return False


def pb_menu(menu: list):
    print('\nМеню:')
    for pos, name in enumerate(menu, start=1):
        print(f'\t{pos}. {name}')


def pb_find_contacts(string): #returns a list of contacts with the string, False if no matches
    """
    Находит все контакты, включающие string, возвращает список с ними или False если нет совпадений
    :param string:
    :return: list или False
    """
    with open(PATH, newline='', encoding='UTF-8') as my_phonebook:
        line_reader = csv.reader(my_phonebook, delimiter=';')
        valid_lines = []
        for line in line_reader:
            line_as_str = ''.join(line)
            if string.casefold() in line_as_str.casefold():
                valid_lines.append(line)
        return False if not valid_lines else valid_lines


def pb_get_contact():
    """
    Спрашивает у пользователя часть контакта, ищет все совпадения (с помощью pb_find_contacts()), выводит их, спрашивает
        какой именно нужен пользователю, возвращает один контакт.
    :return: list of str
    """
    contacts = pb_find_contacts(input('Введите имя/фамилию/номер/часть номера/ник/e-mail нужного вам контакта: '))
    contacts_len = len(contacts)
    if not contacts:
        return print('Контакт не найден')
    elif contacts_len == 1:
        index = 0
    else:
        print('Какой из контактов вам нужен? (введите номер пункта): ')
        print_formated(contacts)
        index = input_to_valid_int(1, int(contacts_len)) - 1
    return contacts[index]


def pb_create_contact(contact_data=('-', '-', '-', '-', '-', '-')):
    """
    Передает принятый контакт в функцию edit_contact(), если изменения были сохранены добавляет контакт в файл
    :param contact_data:
    :return:
    """
    new_contact = edit_contact(contact_data)
    if not new_contact:
        print('Изменения не сохранены')
    else:
        with open(PATH, 'a', newline='', encoding='UTF-8') as my_phonebook:
            csv_writer = csv.writer(my_phonebook, delimiter=';')
            csv_writer.writerow(new_contact)


def pb_delete_contact():
    """
    Получает от пользователя информацию о нужном контакте через pb_get_contact(), читает все контакты из файла в список,
    удаляет переданный пользователем контакт из списка, убирает из списка пустые списки, переписывает файл на основе списка
    :return: False если пользователь не подтвердил удаление контакта
    """
    contact_to_delete = pb_get_contact()
    with open(PATH, 'r', encoding='UTF-8', newline='') as my_phonebook:
        csv_reader = csv.reader(my_phonebook, delimiter=';')
        contacts = []
        for line in csv_reader:
            contacts.append(line)
    print_formated([contact_to_delete, ])
    if not input_to_bool('Вы действительно хотите удалить данный контакт? (введите 1 если да, 0 если нет): '):
        return False
    index = contacts.index(contact_to_delete)
    contacts.pop(index)
    contacts = [i for i in contacts if i]
    with open(PATH, 'w', encoding='UTF-8', newline='') as my_phonebook:
        csv_writer = csv.writer(my_phonebook, delimiter=';')
        for i in contacts:
            csv_writer.writerow(i)
    print('\nКонтакт удален.')


def print_formated(list_of_contacts):
    """
    Печатает отформатированный список контактов, переданных в функцию.
    """
    print('*' * 110)
    for place, i in enumerate(list_of_contacts, start=1):
        print(f'\t{place}. {i[0]:.<12}{i[1]:.<15}{i[2]:.<15}{i[3]:.<25}{i[4]:.<18}{i[5]}')
    print('*' * 110)


def pb_show_all():
    """
    Печатает все контакты в справочнике, сначала прочитав их из файла, а затем передав их в функцию print_formated()
    """
    with open(PATH, 'r', encoding='UTF-8') as my_phonebook:
        csv_reader = csv.reader(my_phonebook, delimiter=';')
        contacts = []
        for line in csv_reader:
            contacts.append(line)
        print_formated(contacts)


def pb_edit_contact():
    """
    С помощью pb_get_contact() и edit_contact() узнает у пользователя нужный контакт и изменяет его, сохранив контакт
        до и после изменения в разные переменные. Считывает все контакты из справочника в список, удаляет из списка
        контакт, совпадающий с переменной "contact_to_edit", и добавляет контакт из переменной "edited_contact".
        Удаляет пустые списки из списка, записывает список в файл сsv.
    """
    contact_to_edit = pb_get_contact()
    edited_contact = edit_contact(contact_to_edit)
    with open(PATH, 'r', encoding='UTF-8', newline='') as my_phonebook:
        csv_reader = csv.reader(my_phonebook, delimiter=';')
        contacts = []
        for line in csv_reader:
            contacts.append(line)
    if edited_contact:
        contacts.pop(contacts.index(contact_to_edit))
        contacts.append(edited_contact)
        contacts = [i for i in contacts if i]
    with open(PATH, 'w', encoding='UTF-8', newline='') as my_phonebook:
        csv_writer = csv.writer(my_phonebook, delimiter=';')
        for i in contacts:
            csv_writer.writerow(i)


my_menu = [
    'Найти информацию о контакте',
    'Создать новый контакт',
    'Удалить контакт',
    'Редактировать контакт',
    'Показать все контакты',
    'Выйти'
]

fields = [
    '1. Имя',
    '2. Фамилия',
    '3. Телефон',
    '4. Email',
    '5. Ник в телеграме',
    '6. Комментарий',
    '7. Закончить редактирование и сохранить',
    '8. Выйти без сохранения контакта'
    ]

PATH = 'phonebook.csv'

while True:
    pb_menu(my_menu)
    a = input_to_valid_int(1, 6)
    if a == 1: # done
        fit_contacts = pb_find_contacts(input('Введите имя/фамилию/номер/часть номера/ник/e-mail: '))
        if not fit_contacts:
            print('Совпадений не найдено')
        else:
            print_formated(fit_contacts)
    elif a == 2: # done
        pb_create_contact()
    elif a == 3: # done
        a = pb_delete_contact()
        if not a:
            continue
    elif a == 4:
        pb_edit_contact()
    elif a == 5: # done
        pb_show_all()
    elif a == 6: # done
        break

from collections import UserDict
from datetime import datetime, timedelta


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record


class Record:
    def __init__(self, new_name, birthday=None):
        self.name = Name(new_name)
        self.phones = []
        self.birthday = ''

    def add_phone(self, new_phone):
        if not Phone.is_phone_valid(new_phone):
            print('not valid phone')
            return
        self.phones.append(Phone(new_phone))

    def change_phone(self, old_phone, new_phone):
        if not Phone.is_phone_valid(new_phone):
            print('not valid phone')
            return
        for phone in self.phones:
            if phone.value == old_phone:
                self.phones.append(Phone(new_phone))
                self.phones.remove(phone)
            else:
                print('Cant find this phone number')

    def remove_phone(self, old_phone):
        for phone in self.phones:
            if phone.value == old_phone:
                self.phones.remove(phone)
            else:
                print('cant find this phone number')

    def add_birthday(self, birthday):
        '''birthday = year.month.day'''
        if not Birthday.is_birthday_valid(birthday):
            print('not valid birthday')
            return
        self.birthday = Birthday(birthday)

    def days_to_birthday(self):
        if self.birthday:
            today = datetime.now().date()
            if self.birthday._value.replace(year=today.year) >= today:
                result = self.birthday._value.replace(
                    year=today.year) - today
            else:
                result = self.birthday._value.replace(
                    year=today.year) - today.replace(year=today.year - 1)
            print(result)
        else:
            print('empty')

    def __repr__(self):
        return f'{self.phones}'


class Field:
    def __init__(self):
        self._value = ''

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value


class Name(Field):
    def __init__(self, name):
        self.value = name


class Phone(Field):
    def __init__(self, phone):
        self._value = phone

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, phone):
        self._value = phone

    @classmethod
    def is_phone_valid(cls, value):
        return 10 <= len(value) <= 12

    def __repr__(self):
        return self._value


class Birthday(Field):
    def __init__(self, date: str):
        '''date = year.month.day'''
        self._value = datetime.strptime(date, '%Y.%m.%d').date()

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, birthday):
        self._value = datetime.strptime(birthday, '%Y.%m.%d').date()

    @classmethod
    def is_birthday_valid(cls, value):
        return 0 < int(value.split('.')[0]) <= datetime.now().date().year and 0 < int(value.split('.')[1]) <= 12 and 0 < int(value.split('.')[2]) <= 31

    def __repr__(self):
        return self._value


addressbook = AddressBook()


def input_error(funk):
    def inner(text_input=None):
        try:
            if len(text_input.split()) > 3:
                print('to many parameters')
                return
            if len(text_input.split()) == 3:
                text_input.split()[1] == str(text_input.split()[1])
                text_input.split()[2] == int(text_input.split()[2])
            return funk(text_input)
        except (AttributeError, IndexError, ValueError, KeyError):
            print('Enter name or phone correctly')
    return inner


def hello(_=None):
    print('How can I help you?')


def show_all(_=None):
    print(addressbook.data)


@ input_error
def add(text_input: str):
    if text_input.split()[1] not in addressbook.data:
        adding = Record(text_input.split()[1])
        adding.add_phone(text_input.split()[2])
        addressbook.add_record(adding)
        print('.')
    else:
        adder = addressbook.data[text_input.split()[1]]
        adder.add_phone(text_input.split()[2])
        print('Done')


@ input_error
def change(text_input: str):
    if text_input.split()[1] in addressbook.data:
        old_phone = input('enter phone number to change  ')
        changing = addressbook.data[text_input.split()[1]]
        changing.change_phone(old_phone, text_input.split()[2])
        print('.')
    else:
        print('no contact')


@ input_error
def delete_contact(text_input: str):
    if text_input.split()[1] in addressbook.data:
        addressbook.data.pop(text_input.split()[1])
        print('Done')


@ input_error
def remove_phone(text_input: str):
    if text_input.split()[1] in addressbook.data:
        removing = addressbook.data[text_input.split()[1]]
        removing.remove_phone(text_input.split()[2])
        print('Done')


@ input_error
def phone(text_input: str):
    if text_input.split()[1] in addressbook.data:
        print(addressbook.data[text_input.split()[1]])
    else:
        print('This contact doesnt exist')


def set_birthday(text_input: str):
    if text_input.split()[1] in addressbook.data:
        setting = addressbook.data[text_input.split()[1]]
        setting.add_birthday(text_input.split()[2])
        print('done')


def show_birthday(text_input: str):
    birthding = addressbook.data[text_input.split()[1]]
    birthding.days_to_birthday()


USER_INPUT = {
    'hello': hello,
    'add': add,
    'change': change,
    'phone': phone,
    'show all': show_all,
    'delete': delete_contact,
    'remove': remove_phone,
    'set_birthday': set_birthday,
    'birthday': show_birthday
}


def main():
    while True:
        user_input = input('Enter something  ')
        user_input = user_input.lower()
        if user_input == '.':
            break
        if user_input == 'good bye' or user_input == 'close' or user_input == 'exit':
            print('Good bye!')
            break
        if user_input in USER_INPUT:
            USER_INPUT[user_input]()
        elif user_input.split()[0] in USER_INPUT:
            USER_INPUT[user_input.split()[0]](user_input)


main()

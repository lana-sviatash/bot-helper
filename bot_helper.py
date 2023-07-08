import difflib
import functools
import os

from accessary import welcome_message, hello_instruction, parser_input
from contact_manager import AddressBook, Record, Name, Phone, PhoneError


address_book = AddressBook()


def load_contacts_from_file():
    if os.path.exists('contacts.txt'):
        with open('contacts.txt', 'r') as file:
            for line in file:
                line = line.strip()
                if line:
                    name, phones = line.split(':')
                    record = Record(Name(name.strip()))
                    for phone in phones.strip().split(','):
                            phone = Phone(phone.strip())
                            record.add_phone(phone)
                    address_book.add_record(record)


def input_errors(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (TypeError, KeyError, ValueError, IndexError) as e:
            error_message = str(e).split(':')[1]
            return f"Give me {error_message}"
    return wrapper


@input_errors
def adding_contact(name: str, phone: str, *args):
    name = Name(name.capitalize())
    
    try:
        name.check_name(name.value)
    except NameError as e:
        return e
    
    phone = Phone(phone)
    try:
        phone.check_phone(phone.value)
    except PhoneError as e:
        return e
    
    if name.value in address_book.data:
        return f"A record with the name '{name.value}' already exists."
    
    record = Record(name, phone.check_phone(phone.value))
    address_book.add_record(record)
    save_contacts_to_file()
    return 'Contact added successfully'


@input_errors
def changing_contact(name: str, phone: str, *args):
    name = Name(name.capitalize())
    phone = Phone(phone)
    if name.value in address_book.data:
        try:
            phone.check_phone(phone.value)
        except PhoneError as e:
            return e
        record = Record(name, phone.check_phone(phone.value))
        address_book.add_record(record)
        save_contacts_to_file()
        return 'Contact changed successfully'
    else:
        return f'Contact {name} does not exist'



def save_contacts_to_file(*args):
    with open("contacts.txt", "w") as file:
        for name, record in address_book.data.items():
                phones = ", ".join(str(phone) for phone in record.phones)
                file.write(f"{name}: {phones}\n")


@input_errors
def phone(name: str, *args):
    name = Name(name.capitalize())
    record = address_book.data.get(name.value)
    if record is not None:
        return str(record)
    else:
        return 'Contact not found'


def show_contacts(*args):
    if not address_book:
        return 'No contacts'
    return address_book.show_records()


@input_errors
def delete_contact(name: str, *args):
    name = Name(name.capitalize())
    record = Record(name)
    try:
        address_book.delete_record(record)
        save_contacts_to_file()
        return 'Contact deleted successfully'
    except NameError as e:
        return str(e)


command_dict = {
    'add': [adding_contact, 'add contact'],
    'change': [changing_contact, 'change existing phone of the contact'],
    'phone': [phone, 'show phone of existing contact'],
    'show all': [show_contacts, 'show all contacts'],
    'del': [delete_contact, 'delete the contact']
}


def command_handler(user_input, command_dict):
    if user_input in command_dict:
        return command_dict[user_input][0]
    possible_command = difflib.get_close_matches(user_input.split()[0], command_dict, cutoff=0.6)
    if possible_command:
        return f'An unknown command. Maybe you mean: {", ".join(possible_command)}'
    else:
        return f'An unknown command.'


def main():
    print(welcome_message())

    if "contacts.txt":
        load_contacts_from_file()

    while True:
        user_input = input('>>> ').lower()
        if user_input == 'hello':
            print("How can I help you?\n")
            print(hello_instruction(command_dict))
        elif user_input in ('good bye', "close", "exit"):
            if os.path.exists("contacts.txt") and os.path.getsize("contacts.txt") == 0:
                os.remove("contacts.txt")
            print('Good bye!')
            break
        else:
            command, arguments = parser_input(user_input, command_dict)
            if command in command_dict:
                result = command_handler(command, command_dict)(*arguments)
            else:
                result = command_handler(user_input, command_dict)
            print(result)
        

if __name__ == "__main__":
    main()

import difflib
import functools
import os
import pickle

from accessary import welcome_message, hello_instruction, parser_input
from contact_manager import AddressBook, Record, Name, Phone, BirthDay, PhoneError, BirthDayError


address_book = AddressBook()


def save_contacts_to_file():
    with open('contacts.bin', 'wb') as file:
        pickle.dump(address_book, file)


def load_contacts_from_file():
    if os.path.exists('contacts.bin'):
        with open('contacts.bin', 'rb') as file:
            loaded_address_book = pickle.load(file)
            address_book.data = loaded_address_book.data
            return address_book


# Or Custom Serialization using txt:

# def load_contacts_from_file():
#     if os.path.exists('contacts.txt'):
#         with open('contacts.txt', 'r') as file:
#             for line in file:
#                 line = line.strip()
#                 if line:
#                     name, phones, birthday = line.split('|')
#                     record = Record(Name(name.strip()))
#                     if phones != 'No records':
#                         for phone in phones.replace('Phones:', '').strip().split(','):
#                                 phone = Phone(phone.strip())
#                                 record.add_phone(phone)
#                     if birthday.replace('Birthday:', '').strip():
#                         record.birthday = BirthDay((birthday.replace('Birthday:', '')).strip())
#                     address_book.add_record(record)


# def save_contacts_to_file():
#     with open("contacts.txt", "w") as file:
#             for record in address_book.values():
#                 phones = ', '.join(str(phone) for phone in record.phones)
#                 birthday = str(record.birthday.value) if record.birthday else ""
#                 file.write(f"{record.name.value} | Phones: {phones} | Birthday: {birthday}\n")


def input_errors(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (KeyError, ValueError, IndexError,TypeError) as e:
            if "takes" in str(e) and "but" in str(e):
                error_message = "Too many arguments provided"
                return error_message
            else:
                error_message = str(e).split(':')[1]
                return f"Give me {error_message}"
    return wrapper


@input_errors
def adding_contact(name: str, phone: str):
    name = Name(name.capitalize())
    
    try:
        phone = Phone(phone)
    except PhoneError as e:
        return str(e)
    
    if name.value in address_book.data:
        return f"A record with the name '{name.value}' already exists."
    
    record = Record(name, phone.value)
    address_book.add_record(record)
    save_contacts_to_file()
    return 'Contact added successfully'


@input_errors
def number(name: str, phone: str):
    name = Name(name.capitalize())

    try:
        phone = Phone(phone)
    except PhoneError as e:
        return str(e)
    
    if name.value in address_book.data:
        record:Record = address_book.data[name.value]
        if phone in record.phones:
            return f'phone number {phone} exists for contact {name.value}'
        else:
            record.add_phone(phone)
            save_contacts_to_file()
            return f'Phone number added successfully'


@input_errors
def changing_contact(name: str, old_phone: str, new_phone:str):
    name = Name(name.capitalize())
    
    if name.value in address_book.data:
        try:
            old_phone = Phone(old_phone)
            new_phone = Phone(new_phone)
        except PhoneError as e:
            return str(e)
        record:Record = address_book.data[name.value]
        record.change_phone(old_phone, new_phone)
        save_contacts_to_file()
        return 'Contact changed successfully'
    else:
        return f'Contact {name} does not exist'


@input_errors
def phone(name: str):
    name = Name(name.capitalize())
    record:Record = address_book.data.get(name.value)
    if record is not None:
        return f'{record.name}: {", ".join(phone for phone in record.phones)}'
    else:
        return 'Contact not found'


def show_contacts(*args):
    if not address_book:
        return 'No contacts'
    return address_book.print_part_records()


@input_errors
def find(text:str):
    finded_results = address_book.find_in_contacts(text)
    if not finded_results:
        return 'No matches found'
    for result in finded_results:
        if result.birthday:
            return f'{result.name.value}, {result.phones}, {result.birthday.value}'
        else:
            return f'{result.name.value}, {result.phones}'
    

@input_errors
def delete_contact(name: str):
    name = Name(name.capitalize())
    record = Record(name)
    if name.value in address_book.data:
        address_book.delete_record(record)
        save_contacts_to_file()
        return 'Contact deleted successfully'
    else:
        return f'Contact {name} does not exist'


@input_errors
def birthday(name:str, birthday:str):
    name = Name(name.capitalize())
    
    if name.value in address_book.data:
        try:
            b_day = BirthDay(birthday)
        except BirthDayError as e:
            return str(e)
        record:Record = address_book.data[name.value]
        record.birthday = b_day
        save_contacts_to_file()
        return 'Birthday added successfully'
    else:
        return f'Contact {name} does not exist'


@input_errors
def days_to_birthday(name: str):
    name:Name = Name(name.capitalize())
    
    if name.value in address_book.data:
        record = address_book.data[name.value]
        days = record.days_to_birthday()
        return f"Days to birthday for {name.value}: {days}" if days is not None else f"No birthday recorded for {name.value}"
    else:
        return f"Contact {name.value} does not exist"


command_dict = {
    'add': [adding_contact, 'add contact'],
    'number': [number, 'add another number to existing contact'],
    'change': [changing_contact, 'change existing phone of the contact'],
    'phone': [phone, 'show phone of existing contact'],
    'show all': [show_contacts, 'show all contacts'],
    'del': [delete_contact, 'delete the contact'],
    'birthday': [birthday, 'add birthday to existing contact'],
    'days': [days_to_birthday, 'how many days to birtday of the contact'],
    'find': [find, 'find in the address book']
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

    if os.path.exists("contacts.bin") and os.path.getsize("contacts.bin") > 0:
        load_contacts_from_file()

    while True:
        user_input = input('>>> ').lower()
        if user_input == 'hello':
            print("How can I help you?\n")
            print(hello_instruction(command_dict))
        elif user_input in ('good bye', "close", "exit"):
            if os.path.getsize("contacts.bin") > 0:
                address_book = load_contacts_from_file()
                if not address_book.data:
                    os.remove("contacts.bin")
            # For Custom Serialization using txt:
            # if os.path.exists("contacts.txt") and os.path.getsize("contacts.txt") == 0:
            #     os.remove("contacts.txt")
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

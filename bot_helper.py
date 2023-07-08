import difflib
import functools
import os
from contact_manager import *
from accessary import welcome_message, hello_instruction, parser_input


class Bot:
    def __init__(self):
        self.address_book = AddressBook()

    def load_contacts_from_file(self):
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
                        self.address_book.add_record(record)
        else:
            return self.address_book
        
    def save_contacts_to_file(self):
        with open("contacts.txt", "w") as file:
            for name, record in self.address_book.data.items():
                phones = ", ".join(str(phone) for phone in record.phones)
                file.write(f"{name}: {phones}\n")
    
    def input_errors(func):
        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            try:
                return func(self, *args, **kwargs)
            except (TypeError, KeyError, ValueError, IndexError) as e:
                error_message = str(e).split(':')[1]
                return f"Give me {error_message}"
        return wrapper

    @input_errors
    def adding_contact(self, name:str, phone=None):
        try:
            name = Name(name)
            name.check_name(name.value)
        except NameError as e:
            return e
        
        if phone:
            phone = Phone(phone)
            try:
                phone.check_phone(phone.value)
            except PhoneError as e:
                return e
            record = Record(name.check_name(name.value))
            record.add_phone(phone.check_phone(phone.value))
        else:
            record = Record(name.check_name(name.value))
        self.address_book.data[record.name] = record
        self.save_contacts_to_file()
        return 'Contact added successfully'
    
    @input_errors
    def adding_contact_phone(self, name: str, phone: str):
        name = Name(name.capitalize())
        try:
            name.check_name(name.value)
        except NameError as e:
            return e

        record = self.address_book.data.get(name.value)
        if record:
            try:
                phone = Phone(phone)
                phone.check_phone(phone.value)
            except PhoneError as e:
                return e
            
            existing_phones = [str(p)[-10:] for p in record.phones]
            new_phone = phone.check_phone(phone.value)[-10:]
            if new_phone in existing_phones:
                return f"The phone number {phone.value} already exists in the contact."
        
            record.add_phone(phone.check_phone(phone.value))
            self.save_contacts_to_file()
            return 'Phone added successfully'
        else:
            return f"No record found for {name.value}"

    @input_errors
    def changing_contact_name(self, old_name: str, new_name: str):
        old_name = Name(old_name.capitalize())
        try:
            old_name.check_name(old_name.value)
        except NameError as e:
            return e

        new_name = Name(new_name.capitalize())
        try:
            new_name.check_name(new_name.value)
        except NameError as e:
            return e

        old_record = self.address_book.data.get(old_name.value)
        if old_record:
            new_record = Record(new_name, phone=old_record.phones)
            try:
                self.address_book.change_record_name(old_record, new_record)
                old_record.name = new_name
                self.save_contacts_to_file()
                return 'Contact changed successfully'
            except NameError as e:
                return str(e)
        else:
            return f"No record found for {old_name.value}"

    @input_errors
    def changing_contact_phone(self, name: str, old_phone: str, new_phone: str):
        name = Name(name.capitalize())
        record = self.address_book.data.get(name.value)

        if record:
            try:
                old_phone = Phone(old_phone)
                old_phone.check_phone(old_phone.value)
                new_phone = Phone(new_phone)
                new_phone.check_phone(new_phone.value)
            except PhoneError as e:
                return e
            if record.change_phone(old_phone.check_phone(old_phone.value), new_phone.check_phone(new_phone.value)):
                self.save_contacts_to_file()
                return 'Phone changed successfully'
            else:
                return f"Phone number '{old_phone.check_phone(old_phone.value)}' not found in the record."
        else:
            return f"No record found for {name.value}"

    @input_errors
    def show_phone(self, name: str):
        name = Name(name.capitalize())
        record = self.address_book.data.get(name.value)
        if record:
            if record.phones:
                return f"The phone(s) for {record.name.value} are: {', '.join(str(phone) for phone in record.phones)}"
            else:
                return f"No phone numbers found for {record.name.value}"
        else:
            return f"No record found for {name.value}"

    @input_errors
    def show_contact(self, name: str):
        name = Name(name.capitalize())
        record = self.address_book.data.get(name.value)

        try:
            result = self.address_book.show_record(record)
            return result
        except NameError as e:
            return str(e)

    def show_book(self):
        return self.address_book.show_records()
        
    @input_errors
    def delete_contact(self, name: str):
        name = Name(name.capitalize())
        record = Record(name)
        try:
            self.address_book.delete_record(record)
            self.save_contacts_to_file()
            return 'Contact deleted successfully'
        except NameError as e:
            return str(e)

    @input_errors
    def delete_phone(self, name: str, phone: str):
        name = Name(name.capitalize())
        record = self.address_book.data.get(name.value)

        try:
            phone = Phone(phone)
            phone.check_phone(phone.value)
        except PhoneError as e:
            return e

        if record:
            phone_to_delete = phone.check_phone(phone.value)
            if record.del_phone(phone_to_delete):
                self.save_contacts_to_file()
                return f'Phone number {phone_to_delete} deleted successfully'
            else:
                return f'Phone number {phone_to_delete} not found in the record'
        else:
            return f'No record found for {name.value}'

    command_dict = {
        'add': [adding_contact, 'add contact name or name and phone'],
        'phone': [adding_contact_phone, 'add phone to existing contact'],
        'change name': [changing_contact_name, 'change existing name of the contact'],
        'change phone': [changing_contact_phone, 'change existing phone of the contact'],
        'show phone': [show_phone, 'show phone of existing contact'],
        'show contact': [show_contact, 'show existing contact'],
        'show book': [show_book, 'show all contacts'],
        'del contact': [delete_contact, 'delete the contact'],
        'del phone': [delete_phone, 'delete the phone of contact']
        }
    
    def command_handler(self, user_input, command_dict):
        if user_input in command_dict:
            return command_dict[user_input][0]
        possible_command = difflib.get_close_matches(user_input.split()[0], command_dict, cutoff=0.6)
        if possible_command:
            return f'An unknown command. Maybe you mean: {", ".join(possible_command)}'
        else:
            return f'An unknown command.'
    
    def main(self):
        print(welcome_message())
        self.load_contacts_from_file()

        while True:
            user_input = input('>>> ').lower()
            if user_input == 'hello':
                print("How can I help you?\n")
                print(hello_instruction(self.command_dict))
            elif user_input in ('good bye', "close", "exit"):
                if os.path.exists("contacts.txt") and os.path.getsize("contacts.txt") == 0:
                    os.remove("contacts.txt")
                print('Good bye!')
                break
            else:
                command, arguments = parser_input(user_input, self.command_dict)
                if command in self.command_dict:
                    result = self.command_handler(command, self.command_dict)(self, *arguments)
                else:
                    result = self.command_handler(user_input, self.command_dict)
                print(result)
    

if __name__ == "__main__":
    bot = Bot()
    bot.main()

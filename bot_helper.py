import difflib
import functools
import os

from accessary import welcome_message, hello_instruction, parser_input


contacts_dict = {}

def load_contacts_from_file():
    if os.path.exists('contacts.txt'):
        with open('contacts.txt', 'r') as file:
            for line in file:
                line = line.strip()
                if line:
                    name, phone = line.split(':')
                    contacts_dict[name.strip()] = phone.strip()

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
def adding_contact(name: str, phone: str):
    if phone.isnumeric() and len(phone) in range(10, 13):
        contacts_dict[name.capitalize()] = phone
        save_contacts_to_file()
        return 'Contact added successfully'
    else:
        return 'Phone number should have 10-12 numbers without space'


@input_errors
def changing_contact(name: str, phone: str):
    if phone.isnumeric() and len(phone) in range(10, 13):
        contacts_dict[name.capitalize()] = phone
        save_contacts_to_file()
        return 'Contact changed successfully'
    else:
        return 'Phone number should have 10-12 numbers without space'

def save_contacts_to_file():
    with open("contacts.txt", "w") as file:
        for name, phone in contacts_dict.items():
            file.write(f"{name}: {phone}\n")

@input_errors
def phone(name: str):
    if contacts_dict[name.capitalize()]:
        return contacts_dict[name.capitalize()]
    else:
        return 'Contact not found'

def show_contacts(*args):
    if not contacts_dict:
        return 'No contacts'
    
    contacts = ""
    for name, phone in contacts_dict.items():
        contact = f"{name}: {phone}"
        contacts += contact + "\n"
    return contacts.rstrip('\n')

@input_errors
def delete_contact(name: str):
    if name.capitalize() in contacts_dict:
        del contacts_dict[name.capitalize()]
        save_contacts_to_file()  # Save the updated contacts to file
        return f"Contact '{name.capitalize()}' deleted successfully."
    else:
        return f"Contact '{name.capitalize()}' not found."

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

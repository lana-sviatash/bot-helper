import difflib
import os


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
    def wrapper(*args, **kwargs):
        try:
            if func.__name__ in ['adding_contact', 'changing_contact']:
                name = args[0]
                phone = args[1] if len(args) > 1 else ""
                if len(name) == 0 or not phone.isdigit() or len(phone) not in [10, 11, 12]:
                    return 'Give me name and a CORRECT phone number (10-12 numbers)'
            elif func.__name__ in ['phone', 'delete_contact']:
                name = args[0] if len(args) > 0 else ""
                if len(name) == 0:
                    return 'Enter user name'
            return func(*args, **kwargs)
        except (TypeError, ValueError, IndexError):
            if func.__name__ in ['adding_contact', 'changing_contact']:
                return 'Give me name and phone please'
            elif func.__name__ == 'phone':
                return 'Enter user name'
    return wrapper

@input_errors
def adding_contact(name: str, phone: str):
    contacts_dict[name.capitalize()] = phone
    save_contacts_to_file()
    return 'Contact added successfully'

@input_errors
def changing_contact(name: str, phone: str):
    contacts_dict[name.capitalize()] = phone
    save_contacts_to_file()
    return 'Contact changed successfully'

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

def show_contacts():
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
    'add': adding_contact,
    'change': changing_contact,
    'phone': phone,
    'show all': show_contacts,
    'del': delete_contact
}

def command_parser_handler(user_input, command_dict):
    if user_input in command_dict:
        return command_dict[user_input]
    possible_command = difflib.get_close_matches(user_input, command_dict, cutoff=0.6)
    if possible_command:
        return f'An unknown command. Maybe you mean: {", ".join(possible_command)}'
    else:
        return f'An unknown command.'

def main():
    if "contacts.txt":
        load_contacts_from_file()

    while True:
        user_input = input('>>> ').lower()
        if user_input == 'hello':
            print("How can I help you?\n command:\n add <name> <phone> \n change <name> <phone> \n phone <name> \n show all \n del <name>" )
        elif user_input in ('good bye', "close", "exit"):
            if os.path.exists("contacts.txt") and os.path.getsize("contacts.txt") == 0:
                os.remove("contacts.txt")
            print('Good bye!')
            break
        else:
            user_command = user_input.split()
            if user_command:
                command = user_command[0]
                arguments = user_command[1:]
                if command == 'show' and arguments == ['all']:
                    result = command_parser_handler('show all', command_dict)()
                elif command in command_dict:
                    result = command_parser_handler(command, command_dict)(*arguments)
                else:
                    result = command_parser_handler(command, command_dict)
                print(result)
            else:
                print("Invalid command")
        

if __name__ == "__main__":
    main()

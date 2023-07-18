import inspect
import os

from contact_manager import AddressBook


def welcome_message():
    welcome_message = """
════════════════════════════════
hello ->                       
         to see list of commands
                                
exit, close, good bye ->       
                       to exit  
════════════════════════════════
    """
    return welcome_message


def hello_instruction (command_dict):
    result = []
    for func_name, func in command_dict.items():
        signature = inspect.signature(func[0])
        parameters = signature.parameters
        param_names = ' '.join(parameters.keys())

        if 'args' in parameters or 'kwargs' in parameters:
            result.append(f'{func_name} --> {func[1]}')
        else:
            result.append(f'{func_name} [{param_names}]--> {func[1]}')

    rows_command = ''
    for command in result:
        rows_command += command + '\n'
    return rows_command.strip('\n')


def parser_input(user_input: str, command_dict) -> tuple():
    command = None
    arguments = ''

    for key in command_dict.keys():
        if user_input.startswith(key):
            command = key
            arguments = user_input.replace(key, '').strip().split()
            break
    return command, arguments


def del_file_if_empty():
    if os.path.exists("contacts.bin") and os.path.getsize("contacts.bin") > 0:
        address_book = AddressBook.load_contacts_from_file()
        if not address_book.data:
            os.remove("contacts.bin")


if __name__=='__main__':
    # Check welcome_message
    print(welcome_message())

    # Check hello_instuction
    def adding_contact(name, phone):
        pass

    def show_contacts(*args):
        pass

    command_dict = {
    'add': [adding_contact, 'To add contact'],
    'show all': [show_contacts, 'To show all contacts']
    }

    print(hello_instruction(command_dict))

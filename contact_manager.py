from collections import UserDict


class PhoneError(Exception):
    pass


class NameError(Exception):
    pass


class Field:
    def __init__(self, value):
        self.value = value
        

class Name(Field):
    def check_name(self, name:str):
        if len(name) < 2:
            raise NameError('Name should have more then 1 char')
        if str(name).startswith(' '):
            raise NameError('Name should start with a letter')
        return name.capitalize()
    
    def __str__(self):
        return self.value


class Phone(Field):
    def __str__(self):
        return self.value
    
    def check_phone(self, phone):
        if phone.isnumeric() and len(phone) in range(10, 13):
            if len(phone) == 10:
                phone = '+38' + phone
            elif len(phone) == 11:
                phone = '+3' + phone
            elif len (phone) == 12:
                phone = '+' + phone
            return phone
        else:
            raise PhoneError('Phone number should have 10-12 numbers without space')
        

class Record:
    def __init__(self, name, phone:Phone=None):
        self.name = name
        self.phones = []
        if phone:
            self.phones.append(phone)
    
    def __str__(self):
        phone_numbers = ', '.join(str(phone) for phone in self.phones)
        return f'{self.name}: {phone_numbers}'

    def add_phone(self, phone:Phone):
        self.phones.append(phone)
    
    def del_phone(self, phone: Phone):
        phone_str = str(phone)
        for i, record_phone in enumerate(self.phones):
            if str(record_phone) == phone_str:
                self.phones.pop(i)
                return True
        return False

    def change_phone(self, old_phone:Phone, new_phone:Phone):
        old_phone_str = str(old_phone)
        new_phone_str = str(new_phone)
        for i, phone in enumerate(self.phones):
            if str(phone) == old_phone_str:
                self.phones[i] = new_phone_str
                return True
        return False

class AddressBook(UserDict):
    def add_record(self, record:Record):
        self.data[record.name.value] = record
    
    def delete_record(self, record:Record):
        if record.name.value in self.data:
            del self.data[record.name.value]
        else:
            raise NameError(f'Record with name {record.name.value} not found in the address book.')
    
    def change_record_name(self, old_record:Record, new_record:Record):
        if str(old_record.name) in self.data:
            self.data[new_record.name.value] = self.data.pop(old_record.name.value)
        else:
            raise NameError(f'Record with name {old_record.name.value} not found in the address book.')

    def show_records(self):
        rows = []
        for record in self.data.values():
            phones = [str(phone) for phone in record.phones]
            row = f'{record.name.value}: {", ".join(phones)}'
            rows.append(row)
        return '\n'.join(rows)
        
    def show_record(self, record:Record):
        if record.name.value in self.data:
            phones = [str(phone) for phone in record.phones]
            return f'{record.name.value}: {", ".join(phones)}'
        else:
            raise NameError(f"Record with name '{record.name.value}' not found in the address book.")
    
    def __repr__(self):
        return "\n".join(str(record) for record in self.data.values())


if __name__ == '__main__':
    ab = AddressBook()

    # Create a Name instance
    name = Name("bill")

    try:
        # Check the validity of the name
        name_value = name.check_name(name.value)
        print(name_value)  # Print the validated name
    except NameError as e:
        print(str(e))

    # Create a Phone instance
    phone1 = Phone("12345")

    try:
        # Check the validity of the name
        name.check_name(name.value)
    except NameError as e:
        print(str(e))

    try:
        # Check the validity of the phone number
        phone1.check_phone(phone1.value)
    except PhoneError as e:
        print(str(e))

    # Create a Record with name and phone number
    rec = Record(name, phone1)
    print(rec.name)

    # Add the record to the address book
    ab.add_record(rec)

    # Add a record without a phone number
    ab.add_record(Record(Name("Jill")))

    # Check if the records in the address book are instances of Record
    for rec in ab.values():
        assert isinstance(rec, Record)

    # Create another Phone instance
    phone2 = Phone("56784")

    # Print the address book
    print(ab)

    # Get a record by name
    rec2 = ab["Jill"]
    print(rec)

    # Add a phone number to the record
    rec2.add_phone(phone2)
    print(rec2)
    
     # Change a phone number in the record
    rec2.change_phone(Phone("56784"), Phone("99345"))

    # Print the updated address book
    print(ab)

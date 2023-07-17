from collections import UserDict
from datetime import datetime, date


class PhoneError(Exception):
    pass


class NameError(Exception):
    pass


class BirthDayError(Exception):
    pass


class Field:
    def __init__(self, value):
        self.value = value
    
    def __repr__(self) -> str:
        return self.value
        

class Name(Field):
    pass


class Phone(Field):
    def __str__(self):
        return str(self._value)

    @property
    def value(self):
        return self._value
    
    @value.setter
    def value(self, phone):
        if str(phone).startswith('+') and phone[-12:].isnumeric():
            self._value = phone
        elif phone.isnumeric() and len(phone) in range(10, 13):
            if len(phone) == 10:
                phone = '+38' + phone
            elif len(phone) == 11:
                phone = '+3' + phone
            elif len (phone) == 12:
                phone = '+' + phone
            self._value = phone
        else:
            raise PhoneError('Phone number should have 10-12 numbers without space')


class BirthDay(Field):
    @property
    def value(self):
        return self._value
    
    @value.setter
    def value(self, birthday):
        try:
            b_day = datetime.strptime(birthday, '%Y-%m-%d')
            self._value = b_day.date()
        except ValueError:
            raise BirthDayError('Invalid birthday format. Please use YYYY-MM-DD format.')
        

class Record:
    def __init__(self, name, phone:Phone=None, birthday:BirthDay=None):
        self.name = name
        self.phones = []
        if phone:
            self.phones.append(phone)
        if birthday:
            self.birthday = birthday
        else:
            self.birthday = None
    
    def add_phone(self, phone:Phone) -> None:
        self.phones.append(phone)
    
    def del_phone(self, phone:Phone) -> None:
        if phone in self.phones:
            self.phones.remove(phone)
        else:
            raise PhoneError(f'Phone number {phone} does not exist')
    
    def change_phone(self, old_phone:Phone, new_phone:Phone) -> bool:
        old_phone_str = str(old_phone.value)
        new_phone_str = str(new_phone.value)

        for i, phone in enumerate(self.phones):
            if str(phone) == old_phone_str:
                self.phones[i] = new_phone_str
                return True
        return False
    
    def days_to_birthday(self):
        if self.birthday is None:
            return None
        
        current_date = date.today()
        birthday_current_year = date(current_date.year, self.birthday.value.month, self.birthday.value.day)
        
        if birthday_current_year >= current_date:
            days = (birthday_current_year - current_date).days
        else:
            birthday_next_year = date(current_date.year + 1, self.birthday.value.month, self.birthday.value.day)
            days = (birthday_next_year - current_date).days
        
        return days
    
    def __str__(self) -> str:
        phone_numbers = ', '.join([str(phone) for phone in self.phones])
        birthday = str(self.birthday.value) if self.birthday else ""
        if phone_numbers and birthday:
            return f'{self.name} | Phones: {phone_numbers} | Birthday: {birthday}'
        if phone_numbers and (not birthday):
            return f'{self.name} | Phones: {phone_numbers}'
        if (not phone_numbers) and (not birthday):
            return f'{self.name} | No records'


class AddressBook(UserDict):
    def add_record(self, record:Record) -> None:
        self.data[record.name.value] = record
    
    def delete_record(self, record:Record) -> None:
        if record.name.value in self.data:
            del self.data[record.name.value]
        else:
            raise NameError(f'Record with name {record.name.value} not found in the address book.')
    
    def change_record_name(self, old_record:Record, new_record:Record) -> None:
        if str(old_record.name) in self.data:
            self.data[new_record.name.value] = self.data.pop(old_record.name.value)
        else:
            raise NameError(f'Record with name {old_record.name.value} not found in the address book.')

    def show_record(self, record:Record) -> str:
        if record.name.value in self.data:
            phones = [str(phone) for phone in record.phones]
            return f'{record.name.value}: {", ".join(phones)}'
        else:
            raise NameError(f"Record with name '{record.name.value}' not found in the address book.")
    
    def find_in_contacts(self, text: str):
        found_contacts = []
        for record in self.data.values():
            if ((record.name.value.startswith(text.capitalize()) or text in record.name.value)
                    or any(text in phone for phone in record.phones)
                    or (record.birthday and (text.strip() == str(record.birthday.value.year))) 
                    if text.isdigit() else text.strip() == str(record.birthday.value).strip()):
                found_contacts.append(record)
        return found_contacts

    def iterator(self, n=5):
        index = 1
        print_block = str("{:<10s} {:<40s} {:<10s}\n".format('Contact', 'Phones', 'Birthday'))
        for record in self.data.values():
            print_block += str("{:<10s} {:<40s} {:<10s}\n".format(record.name.value, 
                                                                  ",".join(str(phone) for phone in record.phones), 
                                                                  str(record.birthday.value) if record.birthday else ""))
            if index < n:
                index += 1
            else:
                yield print_block
                index = 1
                print_block = '\n' + str("{:<10s} {:<40s} {:<10s}\n".format('Contact', 'Phones', 'Birthday'))
        yield print_block

    def print_part_records(self, n=5):
        iterator_result = self.iterator(n)
        result = ''
        for record in iterator_result:
            result += f'{record}'
        return result
        
    def __repr__(self):
        return "\n".join(str(record) for record in self.data.values())


if __name__ == '__main__':
    ab = AddressBook()

    # Create a Name instance
    name = Name("bill")

    try:
        # Check the validity of the name
        name_value = name.value
        print(name_value)  # Print the validated name
    except NameError as e:
        print(str(e))

    # Create a Phone instance
    try:
        phone1 = Phone("12345")
    except PhoneError as e:
        print(str(e))
    
    try:
        phone1 = Phone("1234567890")
    except PhoneError as e:
        print(str(e))
    
    try:
        b_day = BirthDay('2000-01-03')
        print(b_day.value)
    except BirthDayError as e:
        print(str(e))

    try:
        # Check the validity of the phone number
        phone1_value = phone1.value
        print(phone1_value)
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
    phone2 = Phone("5678409876")

    # Print the address book
    print(ab)

    # Get a record by name
    rec2 = ab["Jill"]
    print(rec2)

    # Add a phone number to the record
    rec2.add_phone(phone2)
    print(rec2)
    
     # Change a phone number in the record
    rec2.change_phone(Phone("5678409876"), Phone("9934511111"))

    # Print the updated address book
    print(ab)

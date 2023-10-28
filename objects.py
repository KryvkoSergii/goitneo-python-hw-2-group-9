from collections import UserDict
import re


class IncorrectPhoneFormatException(Exception):
    def __init__(self, message: str):
        self.message = message

    def __str__(self):
        return f"Incorrect phone format: {self.message}"


class IncorrectNameException(Exception):
    def __init__(self, message: str):
        self.message = message

    def __str__(self):
        return f"Incorrect name: {self.message}"
    
class UnableToEditPhoneException(Exception):
    def __init__(self, message: str):
        self.message = message

    def __str__(self):
        return f"Phone does not exist: {self.message}"


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    def __init__(self, name: str):
        Name.validate(name)
        super().__init__(name)

    def validate(name: str):
        if not str:
            raise IncorrectNameException("missing required name")


class Phone(Field):
    def __init__(self, phone: str):
        Phone.validate(phone)
        super().__init__(phone)

    def update_value(self, new_value: str):
        Phone.validate(new_value)
        self.value = new_value

    def validate(phone: str):
        if not re.match(r"\d{10}", phone):
            raise IncorrectPhoneFormatException(
                f"string '{phone}' does not match. Allowed digits only, lenght 10 digits")


class Email(Field):
    def __init__(self, email: str):
        Email.validate(email)
        super().__init__(email)

    def validate(email: str):
        if not re.match(r"[a-z0-9._]+@[a-z]+\.[a-z]{2,3}", email):
            raise IncorrectPhoneFormatException(
                f"string '{email}' does not match. Pattern [a-z0-9]+@[a-z]+\.[a-z]"+"{2,3}")


class Record:
    def __init__(self, name: Name):
        self.name = name
        self.phones: list[Phone] = []
        self.email = None

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"

    def add_phone(self, phone: Phone):
        self.phones.append(phone)

    def remove_phone(self, phone: Phone):
        found = list(filter(lambda p: str(p) == str(phone), self.phones))
        for i in found:
            self.phones.remove(i)

    def add_email(self, email: Email):
        self.email = email


class AddressBook(UserDict):
    def __init__(self):
        self.data = list()

    def add_record(self, record: Record):
        self.data.append(record)

    def find(self, name: Name):
        found = list(filter(lambda record: str(record.name).lower()
                     == str(name).lower(), self.data))
        return found[0] if found else None

    def delete(self, name: Name):
        found = AddressBook.find(name)
        if found:
            self.data.remove(found)
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


class PhoneNotExistException(Exception):
    pass


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
    def __init__(self, value: str):
        Phone.validate(value)
        super().__init__(value)

    # def update_value(self, new_value: str):
    #     Phone.validate(new_value)
    #     self.value = new_value

    def validate(phone: str):
        if not re.match(r"\d{10}", phone):
            raise IncorrectPhoneFormatException(
                f"string '{phone}' does not match. Allowed digits only, lenght 10 digits")
        
    def __eq__(self, __value: object) -> bool:
        return self.value == __value.value


class Email(Field):
    def __init__(self, email: str):
        Email.validate(email)
        super().__init__(email)

    def validate(email: str):
        if not re.match(r"[a-z0-9._]+@[a-z]+\.[a-z]{2,3}", email):
            raise IncorrectPhoneFormatException(
                f"string '{email}' does not match. Pattern [a-z0-9]+@[a-z]+\.[a-z]"+"{2,3}")


class Record:
    def __init__(self, name: Name, phone: Phone | None = None):
        self.name = name
        self.phones: list[Phone] = [phone] if phone else [] 
        self.email = None

    def add_phone(self, phone: Phone):
        self.phones.append(phone)
        
    def edit_phone(self, old_phone: Phone, new_phone: Phone) -> None:
        if old_phone in self.phones:
            self.phones[self.phones.index(old_phone)] = new_phone
            return None
        raise PhoneNotExistException(f"No phone with number {old_phone} in contact {self.name}")
        
    def remove_phone(self, phone: Phone):
        found = list(filter(lambda p: str(p) == str(phone), self.phones))
        for i in found:
            self.phones.remove(i)

    def add_email(self, email: Email):
        self.email = email
    
    def __str__(self):
        return f"Contact name: {self.name}, phones: {'; '.join(p.value for p in self.phones)}"


class AddressBook(UserDict):
    # def __init__(self):
    #     self.data = list()

    def add_record(self, record: Record):
        self.data[str(record.name)] = record
        
    def find(self, name: Name):
        return self.data.get(str(name))
        # found = list(filter(lambda record: str(record.name).lower()
        #              == str(name).lower(), self.data))
        # return found[0] if found else None

    def delete(self, name: Name):
        found = self.find(name)
        if found:
            self.data.remove(found)
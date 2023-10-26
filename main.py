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
        found = list(filter(lambda record: str(record.name).lower() == str(name).lower(), self.data))
        return found[0] if found else None

    def delete(self, name: Name):
        found = AddressBook.find(name)
        if found:
            self.data.remove(found)


class Assistent:
    def input_error(func):
        def inner(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except ValueError:
                return "Give me name and phone please."
            except KeyError:
                return "Unable to find record"
            except TypeError:
                return "Internal error. Contact developer"
            except IncorrectPhoneFormatException as err:
                return err
            except IncorrectNameException as err:
                return err
        return inner

    def parse_input(self, user_input):
        cmd, *args = user_input.split(" ")
        cmd = cmd.strip().lower()
        return cmd, *args

    @input_error
    def add_contact(self, address_book: AddressBook, args):
        name, phone = args
        name_obj = Name(name)
        record_obj = Record(name_obj)

        phone_obj = Phone(phone)
        record_obj.add_phone(phone_obj)

        address_book.add_record(record_obj)
        return "Contact added."

    def find_contact(self, name: str, address_book: AddressBook) -> Record:
        found = address_book.find(Name(name))
        if not found:
            raise KeyError
        return found 

    @input_error
    def add_phone(self, address_book: AddressBook, args):
        name, phone = args
        phones = phone.split(",")
        name_obj = Name(name)
        record: Record = self.find_contact(name_obj, address_book)
        for ph in phones:
            record.add_phone(Phone(ph))
        return "Phone/s added."

    @input_error
    def remove_phone(self, address_book: AddressBook, args):
        name, phone = args
        record: Record = self.find_contact(name, address_book)
        record.remove_phone(Phone(phone))
        return "Phone removed."

    @input_error
    def get_phone(self, address_book: AddressBook, args):
        name = args[0]
        record: Record = self.find_contact(name, address_book)
        phones = list(map(lambda r: str(r), record.phones))
        return ", ".join(phones)

    @input_error
    def add_email(self, address_book: AddressBook, args):
        name, email = args
        record: Record = self.find_contact(name, address_book)
        record.email = Email(email)
        return "Email added."

    @input_error
    def change_email(self, address_book: AddressBook, args):
        name, email = args
        record: Record = self.find_contact(name, address_book)
        record.email = Email(email)
        return "Email changed."
    
    @input_error
    def remove_email(self, address_book: AddressBook, args):
        name = args[0]
        record: Record = self.find_contact(name, address_book)
        record.add_email(None)
        return "Email removed."

    @input_error
    def remove(self, address_book: AddressBook, args):
        name_obj = Name(args[0])
        address_book.delete(name_obj)
        return "Removed."

    def get_all(self, address_book: AddressBook):
        print(f"{'_'*104}")
        print(f"|{'Name:':^40}|{'Phone:':^30}|{'Email:':^30}|")
        print(f"|{'_'*40}|{'_'*30}|{'_'*30}|")
        if len(address_book.data) > 0:
            for record in address_book.data:
                print(f"|{str(record.name):^40}|{', '.join(list(map(lambda rec: str(rec), record.phones))):^30}|{str(record.email) if record.email else '':^30}|")
                print(f"|{'_'*40}|{'_'*30}|{'_'*30}|")
        else:
            print(f"|{' '*102}|")
            print(f"|{'No records found. Add at first':^102}|")
            print(f"|{'_'*102}|")

    def run(self):
        address_book = AddressBook()
        print("Welcome to the assistant bot!")
        help = """
Available commands:
Exit - 'close' or 'exit'
Start work - 'hello'
Add new contact - 'add' <name without spaces> <phone>
Add new phone - 'add-phone' <name without spaces> <phone1>,<phone2>,...
Remove phone - 'remove-phone' <name without spaces> <phone>
Get all phones for contact - 'get-phone' <name without spaces>
Add email - 'add-email' <name without spaces> <email>
Change email - 'change-email' <name without spaces> <email>
Remove email - 'remove-email' <name without spaces>
Remove contact - 'remove' <name without spaces> 
Print all contacts - 'all'            
        """
        print(help)
        while True:
            user_input = input("Enter a command: ")
            command, *args = self.parse_input(user_input)
            if command in ["close", "exit"]:
                print("Good bye!")
                break
            elif command == "hello":
                print("How can I help you?")
            elif command == "add":
                print(self.add_contact(address_book, args))
            elif command == "add-phone":
                print(self.add_phone(address_book,args))
            elif command == "remove-phone":
                print(self.remove_phone(address_book, args))
            elif command == "get-phone":
                print(self.get_phone(address_book, args))
            elif command == "add-email":
                print(self.add_email(address_book, args))
            elif command == "change-email":
                print(self.change_email(address_book, args))
            elif command == "remove-email":
                print(self.remove_email(address_book, args))
            elif command == 'remove':
                print(self.remove(address_book, args))
            elif command == "all":
                self.get_all(address_book)
            elif command == "help":
                print(help)
            else:
                print("Invalid command.")


if __name__ == "__main__":
    Assistent().run()

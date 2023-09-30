from datetime import date
from collections import UserDict



days_in_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

'''
days_in_month потрібна для перевірки дати в сеттері у класі Birthday.
Може краще зробити ії змінною класа ?
'''


class Field:
    def __init__(self):
        self.__value = None

    def __str__(self):
        return str(self.value)

    def __eq__(self, other):
        return self.value == other.value


class Name(Field):
    def __init__(self, value):
        self.__value = None
        self.value = value    
        
    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, new_value):
        if (len(new_value) <=3) or (len(new_value) >=12):
            raise ValueError(f"ERROR: Name '{new_value}' shoud be from 3 to 12 letters")
        if not new_value.isalpha():
            raise ValueError(f"ERROR: invalid letters in the name '{new_value}'")
        self.__value = new_value.capitalize()


class Phone(Field):
    def __init__(self, value):
        self.__value = None
        self.value = value

    def __str__(self):
        return f"({self.__value[0:3]}){self.__value[3:6]}-{self.__value[6:]}"

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, new_value):
        if len(new_value) != 10:
            raise ValueError(f"ERROR: phone number '{new_value}' must be 10 digits long")
        if not new_value.isnumeric():
            raise ValueError(f"ERROR: phone number '{new_value}' contains invalid characters")
        self.__value = new_value


class Birthday(Field):

    def __str__(self):
        return self.__value.strftime('%A %d %B %Y')
 
    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, new_value): 
        today = date.today()
        dmy = new_value.split('-')
        print(f"{new_value=}  {dmy=}")
        if dmy[2].isdigit() and ((today.year - 120) < int(dmy[2]) <= today.year):
            y = int(dmy[2]) 
        else:
            raise ValueError(f"ERROR: year '{dmy[2]}' is wrong")
        if dmy[1].isdigit() and (1 <= int(dmy[1]) <= 12):
            m = int(dmy[1]) 
        else:
            raise ValueError(f"ERROR: month '{dmy[1]}' is wrong")
        if dmy[0].isdigit() and (1 <= int(dmy[0]) <= days_in_month[m-1]):
            d = int(dmy[0]) 
        else:
            raise ValueError(f"ERROR: day '{dmy[0]}' is wrong")

        bd = date(year = y, month = m, day = d)
        self.__value = bd


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.birthday = Birthday() 
        self.phones = []
        self.emails = []
    
    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"

    def index_phone(self, f_phone) -> int:
        i, indx, fp = 0, -1, Phone(f_phone)
        while i < len(self.phones):
            if self.phones[i] == fp:
                indx = i
                break
            i += 1
        return indx

    def find_phone(self, f_phone) -> Phone:
        found = None
        for p in self.phones:
            if p.value == f_phone:
                found = p
                break
        return found

    def add_phone(self, n_phone):
        if self.find_phone(n_phone):  # if self.phones.count(np) == 0:  
            raise ValueError(f"ERROR: this number {n_phone} already exists")
        else:    
            self.phones.append(Phone(n_phone))

    def edit_phone(self, old, new):
        i, indx, op, np = 0, -1, Phone(old), Phone(new)
        if self.find_phone(new):  # if self.phones.count(np) > 0: 
            raise ValueError(f"ERROR: this number {new} already exists")
        while i < len(self.phones):
            if self.phones[i] == op:
                indx = i
                self.phones[i] = np  #self.phones[i].value = np.value
                break
            i += 1
        if indx == -1:
            raise ValueError(f"ERROR: phone number '{old}' does not exists")  
 
    def remove_phone(self, old):
        i, indx, op = 0, -1, Phone(old)
        while i < len(self.phones):
            if self.phones[i] == op:
                indx = i
                self.phones.remove(self.phones[i])
                break
            i += 1
        if indx == -1:
            raise ValueError(f"ERROR: phone number '{old}' does not exists") 

    def add_birthday(self):
        pass

    def edit_birthday(self):
        pass

    def days_to_birthday(self):
        pass


class AddressBook(UserDict):

    def show_records(self):
        for record in self.data.values():
            print(record)    
                
    def find(self, fname) -> Record: # == get(fname)
        return self.data[fname] if fname in self.data.keys() else None

    def add_record(self, new_rec):
        self.data[new_rec.name.value] = new_rec
            
    def delete(self, dname): # delete_record(self):
        if self.find(dname):
            del(self.data[dname]) # self.data.pop(commands[1])  # popitem()
        else:
            raise ValueError(f"ERROR: name '{dname}' not found")

    def edit_record(self, name, old, new):
        r = self.find(name)
        r.edit_phone(old, new)
 
    def iterator(self):
        pass

    def save(self): 
        print("=> AddressBook.save()")

    def load(self):
        print("=> AddressBook.load()")

    def find_names(self):
        pass

    def find_phones(self):
        pass



namebook = AddressBook()
commands = []
'''
Питання - ці дві глобальні змінні мають бути глобальними, чи краще їх зробити,
наприклад, в main(), але тоді їх тягнути як аргументи через усі handler-и ?
'''

def hello_func():
    print("How can I help you?")

def add_func():
    if len(commands) < 3:
        raise ValueError("ERROR: command 'add' wrong parameters")
    rec = namebook.find(commands[1])
    if rec:
        rec.add_phone(commands[2])
    else:
        rec = Record(commands[1])
        rec.add_phone(commands[2])
    namebook.add_record(rec)
 
def change_func():
    if len(commands) < 4:
        raise ValueError("ERROR: command 'change' wrong parameters")
    namebook.edit_record(commands[1].capitalize(), commands[2], commands[3])

def del_func():
    if len(commands) < 2:
        raise ValueError("ERROR: command 'del' wrong parameters")
    namebook.delete(commands[1])

def phone_func():
    print("phone_func")

def show_func():
    if len(namebook) == 0:
        raise ValueError("ERROR: dictionary is empty yet")
    if len(commands) == 1:
        for record in namebook.data.values():
            print(record)

def save_func():
    # namebook.save()
    print("save_func")

def exit_func():
    # namebook.save()
    print("Good bye!")
    exit()

def help_func():
    print("?, help: this list")
    print("goodbye, close, exit: exit program")
    print("showall: show all records")
    print("save: save all records")
    print("phone name: show name's telephon number")
    print("add name number: add record with name and telephon number")
    print("change name oldnumber newnumber: change number for name")
    print("del name: delete name's record")

OPERATIONS = {
    'hello': hello_func,
    'add': add_func,
    'change': change_func,
    'del': del_func,
    'phone': phone_func,
    'showall': show_func,
    'save': save_func,
    'goodbye': exit_func,
    'close': exit_func,
    'exit': exit_func,
    '?': help_func,
    'help': help_func
}

def get_handler(operator):
    global commands
    com_attr = operator.split()
    if com_attr[0].lower() in OPERATIONS:
        commands = com_attr
        OPERATIONS[com_attr[0]]()
    else:
        raise ValueError(f"ERROR: unnown command '{operator}'. Type ? to get help")  


def main():
    while True:
        try:
            get_handler(input("Enter command, please (? to get help): \n>>>"))
                      
        except ValueError  as ve:
            print(ve)


if __name__ == "__main__":
    main()
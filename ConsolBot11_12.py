'''
згідно завдання 11 модулю:
- реалізований метод iterator, який повертає генератор - AddressBook.yield_gen,  AddressBook.iter_rec
  команда "show n"
- клас Record приймає аргумент класу Birthday:
  команда "setb name dd-mm-yyyy" - додати / змінити день народження, метод Record.set_birthday
- клас Record реалізує метод days_to_birthday, який повертає кількість днів до наступного 
  дня народження, якщо день народження заданий: 
  команда "daysb name", метод Record.days_to_birthday

згідно завдання 12 модулю:
- додан функціонал збереження адресної книги (AddressBook.save та AddressBook.load)
- "пошук вмісту книги контактів ... за кількома цифрами номера телефону або літерами імені":
  команда 'findname namepart',  метод AddressBook.find_names, 
  команда 'findphone numberpart',  метод AddressBook.find_phones)
'''

from datetime import datetime
from collections import UserDict
from pathlib import Path

start = 0

class Field:
    def __init__(self):
        self.__value = None
        self.value = None

    def __str__(self):
        return str(self.value)

    def __eq__(self, other):
        return self.value == other.value


class Birthday(Field):
    def __str__(self):
        return (self.value if self.value else "")
    
    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, newvalue): 
        if newvalue:
            bd = datetime.strptime(newvalue, '%d-%m-%Y')
            today = datetime.today()
            if bd > today:
                raise ValueError(f"ERROR: date of birth '{newvalue}' in the future")
            if (today.year - bd.year) > 120:
                raise ValueError(f"ERROR: date of birth '{newvalue}' is very ancient")
        self.__value = newvalue        # self.__value = bd


class Name(Field):
    def __init__(self, value):
        self.__value = None
        self.value = value    
        
    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, newvalue):
        if (len(newvalue) <=2) or (len(newvalue) >=12):
            raise ValueError(f"ERROR: Name '{newvalue}' shoud be from 3 to 12 letters")
        if not newvalue.isalpha():
            raise ValueError(f"ERROR: invalid letters in the name '{newvalue}'")
        self.__value = newvalue.capitalize()


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
    def value(self, newvalue):
        if len(newvalue) != 10:
            raise ValueError(f"ERROR: phone number '{newvalue}' must be 10 digits long")
        if not newvalue.isnumeric():
            raise ValueError(f"ERROR: phone number '{newvalue}' contains invalid characters")
        self.__value = newvalue


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.birthday = Birthday() 
        self.phones = []
    
    def __str__(self):
        bd = (", birthday: " + self.birthday.value if self.birthday.value else "")
        ph = (", phones: "+'; '.join(p.value for p in self.phones) if len(self.phones) > 0 else '')
        return f"Contact name: {self.name.value}{bd}{ph}"
        # return f"Contact name: {self.name.value}{bd}, phones: {'; '.join(p.value for p in self.phones)}"

    def index_phone(self, phone) -> int:
        i, indx, fp = 0, -1, Phone(phone)
        while i < len(self.phones):
            if self.phones[i] == fp:
                indx = i
                break
            i += 1
        return indx

    def find_phone(self, phone) -> Phone:
        found = None
        for p in self.phones:
            if p.value == phone:
                found = p
                break
        return found

    def add_phone(self, newphone):
        if self.find_phone(newphone):  # if self.phones.count(np) == 0:  
            raise ValueError(f"ERROR: this number {newphone} already exists")
        else:    
            self.phones.append(Phone(newphone))

    def edit_phone(self, oldphone, newphone):
        i, indx, op, np = 0, -1, Phone(oldphone), Phone(newphone)
        if self.find_phone(newphone):  # if self.phones.count(np) > 0: 
            raise ValueError(f"ERROR: this number {newphone} already exists")
        while i < len(self.phones):
            if self.phones[i] == op:
                indx = i
                self.phones[i] = np  #self.phones[i].value = np.value
                break
            i += 1
        if indx == -1:
            raise ValueError(f"ERROR: phone number '{oldphone}' does not exists")  
 
    def remove_phone(self, phone):
        i, indx, op = 0, -1, Phone(phone)
        while i < len(self.phones):
            if self.phones[i] == op:
                indx = i
                self.phones.remove(self.phones[i])
                break
            i += 1
        if indx == -1:
            raise ValueError(f"ERROR: phone number '{phone}' does not exists") 

    def set_birthday(self, value):
        self.birthday.value = value

    def days_to_birthday(self) -> int:
        today = datetime.today()    # today datetime.date(2007, 12, 5)
        if not self.birthday.value:
            return -1
        bday = datetime.strptime(self.birthday.value, '%d-%m-%Y')
        bday = bday.replace(year = today.year)
        if bday < today:
            bday = bday.replace(year = today.year + 1)  # birthday = datetime.date(2008, 6, 24)
        return (bday - today).days     # to_birthday = abs(bday - today)


class AddressBook(UserDict):

    def show_records(self):
        for record in self.data.values():
            print(record)    
                
    def find(self, name) -> Record: # == get(name)
        name = name.capitalize()
        return self.data[name] if name in self.data.keys() else None

    def add_record(self, newrec):
        self.data[newrec.name.value] = newrec
            
    def delete(self, name): # delete_record
        if self.find(name):
            del(self.data[name]) # self.data.pop(cl[1])  # popitem()
        else:
            raise ValueError(f"ERROR: name '{name}' not found")

    def edit_record(self, name, oldphone, newphone):
        r = self.find(name)
        r.edit_phone(oldphone, newphone)
 
    def find_names(self, namepart):
        for key in self.data.keys():
            name = key.lower()
            if namepart in name:
                print(self.data[key])

    def find_phones(self, phonepart):
        for key, rec in self.data.items():
            for p in rec.phones:
                if phonepart in p.value:
                    print(self.data[key])
 
    def save(self, filename): 
        with open(filename, "w") as f:
            for rec in self.data.values():
                bd = (rec.birthday.value if rec.birthday.value else "-is-empty-")
                f.write(f"{rec.name.value}|{bd}")
                for p in rec.phones:
                    f.write(f"|{p.value}")
                f.write("\n")

    def load(self, filename):
        with open(filename, "r") as f:
            raws = f.readlines()
            for raw in raws:
                al = raw[:-1].split("|")
                rec = Record(al[0])
                rec.birthday = Birthday()  
                rec.birthday.value = (None if al[1] == "-is-empty-"  else al[1]) 
                for i in range(2, len(al)):
                    rec.phones.append(Phone(al[i])) 
                self.add_record(rec)

    def yield_gen(self, start = 0):
        num = start
        while True:
            print(list(self.data.values())[num])
            yield num
            num += 1

    def iter_rec(self, pos, quan):
        c = self.yield_gen(pos)
        i = 0
        end = min(pos + quan, len(self.data))
        while i < (end - pos):
            try:
                next(c)
            except StopIteration:
                break    
            i += 1    
        return pos+i



def iter_func(nb, cl):    # show n : show n records at a time
    if (len(cl) < 2) or (not cl[1].isnumeric()) or ((quan := int(cl[1])) < 1):
        raise ValueError("ERROR: command 'show' wrong parameters")

    global start   #start = 0
    start = nb.iter_rec(start, quan)
    if start == len(nb.data):
        start = 0

def hello_func(nb, cl):
    print("How can I help you?")

def add_func(nb, cl):   # add name number : add record with name and telephon number
    print("add_func")
    if len(cl) < 2:
        # print("ERROR: command 'add' wrong parameters")
        # return  # в цьому варіанті не потрібні raise
        # АЛЕ: "Вся логіка взаємодії з користувачем реалізована у функції main, 
        # всі print та input відбуваються тільки там." - завдання 9 модуль
        raise ValueError("ERROR: command 'add' wrong parameters")
    rec = nb.find(cl[1])
    if rec:
        if len(cl) > 2:
            rec.add_phone(cl[2])
    else:
        rec = Record(cl[1])
        if len(cl) > 2:
            rec.add_phone(cl[2])
    nb.add_record(rec)
 
def change_func(nb, cl):    # change name oldnumber newnumber : change number for name
    if len(cl) < 4:
        raise ValueError("ERROR: command 'change' wrong parameters")
    nb.edit_record(cl[1].capitalize(), cl[2], cl[3])

def del_func(nb, cl):   # del name : delete name's record
    if len(cl) < 2:
        raise ValueError("ERROR: command 'del' wrong parameters")
    nb.delete(cl[1])

def showall_func(nb, cl):  # showall : show all records
    if len(nb) == 0:
        raise ValueError("ERROR: dictionary is empty yet")
    if len(cl) == 1:
        print(f"total {len(nb.data)} records")
        for record in nb.data.values():
            print(record)

def exit_func(nb, cl):
    raise RuntimeError("Good bye!")

def phone_func(nb, cl): # phone name : show name's telephon number
    if len(cl) < 2:
        raise ValueError("ERROR: command 'phone' wrong parameters")
    rec = nb.find(cl[1])
    if not rec:
        raise ValueError(f"ERROR: name '{cl[1]}' not found")
    print(rec)

def setb_func(nb, cl):  # setb name dd-mm-yyyy : set name's birthday
    if len(cl) < 3:
        raise ValueError("ERROR: command 'setb' wrong parameters")
    rec = nb.find(cl[1])
    if not rec:
        raise ValueError(f"ERROR: name '{cl[1]}' not found")
    rec.set_birthday(cl[2])

def daysb_func(nb, cl): # daysb name : calculate how many days until the birthday
    if len(cl) < 2:
        raise ValueError("ERROR: command 'daysb' wrong parameters")
    rec = nb.find(cl[1])
    if not rec:
        raise ValueError(f"ERROR: name '{cl[1]}' not found")
    days = rec.days_to_birthday()
    if days < 0:
        raise ValueError(f"ERROR: name '{cl[1]}': birthday not specified")
    print(f"{cl[1]} days for bithday: {days}")

def findname_func(nb, cl):  # findname namepart : search for phones by part of the name
    if (len(cl) < 2) or (not cl[1].isalpha()):
        raise ValueError("ERROR: command 'findname' wrong parameters")
    nb.find_names(cl[1])

def findph_func(nb, cl):    # findph numberpart : search for names by part of the phone number
    if (len(cl) < 2) or (not cl[1].isnumeric()):
        raise ValueError("ERROR: command 'findph' wrong parameters")
    nb.find_phones(cl[1])

def help_func(nb, cl):
    print("?, help : this list")
    print("goodbye, close, exit : exit program")
    print("showall : show all records")
    print("show n : show n records at a time")
    print("add name number : add record with name and telephon number")
    print("add name : add record with name")
    print("change name oldnumber newnumber : change number for name")
    print("del name : delete name's record")
    print("phone name : show name's telephon number")
    print("setb name dd-mm-yyyy : set name's birthday")
    print("daysb name : calculate how many days until the birthday")
    print("findname namepart : search for phones by part of the name")
    print("findphone numberpart : search for names by part of the phone number")
    
OPERATIONS = {
    'help': help_func,
    '?': help_func,
    'hello': hello_func,
    'goodbye': exit_func,
    'close': exit_func,
    'exit': exit_func,
    'showall': showall_func,
    'add': add_func,
    'change': change_func,
    'del': del_func,
    'phone': phone_func,
    'setb': setb_func,
    'daysb': daysb_func,
    'findname': findname_func,
    'findphone': findph_func,
    'show': iter_func
}

def get_handler(nb, operator):
    com_attr = operator.split()
    if com_attr[0].lower() in OPERATIONS:
        OPERATIONS[com_attr[0]](nb, com_attr)
    else:
        raise ValueError(f"ERROR: unnown command '{operator}'. Type ? to get help")  


def main():
    print("\n\n>>> main <ControlBot11_12>")
    
    file_dir = Path(__file__)
    file_path = file_dir.parent/"namesrec.txt"

    namebook = AddressBook()
    if file_path.exists():
        namebook.load(file_path)

    while True:
        try:
            get_handler(namebook, input("\nEnter command, please (? to get help): \n>>>"))
                      
        except ValueError as ve:
            print(ve)
        except RuntimeError  as re:
            print(re)
            break

    namebook.save(file_path)

if __name__ == "__main__":
    main()
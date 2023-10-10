namebook = []
commands = []  

def findrec(name):
    indx = -1
    if len(namebook) < 1:
        return indx
    i = 0
    while i < len(namebook):
        if name.capitalize() == namebook[i]["name"]:
            indx = i
            break
        i += 1
    return indx

def add_func(): # add name number: add record with name and telephon number"
    if len(commands) < 3:
        raise ValueError("ERROR: command 'add' wrong parameters")
    if findrec(commands[1]) > -1:
        raise ValueError(f"ERROR: name '{commands[1]}' already exists")
    newrec = {"name": commands[1].capitalize(), "phone": commands[2]}
    namebook.append(newrec)
 
def change_func():  # change name number: change number for name
    if len(commands) < 3:
        raise ValueError("ERROR: command 'change' wrong parameters")
    recindx = findrec(commands[1])    
    if recindx < 0:
        raise ValueError(f"ERROR: name '{commands[1]}' not found")
    namebook[recindx]["phone"] = commands[2]

def del_func(): # del name: delete name's record
    if len(commands) < 2:
        raise ValueError("ERROR: command 'del' wrong parameters")
    recindx = findrec(commands[1])    
    if recindx < 0:
        raise ValueError(f"ERROR: name '{commands[1]}' not found")
    del(namebook[recindx])

def phone_func():  # phone name : show name's telephon number
    if len(commands) < 2:
        raise ValueError("ERROR: command 'phone' wrong parameters")
    recindx = findrec(commands[1])
    if recindx < 0:
        raise ValueError(f"ERROR: name '{commands[1]}' not found")    
    record = namebook[recindx]
    print(f"Contact name: {record['name']};  phone: {record['phone']}")

def show_func():  # showall : show all records
    if len(namebook) == 0:
        raise ValueError("dictionary is empty yet")
    for record in namebook:
        print(f"Contact name: {record['name']};  phone: {record['phone']}")

def hello_func():
    print("How can I help you?")

def exit_func():
    raise RuntimeError("Good bye!")

def help_func():
    print("?: this list")
    print("hello: program hello")
    print("goodbye, close, exit: exit program")
    print("showall: show all records")
    print("phone name: show name's telephon number")
    print("add name number: add record with name and telephon number")
    print("change name number: change number for name")
    print("del name: delete name's record")

OPERATIONS = {
    'hello': hello_func,
    'add': add_func,
    'change': change_func,
    'del': del_func,
    'phone': phone_func,
    'showall': show_func,
    'goodbye': exit_func,
    'close': exit_func,
    'exit': exit_func,
    '?': help_func,
}

def input_error(func):
    def check(oper):
        comlist = oper.split()
        if comlist[0].lower() not in OPERATIONS:
            raise ValueError(f"ERROR: unnown command '{comlist[0]}'. Type ? to get help")
        if len(comlist) > 1:
            if (len(comlist[1]) <=3) or (len(comlist[1]) >=12):
                raise ValueError(f"ERROR: Name '{comlist[1]}' shoud be from 3 to 12 letters")
            if not comlist[1].isalpha():
                raise ValueError(f"ERROR: invalid letters in the name '{comlist[1]}'")
        if len(comlist) > 2:   
            if len(comlist[2]) != 10:
                raise ValueError(f"ERROR: phone number '{comlist[2]}' must be 10 digits long")
            if not comlist[2].isnumeric():
                raise ValueError(f"ERROR: phone number '{comlist[2]}' contains invalid characters")            
        result = func(oper)
        return result
    return check

@input_error
def get_handler(operator):
    global commands
    com_attr = operator.split()
    commands = com_attr
    OPERATIONS[com_attr[0]]()

def main():
    global commands, namebook
    while True:
        try:
            get_handler(input("\nEnter command, please (? to get help): \n>>>"))
                      
        except ValueError  as ve:
            print(ve)
        except RuntimeError  as re:
            print(re)
            break


if __name__ == "__main__":
    main()
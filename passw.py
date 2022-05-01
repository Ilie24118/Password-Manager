import os
import sys
import json
import random
from string import ascii_letters, punctuation, digits
import base64
import hashlib
from termcolor import colored, cprint
from cryptography.fernet import Fernet

def clear(): 
      # for windows
    if os.name == 'nt':
        _ = os.system('cls')
  
    # for mac and linux(here, os.name is 'posix')
    else:
        _ = os.system('clear')

def mainScreen():
    clear()
    print(colored('Password-Manager', 'green', attrs=['bold']))
    print(colored('User-> ', 'yellow') + colored(user_name + '\n', 'white'))
    #print(colored(user_name, 'white'))
    print(colored('1-> New Password\n2-> See all passwords\n3-> Clear all Passwords', 'magenta'))
    print(colored('\n9-> Delete All Data', 'red', attrs=['bold']))
    print(colored('0-> Log Out\n', 'red'))

def lineCounter(filename):
    counter = 0
    passwFileRead = open(filename, 'rt')
    #print(passwFileRead.read())
    for i in (passwFileRead.read()).split('\n'):
        if i:
            counter +=1
    return counter + 1

def lineCounterBytes(filename):
    counter = 0
    passwFileRead = open(filename, 'rb')
    #print(passwFileRead.read())
    for i in (passwFileRead.read()).split(b'\n'):
        if i:
            counter +=1
    return counter + 1

def authantication(nr):
    usrFile = open('usrID.json', 'r')
    data = usrFile.readlines()
    d = json.loads(data[nr])
    return d

def passGen(passw_length):
    string_format = ascii_letters + punctuation + digits
    passw = "".join(random.choice(string_format) for x in range(passw_length))
    return passw

def writeFile(file):
    
    def encPassword():
        key = Fernet.generate_key()
        fernet = Fernet(key + passwordBytes) #key
        encPassw = fernet.encrypt(passw.encode())
        passwDic = {'password':encPassw.decode(),'name':name,'email':email,'key':key.decode()}
        entry = json.dumps(passwDic)
        passwFile.write(entry + '\n')
        passwFile.close()
        passwProgram()  

    clear()
    passwFile = open(file, 'a')
    name=str(input('Add a name: '))
    email = str(input('Add an email: '))

    #Choice for Generated password vs user input:
    choice =str(input('1->Generated password\n2->Write your own password\n\n'))
    if choice == '1':
        passw_length_str = str(input('(Deafault length 64)\nPassword length: '))
        if passw_length_str == '':
            passw_length = 64
            passw = passGen(passw_length)
        else: 
            passw_length = int(passw_length_str)
            passw = passGen(passw_length)

        print(passw)
        j = int(input("\nIs this password OK ?\n\n1-> Yes\n2-> No\n\n"))
        if j == 1:
            #Write the password to the file:

            encPassword()

        elif j == 2:
            clear()
            passwProgram()  
    elif choice == '2':
        passw = str(input('Add a new Password: '))

        encPassword()

    return 0

def remove_line(file,lineToSkip):
    with open(file,'r') as read_file:
        data = read_file.readlines()

    curentLine = 1 
    with open(file, 'w') as passwFile:
        for line in data:
            if curentLine == lineToSkip:
                pass
            else:
                passwFile.write(line)
            curentLine += 1
    return 0

def readFile(file):
    clear()
    for i in range(lineCounter(file) - 1):
        passwFile = open(file, 'r')
        data = passwFile.readlines()
        d = json.loads(data[i])
        string_i = str(i + 1)

        print(colored(string_i + ' -> ', 'yellow') + colored(d['name'], 'green') + colored('\nEmail: ', 'blue') + colored(d['email'], 'cyan'))
        
        stringKey = d['key']
        bytesKey = stringKey.encode()
        fernet = Fernet(bytesKey + passwordBytes)
        encPassword = d['password'].encode()

        password = fernet.decrypt(encPassword).decode()
        print(colored('Password: ', 'red')  + colored(password, 'magenta') + '\n')
        passwFile.close()
    
    k = input("1 -> DELETE specific password\n0 -> Press Enter for Main Screen\n\n")

    if k == '1':
        line_nr = int(input('Write the number of the password: '))

        remove_line(file,line_nr)

        d = str(input(""))
        passwProgram()
    elif k == '0':
        passwProgram()    
    return 0

def clearFile(file):
    clear()
    c = str(input("Are you sure you want to DELETE all Passwords\n Write YES or NO\n"))
    if c == 'YES':
        passwFile = open(file, 'wt')
        clear()
        print("All your passwords have been deleted.\n")
        k = input('Press Enter for Main Scren\n')
        if k == '':
            passwProgram()
    elif c == 'NO':
        passwProgram()   
    return 0

def userId():
    clear()
    print(colored('Password-Manager', 'green', attrs=['bold']))
    print(colored("Authentication\n", 'blue'))
    print(colored("1-> Log in\n2-> Sign up\n", 'cyan'))
    print(colored('0-> Exit', 'red'))
    i = input()
    if i == '1':
        clear()
        username = str(input('Username: '))
        plain_password = str(input('Password: '))

        global userIdNumber
        userIdNumber =  0

        global passwordBytes
        passwordBytes = plain_password.encode()

        encoded_password = base64.b64encode(plain_password.encode('utf-8'))

        for x in range(lineCounterBytes('usrID.json') - 1):
            salt_usr = authantication(x)['salt'].encode('iso-8859-1')
            password = hashlib.sha256(encoded_password + salt_usr).hexdigest()

            userIdNumber += 1

            if (authantication(x)['username'] == username and authantication(x)['password'] == password):
                print('Succesfull Authentication')
                global user_name
                user_name = authantication(x)['username']
                global user
                user = 'passwUsers/' + authantication(x)['username'] + '.json'
                createUsrID_json = open('passwUsers/' + authantication(x)['username'] + '.json', 'a')
                return 2

        if(authantication(x)['username'] != username or authantication(x)['password'] != password):#print("Authentication Failed")
            g = input("\nAuthentication Failed.\nNo such Username or Password\nTry again.\n\n")
            if (g == ''):
                pass 
    elif i == '2':
        clear()

        username = str(input('Username: '))
        password = str(input('Password: '))
        
        usrMatch = 0
        for x in range(lineCounterBytes('usrID.json') -1):
            if (authantication(x)['username'] == username):
                usrMatch += 1
            elif (authantication(x)['username'] != username):
                usrMatch = usrMatch
                
        if (usrMatch == 0):
            clear()
            q = input('New User\nPress Enter')
            if q == '':
                salt = os.urandom(32)

                encoded_password = base64.b64encode(password.encode('utf-8'))
                sha256_encoded_string = hashlib.sha256(encoded_password + salt).hexdigest()

                usrDic = {'username':username, 'password':sha256_encoded_string, 'salt':salt.decode('iso-8859-1')}#iso-8859-1

                #JSON file
                jsonFile = open('usrID.json', 'a')
                entry_2 = json.dumps(usrDic)
                jsonFile.write(entry_2 + '\n')
                jsonFile.close()

        elif (usrMatch == 1):
            clear()
            #sys.exit('User already exists\nPress Enter for Authentication')
            #print('User already exists\nPress Enter for Authentication')
            q = input('Username already exists\nPress Enter')
            if q == '':
                #userId()
                pass
        
    elif i == '0':
        clear()
        sys.exit(colored("Password-Mananger Closed", "red"))
    else:
        userId()

def deleteUser(file):
    clear()
    print(colored('DELETE this account.', 'red', attrs=['bold']))
    print(colored('All data will be lost.', 'red', attrs=['bold']))
    print(colored('Type your master "Confrim" to continue: ', 'cyan'))
    print(colored('\n0-> Cancel\n', 'green', attrs=['bold']))

    i = input()
    if i == 'Confirm':
        remove_line('usrID.json', userIdNumber)
        os.remove(file)
    elif i == '0':
        pass

def passwProgram():
    mainScreen()
    x = input()
    if x == '1':
        writeFile(user)
    elif x == '2':
        readFile(user)
    elif x == '3':

        clearFile(user)
    elif x == '0':
        clear()
        return 1
    elif x == '9':
        deleteUser(user)
    else: 
        mainScreen()


state = True
while (state):
    if (userId() == 2):
        passwProgram()


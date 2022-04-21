import os
import pickle
import sys
import json
import random
from string import ascii_letters, punctuation, digits
import base64
import hashlib


def clear(): 
      # for windows
    if os.name == 'nt':
        _ = os.system('cls')
  
    # for mac and linux(here, os.name is 'posix')
    else:
        _ = os.system('clear')

def mainScreen():
    clear()
    print('Password-Manager\nUser-> ' + user_name + '\n')
    print('1-> New Password\n2-> See all passwords\n3-> Clear all Passwords\n\n0-> Log Out\n')

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
            passwDic = {'password':passw,'name':name,'email':email}
            entry = json.dumps(passwDic)
            passwFile.write(entry + '\n')
            passwFile.close()
            passwProgram()
        elif j == 2:
            clear()
            passwProgram()  
    elif choice == '2':
        passw = str(input('Add a new Password: '))
        passwDic = {'password':passw,'name':name,'email':email}
        entry = json.dumps(passwDic)
        passwFile.write(entry + '\n')
        passwFile.close()
        passwProgram()
    
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
        print(string_i + ' -> ' + d['name'] + '\nEmail: ' + d['email'] + '\nPassword: ' + d['password'] + '\n')
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
    print('Password-Manager\nAuthentication')
    i = input('1-> Log in\n2-> Sign Up\n\n0-> Close\n\n')
    if i == '1':
        clear()
        username = str(input('Username: '))
        plain_password = str(input('Password: '))

        encoded_password = base64.b64encode(plain_password.encode('utf-8'))

        for x in range(lineCounterBytes('usrID.json') - 1):
            salt_usr = authantication(x)['salt'].encode('iso-8859-1')
            password = hashlib.sha256(encoded_password + salt_usr).hexdigest()

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
        sys.exit("Password-Mananger Closed")
    else:
        userId()

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
    else: 
        mainScreen()


state = True
while (state):
    if (userId() == 2):
        passwProgram()


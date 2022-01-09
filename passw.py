import os
import pickle
import sys
import json

def clear(): 
    os.system('clear')

def mainScreen():
    clear()
    print('Password-Manager\nUser-> ' + user_name + '\n')
    print('1-> New Password\n2-> See all passwords\n3-> Clear all Passwords\n0-> Log Out\n')

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
    usrFile = open('usrID.txt', 'rb')
    data = usrFile.readlines()
    d = pickle.loads(data[nr])
    return d

def writeFile(file):
    clear()
    passwFile = open(file, 'a')
    name=str(input('Add a name: '))
    email = str(input('Add an email: '))
    passw = str(input('Add a new Password: '))
    passwDic = {'password':passw,'name':name,'email':email}
    #entry = pickle.dumps(passwDic)
    #passwFile.write(entry + b'\n')
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
        password = str(input('Password: '))
        for x in range(lineCounterBytes('usrID.txt') - 1):
            if (authantication(x)['username'] == username and authantication(x)['password'] == password):
                print('Succesfull Authentication')
                global user_name
                user_name = authantication(x)['username']
                global user
                user = 'passwUsers/' + authantication(x)['username'] + '.json'
                return 2
        if(authantication(x)['username'] != username or authantication(x)['password'] != password):#print("Authentication Failed")
            g = input("\nAuthentication Failed.\nNo such Username or Password\nTry again.\n\n")
            if (g == ''):
                pass 
    elif i == '2':
        clear()
        usrFile = open('usrID.txt', 'ab')
        username = str(input('Username: '))
        password = str(input('Password: '))
        
        usrMatch = 0
        for x in range(lineCounterBytes('usrID.txt') -1):
            if (authantication(x)['username'] == username):
                usrMatch += 1
            elif (authantication(x)['username'] != username):
                usrMatch = usrMatch
                
        if (usrMatch == 0):
            clear()
            q = input('New User\nPress Enter')
            if q == '':
                usrDic = {'username':username, 'password':password}
                entry = pickle.dumps(usrDic)
                usrFile.write(entry + b'\n')
                usrFile.close()
                fileName = username + '.json' 
                newFilepassw = open('passwUsers/' + fileName, 'w')
                newFilepassw.close()
                #userId()
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


import os, pwd, subprocess
from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

app.secret_key = 'secretlkjasfkjdsljksadljf'

@app.route('/userlist', methods=['GET', 'POST'])
def userlist():

    users = pwd.getpwall()
    count = 0
    names = []
    for user in users:
        name = user.pw_name
        names.append(name)
        print (name)
        shell = user.pw_shell
        uid = user.pw_uid
        home_dir = user.pw_dir
        count = count + 1
    return 'List of users via pwd.getpwall:  %s ' % names

@app.route('/usersCommand', methods=['GET', 'POST'])
def usersCommand():

    #users = commands.getoutput("echo $(users)")
    userresults = subprocess.check_output("users")
    print(userresults)
    users = userresults.decode('utf-8').split('\n')
    print(users)

    return render_template('users.html', title='Welcome to ', users=users)
    #return 'List of users via users command:  %s ' % users


@app.route('/whoCommand', methods=['GET', 'POST'])
def whoCommand():

    hostname = subprocess.check_output("hostname").decode('utf-8')
    print('hostname: ' + hostname)

    #userresults = subprocess.check_output("who | cut -d' ' -f1 | sort | uniq")
    userresults = subprocess.check_output("who").decode('utf-8').split('\n')
    print(userresults)
    #users = userresults.decode('utf-8').split('\n')
    #print(users)

    results = []
    for row in userresults:
      if '  ' in row:
          # user name, tty number, date and time, machine address
            user = row
            user = user.split('  ')
            print(user)

            date = user[len(user)-1]
            name = user[0]
            address = user[2]
            terminal = user[1]

            su = SystemUser(name, terminal, date, address)
            results.append(su)

    return render_template('users.html', title='Welcome to ', hostname=hostname, users=results)

class SystemUser:
    def __init__(self, name, tty, date, address):
        self.name = name
        self.tty = tty
        self.date = date
        self.address = address

if __name__ == '__main__':
    app.run(debug='True')
    #host='0.0.0.0'
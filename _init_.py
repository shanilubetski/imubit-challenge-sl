import os, pwd, subprocess
from flask import Flask, session, redirect, url_for, escape, request, render_template
#login_manager
app = Flask(__name__)

@app.route('/')
def index():
    return 'Welcome'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Gives user's home directory
        userhome = os.path.expanduser('~')
        usernameOS = os.path.split(userhome)[-1]
        #usernameCommands = commands.getoutput("echo $(whoami)")
        usernameCommands = subprocess.check_output("whoami").replace("\r\n", "")

        print ("User's home Dir: " + userhome)
        # Gives username by splitting path based on OS
        print ("usernameOS: " + usernameOS)
        print ("usernameCommands: " + usernameCommands)
        session['usernameOS'] = usernameOS
        session['usernameCmd'] = usernameCommands

        return redirect(url_for('index'))

    return '''
        <form action="" method="post">
            <p><input type=text name=username>
            <p><input type=password name=password>
            <p><input type=submit value=Login>
        </form>
    '''

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('usernameOS', None)
    session.pop('usernameCommands', None)
    return redirect(url_for('index'))


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
from db import connect, User
from message import send_rabbitmq_message, receive_rabbitmq_message

MENU = '''
1 - Register
2 - Login
3 - Send Message
4 - Receive Message
5 - Print current user
'''

current_user = None

def check_logged_in():
    return current_user is not None

def login():
    global current_user
    if current_user:
        print('Already logged in')
        return
    while True:
        username = input('Enter username: ')
        password = input('Enter password: ')

        user = User.objects(username=username).first()
        if user and user.check_password(password):
            current_user = user
            print('Login successful!')
            return
        else:
            print('User does not exist or password is wrong')

def logout():
    global current_user
    current_user = None
    print('Logout successful')

def register():
    global current_user
    if current_user:
        print('Already logged in')
        return
    while True:
        email = input('Enter email: ')
        user = User.objects(email=email).first()
        if user:
            print('You are already registered')
            return

        username = input('Enter username: ')
        password = input('Enter password: ')
        user = User(email=email, username=username)
        user.set_password(password)
        user.save()
        return


def print_current_user():
    print(current_user)
        
def send_message():
    global current_user
    if current_user is None:
        print('User not logged in!')
        return
    recepient_username = input('Enter recepient: ')
    message_text = input('Enter message: ')
    send_rabbitmq_message(current_user.username, message_text, recepient_username)

def receive_message():
    global current_user
    if current_user is None:
        print('User not logged in!')
        return
    receive_rabbitmq_message(current_user.username)

while True:

    print(MENU)
    if current_user:
        print('6 - Logout')
    print('exit - Exit application')

    user_input = input('Please select option 1-5: ')
    # if user_input == '1':
    match user_input:
        case '1': register()
        case '2': login()
        case '3': send_message()
        case '4': receive_message()
        case '5': print_current_user()
        case '6': logout()
        case 'exit': break
        case _: print('Wrong number!')

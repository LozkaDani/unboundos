import json
import os
from pathlib import Path
import time as t
import shutil
import shlex
import sys


sf = None
usr_now = None
hostname = ""
commands = []

finded_apps = []

class User:
    def __init__(self, username, password=None, isroot=False):
        self.username = username
        self.password = password
        self.isroot = isroot

    def create_usr(self):
        users_dir = Path("./root/usrs")
        users_file = users_dir / "usrs.json"

        users_dir.mkdir(parents=True, exist_ok=True)

        users = self._load_users(users_file)

        if any(u["username"] == self.username for u in users):
            print("Error: there is a user with that name.")
            return False


        users.append({
            "username": self.username,
            "password": self.password,
            "isroot": self.isroot
        })


        self._save_users(users_file, users)
        print(f"User {self.username} created.")
        os.mkdir(f"./root/home/{self.username}")
        return True

    def deluser(self, usrname):
        users_dir = Path("./root/usrs")
        users_file = users_dir / "usrs.json"

        if not users_file.exists():
            print("ERROR: NO usrs.json FILE.")
            want_reg()
            return False

        users = self._load_users(users_file)

        user_found = None

        for user in users:
            if user["username"] == usrname:
                user_found = user
                break
        if user_found is None:
            print("Delete error: this user in NOT exist.")
            return False

        is_root = self.check_is_root(self.username)

        if is_root is False:
            return False
        users.remove(user_found)
        self._save_users(users_file, users)
        home_dir = Path(f"./root/home/{usrname}")
        if home_dir.exists():
            shutil.rmtree(home_dir)

        print(f"User {usrname} deleted.")


    def login(self):
        users_dir = Path("./root/usrs")
        users_file = users_dir / "usrs.json"

        if not users_file.exists():
            print("ERROR: NO usrs.json FILE.")
            want_reg()
            return False
        users = self._load_users(users_file)

        user_found = None
        for user in users:
            if user["username"] == self.username:
                user_found = user
                break
        if user_found is None:
            print("Login error: this user in NOT exist")
            login_konsole()
            return False

        if user_found["password"] == self.password:
            print(f"Welcome, {self.username}!")
            global usr_now
            usr_now = self.username
            return True
        else:
            print("Login error: incorrect password")
            login_konsole()
            return False

    def check_is_root(self, username):
        users_dir = Path("./root/usrs")
        users_file = users_dir / "usrs.json"
        users = self._load_users(users_file)
        user_found = None
        for user in users:
            if user["username"] == username:
                user_found = user
                break
        if user_found["isroot"] == True:
            return True
        else:
            print(f"{usr_now} is don't have permissions for that command.")
            return False


    def _load_users(self, file_path):
        if file_path.exists():
            try:
                with open(file_path, 'r') as f:
                    data = json.load(f)
                    return data
            except json.JSONDecodeError as e:
                print(f"Error reading users file: {e}")
                return []
        return []

    def _save_users(self, file_path, users):
        with open(file_path, 'w') as f:
            json.dump(users, f, indent=4)

def check_apps():
    global finded_apps, sf
    current_dir = Path(".")
    items = list(current_dir.iterdir())
    for item in items:
        # Проверяем, что это файл и имя совпадает
        if item.is_file() and item.name == "slowfetch.py":
            print("Founded slowfetch.py!")
            
            # Добавляем текущую директорию в путь для импорта
            current_dir_path = str(current_dir.absolute())
            if current_dir_path not in sys.path:
                sys.path.insert(0, current_dir_path)
            
            try:
                # Правильный импорт модуля
                import slowfetch
                print("Successfully imported slowfetch module!")
                finded_apps.append("slowfetch")
                sf = slowfetch
                #print(finded_apps)

                
            except ImportError as e:
                print(f"Error importing slowfetch: {e}")
            
            return True  # Выходим из цикла после нахождения файла
        else:
            pass

def create_user_interactive():
    username = input("User name: ")
    password = input("Password: ")
    isroot = input("Is root? (y/n): ").lower() == 'y'

    user = User(username, password, isroot)
    user.create_usr()

def login_konsole():
    usrname = input("UnboundOs login: ")
    password = input("Password: ")

    user = User(usrname, password)
    user.login()


def load_commands():
    global commands, finded_apps
    commands_file = Path("./root/system/commands.txt")
    commands = []

    if commands_file.exists():
        try:
            with open(commands_file, 'r') as f:
                for line in f:
                    command = line.strip()
                    if command and not command.startswith('#'):  # Пропускаем пустые строки и комментарии
                        commands.append(command)
            if finded_apps != None:
                print("Loading app's commands...")
                for app in finded_apps:
                    commands.append(app)
                    #print(commands)
        except Exception as e:
            print(f"Error loading commands: {e}")

    return commands


def check_command(command):
    global commands, finded_apps, is_true

    # Разделяем команду и аргументы
    parts = command.split()
    if not parts:
        return

    cmd = parts[0]
    args = parts[1:] if len(parts) > 1 else []

    # Проверяем, есть ли команда в списке допустимых
    if cmd in commands:
        if cmd == "poweroff":
            poweroff_command()
        elif cmd == "whoami":
            print(f"You are: {usr_now}")
        elif cmd == "whereami":
            print(f"You are at: {os.getcwd()}")
        elif cmd == "echo":
            text = " ".join(args)
            print(text)
        elif cmd == "ls":
            if usr_now != "None":
                current_dir = Path(".")
                items = list(current_dir.iterdir())
                for item in items:
                    print(item.name)
        elif cmd == "mkdir":
            if args:
                dir_name = args
                try:
                    Path(" ".join(dir_name)).mkdir(exist_ok=True)
                    print(f"Directory '{dir_name}' created")
                except Exception as e:
                    print(f"Error creating directory: {e}")
            else:
                print("mkdir: missing operand")
        elif cmd == "cd":
            cd_command(command)
        elif cmd == "unbound":
            print("Unbound package manager is not implemented yet")
        elif cmd == "help":
            help_command()
        elif cmd == "chostname":
            change_hostname_command()
        elif cmd == "hostname":
            print(f"{hostname}")
        elif cmd == "cfile":
            cfile_command(command)
        elif cmd == "deluser":
            del_user_interactive(usr_now)
        elif cmd == "cat":
            cat_command(command)
        elif cmd == "write":
            write_command(command)
        elif cmd == "append":
            append_command(command)
        elif cmd == "mv":
            mv_command(command)
        elif cmd == "rm":
            rm_command(command)
        elif cmd == "cp":
            cp_command(command)
        elif cmd == "pwd":
            pwd_command()
        elif cmd == "find":
            find_command(command)
        elif cmd == "gute":
            start_gute()
        elif cmd == "clear":
            for i in range(80):
                print("")
        elif cmd == "slowfetch":
            if sf is not None:
                slowfetch_output = sf.slowfetch_class()
                #slowfetch_output.slowfetch_out()
            else:
                print("Slowfetch is not installed or loaded!")
        else:
            print(f"Command {cmd} is recognized but not implemented yet")
    else:
        print(f"Command not found: {cmd}")

def pwd_command():
    print(f"You are at: {os.getcwd()}")

def find_command(command):
    parts = command.split()
    if len(parts) < 2:
        print("find: missing operand")
        return
    
    need_find = " ".join(parts[1:])

    """if need_find:
        if os.path.exists(need_find):
            try:
                for pathdir, dirname, filename in os.walk(Path(need_find).replace(need_find, "")):
                    for filename in filename:
                        print(os.path.join(pathdir, filename))
            except Exception as e:
                print(f"Error finding: {e}")
        else:
            print(f"find: cannot find '{need_find}'")
    else:
        print("find: missing operand")"""
    if need_find:
        try:
            current_dir = Path(".")
            found_any = False
            for pathdir, dirname, filenames in os.walk(current_dir):
                # Проверяем директории
                for dirname_item in dirname:
                    if need_find.lower() in dirname_item.lower():
                        print(os.path.join(pathdir, dirname_item))
                        found_any = True
                
                # Проверяем файлы
                for filename in filenames:
                    if need_find.lower() in filename.lower():
                        print(os.path.join(pathdir, filename))
                        found_any = True
            
            if not found_any:
                print(f"find: cannot find '{need_find}'")
                
        except Exception as e:
            print(f"Error finding: {e}")
    else:
        print("find: missing operand")
    
def start_gute():
    print("Starting GUTE...")
    t.sleep(2)
    os.system("python3.13 write_text.py")

def cat_command(command):
    parts = command.split()
    if len(parts) < 2:
        print("cat: missing file operand")
        return

    filename = " ".join(parts[1:])
    filepath = Path(filename)

    if not filepath.exists():
        print(f"cat: {filename}: No such file or directory")
        return

    if filepath.is_dir():
        print(f"cat: {filename}: Is a directory")
        return

    try:
        with open(filepath, 'r') as f:
            content = f.read()
            print(content)
    except Exception as e:
        print(f"cat: error reading file: {e}")

def del_user_interactive(username):
    usr_del = input("What user you need to delete?: ")

    user = User(username)
    user.deluser(usr_del)


def write_command(command):
    try:
        parts = shlex.split(command)
    except ValueError as e:
        print(f"write: error parsing command: {e}")
        return
    
    if len(parts) < 3:
        print("write: usage: write <filename> <text>")
        return

    filename = parts[1]
    text = parts[2]
    filepath = Path(filename)

    try:
        with open(filepath, 'w') as f:
            f.write(text)
        print(f"Text written to {filename}")
    except Exception as e:
        print(f"write: error writing to file: {e}")


def append_command(command):
    try:
        parts = shlex.split(command)
    except ValueError as e:
        print(f"write: error parsing command: {e}")
        return
    if len(parts) < 3:
        print("append: usage: append <filename> <text>")
        return

    filename = parts[1]
    text = parts[2]
    filepath = Path(filename)

    try:
        with open(filepath, 'a') as f:
            f.write(text)
        print(f"Text appended to {filename}")
    except Exception as e:
        print(f"append: error appending to file: {e}")


def rm_command(command):
    parts = command.split()
    if len(parts) < 2:
        print("rm: missing operand")
        return

    filename = " ".join(parts[1:])
    filepath = Path(filename)

    if not filepath.exists():
        print(f"rm: cannot remove '{filename}': No such file or directory")
        return

    try:
        if filepath.is_dir():
            shutil.rmtree(filepath)
            print(f"Directory '{filename}' removed")
        else:
            filepath.unlink()
            print(f"File '{filename}' removed")
    except Exception as e:
        print(f"rm: error removing: {e}")


def cp_command(command):
    parts = command.split()
    if len(parts) < 3:
        print("cp: missing operands")
        print("Usage: cp <source> <destination>")
        return

    source = " ".join(parts[1:-1])
    destination = parts[-1]
    source_path = Path(source)
    dest_path = Path(destination)

    if not source_path.exists():
        print(f"cp: cannot stat '{source}': No such file or directory")
        return

    try:
        if source_path.is_dir():
            shutil.copytree(source_path, dest_path)
            print(f"Directory '{source}' copied to '{destination}'")
        else:
            shutil.copy2(source_path, dest_path)
            print(f"File '{source}' copied to '{destination}'")
    except Exception as e:
        print(f"cp: error copying: {e}")


def mv_command(command):
    parts = command.split()
    if len(parts) < 3:
        print("mv: missing operands")
        print("Usage: mv <source> <destination>")
        return

    source = " ".join(parts[1:-1])
    destination = parts[-1]
    source_path = Path(source)
    dest_path = Path(destination)

    if not source_path.exists():
        print(f"mv: cannot stat '{source}': No such file or directory")
        return

    try:
        shutil.move(str(source_path), str(dest_path))
        print(f"'{source}' moved to '{destination}'")
    except Exception as e:
        print(f"mv: error moving: {e}")


def cfile_command(command):
    parts = command.split()
    if not parts:
        return
    args = parts[1:] if len(parts) > 1 else []
    filename = args
    filepath = os.path.join(os.getcwd(), " ".join(filename))
    try:
        if args:
            with open(filepath, "x"):
                pass
            print(f"New file is at {filepath}")
        else:
            print("cfile: missing operand")
    except FileExistsError as e:
        print(f"File with that name is existing at {os.getcwd()}")

def help_command():
    global finded_apps
    print("Commands: ")
    print("------BASE COMMANDS------")
    print("unbound - package manager. -S -R")
    print("cd - change directory")
    print("ls - list of 'items' in dir")
    print("mkdir - make dir. mkdir hello world")
    print("echo - prints text on your screen")
    print("poweroff - off system")
    print("whoami - prints your user")
    print("whereami - prints your current dir")
    print("help - this command, list of commands.")
    print("chostname - changes hostname")
    print("hostname - prints your hostname")
    print("cfile - creates new file at dir where you are. cfile hello world.cfg")
    print("cat - display file content. cat filename.txt")
    print("write - write text to file (overwrites). write filename.txt 'Hello World'. use '' to write text to file with spaces in name, or text with spaces write 'my source.txt' 'Hello World!")
    print("append - append text to file. append filename.txt 'More text'. use '' to append text to file with spaces in name, or text with spaces. append 'my source.txt' 'hi!")
    print("rm - remove files/directories. rm filename.txt. use '' to remove dirs and files with spaces in name. rm 'my source.txt'")
    print("cp - copy files. use '' to copy dirs and files with spaces in name. cp 'my source.txt' 'my destination.txt")
    print("mv - move/rename files. use '' to move dirs and files with spaces in name. mv root/system/commands.txt root/ because you are moving files relative to the directory where you are running the command.")
    print("pwd - prints current dir")
    print("find - find files/dirs. use '' to find files/dirs with spaces in name. find 'my source.txt'")
    print("clear - clears screen.")
    print("------APPS------")
    print("gute - Graphic Unbound Text Editor")
    for app in finded_apps:
        print(f"{app} - type {app} to use it.")

def change_hostname_command():
    global hostname
    new_host = input("New hostname: ")
    try:
        hostname = new_host
        print("Hostname succefully changed!")
        with open("./root/system/hostname.unbound", "w") as file:
            file.write(hostname)
    except TypeError as t:
        print(f"Type error: {t}")
    except Exception as e:
        print(f"Error: {e}")

def cd_command(command):
    parts = command.split()
    if not parts:
        return
    args = parts[1:] if len(parts) > 1 else []

    try:
        if not args:
            current_dir = os.getcwd()
            print(f"Current directory: {current_dir}")
        else:
            dir_name = args[0]
            if dir_name == "..":
                os.chdir("..")
            else:
                os.chdir(dir_name)

            # Всегда показываем новую текущую директорию после перехода
            new_dir = os.getcwd()
            print(f"Changed directory to {new_dir}")

    except Exception as e:
        print(f"cd: {e}")

def poweroff_command():
    print("Checking errors...")
    print("Saving users...")
    print("Shutdowning system...")
    t.sleep(3)
    global running
    running = False

def want_reg():
    is_want_reg = input("Do you want to register new user?(y/n): ")
    if is_want_reg.lower() == "y":
        create_user_interactive()
        login_konsole()
    else:
        login_konsole()

def system_dir_load():
    global hostname
    with open("./root/system/hostname.unbound", "r") as file:
        hostname = " ".join(file.readlines())

for i in range(70):
    print("")
check_apps()
load_commands()
system_dir_load()
want_reg()

running = True
while running == True:
    command = input(f"{usr_now}@{hostname}: ")
    check_command(command)
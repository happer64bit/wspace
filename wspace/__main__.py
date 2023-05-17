import argparse
import colorama
import sys
import os
import json
import binascii
from prettytable import PrettyTable

import utils.database

def argument():
    parser = argparse.ArgumentParser(
        description="Task Manager For Your Project"
    )

    subparsers = parser.add_subparsers(dest="command")

    init_parser = subparsers.add_parser("init", help="Initialize WSpace Database")
    
    tasks_parser = subparsers.add_parser("tasks", help="List All Tasks from Database")
    
    add_parser = subparsers.add_parser("add", help="Add Tasks to WSpace Database")
    add_parser.add_argument("task", help="The task to be added to the database")
    
    del_parser = subparsers.add_parser("del", help="Delete task from WSpace Database")
    del_parser.add_argument("index", help="The task id del")
    
    args = parser.parse_args()

    if args.command == "init":
        isExist = os.path.exists(".wspace")
        
        if not isExist:
            print(f"[INIT] {colorama.Fore.GREEN} CREATING DATABASE {colorama.Fore.RESET}")
            db = utils.database.Initialize()
            db.__create__()
            sys.exit()
        else:
            print(f"[INIT] {colorama.Fore.GREEN} ALREADY INITIALIZE {colorama.Fore.RESET}")
            sys.exit()

    if args.command == "add":
        if not os.path.exists(".wspace/keys.json"):
            print(f"[ERROR] {colorama.Fore.RED} DATABASE NOT FOUND {colorama.Fore.RESET}")
            sys.exit()
        
        file = binascii.b2a_hex(os.urandom(10)).decode('utf-8')

        with open(".wspace/keys.json", "r") as f:
            try:
                data = json.load(f)
            except json.decoder.JSONDecodeError as e:
                print(f"[ERROR] {colorama.Fore.RED} INVALID JSON DATA {colorama.Fore.RESET}")
                sys.exit()

        data["maps"].append(file)

        with open(".wspace/keys.json", "w") as f:
            json.dump(data, f)

        with open(f".wspace/{file}.hashed", "w+") as f:
            f.write(args.task.encode().hex())

        print(f"[TASK] {colorama.Fore.GREEN} ADDED TASK TO DATABASE: {args.task} {colorama.Fore.RESET}")
    
    if args.command == "tasks":
        with open(".wspace/keys.json", "r") as f:
            data = json.load(f)

        table = PrettyTable()
        count = 0

        table.field_names = ["ID", "Tasks"]
        
        for key in data["maps"]:
            with open(f".wspace/{key}.hashed", "r") as f:
                task = bytes.fromhex(f.read()).decode("utf-8")
                table.add_row([count.__str__(), task])
            count += 1
        print(table)

    if args.command == "del":
        try:
            with open('.wspace/keys.json', 'r') as f:
                data = json.load(f)

            
            removed_ele = data["maps"].pop(int(args.index))

            with open('.wspace/keys.json', 'w') as f:
                json.dump(data, f)
            os.remove(f".wspace/{removed_ele}.hashed")
        except IndexError:
            print(f"[DELE] {colorama.Fore.RED} OUT OF LENGTH {colorama.Fore.RESET}")
if __name__ == "__main__":
    argument()

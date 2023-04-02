import argparse
from datetime import date

from tabulate import tabulate
from colorama import Fore, Style

from cli_actions import show, remove, create, update

parser = argparse.ArgumentParser(description='APP')
parser.add_argument('-a', help='Command: create, update, show, remove, help')
parser.add_argument('-m', help='Command: Grade, Student, Group, Subject, Teacher')
parser.add_argument('--id')
parser.add_argument('--name')
parser.add_argument('--grade')
parser.add_argument('--date')
parser.add_argument('--st_id')
parser.add_argument('--sb_id')
parser.add_argument('--gr_id')
parser.add_argument('--teach_id')

arguments = parser.parse_args()

my_arg = vars(arguments)

help = my_arg.get('help')
action = my_arg.get('a')
model = my_arg.get('m')
_id = my_arg.get('id')
name = my_arg.get('name')
grade = my_arg.get('grade')
_date = my_arg.get('date')
st_id = my_arg.get('st_id')
sb_id = my_arg.get('sb_id')
gr_id = my_arg.get('gr_id')
teach_id = my_arg.get('teach_id')


def pretty_view(info):
    keys = []
    values = []
    for k, v in info.__dict__.items():
        if isinstance(v, (str, int, date, bool)):
            keys.append(k)
            values.append(v)
    return tabulate([keys, values], headers='firstrow', tablefmt='fancy_grid')


def main():
    match action:
        case 'help':
            print("----------------------------------")
            print("You need to use this command:\n")
            print(Fore.BLUE + "py {name_of_file} -a {name_of_table} -m {command} --id {id}\n")
            print(Style.RESET_ALL)
            print("and add some values if you need:\n")
            print(Fore.GREEN + "--name {...} --grade {...} --date {...} --st_id {...} --sb_id {...} --gr_id {...} --teach_id")
            print(Style.RESET_ALL)
            print("----------------------------------")
        case 'show':
            info = show(model, name, _id)
            print(pretty_view(info))
        case 'remove':
            info = remove(model, name, _id)
            print(f"Row '{info}' is removed")
        case 'create':
            info = create(model, _id, name, grade, _date, st_id, sb_id, gr_id, teach_id)
            print(f"Info is added to {model}")
        case 'update':
            info = update(model, _id, name, grade, _date, st_id, sb_id, gr_id, teach_id)
            print(f"Info is updated in {model}")
            print(pretty_view(info))


if __name__ == '__main__':
    main()

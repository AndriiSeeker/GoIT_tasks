help_coms = 'Available commands: hello; add; change; phone; show all; clear.\n' \
            'To end the work write: "bye", "close", "exit", "end" or "stop".'


def input_error(func):
    def wrapper(*args):
        try:
            return func(*args)
        except IndexError:
            return "Not enough parameters"
        except TypeError:
            return "The command is written incorrectly"
    return wrapper


def hello(*args):
    return "How can I help you?"


@input_error
def add(info_list, *args):
    info_dict = {"name": args[0], "phone": args[1]}
    info_list.append(info_dict)
    return info_dict


@input_error
def change(info_list, *args):
    k = -1
    for lists in info_list:
        for info in (filter((lambda x: x == args[0]), lists.values())):
            k += 1
            info_list[k].update({'phone': args[1]})
            return info
            break


@input_error
def phone(info_list, *args):
    k = -1
    for lists in info_list:
        for _ in (filter((lambda x: x == args[0]), lists.values())):
            k += 1
            return lists.get('phone')
            break


@input_error
def show_all(info_list):
    outputs = ''
    num = 0
    if info_list:
        for info in info_list:
            for k, v in info.items():
                num += 1
                if num % 2 == 0:
                    outputs += f', {k}: {v}; '
                else:
                    outputs += f'{k}: {v}'
        return outputs
    else:
        return info_list


@input_error
def clear(info_list, *args):
    info_list.clear()
    return info_list


def start():
    print(help_coms)
    print("-" * 50)


def exiting(*args):
    return 'Good bye!'


def unknown_command(*args):
    return 'Unknown command! Enter again!'


def helper(*args):
    return help_coms


COMMANDS = {hello: ['hello'], add: ['add '], change: ['change '], phone: ['phone '], show_all: ['show all'], clear: ['clear'], exiting: ['bye','close', 'exit', 'end', 'stop'], helper: ["help"]}


def command_parser(user_command: str) -> (str, list):
    for key, list_value in COMMANDS.items():
        for value in list_value:
            if user_command.lower().startswith(value):
                args = user_command[len(value):].split()
                return key, args
    else:
        return unknown_command, []


def main():
    info_list = []
    start()
    while True:
        user_command = input('Enter command >>> ')
        command, data = command_parser(user_command)
        print(command(info_list, *data))
        if command is exiting:
            break


if __name__ == '__main__':
    main()

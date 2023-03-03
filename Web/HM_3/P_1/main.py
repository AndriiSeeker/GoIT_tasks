import shutil
from pathlib import Path
from threading import Thread
import logging

folders = []


def grab_folder(path: Path):
    for el in path.iterdir():
        if el.is_dir():
            folders.append(el)
            grab_folder(el)


def copy_file(path: Path):
    for el in path.iterdir():
        if el.is_file():
            ext = el.suffix[1:]
            new_path = path / ext
            try:
                new_path.mkdir(exist_ok=True, parents=True)
                shutil.move(el, new_path / el.name)
            except OSError as error:
                logging.error(error)


if __name__ == '__main__':
    logging.basicConfig(level=logging.ERROR, format="%(threadName)s %(message)s")
    while True:
        user_input = input("Path to folder\n>>>")
        user_path = Path(user_input)
        if user_path.exists():
            if not user_path.is_dir():
                print(f"{user_path} isn't a directory")
            else:
                folders.append(user_path)
                grab_folder(user_path)
                threads = []
                for folder in folders:
                    th = Thread(target=copy_file, args=(folder, ))
                    th.start()
                    threads.append(th)
                [th.join() for th in threads]
                print("Sorting is finished")
                break
        else:
            print(f"{user_path} doesn't exists")

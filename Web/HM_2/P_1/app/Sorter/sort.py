import os
import sys
import zipfile
import re
import tarfile
from pathlib import Path
from setuptools import find_packages

folder_list = ['images', 'video', 'documents',
               'audio', 'archives', 'different']


def sort(direct):
    if direct:
        u_input = direct
    else:
        print("Enter Directory to sort")
    path = Path(u_input)
    items = path.glob('**/*')
    caunt = 1
    for item in items:
        # Фото
        if '.jpg' in str(item) or '.jpeg' in str(item) or '.png' in str(item) or '.svg' in str(item):
            source_path = Path(path / 'images')
            if not source_path.exists():
                source_path.mkdir()
            try:
                new_location = item.rename(source_path / normalize(item.name))
            except FileExistsError:
                new_location = item.rename(
                    source_path / f"{str(caunt)}{normalize(item.name)}")
                caunt += 1
        # Видио
        elif '.avi' in str(item) or '.mp4' in str(item) or '.mov' in str(item) or '.mkv' in str(item):
            source_path = Path(path / 'video')
            if not source_path.exists():
                source_path.mkdir()
            try:
                new_location = item.rename(source_path / normalize(item.name))
            except FileExistsError:
                new_location = item.rename(
                    source_path / f"{str(caunt)}{normalize(item.name)}")
                caunt += 1
        # Документы
        elif '.doc' in str(item) or '.docx' in str(item) or '.txt' in str(item) or '.pdf' in str(item) or '.xlsx' in str(item) or '.pptx' in str(item):
            source_path = Path(path / 'documents')
            if not source_path.exists():
                source_path.mkdir()
            try:
                new_location = item.rename(source_path / normalize(item.name))
            except FileExistsError:
                new_location = item.rename(
                    source_path / f"{str(caunt)}{normalize(item.name)}")
                caunt += 1
        # Музыка
        elif '.ogg' in str(item) or '.mp3' in str(item) or '.wav' in str(item) or '.amr' in str(item):
            source_path = Path(path / 'audio')
            if not source_path.exists():
                source_path.mkdir()
            try:
                new_location = item.rename(source_path / normalize(item.name))
            except FileExistsError:
                new_location = item.rename(
                    source_path / f"{str(caunt)}{normalize(item.name)}")
                caunt += 1
        # Архивы
        elif '.zip' in str(item):
            source_path = Path(path / 'archives')
            if not source_path.exists():
                source_path.mkdir()
            fantasy_zip = zipfile.ZipFile(item)
            try:
                fantasy_zip.extractall(
                    source_path / normalize(item.name, ex=False))
            except:
                fantasy_zip.extractall(
                    source_path / f"{str(caunt)}{normalize(item.name, ex=False)}")
                caunt += 1
            fantasy_zip.close()
            try:
                new_location = item.rename(source_path / normalize(item.name))
            except FileExistsError:
                new_location = item.rename(
                    source_path / f"{str(caunt)}{normalize(item.name)}")
                caunt += 1

        elif '.gz' in str(item) or '.tar' in str(item):
            source_path = Path(path / 'archives')
            if not source_path.exists():
                source_path.mkdir()
            tar = tarfile.open(zipfile, "r:gz")
            try:
                tar.extractall(source_path / normalize(item.name, ex=False))
            except:
                tar.extractall(
                    source_path / f"{str(caunt)}{normalize(item.name, ex=False)}")
                caunt += 1
            tar.close()

        elif '.tar' in str(item):
            source_path = Path(path / 'archives')
            if not source_path.exists():
                source_path.mkdir()
            tar = tarfile.open(zipfile, "r:")
            try:
                tar.extractall(source_path / normalize(item.name, ex=False))
            except:
                tar.extractall(
                    source_path / f"{str(caunt)}{normalize(item.name, ex=False)}")
                caunt += 1
            tar.close()
        # Разное
        else:
            if item.is_file() and 'archives' not in item.name:
                source_path = Path(path / "different")
                if not source_path.exists():
                    source_path.mkdir()
                try:
                    new_location = item.rename(
                        source_path / normalize(item.name))
                except FileExistsError:
                    new_location = item.rename(
                        source_path / f"{str(caunt)}{normalize(item.name)}")
                    caunt += 1
    del_empty_dirs(u_input)


def del_empty_dirs(path) -> None:
    for d in os.listdir(path):
        a = os.path.join(path, d)
        if os.path.isdir(a) and 'archives' not in a:
            print(a)
            del_empty_dirs(a)
            if not os.listdir(a):
                os.rmdir(a)


def normalize(x: Path, ex=True) -> str:
    TRANS = {'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'e', 'ж': 'j', 'з': 'z', 'и': 'i', 'й': 'j', 'к': 'k', 'л':
             'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u', 'ф': 'f', 'х': 'h', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'sch', 'ъ': '', 'ы': 'y', 'ь': '', 'э': 'e', 'ю': 'yu', 'я': 'ya', 'є': 'je', 'і': 'i', 'ї': 'ji', 'ґ': 'g',
             'А': 'A', 'Б': 'B', 'В': 'V', 'Г': 'G', 'Д': 'D', 'Е': 'E', 'Ё': 'E', 'Ж': 'J', 'З': 'Z', 'И': 'I', 'Й': 'J', 'К': 'K', 'Л': 'L', 'М': 'M', 'Н': 'N', 'О': 'O', 'П': 'P', 'Р': 'R', 'С': 'S', 'Т': 'T', 'У': 'U', 'Ф': 'F', 'Х': 'H', 'Ц': 'Ts', 'Ч': 'Ch',
             'Ш': 'Sh', 'Щ': 'Sch', 'Ъ': '', 'Ы': 'Y', 'Ь': '', 'Э': 'E', 'Ю': 'Yu', 'Я': 'Ya', 'Є': 'Je', 'І': 'I', 'Ї': 'Ji', 'Ґ': 'G'}
    chars2drop = "!\"$%&'*+,-№#/:.;<>=?[\]^`{|}~\t\n\x0b\x0c\r"
    x = str(x)
    separator = None
    ext = ''
    for i in range(len(x)):
        if x[i] == ".":
            separator = i
    if separator:
        separator = len(x) - separator
        s, ext = x[:-separator], x[-separator:]
    else:
        s = x
    trans_tab = str.maketrans(dict.fromkeys(list(chars2drop), "_"))
    res = " ".join((s.translate(trans_tab).split()))
    res = re.sub("\s*>\s*$", "_", res)
    res = res.translate(res.maketrans(TRANS))
    if ex == False or separator == None:
        return res
    else:
        res += ext
        return res

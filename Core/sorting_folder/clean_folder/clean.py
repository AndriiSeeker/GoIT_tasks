import os
import shutil
import string

#renaming files
def normalize(file):
    correct_name = ''
    pointer = 0
    for num in file:
        if num == '.':
            pointer += 1
    splitting = file.split(".", pointer)
    ending = '.' + splitting.pop(-1)
    if ending in file:
        file = file.replace(ending, '')
    cyrillic_symbols = "абвгдежзийклмнопрстуфхцчшщьюяєіїґ"
    cyrillic_symbols_upper = "АБВГДЕЖЗТЙКЛМНОПРСТУФХЦЧШЩЬЮЯЄШЇҐ"
    translation = (
        "a", "b", "v", "g", "d", "e", "y", "z", "i", "y", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u", "f", "h",
        "ts", "ch", "sh", "sch", "", "yu", "ya", "ye", "i", "ji", "g")
    trans = {}
    correct = string.ascii_letters + string.digits
    for c, t in zip(cyrillic_symbols, translation):
        trans[ord(c)] = t
        trans[ord(c.upper())] = t.upper()

    for letter in file:
        if letter in correct:
            correct_name += letter
        elif letter in cyrillic_symbols:
            correct_name += letter
        elif letter in cyrillic_symbols_upper:
            correct_name += letter
        else:
            correct_name += letter.replace(letter, "_")

    correct_name = correct_name.translate(trans)
    correct_name += ending
    file = correct_name
    return file

#sorting files
def folder_sorting(folder_path):
    os.chdir(folder_path)
    obj = os.scandir()
    file_list = []
    for entry in obj:
        if entry.is_dir():
            if len(os.listdir(entry)) == 0:
                os.rmdir(entry.name)
        else:
            file_list.append(entry.name)

    files = {
            "images" : ['JPEG', 'PNG', 'JPG', 'SVG'],
            "video": ['AVI', 'MP4', 'MOV', 'MKV'],
            "documents": ['DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX'],
            "music": ['MP3', 'OGG', 'WAV', 'AMR'],
            "archives": ['ZIP', 'GZ', 'TAR']
    }
    sorted_files = {
        "images": [],
        "video": [],
        "documents": [],
        "music": [],
        "archives": [],
        "garbage": []
    }
    ending_list = []
    unknown_ending_list = []
    sign = False
    required_value = ''
    unzipped_files = []

    #sorting files
    for file in file_list:
        for k, v in files.items():
            for value in v:
                new_value = '.' + value.lower()
                if file.endswith(new_value):
                    if value.lower() not in ending_list:
                        ending_list.append(value.lower())
                    if file.endswith(".zip") or file.endswith(".tar") or file.endswith(".gz"):
                        os.rename(file, normalize(file))
                        file = normalize(file) #using normalize function
                        unzipped_files.append(file)
                    sign = True
                    os.rename(file, normalize(file))
                    file = normalize(file) #using normalize function
                    required_value = file
                    break
            if sign == True:
                required_key = k
                sign = False
                sorted_files[required_key].append(required_value)
                break
        else:
            if value.lower() not in unknown_ending_list:
                unknown_ending_list.append(value.lower())
            sorted_files["garbage"].append(file)

    #creating folders and transferring files
    for folder, f in sorted_files.items():
        checking = folder_path + "/" + folder
        if not sorted_files[folder] == []:
            if not folder == "archives":
                if not os.path.exists(checking):
                    os.mkdir(folder)
                for nf in f:
                    path_of_file = folder_path + "/" + folder + "/" + nf
                    if os.path.exists(path_of_file):
                        os.replace(nf, path_of_file)
                    else:
                        shutil.move(nf, folder)

    #unzipping archives
    if unzipped_files:
        for zip in unzipped_files:
            name_zip_folder = zip.split('.')
            zip_folder = name_zip_folder[0]
            zip_path_folder = folder_path + "/" + "archives"
            if not os.path.exists(zip_path_folder):
                os.mkdir(zip_path_folder)
            zip_path_file = zip_path_folder + "/" + zip_folder
            if not os.path.exists(zip_path_file):
                os.mkdir(zip_path_file)
            shutil.move(zip, zip_path_file + "/" + zip)
            shutil.unpack_archive(zip_path_file + "/" + zip, zip_path_file)
            os.listdir(zip_path_file)

    print(sorted_files)
    print(ending_list)
    print(unknown_ending_list)

def start():
    definition = True
    while definition == True:
        folder_path = str(input("Write a directory: "))
        try:
            os.path.isdir(folder_path)
            print(folder_sorting(folder_path))
            definition = False
        except OSError:
            print(f"Your directory '{folder_path}' doesn't exists!")

if __name__ == '__main__':
    start()
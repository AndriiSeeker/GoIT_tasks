from faker import Factory
import json
from csv import DictWriter

fake = Factory.create("de_DE")
users = []


def create_users(fake, users: list, n=10):
    for _ in range(n):
        user = {}
        user["name"] = fake.name()
        user["phone"] = fake.phone_number()
        user["birthday"] = fake.date()
        user["email"] = fake.email()
        users.append(user)
    write_in_json(users)


def write_in_json(users: list):
    with open("users.json", "w") as file:
        json.dump(users, file, indent=4)


def get_users():
    with open('users.json') as file:
        users = json.load(file)
        return users


def write_to_csv():
    users_ = get_users()
    with open("users.csv", 'w', encoding='utf-8', newline='') as file:
        fieldsnames = users_[0].keys()
        writer = DictWriter(file, delimiter=";", fieldnames=fieldsnames)
        writer.writeheader()
        for row in users:
            writer.writerow(rowdict=row)
        return users


def main():
    create_users(fake, users)
    all_users = write_to_csv()
    request = input("Write a name or a phone number\n>>>")
    for row in all_users:
        if row["name"].startswith(request) or row["phone"].startswith(request):
            print(f"Name: {row['name']},\nPhone: {row['phone']},\nBirthday: {row['birthday']}, \nEmail: {row['email']}")


if __name__ == '__main__':
    main()

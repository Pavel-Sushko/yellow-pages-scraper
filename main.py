import api
import args
import json


def main():
    arguments = args.get_args()

    search_term = ''

    if not arguments.search:
        search_term = input('Search term: ')
    else:
        search_term = arguments.search

    contacts = api.get_contacts(search_term, arguments.website)

    with open('contacts.json', 'w') as f:
        json.dump(contacts, f, indent=4)

    with open('contacts.csv', 'w') as f:
        f.write('Name,Phone\n')

        for contact in contacts:
            f.write(f'{contact["name"]},{contact["phone"]}\n')


if __name__ == '__main__':
    main()

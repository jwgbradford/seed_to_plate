import json

def ask_boolean(data):
    question = f"{data['question']}\n >>> "
    options = data["options"]
    choice = input(question).lower()[0]
    while choice not in options:
        choice = input(question).lower()[0]
    if choice == options[0]:
        return True
    return False

def pick_from_dict(data):
    options = data["options"].keys()
    question = f"{data['question']}\n >>> "
    print(json.dumps(data["options"], indent=4))
    choice = input(question).lower()
    while choice not in options:
        print('not a valid awnser')
        choice = input(question).lower()
    return choice

def read_data(file_name):
    with open(file_name, 'r') as file:
        data = json.load(file)
    file.closed
    return data

my_options = {}
my_options["options"] = read_data('Server_Side/modifiers_simple.json')
my_options["question"] = "pick one from list"
pick_from_dict(my_options)
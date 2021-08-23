import json

def pick_from_dict(data):
    options = data["options"].keys()
    question = f"{data['question']}\n >>> "
    print(json.dumps(data["options"], indent=4))
    choice = input(question).lower()
    while choice not in options:
        print('not a valid awnser')
        choice = input(question).lower()
    return choice

send = {
    "question" : "Enter Game ID to load",
    "options" : {
    }
}

file = pick_from_dict(send)
print(file)
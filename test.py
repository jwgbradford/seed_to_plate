test = {
    "a" : "some",
    "b" : "stuff"
}
diction = {
    "a" : "different",
    "c" : "data"
}
final = {**test,  **diction}
print(final)
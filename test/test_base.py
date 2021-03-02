a = {
    'a': {
        "a": 1
    },
    'b': {
        "a": 2
    },
    'c': {
        "a": 4
    },
    'd': {
        "a": 1
    },
    'e': {
        "a": 6
    },
}

print(sum([i['a'] for i in a.values()]))
my_dict = {'fruit' : 
            {'0' : {
                    'name': 'pea',
                    'size' : 'small'
            },
            '1' : {'name' : 'bean',
                    'size' : 'large'}
            },
            'tuber' :
            {'0' : {
                    'name': 'potato',
                    'size' : 'small'
            },
            '1' : {'name' : 'carrot',
                    'size' : 'large'}            
            }
}

for key, data in enumerate(my_dict['fruit'].values()):
    print(data['name'])

choice = input('pick plant')
for key, data in enumerate(my_dict['fruit'].values()):
    if choice in data.values():
            print(key)
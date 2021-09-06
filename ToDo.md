# TO DO

## Short list
1. Send client id - send to client
2. Receive starting data - handle on client side
3. Run play game - new game / load game / etc
5. send / recv data - check
6. plants cost money
7. you get a start amount of money

## long list
6. ignore recv_data if it is same as last
7. check on serverside that clock speed is valid
1. get missed data

# Reference
http://datapoint.metoffice.gov.uk/public/data/{resource}?key={APIkey}
https://www.metoffice.gov.uk/services/data/datapoint/code-definitions
https://www.metoffice.gov.uk/services/data/datapoint/uk-3-hourly-site-specific-forecast
https://www.metoffice.gov.uk/services/data/datapoint/api-reference


## Messages to client
``` 
{
    "msg_id" : 1234,
    "player_id" : 5678,
    "msg" : "load_data",
    "data" : {
        "date_last_saved": save_date,
        "clock_speed": self.clock_speed,
        "score": self.score,
        "my_plants": plants_to_write,
        "my_inventory" : self.inventory
    }
}
{
    "msg_id" : 1234,
    "player_id" : 5678,
    "msg" : "ask_boolean",
    "data" : {
        "question" : "Would you like to (l)oad a saved game or start a (n)ew game?",
        "options" : [
            "l",
            "n"
        ]
    }
}
{
    "msg_id" : 1234,
    "player_id" : 5678,
    "msg" : "confirm_plant",
    "data" : {
        "accepted" : "n",
        "reason" : "insufficient funds",
        "plant_data" : {
            "type" : "Fruit",
            "id" : "1"
        }
    }
}
{
    "msg_id" : 1234,
    "player_id" : 5678,
    "msg" : "ask_boolean",
    "data" : {
        "question" : "Which modifiers would you like to use for this plant?",
        "options" : {modifiers.json}
    }
}
{
    "msg_id" : 1234,
    "player_id" : 5678,
    "msg" : "weather",
    "data" : {
        'type': random.choice(['Snow', 'Normal']),
        'temp': round(random.uniform(9, 21), 2),
        'sun': round(random.uniform(0,8), 2),
        'rainfall': random.uniform(0, 0.13143)
    }
}
```

## Messages to server
```
{
    "msg_id" : 1234,
    "player_id" : 5678,
    "msg" : "modifier",
    "data" : {
        "user_id": "something"
    }
}
```

```
{
    "msg_id" : 1234,
    "player_id" : 5678,
    "msg" : "request_for_weather",
    "data" : {}
}
{
    "msg_id" : 1234,
    "player_id" : 5678,
    "msg" : "selected_plant",
    "data" : {
        "plant" : {
            "type" : "Fruit",
            "id" : "01"
            }
        }
}

```

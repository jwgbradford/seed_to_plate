# TO DO

## Short list
1. Send client id - send to client
2. Receive starting data - handle on client side
3. Run play game - new game / load game / etc
5. send / recv data - check

## long list
6. ignore recv_data if it is same as last
7. check on serverside that clock speed is valid
1. get missed data

# Reference

## Messages to client
``` 
{
    "msg_id" : 1234,
    "player_id" : 5678,
    "msg" : "load",
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
    "msg" : "modifier",
    "data" : {
        "user_id": "something"
    }
}
```

```
{
    "msg_id" : 1234,
    "msg" : "request_for_weather",
    "data" : {}
}

```
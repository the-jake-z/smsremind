# SMSremind
## Chipper, Scott, Joey, and Jake 

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

```
create [list name]	                # creates a list
delete [list name]
add [list name] [item]			    # adds item to list
rm [list name] [item no.]	    # deletes item from a list 
sub [list name] [phone no.]         # adds a collaborator  
unsub [list name] [phone no.]       # removes a collaborator from a list
stop								# removes all list subscriptions
```

## Tools

- Python 3.7
- Flask
- MongoEngine
- MongoDB

## Document Structure

```
{
    "subs": [
        "708-287-0004",
        "205-799-9923",
        ...
    ],
    "items": [
        "Milk",
        "Eggs",
        "Butter",
        "Cheese",
        "Brownies",
        ...
    ]
}
```


## Examples

### Create List

** creates an empty list with sender as first subscriber**

```
create groceries
```

```
list "groceries" created
```

### Display List

```
ls groceries
```

```
1. Milk
2. Eggs
3. Butter
4. Cheese
```

### Delete List

```
delete groceries
```

```
list "groceries" deleted
```

### Add Item

```
add groceries brownies
```

```
1. Milk
2. Eggs
3. Butter
4. Cheese
5. Brownies
```

### Remove Item

```
rm groceries 3
```

```
1. Milk
2. Eggs
3. Cheese
4. Brownies
```

### Add Subscription

```
sub groceries 708-287-0004
```

Reply:

```
added 708-287-0004 to groceries
```

Notify:

```
You're been added to groceries by 867-5309 reply HELP
for more options.
```

### Unsubscribe

**Note**: if phone number is omitted, delete sender

```
unsub groceries 708-287-0004
```

```
removed '708-287-0004' from groceries
```

### Stop

```
stop
```

```
removed you from all lists. thanks for using smsremind
```

### Help

```
help
```

```
smsremind:
commons ops:
[see top of file]
```

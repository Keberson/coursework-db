**# Basket system

This section works with tables: ``detail``, ``history``, ``line`` and ``document``.

```
Option card:

Working with queries

1. Precondition: The user has successfully logged in and logged in as a director.
2. Guarantee: the user will receive the result of the request on the screen
3. Minimum warranty: In case of an error, the user will receive the message `Repeat input`
```

```
The user has successfully logged in, he can work with requests, by selecting this item, he has chosen which request he needs. After that, I entered the parameters and sent them. As a result, the user returned a table with the results of the query.

1. The user starts working with queries
2. The system sends a request menu form in response
3. The user selects a request
4. The system sends in response a form for entering parameters
5. The user enters the parameters and submits the form to the system
6. The system executes the request and sends the user the result and the opportunity to return to the menu
```

UML diagram of the menu of this blueprint:

!["UML-menu"](https://github.com/Keberson/coursework-db/blob/master/docs/query/uml-menu.png?raw=true)

UML diagram of the request of this blueprint:

!["UML-query"](https://github.com/Keberson/coursework-db/blob/master/docs/query/uml-query.png?raw=true)

The Search in Clients page:

!["Client"](https://github.com/Keberson/coursework-db/blob/master/docs/query/client.png?raw=true)

The Search in Details page:

!["Details"](https://github.com/Keberson/coursework-db/blob/master/docs/query/details.png?raw=true)

Page with complex queries:

!["Complex"](https://github.com/Keberson/coursework-db/blob/master/docs/query/complex.png?raw=true)

Results page:

!["Result"](https://github.com/Keberson/coursework-db/blob/master/docs/query/result.png?raw=true)**


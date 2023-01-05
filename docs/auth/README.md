# Authentication system

This section works with tables: ``external_user`` and ``internal_user``.

```
Option card:

User Authentication

1. Precondition: The user has registered and is in the table of external or internal users
2. Guarantee: an external user has registered and gained access to the user menu, an internal one - to the role
3. Minimum guarantee: the system has reported an unauthorized authorization, the user must enter the password again or log out
```

```
End User Scenario:

1. The user starts the authentication process
2. The system sends a form for login and password
3. The user enters the login and password for access
4. The system opens access that corresponds to its role

Exceptions:
- the user entered an incorrect username and password or did not enter them → item 2.
```

UML diagram of this blueprint:

!["UML"](https://github.com/Keberson/coursework-db/blob/master/docs/auth/uml.png?raw=true)

The main page of this section is Authorization:

!["Auth page"](https://github.com/Keberson/coursework-db/blob/master/docs/auth/auth.png?raw=true)

The user can log in *(as internal or external)* or register *(only as external)*. 
If the user enters incorrect data the system will send an error message (red toast).

!["Error"](https://github.com/Keberson/coursework-db/blob/master/docs/auth/error.png?raw=true)

The Registration page looks like this:

!["Reg page"](https://github.com/Keberson/coursework-db/blob/master/docs/auth/reg.png?raw=true)

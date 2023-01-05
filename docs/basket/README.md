# Basket system

This section works with tables: ``detail``, ``history``, ``line`` and ``document``.

```
Option card:

The “Basket” system

1. Precondition: The user has successfully logged in and has access to the shopping cart. A table for orders has been created in the database.
2. Guarantee: When forming an order, new records are created in the order tables.
3. Minimum Warranty: When trying to create an empty order, the user will receive an error message.
```

```
End User Scenario:

1. The user starts working with the shopping cart
2. The system sends a page that displays a list of all the parts and their available quantity, as well as the current basket
3. The user clicks the "Add" button
4. The system updates the shopping cart and sends a page with it
5. The user clicks the "Checkout" button
6. The system creates records in the corresponding tables, edits the details table and sends the user the composition of the order, as well as the total cost

Exceptions:
- The user has not added products to the cart: the system gives an error.
```

UML diagram of this blueprint:

!["UML"](https://github.com/Keberson/coursework-db/blob/master/docs/basket/uml.png?raw=true)

The main page of this section:

!["Main page"](https://github.com/Keberson/coursework-db/blob/master/docs/basket/main.png?raw=true)

The user can add products to the cart, delete the entire cart or some products, place an order.

The Order page looks like this:

!["Order page"](https://github.com/Keberson/coursework-db/blob/master/docs/basket/order.png?raw=true)

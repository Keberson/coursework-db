# Coursework Database - Information system «Sale of parts»

This information system is a solution for an enterprise selling parts.

## Table of contents

- [Overview](#overview)
  - [Task](#task)
  - [Screenshot](#screenshot)
- [My process](#my-process)
  - [Built with](#built-with)
  - [Project files](#project-files)
  - [Run](#run)
- [Author](#author)


## Overview

### Task

At a small enterprise, various types of *parts* are manufactured and sold to *customers*.

Each type of manufactured *parts* has a unique code, name, material, weight and price of the finished part are known. The number of available parts and the date of the last update of the quantity are stored. The number of parts changes due to their sale to customers.

The parts are sold to *buyers* who know the unique number of the buyer, his name, city, date of conclusion of the contract with a small enterprise for the purchase of parts and phone number.

The details are released to customers on *invoices*. Each *invoice* has a unique number, the date of the transaction and the total cost of the purchase. According to one invoice, any number of types of parts can be released in any quantity. Therefore, each invoice generally has several *invoice lines*. Each *invoice line* refers to a specific type of purchased parts and contains their quantity.

At a small enterprise, information about the *sales history* of parts is also saved. Each instance of the *sales history* refers to a specific type of parts, contains the old number of parts (before the sale), the new number (after the sale) and the date of sale.

### Screenshot

*Soon will be*

## My process

### Built with
+ Python3
+ Flask
+ pymysql
+ Redis
+ BootStrap5

### Database schema

!["DB"](https://github.com/Keberson/coursework-db/blob/master/docs/db.png?raw=true)


### Project files:
+ `auth` - Authorization and Registration section
+ `basket` - Directory section for external user (client)
+ `blueprint_edit` - Section for editing the list of Parts and Internal users
+ `blueprint_query` - Section for calling requests
+ `blueprint_report` - Section for creating reports
+ `cache` - Working with Redis
+ `data_files` - Configuration files
+ `templates` - Basic system templates
+ `access.py` - Access control
+ `app.py` - The main startup file
+ `db_context_manager.py` - Connecting to and working with a database
+ `db_work.py` - Sending a request to the database
+ `requirements.txt` - List of required libraries and frameworks, as well as their versions
+ `sql_provider.py` - Processing sql files

Every blueprint-folder consist of:
+ ``sql/`` includes a list of all sql queries
+ ``templates/`` includes a list of all html pages and jinja-templates
+ ``route.py`` describes the logic of the server part of current blueprint

### About blueprints
+ [Authentication](docs/auth/README.md)

## Run

To run this app use:

```pip install```
```python3 app.py```

## Author
- Telegram - [@Keberson](https://www.t.me/Keberson)

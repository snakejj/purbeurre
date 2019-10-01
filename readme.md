# Purbeurre

PurBeurre is a script which allows anyone to find a surrogate to an unhealthy
product.

## Dependencies

Use the package manager [pip](https://pip.pypa.io/en/stable/) to 
install all the dependencies. Here are the steps :

1. Open the command prompt.  
2. cd to the directory where requirements.txt is located.  
3. Run this command in your shell:  

```bash
pip install -r requirements.txt
```

## Configuration :

Edit the "configdb.py", located in the subfolder "database", with all the 
informations related to the database, knowingly :

USER : the username   
PASSWORD : the password  
HOST : the host  
DB_NAME : the database name  
AUTH_PLUGIN : the Authentication Plugin  
PORT : the port through which the connection to the database will go
(3306 by default)

## Create/Delete the database :

In order to create or delete the database, you have to first edit the file
"configdb.py" located in the subfolder "database" in order to choose the name
of the database you wish to create or delete.

***
Create the database :  
################

1. Open the command prompt.  
2. cd to the directory where dbcreator.py is located,
in the subfolder "database".  
3. Run this command in your shell:

```bash
python3 dbcreator.py
```
***
Delete the database :  
################

1. Open the command prompt.  
2. cd to the directory where dberaser.py is located,
in the subfolder "database".   
3. Run this command in your shell:

```bash
python3 dberaser.py
```
***
## Start the script

1. Open the command prompt.  
2. cd to the directory where index.py is located.  
3. Run this command in your shell:

```bash
python3 index.py
```


## Contributing
Pull requests are welcome. For major changes, please open an issue first to 
discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)
# Deploying the Application

## install python
install python (preferably 3.10 or later) in your device, if not already install.

To install python3 in Windows using powershell use the command below:
```
winget install -e --id Python.Python.3.10
```

To install python3 in Linux(debian) use the command below:
```
sudo apt install python3
```


## Create virtual environment
Create a virtual environment 

For Windows based systems
```
python3 -m pip install virtualenv
python3 -m virtualenv env
```

For Linux(debian) based systems
```
python3 -m pip install virtualenv
python3 -m virtualenv env
```

## Activating Virtual Environment
In Windows based systems
```
.\env\Scripts\activate
```

In Linux(debian) based systems
```
source ./env/bin/activate
```

## Installing Requirements
After installing and activating the virtualenvironment install the requirements using the command below
```
pip install -r requirements.txt
```

## Starting the server
After activating the Virtual Environment use the command below to start the server
```
python3 app.py
```
Make sure you are in the directory where the file app.py is present

## Using the application
Go to the URL displayed in the terminal
it looks similar to this
>  * Running on all addresses (0.0.0.0)
>  * Running on http://127.0.0.1:5000

You can now use the application
The username for admin is "Admin"
The password for the same is "password"


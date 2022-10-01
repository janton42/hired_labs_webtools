# Hired Labs Webtools

Main repository for web-based tools designed and created by Hired Labs.

## Installation

### 1. Check your Python
Make sure you have some version of `Python 3` installed.

Linux/MacOS
```bash
python --version
```

Windows
```
py --version
```

If not, you can find downloads and setup instructions [here](https://www.python.org/downloads/)

### 2. Create a project folder
```bash
mkdir project_name && cd project_name
```

### 3. Start a virtual environment

Linux/MacOS
```bash
python3 -m venv venv && source venv/bin/activate
```

Windows
```bash
py -m venv venv
venv\Scripts\activate.bat
```

### 4. Clone the repository and change to working directory
```bash
git clone git@github.com:janton42/hired_labs_webtools.git
cd hired_labs_webtools
```

### 5. Install requirements.
```bash
pip install --upgrade pip && pip install -r requirements.txt
```

### 6. Genarate a DJANGO_SECRET_KEY
Linux/MacOS
```bash
python -c "import secrets; print(secrets.token_urlsafe())
```

Windows
```bash
py -c "import secrets; print(secrets.token_urlsafe())
```

This will print a secret key out to your terminal. Copy that to your clipboard, then move on to the next step.

### 7. Create a local environment for secret keys, etc.

Using `echo` on both Linux/MacOS and Windows operating systems can be used to create a config/.env file and paste the secret key you created in step 5. into a variable `DJANGO_SECRET_KEY`, as well as add the `DJANGO_DEBUG=True` for development.

For Windows users, make sure to enter `config\.env`
```bash
echo DJANG_SECRET_KEY='the-secret-key-you-generated-alsdkj-q3j9w28eb' >> config/.env
echo DJANGO_DEBUG=True >> config/.env
```

## Usage

Linux/MacOS
```bash
python3 manage.py runserver
```
Windows
```bash
py manage.py runserver
```


## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss the change.

## License
[GPL-3.0 license](https://www.gnu.org/licenses/gpl-3.0.en.html)

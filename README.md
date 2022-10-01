# Hired Labs Webtools

Main repository for web-based tools designed and created by Hired Labs.

## Installation

### 1. Check your Python
Make sure you have some version of `Python 3` installed.

```bash
python --version
```
If not, you can find downloads and setup instructions [here](https://www.python.org/downloads/)

### 2. Create a project folder
```bash
mkdir project_name\
&& cd project_name
```

### 3. Start a virtual environment
```bash
python3 -m venv venv\
&& source venv/bin/activate
```

### 4. Clone the repository and change to working directory
```bash
git clone git@github.com:janton42/hired_labs_webtools.git
cd hired_labs_webtools
```

### 5. Install requirements.
```bash
pip install --upgrade pip &&\
pip install -r requirements.txt
```

### 6. Genarate a DJANGO_SECRET_KEY
```
python -c "import secrets; print(secrets.token_urlsafe())
```
This will print a secret key out to your terminal. Copy that to your clipboard, then move on to the next step.

### 7. Create a local environment for secret keys, etc.
Using the text editor VIM in the terminal, create a config/.env file, and paste the secret key you created in step 5. into a variable `DJANGO_SECRET_KEY`. While you have this file open, also add the `DJANGO_DEBUG=True` for development.
```bash
vi config/.env
i
DJANGO_SECRET_KEY='the-secret-key-you-generated-alsdkj-q3j9w28eb'
DJANGO_DEBUG=True
esc
:wq
```

## Usage

```bash
python3 manage.py runserver
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss the change.

## License
[GPL-3.0 license](https://www.gnu.org/licenses/gpl-3.0.en.html)

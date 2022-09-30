# Hired Labs Webtools

Main repository for web-based tools designed and created by Hired Labs.

## Installation

Start a virtual environment by any means with which you are comfortable.

### pyenv
```bash
pyenv virtualenv [PYTHON VERSION*(>=3)] environment_name\
&& pyenv activate environment_name
```
Update and install basic packages.
```bash
python3 -m pip install pip --upgrade
```

Install requirements.
```bash
pip install -r requirements.txt
```

## Usage

```bash
python3 manage.py runserver
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss the change.

## License
[GPL-3.0 license](https://www.gnu.org/licenses/gpl-3.0.en.html)

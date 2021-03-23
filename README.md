# Photokeeper

Django web-application for storing and organizing your collections of photos.

## Getting Started

This is a learning project and it has yet a lot to add. These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. 


### Installing


First of all, get the repository in your working directory.

```
git clone https://github.com/dmarichuk/photokeeper.git
```

Then install virtual environment and enter it.

```
pip install virtualenv

python -m venv <name_of_your environment>

source <name_of_your environment>/Scripts/Activate
```

Install all the dependencies for the project from requirements.txt file.

```
pip install -r "requirements.txt"
```

Finally migrate database and collect staticfiles.

```
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic
```

Now you can run this project on your machine.

```
python manage.py runserver
```

## Running the tests

The project is provided with some tests to check the essential functionality.

To run the tests simply command:

```
python manage.py tests
```

## Deployment

This part is still in development :)

## Built With

* [Python 3.8.5](https://www.python.org/)
* [Django 3.1.2](https://www.djangoproject.com/)

 
## Author

**Daniel Marichuk** -  - [dmarichuk](https://github.com/dmarichuk)

## License

This project is licensed under the Mozilla Public License Version 2.0 - see the [LICENSE.md](LICENSE.md) file for details.

## PS
Any feedback would be appreciated.
Cheers!

# 夢境現實 moondream-reality APIs

## Overview
[Firebase](https://firebase.google.com) provides admin sdk and client sdk.
I have combined admin and client sdk in `firebase/__init__.py`. 
If you need to deal with firebase, you should add functions in `firebase/__init__.py`.

The `doge_api` is owned by previous engineer. To prevent front-end rollback versions, I moved the codes from django to flask.

## API-doc
[內部網頁](http://192.168.8.65/apidoc/pages/moondream/index.html)


## Installation

In cmd:

1. Clone repo to locale
```
git clone https://github.com/MoonShineVFX/moondream-api.git
```
2. Into projct
```
cd moondream-api
```
3. Install virtual environment or environment (example by pipenv)
```
pipenv install
```
4. Into virtual environment
```
pipenv shell
```
5. create `.env` file in `moondream-api/` or ask the current engineer leader for the `.env` file
6. Run app
```
flask --debug run
```

## Testing
Test with roles that will frequently switch between superuser, admin, client and no-login. Sometimes it will fail the test cause the frequent switching of roles. So please try twice, or let it sleep more than 1 second between functions when it fail the test.


1. Test all
```
pytest tests -s
```
2. Test single file
```
pytest tests/test_file.py -s
```
3. Test specific function in file
```
pytest tests/test_file.py::test_func -s
```


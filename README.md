# website-fruits-classification

Our website for Bangkit Capstone Project that can predict the level of ripeness of fruits

## How to run locally?

Go to the project folder
or
use this command.

```bash
cd PATH/TO/FOLDER/website-fruits-classification
```
Use [pip](https://pip.pypa.io/en/stable/) package manager to install requirements.

```bash
pip install -r requirements.txt
```
Create python virtual environment.

```bash
pip install virtualenv
virtualenv --version
```
Set virtual environment and flask app's file
```bash
virtualenv env
set FLASK_APP=main.py
flask run
```
Type http://127.0.0.1:5000/ on your browser.


## API Endpoints

### Recognize Image

----

  Return recognize result as JSON.

* **URL**

  /api/recognize

* **Method:**

  `POST`

* **Content-Type**

  `multipart/form-data`

* **Data Params**

   `image=[file]`

* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `{ freshness_level : 100, price : 10000 }`

## License
[MIT](https://choosealicense.com/licenses/mit/)

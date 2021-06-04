# website-fruits-classification

Our website for Bangkit Capstone Project that can predict the level of ripeness of fruits

## How to install?

Use [pip](https://pip.pypa.io/en/stable/) package manager to install requirements.

```bash
pip install -r requirements.txt
```
Create python virtual environment.

```bash
pip install virtualenv
virtualenv --version
```
Go to project folder.

```bash
set FLASK_APP=main.py
flask run
```

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

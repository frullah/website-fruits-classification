# website-fruits-classification

Our website for Bangkit Capstone Project that can knowing the level of ripeness of fruits

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

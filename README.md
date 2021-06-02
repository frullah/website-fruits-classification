# website-fruits-classification
Our website for Bangkit Capstone Project that can knowing the level of ripeness of fruits

## Endpoints

**Recognize Image**
----
  Return recognize result as JSON.

* **URL**

  /api/recognize

* **Method:**

  `POST`
  
*  **URL Params**

   **Required:**
 
   `image=[file]`

* **Data Params**

  None

* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `{ id : 12, name : "Michael Bloom" }`
 
* **Error Response:**

  * **Code:** 404 NOT FOUND <br />
    **Content:** `{ error : "User doesn't exist" }`

  OR

  * **Code:** 401 UNAUTHORIZED <br />
    **Content:** `{ error : "You are unauthorized to make this request." }`

* **Sample Call:**

  ```javascript
    $.ajax({
      url: "/users/1",
      dataType: "json",
      type : "GET",
      success : function(r) {
        console.log(r);
      }
    });
  ```
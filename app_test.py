from app import app
import json
import unittest

class AppTestCase(unittest.TestCase):
  def test_index(self):
    client = app.test_client(self)
    response = client.get("/")
    self.assertEqual(response.status_code, 200)

  def test_recognize_api(self):
    client = app.test_client(self)
    request_data = {
      "image": (open('test/fixtures/image.jpg', 'rb'), 'image.jpg')
    }
    response = client.post("/api/recognize", data=request_data)
    response_data = json.loads(response.data)
    self.assertEqual(response.status_code, 200)
    self.assertEqual(type(response_data["freshness_level"]), int)
    self.assertEqual(type(response_data["price"]), int)

if __name__ == "__main__":
  unittest.main()
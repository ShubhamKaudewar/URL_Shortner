from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_server_running():
    response = client.get("/")
    assert response.status_code == 200
    assert response.text.strip('"') == "Server is running."


def test_shorten_valid_url():
    response = client.post(
        "/shorten",
        headers={},
        json={"url": "https://stackoverflow.com/questions/18810777/how-do-i-read-a-response-from-python-requests"},
    )
    assert response.status_code == 200
    assert response.json()["data"]["shortUrl"] == "http://127.0.0.1:8000/ZGY4NjJ"


def test_shorten_duplicate_url():
    response = client.post(
        "/shorten",
        headers={},
        json={"url": "https://stackoverflow.com/questions/18810777/how-do-i-read-a-response-from-python-requests"},
    )
    assert response.status_code == 200
    assert response.json()["data"]["shortUrl"] == "http://127.0.0.1:8000/ZGY4NjJ"


def test_shorten_invalid_url():
    response = client.post(
        "/shorten",
        headers={},
        json={"url": "foobar.d"},
    )
    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == "Input should be a valid URL, relative URL without a base"


def populate_data():
    import os
    root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
    file_path = os.path.join(root_path, "urldb.json")
    from tinydb import TinyDB
    db = TinyDB(file_path)
    db.truncate()
    items = [
        {
                "shortUrl": "MzE1OTI",
                "longUrl": "https://www.freecodecamp.org/news/get-started-with-tinydb-in-python/",
                "createTime": 1732718142631,
                "expiry": 1532804542631,
                "expired": False,
                "counter": 4
        },
        {
                "shortUrl": "ZGY4NjJ",
                "longUrl": "https://stackoverflow.com/questions/18810777/how-do-i-read-a-response-from-python-requests",
                "createTime": 1732724504902,
                "expiry": 1732810904902,
                "expired": False,
                "counter": 0
        }
    ]
    db.insert_multiple(items)

def test_short_link_valid():
    # Use a valid short link defined in your application
    populate_data()
    short_link = "ZGY4NjJ"
    response = client.get(f"/{short_link}", follow_redirects=False)
    assert response.status_code == 307  # Temporary redirect
    assert response.headers["location"] == "https://stackoverflow.com/questions/18810777/how-do-i-read-a-response-from-python-requests"


def test_short_link_not_found():
    # Use a non-existent short link
    populate_data()
    short_link = "ZGY4Njp"
    response = client.get(f"/{short_link}")
    assert response.status_code == 404
    assert response.json() == {"detail": "The link does not exist, could not redirect."}


def test_short_link_expired():
    populate_data()
    short_link = "MzE1OTI"
    response = client.get(f"/{short_link}")
    assert response.status_code == 404
    assert response.json() == {"detail": "The link expired"}


def test_data_populate():
    populate_data()
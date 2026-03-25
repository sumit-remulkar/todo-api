import requests

def test_api():

    try:

        res = requests.get("http://127.0.0.1:8000")

        if res.status_code == 200:

            print("API working")

        else:

            print("API error")

    except Exception as e:

        print("API test failed:", e)
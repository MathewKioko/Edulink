import requests

# Test backend connection
try:
    r = requests.get('http://127.0.0.1:8000/test')
    print('Test endpoint:', r.text)
except Exception as e:
    print('Error:', e)

# Test groups endpoint
try:
    r = requests.get('http://127.0.0.1:8000/groups')
    print('Groups endpoint:', r.text)
except Exception as e:
    print('Error:', e)


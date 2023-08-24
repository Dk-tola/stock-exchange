import requests

r = requests.post(

        # Here goes your Base API URL
        "https://api.mailgun.net/v3/sandbox19ce4f1055834080aa0b077e71af98f4.mailgun.org/messages.mime",
        # Authentication part - A Tuple
        auth=("api", "6325dc122ba4abdff8c7bec3d00cc77e-0677517f-7ce70962"),

        # mail data will be used to send emails
        data={"from": "<sandbox19ce4f1055834080aa0b077e71af98f4.mailgun.org>",
              "to": ["newsletter@sandbox19ce4f1055834080aa0b077e71af98f4.mailgun.org"],
              "subject": "Subscription",
              "text": " You have been successfully subscribed to our newsletter"})

print(r.status_code)

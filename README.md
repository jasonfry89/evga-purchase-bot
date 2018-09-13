# evga-purchase-bot

This automates the ordering process for the Wednesday-morning at 12:00AM PST B-stock deals on the EVGA website. 

### Instructions

Follow the instructions to get the Firefox Selenium driver on your machine here:

`https://selenium-python.readthedocs.io/installation.html`

Install Python

Install the requirements:

`pip install -r requirements.txt`

Create a file called `configuration.yml` in `evga_automated_order` like this:

```yaml
username: your_evga_username
password: your_evga_password

creditCard:
  name: your_name
  number: your_cc_number
  month: your_cc_expiration_month
  year: your_cc_expiration_year
  cvv: your_cc_cvv

products:
- terms: GTX 1080
  maximumPrice: 320
```

Run it:

`python evga.py`

Careful, this thing actually works. Be very sure that your order looks good before typing `yes`!
# Shopify store parser

This is a test assigment.
Built using Python 3.10, asyncio and httpx libraries for network requests, 
bs4 and email_validator for data scraping.



## Install
Use virtualenv

```
pip install -r requirements.txt
```

## Usage

```
python parse_stores.py <file.csv>
```

## Known issues

- missing tests
- missing proper logging
- type annotations would be nice to have too
- there are few fragile/not efficient parts that 
  can produce unexpected errors due to low familiarity 
  with shopify and a nature of a web scraping
- probably not fully utilized async capabilities

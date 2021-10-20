"""
"immutable" settings for the script purposes
"""


FB_RE = """(?:(?:http|https):\/\/)?(?:www.)?facebook.com\/(?:(?:\w)*#!\/)?(?:pages\/)?(?:[?\w\-]*\/)?(?:profile.php\
?id=(?=\d.*))?([\w\-]*)?"""
TW_RE = """(?:http:\/\/)?(?:www\.)?twitter\.com\/(?:(?:\w)*#!\/)?(?:pages\/)?(?:[\w\-]*\/)*([\w\-]*)"""
PATHS = ['/', '/pages/about/', '/pages/about-us/', '/pages/contact/', '/pages/contact-us/']
PRODUCT_DATA_ENDPOINT = '{url}/products/{product_handle}.json'
ALL_PRODUCTS_PATH = '/collections/all/'
PRODUCTS_DELIMETER = '/products/'

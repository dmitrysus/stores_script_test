"""
StoreData

Interface for gathering data from stores domains, basically a representation
of a row for a csv file
"""

import asyncio
import re
from bs4 import BeautifulSoup
from email_validator import validate_email

from statics import PATHS, FB_RE, TW_RE, PRODUCT_DATA_ENDPOINT, ALL_PRODUCTS_PATH, PRODUCTS_DELIMETER


class StoreData:
    """Class to extract and prepare data from stores urls"""
    def __init__(self, url, n, session):
        self.data = {}
        self.n = n
        self.url = url
        self.full_url = f'https://{self.url}'
        self.session = session
        self.data['url'] = self.url

    async def get_store_html(self, path):
        """
        Returns html from store url
        """
        try:
            resp = await self.session.get(self.full_url+f'{path}', follow_redirects=True)
            return resp.text, resp.status_code
        except Exception as e:  # abomination for sure but I have no time to properly debug
            return '', 404

    async def get_products_data(self, handle):
        """
        Populates data dict with a data of a certain product
        """
        order, product_handle = handle
        product_details_endpoint = PRODUCT_DATA_ENDPOINT.format(url=self.full_url, product_handle=product_handle)
        resp = await self.session.get(product_details_endpoint)
        json_data = resp.json()
        title = ''
        image = ''
        if json_data:
            title = json_data.get('product').get('title', '')
            images = json_data.get('product').get('images', '')
            if images:
                image = images[0]['src']

        self.data[f'title {order}'] = title
        self.data[f'image {order}'] = image

    async def prepare_products_data(self):
        """
        Finds product links and prepares it for data extraction
        """
        all_collections, status_code = await self.get_store_html(ALL_PRODUCTS_PATH+'?section_id=collection-template')
        if status_code == 404:
            all_collections, status_code = await self.get_store_html(ALL_PRODUCTS_PATH)

        soup = BeautifulSoup(all_collections)
        product_links = [a['href'] for a in soup.find_all('a', href=True) if PRODUCTS_DELIMETER in a['href']]
        unique_links = []
        for link in product_links:
            if link not in unique_links:
                unique_links.append(link)

        # this can probably fail due to bad/not consistent product url
        handles = [handle.split(PRODUCTS_DELIMETER)[1].split('?')[0].replace('#', '')
                   for handle in unique_links[:self.n]]
        tasks = [asyncio.ensure_future(self.get_products_data(handle)) for handle in enumerate(handles, start=1)]
        await asyncio.gather(*tasks)

    async def get_contact_info(self, path):
        """
        Populates data dict with email and social links of a store
        """
        html, status_code = await self.get_store_html(path)
        # this email extraction is quite hacky and not reliable but will do for now
        match = re.findall(r'[\w.+-]+@[\w-]+\.[\w.-]+', html)
        filtered_match = []
        for m in match:
            try:
                validate_email(m)
                filtered_match.append(m)
            except Exception:  # email is bad, don't care, moving on
                continue

        # moving too long items to the end of a list to prevent "bad" emails from entering the table
        match = sorted(filtered_match, key=len)

        if match:
            self.data['email'] = match[0]
        fb = re.search(FB_RE, html)
        tw = re.search(TW_RE, html)

        if fb:
            self.data['facebook'] = fb.group(0)
        if tw:
            self.data['twitter'] = tw.group(0)

    async def get_data(self):
        """
        Returns store data
        """
        tasks = [asyncio.ensure_future(self.get_contact_info(path)) for path in PATHS]
        await asyncio.gather(*tasks)
        try:
            await self.prepare_products_data()
        except Exception as e:
            print('oh no')  # I know it's bad

        print('row:', self.data)
        return self.data

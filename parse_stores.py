import argparse
import asyncio
import httpx
from csv_creator import StoreCSVWizard
from store import StoreData

parser = argparse.ArgumentParser()
parser.add_argument('input_file', help='path to a file data will be loaded from')
args = parser.parse_args()


async def create_csv_file():
    csv_wizard = StoreCSVWizard(path=args.input_file)
    async with httpx.AsyncClient(timeout=None) as session:
        tasks = []
        for line in csv_wizard.load_data():
            url = line['url']
            s = StoreData(url=url, n=5, session=session)  # n should be a command line arg

            tasks.append(asyncio.ensure_future(s.get_data()))
        data = await asyncio.gather(*tasks)
        csv_wizard.write_data(data)


def main_loop():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(create_csv_file())
    finally:
        loop.close()


if __name__ == '__main__':
    main_loop()

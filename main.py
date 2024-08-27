import asyncio
from Searchengines.startFind import WBFind
async def main():
    price = 'result.xlsx'#Path to excel file
    await WBFind(price)
if __name__ == '__main__':
    asyncio.run(main())
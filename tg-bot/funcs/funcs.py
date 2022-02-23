import aiohttp

from config import BASE_URL
from loader import basket, users


async def paginator(data: list, page: int, products_page: int) -> list:
    list_res = []
    key_count = 0
    for i in range(0, len(data), products_page):
        key_count += 1
        list_res.append({key_count: data[i:i + products_page]})
    return list_res[page - 1][page]


async def verify_user(user_id: int):
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{BASE_URL}/account/api/v1/verify/{user_id}/") as response:
            r = await response.json()
            if r['success'] is False:
                return False
            else:
                return r['data']


async def get_categories():
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{BASE_URL}/menu/api/v1/category-list/") as response:
            r = await response.json()
            if r['success'] is False:
                return False
            else:
                return r['data']


async def get_products(category_id: int):
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{BASE_URL}/menu/api/v1/product-list?cat={category_id}") as response:
            r = await response.json()
            if r['success'] is False:
                return False
            else:
                return r['data']


async def product_detail(product_id: int):
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{BASE_URL}/menu/api/v1/product-detail/{product_id}/") as response:
            r = await response.json()
            if r['success'] is False:
                return False
            else:
                return r['data']


async def storage_detail(product_id: int):
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{BASE_URL}/sklad/api/v1/product-detail/{product_id}/") as response:
            r = await response.json()
            if r['success'] is False:
                return False
            else:
                return r['data']


async def categories_supplier():
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{BASE_URL}/sklad/api/v1/category-list/") as response:
            r = await response.json()
            if r['success'] is False:
                return False
            else:
                return r['data']


async def products_supplier(category_id: int):
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{BASE_URL}/sklad/api/v1/product-list?cat={category_id}") as response:
            r = await response.json()
            if r['success'] is False:
                return False
            else:
                return r['data']


async def create_order(user_id: int, table: int):
    data = await basket.find({"user_id": user_id}).to_list(1000)
    waiter = (await users.find_one({"user_id": user_id}))['identification']
    d = {
        "waiter": waiter,
        "table": table,
        "order_items": [],
    }
    for item in data:
        d['order_items'].append({
            "meal": item['product_id'],
            "quantity": item['quantity']
        })
    async with aiohttp.ClientSession() as session:
        async with session.post(f"{BASE_URL}/menu/api/v1/order-list-create/", json=d) as response:
            r = await response.json()
            if r['success'] is False:
                return False
            else:
                await basket.delete_many({"user_id": user_id})
                return r['data']


async def orders_today(user_id: int):
    data = await users.find_one({"user_id": user_id})
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{BASE_URL}/menu/api/v1/order-list-create?waiter={data['identification']}") as response:
            r = await response.json()
            if r['success'] is False:
                return False
            else:
                return r['data']


async def delete_single_product(order_id: int, product_id: int):
    async with aiohttp.ClientSession() as session:
        async with session.delete(f"{BASE_URL}/menu/api/v1/remove-order-item/{order_id}?order_item_id={product_id}") as response:
            r = await response.json()
            if r['success'] is False:
                return False
            else:
                return True


async def update_order(order_id: int, product_id: int, quantity: int):
    async with aiohttp.ClientSession(headers={"Content-Type": "application/json"}) as session:
        products = [
            {
                "meal": product_id,
                "quantity": quantity
            }
        ]
        async with session.post(url=f"{BASE_URL}/menu/api/v1/order-update/{order_id}/", json=products) as response:
            r = await response.json()
            return r['success']


async def create_storage(user_id: int, category_id: int, product_id: int, quantity: int, price: int):
    supplier = (await users.find_one({"user_id": user_id}))['identification']
    i = {
        "supplier": supplier,
        "category": category_id,
        "product": product_id,
        "quantity": quantity,
        "price": price
    }
    async with aiohttp.ClientSession(headers={"Content-Type": "application/json"}) as session:
        async with session.post(f"{BASE_URL}/sklad/api/v1/order-create/", json=i) as response:
            r = await response.json()
            if r['success'] is False:
                return False
            else:
                return True



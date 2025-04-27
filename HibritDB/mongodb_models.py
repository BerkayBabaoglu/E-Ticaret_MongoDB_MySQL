from pymongo import MongoClient
from bson import ObjectId
from django.conf import settings
from datetime import datetime

class Product:
    def __init__(self):
        self.client = MongoClient(settings.MONGODB_URI)
        self.db = self.client[settings.MONGODB_DB]
        self.product_collection = self.db['products']

    def get_all_products(self):
        products = list(self.product_collection.find())
        # MongoDB ObjectId'leri string'e çevir
        for product in products:
            product['id'] = str(product['_id'])
        return products

    def get_products_by_supplier(self, supplier_id):
        products = list(self.product_collection.find({'supplier_id': supplier_id}))
        # MongoDB ObjectId'leri string'e çevir
        for product in products:
            product['id'] = str(product['_id'])
        return products

    def add_product(self, name, price, supplier_id, description=None, image_url=None):
        product = {
            'name': name,
            'price': price,
            'supplier_id': supplier_id,
            'description': description,
            'image_url': image_url,
            'created_at': datetime.now()
        }
        result = self.product_collection.insert_one(product)
        product['id'] = str(result.inserted_id)
        return product

    def get_product_by_id(self, product_id):
        try:
            product = self.product_collection.find_one({'_id': ObjectId(product_id)})
            if product:
                product['id'] = str(product['_id'])
            return product
        except:
            return None

class Cart:
    def __init__(self):
        self.client = MongoClient(settings.MONGODB_URI)
        self.db = self.client[settings.MONGODB_DB]
        self.cart_collection = self.db['carts']

    def add_to_cart(self, user_id, product_id, product_name, price, quantity=1):
        user_id = str(user_id)
        existing = self.cart_collection.find_one({'user_id': user_id, 'product_id': product_id})
        if existing:
            self.cart_collection.update_one(
                {'user_id': user_id, 'product_id': product_id},
                {'$inc': {'quantity': int(quantity)}}
            )
        else:
            cart_item = {
                'user_id': user_id,
                'product_id': product_id,
                'product_name': product_name,
                'price': float(price),
                'quantity': int(quantity)
            }
            self.cart_collection.insert_one(cart_item)

    def get_cart_items(self, user_id):
        try:
            # user_id'yi string'e çevir
            user_id = str(user_id)
            cart_items = list(self.cart_collection.find({'user_id': user_id}))
            # MongoDB ObjectId'leri string'e çevir
            for item in cart_items:
                item['id'] = str(item['_id'])
            return cart_items
        except Exception as e:
            print(f"Error in get_cart_items: {str(e)}")
            return []

    def remove_from_cart(self, user_id, product_id):
        user_id = str(user_id)
        return self.cart_collection.delete_many({
            'user_id': user_id,
            'product_id': product_id
        })

    def update_cart_item_quantity(self, user_id, product_id, quantity):
        return self.cart_collection.update_one(
            {'user_id': user_id, 'product_id': product_id},
            {'$set': {'quantity': quantity}}
        )

    def clear_cart(self, user_id):
        return self.cart_collection.delete_many({'user_id': user_id})

    def get_cart_total(self, user_id):
        try:
            # user_id'yi string'e çevir
            user_id = str(user_id)
            pipeline = [
                {'$match': {'user_id': user_id}},
                {'$group': {
                    '_id': None,
                    'total': {'$sum': {'$multiply': ['$price', '$quantity']}}
                }}
            ]
            result = list(self.cart_collection.aggregate(pipeline))
            return result[0]['total'] if result else 0
        except Exception as e:
            print(f"Error in get_cart_total: {str(e)}")
            return 0 
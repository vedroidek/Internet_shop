import redis
from django.conf import settings
from .models import Product

# redis connected
r = redis.Redis(host=settings.REDIS_HOST,
                port=settings.REDIS_PORT,
                db=settings.REDIS_DB)


class Recommender:
    """ This class makes it possible to store purchases of goods and
     receive offers for this product or products. """

    def get_product_key(self, id):
        """ receives the id of the Product object and
         generates the key of the Redis sorted set,
         which stores related products """
        return f'product:{id}:purchased_with'

    def product_bought(self, products):
        """ Gets a list of Product objects that were purchased together."""
        product_ids = [p.id for p in products]
        for product_id in product_ids:
            # get other products
            for with_id in product_ids:
                if product_id != with_id:
                    # increase the score of the product purchased together
                    r.zincrby(self.get_product_key(product_id), 1, with_id)

    def suggest_products_for(self, products, max_result=6):
        product_ids = [p.id for p in products]
        if len(products) == 1:
            # one product only
            suggestions = r.zrange(self.get_product_key(product_ids[0]), 0, -1, desc=True)[:max_result]
        else:
            # generate a temporary key
            flat_ids = ''.join([str(id) for id in product_ids])
            tmp_key = f'tmp_{flat_ids}'
            keys = [self.get_product_key(id) for id in product_ids]
            r.zunionstore(tmp_key, keys)
            r.zrem(tmp_key, *product_ids)
            suggestions = r.zrange(tmp_key, 0, -1, desc=True)[:max_result]
            r.delete(tmp_key)
        suggested_products_ids = [int(id) for id in suggestions]
        suggested_products = list(Product.objects.filter(id__in=suggested_products_ids))
        suggested_products.sort(key=lambda x: suggested_products_ids.index(x.id))
        return suggested_products

    def clear_purchase(self):
        for id in Product.objects.values_list('id', flat=True):
            r.delete(self.get_product_key(id))

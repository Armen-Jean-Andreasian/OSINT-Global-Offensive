from abc import ABC
import os


class AbsModelCache(ABC):
    SINGLE_ITEM_KEY_TEMPLATE: str
    MULTIPLE_ITEMS_KEY_TEMPLATE: str
    TTL = int(os.environ.get('REDIS_CACHE_TTL'))

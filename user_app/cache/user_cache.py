from django.core.cache import cache
from abstractions.model_cache_abs import AbsModelCache

from service_response import ServiceResponse
from typing import TYPE_CHECKING
from user_app.models import UserModel

if TYPE_CHECKING:
    from uuid import UUID


class UserCache(AbsModelCache):
    SINGLE_ITEM_KEY_TEMPLATE = "user:{user_id}"
    TTL: int

    @classmethod
    def set(cls, user_id: "UUID", user_instance: UserModel, ttl: int = None):
        """Caches one user to cache under user:{user_id} key, with ttl of REDIS_CACHE_TTL"""

        cache.set(
            cls.SINGLE_ITEM_KEY_TEMPLATE.format(user_id=user_id),
            user_instance,
            timeout=cls.TTL if ttl is None else ttl
        )

    @classmethod
    def get(cls, user_id: "UUID", ttl: int = None) -> ServiceResponse[bool, str] | ServiceResponse[bool, UserModel]:
        """Gets user from cache"""

        cache_key = cls.SINGLE_ITEM_KEY_TEMPLATE.format(user_id=user_id)
        user_instance = cache.get(cache_key)

        if not user_instance:
            user_instance = UserModel.objects.filter(id=user_id).first()
            if not user_instance:
                return ServiceResponse(status=False, error="User not found")

        cls.set(user_id=user_id, user_instance=user_instance, ttl=cls.TTL if ttl is None else ttl)

        return ServiceResponse(status=True, data=user_instance)

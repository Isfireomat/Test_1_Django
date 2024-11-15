from typing import Optional, Union, Dict, List
from redis import Redis
from utils.redis_utils import set_cashe_item, get_cashe_item, \
                              get_redis_client

def set_collection_cashe(user_id: Union[str, int],
                        user_collection_id: Union[str, int], 
                        item: Union[Dict, List],
                        time: int=20,
                        client: Redis = get_redis_client()
                        ) -> None:
    set_cashe_item(key=f"{user_id}:{user_collection_id}",
                   item=item,
                   time=time,
                   client=client)

def get_collection_cashe(user_id:  Union[str, int],
                        user_collection_id:  Union[str, int], 
                        client: Redis = get_redis_client()
                        ) -> Optional[Union[List, Dict]]:
    return get_cashe_item(key=f"{user_id}:{user_collection_id}",
                          client=client)

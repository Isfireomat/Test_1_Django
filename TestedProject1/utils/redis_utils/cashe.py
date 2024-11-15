from typing import Optional, Union, Dict, List
import pickle
from redis import Redis
from utils.redis_utils import get_redis_client

def set_cashe_item(key: Union[str, int], 
                   item: Union[Dict, List], 
                   time: int=20,
                   client: Redis = get_redis_client()
                   ) -> None:
    item: bytes = pickle.dumps(item)
    client.set(key, item, ex=time)

def get_cashe_item(key: Union[str, int], 
                   client: Redis = get_redis_client()
                   ) -> Optional[Union[Dict, List]]:
    if not client.exists(key): return None
    item: Union[List, Dict] = pickle.loads(client.get(key))
    return item
import redis
from datetime import datetime
import secrets

redis_client = redis.StrictRedis(host='127.0.0.1', port=6379, db=0)

def get_next_incremental_number():
    try:
        today_date = datetime.now().strftime('%Y-%m-%d')
        last_date = redis_client.get('last_date')
        if last_date is None or last_date.decode('utf-8') != today_date:
            redis_client.set('last_date', today_date)
            redis_client.set('file_number', 0)
        next_number = redis_client.incr('file_number')
        if next_number > 99999:
            redis_client.set('file_number', 0)
            next_number = redis_client.incr('file_number')
        return next_number
    except Exception:
        return secrets.randbelow(100000)

for i in range(0,200):
    print(get_next_incremental_number())

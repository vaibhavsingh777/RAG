# app/cache.py
import redis
import hashlib

r = redis.Redis(host="localhost", port=6379, db=0)

def cache_get(question):
    key = hashlib.md5(question.encode()).hexdigest()
    result = r.get(key)
    return result.decode() if result else None

def cache_set(question, answer, expiry=3600):
    key = hashlib.md5(question.encode()).hexdigest()
    r.set(key, answer, ex=expiry)

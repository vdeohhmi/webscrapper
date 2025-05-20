import random

def get_random_headers():
    agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36...",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15...",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36..."
    ]
    return {"User-Agent": random.choice(agents)}

def load_proxies(proxy_list):
    return proxy_list

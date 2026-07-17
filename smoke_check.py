import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "grocery_store.settings")

import django
from django.test import Client

django.setup()

client = Client()
routes = [
    ("/", 200, "FreshCart Grocery"),
    ("/?q=milk", 200, "Milk 1L"),
    ("/accounts/login/", 200, "Login"),
    ("/admin/", 302, "/admin/login/"),
]

failed = False
for path, expected_status, expected in routes:
    response = client.get(path)
    body = response.content.decode("utf-8", errors="ignore")
    target = response.headers.get("Location", "") if response.status_code in {301, 302} else body
    ok = response.status_code == expected_status and expected in target
    print(f"{path}: {response.status_code} - {'OK' if ok else 'FAILED'}")
    if not ok:
        failed = True

raise SystemExit(1 if failed else 0)

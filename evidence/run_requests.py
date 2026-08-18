import httpx
import json

BASE = "http://127.0.0.1:8000"

client = httpx.Client()

# 1. Create a review
r1 = client.post(f"{BASE}/resenas", json={"producto_id":1,"usuario_id":42,"calificacion":5,"comentario":"Excelente"})
# 2. Create another review
r2 = client.post(f"{BASE}/resenas", json={"producto_id":1,"usuario_id":43,"calificacion":4,"comentario":"Bueno"})
# 3. List reviews for product 1
r3 = client.get(f"{BASE}/resenas", params={"producto_id":1})
# 4. Get average
r4 = client.get(f"{BASE}/productos/1/promedio")
# 5. Delete first review (if created)
try:
    id1 = r1.json().get("id")
    r5 = client.delete(f"{BASE}/resenas/{id1}")
except Exception:
    r5 = None

results = {
    "create1": {"status": r1.status_code, "body": r1.json() if r1.content else None},
    "create2": {"status": r2.status_code, "body": r2.json() if r2.content else None},
    "list": {"status": r3.status_code, "body": r3.json() if r3.content else None},
    "avg": {"status": r4.status_code, "body": r4.json() if r4.content else None},
    "delete1": {"status": r5.status_code if r5 is not None else None, "body": r5.text if r5 is not None else None}
}

with open("evidence/results.json","w",encoding="utf-8") as f:
    json.dump(results,f,ensure_ascii=False,indent=2)

print("Saved evidence to evidence/results.json")

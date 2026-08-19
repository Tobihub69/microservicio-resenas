import httpx
import json

BASE = "http://127.0.0.1:8001"
API_KEY = "mi_secreto"

client = httpx.Client(timeout=10)

def try_post(headers=None):
    return client.post(f"{BASE}/resenas", headers=headers, json={"producto_id":99,"usuario_id":999,"calificacion":5,"comentario":"Prueba auth"})

res = {}

# 1. POST without key
r1 = try_post()
res['post_no_key'] = {'status': r1.status_code, 'text': r1.text}

# 2. POST with key
r2 = try_post(headers={'X-API-Key': API_KEY})
res['post_with_key'] = {'status': r2.status_code, 'body': r2.json() if r2.content else None}

# 3. List reviews for producto_id=99
r3 = client.get(f"{BASE}/resenas", params={"producto_id":99})
res['list'] = {'status': r3.status_code, 'body': r3.json() if r3.content else None}

# 4. Get average
r4 = client.get(f"{BASE}/productos/99/promedio")
res['avg'] = {'status': r4.status_code, 'body': r4.json() if r4.content else None}

# 5. Delete created review (if any)
delete_info = None
try:
    created_id = r2.json().get('id')
    if created_id:
        r5 = client.delete(f"{BASE}/resenas/{created_id}", headers={'X-API-Key': API_KEY})
        delete_info = {'status': r5.status_code, 'text': r5.text}
except Exception as e:
    delete_info = {'error': str(e)}

res['delete'] = delete_info

with open('evidence/results_auth.json','w',encoding='utf-8') as f:
    json.dump(res,f,ensure_ascii=False,indent=2)

print('Saved evidence to evidence/results_auth.json')

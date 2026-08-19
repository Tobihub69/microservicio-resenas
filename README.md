# Microservicio de Reseñas

![CI](https://github.com/Tobihub69/microservicio-resenas/actions/workflows/ci.yml/badge.svg)

Servicio para permitir a los usuarios calificar y comentar productos.

Características principales:
- API REST con endpoints: `POST /resenas`, `GET /resenas?producto_id=X`, `DELETE /resenas/{id}`, `GET /productos/{id}/promedio`.
- Persistencia propia en SQLite (`db/reviews.db`).
- Validaciones (calificación 1-5, campos obligatorios).

Instalación

1. Crear entorno virtual (opcional):

```bash
python -m venv .venv
.\.venv\Scripts\activate
```

2. Instalar dependencias:

```bash
pip install -r requirements.txt
```

Ejecución

```bash
uvicorn src.main:app --reload
```

Docker (opcional)

Construir y ejecutar con Docker:

```bash
docker build -t microservicio-resenas .
docker run -p 8000:8000 microservicio-resenas
```

O usando `docker-compose`:

```bash
docker-compose up --build
```

API Key (opcional)

Para proteger operaciones que modifican datos (crear/eliminar reseñas) puedes definir la variable de entorno `API_KEY`. Si no se define, el servicio permite acceso público.

Ejemplo local (PowerShell):

```powershell
$env:API_KEY = "mi_secreto"
uvicorn src.main:app --reload
```

Ejemplo `curl` usando header `X-API-Key`:

```bash
curl -X POST "http://127.0.0.1:8000/resenas" -H "Content-Type: application/json" -H "X-API-Key: mi_secreto" -d '{"producto_id":1,"usuario_id":99,"calificacion":5,"comentario":"Muy bueno"}'
```

Endpoints

- `POST /resenas` — Crear una reseña
  - Body JSON:

```json
{
  "producto_id": 1,
  "usuario_id": 42,
  "calificacion": 5,
  "comentario": "Muy buen producto"
}
```

- `GET /resenas?producto_id=1` — Listar reseñas de un producto

- `DELETE /resenas/{id}` — Eliminar una reseña

- `GET /productos/{id}/promedio` — Obtener promedio y cantidad de reseñas

Ejemplos (curl)

Crear reseña:

```bash
curl -X POST "http://127.0.0.1:8000/resenas" -H "Content-Type: application/json" -d "{\"producto_id\":1,\"usuario_id\":42,\"calificacion\":5,\"comentario\":\"Excelente\"}"
```

Listar reseñas de producto 1:

```bash
curl "http://127.0.0.1:8000/resenas?producto_id=1"
```

Eliminar reseña con id 2:

```bash
curl -X DELETE "http://127.0.0.1:8000/resenas/2"
```

Obtener promedio:

```bash
curl "http://127.0.0.1:8000/productos/1/promedio"
```

Diagrama de arquitectura

Ver archivo `diagram.svg` en la raíz del repositorio.

Evidencias

- Pruebas automatizadas de humo: `evidence/results.json` (incluye ejemplos de respuestas 201, 200, 204).
- Colección Postman: `postman_collection.json`.

Estructura de carpetas

- `src/` — código fuente
- `db/` — base de datos SQLite generada en tiempo de ejecución
- `requirements.txt` — dependencias
- `diagram.svg` — diagrama de arquitectura

Consideraciones

- Este servicio es autónomo y no depende de otros microservicios en tiempo de ejecución.
- Se evita que un mismo usuario califique dos veces el mismo producto (devuelve 409).

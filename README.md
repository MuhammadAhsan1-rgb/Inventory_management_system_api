# Inventory Management API

A RESTful Inventory Management API built with **Django REST Framework**. It manages product **categories** and **products** using `GenericAPIView` combined with DRF **mixins** (no `APIView`, no ViewSets), and includes custom serializer validation for business rules.

## Features

- Full CRUD for **Categories** and **Products**
- Class-based views built manually from `GenericAPIView` + `ListModelMixin`, `CreateModelMixin`, `RetrieveModelMixin`, `UpdateModelMixin` and `DestroyModelMixin`
- `PUT` (full update) and `PATCH` (partial update) support
- Computed, read-only `product_count` on every category
- Read-only `category_name` on every product (resolved from the related category)
- Field-level and object-level validation (including correct handling of partial `PATCH` updates)
- Category-to-product relation protected with `on_delete=PROTECT`
- Auto-managed `created_at` / `updated_at` timestamps

## Tech Stack

- Python 3
- Django
- Django REST Framework
- SQLite (default database)

## Data Model

**Category**

| Field | Type | Notes |
|---|---|---|
| `name` | CharField(100) | Unique |
| `description` | TextField | Optional |

**Product**

| Field | Type | Notes |
|---|---|---|
| `product_name` | CharField(100) | |
| `category` | ForeignKey → Category | `on_delete=PROTECT`, `related_name="products"` |
| `price` | DecimalField(10, 2) | Must be greater than 0 |
| `stock` | PositiveIntegerField | Cannot be negative |
| `is_available` | BooleanField | Default `True` |
| `created_at` | DateTimeField | Set automatically on creation |
| `updated_at` | DateTimeField | Updated automatically on every save |

## API Endpoints

Base URL: `http://127.0.0.1:8000/api/`

| Endpoint | Methods | Description |
|---|---|---|
| `/categories/` | `GET`, `POST` | List all categories / create a category |
| `/categories/<pk>/` | `GET`, `PUT`, `PATCH`, `DELETE` | Retrieve, update or delete a category |
| `/products/` | `GET`, `POST` | List all products / create a product |
| `/products/<pk>/` | `GET`, `PUT`, `PATCH`, `DELETE` | Retrieve, update or delete a product |

## Validation Rules

- **Category name** must be unique.
- **Price** must be greater than 0.
- **Stock** cannot be negative (enforced by `PositiveIntegerField`).
- A product with `stock = 0` **cannot** be marked `is_available = true`. This is checked on create, on `PUT`, and on `PATCH`. For a partial update, any field missing from the request is read from the existing product, so `PATCH {"stock": 0}` on an available product is correctly rejected.

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/<your-username>/<repo-name>.git
cd <repo-name>
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install django djangorestframework
```

### 4. Apply migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Run the server

```bash
python manage.py runserver
```

The API is now available at `http://127.0.0.1:8000/api/`. Because DRF's browsable API is enabled, you can also open any endpoint in the browser.

## Example Requests

### Create a category

`POST /api/categories/`

```json
{
  "name": "Mobiles",
  "description": "Smartphones and mobile accessories"
}
```

Response `201 Created`:

```json
{
  "id": 1,
  "product_count": 0,
  "name": "Mobiles",
  "description": "Smartphones and mobile accessories"
}
```

### Create a product

`POST /api/products/`

```json
{
  "product_name": "iPhone 15",
  "category": 1,
  "price": "250000.00",
  "stock": 10,
  "is_available": true
}
```

Response `201 Created`:

```json
{
  "id": 1,
  "category_name": "Mobiles",
  "product_name": "iPhone 15",
  "price": "250000.00",
  "stock": 10,
  "is_available": true,
  "created_at": "2026-09-20T08:37:38.165945Z",
  "updated_at": "2026-09-20T08:37:38.165945Z",
  "category": 1
}
```

### Partial update that breaks a business rule

`PATCH /api/products/1/`

```json
{
  "stock": 0
}
```

Response `400 Bad Request` (the product is still marked available):

```json
{
  "is_available": ["A product with 0 stock cannot be available."]
}
```

To set stock to zero, mark the product unavailable in the same request:

```json
{
  "stock": 0,
  "is_available": false
}
```

## Concepts Practiced

- `GenericAPIView` with manually wired mixins (HTTP handler → mixin method mapping)
- `ModelSerializer` with `SerializerMethodField` and `source=` for related data
- Reverse relations via `related_name`
- Field-level (`validate_<field>`) and object-level (`validate`) validation
- Handling `PUT` vs `PATCH` (`update` vs `partial_update`)
- Referential integrity with `on_delete=PROTECT`

## Roadmap

- [ ] Return a clean `400` response (instead of a server error) when deleting a category that still has products, by overriding `destroy()`
- [ ] `GET /api/categories/<pk>/products/` using `ListAPIView`, returning `404` for unknown categories
- [ ] Filtering on `/api/products/`: `?category=`, `?is_available=`, `?min_price=`, `?max_price=`, `?search=`
- [ ] Page-number pagination on the products list
- [ ] Optional: `?ordering=price` / `?ordering=-price`

## Author

**<Your Name>**
GitHub: [@<your-username>](https://github.com/<your-username>)

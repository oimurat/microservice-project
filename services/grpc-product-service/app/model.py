from db.db import get_connection

def get_product_by_id(id: str) -> dict:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id, name, price, description FROM products WHERE id = %s", (id,))
            row = cur.fetchone()
            if row:
                return dict(zip(['id', 'name', 'price', 'description'], row))
            return {}
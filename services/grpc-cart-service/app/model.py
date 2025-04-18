from db.db import get_connection

def create_cart(id: str, product_id: str, quantity: int):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO carts (id, product_id, quantity)
                VALUES (%s, %s, %s)
                ON CONFLICT (id) DO NOTHING;
            """, (id, product_id, quantity))
        conn.commit()

def get_cart_by_id(id: str) -> dict:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT id, product_id, quantity FROM carts WHERE id = %s
            """, (id,))
            row = cur.fetchone()
            if row:
                return dict(zip(['id', 'product_id', 'quantity'], row))
            return {}
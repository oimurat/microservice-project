from db.db import get_connection

def init_tables():
    with get_connection() as conn:
        with conn.cursor() as cur:
            # carts テーブル
            cur.execute("""
            CREATE TABLE IF NOT EXISTS carts (
                id TEXT PRIMARY KEY,
                product_id TEXT NOT NULL REFERENCES products(id),
                quantity INTEGER NOT NULL
            );
            """)

            # carts にテストデータ追加
            cur.execute("""
                INSERT INTO carts (id, product_id, quantity)
                VALUES 
                    ('c1', 'p1', 2),
                    ('c2', 'p2', 1)
                ON CONFLICT (id) DO NOTHING;
            """)

        conn.commit()
        print("✅ Tables created successfully.", flush=True)

if __name__ == "__main__":
    init_tables()

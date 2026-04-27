CREATE TABLE IF NOT EXISTS items (
    id   SERIAL PRIMARY KEY,
    name TEXT NOT NULL
);

INSERT INTO items (name) VALUES
    ('hello'),
    ('world'),
    ('devops')
ON CONFLICT DO NOTHING;

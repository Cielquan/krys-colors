/* Block comment */

WITH active_users AS (
    SELECT
        u.id,
        u.name,
        COUNT(o.id) AS order_count
    FROM users AS u
    LEFT JOIN orders AS o
        ON o.user_id = u.id
    WHERE u.active = TRUE
        AND u.created_at >= DATE '2024-01-01'
    GROUP BY u.id, u.name
    HAVING COUNT(o.id) > 0
)

SELECT
    id,
    name,
    CASE
        WHEN order_count >= 10 THEN 'gold'
        WHEN order_count > 0 THEN 'silver'
        ELSE NULL
    END AS tier
FROM active_users
ORDER BY order_count DESC
LIMIT 10;

INSERT INTO users (name, active)
VALUES ('Alice', TRUE);

UPDATE users
SET active = FALSE
WHERE id = 42;

DELETE FROM users
WHERE created_at < CURRENT_DATE - INTERVAL '1 year';

CREATE TABLE example (
    id INTEGER PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    score DECIMAL(10, 2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_name
ON example(name);

BEGIN TRANSACTION;

COMMIT;
ROLLBACK;

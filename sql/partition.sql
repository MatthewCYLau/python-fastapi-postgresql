CREATE TABLE transactions_2026_q2 PARTITION OF transactions
    FOR VALUES FROM ('2026-04-01') TO ('2026-07-01');

CREATE TABLE transactions_2026_q3 PARTITION OF transactions
    FOR VALUES FROM ('2026-07-01') TO ('2026-10-01');

CREATE TABLE transactions_default PARTITION OF transactions DEFAULT;
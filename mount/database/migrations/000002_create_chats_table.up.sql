CREATE TABLE chats (
    chat_id SERIAL NOT NULL PRIMARY KEY,
    name TEXT NOT NULL,
    topic TEXT NOT NULL,
    read_privileges INT NOT NULL,
    write_privileges INT NOT NULL,
    auto_join BOOLEAN NOT NULL,
    status VARCHAR(64) NOT NULL,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    created_by INT NOT NULL
);

COMMENT ON COLUMN chats.created_by IS 'reference to accounts.id';

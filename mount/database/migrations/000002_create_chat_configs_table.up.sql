CREATE TABLE chat_configs (
    config_id SERIAL NOT NULL PRIMARY KEY,
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

COMMENT ON COLUMN chat_configs.created_by IS 'reference to accounts.id';

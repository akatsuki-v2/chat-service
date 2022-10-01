CREATE TABLE chats (
    chat_id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    name TEXT NOT NULL,
    topic TEXT NOT NULL,
    read_privileges INT NOT NULL,
    write_privileges INT NOT NULL,
    auto_join BOOLEAN NOT NULL,
    status VARCHAR(64) NOT NULL,
    updated_at DATETIME NOT NULL DEFAULT NOW(),
    created_at DATETIME NOT NULL DEFAULT NOW(),
    created_by INT NOT NULL COMMENT 'reference to accounts.id'
);

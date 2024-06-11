-- schema.sql

-- Player Inventory
CREATE TABLE player_inventory (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    health INTEGER NOT NULL,
    max_health INTEGER NOT NULL
);


-- Items
CREATE TABLE item (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    damage INTEGER,
    heal INTEGER,
    type TEXT NOT NULL
);

-- Monsters
CREATE TABLE monster (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    health INTEGER NOT NULL,
    damage INTEGER NOT NULL
);
-- Inventory Items
CREATE TABLE inventory_items (
    player_inventory_id INTEGER,
    item_id INTEGER,
    PRIMARY KEY (player_inventory_id, item_id),
    FOREIGN KEY (player_inventory_id) REFERENCES player_inventory (id),
    FOREIGN KEY (item_id) REFERENCES item (id)
);

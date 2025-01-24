START TRANSACTION;

-- Get the last inserted vehicle ID (or fetch an existing one)
SET @vehicle_id = (SELECT id FROM vehicles WHERE path = '{vehicle_path}');

-- Insert into options
INSERT IGNORE INTO options (uri, display)
VALUES ('{option_uri}', '{option_display}');

-- Get the last inserted option ID (or fetch an existing one)
SET @option_id = (SELECT id FROM options WHERE uri = '{option_uri}');

-- Insert into vehicle_options
INSERT IGNORE INTO vehicle_options (vehicle_id, option_id)
VALUES (@vehicle_id, @option_id);

COMMIT
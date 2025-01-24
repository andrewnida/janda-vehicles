CREATE TABLE IF NOT EXISTS regions (
    id INTEGER PRIMARY KEY AUTO_INCREMENT COMMENT 'Unique primary key',
    uri VARCHAR(100) UNIQUE NOT NULL COMMENT 'URI encoded short text for the name, max length 100',
    display VARCHAR(100) UNIQUE NOT NULL COMMENT 'Short text for display name, max length 100',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT 'Timestamp when the record was created',
    last_modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT 'Timestamp when the record was modified'
) COMMENT = 'Country of origin';

CREATE TABLE IF NOT EXISTS makes (
    id INTEGER PRIMARY KEY AUTO_INCREMENT COMMENT 'Unique primary key',
    uri VARCHAR(100) UNIQUE NOT NULL COMMENT 'URI encoded short text for the name, max length 100',
    display VARCHAR(100) UNIQUE NOT NULL COMMENT 'Short text for display name, max length 100',
    path VARCHAR(255) NOT NULL COMMENT 'Relative URL for scraping path, max length 255',
    region_id INTEGER NOT NULL COMMENT 'Foreign key referencing regions table',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT 'Timestamp when the record was created',
    last_modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT 'Timestamp when the record was modified',
    CONSTRAINT fk_region FOREIGN KEY (region_id) REFERENCES regions(id) ON DELETE CASCADE ON UPDATE CASCADE
) COMMENT = 'Vehicle manufacturer';

CREATE TABLE IF NOT EXISTS models (
    id INT PRIMARY KEY AUTO_INCREMENT COMMENT 'Unique primary key',
    uri VARCHAR(100) UNIQUE NOT NULL COMMENT 'URI encoded short text for the name, max length 100',
    display VARCHAR(100) UNIQUE NOT NULL COMMENT 'Short text for display name, max length 100',
    make_id INT NOT NULL COMMENT 'Foreign key referencing makes table',
    path VARCHAR(255) NOT NULL COMMENT 'Relative URL for resource path, max length 255',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT 'Timestamp when the record was created',
    last_modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT 'Timestamp when the record was modified',
    CONSTRAINT fk_make FOREIGN KEY (make_id) REFERENCES makes(id) ON DELETE CASCADE ON UPDATE CASCADE
) COMMENT = 'Vehicle model';

CREATE TABLE IF NOT EXISTS frames (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT 'Unique primary key',
    uri VARCHAR(100) UNIQUE NOT NULL COMMENT 'URI encoded short text for the name, max length 100',
    display VARCHAR(100) UNIQUE NOT NULL COMMENT 'Short text for display name, max length 100',
    model_id INT NOT NULL COMMENT 'Foreign key referencing models table',
    path VARCHAR(255) NOT NULL COMMENT 'Relative URL for resource path, max length 255',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT 'Timestamp when the record was created',
    last_modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT 'Timestamp when the record was modified',
    CONSTRAINT fk_model_id FOREIGN KEY (model_id) REFERENCES models (id) ON DELETE CASCADE ON UPDATE CASCADE
) COMMENT='Vehicle frame code';

CREATE TABLE IF NOT EXISTS frame_nums (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT 'Unique primary key',
    num_from INT NOT NULL COMMENT 'Number from the start of the frame number range',
    num_to INT NOT NULL COMMENT 'Number from the end of the frame number range',
    date_from DATE NULL COMMENT 'Date from the start of the frame number range',
    date_to DATE NULL COMMENT 'Date from the end of the frame number range',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT 'Timestamp when the record was created',
    last_modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT 'Timestamp when the record was modified',
    UNIQUE (num_from, num_to)
) COMMENT = 'Vehicle frame numbers';

CREATE TABLE IF NOT EXISTS years (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT 'Unique primary key',
    year INT UNIQUE NOT NULL COMMENT 'Integer for year of production',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT 'Timestamp when the record was created',
    last_modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT 'Timestamp when the record was modified',
    CHECK (year >= 1970 AND year <= 2100)
) COMMENT = 'Vehicle production years';

CREATE TABLE IF NOT EXISTS body_styles (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT 'Unique primary key',
    body ENUM('coupe', 'hatch', 'sedan', 'van', 'truck') NOT NULL COMMENT 'Reference to the body_style enum',
    doors INT NOT NULL COMMENT 'Number of doors for the body style',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT 'Timestamp when the record was created',
    last_modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT 'Timestamp when the record was modified',
    CHECK (doors BETWEEN 2 AND 5),
    UNIQUE (body, doors)
) COMMENT = 'Vehicle body styles';

CREATE TABLE IF NOT EXISTS transmissions (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT 'Unique primary key',
    code VARCHAR(50) NOT NULL COMMENT 'Transmission code, max length 50',
    speeds INT NOT NULL COMMENT 'Number of speeds in the transmission',
    auto BOOLEAN NOT NULL COMMENT 'Indicates whether the transmission is automatic (true) or manual (false)',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT 'Timestamp when the record was created',
    last_modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT 'Timestamp when the record was modified',
    CHECK (speeds BETWEEN 0 AND 6),
    UNIQUE (code, speeds)
) COMMENT = 'Vehicle transmission details and characteristics';

CREATE TABLE IF NOT EXISTS trims (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT 'Unique primary key',
    uri VARCHAR(100) NOT NULL UNIQUE COMMENT 'Short text for trim name, max length 100',
    display VARCHAR(100) NOT NULL UNIQUE COMMENT 'Short text for display name, max length 100',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT 'Timestamp when the record was created',
    last_modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT 'Timestamp when the record was modified'
) COMMENT = 'Vehicle trims';

CREATE TABLE IF NOT EXISTS variants (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT 'Unique primary key',
    uri VARCHAR(100) NOT NULL UNIQUE COMMENT 'Short text for variant name, max length 100',
    display VARCHAR(100) NOT NULL UNIQUE COMMENT 'Short text for display name, max length 100',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT 'Timestamp when the record was created',
    last_modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT 'Timestamp when the record was modified'
) COMMENT = 'Vehicle trim variants';

CREATE TABLE IF NOT EXISTS engines (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT 'Unique primary key',
    code VARCHAR(50) NOT NULL COMMENT 'Engine code, max length 50',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT 'Timestamp when the record was created',
    last_modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT 'Timestamp when the record was modified'
) COMMENT = 'Vehicle engine details';

CREATE TABLE IF NOT EXISTS vehicles (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT 'Unique primary key',
    frame_id INT NULL COMMENT 'Optional, foreign key referencing frames table',
    frame_nums_id INT NULL COMMENT 'Optional, must be filled if years_id is empty, foreign key referencing frame_nums table',
    year_id INT NULL COMMENT 'Optional, must be filled if frame_nums_id is empty, foreign key referencing years table',
    body_style_id INT NOT NULL COMMENT 'Reference to the body style',
    trim_id INT NOT NULL COMMENT 'Reference to the trim from the trims table',
    variant_id INT NULL COMMENT 'Reference to the variant from the variants table',
    transmission_id INT NOT NULL COMMENT 'Reference to the transmission information',
    engine_id INT NULL COMMENT 'Reference to the engine information',
    path VARCHAR(255) NOT NULL COMMENT 'Path to the vehicle (URL or relative)',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT 'Timestamp when the record was created',
    last_modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT 'Timestamp when the record was modified',
    CONSTRAINT fk_frame_id FOREIGN KEY (frame_id) REFERENCES frames(id) ON DELETE SET NULL ON UPDATE CASCADE,
    CONSTRAINT fk_frame_nums_id FOREIGN KEY (frame_nums_id) REFERENCES frame_nums(id) ON DELETE SET NULL ON UPDATE CASCADE,
    CONSTRAINT fk_year_id FOREIGN KEY (year_id) REFERENCES years(id) ON DELETE SET NULL ON UPDATE CASCADE,
    CONSTRAINT fk_body_style_id FOREIGN KEY (body_style_id) REFERENCES body_styles(id) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_trim_id FOREIGN KEY (trim_id) REFERENCES trims(id) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_variant_id FOREIGN KEY (variant_id) REFERENCES variants(id) ON DELETE SET NULL ON UPDATE CASCADE,
    CONSTRAINT fk_transmission_id FOREIGN KEY (transmission_id) REFERENCES transmissions(id) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_engine_id FOREIGN KEY (engine_id) REFERENCES engines(id) ON DELETE CASCADE ON UPDATE CASCADE
) COMMENT = 'Vehicle details';

CREATE TABLE IF NOT EXISTS options (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT 'Unique primary key',
    uri VARCHAR(100) NOT NULL UNIQUE COMMENT 'Short text for option name, max length 100',
    display VARCHAR(100) NOT NULL UNIQUE COMMENT 'Name of the option (e.g., AC, power locks)',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT 'Timestamp when the record was created',
    last_modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT 'Timestamp when the record was modified'
) COMMENT = 'Vehicle options';

CREATE TABLE IF NOT EXISTS vehicle_options (
    vehicle_id INT NOT NULL COMMENT 'Reference to the vehicle',
    option_id INT NOT NULL COMMENT 'Reference to the option',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT 'Timestamp when the record was created',
    last_modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT 'Timestamp when the record was modified',
    CONSTRAINT fk_vehicle_id FOREIGN KEY (vehicle_id) REFERENCES vehicles(id) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_option_id FOREIGN KEY (option_id) REFERENCES options(id) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT vehicle_option_unique UNIQUE (vehicle_id, option_id)
) COMMENT = 'Map options to vehicles'

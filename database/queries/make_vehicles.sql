CREATE TABLE IF NOT EXISTS regions (
    id SERIAL PRIMARY KEY,
    uri VARCHAR(100) UNIQUE NOT NULL,
    display VARCHAR(100) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

COMMENT ON TABLE regions IS 'Country of origin';
COMMENT ON COLUMN regions.id IS 'Unique primary key';
COMMENT ON COLUMN regions.uri IS 'URI encoded short text for the name, max length 100';
COMMENT ON COLUMN regions.display IS 'Short text for display name, max length 100';
COMMENT ON COLUMN regions.created_at IS 'Timestamp when the record was created';
COMMENT ON COLUMN regions.last_modified IS 'Timestamp when the record was modified';

CREATE TABLE IF NOT EXISTS makes (
    id SERIAL PRIMARY KEY,
    uri VARCHAR(100) UNIQUE NOT NULL,
    display VARCHAR(100) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

COMMENT ON TABLE makes IS 'Vehicle manufacturer';
COMMENT ON COLUMN makes.id IS 'Unique primary key';
COMMENT ON COLUMN makes.uri IS 'URI encoded short text for the name, max length 100';
COMMENT ON COLUMN makes.display IS 'Short text for display name, max length 100';
COMMENT ON COLUMN makes.created_at IS 'Timestamp when the record was created';
COMMENT ON COLUMN makes.last_modified IS 'Timestamp when the record was modified';

CREATE TABLE IF NOT EXISTS models (
    id SERIAL PRIMARY KEY,
    uri VARCHAR(100) UNIQUE NOT NULL,
    display VARCHAR(100) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

COMMENT ON TABLE models IS 'Vehicle model';
COMMENT ON COLUMN models.id IS 'Unique primary key';
COMMENT ON COLUMN models.uri IS 'URI encoded short text for the name, max length 100';
COMMENT ON COLUMN models.display IS 'Short text for display name, max length 100';
COMMENT ON COLUMN models.created_at IS 'Timestamp when the record was created';
COMMENT ON COLUMN models.last_modified IS 'Timestamp when the record was modified';

CREATE TABLE IF NOT EXISTS frames (
    id SERIAL PRIMARY KEY,
    uri VARCHAR(100) UNIQUE NOT NULL,
    display VARCHAR(100) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

COMMENT ON TABLE frames IS 'Vehicle frame';
COMMENT ON COLUMN frames.id IS 'Unique primary key';
COMMENT ON COLUMN frames.uri IS 'URI encoded short text for the name, max length 100';
COMMENT ON COLUMN frames.display IS 'Short text for display name, max length 100';
COMMENT ON COLUMN frames.created_at IS 'Timestamp when the record was created';
COMMENT ON COLUMN frames.last_modified IS 'Timestamp when the record was modified';

CREATE TABLE IF NOT EXISTS chasiss (
    id SERIAL PRIMARY KEY,
    uri VARCHAR(100) UNIQUE NOT NULL,
    display VARCHAR(100) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

COMMENT ON TABLE chasiss IS 'Vehicle chasiss';
COMMENT ON COLUMN chasiss.id IS 'Unique primary key';
COMMENT ON COLUMN chasiss.uri IS 'URI encoded short text for the name, max length 100';
COMMENT ON COLUMN chasiss.display IS 'Short text for display name, max length 100';
COMMENT ON COLUMN chasiss.created_at IS 'Timestamp when the record was created';
COMMENT ON COLUMN chasiss.last_modified IS 'Timestamp when the record was modified';

CREATE TABLE IF NOT EXISTS frames_chasiss (
    id SERIAL PRIMARY KEY,
    frame_id INT NOT NULL REFERENCES frames(id) ON DELETE CASCADE ON UPDATE CASCADE,
    chasiss_id INT NOT NULL REFERENCES chasiss(id) ON DELETE CASCADE ON UPDATE CASCADE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (frame_id, chasiss_id)
);

COMMENT ON TABLE frames_chasiss IS 'Mapping of frames to their chasiss';
COMMENT ON COLUMN frames_chasiss.id IS 'Unique primary key';
COMMENT ON COLUMN frames_chasiss.frame_id IS 'Foreign key referencing frames table';
COMMENT ON COLUMN frames_chasiss.chasiss_id IS 'Foreign key referencing chasiss table';
COMMENT ON COLUMN frames_chasiss.created_at IS 'Timestamp when the record was created';
COMMENT ON COLUMN frames_chasiss.last_modified IS 'Timestamp when the record was modified';

CREATE TABLE IF NOT EXISTS frame_nums (
    id SERIAL PRIMARY KEY,
    num_from INT NOT NULL,
    num_to INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (num_from, num_to)
);

COMMENT ON TABLE frame_nums IS 'Vehicle frame numbers';
COMMENT ON COLUMN frame_nums.id IS 'Unique primary key';
COMMENT ON COLUMN frame_nums.num_from IS 'Number from the start of the frame number range';
COMMENT ON COLUMN frame_nums.num_to IS 'Number from the end of the frame number range';
COMMENT ON COLUMN frame_nums.created_at IS 'Timestamp when the record was created';
COMMENT ON COLUMN frame_nums.last_modified IS 'Timestamp when the record was modified';

CREATE TABLE IF NOT EXISTS frames_chasiss_frame_nums (
    id SERIAL PRIMARY KEY,
    frames_chasiss_id INT NOT NULL REFERENCES frames_chasiss(id) ON DELETE CASCADE ON UPDATE CASCADE,
    frame_nums_id INT NOT NULL REFERENCES frame_nums(id) ON DELETE CASCADE ON UPDATE CASCADE,
    date_from DATE,
    date_to DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (frames_chasiss_id, frame_nums_id)
);

COMMENT ON TABLE frames_chasiss_frame_nums IS 'Vehicle frame numbers';
COMMENT ON COLUMN frames_chasiss_frame_nums.id IS 'Unique primary key';
COMMENT ON COLUMN frames_chasiss_frame_nums.frames_chasiss_id IS 'Foreign key referencing frames_chasiss table';
COMMENT ON COLUMN frames_chasiss_frame_nums.frame_nums_id IS 'Foreign key referencing frame_nums table';
COMMENT ON COLUMN frames_chasiss_frame_nums.date_from IS 'Date from the start of the frame number range';
COMMENT ON COLUMN frames_chasiss_frame_nums.date_to IS 'Date from the end of the frame number range';
COMMENT ON COLUMN frames_chasiss_frame_nums.created_at IS 'Timestamp when the record was created';
COMMENT ON COLUMN frames_chasiss_frame_nums.last_modified IS 'Timestamp when the record was modified';

CREATE TABLE IF NOT EXISTS body_styles (
    id SERIAL PRIMARY KEY,
    body VARCHAR(50) NOT NULL,
    doors INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (body, doors)
);

COMMENT ON TABLE body_styles IS 'Vehicle body styles';
COMMENT ON COLUMN body_styles.id IS 'Unique primary key';
COMMENT ON COLUMN body_styles.body IS 'Reference to the body_style enum';
COMMENT ON COLUMN body_styles.doors IS 'Number of doors for the body style';
COMMENT ON COLUMN body_styles.created_at IS 'Timestamp when the record was created';
COMMENT ON COLUMN body_styles.last_modified IS 'Timestamp when the record was modified';

CREATE TABLE IF NOT EXISTS transmissions (
    id SERIAL PRIMARY KEY,
    code VARCHAR(50) NOT NULL,
    speeds VARCHAR(50) NOT NULL,
    auto BOOLEAN NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (code, speeds)
);

COMMENT ON TABLE transmissions IS 'Vehicle transmission details and characteristics';
COMMENT ON COLUMN transmissions.id IS 'Unique primary key';
COMMENT ON COLUMN transmissions.code IS 'Transmission code, max length 50';
COMMENT ON COLUMN transmissions.speeds IS 'Number of speeds in the transmission';
COMMENT ON COLUMN transmissions.auto IS 'Indicates whether the transmission is automatic (true) or manual (false)';
COMMENT ON COLUMN transmissions.created_at IS 'Timestamp when the record was created';
COMMENT ON COLUMN transmissions.last_modified IS 'Timestamp when the record was modified';

CREATE TABLE IF NOT EXISTS trims (
    id SERIAL PRIMARY KEY,
    uri VARCHAR(100) NOT NULL UNIQUE,
    display VARCHAR(100) NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

COMMENT ON TABLE trims IS 'Vehicle trims';
COMMENT ON COLUMN trims.id IS 'Unique primary key';
COMMENT ON COLUMN trims.uri IS 'Short text for trim name, max length 100';
COMMENT ON COLUMN trims.display IS 'Short text for display name, max length 100';
COMMENT ON COLUMN trims.created_at IS 'Timestamp when the record was created';
COMMENT ON COLUMN trims.last_modified IS 'Timestamp when the record was modified';

CREATE TABLE IF NOT EXISTS variants (
    id SERIAL PRIMARY KEY,
    uri VARCHAR(100) NOT NULL UNIQUE,
    display VARCHAR(100) NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

COMMENT ON TABLE variants IS 'Vehicle trim variants';
COMMENT ON COLUMN variants.id IS 'Unique primary key';
COMMENT ON COLUMN variants.uri IS 'Short text for variant name, max length 100';
COMMENT ON COLUMN variants.display IS 'Short text for display name, max length 100';
COMMENT ON COLUMN variants.created_at IS 'Timestamp when the record was created';
COMMENT ON COLUMN variants.last_modified IS 'Timestamp when the record was modified';

CREATE TABLE IF NOT EXISTS engines (
    id SERIAL PRIMARY KEY,
    code VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

COMMENT ON TABLE engines IS 'Vehicle engine details';
COMMENT ON COLUMN engines.id IS 'Unique primary key';
COMMENT ON COLUMN engines.code IS 'Engine code, max length 50';
COMMENT ON COLUMN engines.created_at IS 'Timestamp when the record was created';
COMMENT ON COLUMN engines.last_modified IS 'Timestamp when the record was modified';

CREATE TABLE IF NOT EXISTS area_codes (
    id SERIAL PRIMARY KEY,
    uri VARCHAR(100) UNIQUE NOT NULL,
    display VARCHAR(100) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

COMMENT ON TABLE area_codes IS 'Destination area code';
COMMENT ON COLUMN area_codes.id IS 'Unique primary key';
COMMENT ON COLUMN area_codes.uri IS 'URI encoded short text for the name, max length 100';
COMMENT ON COLUMN area_codes.display IS 'Short text for display name, max length 100';
COMMENT ON COLUMN area_codes.created_at IS 'Timestamp when the record was created';
COMMENT ON COLUMN area_codes.last_modified IS 'Timestamp when the record was modified';

CREATE TABLE IF NOT EXISTS vehicles (
    id SERIAL PRIMARY KEY,
    region_id INT NOT NULL REFERENCES regions(id) ON DELETE CASCADE ON UPDATE CASCADE,
    make_id INT NOT NULL REFERENCES makes(id) ON DELETE CASCADE ON UPDATE CASCADE,
    model_id INT NOT NULL REFERENCES models(id) ON DELETE CASCADE ON UPDATE CASCADE,
    year INT,
    frames_chasiss_frame_nums_id INT REFERENCES frames_chasiss_frame_nums(id) ON DELETE CASCADE ON UPDATE CASCADE,
    body_style_id INT NOT NULL REFERENCES body_styles(id) ON DELETE CASCADE ON UPDATE CASCADE,
    transmission_id INT NOT NULL REFERENCES transmissions(id) ON DELETE CASCADE ON UPDATE CASCADE,
    trim_id INT NOT NULL REFERENCES trims(id) ON DELETE CASCADE ON UPDATE CASCADE,
    variant_id INT REFERENCES variants(id) ON DELETE CASCADE ON UPDATE CASCADE,
    engine_id INT REFERENCES engines(id) ON DELETE CASCADE ON UPDATE CASCADE,
    area_code_id INT REFERENCES area_codes(id) ON DELETE CASCADE ON UPDATE CASCADE,
    scrape_path VARCHAR(255) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

COMMENT ON TABLE vehicles IS 'Vehicle details';
COMMENT ON COLUMN vehicles.id IS 'Unique primary key';
COMMENT ON COLUMN vehicles.region_id IS 'Reference to the region from the region table';
COMMENT ON COLUMN vehicles.make_id IS 'Reference to the make from the makes table';
COMMENT ON COLUMN vehicles.model_id IS 'Reference to the model from the models table';
COMMENT ON COLUMN vehicles.year IS 'For USDM, must be filled if frames_chasiss_frame_nums is empty';
COMMENT ON COLUMN vehicles.frames_chasiss_frame_nums_id IS 'For JDM, foreign key referencing frames_chasiss_frame_nums table';
COMMENT ON COLUMN vehicles.body_style_id IS 'Reference to the body style';
COMMENT ON COLUMN vehicles.transmission_id IS 'Reference to the transmission information';
COMMENT ON COLUMN vehicles.trim_id IS 'Reference to the trim from the trims table';
COMMENT ON COLUMN vehicles.variant_id IS 'Reference to the variant from the variants table';
COMMENT ON COLUMN vehicles.engine_id IS 'Reference to the engine information';
COMMENT ON COLUMN vehicles.area_code_id IS 'Reference to the area_code information';
COMMENT ON COLUMN vehicles.scrape_path IS 'Path to the vehicle (URL or relative)';
COMMENT ON COLUMN vehicles.created_at IS 'Timestamp when the record was created';
COMMENT ON COLUMN vehicles.last_modified IS 'Timestamp when the record was modified';

CREATE TABLE IF NOT EXISTS options (
    id SERIAL PRIMARY KEY,
    uri VARCHAR(100) NOT NULL UNIQUE,
    display VARCHAR(100) NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

COMMENT ON TABLE options IS 'Vehicle options';
COMMENT ON COLUMN options.id IS 'Unique primary key';
COMMENT ON COLUMN options.uri IS 'Short text for option name, max length 100';
COMMENT ON COLUMN options.display IS 'Name of the option (e.g., AC, power locks)';
COMMENT ON COLUMN options.created_at IS 'Timestamp when the record was created';
COMMENT ON COLUMN options.last_modified IS 'Timestamp when the record was modified';

CREATE TABLE IF NOT EXISTS vehicle_options (
    vehicle_id INT NOT NULL REFERENCES vehicles(id) ON DELETE CASCADE ON UPDATE CASCADE,
    option_id INT NOT NULL REFERENCES options(id) ON DELETE CASCADE ON UPDATE CASCADE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (vehicle_id, option_id)
);

COMMENT ON TABLE vehicle_options IS 'Map options to vehicles';
COMMENT ON COLUMN vehicle_options.vehicle_id IS 'Reference to the vehicle';
COMMENT ON COLUMN vehicle_options.option_id IS 'Reference to the option';
COMMENT ON COLUMN vehicle_options.created_at IS 'Timestamp when the record was created';
COMMENT ON COLUMN vehicle_options.last_modified IS 'Timestamp when the record was modified';

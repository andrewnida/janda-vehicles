START TRANSACTION;

-- Insert into regions
INSERT IGNORE INTO regions (uri, display)
VALUES ('{region_uri}', '{region_display}');

-- Get the last inserted ID (or fetch an existing one)
SET @region_id = (SELECT id FROM regions WHERE uri = '{region_uri}');

-- Insert into makes
INSERT IGNORE INTO makes (uri, display, path, region_id)
VALUES ('{make_uri}', '{make_display}', '{make_path}', @region_id);

-- Get the last inserted make ID (or fetch an existing one)
SET @make_id = (SELECT id FROM makes WHERE uri = '{make_uri}');

-- Insert into models
INSERT IGNORE INTO models (uri, display, make_id, path)
VALUES ('{model_uri}', '{model_display}', @make_id, '{model_path}');

-- Get the last inserted model ID (or fetch an existing one)
SET @model_id = (SELECT id FROM models WHERE uri = '{model_uri}');

-- Insert into frames
INSERT IGNORE INTO frames (uri, display, model_id, path)
VALUES ('{frame_uri}', '{frame_display}', @model_id, '{frame_path}');

-- Get the last inserted frame ID (or fetch an existing one)
SET @frame_id = (SELECT id FROM frames WHERE uri = '{frame_uri}');

-- Insert into frame_nums
INSERT IGNORE INTO frame_nums (num_from, num_to)
VALUES ({frame_num_from}, {frame_num_to});

-- Get the last inserted frame_nums ID (or fetch an existing one)
SET @frame_nums_id = (SELECT id FROM frame_nums WHERE num_from = {frame_num_from} AND num_to = {frame_num_to});

-- Insert into years (only if year is valid)
INSERT IGNORE INTO years (year)
SELECT {year}
WHERE {year} >= 1970 AND {year} <= 2100;

-- Get the last inserted year ID (or fetch an existing one)
SET @year_id = (SELECT id FROM years WHERE year = {year});

-- Insert into body_styles
INSERT IGNORE INTO body_styles (body, doors)
SELECT 
    CASE 
        WHEN {doors} = 2 THEN 'coupe'
        WHEN {doors} = 3 THEN 'hatch'
        WHEN {doors} = 4 THEN 'sedan'
        WHEN {doors} = 5 THEN 'van'
        ELSE NULL
    END AS body,
    {doors}
WHERE {doors} BETWEEN 2 AND 5;

-- Get the last inserted body_style ID (or fetch an existing one)
SET @body_style_id = (SELECT id FROM body_styles WHERE doors = {doors} LIMIT 1);

-- Insert into transmissions
INSERT IGNORE INTO transmissions (code, speeds, auto)
VALUES ('{transmission_code}', {transmission_speeds}, {transmission_auto});

-- Get the last inserted transmission ID (or fetch an existing one)
SET @transmission_id = (SELECT id FROM transmissions WHERE code = '{transmission_code}');

-- Insert into trims
INSERT IGNORE INTO trims (uri, display)
VALUES ('{trim_uri}', '{trim_display}');

-- Get the last inserted trim ID (or fetch an existing one)
SET @trim_id = (SELECT id FROM trims WHERE uri = '{trim_uri}');

-- Insert into variants
INSERT INTO variants (uri, display)
SELECT '{variant_uri}', '{variant_display}'
WHERE '{variant_uri}' != 'None' AND '{variant_display}' != 'None';

-- Get the last inserted variant ID (or fetch an existing one)
SET @variant_id = (SELECT id FROM variants WHERE uri = '{variant_uri}');

-- Insert into vehicles
INSERT IGNORE INTO vehicles (frame_id, frame_nums_id, year_id, body_style_id, trim_id, variant_id, transmission_id, path)
VALUES (@frame_id, @frame_nums_id, @year_id, @body_style_id, @trim_id, @variant_id, @transmission_id, '{vehicle_path}');

COMMIT

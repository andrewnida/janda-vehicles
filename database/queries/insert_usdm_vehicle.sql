START TRANSACTION;

-- Insert into regions
INSERT IGNORE INTO regions (uri, display)
VALUES ("{region_uri}", "{region_display}");

-- Get the last inserted ID (or fetch an existing one)
SET @region_id = (SELECT id FROM regions WHERE uri = "{region_uri}");

-- Insert into makes
INSERT IGNORE INTO makes (uri, display)
VALUES ("{make_uri}", "{make_display}");

-- Get the last inserted make ID (or fetch an existing one)
SET @make_id = (SELECT id FROM makes WHERE uri = "{make_uri}");

-- Insert into models
INSERT IGNORE INTO models (uri, display)
VALUES ("{model_uri}", "{model_display}");

-- Get the last inserted model ID (or fetch an existing one)
SET @model_id = (SELECT id FROM models WHERE uri = '{model_uri}');

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
VALUES ("{transmission_code}", "{transmission_speeds}", {transmission_auto});

-- Get the last inserted transmission ID (or fetch an existing one)
SET @transmission_id = (SELECT id FROM transmissions WHERE code = "{transmission_code}" AND speeds = "{transmission_speeds}");

-- Insert into trims
INSERT IGNORE INTO trims (uri, display)
VALUES ("{trim_uri}", "{trim_display}");

-- Get the last inserted trim ID (or fetch an existing one)
SET @trim_id = (SELECT id FROM trims WHERE uri = "{trim_uri}");

-- Insert into variants
INSERT IGNORE INTO variants (uri, display)
VALUES ("{variant_uri}", "{variant_display}");

-- Get the last inserted variant ID (or fetch an existing one)
SET @variant_id = (SELECT id FROM variants WHERE uri = "{variant_uri}");

-- Insert into area_codes
INSERT IGNORE INTO area_codes (uri, display)
VALUES ("{area_code_uri}", "{area_code_display}");

-- Get the last inserted area_code ID (or fetch an existing one)
SET @area_code_id = (SELECT id FROM area_codes WHERE uri = "{area_code_uri}");

-- Insert into vehicles
INSERT IGNORE INTO vehicles (
    region_id,
    make_id,
    model_id, 
    year,
    body_style_id, 
    transmission_id, 
    trim_id, 
    variant_id, 
    area_code_id, 
    scrape_path
)
VALUES (
    @region_id,
    @make_id,
    @model_id, 
    {year}, 
    @body_style_id, 
    @transmission_id, 
    @trim_id, 
    @variant_id, 
    @area_code_id, 
    "{vehicle_path}"
);

COMMIT

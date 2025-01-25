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
INSERT IGNORE INTO models (uri, display, make_id)
VALUES ("{model_uri}", "{model_display}", @make_id);

-- Get the last inserted model ID (or fetch an existing one)
SET @model_id = (SELECT id FROM models WHERE uri = '{model_uri}');

-- Insert into frames
INSERT IGNORE INTO frames (uri, display)
VALUES ("{frame_uri}", "{frame_display}");

-- Get the last inserted frame ID (or fetch an existing one)
SET @frame_id = (SELECT id FROM frames WHERE uri = '{frame_uri}');

-- Insert into chasiss
INSERT IGNORE INTO chasiss (uri, display)
VALUES ("{chasiss_uri}", "{chasiss_display}");

-- Get the last inserted frame ID (or fetch an existing one)
SET @chasiss_id = (SELECT id FROM chasiss WHERE uri = '{chasiss_uri}');

-- Insert into frames_chasiss
INSERT IGNORE INTO frames_chasiss (frame_id, chasiss_id)
VALUES (@frame_id, @chasiss_id);

-- Get the last inserted frames_chasiss ID (or fetch an existing one)
SET @frames_chasiss_id = (SELECT id FROM frames_chasiss WHERE frame_id = @frame_id AND chasiss_id = @chasiss_id);

-- Insert into frame_nums
INSERT IGNORE INTO frame_nums (num_from, num_to)
VALUES ({frame_num_from}, {frame_num_to});

-- Get the last inserted frame_nums ID (or fetch an existing one)
SET @frame_nums_id = (SELECT id FROM frame_nums WHERE num_from = {frame_num_from} AND num_to = {frame_num_to});

-- Insert into frames_chasiss_frame_nums
INSERT IGNORE INTO frames_chasiss_frame_nums (frames_chasiss_id, frame_nums_id)
VALUES (@frames_chasiss_id, @frame_nums_id);

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

-- Insert into vehicles
INSERT IGNORE INTO vehicles (
    region_id, 
    model_id, 
    frames_chasiss_id,
    frame_nums_id,
    body_style_id, 
    transmission_id, 
    trim_id, 
    path
)
VALUES (
    @region_id, 
    @model_id,
    @frames_chasiss_id,
    @frame_nums_id,
    @body_style_id, 
    @transmission_id, 
    @trim_id, 
    "{vehicle_path}"
);

COMMIT

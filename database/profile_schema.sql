CREATE TABLE IF NOT EXISTS profile_runs (

    profile_id INT AUTO_INCREMENT PRIMARY KEY,

    profile_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    total_rows INT,

    total_columns INT,

    duplicate_rows INT,

    missing_cells INT

);


CREATE TABLE IF NOT EXISTS profile_column_summary (

    id INT AUTO_INCREMENT PRIMARY KEY,

    profile_id INT,

    column_name VARCHAR(100),

    data_type VARCHAR(50),

    missing_values INT,

    unique_values INT

);
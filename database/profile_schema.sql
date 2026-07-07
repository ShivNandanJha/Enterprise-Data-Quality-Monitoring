USE enterprise_quality;

CREATE TABLE IF NOT EXISTS data_profile (

    id INT AUTO_INCREMENT PRIMARY KEY,

    profile_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    column_name VARCHAR(100),

    data_type VARCHAR(50),

    total_rows INT,

    null_count INT,

    null_percentage DECIMAL(8,2),

    unique_values INT,

    minimum_value VARCHAR(255),

    maximum_value VARCHAR(255),

    average_value DOUBLE

);
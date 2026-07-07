USE enterprise_quality;

CREATE TABLE IF NOT EXISTS pipeline_runs (

    run_id INT AUTO_INCREMENT PRIMARY KEY,

    execution_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    total_rows INT,

    loaded_rows INT,

    rejected_rows INT,

    quality_score DECIMAL(5,2),

    execution_status VARCHAR(20),

    execution_duration DOUBLE,

    remarks TEXT

);
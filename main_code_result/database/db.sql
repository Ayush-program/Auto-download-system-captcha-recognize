CREATE DATABASE tender_db;
USE tender_db;

CREATE TABLE kerala_tender (
    id INT AUTO_INCREMENT PRIMARY KEY,
    tender_id VARCHAR(100) NOT NULL,
    pdf_path VARCHAR(255),
    state varchar(50),
    downloaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

USE tender_db;
SHOW TABLES;


SELECT * FROM tender_pdfs;















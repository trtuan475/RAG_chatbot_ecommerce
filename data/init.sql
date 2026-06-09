USE rag_chatbot_db;

# bảng 1: products
CREATE TABLE IF NOT EXISTS products (
    id INT PRIMARY KEY,
    gender VARCHAR(50),
    masterCategory VARCHAR(100),
    subCategory VARCHAR(100),
    articleType VARCHAR(100),
    baseColour VARCHAR(50),
    season VARCHAR(50),
    year INT,
    `usage` VARCHAR(50),
    productDisplayName VARCHAR(255)
);

# bảng 2: product_images
CREATE TABLE IF NOT EXISTS product_images (
    filename VARCHAR(100) PRIMARY KEY,
    link TEXT,
    style_id INT
);

# gán styles.csv vào bảng products
LOAD DATA INFILE '/var/lib/mysql-files/styles.csv'
INTO TABLE products
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"' 
LINES TERMINATED BY '\n' 
IGNORE 1 LINES   
(id, gender, masterCategory, subCategory, articleType, baseColour, season, year, `usage`, productDisplayName);

# gán images.csv vào bảng 
LOAD DATA INFILE '/var/lib/mysql-files/images.csv'
INTO TABLE product_images
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"' 
LINES TERMINATED BY '\n' 
IGNORE 1 LINES   
(@vfilename, @vlink) 
SET 
    filename = @vfilename,
    link = @vlink,
    style_id = CAST(SUBSTRING_INDEX(@vfilename, '.', 1) AS UNSIGNED); -- trích xuất số từ tên file 

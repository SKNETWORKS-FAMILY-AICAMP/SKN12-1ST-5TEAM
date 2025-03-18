CREATE DATABASE IF NOT EXISTS car_data;
USE car_data;

CREATE TABLE IF NOT EXISTS car_registration (
    id INT AUTO_INCREMENT PRIMARY KEY,
    `year_month` VARCHAR(10),  -- "2011-01" 형식
    city VARCHAR(20),        -- "서울", "부산" 같은 시도명
    district VARCHAR(30),    -- "강남구", "중구" 같은 시군구

    passenger_official INT,  -- 승용 관용
    passenger_private INT,   -- 승용 자가용
    passenger_business INT,  -- 승용 영업용
    passenger_total INT,     -- 승용 계

    van_official INT,        -- 승합 관용
    van_private INT,         -- 승합 자가용
    van_business INT,        -- 승합 영업용
    van_total INT,           -- 승합 계

    truck_official INT,      -- 화물 관용
    truck_private INT,       -- 화물 자가용
    truck_business INT,      -- 화물 영업용
    truck_total INT,         -- 화물 계

    special_official INT,    -- 특수 관용
    special_private INT,     -- 특수 자가용
    special_business INT,    -- 특수 영업용
    special_total INT        -- 특수 계
);

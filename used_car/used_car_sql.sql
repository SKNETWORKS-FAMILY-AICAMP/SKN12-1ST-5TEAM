SELECT * FROM used_car.used_car_table;

# 외래키 생성
ALTER TABLE used_car.used_car_table
ADD COLUMN brand_num INT;

# 브랜드 테이블 생성
CREATE TABLE used_car.car_brands (
    brand_num INT AUTO_INCREMENT PRIMARY KEY,
    car_brand VARCHAR(50) NOT NULL
);

# 브랜드 테이블 데이터 넣기
INSERT INTO used_car.car_brands (car_brand) VALUES
('현대'),
('르노코리아'),
('기아'),
('쉐보레'),
('KGM'),
('제네시스'),
('기타'),
('벤츠'),
('BMW'),
('AUDI'),
('폭스바겐'),
('렉서스'),
('볼보'),
('미니'),
('도요타'),
('포드'),
('랜드로버'),
('포르쉐'),
('크라이슬러'),
('혼다'),
('쉐보레'),
('푸조'),
('테슬라'),
('닛산'),
('재규어'),
('링컨'),
('인피니티'),
('캐딜락'),
('시트로앵'),
('마세라티'),
('폴스타'),
('벤틀리'),
('람보르기니'),
('피아트'),
('롤스로이스'),
('gmc'),
('ds'),
('페라리');

# 외래키 연결
ALTER TABLE used_car.used_car_table
ADD CONSTRAINT fk_car_brand
FOREIGN KEY (brand_num) REFERENCES used_car.car_brands(brand_num)
ON DELETE CASCADE;

SELECT *
FROM information_schema.key_column_usage
WHERE table_name = 'used_car_table' AND constraint_name = 'fk_car_brand';

SET SQL_SAFE_UPDATES = 0;

SELECT u.id, u.car_brand, c.brand_num
FROM used_car.used_car_table u
JOIN used_car.car_brands c 
  ON TRIM(LOWER(u.car_brand)) = TRIM(LOWER(c.car_brand));

SET SQL_SAFE_UPDATES = 0;  -- 안전한 업데이트 모드 비활성화

UPDATE used_car.used_car_table u
JOIN used_car.car_brands c 
  ON TRIM(LOWER(REPLACE(u.car_brand, ' ', ''))) = TRIM(LOWER(REPLACE(c.car_brand, ' ', '')))
SET u.brand_num = c.brand_num;


SELECT id, car_brand, brand_num
FROM used_car.used_car_table
WHERE brand_num = 8;

UPDATE used_car.car_brands
SET car_brand = 'Mercedes-Benz'
WHERE car_brand = '벤츠';

UPDATE used_car.car_brands
SET car_brand = 'Audi'
WHERE car_brand = 'AUDI';

commit

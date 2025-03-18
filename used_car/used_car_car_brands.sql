-- MySQL dump 10.13  Distrib 8.0.41, for Win64 (x86_64)
--
-- Host: localhost    Database: used_car
-- ------------------------------------------------------
-- Server version	8.0.41

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `car_brands`
--

DROP TABLE IF EXISTS `car_brands`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `car_brands` (
  `brand_num` int NOT NULL AUTO_INCREMENT,
  `car_brand` varchar(50) NOT NULL,
  PRIMARY KEY (`brand_num`)
) ENGINE=InnoDB AUTO_INCREMENT=39 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `car_brands`
--

LOCK TABLES `car_brands` WRITE;
/*!40000 ALTER TABLE `car_brands` DISABLE KEYS */;
INSERT INTO `car_brands` VALUES (1,'현대'),(2,'르노코리아'),(3,'기아'),(4,'쉐보레'),(5,'KGM'),(6,'제네시스'),(7,'기타'),(8,'Mercedes-Benz'),(9,'BMW'),(10,'Audi'),(11,'폭스바겐'),(12,'렉서스'),(13,'볼보'),(14,'미니'),(15,'도요타'),(16,'포드'),(17,'랜드로버'),(18,'포르쉐'),(19,'크라이슬러'),(20,'혼다'),(21,'쉐보레'),(22,'푸조'),(23,'테슬라'),(24,'닛산'),(25,'재규어'),(26,'링컨'),(27,'인피니티'),(28,'캐딜락'),(29,'시트로앵'),(30,'마세라티'),(31,'폴스타'),(32,'벤틀리'),(33,'람보르기니'),(34,'피아트'),(35,'롤스로이스'),(36,'gmc'),(37,'ds'),(38,'페라리');
/*!40000 ALTER TABLE `car_brands` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-03-17 18:38:55

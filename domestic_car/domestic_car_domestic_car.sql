-- MySQL dump 10.13  Distrib 8.0.41, for macos15 (arm64)
--
-- Host: localhost    Database: domestic_car
-- ------------------------------------------------------
-- Server version	9.2.0

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
-- Table structure for table `domestic_car`
--

DROP TABLE IF EXISTS `domestic_car`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `domestic_car` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `Year` int DEFAULT NULL,
  `Month` int DEFAULT NULL,
  `Rank` int DEFAULT NULL,
  `Brand` varchar(100) DEFAULT NULL,
  `Sales` int DEFAULT NULL,
  `Market_Share` float DEFAULT NULL,
  `Brand_index` int DEFAULT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=126 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `domestic_car`
--

LOCK TABLES `domestic_car` WRITE;
/*!40000 ALTER TABLE `domestic_car` DISABLE KEYS */;
INSERT INTO `domestic_car` VALUES (1,2023,1,1,'현대',42420,42.5,1),(2,2023,1,2,'기아',38682,38.8,3),(3,2023,1,3,'제네시스',8355,8.4,6),(4,2023,1,5,'르노코리아',2116,2.1,2),(5,2023,1,6,'쉐보레',1021,1,4),(6,2023,2,1,'현대',54604,43.9,1),(7,2023,2,2,'기아',50009,40.2,3),(8,2023,2,3,'제네시스',9696,7.8,6),(9,2023,2,5,'르노코리아',2218,1.8,2),(10,2023,2,6,'쉐보레',1054,0.8,4),(11,2023,3,1,'현대',60100,43.2,1),(12,2023,3,2,'기아',53032,38.1,3),(13,2023,3,3,'제네시스',12735,9.2,6),(14,2023,3,5,'르노코리아',2636,1.9,2),(15,2023,3,6,'쉐보레',1636,1.2,4),(16,2023,4,1,'현대',53407,41.9,1),(17,2023,4,2,'기아',49200,38.6,3),(18,2023,4,3,'제네시스',12187,9.6,6),(19,2023,4,5,'쉐보레',5180,4.1,4),(20,2023,4,6,'르노코리아',1801,1.4,2),(21,2023,5,1,'현대',54728,42.5,1),(22,2023,5,2,'기아',50254,39,3),(23,2023,5,3,'제네시스',12428,9.7,6),(24,2023,5,5,'쉐보레',4708,3.7,4),(25,2023,5,6,'르노코리아',1778,1.4,2),(26,2023,6,1,'현대',54751,41.4,1),(27,2023,6,2,'기아',51018,38.6,3),(28,2023,6,3,'제네시스',13838,10.5,6),(29,2023,6,5,'쉐보레',5136,3.9,4),(30,2023,6,6,'르노코리아',1721,1.3,2),(31,2023,7,1,'기아',47380,41.8,3),(32,2023,7,2,'현대',45773,40.3,1),(33,2023,7,3,'제네시스',10455,9.2,6),(34,2023,7,4,'쉐보레',4086,3.6,4),(35,2023,7,6,'르노코리아',1705,1.5,2),(36,2023,8,1,'현대',45099,42.9,1),(37,2023,8,2,'기아',42232,40.2,3),(38,2023,8,3,'제네시스',9180,8.7,6),(39,2023,8,5,'쉐보레',3259,3.1,4),(40,2023,8,6,'르노코리아',1502,1.4,2),(41,2023,9,1,'기아',44299,42,3),(42,2023,9,2,'현대',44231,42,1),(43,2023,9,3,'제네시스',8514,8.1,6),(44,2023,9,5,'쉐보레',2602,2.5,4),(45,2023,9,6,'르노코리아',1651,1.6,2),(46,2023,10,1,'현대',55353,47.8,1),(47,2023,10,2,'기아',43163,37.3,3),(48,2023,10,3,'제네시스',7596,6.6,6),(49,2023,10,4,'쉐보레',4437,3.8,4),(50,2023,10,6,'르노코리아',1451,1.3,2),(51,2023,11,1,'현대',59751,45.7,1),(52,2023,11,2,'기아',50193,38.4,3),(53,2023,11,3,'제네시스',10889,8.3,6),(54,2023,11,5,'쉐보레',2993,2.3,4),(55,2023,11,6,'르노코리아',1875,1.4,2),(56,2023,12,1,'현대',50265,44.4,1),(57,2023,12,2,'기아',45061,39.8,3),(58,2023,12,3,'제네시스',10694,9.4,6),(59,2023,12,5,'쉐보레',2194,1.9,4),(60,2023,12,6,'르노코리아',1594,1.4,2),(61,2024,1,1,'기아',44561,43.7,3),(62,2024,1,2,'현대',37696,37,1),(63,2024,1,3,'제네시스',11349,11.1,6),(64,2024,1,5,'쉐보레',2880,2.8,4),(65,2024,1,6,'르노코리아',1645,1.6,2),(66,2024,2,1,'기아',43968,44.8,3),(67,2024,2,2,'현대',36047,36.7,1),(68,2024,2,3,'제네시스',10582,10.8,6),(69,2024,2,5,'쉐보레',1963,2,4),(70,2024,2,6,'르노코리아',1807,1.8,2),(71,2024,3,1,'현대',49383,41.6,1),(72,2024,3,2,'기아',48985,41.2,3),(73,2024,3,3,'제네시스',11674,9.8,6),(74,2024,3,5,'르노코리아',2039,1.7,2),(75,2024,3,6,'쉐보레',2003,1.7,4),(76,2024,4,1,'현대',50535,43,1),(77,2024,4,2,'기아',47509,40.4,3),(78,2024,4,3,'제네시스',11784,10,6),(79,2024,4,5,'쉐보레',2265,1.9,4),(80,2024,4,6,'르노코리아',1780,1.5,2),(81,2024,5,1,'현대',50561,44,1),(82,2024,5,2,'기아',45993,40,3),(83,2024,5,3,'제네시스',10136,8.8,6),(84,2024,5,5,'쉐보레',2317,2,4),(85,2024,5,6,'르노코리아',1901,1.7,2),(86,2024,6,1,'현대',46087,41.8,1),(87,2024,6,2,'기아',44162,40,3),(88,2024,6,3,'제네시스',12104,11,6),(89,2024,6,5,'르노코리아',2041,1.8,2),(90,2024,6,6,'쉐보레',1871,1.7,4),(91,2024,7,1,'기아',46125,42.5,3),(92,2024,7,2,'현대',43931,40.4,1),(93,2024,7,3,'제네시스',10703,9.9,6),(94,2024,7,5,'쉐보레',2164,2,4),(95,2024,7,6,'르노코리아',1469,1.4,2),(96,2024,8,1,'현대',46241,44.5,1),(97,2024,8,2,'기아',40574,39,3),(98,2024,8,3,'제네시스',10323,9.9,6),(99,2024,8,5,'쉐보레',1587,1.5,4),(100,2024,8,6,'르노코리아',1350,1.3,2),(101,2024,9,1,'현대',43809,42.1,1),(102,2024,9,2,'기아',38175,36.7,3),(103,2024,9,3,'제네시스',10638,10.2,6),(104,2024,9,4,'르노코리아',5010,4.8,2),(105,2024,9,6,'쉐보레',1927,1.9,4),(106,2024,10,1,'현대',52631,43,1),(107,2024,10,2,'기아',46286,37.8,3),(108,2024,10,3,'제네시스',10655,8.7,6),(109,2024,10,4,'르노코리아',6395,5.2,2),(110,2024,10,6,'쉐보레',1949,1.6,4),(111,2024,11,1,'현대',50741,41.5,1),(112,2024,11,2,'기아',48069,39.3,3),(113,2024,11,3,'제네시스',10951,9,6),(114,2024,11,4,'르노코리아',7301,6,2),(115,2024,11,6,'쉐보레',1796,1.5,4),(116,2024,12,1,'현대',50522,42.9,1),(117,2024,12,2,'기아',46200,39.2,3),(118,2024,12,3,'제네시스',9610,8.2,6),(119,2024,12,4,'르노코리아',7078,6,2),(120,2024,12,6,'쉐보레',1773,1.5,4),(121,2025,1,1,'기아',38311,42.8,3),(122,2025,1,2,'현대',36276,40.5,1),(123,2025,1,3,'제네시스',8824,9.9,6),(124,2025,1,4,'르노코리아',2601,2.9,2),(125,2025,1,6,'쉐보레',1219,1.4,4);
/*!40000 ALTER TABLE `domestic_car` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-03-18 10:36:18

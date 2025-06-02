-- MySQL dump 10.13  Distrib 8.0.42, for Win64 (x86_64)
--
-- Host: localhost    Database: hospital_system
-- ------------------------------------------------------
-- Server version	8.0.33

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
-- Table structure for table `prescriptiondetail`
--

DROP TABLE IF EXISTS `prescriptiondetail`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `prescriptiondetail` (
  `record_id` varchar(20) NOT NULL,
  `medicine_id` varchar(10) NOT NULL,
  `quantity` int DEFAULT NULL,
  `dosage` varchar(50) DEFAULT NULL,
  `frequency` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`record_id`,`medicine_id`),
  KEY `medicine_id` (`medicine_id`),
  CONSTRAINT `prescriptiondetail_ibfk_1` FOREIGN KEY (`record_id`) REFERENCES `medicalrecord` (`record_id`),
  CONSTRAINT `prescriptiondetail_ibfk_2` FOREIGN KEY (`medicine_id`) REFERENCES `medicine` (`medicine_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `prescriptiondetail`
--

LOCK TABLES `prescriptiondetail` WRITE;
/*!40000 ALTER TABLE `prescriptiondetail` DISABLE KEYS */;
INSERT INTO `prescriptiondetail` VALUES ('MR001','M001',1,'1片','每日3次'),('MR001','M003',2,'1片','每日2次'),('MR002','M005',1,'1粒','每日1次'),('MR003','M002',2,'1粒','每日2次'),('MR003','M003',1,'1片','每日3次'),('MR004','M004',1,'10单位','每日注射'),('MR005','M001',1,'1片','每日3次'),('MR006','M006',1,'1片','每日1次'),('MR007','M008',1,'1袋','每日3次'),('MR008','M004',1,'15单位','每日注射'),('MR009','M009',2,'1片','每日1次'),('MR010','M010',1,'250ml','静脉滴注');
/*!40000 ALTER TABLE `prescriptiondetail` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-06-02 23:26:25

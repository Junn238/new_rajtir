-- MySQL dump 10.13  Distrib 8.0.42, for Win64 (x86_64)
--
--LEER LEER LEER LEER LEER LEER LEER LEER LEER LEER LEER LEER LEER LEER
--Ocupas crear primero la base de datos dentro de MySQL Workbench
--Despues la colocas como la base de datos predeterminada
--Y ejecutas este query dentro de la base de datos

-- Host: localhost    Database: rajtir
-- ------------------------------------------------------
-- Server version	8.0.42

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
-- Table structure for table `cliente`
--

DROP TABLE IF EXISTS `cliente`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cliente` (
  `Id_cli` int NOT NULL AUTO_INCREMENT,
  `Nom_cli` varchar(50) DEFAULT NULL,
  `Tip_cli` varchar(20) NOT NULL,
  PRIMARY KEY (`Id_cli`),
  UNIQUE KEY `Id_cli_UNIQUE` (`Id_cli`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cliente`
--

LOCK TABLES `cliente` WRITE;
/*!40000 ALTER TABLE `cliente` DISABLE KEYS */;
/*!40000 ALTER TABLE `cliente` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `comision`
--

DROP TABLE IF EXISTS `comision`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `comision` (
  `Id_pa` int NOT NULL AUTO_INCREMENT,
  `Id_emp` int NOT NULL,
  `Id_cli` int NOT NULL,
  `Can_pa` decimal(10,2) NOT NULL,
  PRIMARY KEY (`Id_pa`,`Id_emp`,`Id_cli`),
  UNIQUE KEY `Id_pa_UNIQUE` (`Id_pa`),
  KEY `fk_Empleado_has_Cliente_Cliente1_idx` (`Id_cli`),
  KEY `fk_Empleado_has_Cliente_Empleado1_idx` (`Id_emp`),
  CONSTRAINT `fk_Empleado_has_Cliente_Cliente1` FOREIGN KEY (`Id_cli`) REFERENCES `cliente` (`Id_cli`),
  CONSTRAINT `fk_Empleado_has_Cliente_Empleado1` FOREIGN KEY (`Id_emp`) REFERENCES `empleado` (`Id_emp`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `comision`
--

LOCK TABLES `comision` WRITE;
/*!40000 ALTER TABLE `comision` DISABLE KEYS */;
/*!40000 ALTER TABLE `comision` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `empleado`
--

DROP TABLE IF EXISTS `empleado`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `empleado` (
  `Id_emp` int NOT NULL AUTO_INCREMENT,
  `Nom_emp` varchar(50) NOT NULL,
  `Ed_emp` tinyint NOT NULL,
  `Tel_emp` varchar(15) NOT NULL,
  `Em_emp` varchar(50) NOT NULL,
  `Tie_emp` int NOT NULL,
  `Tur_emp` varchar(20) NOT NULL,
  PRIMARY KEY (`Id_emp`),
  UNIQUE KEY `Id_emp_UNIQUE` (`Id_emp`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `empleado`
--

LOCK TABLES `empleado` WRITE;
/*!40000 ALTER TABLE `empleado` DISABLE KEYS */;
/*!40000 ALTER TABLE `empleado` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `movimiento`
--

DROP TABLE IF EXISTS `movimiento`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `movimiento` (
  `Id_mov` int NOT NULL AUTO_INCREMENT,
  `Cliente_Id` int NOT NULL,
  `Id_pr` int NOT NULL,
  `Pag_mov` decimal(10,2) NOT NULL,
  `Cam_mov` decimal(10,2) NOT NULL,
  `Fal_mov` decimal(10,2) NOT NULL,
  `Fec_mov` datetime NOT NULL,
  `Fin_mov` datetime NOT NULL,
  PRIMARY KEY (`Id_mov`,`Cliente_Id`,`Id_pr`),
  UNIQUE KEY `Id_mov_UNIQUE` (`Id_mov`),
  KEY `fk_Cliente_has_Producto_Producto1_idx` (`Id_pr`),
  KEY `fk_Cliente_has_Producto_Cliente_idx` (`Cliente_Id`),
  CONSTRAINT `fk_Cliente_has_Producto_Cliente` FOREIGN KEY (`Cliente_Id`) REFERENCES `cliente` (`Id_cli`),
  CONSTRAINT `fk_Cliente_has_Producto_Producto1` FOREIGN KEY (`Id_pr`) REFERENCES `producto` (`Id_pro`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `movimiento`
--

LOCK TABLES `movimiento` WRITE;
/*!40000 ALTER TABLE `movimiento` DISABLE KEYS */;
/*!40000 ALTER TABLE `movimiento` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `producto`
--

DROP TABLE IF EXISTS `producto`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `producto` (
  `Id_pro` int NOT NULL AUTO_INCREMENT,
  `Nom_pro` varchar(50) NOT NULL,
  `Val_pro` decimal(10,2) NOT NULL,
  `Mar_pro` varchar(30) NOT NULL,
  `Can_pro` int NOT NULL,
  `Des_pro` varchar(255) NOT NULL,
  `Id_prov` int NOT NULL,
  PRIMARY KEY (`Id_pro`),
  UNIQUE KEY `Id_pro_UNIQUE` (`Id_pro`),
  KEY `fk_proveedor` (`Id_prov`),
  CONSTRAINT `fk_proveedor` FOREIGN KEY (`Id_prov`) REFERENCES `proveedor` (`Id_prov`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `producto`
--

LOCK TABLES `producto` WRITE;
/*!40000 ALTER TABLE `producto` DISABLE KEYS */;
-- INSERT INTO `producto` VALUES (5,'takis juego',100.23,'takis',200,'takis asi bien pikosos asi bien fleiminjot',1);
/*!40000 ALTER TABLE `producto` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `proveedor`
--

DROP TABLE IF EXISTS `proveedor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `proveedor` (
  `Id_prov` int NOT NULL AUTO_INCREMENT,
  `Ho_prov` varchar(20) NOT NULL,
  `Nom_prov` varchar(50) NOT NULL,
  `Ubi_pro` varchar(100) NOT NULL,
  `Mar_prov` varchar(50) NOT NULL,
  PRIMARY KEY (`Id_prov`),
  UNIQUE KEY `Id_pro_UNIQUE` (`Id_prov`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `proveedor`
--

LOCK TABLES `proveedor` WRITE;
/*!40000 ALTER TABLE `proveedor` DISABLE KEYS */;
INSERT INTO `proveedor` VALUES (1,'12 a 16','Barcel','juarez','takis');
/*!40000 ALTER TABLE `proveedor` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ticket`
--

DROP TABLE IF EXISTS `ticket`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ticket` (
  `Id_tic` int NOT NULL AUTO_INCREMENT,
  `Id_cli` int NOT NULL,
  `Id_pro` int NOT NULL,
  `Pag_tic` decimal(10,2) NOT NULL,
  `Cam_tic` decimal(10,2) NOT NULL,
  `Fal_tic` decimal(10,2) NOT NULL,
  `Fec_tic` datetime NOT NULL,
  `Fin_tic` datetime NOT NULL,
  `NomSuc_tic` varchar(50) NOT NULL,
  `Hor_tic` time NOT NULL,
  PRIMARY KEY (`Id_tic`,`Id_cli`,`Id_pro`),
  UNIQUE KEY `Id_tic_UNIQUE` (`Id_tic`),
  KEY `fk_Cliente_has_Producto_Producto2_idx` (`Id_pro`),
  KEY `fk_Cliente_has_Producto_Cliente1_idx` (`Id_cli`),
  CONSTRAINT `fk_Cliente_has_Producto_Cliente1` FOREIGN KEY (`Id_cli`) REFERENCES `cliente` (`Id_cli`),
  CONSTRAINT `fk_Cliente_has_Producto_Producto2` FOREIGN KEY (`Id_pro`) REFERENCES `producto` (`Id_pro`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ticket`
--

LOCK TABLES `ticket` WRITE;
/*!40000 ALTER TABLE `ticket` DISABLE KEYS */;
/*!40000 ALTER TABLE `ticket` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-05-07  0:39:03

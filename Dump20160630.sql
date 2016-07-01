-- MySQL dump 10.13  Distrib 5.7.9, for osx10.9 (x86_64)
--
-- Host: localhost    Database: schedules
-- ------------------------------------------------------
-- Server version	5.5.42

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `locations`
--

DROP TABLE IF EXISTS `locations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `locations` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `location_name` varchar(105) DEFAULT NULL,
  `street_name` varchar(155) NOT NULL,
  `city` varchar(45) DEFAULT NULL,
  `state` varchar(2) DEFAULT NULL,
  `zip_code` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_location_users1_idx` (`user_id`),
  CONSTRAINT `fk_location_users1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `locations`
--

LOCK TABLES `locations` WRITE;
/*!40000 ALTER TABLE `locations` DISABLE KEYS */;
INSERT INTO `locations` VALUES (1,'Coding Dojo','1980 Zanker Rd','San Jose','CA',95112,1),(3,'Walgreens','780 E Santa Clara St','San Jose','CA',95112,1),(4,'Starbucks','2579 North First Street','San Jose','CA',95131,1),(5,'Gym','610 Newhall Dr','San Jose','CA',95110,1),(6,'Safeway','2605 The Alameda','Santa Clara','CA',95050,1),(7,'Academy of Science','55 Music Concourse Dr','San Francisco','CA',94118,1),(8,'Ex-Home','320 5th St','New York','NY',11215,1),(11,'Petco','160 E El Camino Real','Sunnyvale','CA',94087,1),(12,'PetSmart','770 E El Camino Real','Sunnyvale','CA',94087,1),(13,'Coding Dojo','1980 Zanker Rd','San Jose','CA',95112,2),(14,'Flickinger Park','Flickinger Ave','San Jose','CA',95131,2),(15,'Koja','1085 E Brokaw Rd','San Jose','CA',95131,2),(16,'Starbucks','1751 N First St','San Jose','CA',95113,2);
/*!40000 ALTER TABLE `locations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tasks`
--

DROP TABLE IF EXISTS `tasks`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tasks` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `task_name` varchar(45) DEFAULT NULL,
  `description` varchar(1000) DEFAULT NULL,
  `priority` varchar(40) DEFAULT NULL,
  `status` varchar(45) DEFAULT NULL,
  `date` date DEFAULT NULL,
  `time` time DEFAULT NULL,
  `notification` varchar(45) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  `location_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_tasks_users_idx` (`user_id`),
  KEY `fk_tasks_location1_idx` (`location_id`),
  CONSTRAINT `fk_tasks_location1` FOREIGN KEY (`location_id`) REFERENCES `locations` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_tasks_users` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tasks`
--

LOCK TABLES `tasks` WRITE;
/*!40000 ALTER TABLE `tasks` DISABLE KEYS */;
INSERT INTO `tasks` VALUES (1,'Project presentation','Present Task Slaughter','Important','Pending','2016-07-01','11:00:00','off',1,1),(2,'Groceries','Buy milk, eggs and bread','Urgent','Cancelled','2016-06-29','09:00:00','off',1,6),(3,'Get meds','','Medium','Pending','2016-06-30','14:00:00','off',1,3),(4,'Workout',NULL,'Medium','Cancelled','2016-06-28','19:00:00','off',1,5),(5,'Lunch',NULL,'Medium','Done','2016-06-28','12:30:00','off',1,4),(6,'Lunch','','Medium','Done','2016-06-29','12:30:00','off',1,4),(7,'Diner','','Low','Done','2016-06-29','19:00:00','off',1,4),(8,'Work Out',NULL,'Important','Pending','2016-06-29','20:30:00','off',1,5),(10,'See the stars','','Important','Pending','2016-06-28','22:00:00','off',1,8),(11,'Work Out',NULL,'Important','Done','2016-06-30','20:30:00','off',1,5),(12,'Work Out',NULL,'Important','Cancelled','2016-06-30','20:30:00','off',1,5),(14,'Dog food','','Urgent','Pending','2016-06-30','16:00:00','off',1,12),(15,'Dog food','','','Pending','2016-06-30','16:30:00','off',1,12),(16,'Deployment','Deploy for tomorrow\'s presentation','Urgent','Done','2016-06-30','18:00:00','off',2,13),(17,'Deployment','updated','Urgent','Cancelled','2016-06-30','21:00:00','off',2,13),(18,'Dinner','Have dinner with my friends','Important','Pending','2016-06-30','21:00:00','off',2,15),(19,'Breakfast','','Low','Cancelled','2016-06-30','09:00:00','off',2,13),(20,'Task 1','','Urgent','Pending','2016-06-30','10:00:00','off',2,13),(21,'Task 2','','Urgent','Pending','2016-06-30','12:00:00','off',2,14),(22,'Task 3','','Important','Pending','2016-06-30','22:00:00','off',2,15);
/*!40000 ALTER TABLE `tasks` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `first_name` varchar(105) NOT NULL,
  `last_name` varchar(155) NOT NULL,
  `email` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `phone` varchar(15) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'Luke','Skywalker','email1@gmail.com','$2b$12$ZBam7DHarPEOw6xu9pi8Cu80YTADKAOymmL0j7uSxJ0XC6D/blRxm','9292475506'),(2,'Edlene','Miguel','edlene@email.com','$2b$12$MwDvAv7rblJK8wq5b/mu/uhwmWe3FpPv5Xm3C8DTRAO9Fq6cVReO2','5105169639');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2016-06-30 18:46:51

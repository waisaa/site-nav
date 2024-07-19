-- MySQL dump 10.13  Distrib 5.5.62, for Win64 (AMD64)
-- --------------------------------------------------
-- Database: db_site_navigation
-- --------------------------------------------------
-- Server version	5.7.25-log

-- 设置字符集为 utf8mb4
SET NAMES utf8mb4;
SET character_set_client = utf8mb4;
SET character_set_connection = utf8mb4;
SET character_set_results = utf8mb4;

DROP DATABASE IF EXISTS db_site_navigation;
CREATE DATABASE db_site_navigation CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE `db_site_navigation`;

--
-- Table structure for table `site_type`
--

DROP TABLE IF EXISTS `site_type`;
CREATE TABLE `site_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '类型id',
  `name` varchar(100) DEFAULT NULL COMMENT '类型名称',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='网站类型表';

--
-- Dumping data for table `site_type`
--

LOCK TABLES `site_type` WRITE;
INSERT INTO `site_type` VALUES 
(1,'Web'),
(11,'原型'),
(22,'后台'),
(33,'监控'),
(44,'中间件'),
(55,'其他');
UNLOCK TABLES;

--
-- Table structure for table `sites`
--

DROP TABLE IF EXISTS `sites`;
CREATE TABLE `sites` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键id',
  `type_id` int(11) NOT NULL COMMENT '类型id',
  `name` varchar(100) DEFAULT NULL COMMENT '名字',
  `link` varchar(255) DEFAULT NULL COMMENT '地址',
  `remarks` varchar(255) DEFAULT NULL COMMENT '备注',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='网站信息表';

--
-- Dumping data for table `sites`
--

LOCK TABLES `sites` WRITE;
INSERT INTO `sites` VALUES 
(1,1,'百度','http://www.baidu.com',''),
(2,11,'百度','http://www.baidu.com',''),
(3,22,'百度','http://www.baidu.com',''),
(4,33,'百度','http://www.baidu.com',''),
(5,44,'百度','http://www.baidu.com',''),
(6,55,'百度','http://www.baidu.com','');
UNLOCK TABLES;

--
-- Dumping routines for database 'db_site_navigation'
--

-- Dump completed on 2024-07-16 15:16:53

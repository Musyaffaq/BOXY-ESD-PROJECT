-- phpMyAdmin SQL Dump
-- version 4.7.4
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3306
-- Generation Time: Jun 12, 2020 at 02:17 AM
-- Server version: 5.7.19
-- PHP Version: 7.1.9

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `inventory`
--
CREATE DATABASE IF NOT EXISTS `inventory` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `inventory`;

-- --------------------------------------------------------

--
-- Table structure for table `inventory`
--

DROP TABLE IF EXISTS `inventory`;
CREATE TABLE IF NOT EXISTS `inventory` (
    `type` varchar(15) NOT NULL,
    `stripe_id` varchar(30) NOT NULL,
    `available` int NOT NULL,
    `loaned` int NOT NULL,
  PRIMARY KEY (`type`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

--
-- Dumping data for table `inventory`
--

INSERT INTO `inventory` (`type`,`stripe_id`,`available`,`loaned`) VALUES
('small-bento', 'price_1MsTvOHfoHRbQNfbvfkCAvdQ', 1000, 500),
('medium-bento', 'price_1MsTwOHfoHRbQNfbErNoHAjo', 1000, 500),
('large-bento', 'price_1MsTwuHfoHRbQNfbrH3UAdrJ', 1000, 500),
('small-bowl', 'price_1MsTxSHfoHRbQNfbBUxCjsNP', 1000, 500),
('medium-bowl', 'price_1MsTxtHfoHRbQNfb1N7DpzRl', 1000, 500),
('large-bowl', 'price_1MsTyHHfoHRbQNfbzF38Qucq', 1000, 500);
COMMIT;
-- --------------------------------------------------------

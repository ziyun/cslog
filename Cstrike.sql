-- phpMyAdmin SQL Dump
-- version 4.0.3
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Dec 24, 2013 at 05:17 PM
-- Server version: 5.5.25
-- PHP Version: 5.4.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `Cstrike`
--
CREATE DATABASE IF NOT EXISTS `Cstrike` DEFAULT CHARACTER SET utf8 COLLATE utf8_unicode_ci;
USE `Cstrike`;

-- --------------------------------------------------------

--
-- Table structure for table `Alias`
--

CREATE TABLE IF NOT EXISTS `Alias` (
  `row_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `profile_id` int(10) unsigned NOT NULL,
  `alias` varchar(64) COLLATE utf8_unicode_ci NOT NULL,
  PRIMARY KEY (`row_id`),
  KEY `profile_id` (`profile_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `Attack`
--

CREATE TABLE IF NOT EXISTS `Attack` (
  `row_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `match_id` int(10) unsigned NOT NULL,
  `player_a` int(10) unsigned NOT NULL,
  `player_b` int(10) unsigned NOT NULL,
  `team` tinyint(1) NOT NULL,
  `weapon` int(4) unsigned NOT NULL,
  `hitgroup` enum('head','chest','stomach','left arm','left leg','right arm','right leg','generic') COLLATE utf8_unicode_ci NOT NULL,
  `damage` int(4) unsigned NOT NULL,
  `damage_armor` int(4) unsigned NOT NULL,
  PRIMARY KEY (`row_id`),
  KEY `player_a` (`player_a`),
  KEY `player_b` (`player_b`),
  KEY `match_id` (`match_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `Kill`
--

CREATE TABLE IF NOT EXISTS `Kill` (
  `row_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `match_id` int(10) unsigned NOT NULL,
  `player_a` int(10) unsigned NOT NULL,
  `player_b` int(10) unsigned NOT NULL,
  `team` tinyint(1) NOT NULL,
  `weapon` int(4) unsigned NOT NULL,
  `headshot` tinyint(1) NOT NULL,
  PRIMARY KEY (`row_id`),
  KEY `player_a` (`player_a`),
  KEY `player_b` (`player_b`),
  KEY `match_id` (`match_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `Match`
--

CREATE TABLE IF NOT EXISTS `Match` (
  `match_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `map` varchar(32) COLLATE utf8_unicode_ci NOT NULL,
  `created_on` datetime NOT NULL,
  `terrorist` int(11) NOT NULL,
  `counter_terrorist` int(11) NOT NULL,
  PRIMARY KEY (`match_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `Profile`
--

CREATE TABLE IF NOT EXISTS `Profile` (
  `profile_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `steam_id` varchar(64) COLLATE utf8_unicode_ci NOT NULL,
  `fname` varchar(32) COLLATE utf8_unicode_ci DEFAULT NULL,
  `lname` varchar(32) COLLATE utf8_unicode_ci DEFAULT NULL,
  `email` varchar(32) COLLATE utf8_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`profile_id`),
  UNIQUE KEY `steam_id` (`steam_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `Weapon`
--

CREATE TABLE IF NOT EXISTS `Weapon` (
  `weapon_id` int(4) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(24) COLLATE utf8_unicode_ci NOT NULL,
  PRIMARY KEY (`weapon_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci AUTO_INCREMENT=28 ;

--
-- Dumping data for table `Weapon`
--

INSERT INTO `Weapon` (`weapon_id`, `name`) VALUES
(1, 'galil'),
(2, 'ak47'),
(3, 'scout'),
(4, 'sg552'),
(5, 'awp'),
(6, 'g3sg1'),
(7, 'famas'),
(8, 'm4a1'),
(9, 'aug'),
(10, 'sg550'),
(11, 'glock'),
(12, 'usp'),
(13, 'p228'),
(14, 'deagle'),
(15, 'elite'),
(16, 'fiveseven'),
(17, 'm3'),
(18, 'xm1014'),
(19, 'mac10'),
(20, 'tmp'),
(21, 'mp5navy'),
(22, 'ump45'),
(23, 'p90'),
(24, 'm249'),
(25, 'knife'),
(26, 'hegrenade'),
(27, 'prop_physics');

--
-- Constraints for dumped tables
--

--
-- Constraints for table `Alias`
--
ALTER TABLE `Alias`
  ADD CONSTRAINT `Alias_ibfk_1` FOREIGN KEY (`profile_id`) REFERENCES `Profile` (`profile_id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `Attack`
--
ALTER TABLE `Attack`
  ADD CONSTRAINT `Attack_ibfk_1` FOREIGN KEY (`player_a`) REFERENCES `Profile` (`profile_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `Attack_ibfk_2` FOREIGN KEY (`player_b`) REFERENCES `Profile` (`profile_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `Attack_ibfk_3` FOREIGN KEY (`match_id`) REFERENCES `Match` (`match_id`) ON DELETE NO ACTION ON UPDATE NO ACTION;

--
-- Constraints for table `Kill`
--
ALTER TABLE `Kill`
  ADD CONSTRAINT `Kill_ibfk_1` FOREIGN KEY (`player_a`) REFERENCES `Profile` (`profile_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `Kill_ibfk_2` FOREIGN KEY (`player_b`) REFERENCES `Profile` (`profile_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `Kill_ibfk_3` FOREIGN KEY (`match_id`) REFERENCES `Match` (`match_id`) ON DELETE NO ACTION ON UPDATE NO ACTION;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

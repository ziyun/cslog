-- phpMyAdmin SQL Dump
-- version 3.4.10.1deb1
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Dec 24, 2013 at 01:39 PM
-- Server version: 5.5.31
-- PHP Version: 5.3.10-1ubuntu3.9

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `Cstrike`
--

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
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci AUTO_INCREMENT=8 ;

-- --------------------------------------------------------

--
-- Table structure for table `Attack`
--

CREATE TABLE IF NOT EXISTS `Attack` (
  `row_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `match_id` int(10) unsigned NOT NULL,
  `player_a` int(10) unsigned NOT NULL,
  `player_b` int(10) unsigned NOT NULL,
  `team` tinyint(4) NOT NULL,
  `weapon` enum('galil','ak47','scout','sg552','awp','g3sg1','famas','m4a1','aug','sg550','glock','usp','p228','deagle','elite','fiveseven','m3','xm1014','mac10','tmp','mp5navy','ump45','p90','m249','knife','hegrenade') COLLATE utf8_unicode_ci NOT NULL,
  `hitgroup` enum('head','chest','stomach','left arm','left leg','right arm','right leg','generic') COLLATE utf8_unicode_ci NOT NULL,
  `damage` int(4) unsigned NOT NULL,
  `damage_armor` int(4) unsigned NOT NULL,
  PRIMARY KEY (`row_id`),
  KEY `player_a` (`player_a`),
  KEY `player_b` (`player_b`),
  KEY `match_id` (`match_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci AUTO_INCREMENT=4990 ;

-- --------------------------------------------------------

--
-- Table structure for table `Kill`
--

CREATE TABLE IF NOT EXISTS `Kill` (
  `row_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `match_id` int(10) unsigned NOT NULL,
  `player_a` int(10) unsigned NOT NULL,
  `player_b` int(10) unsigned NOT NULL,
  `team` tinyint(4) NOT NULL,
  `weapon` enum('galil','ak47','scout','sg552','awp','g3sg1','famas','m4a1','aug','sg550','glock','usp','p228','deagle','elite','fiveseven','m3','xm1014','mac10','tmp','mp5navy','ump45','p90','m249','knife','hegrenade') COLLATE utf8_unicode_ci NOT NULL,
  `headshot` tinyint(1) NOT NULL,
  PRIMARY KEY (`row_id`),
  KEY `player_a` (`player_a`),
  KEY `player_b` (`player_b`),
  KEY `match_id` (`match_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci AUTO_INCREMENT=1146 ;

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
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci AUTO_INCREMENT=47 ;

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
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci AUTO_INCREMENT=8 ;

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

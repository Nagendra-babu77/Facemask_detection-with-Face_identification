-- phpMyAdmin SQL Dump
-- version 2.11.6
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Apr 17, 2021 at 05:33 AM
-- Server version: 5.0.51
-- PHP Version: 5.2.6

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `face_mask`
--

-- --------------------------------------------------------

--
-- Table structure for table `admin`
--

CREATE TABLE `admin` (
  `username` varchar(20) NOT NULL,
  `password` varchar(20) NOT NULL,
  `period` int(11) NOT NULL,
  `mobile` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `admin`
--

INSERT INTO `admin` (`username`, `password`, `period`, `mobile`) VALUES
('admin', 'admin', 0, 9976570006);

-- --------------------------------------------------------

--
-- Table structure for table `details`
--

CREATE TABLE `details` (
  `id` int(11) NOT NULL,
  `regno` varchar(20) NOT NULL,
  `face_st` int(11) NOT NULL,
  `fine_amt` int(11) NOT NULL,
  `dtime` timestamp NOT NULL default CURRENT_TIMESTAMP on update CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `details`
--

INSERT INTO `details` (`id`, `regno`, `face_st`, `fine_amt`, `dtime`) VALUES
(1, '101', 2, 200, '2021-04-17 11:01:43'),
(2, '101', 2, 200, '2021-04-17 11:01:53'),
(3, '101', 1, 0, '2021-04-17 11:02:04');

-- --------------------------------------------------------

--
-- Table structure for table `register`
--

CREATE TABLE `register` (
  `regno` varchar(20) NOT NULL,
  `name` varchar(20) NOT NULL,
  `mobile` bigint(20) NOT NULL,
  `email` varchar(40) NOT NULL,
  `address` varchar(50) NOT NULL,
  `fimg` varchar(30) NOT NULL,
  UNIQUE KEY `regno` (`regno`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `register`
--

INSERT INTO `register` (`regno`, `name`, `mobile`, `email`, `address`, `fimg`) VALUES
('101', 'Raj', 9360967387, 'raj@gmail.com', '33,ss road', '101_2.jpg');

-- --------------------------------------------------------

--
-- Table structure for table `st_face`
--

CREATE TABLE `st_face` (
  `id` int(11) NOT NULL,
  `regno` varchar(20) NOT NULL,
  `vface` varchar(30) NOT NULL,
  `mask_st` varchar(5) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `st_face`
--

INSERT INTO `st_face` (`id`, `regno`, `vface`, `mask_st`) VALUES
(1, '101', '101_1.jpg', '2'),
(2, '101', '101_2.jpg', '1');

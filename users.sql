-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Oct 22, 2025 at 04:28 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.1.25

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `portal_magang`
--

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `nama` varchar(100) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `password` varchar(255) DEFAULT NULL,
  `role` enum('user','admin') DEFAULT 'user',
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `nama`, `email`, `password`, `role`, `created_at`) VALUES
(1, 'aaaa', 'aaaa@gmail', 'aaaa', 'user', '2025-09-23 01:44:39'),
(4, 'aaaa', 'aaa@gmail', 'aaa', 'user', '2025-09-23 03:14:24'),
(5, 'abc', 'abc@gmail.com', 'abc', 'user', '2025-09-23 04:18:06'),
(6, 'zzz', 'zzz@gmail.com', 'zzz', 'user', '2025-09-29 01:50:14'),
(7, 'Admin Portal', 'admin@gmail.com', 'admin123', 'admin', '2025-09-29 02:00:49'),
(8, 'zaq', 'zaq@gmail.com', 'zaq', 'user', '2025-09-29 03:05:14'),
(9, 'virly1', 'virly1@gmail.com', 'virly1', 'user', '2025-10-02 01:08:37'),
(10, 'aulia', 'aulia@gmail.com', 'aulia1', 'user', '2025-10-12 16:13:38'),
(11, 'alma', 'alma@gmail.com', 'alma', 'user', '2025-10-15 04:08:11'),
(12, 'dini', 'dini@gmail.com', 'dini1', 'user', '2025-10-15 04:30:28'),
(13, 'budi', 'budi@gmail.com', 'budi', 'user', '2025-10-19 17:45:12');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

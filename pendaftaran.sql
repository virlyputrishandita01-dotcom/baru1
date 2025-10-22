-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Oct 22, 2025 at 04:23 AM
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
-- Table structure for table `pendaftaran`
--

CREATE TABLE `pendaftaran` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `nama` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `no_telp` varchar(20) DEFAULT NULL,
  `tgl_mulai` date NOT NULL,
  `tgl_selesai` date DEFAULT NULL,
  `universitas` varchar(150) DEFAULT NULL,
  `surat_izin` varchar(255) DEFAULT NULL,
  `proposal` varchar(255) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `status` varchar(50) NOT NULL DEFAULT 'diproses',
  `surat_balasan` varchar(255) DEFAULT NULL,
  `alasan_penolakan` text DEFAULT NULL,
  `jenis_pendaftar` enum('mahasiswa','siswa') DEFAULT 'mahasiswa',
  `sekolah` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `pendaftaran`
--

INSERT INTO `pendaftaran` (`id`, `user_id`, `nama`, `email`, `no_telp`, `tgl_mulai`, `tgl_selesai`, `universitas`, `surat_izin`, `proposal`, `created_at`, `status`, `surat_balasan`, `alasan_penolakan`, `jenis_pendaftar`, `sekolah`) VALUES
(3, 8, 'zaq', 'zaq@gmail.com', '123', '2025-11-11', '2025-12-12', 'universitas negeri surabaya', 'Jurusan_Kuliah_Tujuan.pdf', 'ppt_day_4.pdf', '2025-09-29 03:18:29', 'sedang didisposisi', NULL, NULL, 'mahasiswa', NULL),
(4, 9, 'virly putri', 'virly1@gmail.com', '111', '2001-01-01', '2001-02-01', 'universitas indonesia', 'ppt_day_4.pdf', 'ppt_day_4.pdf', '2025-10-02 01:13:42', 'diterima', 'Mini_Project_Virly_Putri_Shandita_TI_E.pdf', NULL, 'mahasiswa', NULL),
(7, 11, 'alma', 'alma@gmail.com', '088888', '2000-01-01', '2000-02-01', 'universitas negeri surabaya', 'Mini_Project_Virly_Putri_Shandita_TI_E_1.pdf', 'Mini_Project_Virly_Putri_Shandita_TI_E_1.pdf', '2025-10-15 04:26:10', 'sedang didisposisi', 'logbook_magang.pdf', NULL, 'mahasiswa', NULL),
(8, 12, 'dini', 'dini@gmail.com', '08888', '2025-11-20', '2025-12-20', 'universitas negeri surabaya', 'Mini_Project_Virly_Putri_Shandita_TI_E_1.pdf', 'Mini_Project_Virly_Putri_Shandita_TI_E_1.pdf', '2025-10-15 04:31:30', 'diterima', 'logbook_magang.pdf', NULL, 'mahasiswa', NULL),
(9, 13, 'budi', 'budi@gmail.com', '01111111111', '2222-02-22', '2222-03-22', NULL, 'Jurusan_Kuliah_Tujuan.pdf', 'Jurusan_Kuliah_Tujuan.pdf', '2025-10-19 18:30:55', 'diproses', NULL, NULL, 'mahasiswa', NULL),
(10, 13, 'budi', 'budi@gmail.com', '01111111111', '2222-02-22', '2222-03-22', NULL, 'Jurusan_Kuliah_Tujuan.pdf', 'Jurusan_Kuliah_Tujuan.pdf', '2025-10-19 18:52:17', 'diproses', NULL, NULL, 'mahasiswa', NULL),
(11, 13, 'budi', 'budi@gmail.com', '01111111111', '2222-02-22', '2222-03-22', NULL, 'Jurusan_Kuliah_Tujuan.pdf', 'Jurusan_Kuliah_Tujuan.pdf', '2025-10-19 19:35:43', 'diproses', NULL, NULL, NULL, NULL);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `pendaftaran`
--
ALTER TABLE `pendaftaran`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `pendaftaran`
--
ALTER TABLE `pendaftaran`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

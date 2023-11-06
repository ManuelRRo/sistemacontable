-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: mysql
-- Generation Time: Nov 06, 2023 at 01:11 AM
-- Server version: 8.2.0
-- PHP Version: 8.2.8

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `dbanfav`
--
-- --------------------------------------------------------

--
-- Table structure for table `contabilidad_catalogo`
--

CREATE TABLE `contabilidad_catalogo` (
  `id` bigint NOT NULL,
  `nombre_catalogo` varchar(255) NOT NULL,
  `archivo` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `contabilidad_catalogo`
--

INSERT INTO `contabilidad_catalogo` (`id`, `nombre_catalogo`, `archivo`) VALUES
(1, 'catalogo', 'archivos_excel/4cuentas-av.xlsx'),
(2, 'catalogo', 'archivos_excel/4cuentas_av.xlsx');

-- --------------------------------------------------------

--
-- Table structure for table `contabilidad_empresa`
--

CREATE TABLE `contabilidad_empresa` (
  `id` bigint NOT NULL,
  `nombre_empresa` varchar(255) NOT NULL,
  `catalogo_empresa_id` bigint NOT NULL,
  `propietario_id` bigint NOT NULL,
  `sector` varchar(5) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `contabilidad_empresa`
--

INSERT INTO `contabilidad_empresa` (`id`, `nombre_empresa`, `catalogo_empresa_id`, `propietario_id`, `sector`) VALUES
(1, 'Ferrominera', 1, 1, 'MNR'),
(2, 'Importaciones NFA', 2, 2, 'MNR');

-- --------------------------------------------------------
-- Table structure for table `contabilidad_propietario`
--

CREATE TABLE `contabilidad_propietario` (
  `id` bigint NOT NULL,
  `empresactiva` tinyint(1) NOT NULL,
  `user_id` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `contabilidad_propietario`
--

INSERT INTO `contabilidad_propietario` (`id`, `empresactiva`, `user_id`) VALUES
(1, 1, 1),
(2, 1, 2);

-- --------------------------------------------------------
--
-- Table structure for table `contabilidad_cuenta`
--

CREATE TABLE `contabilidad_cuenta` (
  `id` bigint NOT NULL,
  `codigo` varchar(255) NOT NULL,
  `nombre` varchar(255) NOT NULL,
  `categoria` varchar(5) NOT NULL,
  `subcategoria` varchar(5) NOT NULL,
  `catalogo_id` bigint NOT NULL,
  `cuenta_ratio` varchar(6) NOT NULL,
  `cuenta_av` varchar(6) NOT NULL,
  `categoria_av` varchar(5) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `contabilidad_cuenta`
--

INSERT INTO `contabilidad_cuenta` (`id`, `codigo`, `nombre`, `categoria`, `subcategoria`, `catalogo_id`, `cuenta_ratio`, `cuenta_av`, `categoria_av`) VALUES
(1, 'ac', 'Activo Corriente', '', 'NNG', 1, 'NNG', 'NNG', 'ASV'),
(2, '112', 'Efectivo', 'ASV', 'NNG', 1, 'NNG', 'NNG', 'ASV'),
(3, '113', 'Cuentas por cobrar', 'ASV', 'NNG', 1, 'NNG', 'NNG', 'ASV'),
(4, '114', 'Inventario', 'ASV', 'NNG', 1, 'NNG', 'NNG', 'ASV'),
(5, '115', 'Materia prima', 'ASV', 'NNG', 1, 'NNG', 'NNG', 'ASV'),
(6, '116', 'Productos en proceso', 'ASV', 'NNG', 1, 'NNG', 'NNG', 'ASV'),
(7, '117', 'Producto terminado', 'ASV', 'NNG', 1, 'NNG', 'NNG', 'ASV'),
(8, '118', 'Otros circulantes', 'ASV', 'NNG', 1, 'NNG', 'NNG', 'ASV'),
(9, '119', 'Activo No Corriente', 'ASV', 'NNG', 1, 'NNG', 'NNG', 'ASV'),
(10, '120', 'Terrenos, mejoras y arrendamientos', 'ASV', 'NNG', 1, 'NNG', 'NNG', 'ASV'),
(11, '121', 'Edificios', 'ASV', 'NNG', 1, 'NNG', 'NNG', 'ASV'),
(12, '122', 'Maquinaria y equipo', 'ASV', 'NNG', 1, 'NNG', 'NNG', 'ASV'),
(13, '123', 'Cosntrucciones en proceso', 'ASV', 'NNG', 1, 'NNG', 'NNG', 'ASV'),
(14, '124', 'Depreciacion y amortozacion', 'ASV', 'NNG', 1, 'NNG', 'NNG', 'ASV'),
(15, '125', 'Activo intangible', 'ASV', 'NNG', 1, 'NNG', 'NNG', 'ASV'),
(16, '126', 'otros activos', 'ASV', 'NNG', 1, 'NNG', 'NNG', 'ASV'),
(17, '127', 'Total Activos', 'ASV', 'NNG', 1, 'NNG', 'TTACT', 'ASV'),
(18, '210', 'Pasivo Corriente', 'PSV', 'NNG', 1, 'NNG', 'NNG', 'PSV'),
(19, '211', 'Cuentas por pagar', 'PSV', 'NNG', 1, 'NNG', 'NNG', 'PSV'),
(20, '212', 'Documentos por pagar', 'PSV', 'NNG', 1, 'NNG', 'NNG', 'PSV'),
(21, '213', 'Impuestos por pagar', 'PSV', 'NNG', 1, 'NNG', 'NNG', 'PSV'),
(22, '214', 'Pasivo No Corriente', 'PSV', 'NNG', 1, 'NNG', 'NNG', 'PSV'),
(23, '215', 'Porcion circulante del pasivo a largo plazo', 'PSV', 'NNG', 1, 'NNG', 'NNG', 'PSV'),
(24, '216', 'Pasivo a largo plazo', 'PSV', 'NNG', 1, 'NNG', 'NNG', 'PSV'),
(25, '217', 'Impuestos y otros creditos diferidos', 'PSV', 'NNG', 1, 'NNG', 'NNG', 'PSV'),
(26, '218', 'Intenres minotarios en otras subsidiarios', 'PSV', 'NNG', 1, 'NNG', 'NNG', 'PSV'),
(27, '219', 'Total Pasivos', 'PSV', 'NNG', 1, 'NNG', 'TTPSV', 'PSV'),
(28, '311', 'Acciones preferentes', 'PTR', 'NNG', 1, 'NNG', 'NNG', 'PTR'),
(29, '312', 'Acciones comunes', 'PTR', 'NNG', 1, 'NNG', 'NNG', 'PTR'),
(30, '314', 'Superavit de capital', 'PTR', 'NNG', 1, 'NNG', 'NNG', 'PTR'),
(31, '315', 'Utilidades retenidas', 'PTR', 'NNG', 1, 'NNG', 'NNG', 'PTR'),
(32, '316', 'Menos acciones tesoreria al costo', 'PTR', 'NNG', 1, 'NNG', 'NNG', 'PTR'),
(33, '317', 'Total Capital', 'PTR', 'NNG', 1, 'NNG', 'TTCPT', 'PTR'),
(34, '5101', 'Ingresos por Ventas', 'CRA', 'INOP', 1, 'NNG', 'NNG', 'ESR'),
(35, '4101', 'Costos de Venta', 'CRD', 'CTS', 1, 'NNG', 'NNG', 'ESR'),
(36, 'ub', 'Utilidad Bruta', 'ESR', 'NNG', 1, 'NNG', 'NNG', 'ESR'),
(37, '4201', 'Gastos de Ventas', 'CRD', 'GTOP', 1, 'NNG', 'NNG', 'ESR'),
(38, '4202', 'Gastos de Administración', 'CRD', 'GTOP', 1, 'NNG', 'NNG', 'ESR'),
(39, '4204', 'Gastos Financieros', 'CRD', 'GTOP', 1, 'NNG', 'NNG', 'ESR'),
(40, 'uo', 'Utilidad de Operación', 'ESR', 'NNG', 1, 'NNG', 'NNG', 'ESR'),
(41, '5102', 'Productos Financieros', 'CRA', 'INOP', 1, 'NNG', 'NNG', 'ESR'),
(42, 'ua', 'Utilidad antes de IsR', 'ESR', 'NNG', 1, 'NNG', 'NNG', 'ESR'),
(43, '4203', 'Impuesto sobre la Renta', 'CRD', 'GTOP', 1, 'NNG', 'NNG', 'ESR'),
(44, 'un', 'Utilidad Neta', 'ESR', 'NNG', 1, 'NNG', 'VNTST', 'ESR'),
(45, '111', 'Activo Corriente', 'ASV', 'NNG', 2, 'ACTC', 'NNG', 'ASV'),
(46, '112', 'Efectivo', 'ASV', 'NNG', 2, 'EFCT', 'NNG', 'ASV'),
(47, '113', 'Cuentas por cobrar', 'ASV', 'NNG', 2, 'INVT', 'NNG', 'ASV'),
(48, '114', 'Inventario', 'ASV', 'NNG', 2, 'NNG', 'NNG', 'ASV'),
(49, '115', 'Materia prima', 'ASV', 'NNG', 2, 'NNG', 'NNG', 'ASV'),
(50, '116', 'Productos en proceso', 'ASV', 'NNG', 2, 'NNG', 'NNG', 'ASV'),
(51, '117', 'Producto terminado', 'ASV', 'NNG', 2, 'NNG', 'NNG', 'ASV'),
(52, '118', 'Otros circulantes', 'ASV', 'NNG', 2, 'CMPRS', 'NNG', 'ASV'),
(53, '119', 'Activo No Corriente', 'ASV', 'NNG', 2, 'NNG', 'NNG', 'ASV'),
(54, '120', 'Terrenos, mejoras y arrendamientos', 'ASV', 'NNG', 2, 'VLRS', 'NNG', 'ASV'),
(55, '121', 'Edificios', 'ASV', 'NNG', 2, 'NNG', 'NNG', 'ASV'),
(56, '122', 'Maquinaria y equipo', 'ASV', 'NNG', 2, 'NNG', 'NNG', 'ASV'),
(57, '123', 'Cosntrucciones en proceso', 'ASV', 'NNG', 2, 'NNG', 'NNG', 'ASV'),
(58, '124', 'Depreciacion y amortozacion', 'ASV', 'NNG', 2, 'NNG', 'NNG', 'ASV'),
(59, '125', 'Activo intangible', 'ASV', 'NNG', 2, 'NNG', 'NNG', 'ASV'),
(60, '126', 'otros activos', 'ASV', 'NNG', 2, 'NNG', 'NNG', 'ASV'),
(61, '127', 'Total Activos', 'ASV', 'NNG', 2, 'ACTV', 'TTACT', 'ASV'),
(62, '210', 'Pasivo Corriente', 'PSV', 'NNG', 2, 'PSVC', 'NNG', 'PSV'),
(63, '211', 'Cuentas por pagar', 'PSV', 'NNG', 2, 'NNG', 'NNG', 'PSV'),
(64, '212', 'Documentos por pagar', 'PSV', 'NNG', 2, 'NNG', 'NNG', 'PSV'),
(65, '213', 'Impuestos por pagar', 'PSV', 'NNG', 2, 'NNG', 'NNG', 'PSV'),
(66, '214', 'Pasivo No Corriente', 'PSV', 'NNG', 2, 'NNG', 'NNG', 'PSV'),
(67, '215', 'Porcion circulante del pasivo a largo plazo', 'PSV', 'NNG', 2, 'NNG', 'NNG', 'PSV'),
(68, '216', 'Pasivo a largo plazo', 'PSV', 'NNG', 2, 'NNG', 'NNG', 'PSV'),
(69, '217', 'Impuestos y otros creditos diferidos', 'PSV', 'NNG', 2, 'NNG', 'NNG', 'PSV'),
(70, '218', 'Intenres minotarios en otras subsidiarios', 'PSV', 'NNG', 2, 'NNG', 'NNG', 'PSV'),
(71, '219', 'Total Pasivos', 'PSV', 'NNG', 2, 'NNG', 'TTPSV', 'PSV'),
(72, '311', 'Acciones preferentes', 'PTR', 'NNG', 2, 'NNG', 'NNG', 'PTR'),
(73, '312', 'Acciones comunes', 'PTR', 'NNG', 2, 'NNG', 'NNG', 'PTR'),
(74, '314', 'Superavit de capital', 'PTR', 'NNG', 2, 'NNG', 'NNG', 'PTR'),
(75, '315', 'Utilidades retenidas', 'PTR', 'NNG', 2, 'NNG', 'NNG', 'PTR'),
(76, '316', 'Menos acciones tesoreria al costo', 'PTR', 'NNG', 2, 'NNG', 'NNG', 'PTR'),
(77, '317', 'Total Capital', 'PTR', 'NNG', 2, 'NNG', 'TTCPT', 'PTR'),
(78, '5101', 'Ingresos por Ventas', 'CRA', 'INOP', 2, 'NNG', 'NNG', 'ESR'),
(79, '4101', 'Costos de Venta', 'CRD', 'CTS', 2, 'NNG', 'NNG', 'ESR'),
(80, 'ub', 'Utilidad Bruta', 'ESR', 'NNG', 2, 'NNG', 'NNG', 'ESR'),
(81, '4201', 'Gastos de Ventas', 'CRD', 'GTOP', 2, 'NNG', 'NNG', 'ESR'),
(82, '4202', 'Gastos de Administración', 'CRD', 'GTOP', 2, 'VNTSN', 'NNG', 'ESR'),
(83, '4204', 'Gastos Financieros', 'CRD', 'GTOP', 2, 'NNG', 'NNG', 'ESR'),
(84, 'uo', 'Utilidad de Operación', 'ESR', 'NNG', 2, 'NNG', 'NNG', 'ESR'),
(85, '5102', 'Productos Financieros', 'CRA', 'INOP', 2, 'CSTDV', 'NNG', 'ESR'),
(86, 'ua', 'Utilidad antes de IsR', 'ESR', 'NNG', 2, 'NNG', 'NNG', 'ESR'),
(87, '4203', 'Impuesto sobre la Renta', 'CRD', 'GTOP', 2, 'CNTAPC', 'NNG', 'ESR'),
(88, 'un', 'Utilidad Neta', 'ESR', 'NNG', 2, 'CNTAPP', 'VNTST', 'ESR');


-- --------------------------------------------------------

--
-- Table structure for table `contabilidad_transaccion`
--

CREATE TABLE `contabilidad_transaccion` (
  `id` bigint NOT NULL,
  `monto` decimal(9,2) NOT NULL,
  `descripcion` varchar(255) NOT NULL,
  `slug` varchar(250) NOT NULL,
  `fecha_creacion` datetime(6) NOT NULL,
  `tipo_transaccion` varchar(3) NOT NULL,
  `naturaleza` varchar(3) NOT NULL,
  `cuenta_id` bigint NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `contabilidad_transaccion`
--

INSERT INTO `contabilidad_transaccion` (`id`, `monto`, `descripcion`, `slug`, `fecha_creacion`, `tipo_transaccion`, `naturaleza`, `cuenta_id`) VALUES
(1, 549400.00, 'Cuenta del 2023', 'Balance general', '2023-10-25 06:00:00.000000', 'CMP', 'DBT', 1),
(2, 548100.00, 'Cuenta del 2022', 'Balance general', '2022-10-25 06:00:00.000000', 'CMP', 'DBT', 1),
(3, 534400.00, 'Cuenta del 2021', 'Balance general', '2021-10-25 06:00:00.000000', 'CMP', 'DBT', 1),
(4, 534400.00, 'Cuenta del 2020', 'Balance general', '2020-10-25 06:00:00.000000', 'CMP', 'DBT', 1),
(5, 30000.00, 'Cuenta del 2023', 'Balance general', '2023-10-25 06:00:00.000000', 'CMP', 'DBT', 2),
(6, 33700.00, 'Cuenta del 2022', 'Balance general', '2022-10-25 06:00:00.000000', 'CMP', 'DBT', 2),
(7, 25000.00, 'Cuenta del 2021', 'Balance general', '2021-10-25 06:00:00.000000', 'CMP', 'DBT', 2),
(8, 25000.00, 'Cuenta del 2020', 'Balance general', '2020-10-25 06:00:00.000000', 'CMP', 'DBT', 2),
(9, 240100.00, 'Cuenta del 2023', 'Balance general', '2023-10-25 06:00:00.000000', 'CMP', 'DBT', 3),
(10, 237800.00, 'Cuenta del 2022', 'Balance general', '2022-10-25 06:00:00.000000', 'CMP', 'DBT', 3),
(11, 235500.00, 'Cuenta del 2021', 'Balance general', '2021-10-25 06:00:00.000000', 'CMP', 'DBT', 3),
(12, 235500.00, 'Cuenta del 2020', 'Balance general', '2020-10-25 06:00:00.000000', 'CMP', 'DBT', 3),
(13, 253400.00, 'Cuenta del 2023', 'Balance general', '2023-10-25 06:00:00.000000', 'CMP', 'DBT', 4),
(14, 251200.00, 'Cuenta del 2022', 'Balance general', '2022-10-25 06:00:00.000000', 'CMP', 'DBT', 4),
(15, 249000.00, 'Cuenta del 2021', 'Balance general', '2021-10-25 06:00:00.000000', 'CMP', 'DBT', 4),
(16, 249000.00, 'Cuenta del 2020', 'Balance general', '2020-10-25 06:00:00.000000', 'CMP', 'DBT', 4),
(17, 0.00, 'Cuenta del 2023', 'Balance general', '2023-10-25 06:00:00.000000', 'CMP', 'DBT', 5),
(18, 0.00, 'Cuenta del 2022', 'Balance general', '2022-10-25 06:00:00.000000', 'CMP', 'DBT', 5),
(19, 0.00, 'Cuenta del 2021', 'Balance general', '2021-10-25 06:00:00.000000', 'CMP', 'DBT', 5),
(20, 0.00, 'Cuenta del 2020', 'Balance general', '2020-10-25 06:00:00.000000', 'CMP', 'DBT', 5),
(21, 95600.00, 'Cuenta del 2023', 'Balance general', '2023-10-25 06:00:00.000000', 'CMP', 'DBT', 6),
(22, 94900.00, 'Cuenta del 2022', 'Balance general', '2022-10-25 06:00:00.000000', 'CMP', 'DBT', 6),
(23, 94200.00, 'Cuenta del 2021', 'Balance general', '2021-10-25 06:00:00.000000', 'CMP', 'DBT', 6),
(24, 94200.00, 'Cuenta del 2020', 'Balance general', '2020-10-25 06:00:00.000000', 'CMP', 'DBT', 6),
(25, 157800.00, 'Cuenta del 2023', 'Balance general', '2023-10-25 06:00:00.000000', 'CMP', 'DBT', 7),
(26, 156300.00, 'Cuenta del 2022', 'Balance general', '2022-10-25 06:00:00.000000', 'CMP', 'DBT', 7),
(27, 154800.00, 'Cuenta del 2021', 'Balance general', '2021-10-25 06:00:00.000000', 'CMP', 'DBT', 7),
(28, 154800.00, 'Cuenta del 2020', 'Balance general', '2020-10-25 06:00:00.000000', 'CMP', 'DBT', 7),
(29, 25900.00, 'Cuenta del 2023', 'Balance general', '2023-10-25 06:00:00.000000', 'CMP', 'DBT', 8),
(30, 25400.00, 'Cuenta del 2022', 'Balance general', '2022-10-25 06:00:00.000000', 'CMP', 'DBT', 8),
(31, 24900.00, 'Cuenta del 2021', 'Balance general', '2021-10-25 06:00:00.000000', 'CMP', 'DBT', 8),
(32, 24900.00, 'Cuenta del 2020', 'Balance general', '2020-10-25 06:00:00.000000', 'CMP', 'DBT', 8),
(33, 1492600.00, 'Cuenta del 2023', 'Balance general', '2023-10-25 06:00:00.000000', 'CMP', 'DBT', 9),
(34, 1480000.00, 'Cuenta del 2022', 'Balance general', '2022-10-25 06:00:00.000000', 'CMP', 'DBT', 9),
(35, 1467400.00, 'Cuenta del 2021', 'Balance general', '2021-10-25 06:00:00.000000', 'CMP', 'DBT', 9),
(36, 1467400.00, 'Cuenta del 2020', 'Balance general', '2020-10-25 06:00:00.000000', 'CMP', 'DBT', 9),
(37, 29200.00, 'Cuenta del 2023', 'Balance general', '2023-10-25 06:00:00.000000', 'CMP', 'DBT', 10),
(38, 28600.00, 'Cuenta del 2022', 'Balance general', '2022-10-25 06:00:00.000000', 'CMP', 'DBT', 10),
(39, 28000.00, 'Cuenta del 2021', 'Balance general', '2021-10-25 06:00:00.000000', 'CMP', 'DBT', 10),
(40, 28000.00, 'Cuenta del 2020', 'Balance general', '2020-10-25 06:00:00.000000', 'CMP', 'DBT', 10),
(41, 204900.00, 'Cuenta del 2023', 'Balance general', '2023-10-25 06:00:00.000000', 'CMP', 'DBT', 11),
(42, 203400.00, 'Cuenta del 2022', 'Balance general', '2022-10-25 06:00:00.000000', 'CMP', 'DBT', 11),
(43, 201900.00, 'Cuenta del 2021', 'Balance general', '2021-10-25 06:00:00.000000', 'CMP', 'DBT', 11),
(44, 201900.00, 'Cuenta del 2020', 'Balance general', '2020-10-25 06:00:00.000000', 'CMP', 'DBT', 11),
(45, 439500.00, 'Cuenta del 2023', 'Balance general', '2023-10-25 06:00:00.000000', 'CMP', 'DBT', 12),
(46, 436800.00, 'Cuenta del 2022', 'Balance general', '2022-10-25 06:00:00.000000', 'CMP', 'DBT', 12),
(47, 434100.00, 'Cuenta del 2021', 'Balance general', '2021-10-25 06:00:00.000000', 'CMP', 'DBT', 12),
(48, 434100.00, 'Cuenta del 2020', 'Balance general', '2020-10-25 06:00:00.000000', 'CMP', 'DBT', 12),
(49, 10400.00, 'Cuenta del 2023', 'Balance general', '2023-10-25 06:00:00.000000', 'CMP', 'DBT', 13),
(50, 10200.00, 'Cuenta del 2022', 'Balance general', '2022-10-25 06:00:00.000000', 'CMP', 'DBT', 13),
(51, 10000.00, 'Cuenta del 2021', 'Balance general', '2021-10-25 06:00:00.000000', 'CMP', 'DBT', 13),
(52, 10000.00, 'Cuenta del 2020', 'Balance general', '2020-10-25 06:00:00.000000', 'CMP', 'DBT', 13),
(53, 325900.00, 'Cuenta del 2023', 'Balance general', '2023-10-25 06:00:00.000000', 'CMP', 'DBT', 14),
(54, 323400.00, 'Cuenta del 2022', 'Balance general', '2022-10-25 06:00:00.000000', 'CMP', 'DBT', 14),
(55, 320900.00, 'Cuenta del 2021', 'Balance general', '2021-10-25 06:00:00.000000', 'CMP', 'DBT', 14),
(56, 320900.00, 'Cuenta del 2020', 'Balance general', '2020-10-25 06:00:00.000000', 'CMP', 'DBT', 14),
(57, 437300.00, 'Cuenta del 2023', 'Balance general', '2023-10-25 06:00:00.000000', 'CMP', 'DBT', 15),
(58, 432900.00, 'Cuenta del 2022', 'Balance general', '2022-10-25 06:00:00.000000', 'CMP', 'DBT', 15),
(59, 428500.00, 'Cuenta del 2021', 'Balance general', '2021-10-25 06:00:00.000000', 'CMP', 'DBT', 15),
(60, 428500.00, 'Cuenta del 2020', 'Balance general', '2020-10-25 06:00:00.000000', 'CMP', 'DBT', 15),
(61, 45400.00, 'Cuenta del 2023', 'Balance general', '2023-10-25 06:00:00.000000', 'CMP', 'DBT', 16),
(62, 44700.00, 'Cuenta del 2022', 'Balance general', '2022-10-25 06:00:00.000000', 'CMP', 'DBT', 16),
(63, 44000.00, 'Cuenta del 2021', 'Balance general', '2021-10-25 06:00:00.000000', 'CMP', 'DBT', 16),
(64, 44000.00, 'Cuenta del 2020', 'Balance general', '2020-10-25 06:00:00.000000', 'CMP', 'DBT', 16),
(65, 2042000.00, 'Cuenta del 2023', 'Balance general', '2023-10-25 06:00:00.000000', 'CMP', 'DBT', 17),
(66, 2028100.00, 'Cuenta del 2022', 'Balance general', '2022-10-25 06:00:00.000000', 'CMP', 'DBT', 17),
(67, 2001800.00, 'Cuenta del 2021', 'Balance general', '2021-10-25 06:00:00.000000', 'CMP', 'DBT', 17),
(68, 2001800.00, 'Cuenta del 2020', 'Balance general', '2020-10-25 06:00:00.000000', 'CMP', 'DBT', 17),
(69, 449000.00, 'Cuenta del 2023', 'Balance general', '2023-10-25 06:00:00.000000', 'CMP', 'DBT', 18),
(70, 444800.00, 'Cuenta del 2022', 'Balance general', '2022-10-25 06:00:00.000000', 'CMP', 'DBT', 18),
(71, 440600.00, 'Cuenta del 2021', 'Balance general', '2021-10-25 06:00:00.000000', 'CMP', 'DBT', 18),
(72, 440600.00, 'Cuenta del 2020', 'Balance general', '2020-10-25 06:00:00.000000', 'CMP', 'DBT', 18),
(73, 169500.00, 'Cuenta del 2023', 'Balance general', '2023-10-25 06:00:00.000000', 'CMP', 'DBT', 19),
(74, 167900.00, 'Cuenta del 2022', 'Balance general', '2022-10-25 06:00:00.000000', 'CMP', 'DBT', 19),
(75, 166300.00, 'Cuenta del 2021', 'Balance general', '2021-10-25 06:00:00.000000', 'CMP', 'DBT', 19),
(76, 166300.00, 'Cuenta del 2020', 'Balance general', '2020-10-25 06:00:00.000000', 'CMP', 'DBT', 19),
(77, 162300.00, 'Cuenta del 2023', 'Balance general', '2023-10-25 06:00:00.000000', 'CMP', 'DBT', 20),
(78, 160700.00, 'Cuenta del 2022', 'Balance general', '2022-10-25 06:00:00.000000', 'CMP', 'DBT', 20),
(79, 159100.00, 'Cuenta del 2021', 'Balance general', '2021-10-25 06:00:00.000000', 'CMP', 'DBT', 20),
(80, 159100.00, 'Cuenta del 2020', 'Balance general', '2020-10-25 06:00:00.000000', 'CMP', 'DBT', 20),
(81, 117200.00, 'Cuenta del 2023', 'Balance general', '2023-10-25 06:00:00.000000', 'CMP', 'DBT', 21),
(82, 116200.00, 'Cuenta del 2022', 'Balance general', '2022-10-25 06:00:00.000000', 'CMP', 'DBT', 21),
(83, 115200.00, 'Cuenta del 2021', 'Balance general', '2021-10-25 06:00:00.000000', 'CMP', 'DBT', 21),
(84, 115200.00, 'Cuenta del 2020', 'Balance general', '2020-10-25 06:00:00.000000', 'CMP', 'DBT', 21),
(85, 584800.00, 'Cuenta del 2023', 'Balance general', '2023-10-25 06:00:00.000000', 'CMP', 'DBT', 22),
(86, 581400.00, 'Cuenta del 2022', 'Balance general', '2022-10-25 06:00:00.000000', 'CMP', 'DBT', 22),
(87, 578000.00, 'Cuenta del 2021', 'Balance general', '2021-10-25 06:00:00.000000', 'CMP', 'DBT', 22),
(88, 578000.00, 'Cuenta del 2020', 'Balance general', '2020-10-25 06:00:00.000000', 'CMP', 'DBT', 22),
(89, 8500.00, 'Cuenta del 2023', 'Balance general', '2023-10-25 06:00:00.000000', 'CMP', 'DBT', 23),
(90, 8400.00, 'Cuenta del 2022', 'Balance general', '2022-10-25 06:00:00.000000', 'CMP', 'DBT', 23),
(91, 8300.00, 'Cuenta del 2021', 'Balance general', '2021-10-25 06:00:00.000000', 'CMP', 'DBT', 23),
(92, 8300.00, 'Cuenta del 2020', 'Balance general', '2020-10-25 06:00:00.000000', 'CMP', 'DBT', 23),
(93, 440900.00, 'Cuenta del 2023', 'Balance general', '2023-10-25 06:00:00.000000', 'CMP', 'DBT', 24),
(94, 439200.00, 'Cuenta del 2022', 'Balance general', '2022-10-25 06:00:00.000000', 'CMP', 'DBT', 24),
(95, 437500.00, 'Cuenta del 2021', 'Balance general', '2021-10-25 06:00:00.000000', 'CMP', 'DBT', 24),
(96, 437500.00, 'Cuenta del 2020', 'Balance general', '2020-10-25 06:00:00.000000', 'CMP', 'DBT', 24),
(97, 24700.00, 'Cuenta del 2023', 'Balance general', '2023-10-25 06:00:00.000000', 'CMP', 'DBT', 25),
(98, 24000.00, 'Cuenta del 2022', 'Balance general', '2022-10-25 06:00:00.000000', 'CMP', 'DBT', 25),
(99, 23300.00, 'Cuenta del 2021', 'Balance general', '2021-10-25 06:00:00.000000', 'CMP', 'DBT', 25),
(100, 23300.00, 'Cuenta del 2020', 'Balance general', '2020-10-25 06:00:00.000000', 'CMP', 'DBT', 25),
(101, 110700.00, 'Cuenta del 2023', 'Balance general', '2023-10-25 06:00:00.000000', 'CMP', 'DBT', 26),
(102, 109800.00, 'Cuenta del 2022', 'Balance general', '2022-10-25 06:00:00.000000', 'CMP', 'DBT', 26),
(103, 108900.00, 'Cuenta del 2021', 'Balance general', '2021-10-25 06:00:00.000000', 'CMP', 'DBT', 26),
(104, 108900.00, 'Cuenta del 2020', 'Balance general', '2020-10-25 06:00:00.000000', 'CMP', 'DBT', 26),
(105, 1033800.00, 'Cuenta del 2023', 'Balance general', '2023-10-25 06:00:00.000000', 'CMP', 'DBT', 27),
(106, 1026200.00, 'Cuenta del 2022', 'Balance general', '2022-10-25 06:00:00.000000', 'CMP', 'DBT', 27),
(107, 1018600.00, 'Cuenta del 2021', 'Balance general', '2021-10-25 06:00:00.000000', 'CMP', 'DBT', 27),
(108, 1018600.00, 'Cuenta del 2020', 'Balance general', '2020-10-25 06:00:00.000000', 'CMP', 'DBT', 27),
(109, 78500.00, 'Cuenta del 2023', 'Balance general', '2023-10-25 06:00:00.000000', 'CMP', 'DBT', 28),
(110, 77900.00, 'Cuenta del 2022', 'Balance general', '2022-10-25 06:00:00.000000', 'CMP', 'DBT', 28),
(111, 77300.00, 'Cuenta del 2021', 'Balance general', '2021-10-25 06:00:00.000000', 'CMP', 'DBT', 28),
(112, 77300.00, 'Cuenta del 2020', 'Balance general', '2020-10-25 06:00:00.000000', 'CMP', 'DBT', 28),
(113, 175900.00, 'Cuenta del 2023', 'Balance general', '2023-10-25 06:00:00.000000', 'CMP', 'DBT', 29),
(114, 174400.00, 'Cuenta del 2022', 'Balance general', '2022-10-25 06:00:00.000000', 'CMP', 'DBT', 29),
(115, 172900.00, 'Cuenta del 2021', 'Balance general', '2021-10-25 06:00:00.000000', 'CMP', 'DBT', 29),
(116, 172900.00, 'Cuenta del 2020', 'Balance general', '2020-10-25 06:00:00.000000', 'CMP', 'DBT', 29),
(117, 40400.00, 'Cuenta del 2023', 'Balance general', '2023-10-25 06:00:00.000000', 'CMP', 'DBT', 30),
(118, 39800.00, 'Cuenta del 2022', 'Balance general', '2022-10-25 06:00:00.000000', 'CMP', 'DBT', 30),
(119, 39200.00, 'Cuenta del 2021', 'Balance general', '2021-10-25 06:00:00.000000', 'CMP', 'DBT', 30),
(120, 39200.00, 'Cuenta del 2020', 'Balance general', '2020-10-25 06:00:00.000000', 'CMP', 'DBT', 30),
(121, 763100.00, 'Cuenta del 2023', 'Balance general', '2023-10-25 06:00:00.000000', 'CMP', 'DBT', 31),
(122, 756500.00, 'Cuenta del 2022', 'Balance general', '2022-10-25 06:00:00.000000', 'CMP', 'DBT', 31),
(123, 749900.00, 'Cuenta del 2021', 'Balance general', '2021-10-25 06:00:00.000000', 'CMP', 'DBT', 31),
(124, 749900.00, 'Cuenta del 2020', 'Balance general', '2020-10-25 06:00:00.000000', 'CMP', 'DBT', 31),
(125, 98900.00, 'Cuenta del 2023', 'Balance general', '2023-10-25 06:00:00.000000', 'CMP', 'DBT', 32),
(126, 98200.00, 'Cuenta del 2022', 'Balance general', '2022-10-25 06:00:00.000000', 'CMP', 'DBT', 32),
(127, 97500.00, 'Cuenta del 2021', 'Balance general', '2021-10-25 06:00:00.000000', 'CMP', 'DBT', 32),
(128, 97500.00, 'Cuenta del 2020', 'Balance general', '2020-10-25 06:00:00.000000', 'CMP', 'DBT', 32),
(129, 1156800.00, 'Cuenta del 2023', 'Balance general', '2023-10-25 06:00:00.000000', 'CMP', 'DBT', 33),
(130, 1146800.00, 'Cuenta del 2022', 'Balance general', '2022-10-25 06:00:00.000000', 'CMP', 'DBT', 33),
(131, 1136800.00, 'Cuenta del 2021', 'Balance general', '2021-10-25 06:00:00.000000', 'CMP', 'DBT', 33),
(132, 1136800.00, 'Cuenta del 2020', 'Balance general', '2020-10-25 06:00:00.000000', 'CMP', 'DBT', 33),
(133, 40000.00, 'Cuenta del 2023', 'Estado de Resultado', '2023-12-31 06:00:00.000000', 'OPE', 'DBT', 34),
(134, 20000.00, 'Cuenta del 2022', 'Estado de Resultado', '2022-12-31 06:00:00.000000', 'OPE', 'DBT', 34),
(135, 30000.00, 'Cuenta del 2021', 'Estado de Resultado', '2021-12-31 06:00:00.000000', 'OPE', 'DBT', 34),
(136, 25000.00, 'Cuenta del 2023', 'Estado de Resultado', '2023-12-31 06:00:00.000000', 'OPE', 'CRD', 35),
(137, 12000.00, 'Cuenta del 2022', 'Estado de Resultado', '2022-12-31 06:00:00.000000', 'OPE', 'CRD', 35),
(138, 18031.00, 'Cuenta del 2021', 'Estado de Resultado', '2021-12-31 06:00:00.000000', 'OPE', 'CRD', 35),
(139, 15000.00, 'Cuenta del 2023', 'Estado de Resultado', '2023-12-31 06:00:00.000000', 'OPE', 'CRD', 36),
(140, 8000.00, 'Cuenta del 2022', 'Estado de Resultado', '2022-12-31 06:00:00.000000', 'OPE', 'CRD', 36),
(141, 11969.00, 'Cuenta del 2021', 'Estado de Resultado', '2021-12-31 06:00:00.000000', 'OPE', 'CRD', 36),
(142, 4569.00, 'Cuenta del 2023', 'Estado de Resultado', '2023-12-31 06:00:00.000000', 'OPE', 'CRD', 37),
(143, 4569.00, 'Cuenta del 2022', 'Estado de Resultado', '2022-12-31 06:00:00.000000', 'OPE', 'CRD', 37),
(144, 4569.00, 'Cuenta del 2021', 'Estado de Resultado', '2021-12-31 06:00:00.000000', 'OPE', 'CRD', 37),
(145, 3057.00, 'Cuenta del 2023', 'Estado de Resultado', '2023-12-31 06:00:00.000000', 'OPE', 'CRD', 38),
(146, 3057.00, 'Cuenta del 2022', 'Estado de Resultado', '2022-12-31 06:00:00.000000', 'OPE', 'CRD', 38),
(147, 3057.00, 'Cuenta del 2021', 'Estado de Resultado', '2021-12-31 06:00:00.000000', 'OPE', 'CRD', 38),
(148, 0.00, 'Cuenta del 2023', 'Estado de Resultado', '2023-12-31 06:00:00.000000', 'OPE', 'CRD', 39),
(149, 0.00, 'Cuenta del 2022', 'Estado de Resultado', '2022-12-31 06:00:00.000000', 'OPE', 'CRD', 39),
(150, 0.00, 'Cuenta del 2021', 'Estado de Resultado', '2021-12-31 06:00:00.000000', 'OPE', 'CRD', 39),
(151, 7374.00, 'Cuenta del 2023', 'Estado de Resultado', '2023-12-31 06:00:00.000000', 'OPE', 'CRD', 40),
(152, 374.00, 'Cuenta del 2022', 'Estado de Resultado', '2022-12-31 06:00:00.000000', 'OPE', 'CRD', 40),
(153, 4343.00, 'Cuenta del 2021', 'Estado de Resultado', '2021-12-31 06:00:00.000000', 'OPE', 'CRD', 40),
(154, 3273.00, 'Cuenta del 2023', 'Estado de Resultado', '2023-12-31 06:00:00.000000', 'OPE', 'DBT', 41),
(155, 3273.00, 'Cuenta del 2022', 'Estado de Resultado', '2022-12-31 06:00:00.000000', 'OPE', 'DBT', 41),
(156, 3273.00, 'Cuenta del 2021', 'Estado de Resultado', '2021-12-31 06:00:00.000000', 'OPE', 'DBT', 41),
(157, 4101.00, 'Cuenta del 2023', 'Estado de Resultado', '2023-12-31 06:00:00.000000', 'OPE', 'DBT', 42),
(158, -2899.00, 'Cuenta del 2022', 'Estado de Resultado', '2022-12-31 06:00:00.000000', 'OPE', 'DBT', 42),
(159, 1070.00, 'Cuenta del 2021', 'Estado de Resultado', '2021-12-31 06:00:00.000000', 'OPE', 'DBT', 42),
(160, 0.00, 'Cuenta del 2023', 'Estado de Resultado', '2023-12-31 06:00:00.000000', 'OPE', 'CRD', 43),
(161, 0.00, 'Cuenta del 2022', 'Estado de Resultado', '2022-12-31 06:00:00.000000', 'OPE', 'CRD', 43),
(162, 0.00, 'Cuenta del 2021', 'Estado de Resultado', '2021-12-31 06:00:00.000000', 'OPE', 'CRD', 43),
(163, 4101.00, 'Cuenta del 2023', 'Estado de Resultado', '2023-12-31 06:00:00.000000', 'OPE', 'CRD', 44),
(164, -2899.00, 'Cuenta del 2022', 'Estado de Resultado', '2022-12-31 06:00:00.000000', 'OPE', 'CRD', 44),
(165, 1070.00, 'Cuenta del 2021', 'Estado de Resultado', '2021-12-31 06:00:00.000000', 'OPE', 'CRD', 44),
(166, 549400.00, 'Cuenta del 2023', 'Balance general', '2023-10-25 06:00:00.000000', 'CMP', 'DBT', 45),
(167, 548100.00, 'Cuenta del 2022', 'Balance general', '2022-10-25 06:00:00.000000', 'CMP', 'DBT', 45),
(168, 534400.00, 'Cuenta del 2021', 'Balance general', '2021-10-25 06:00:00.000000', 'CMP', 'DBT', 45),
(169, 534400.00, 'Cuenta del 2020', 'Balance general', '2020-10-25 06:00:00.000000', 'CMP', 'DBT', 45),
(170, 30000.00, 'Cuenta del 2023', 'Balance general', '2023-10-25 06:00:00.000000', 'CMP', 'DBT', 46),
(171, 33700.00, 'Cuenta del 2022', 'Balance general', '2022-10-25 06:00:00.000000', 'CMP', 'DBT', 46),
(172, 25000.00, 'Cuenta del 2021', 'Balance general', '2021-10-25 06:00:00.000000', 'CMP', 'DBT', 46),
(173, 25000.00, 'Cuenta del 2020', 'Balance general', '2020-10-25 06:00:00.000000', 'CMP', 'DBT', 46),
(174, 240100.00, 'Cuenta del 2023', 'Balance general', '2023-10-25 06:00:00.000000', 'CMP', 'DBT', 47),
(175, 237800.00, 'Cuenta del 2022', 'Balance general', '2022-10-25 06:00:00.000000', 'CMP', 'DBT', 47),
(176, 235500.00, 'Cuenta del 2021', 'Balance general', '2021-10-25 06:00:00.000000', 'CMP', 'DBT', 47),
(177, 235500.00, 'Cuenta del 2020', 'Balance general', '2020-10-25 06:00:00.000000', 'CMP', 'DBT', 47),
(178, 253400.00, 'Cuenta del 2023', 'Balance general', '2023-10-25 06:00:00.000000', 'CMP', 'DBT', 48),
(179, 251200.00, 'Cuenta del 2022', 'Balance general', '2022-10-25 06:00:00.000000', 'CMP', 'DBT', 48),
(180, 249000.00, 'Cuenta del 2021', 'Balance general', '2021-10-25 06:00:00.000000', 'CMP', 'DBT', 48),
(181, 249000.00, 'Cuenta del 2020', 'Balance general', '2020-10-25 06:00:00.000000', 'CMP', 'DBT', 48),
(182, 0.00, 'Cuenta del 2023', 'Balance general', '2023-10-25 06:00:00.000000', 'CMP', 'DBT', 49),
(183, 0.00, 'Cuenta del 2022', 'Balance general', '2022-10-25 06:00:00.000000', 'CMP', 'DBT', 49),
(184, 0.00, 'Cuenta del 2021', 'Balance general', '2021-10-25 06:00:00.000000', 'CMP', 'DBT', 49),
(185, 0.00, 'Cuenta del 2020', 'Balance general', '2020-10-25 06:00:00.000000', 'CMP', 'DBT', 49),
(186, 95600.00, 'Cuenta del 2023', 'Balance general', '2023-10-25 06:00:00.000000', 'CMP', 'DBT', 50),
(187, 94900.00, 'Cuenta del 2022', 'Balance general', '2022-10-25 06:00:00.000000', 'CMP', 'DBT', 50),
(188, 94200.00, 'Cuenta del 2021', 'Balance general', '2021-10-25 06:00:00.000000', 'CMP', 'DBT', 50),
(189, 94200.00, 'Cuenta del 2020', 'Balance general', '2020-10-25 06:00:00.000000', 'CMP', 'DBT', 50),
(190, 157800.00, 'Cuenta del 2023', 'Balance general', '2023-10-25 06:00:00.000000', 'CMP', 'DBT', 51),
(191, 156300.00, 'Cuenta del 2022', 'Balance general', '2022-10-25 06:00:00.000000', 'CMP', 'DBT', 51),
(192, 154800.00, 'Cuenta del 2021', 'Balance general', '2021-10-25 06:00:00.000000', 'CMP', 'DBT', 51),
(193, 154800.00, 'Cuenta del 2020', 'Balance general', '2020-10-25 06:00:00.000000', 'CMP', 'DBT', 51),
(194, 25900.00, 'Cuenta del 2023', 'Balance general', '2023-10-25 06:00:00.000000', 'CMP', 'DBT', 52),
(195, 25400.00, 'Cuenta del 2022', 'Balance general', '2022-10-25 06:00:00.000000', 'CMP', 'DBT', 52),
(196, 24900.00, 'Cuenta del 2021', 'Balance general', '2021-10-25 06:00:00.000000', 'CMP', 'DBT', 52),
(197, 24900.00, 'Cuenta del 2020', 'Balance general', '2020-10-25 06:00:00.000000', 'CMP', 'DBT', 52),
(198, 1492600.00, 'Cuenta del 2023', 'Balance general', '2023-10-25 06:00:00.000000', 'CMP', 'DBT', 53),
(199, 1480000.00, 'Cuenta del 2022', 'Balance general', '2022-10-25 06:00:00.000000', 'CMP', 'DBT', 53),
(200, 1467400.00, 'Cuenta del 2021', 'Balance general', '2021-10-25 06:00:00.000000', 'CMP', 'DBT', 53),
(201, 1467400.00, 'Cuenta del 2020', 'Balance general', '2020-10-25 06:00:00.000000', 'CMP', 'DBT', 53),
(202, 29200.00, 'Cuenta del 2023', 'Balance general', '2023-10-25 06:00:00.000000', 'CMP', 'DBT', 54),
(203, 28600.00, 'Cuenta del 2022', 'Balance general', '2022-10-25 06:00:00.000000', 'CMP', 'DBT', 54),
(204, 28000.00, 'Cuenta del 2021', 'Balance general', '2021-10-25 06:00:00.000000', 'CMP', 'DBT', 54),
(205, 28000.00, 'Cuenta del 2020', 'Balance general', '2020-10-25 06:00:00.000000', 'CMP', 'DBT', 54),
(206, 204900.00, 'Cuenta del 2023', 'Balance general', '2023-10-25 06:00:00.000000', 'CMP', 'DBT', 55),
(207, 203400.00, 'Cuenta del 2022', 'Balance general', '2022-10-25 06:00:00.000000', 'CMP', 'DBT', 55),
(208, 201900.00, 'Cuenta del 2021', 'Balance general', '2021-10-25 06:00:00.000000', 'CMP', 'DBT', 55),
(209, 201900.00, 'Cuenta del 2020', 'Balance general', '2020-10-25 06:00:00.000000', 'CMP', 'DBT', 55),
(210, 439500.00, 'Cuenta del 2023', 'Balance general', '2023-10-25 06:00:00.000000', 'CMP', 'DBT', 56),
(211, 436800.00, 'Cuenta del 2022', 'Balance general', '2022-10-25 06:00:00.000000', 'CMP', 'DBT', 56),
(212, 434100.00, 'Cuenta del 2021', 'Balance general', '2021-10-25 06:00:00.000000', 'CMP', 'DBT', 56),
(213, 434100.00, 'Cuenta del 2020', 'Balance general', '2020-10-25 06:00:00.000000', 'CMP', 'DBT', 56),
(214, 10400.00, 'Cuenta del 2023', 'Balance general', '2023-10-25 06:00:00.000000', 'CMP', 'DBT', 57),
(215, 10200.00, 'Cuenta del 2022', 'Balance general', '2022-10-25 06:00:00.000000', 'CMP', 'DBT', 57),
(216, 10000.00, 'Cuenta del 2021', 'Balance general', '2021-10-25 06:00:00.000000', 'CMP', 'DBT', 57),
(217, 10000.00, 'Cuenta del 2020', 'Balance general', '2020-10-25 06:00:00.000000', 'CMP', 'DBT', 57),
(218, 325900.00, 'Cuenta del 2023', 'Balance general', '2023-10-25 06:00:00.000000', 'CMP', 'DBT', 58),
(219, 323400.00, 'Cuenta del 2022', 'Balance general', '2022-10-25 06:00:00.000000', 'CMP', 'DBT', 58),
(220, 320900.00, 'Cuenta del 2021', 'Balance general', '2021-10-25 06:00:00.000000', 'CMP', 'DBT', 58),
(221, 320900.00, 'Cuenta del 2020', 'Balance general', '2020-10-25 06:00:00.000000', 'CMP', 'DBT', 58),
(222, 437300.00, 'Cuenta del 2023', 'Balance general', '2023-10-25 06:00:00.000000', 'CMP', 'DBT', 59),
(223, 432900.00, 'Cuenta del 2022', 'Balance general', '2022-10-25 06:00:00.000000', 'CMP', 'DBT', 59),
(224, 428500.00, 'Cuenta del 2021', 'Balance general', '2021-10-25 06:00:00.000000', 'CMP', 'DBT', 59),
(225, 428500.00, 'Cuenta del 2020', 'Balance general', '2020-10-25 06:00:00.000000', 'CMP', 'DBT', 59),
(226, 45400.00, 'Cuenta del 2023', 'Balance general', '2023-10-25 06:00:00.000000', 'CMP', 'DBT', 60),
(227, 44700.00, 'Cuenta del 2022', 'Balance general', '2022-10-25 06:00:00.000000', 'CMP', 'DBT', 60),
(228, 44000.00, 'Cuenta del 2021', 'Balance general', '2021-10-25 06:00:00.000000', 'CMP', 'DBT', 60),
(229, 44000.00, 'Cuenta del 2020', 'Balance general', '2020-10-25 06:00:00.000000', 'CMP', 'DBT', 60),
(230, 2042000.00, 'Cuenta del 2023', 'Balance general', '2023-10-25 06:00:00.000000', 'CMP', 'DBT', 61),
(231, 2028100.00, 'Cuenta del 2022', 'Balance general', '2022-10-25 06:00:00.000000', 'CMP', 'DBT', 61),
(232, 2001800.00, 'Cuenta del 2021', 'Balance general', '2021-10-25 06:00:00.000000', 'CMP', 'DBT', 61),
(233, 2001800.00, 'Cuenta del 2020', 'Balance general', '2020-10-25 06:00:00.000000', 'CMP', 'DBT', 61),
(234, 449000.00, 'Cuenta del 2023', 'Balance general', '2023-10-25 06:00:00.000000', 'CMP', 'DBT', 62),
(235, 444800.00, 'Cuenta del 2022', 'Balance general', '2022-10-25 06:00:00.000000', 'CMP', 'DBT', 62),
(236, 440600.00, 'Cuenta del 2021', 'Balance general', '2021-10-25 06:00:00.000000', 'CMP', 'DBT', 62),
(237, 440600.00, 'Cuenta del 2020', 'Balance general', '2020-10-25 06:00:00.000000', 'CMP', 'DBT', 62),
(238, 169500.00, 'Cuenta del 2023', 'Balance general', '2023-10-25 06:00:00.000000', 'CMP', 'DBT', 63),
(239, 167900.00, 'Cuenta del 2022', 'Balance general', '2022-10-25 06:00:00.000000', 'CMP', 'DBT', 63),
(240, 166300.00, 'Cuenta del 2021', 'Balance general', '2021-10-25 06:00:00.000000', 'CMP', 'DBT', 63),
(241, 166300.00, 'Cuenta del 2020', 'Balance general', '2020-10-25 06:00:00.000000', 'CMP', 'DBT', 63),
(242, 162300.00, 'Cuenta del 2023', 'Balance general', '2023-10-25 06:00:00.000000', 'CMP', 'DBT', 64),
(243, 160700.00, 'Cuenta del 2022', 'Balance general', '2022-10-25 06:00:00.000000', 'CMP', 'DBT', 64),
(244, 159100.00, 'Cuenta del 2021', 'Balance general', '2021-10-25 06:00:00.000000', 'CMP', 'DBT', 64),
(245, 159100.00, 'Cuenta del 2020', 'Balance general', '2020-10-25 06:00:00.000000', 'CMP', 'DBT', 64),
(246, 117200.00, 'Cuenta del 2023', 'Balance general', '2023-10-25 06:00:00.000000', 'CMP', 'DBT', 65),
(247, 116200.00, 'Cuenta del 2022', 'Balance general', '2022-10-25 06:00:00.000000', 'CMP', 'DBT', 65),
(248, 115200.00, 'Cuenta del 2021', 'Balance general', '2021-10-25 06:00:00.000000', 'CMP', 'DBT', 65),
(249, 115200.00, 'Cuenta del 2020', 'Balance general', '2020-10-25 06:00:00.000000', 'CMP', 'DBT', 65),
(250, 584800.00, 'Cuenta del 2023', 'Balance general', '2023-10-25 06:00:00.000000', 'CMP', 'DBT', 66),
(251, 581400.00, 'Cuenta del 2022', 'Balance general', '2022-10-25 06:00:00.000000', 'CMP', 'DBT', 66),
(252, 578000.00, 'Cuenta del 2021', 'Balance general', '2021-10-25 06:00:00.000000', 'CMP', 'DBT', 66),
(253, 578000.00, 'Cuenta del 2020', 'Balance general', '2020-10-25 06:00:00.000000', 'CMP', 'DBT', 66),
(254, 8500.00, 'Cuenta del 2023', 'Balance general', '2023-10-25 06:00:00.000000', 'CMP', 'DBT', 67),
(255, 8400.00, 'Cuenta del 2022', 'Balance general', '2022-10-25 06:00:00.000000', 'CMP', 'DBT', 67),
(256, 8300.00, 'Cuenta del 2021', 'Balance general', '2021-10-25 06:00:00.000000', 'CMP', 'DBT', 67),
(257, 8300.00, 'Cuenta del 2020', 'Balance general', '2020-10-25 06:00:00.000000', 'CMP', 'DBT', 67),
(258, 440900.00, 'Cuenta del 2023', 'Balance general', '2023-10-25 06:00:00.000000', 'CMP', 'DBT', 68),
(259, 439200.00, 'Cuenta del 2022', 'Balance general', '2022-10-25 06:00:00.000000', 'CMP', 'DBT', 68),
(260, 437500.00, 'Cuenta del 2021', 'Balance general', '2021-10-25 06:00:00.000000', 'CMP', 'DBT', 68),
(261, 437500.00, 'Cuenta del 2020', 'Balance general', '2020-10-25 06:00:00.000000', 'CMP', 'DBT', 68),
(262, 24700.00, 'Cuenta del 2023', 'Balance general', '2023-10-25 06:00:00.000000', 'CMP', 'DBT', 69),
(263, 24000.00, 'Cuenta del 2022', 'Balance general', '2022-10-25 06:00:00.000000', 'CMP', 'DBT', 69),
(264, 23300.00, 'Cuenta del 2021', 'Balance general', '2021-10-25 06:00:00.000000', 'CMP', 'DBT', 69),
(265, 23300.00, 'Cuenta del 2020', 'Balance general', '2020-10-25 06:00:00.000000', 'CMP', 'DBT', 69),
(266, 110700.00, 'Cuenta del 2023', 'Balance general', '2023-10-25 06:00:00.000000', 'CMP', 'DBT', 70),
(267, 109800.00, 'Cuenta del 2022', 'Balance general', '2022-10-25 06:00:00.000000', 'CMP', 'DBT', 70),
(268, 108900.00, 'Cuenta del 2021', 'Balance general', '2021-10-25 06:00:00.000000', 'CMP', 'DBT', 70),
(269, 108900.00, 'Cuenta del 2020', 'Balance general', '2020-10-25 06:00:00.000000', 'CMP', 'DBT', 70),
(270, 1033800.00, 'Cuenta del 2023', 'Balance general', '2023-10-25 06:00:00.000000', 'CMP', 'DBT', 71),
(271, 1026200.00, 'Cuenta del 2022', 'Balance general', '2022-10-25 06:00:00.000000', 'CMP', 'DBT', 71),
(272, 1018600.00, 'Cuenta del 2021', 'Balance general', '2021-10-25 06:00:00.000000', 'CMP', 'DBT', 71),
(273, 1018600.00, 'Cuenta del 2020', 'Balance general', '2020-10-25 06:00:00.000000', 'CMP', 'DBT', 71),
(274, 78500.00, 'Cuenta del 2023', 'Balance general', '2023-10-25 06:00:00.000000', 'CMP', 'DBT', 72),
(275, 77900.00, 'Cuenta del 2022', 'Balance general', '2022-10-25 06:00:00.000000', 'CMP', 'DBT', 72),
(276, 77300.00, 'Cuenta del 2021', 'Balance general', '2021-10-25 06:00:00.000000', 'CMP', 'DBT', 72),
(277, 77300.00, 'Cuenta del 2020', 'Balance general', '2020-10-25 06:00:00.000000', 'CMP', 'DBT', 72),
(278, 175900.00, 'Cuenta del 2023', 'Balance general', '2023-10-25 06:00:00.000000', 'CMP', 'DBT', 73),
(279, 174400.00, 'Cuenta del 2022', 'Balance general', '2022-10-25 06:00:00.000000', 'CMP', 'DBT', 73),
(280, 172900.00, 'Cuenta del 2021', 'Balance general', '2021-10-25 06:00:00.000000', 'CMP', 'DBT', 73),
(281, 172900.00, 'Cuenta del 2020', 'Balance general', '2020-10-25 06:00:00.000000', 'CMP', 'DBT', 73),
(282, 40400.00, 'Cuenta del 2023', 'Balance general', '2023-10-25 06:00:00.000000', 'CMP', 'DBT', 74),
(283, 39800.00, 'Cuenta del 2022', 'Balance general', '2022-10-25 06:00:00.000000', 'CMP', 'DBT', 74),
(284, 39200.00, 'Cuenta del 2021', 'Balance general', '2021-10-25 06:00:00.000000', 'CMP', 'DBT', 74),
(285, 39200.00, 'Cuenta del 2020', 'Balance general', '2020-10-25 06:00:00.000000', 'CMP', 'DBT', 74),
(286, 763100.00, 'Cuenta del 2023', 'Balance general', '2023-10-25 06:00:00.000000', 'CMP', 'DBT', 75),
(287, 756500.00, 'Cuenta del 2022', 'Balance general', '2022-10-25 06:00:00.000000', 'CMP', 'DBT', 75),
(288, 749900.00, 'Cuenta del 2021', 'Balance general', '2021-10-25 06:00:00.000000', 'CMP', 'DBT', 75),
(289, 749900.00, 'Cuenta del 2020', 'Balance general', '2020-10-25 06:00:00.000000', 'CMP', 'DBT', 75),
(290, 98900.00, 'Cuenta del 2023', 'Balance general', '2023-10-25 06:00:00.000000', 'CMP', 'DBT', 76),
(291, 98200.00, 'Cuenta del 2022', 'Balance general', '2022-10-25 06:00:00.000000', 'CMP', 'DBT', 76),
(292, 97500.00, 'Cuenta del 2021', 'Balance general', '2021-10-25 06:00:00.000000', 'CMP', 'DBT', 76),
(293, 97500.00, 'Cuenta del 2020', 'Balance general', '2020-10-25 06:00:00.000000', 'CMP', 'DBT', 76),
(294, 800.00, 'Cuenta del 2023', 'Balance general', '2023-10-25 06:00:00.000000', 'CMP', 'DBT', 77),
(295, 1146800.00, 'Cuenta del 2022', 'Balance general', '2022-10-25 06:00:00.000000', 'CMP', 'DBT', 77),
(296, 1136800.00, 'Cuenta del 2021', 'Balance general', '2021-10-25 06:00:00.000000', 'CMP', 'DBT', 77),
(297, 1136800.00, 'Cuenta del 2020', 'Balance general', '2020-10-25 06:00:00.000000', 'CMP', 'DBT', 77),
(298, 40000.00, 'Cuenta del 2023', 'Estado de Resultado', '2023-12-31 06:00:00.000000', 'OPE', 'DBT', 78),
(299, 20000.00, 'Cuenta del 2022', 'Estado de Resultado', '2022-12-31 06:00:00.000000', 'OPE', 'DBT', 78),
(300, 30000.00, 'Cuenta del 2021', 'Estado de Resultado', '2021-12-31 06:00:00.000000', 'OPE', 'DBT', 78),
(301, 30000.00, 'Cuenta del 2020', 'Estado de Resultado', '2020-12-31 06:00:00.000000', 'OPE', 'DBT', 78),
(302, 25000.00, 'Cuenta del 2023', 'Estado de Resultado', '2023-12-31 06:00:00.000000', 'OPE', 'CRD', 79),
(303, 12000.00, 'Cuenta del 2022', 'Estado de Resultado', '2022-12-31 06:00:00.000000', 'OPE', 'CRD', 79),
(304, 18031.00, 'Cuenta del 2021', 'Estado de Resultado', '2021-12-31 06:00:00.000000', 'OPE', 'CRD', 79),
(305, 18031.00, 'Cuenta del 2020', 'Estado de Resultado', '2020-12-31 06:00:00.000000', 'OPE', 'CRD', 79),
(306, 15000.00, 'Cuenta del 2023', 'Estado de Resultado', '2023-12-31 06:00:00.000000', 'OPE', 'CRD', 80),
(307, 8000.00, 'Cuenta del 2022', 'Estado de Resultado', '2022-12-31 06:00:00.000000', 'OPE', 'CRD', 80),
(308, 11969.00, 'Cuenta del 2021', 'Estado de Resultado', '2021-12-31 06:00:00.000000', 'OPE', 'CRD', 80),
(309, 11969.00, 'Cuenta del 2020', 'Estado de Resultado', '2020-12-31 06:00:00.000000', 'OPE', 'CRD', 80),
(310, 4569.00, 'Cuenta del 2023', 'Estado de Resultado', '2023-12-31 06:00:00.000000', 'OPE', 'CRD', 81),
(311, 4569.00, 'Cuenta del 2022', 'Estado de Resultado', '2022-12-31 06:00:00.000000', 'OPE', 'CRD', 81),
(312, 4569.00, 'Cuenta del 2021', 'Estado de Resultado', '2021-12-31 06:00:00.000000', 'OPE', 'CRD', 81),
(313, 4569.00, 'Cuenta del 2020', 'Estado de Resultado', '2020-12-31 06:00:00.000000', 'OPE', 'CRD', 81),
(314, 3057.00, 'Cuenta del 2023', 'Estado de Resultado', '2023-12-31 06:00:00.000000', 'OPE', 'CRD', 82),
(315, 3057.00, 'Cuenta del 2022', 'Estado de Resultado', '2022-12-31 06:00:00.000000', 'OPE', 'CRD', 82),
(316, 3057.00, 'Cuenta del 2021', 'Estado de Resultado', '2021-12-31 06:00:00.000000', 'OPE', 'CRD', 82),
(317, 3057.00, 'Cuenta del 2020', 'Estado de Resultado', '2020-12-31 06:00:00.000000', 'OPE', 'CRD', 82),
(318, 50.00, 'Cuenta del 2023', 'Estado de Resultado', '2023-12-31 06:00:00.000000', 'OPE', 'CRD', 83),
(319, 60.00, 'Cuenta del 2022', 'Estado de Resultado', '2022-12-31 06:00:00.000000', 'OPE', 'CRD', 83),
(320, 70.00, 'Cuenta del 2021', 'Estado de Resultado', '2021-12-31 06:00:00.000000', 'OPE', 'CRD', 83),
(321, 80.00, 'Cuenta del 2020', 'Estado de Resultado', '2020-12-31 06:00:00.000000', 'OPE', 'CRD', 83),
(322, 7374.00, 'Cuenta del 2023', 'Estado de Resultado', '2023-12-31 06:00:00.000000', 'OPE', 'CRD', 84),
(323, 374.00, 'Cuenta del 2022', 'Estado de Resultado', '2022-12-31 06:00:00.000000', 'OPE', 'CRD', 84),
(324, 4343.00, 'Cuenta del 2021', 'Estado de Resultado', '2021-12-31 06:00:00.000000', 'OPE', 'CRD', 84),
(325, 4343.00, 'Cuenta del 2020', 'Estado de Resultado', '2020-12-31 06:00:00.000000', 'OPE', 'CRD', 84),
(326, 3273.00, 'Cuenta del 2023', 'Estado de Resultado', '2023-12-31 06:00:00.000000', 'OPE', 'DBT', 85),
(327, 3273.00, 'Cuenta del 2022', 'Estado de Resultado', '2022-12-31 06:00:00.000000', 'OPE', 'DBT', 85),
(328, 3273.00, 'Cuenta del 2021', 'Estado de Resultado', '2021-12-31 06:00:00.000000', 'OPE', 'DBT', 85),
(329, 3273.00, 'Cuenta del 2020', 'Estado de Resultado', '2020-12-31 06:00:00.000000', 'OPE', 'DBT', 85),
(330, 4101.00, 'Cuenta del 2023', 'Estado de Resultado', '2023-12-31 06:00:00.000000', 'OPE', 'DBT', 86),
(331, -2899.00, 'Cuenta del 2022', 'Estado de Resultado', '2022-12-31 06:00:00.000000', 'OPE', 'DBT', 86),
(332, 1070.00, 'Cuenta del 2021', 'Estado de Resultado', '2021-12-31 06:00:00.000000', 'OPE', 'DBT', 86),
(333, 1070.00, 'Cuenta del 2020', 'Estado de Resultado', '2020-12-31 06:00:00.000000', 'OPE', 'DBT', 86),
(334, 25.00, 'Cuenta del 2023', 'Estado de Resultado', '2023-12-31 06:00:00.000000', 'OPE', 'CRD', 87),
(335, 28.00, 'Cuenta del 2022', 'Estado de Resultado', '2022-12-31 06:00:00.000000', 'OPE', 'CRD', 87),
(336, 30.00, 'Cuenta del 2021', 'Estado de Resultado', '2021-12-31 06:00:00.000000', 'OPE', 'CRD', 87),
(337, 50.00, 'Cuenta del 2020', 'Estado de Resultado', '2020-12-31 06:00:00.000000', 'OPE', 'CRD', 87),
(338, 4101.00, 'Cuenta del 2023', 'Estado de Resultado', '2023-12-31 06:00:00.000000', 'OPE', 'CRD', 88),
(339, -2899.00, 'Cuenta del 2022', 'Estado de Resultado', '2022-12-31 06:00:00.000000', 'OPE', 'CRD', 88),
(340, 1070.00, 'Cuenta del 2021', 'Estado de Resultado', '2021-12-31 06:00:00.000000', 'OPE', 'CRD', 88),
(341, 1070.00, 'Cuenta del 2020', 'Estado de Resultado', '2020-12-31 06:00:00.000000', 'OPE', 'CRD', 88);

-- --------------------------------------------------------

--
-- Table structure for table `auth_group`
--

CREATE TABLE `auth_group` (
  `id` int NOT NULL,
  `name` varchar(150) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `auth_group_permissions`
--

CREATE TABLE `auth_group_permissions` (
  `id` bigint NOT NULL,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `auth_permission`
--

CREATE TABLE `auth_permission` (
  `id` int NOT NULL,
  `name` varchar(255) NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `auth_permission`
--

INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES
(1, 'Can add log entry', 1, 'add_logentry'),
(2, 'Can change log entry', 1, 'change_logentry'),
(3, 'Can delete log entry', 1, 'delete_logentry'),
(4, 'Can view log entry', 1, 'view_logentry'),
(5, 'Can add permission', 2, 'add_permission'),
(6, 'Can change permission', 2, 'change_permission'),
(7, 'Can delete permission', 2, 'delete_permission'),
(8, 'Can view permission', 2, 'view_permission'),
(9, 'Can add group', 3, 'add_group'),
(10, 'Can change group', 3, 'change_group'),
(11, 'Can delete group', 3, 'delete_group'),
(12, 'Can view group', 3, 'view_group'),
(13, 'Can add user', 4, 'add_user'),
(14, 'Can change user', 4, 'change_user'),
(15, 'Can delete user', 4, 'delete_user'),
(16, 'Can view user', 4, 'view_user'),
(17, 'Can add content type', 5, 'add_contenttype'),
(18, 'Can change content type', 5, 'change_contenttype'),
(19, 'Can delete content type', 5, 'delete_contenttype'),
(20, 'Can view content type', 5, 'view_contenttype'),
(21, 'Can add session', 6, 'add_session'),
(22, 'Can change session', 6, 'change_session'),
(23, 'Can delete session', 6, 'delete_session'),
(24, 'Can view session', 6, 'view_session'),
(25, 'Can add catalogo', 7, 'add_catalogo'),
(26, 'Can change catalogo', 7, 'change_catalogo'),
(27, 'Can delete catalogo', 7, 'delete_catalogo'),
(28, 'Can view catalogo', 7, 'view_catalogo'),
(29, 'Can add cuenta', 8, 'add_cuenta'),
(30, 'Can change cuenta', 8, 'change_cuenta'),
(31, 'Can delete cuenta', 8, 'delete_cuenta'),
(32, 'Can view cuenta', 8, 'view_cuenta'),
(33, 'Can add transaccion', 9, 'add_transaccion'),
(34, 'Can change transaccion', 9, 'change_transaccion'),
(35, 'Can delete transaccion', 9, 'delete_transaccion'),
(36, 'Can view transaccion', 9, 'view_transaccion'),
(37, 'Can add propietario', 10, 'add_propietario'),
(38, 'Can change propietario', 10, 'change_propietario'),
(39, 'Can delete propietario', 10, 'delete_propietario'),
(40, 'Can view propietario', 10, 'view_propietario'),
(41, 'Can add empresa', 11, 'add_empresa'),
(42, 'Can change empresa', 11, 'change_empresa'),
(43, 'Can delete empresa', 11, 'delete_empresa'),
(44, 'Can view empresa', 11, 'view_empresa'),
(45, 'Can add ratio', 12, 'add_ratio'),
(46, 'Can change ratio', 12, 'change_ratio'),
(47, 'Can delete ratio', 12, 'delete_ratio'),
(48, 'Can view ratio', 12, 'view_ratio');

-- --------------------------------------------------------

--
-- Table structure for table `auth_user`
--

CREATE TABLE `auth_user` (
  `id` int NOT NULL,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `auth_user`
--

INSERT INTO `auth_user` (`id`, `password`, `last_login`, `is_superuser`, `username`, `first_name`, `last_name`, `email`, `is_staff`, `is_active`, `date_joined`) VALUES
(1, 'pbkdf2_sha256$600000$Y8hfQxeEKH6y5geTfr2YFg$QnMNntHxwhNAYJZ/BrgQTO9qkEQLCIwVteO83QlvOEs=', '2023-11-05 23:02:11.649777', 0, 'user1', '', '', 'sdfasdf@mail.com', 0, 1, '2023-11-05 23:02:06.557984'),
(2, 'pbkdf2_sha256$600000$9eWTZF2LWyOzAbHhgrXTkr$V3acmgyNQCQlGYkDCN39yQi9ErRqxYyUbIoXJ/hBThw=', '2023-11-06 01:08:02.908404', 0, 'user2', '', '', 'jsafsa@mail.com', 0, 1, '2023-11-05 23:08:15.050047');

-- --------------------------------------------------------

--
-- Table structure for table `auth_user_groups`
--

CREATE TABLE `auth_user_groups` (
  `id` bigint NOT NULL,
  `user_id` int NOT NULL,
  `group_id` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `auth_user_user_permissions`
--

CREATE TABLE `auth_user_user_permissions` (
  `id` bigint NOT NULL,
  `user_id` int NOT NULL,
  `permission_id` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


--
-- Table structure for table `contabilidad_ratio`
--

CREATE TABLE `contabilidad_ratio` (
  `id` bigint NOT NULL,
  `nombre_ratio` varchar(5) NOT NULL,
  `valor` decimal(9,2) NOT NULL,
  `empresa_id` bigint NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Table structure for table `django_admin_log`
--

CREATE TABLE `django_admin_log` (
  `id` int NOT NULL,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint UNSIGNED NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` int NOT NULL
) ;

-- --------------------------------------------------------

--
-- Table structure for table `django_content_type`
--

CREATE TABLE `django_content_type` (
  `id` int NOT NULL,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `django_content_type`
--

INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES
(1, 'admin', 'logentry'),
(3, 'auth', 'group'),
(2, 'auth', 'permission'),
(4, 'auth', 'user'),
(7, 'contabilidad', 'catalogo'),
(8, 'contabilidad', 'cuenta'),
(11, 'contabilidad', 'empresa'),
(10, 'contabilidad', 'propietario'),
(12, 'contabilidad', 'ratio'),
(9, 'contabilidad', 'transaccion'),
(5, 'contenttypes', 'contenttype'),
(6, 'sessions', 'session');

-- --------------------------------------------------------

--
-- Table structure for table `django_migrations`
--

CREATE TABLE `django_migrations` (
  `id` bigint NOT NULL,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `django_migrations`
--

INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES
(1, 'contenttypes', '0001_initial', '2023-11-05 22:26:19.262308'),
(2, 'auth', '0001_initial', '2023-11-05 22:26:42.479342'),
(3, 'admin', '0001_initial', '2023-11-05 22:26:47.830941'),
(4, 'admin', '0002_logentry_remove_auto_add', '2023-11-05 22:26:48.022062'),
(5, 'admin', '0003_logentry_add_action_flag_choices', '2023-11-05 22:26:48.194544'),
(6, 'contenttypes', '0002_remove_content_type_name', '2023-11-05 22:26:51.255720'),
(7, 'auth', '0002_alter_permission_name_max_length', '2023-11-05 22:26:53.709217'),
(8, 'auth', '0003_alter_user_email_max_length', '2023-11-05 22:26:54.199187'),
(9, 'auth', '0004_alter_user_username_opts', '2023-11-05 22:26:54.356408'),
(10, 'auth', '0005_alter_user_last_login_null', '2023-11-05 22:26:56.623369'),
(11, 'auth', '0006_require_contenttypes_0002', '2023-11-05 22:26:56.765277'),
(12, 'auth', '0007_alter_validators_add_error_messages', '2023-11-05 22:26:56.888504'),
(13, 'auth', '0008_alter_user_username_max_length', '2023-11-05 22:26:59.554632'),
(14, 'auth', '0009_alter_user_last_name_max_length', '2023-11-05 22:27:01.977866'),
(15, 'auth', '0010_alter_group_name_max_length', '2023-11-05 22:27:02.325928'),
(16, 'auth', '0011_update_proxy_permissions', '2023-11-05 22:27:02.485465'),
(17, 'auth', '0012_alter_user_first_name_max_length', '2023-11-05 22:27:04.917027'),
(18, 'contabilidad', '0001_initial', '2023-11-05 22:27:22.090151'),
(19, 'contabilidad', '0002_rename_catalago_cuenta_catalogo_and_more', '2023-11-05 22:27:25.580313'),
(20, 'contabilidad', '0003_alter_catalogo_nombre_catalogo_and_more', '2023-11-05 22:27:25.736991'),
(21, 'contabilidad', '0004_empresa_sector', '2023-11-05 22:27:26.783435'),
(22, 'contabilidad', '0005_alter_cuenta_subcategoria_ratio', '2023-11-05 22:27:29.799463'),
(23, 'contabilidad', '0006_cuenta_cuenta_ratio', '2023-11-05 22:27:30.729406'),
(24, 'contabilidad', '0007_alter_cuenta_cuenta_ratio_alter_ratio_nombre_ratio', '2023-11-05 22:27:31.053793'),
(25, 'contabilidad', '0008_alter_cuenta_cuenta_ratio', '2023-11-05 22:27:31.221838'),
(26, 'contabilidad', '0009_alter_empresa_sector', '2023-11-05 22:27:31.341084'),
(27, 'contabilidad', '0010_cuenta_cuenta_av_alter_cuenta_subcategoria', '2023-11-05 22:27:32.581574'),
(28, 'contabilidad', '0011_cuenta_categoria_av', '2023-11-05 22:27:33.509048'),
(29, 'sessions', '0001_initial', '2023-11-05 22:27:35.101032');

-- --------------------------------------------------------

--
-- Table structure for table `django_session`
--

CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `auth_group`
--
ALTER TABLE `auth_group`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Indexes for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  ADD KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`);

--
-- Indexes for table `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`);

--
-- Indexes for table `auth_user`
--
ALTER TABLE `auth_user`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- Indexes for table `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  ADD KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`);

--
-- Indexes for table `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  ADD KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`);

--
-- Indexes for table `contabilidad_catalogo`
--
ALTER TABLE `contabilidad_catalogo`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `contabilidad_cuenta`
--
ALTER TABLE `contabilidad_cuenta`
  ADD PRIMARY KEY (`id`),
  ADD KEY `contabilidad_cuenta_catalogo_id_0fb31f97_fk_contabili` (`catalogo_id`);

--
-- Indexes for table `contabilidad_empresa`
--
ALTER TABLE `contabilidad_empresa`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `catalogo_empresa_id` (`catalogo_empresa_id`),
  ADD UNIQUE KEY `propietario_id` (`propietario_id`);

--
-- Indexes for table `contabilidad_propietario`
--
ALTER TABLE `contabilidad_propietario`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `user_id` (`user_id`);

--
-- Indexes for table `contabilidad_ratio`
--
ALTER TABLE `contabilidad_ratio`
  ADD PRIMARY KEY (`id`),
  ADD KEY `contabilidad_ratio_empresa_id_58d05f46_fk_contabili` (`empresa_id`);

--
-- Indexes for table `contabilidad_transaccion`
--
ALTER TABLE `contabilidad_transaccion`
  ADD PRIMARY KEY (`id`),
  ADD KEY `contabilidad_transac_cuenta_id_7eb70f2b_fk_contabili` (`cuenta_id`),
  ADD KEY `contabilidad_transaccion_slug_a7e1a5d2` (`slug`);

--
-- Indexes for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD PRIMARY KEY (`id`),
  ADD KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  ADD KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`);

--
-- Indexes for table `django_content_type`
--
ALTER TABLE `django_content_type`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`);

--
-- Indexes for table `django_migrations`
--
ALTER TABLE `django_migrations`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `django_session`
--
ALTER TABLE `django_session`
  ADD PRIMARY KEY (`session_key`),
  ADD KEY `django_session_expire_date_a5c62663` (`expire_date`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `auth_group`
--
ALTER TABLE `auth_group`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `auth_permission`
--
ALTER TABLE `auth_permission`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=49;

--
-- AUTO_INCREMENT for table `auth_user`
--
ALTER TABLE `auth_user`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `contabilidad_catalogo`
--
ALTER TABLE `contabilidad_catalogo`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `contabilidad_cuenta`
--
ALTER TABLE `contabilidad_cuenta`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=89;

--
-- AUTO_INCREMENT for table `contabilidad_empresa`
--
ALTER TABLE `contabilidad_empresa`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `contabilidad_propietario`
--
ALTER TABLE `contabilidad_propietario`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `contabilidad_ratio`
--
ALTER TABLE `contabilidad_ratio`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `contabilidad_transaccion`
--
ALTER TABLE `contabilidad_transaccion`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=342;

--
-- AUTO_INCREMENT for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `django_content_type`
--
ALTER TABLE `django_content_type`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT for table `django_migrations`
--
ALTER TABLE `django_migrations`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=30;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`);

--
-- Constraints for table `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`);

--
-- Constraints for table `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  ADD CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  ADD CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Constraints for table `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  ADD CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Constraints for table `contabilidad_cuenta`
--
ALTER TABLE `contabilidad_cuenta`
  ADD CONSTRAINT `contabilidad_cuenta_catalogo_id_0fb31f97_fk_contabili` FOREIGN KEY (`catalogo_id`) REFERENCES `contabilidad_catalogo` (`id`);

--
-- Constraints for table `contabilidad_empresa`
--
ALTER TABLE `contabilidad_empresa`
  ADD CONSTRAINT `contabilidad_empresa_catalogo_empresa_id_c680799e_fk_contabili` FOREIGN KEY (`catalogo_empresa_id`) REFERENCES `contabilidad_catalogo` (`id`),
  ADD CONSTRAINT `contabilidad_empresa_propietario_id_5f5183ce_fk_contabili` FOREIGN KEY (`propietario_id`) REFERENCES `contabilidad_propietario` (`id`);

--
-- Constraints for table `contabilidad_propietario`
--
ALTER TABLE `contabilidad_propietario`
  ADD CONSTRAINT `contabilidad_propietario_user_id_f315de92_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Constraints for table `contabilidad_ratio`
--
ALTER TABLE `contabilidad_ratio`
  ADD CONSTRAINT `contabilidad_ratio_empresa_id_58d05f46_fk_contabili` FOREIGN KEY (`empresa_id`) REFERENCES `contabilidad_empresa` (`id`);

--
-- Constraints for table `contabilidad_transaccion`
--
ALTER TABLE `contabilidad_transaccion`
  ADD CONSTRAINT `contabilidad_transac_cuenta_id_7eb70f2b_fk_contabili` FOREIGN KEY (`cuenta_id`) REFERENCES `contabilidad_cuenta` (`id`);

--
-- Constraints for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  ADD CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

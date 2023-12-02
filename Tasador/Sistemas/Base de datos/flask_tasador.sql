-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 19-11-2023 a las 22:31:48
-- Versión del servidor: 8.1.0
-- Versión de PHP: 8.2.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `flask_tasador`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `datos_propiedad`
--

CREATE TABLE `datos_propiedad` (
  `id` int NOT NULL COMMENT 'Numero de identificación de cada tasacion.',
  `comuna` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT 'Comunas de valparaiso.',
  `region` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT 'Regiones disponibles.',
  `area_total` float(90,4) NOT NULL COMMENT 'Area total de la propiedad.',
  `area_construida` float(90,4) NOT NULL COMMENT 'Area construida en la propiedad.',
  `condicion` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT 'Condicion de la propiedad.',
  `fecha_ingreso` timestamp NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'Fecha de la tasación.',
  `estacionamientos` int NOT NULL COMMENT 'Número de estacionamientos de la propiedad.',
  `baños` int NOT NULL COMMENT 'Cantidad de baños de la propiedad.',
  `operacion` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT 'Venta o arriendo.',
  `dormitorio` int NOT NULL COMMENT 'Cantidad de dormitorios de la propiedad.',
  `tipo_propiedad` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT 'Casa o depto.',
  `direccion` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT 'Direccion de la propiedad.',
  `longitud` float DEFAULT NULL COMMENT 'Longitud geográfica.',
  `latitud` float DEFAULT NULL COMMENT 'Latitud geográfica.',
  `valor_predicho` float(90,2) DEFAULT NULL COMMENT 'Prediccion de la tasación.'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Volcado de datos para la tabla `datos_propiedad`
--

INSERT INTO `datos_propiedad` (`id`, `comuna`, `region`, `area_total`, `area_construida`, `condicion`, `fecha_ingreso`, `estacionamientos`, `baños`, `operacion`, `dormitorio`, `tipo_propiedad`, `direccion`, `longitud`, `latitud`, `valor_predicho`) VALUES
(497, 'Limache', 'Valparaiso', 125.0000, 110.0000, 'usado', '2023-11-19 02:01:42', 2, 1, 'venta', 2, 'depto', 'El Sauce, Limache, Chile', -71.2636, -33.014, 9452.09),
(498, 'Viña', 'Valparaiso', 125.0000, 110.0000, 'usado', '2023-11-19 02:01:59', 2, 1, 'venta', 2, 'depto', '5 Norte, Viña del Mar, Chile', -71.5494, -33.0186, 9242.16),
(499, 'Quilpue', 'Valparaiso', 125.0000, 110.0000, 'usado', '2023-11-19 02:02:32', 2, 1, 'venta', 2, 'depto', 'Los Carreras, Quilpué, Chile', -71.4287, -33.049, 7607.61),
(500, 'Concon', 'Valparaiso', 125.0000, 110.0000, 'usado', '2023-11-19 02:02:44', 2, 1, 'venta', 2, 'depto', 'Concón, Chile', -71.5186, -32.9299, 9041.80),
(501, 'Quillota', 'Valparaiso', 125.0000, 110.0000, 'usado', '2023-11-19 02:03:00', 2, 1, 'venta', 2, 'depto', 'Quillota, Chile', -71.2497, -32.8803, 9041.80),
(502, 'Viña', 'Valparaiso', 120.0000, 110.0000, 'usado', '2023-11-19 03:18:16', 2, 2, 'venta', 2, 'casa', 'Viña del Mar, Chile', -71.55, -33.0153, 8329.02),
(503, 'Quilpue', 'Valparaiso', 120.0000, 110.0000, 'usado', '2023-11-19 03:18:19', 2, 2, 'venta', 2, 'casa', 'Viña del Mar, Chile', -71.55, -33.0153, 8329.02);

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `datos_propiedad`
--
ALTER TABLE `datos_propiedad`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `datos_propiedad`
--
ALTER TABLE `datos_propiedad`
  MODIFY `id` int NOT NULL AUTO_INCREMENT COMMENT 'Numero de identificación de cada tasacion.', AUTO_INCREMENT=504;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

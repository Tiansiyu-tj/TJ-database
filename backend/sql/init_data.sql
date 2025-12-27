-- ============================================
-- 嘉定出行后端数据库初始数据
-- ============================================

-- 设置客户端字符集为 UTF-8
SET NAMES utf8mb4;
SET CHARACTER SET utf8mb4;
SET character_set_connection=utf8mb4;

USE jiading_commute;

-- ============================================
-- 1. DZ1 短驳时刻表
-- ============================================

-- DZ1 工作日 校区→地铁站
INSERT INTO commute_schedule (campus, route_key, day_type, direction, departure_time) VALUES
('jiading', 'dz1', 'weekday', 'campusToStation', '07:10'),
('jiading', 'dz1', 'weekday', 'campusToStation', '07:30'),
('jiading', 'dz1', 'weekday', 'campusToStation', '07:50'),
('jiading', 'dz1', 'weekday', 'campusToStation', '08:10'),
('jiading', 'dz1', 'weekday', 'campusToStation', '08:30'),
('jiading', 'dz1', 'weekday', 'campusToStation', '09:00'),
('jiading', 'dz1', 'weekday', 'campusToStation', '09:30'),
('jiading', 'dz1', 'weekday', 'campusToStation', '10:00'),
('jiading', 'dz1', 'weekday', 'campusToStation', '10:30'),
('jiading', 'dz1', 'weekday', 'campusToStation', '11:00'),
('jiading', 'dz1', 'weekday', 'campusToStation', '11:30'),
('jiading', 'dz1', 'weekday', 'campusToStation', '12:00'),
('jiading', 'dz1', 'weekday', 'campusToStation', '12:30'),
('jiading', 'dz1', 'weekday', 'campusToStation', '13:00'),
('jiading', 'dz1', 'weekday', 'campusToStation', '13:30'),
('jiading', 'dz1', 'weekday', 'campusToStation', '14:00'),
('jiading', 'dz1', 'weekday', 'campusToStation', '14:30'),
('jiading', 'dz1', 'weekday', 'campusToStation', '15:00'),
('jiading', 'dz1', 'weekday', 'campusToStation', '15:30'),
('jiading', 'dz1', 'weekday', 'campusToStation', '16:00'),
('jiading', 'dz1', 'weekday', 'campusToStation', '16:30'),
('jiading', 'dz1', 'weekday', 'campusToStation', '17:00'),
('jiading', 'dz1', 'weekday', 'campusToStation', '17:30'),
('jiading', 'dz1', 'weekday', 'campusToStation', '18:00'),
('jiading', 'dz1', 'weekday', 'campusToStation', '18:30'),
('jiading', 'dz1', 'weekday', 'campusToStation', '19:00'),
('jiading', 'dz1', 'weekday', 'campusToStation', '19:30'),
('jiading', 'dz1', 'weekday', 'campusToStation', '20:00'),
('jiading', 'dz1', 'weekday', 'campusToStation', '20:30'),
('jiading', 'dz1', 'weekday', 'campusToStation', '21:00');

-- DZ1 工作日 地铁站→校区
INSERT INTO commute_schedule (campus, route_key, day_type, direction, departure_time) VALUES
('jiading', 'dz1', 'weekday', 'stationToCampus', '07:20'),
('jiading', 'dz1', 'weekday', 'stationToCampus', '07:40'),
('jiading', 'dz1', 'weekday', 'stationToCampus', '08:00'),
('jiading', 'dz1', 'weekday', 'stationToCampus', '08:20'),
('jiading', 'dz1', 'weekday', 'stationToCampus', '08:40'),
('jiading', 'dz1', 'weekday', 'stationToCampus', '09:10'),
('jiading', 'dz1', 'weekday', 'stationToCampus', '09:40'),
('jiading', 'dz1', 'weekday', 'stationToCampus', '10:10'),
('jiading', 'dz1', 'weekday', 'stationToCampus', '10:40'),
('jiading', 'dz1', 'weekday', 'stationToCampus', '11:10'),
('jiading', 'dz1', 'weekday', 'stationToCampus', '11:40'),
('jiading', 'dz1', 'weekday', 'stationToCampus', '12:10'),
('jiading', 'dz1', 'weekday', 'stationToCampus', '12:40'),
('jiading', 'dz1', 'weekday', 'stationToCampus', '13:10'),
('jiading', 'dz1', 'weekday', 'stationToCampus', '13:40'),
('jiading', 'dz1', 'weekday', 'stationToCampus', '14:10'),
('jiading', 'dz1', 'weekday', 'stationToCampus', '14:40'),
('jiading', 'dz1', 'weekday', 'stationToCampus', '15:10'),
('jiading', 'dz1', 'weekday', 'stationToCampus', '15:40'),
('jiading', 'dz1', 'weekday', 'stationToCampus', '16:10'),
('jiading', 'dz1', 'weekday', 'stationToCampus', '16:40'),
('jiading', 'dz1', 'weekday', 'stationToCampus', '17:10'),
('jiading', 'dz1', 'weekday', 'stationToCampus', '17:40'),
('jiading', 'dz1', 'weekday', 'stationToCampus', '18:10'),
('jiading', 'dz1', 'weekday', 'stationToCampus', '18:40'),
('jiading', 'dz1', 'weekday', 'stationToCampus', '19:10'),
('jiading', 'dz1', 'weekday', 'stationToCampus', '19:40'),
('jiading', 'dz1', 'weekday', 'stationToCampus', '20:10'),
('jiading', 'dz1', 'weekday', 'stationToCampus', '20:40'),
('jiading', 'dz1', 'weekday', 'stationToCampus', '21:10');

-- DZ1 周末 校区→地铁站
INSERT INTO commute_schedule (campus, route_key, day_type, direction, departure_time) VALUES
('jiading', 'dz1', 'weekend', 'campusToStation', '08:00'),
('jiading', 'dz1', 'weekend', 'campusToStation', '09:00'),
('jiading', 'dz1', 'weekend', 'campusToStation', '10:00'),
('jiading', 'dz1', 'weekend', 'campusToStation', '11:00'),
('jiading', 'dz1', 'weekend', 'campusToStation', '12:00'),
('jiading', 'dz1', 'weekend', 'campusToStation', '13:00'),
('jiading', 'dz1', 'weekend', 'campusToStation', '14:00'),
('jiading', 'dz1', 'weekend', 'campusToStation', '15:00'),
('jiading', 'dz1', 'weekend', 'campusToStation', '16:00'),
('jiading', 'dz1', 'weekend', 'campusToStation', '17:00'),
('jiading', 'dz1', 'weekend', 'campusToStation', '18:00'),
('jiading', 'dz1', 'weekend', 'campusToStation', '19:00'),
('jiading', 'dz1', 'weekend', 'campusToStation', '20:00');

-- DZ1 周末 地铁站→校区
INSERT INTO commute_schedule (campus, route_key, day_type, direction, departure_time) VALUES
('jiading', 'dz1', 'weekend', 'stationToCampus', '08:15'),
('jiading', 'dz1', 'weekend', 'stationToCampus', '09:15'),
('jiading', 'dz1', 'weekend', 'stationToCampus', '10:15'),
('jiading', 'dz1', 'weekend', 'stationToCampus', '11:15'),
('jiading', 'dz1', 'weekend', 'stationToCampus', '12:15'),
('jiading', 'dz1', 'weekend', 'stationToCampus', '13:15'),
('jiading', 'dz1', 'weekend', 'stationToCampus', '14:15'),
('jiading', 'dz1', 'weekend', 'stationToCampus', '15:15'),
('jiading', 'dz1', 'weekend', 'stationToCampus', '16:15'),
('jiading', 'dz1', 'weekend', 'stationToCampus', '17:15'),
('jiading', 'dz1', 'weekend', 'stationToCampus', '18:15'),
('jiading', 'dz1', 'weekend', 'stationToCampus', '19:15'),
('jiading', 'dz1', 'weekend', 'stationToCampus', '20:15');

-- ============================================
-- 2. 北安跨线时刻表
-- ============================================

-- 北安跨线 工作日 校区→地铁站
INSERT INTO commute_schedule (campus, route_key, day_type, direction, departure_time) VALUES
('jiading', 'beian', 'weekday', 'campusToStation', '06:50'),
('jiading', 'beian', 'weekday', 'campusToStation', '07:10'),
('jiading', 'beian', 'weekday', 'campusToStation', '07:25'),
('jiading', 'beian', 'weekday', 'campusToStation', '07:40'),
('jiading', 'beian', 'weekday', 'campusToStation', '07:55'),
('jiading', 'beian', 'weekday', 'campusToStation', '08:10'),
('jiading', 'beian', 'weekday', 'campusToStation', '08:30'),
('jiading', 'beian', 'weekday', 'campusToStation', '09:00'),
('jiading', 'beian', 'weekday', 'campusToStation', '09:30'),
('jiading', 'beian', 'weekday', 'campusToStation', '10:00'),
('jiading', 'beian', 'weekday', 'campusToStation', '10:30'),
('jiading', 'beian', 'weekday', 'campusToStation', '11:00'),
('jiading', 'beian', 'weekday', 'campusToStation', '11:30'),
('jiading', 'beian', 'weekday', 'campusToStation', '12:00'),
('jiading', 'beian', 'weekday', 'campusToStation', '12:30'),
('jiading', 'beian', 'weekday', 'campusToStation', '13:00'),
('jiading', 'beian', 'weekday', 'campusToStation', '13:30'),
('jiading', 'beian', 'weekday', 'campusToStation', '14:00'),
('jiading', 'beian', 'weekday', 'campusToStation', '14:30'),
('jiading', 'beian', 'weekday', 'campusToStation', '15:00'),
('jiading', 'beian', 'weekday', 'campusToStation', '15:30'),
('jiading', 'beian', 'weekday', 'campusToStation', '16:00'),
('jiading', 'beian', 'weekday', 'campusToStation', '16:30'),
('jiading', 'beian', 'weekday', 'campusToStation', '17:00'),
('jiading', 'beian', 'weekday', 'campusToStation', '17:30'),
('jiading', 'beian', 'weekday', 'campusToStation', '18:00'),
('jiading', 'beian', 'weekday', 'campusToStation', '18:30'),
('jiading', 'beian', 'weekday', 'campusToStation', '19:00'),
('jiading', 'beian', 'weekday', 'campusToStation', '19:30'),
('jiading', 'beian', 'weekday', 'campusToStation', '20:00'),
('jiading', 'beian', 'weekday', 'campusToStation', '20:30'),
('jiading', 'beian', 'weekday', 'campusToStation', '21:00'),
('jiading', 'beian', 'weekday', 'campusToStation', '21:30');

-- 北安跨线 工作日 地铁站→校区
INSERT INTO commute_schedule (campus, route_key, day_type, direction, departure_time) VALUES
('jiading', 'beian', 'weekday', 'stationToCampus', '07:00'),
('jiading', 'beian', 'weekday', 'stationToCampus', '07:20'),
('jiading', 'beian', 'weekday', 'stationToCampus', '07:35'),
('jiading', 'beian', 'weekday', 'stationToCampus', '07:50'),
('jiading', 'beian', 'weekday', 'stationToCampus', '08:05'),
('jiading', 'beian', 'weekday', 'stationToCampus', '08:20'),
('jiading', 'beian', 'weekday', 'stationToCampus', '08:40'),
('jiading', 'beian', 'weekday', 'stationToCampus', '09:10'),
('jiading', 'beian', 'weekday', 'stationToCampus', '09:40'),
('jiading', 'beian', 'weekday', 'stationToCampus', '10:10'),
('jiading', 'beian', 'weekday', 'stationToCampus', '10:40'),
('jiading', 'beian', 'weekday', 'stationToCampus', '11:10'),
('jiading', 'beian', 'weekday', 'stationToCampus', '11:40'),
('jiading', 'beian', 'weekday', 'stationToCampus', '12:10'),
('jiading', 'beian', 'weekday', 'stationToCampus', '12:40'),
('jiading', 'beian', 'weekday', 'stationToCampus', '13:10'),
('jiading', 'beian', 'weekday', 'stationToCampus', '13:40'),
('jiading', 'beian', 'weekday', 'stationToCampus', '14:10'),
('jiading', 'beian', 'weekday', 'stationToCampus', '14:40'),
('jiading', 'beian', 'weekday', 'stationToCampus', '15:10'),
('jiading', 'beian', 'weekday', 'stationToCampus', '15:40'),
('jiading', 'beian', 'weekday', 'stationToCampus', '16:10'),
('jiading', 'beian', 'weekday', 'stationToCampus', '16:40'),
('jiading', 'beian', 'weekday', 'stationToCampus', '17:10'),
('jiading', 'beian', 'weekday', 'stationToCampus', '17:40'),
('jiading', 'beian', 'weekday', 'stationToCampus', '18:10'),
('jiading', 'beian', 'weekday', 'stationToCampus', '18:40'),
('jiading', 'beian', 'weekday', 'stationToCampus', '19:10'),
('jiading', 'beian', 'weekday', 'stationToCampus', '19:40'),
('jiading', 'beian', 'weekday', 'stationToCampus', '20:10'),
('jiading', 'beian', 'weekday', 'stationToCampus', '20:40'),
('jiading', 'beian', 'weekday', 'stationToCampus', '21:10'),
('jiading', 'beian', 'weekday', 'stationToCampus', '21:40');

-- 北安跨线 周末
INSERT INTO commute_schedule (campus, route_key, day_type, direction, departure_time) VALUES
('jiading', 'beian', 'weekend', 'campusToStation', '08:00'),
('jiading', 'beian', 'weekend', 'campusToStation', '09:00'),
('jiading', 'beian', 'weekend', 'campusToStation', '10:00'),
('jiading', 'beian', 'weekend', 'campusToStation', '11:00'),
('jiading', 'beian', 'weekend', 'campusToStation', '12:00'),
('jiading', 'beian', 'weekend', 'campusToStation', '13:00'),
('jiading', 'beian', 'weekend', 'campusToStation', '14:00'),
('jiading', 'beian', 'weekend', 'campusToStation', '15:00'),
('jiading', 'beian', 'weekend', 'campusToStation', '16:00'),
('jiading', 'beian', 'weekend', 'campusToStation', '17:00'),
('jiading', 'beian', 'weekend', 'campusToStation', '18:00'),
('jiading', 'beian', 'weekend', 'campusToStation', '19:00'),
('jiading', 'beian', 'weekend', 'campusToStation', '20:00'),
('jiading', 'beian', 'weekend', 'stationToCampus', '08:15'),
('jiading', 'beian', 'weekend', 'stationToCampus', '09:15'),
('jiading', 'beian', 'weekend', 'stationToCampus', '10:15'),
('jiading', 'beian', 'weekend', 'stationToCampus', '11:15'),
('jiading', 'beian', 'weekend', 'stationToCampus', '12:15'),
('jiading', 'beian', 'weekend', 'stationToCampus', '13:15'),
('jiading', 'beian', 'weekend', 'stationToCampus', '14:15'),
('jiading', 'beian', 'weekend', 'stationToCampus', '15:15'),
('jiading', 'beian', 'weekend', 'stationToCampus', '16:15'),
('jiading', 'beian', 'weekend', 'stationToCampus', '17:15'),
('jiading', 'beian', 'weekend', 'stationToCampus', '18:15'),
('jiading', 'beian', 'weekend', 'stationToCampus', '19:15'),
('jiading', 'beian', 'weekend', 'stationToCampus', '20:15');

-- ============================================
-- 3. 822路公交时刻表
-- ============================================

-- 822路 工作日 校区→地铁站
INSERT INTO commute_schedule (campus, route_key, day_type, direction, departure_time) VALUES
('jiading', 'bus822', 'weekday', 'campusToStation', '05:05'),
('jiading', 'bus822', 'weekday', 'campusToStation', '06:08'),
('jiading', 'bus822', 'weekday', 'campusToStation', '06:48'),
('jiading', 'bus822', 'weekday', 'campusToStation', '07:09'),
('jiading', 'bus822', 'weekday', 'campusToStation', '07:18'),
('jiading', 'bus822', 'weekday', 'campusToStation', '07:29'),
('jiading', 'bus822', 'weekday', 'campusToStation', '07:38'),
('jiading', 'bus822', 'weekday', 'campusToStation', '07:48'),
('jiading', 'bus822', 'weekday', 'campusToStation', '07:58'),
('jiading', 'bus822', 'weekday', 'campusToStation', '08:08'),
('jiading', 'bus822', 'weekday', 'campusToStation', '08:18'),
('jiading', 'bus822', 'weekday', 'campusToStation', '08:28'),
('jiading', 'bus822', 'weekday', 'campusToStation', '08:38'),
('jiading', 'bus822', 'weekday', 'campusToStation', '08:52'),
('jiading', 'bus822', 'weekday', 'campusToStation', '09:12'),
('jiading', 'bus822', 'weekday', 'campusToStation', '09:32'),
('jiading', 'bus822', 'weekday', 'campusToStation', '09:52'),
('jiading', 'bus822', 'weekday', 'campusToStation', '10:12'),
('jiading', 'bus822', 'weekday', 'campusToStation', '10:32'),
('jiading', 'bus822', 'weekday', 'campusToStation', '10:52'),
('jiading', 'bus822', 'weekday', 'campusToStation', '11:12'),
('jiading', 'bus822', 'weekday', 'campusToStation', '11:32'),
('jiading', 'bus822', 'weekday', 'campusToStation', '11:52'),
('jiading', 'bus822', 'weekday', 'campusToStation', '12:12'),
('jiading', 'bus822', 'weekday', 'campusToStation', '12:32'),
('jiading', 'bus822', 'weekday', 'campusToStation', '12:52'),
('jiading', 'bus822', 'weekday', 'campusToStation', '13:12'),
('jiading', 'bus822', 'weekday', 'campusToStation', '13:32'),
('jiading', 'bus822', 'weekday', 'campusToStation', '13:52'),
('jiading', 'bus822', 'weekday', 'campusToStation', '14:12'),
('jiading', 'bus822', 'weekday', 'campusToStation', '14:32'),
('jiading', 'bus822', 'weekday', 'campusToStation', '14:52'),
('jiading', 'bus822', 'weekday', 'campusToStation', '15:12'),
('jiading', 'bus822', 'weekday', 'campusToStation', '15:32'),
('jiading', 'bus822', 'weekday', 'campusToStation', '15:52'),
('jiading', 'bus822', 'weekday', 'campusToStation', '16:12'),
('jiading', 'bus822', 'weekday', 'campusToStation', '16:32'),
('jiading', 'bus822', 'weekday', 'campusToStation', '16:52'),
('jiading', 'bus822', 'weekday', 'campusToStation', '17:12'),
('jiading', 'bus822', 'weekday', 'campusToStation', '17:32'),
('jiading', 'bus822', 'weekday', 'campusToStation', '17:52'),
('jiading', 'bus822', 'weekday', 'campusToStation', '18:12'),
('jiading', 'bus822', 'weekday', 'campusToStation', '18:32'),
('jiading', 'bus822', 'weekday', 'campusToStation', '18:52'),
('jiading', 'bus822', 'weekday', 'campusToStation', '19:12'),
('jiading', 'bus822', 'weekday', 'campusToStation', '19:32'),
('jiading', 'bus822', 'weekday', 'campusToStation', '20:02'),
('jiading', 'bus822', 'weekday', 'campusToStation', '20:32'),
('jiading', 'bus822', 'weekday', 'campusToStation', '21:02'),
('jiading', 'bus822', 'weekday', 'campusToStation', '21:42'),
('jiading', 'bus822', 'weekday', 'campusToStation', '22:22');

-- 822路 工作日 地铁站→校区
INSERT INTO commute_schedule (campus, route_key, day_type, direction, departure_time) VALUES
('jiading', 'bus822', 'weekday', 'stationToCampus', '05:30'),
('jiading', 'bus822', 'weekday', 'stationToCampus', '06:30'),
('jiading', 'bus822', 'weekday', 'stationToCampus', '07:00'),
('jiading', 'bus822', 'weekday', 'stationToCampus', '07:20'),
('jiading', 'bus822', 'weekday', 'stationToCampus', '07:35'),
('jiading', 'bus822', 'weekday', 'stationToCampus', '07:50'),
('jiading', 'bus822', 'weekday', 'stationToCampus', '08:05'),
('jiading', 'bus822', 'weekday', 'stationToCampus', '08:20'),
('jiading', 'bus822', 'weekday', 'stationToCampus', '08:35'),
('jiading', 'bus822', 'weekday', 'stationToCampus', '08:50'),
('jiading', 'bus822', 'weekday', 'stationToCampus', '09:10'),
('jiading', 'bus822', 'weekday', 'stationToCampus', '09:30'),
('jiading', 'bus822', 'weekday', 'stationToCampus', '09:50'),
('jiading', 'bus822', 'weekday', 'stationToCampus', '10:10'),
('jiading', 'bus822', 'weekday', 'stationToCampus', '10:30'),
('jiading', 'bus822', 'weekday', 'stationToCampus', '10:50'),
('jiading', 'bus822', 'weekday', 'stationToCampus', '11:10'),
('jiading', 'bus822', 'weekday', 'stationToCampus', '11:30'),
('jiading', 'bus822', 'weekday', 'stationToCampus', '11:50'),
('jiading', 'bus822', 'weekday', 'stationToCampus', '12:10'),
('jiading', 'bus822', 'weekday', 'stationToCampus', '12:30'),
('jiading', 'bus822', 'weekday', 'stationToCampus', '12:50'),
('jiading', 'bus822', 'weekday', 'stationToCampus', '13:10'),
('jiading', 'bus822', 'weekday', 'stationToCampus', '13:30'),
('jiading', 'bus822', 'weekday', 'stationToCampus', '13:50'),
('jiading', 'bus822', 'weekday', 'stationToCampus', '14:10'),
('jiading', 'bus822', 'weekday', 'stationToCampus', '14:30'),
('jiading', 'bus822', 'weekday', 'stationToCampus', '14:50'),
('jiading', 'bus822', 'weekday', 'stationToCampus', '15:10'),
('jiading', 'bus822', 'weekday', 'stationToCampus', '15:30'),
('jiading', 'bus822', 'weekday', 'stationToCampus', '15:50'),
('jiading', 'bus822', 'weekday', 'stationToCampus', '16:10'),
('jiading', 'bus822', 'weekday', 'stationToCampus', '16:30'),
('jiading', 'bus822', 'weekday', 'stationToCampus', '16:50'),
('jiading', 'bus822', 'weekday', 'stationToCampus', '17:10'),
('jiading', 'bus822', 'weekday', 'stationToCampus', '17:30'),
('jiading', 'bus822', 'weekday', 'stationToCampus', '17:50'),
('jiading', 'bus822', 'weekday', 'stationToCampus', '18:10'),
('jiading', 'bus822', 'weekday', 'stationToCampus', '18:30'),
('jiading', 'bus822', 'weekday', 'stationToCampus', '18:50'),
('jiading', 'bus822', 'weekday', 'stationToCampus', '19:10'),
('jiading', 'bus822', 'weekday', 'stationToCampus', '19:40'),
('jiading', 'bus822', 'weekday', 'stationToCampus', '20:10'),
('jiading', 'bus822', 'weekday', 'stationToCampus', '20:40'),
('jiading', 'bus822', 'weekday', 'stationToCampus', '21:20'),
('jiading', 'bus822', 'weekday', 'stationToCampus', '22:00');

-- 822路 周末 校区→地铁站
INSERT INTO commute_schedule (campus, route_key, day_type, direction, departure_time) VALUES
('jiading', 'bus822', 'weekend', 'campusToStation', '06:00'),
('jiading', 'bus822', 'weekend', 'campusToStation', '07:00'),
('jiading', 'bus822', 'weekend', 'campusToStation', '08:00'),
('jiading', 'bus822', 'weekend', 'campusToStation', '09:00'),
('jiading', 'bus822', 'weekend', 'campusToStation', '10:00'),
('jiading', 'bus822', 'weekend', 'campusToStation', '11:00'),
('jiading', 'bus822', 'weekend', 'campusToStation', '12:00'),
('jiading', 'bus822', 'weekend', 'campusToStation', '13:00'),
('jiading', 'bus822', 'weekend', 'campusToStation', '14:00'),
('jiading', 'bus822', 'weekend', 'campusToStation', '15:00'),
('jiading', 'bus822', 'weekend', 'campusToStation', '16:00'),
('jiading', 'bus822', 'weekend', 'campusToStation', '17:00'),
('jiading', 'bus822', 'weekend', 'campusToStation', '18:00'),
('jiading', 'bus822', 'weekend', 'campusToStation', '19:00'),
('jiading', 'bus822', 'weekend', 'campusToStation', '20:00'),
('jiading', 'bus822', 'weekend', 'campusToStation', '21:00');

-- 822路 周末 地铁站→校区
INSERT INTO commute_schedule (campus, route_key, day_type, direction, departure_time) VALUES
('jiading', 'bus822', 'weekend', 'stationToCampus', '06:30'),
('jiading', 'bus822', 'weekend', 'stationToCampus', '07:30'),
('jiading', 'bus822', 'weekend', 'stationToCampus', '08:30'),
('jiading', 'bus822', 'weekend', 'stationToCampus', '09:30'),
('jiading', 'bus822', 'weekend', 'stationToCampus', '10:30'),
('jiading', 'bus822', 'weekend', 'stationToCampus', '11:30'),
('jiading', 'bus822', 'weekend', 'stationToCampus', '12:30'),
('jiading', 'bus822', 'weekend', 'stationToCampus', '13:30'),
('jiading', 'bus822', 'weekend', 'stationToCampus', '14:30'),
('jiading', 'bus822', 'weekend', 'stationToCampus', '15:30'),
('jiading', 'bus822', 'weekend', 'stationToCampus', '16:30'),
('jiading', 'bus822', 'weekend', 'stationToCampus', '17:30'),
('jiading', 'bus822', 'weekend', 'stationToCampus', '18:30'),
('jiading', 'bus822', 'weekend', 'stationToCampus', '19:30'),
('jiading', 'bus822', 'weekend', 'stationToCampus', '20:30'),
('jiading', 'bus822', 'weekend', 'stationToCampus', '21:30');

-- ============================================
-- 4. 教职班车时刻表
-- ============================================

-- 教职班车 工作日 校区→地铁站
INSERT INTO commute_schedule (campus, route_key, day_type, direction, departure_time) VALUES
('jiading', 'teacher', 'weekday', 'campusToStation', '07:00'),
('jiading', 'teacher', 'weekday', 'campusToStation', '07:30'),
('jiading', 'teacher', 'weekday', 'campusToStation', '08:00'),
('jiading', 'teacher', 'weekday', 'campusToStation', '12:00'),
('jiading', 'teacher', 'weekday', 'campusToStation', '17:00'),
('jiading', 'teacher', 'weekday', 'campusToStation', '17:30'),
('jiading', 'teacher', 'weekday', 'campusToStation', '18:00'),
('jiading', 'teacher', 'weekday', 'campusToStation', '21:00');

-- 教职班车 工作日 地铁站→校区
INSERT INTO commute_schedule (campus, route_key, day_type, direction, departure_time) VALUES
('jiading', 'teacher', 'weekday', 'stationToCampus', '07:20'),
('jiading', 'teacher', 'weekday', 'stationToCampus', '07:50'),
('jiading', 'teacher', 'weekday', 'stationToCampus', '08:20'),
('jiading', 'teacher', 'weekday', 'stationToCampus', '12:20'),
('jiading', 'teacher', 'weekday', 'stationToCampus', '17:20'),
('jiading', 'teacher', 'weekday', 'stationToCampus', '17:50'),
('jiading', 'teacher', 'weekday', 'stationToCampus', '18:20'),
('jiading', 'teacher', 'weekday', 'stationToCampus', '21:20');

-- 教职班车 周末（班次较少）
INSERT INTO commute_schedule (campus, route_key, day_type, direction, departure_time) VALUES
('jiading', 'teacher', 'weekend', 'campusToStation', '09:00'),
('jiading', 'teacher', 'weekend', 'campusToStation', '17:00'),
('jiading', 'teacher', 'weekend', 'stationToCampus', '09:20'),
('jiading', 'teacher', 'weekend', 'stationToCampus', '17:20');

-- ============================================
-- 5. 地铁拥挤度曲线 (11号线 & 14号线)
-- ============================================

-- 11号线 每小时拥挤度
INSERT INTO metro_congestion_profile (line_id, hour, congestion) VALUES
('11', 0, 0.15), ('11', 1, 0.10), ('11', 2, 0.08), ('11', 3, 0.08),
('11', 4, 0.10), ('11', 5, 0.20), ('11', 6, 0.45), ('11', 7, 0.85),
('11', 8, 0.95), ('11', 9, 0.70), ('11', 10, 0.50), ('11', 11, 0.45),
('11', 12, 0.50), ('11', 13, 0.48), ('11', 14, 0.45), ('11', 15, 0.50),
('11', 16, 0.60), ('11', 17, 0.88), ('11', 18, 0.92), ('11', 19, 0.75),
('11', 20, 0.55), ('11', 21, 0.40), ('11', 22, 0.30), ('11', 23, 0.20);

-- 14号线 每小时拥挤度
INSERT INTO metro_congestion_profile (line_id, hour, congestion) VALUES
('14', 0, 0.12), ('14', 1, 0.08), ('14', 2, 0.06), ('14', 3, 0.06),
('14', 4, 0.08), ('14', 5, 0.18), ('14', 6, 0.40), ('14', 7, 0.78),
('14', 8, 0.88), ('14', 9, 0.62), ('14', 10, 0.45), ('14', 11, 0.40),
('14', 12, 0.45), ('14', 13, 0.42), ('14', 14, 0.40), ('14', 15, 0.45),
('14', 16, 0.55), ('14', 17, 0.82), ('14', 18, 0.85), ('14', 19, 0.68),
('14', 20, 0.50), ('14', 21, 0.35), ('14', 22, 0.25), ('14', 23, 0.18);

-- ============================================
-- 6. 路径元数据
-- ============================================
INSERT INTO commute_route_meta (line_key, display_name, color, default_metro_minutes, walk_steps, shuttle_key, description_template) VALUES
('line11', '路径 A · 11号线安亭', '#ef4444', 38, 820, 'beian', '嘉定校区 → 北安跨线 → 11号线安亭方向 → {{destination}}'),
('line14', '路径 B · 14号线封浜', '#22c55e', 30, 420, 'bus822', '嘉定校区 → 822/DZ1 → 封浜 → 14号线 → {{destination}}');

-- ============================================
-- 7. 终点站-线路时间对照
-- ============================================
INSERT INTO destination_travel_time (station_name, line_key, travel_minutes) VALUES
('真如', 'line11', 38),
('真如', 'line14', 30),
('江苏路', 'line11', 42),
('江苏路', 'line14', 34),
('徐家汇', 'line11', 48),
('徐家汇', 'line14', 40),
('陆家嘴', 'line11', 60),
('陆家嘴', 'line14', 48),
('人民广场', 'line11', 52),
('人民广场', 'line14', 42),
('静安寺', 'line11', 45),
('静安寺', 'line14', 36),
('封浜', 'line11', 50),
('封浜', 'line14', 8),
('嘉定新城', 'line11', 15),
('嘉定新城', 'line14', 25),
('南翔', 'line11', 20),
('南翔', 'line14', 18),
('曹杨路', 'line11', 32),
('曹杨路', 'line14', 25),
('中山公园', 'line11', 40),
('中山公园', 'line14', 32),
('虹桥火车站', 'line11', 28),
('虹桥火车站', 'line14', 35);

-- ============================================
-- 8. 地铁线路
-- ============================================
INSERT INTO metro_line (line_id, line_name) VALUES
('11', '11号线'),
('14', '14号线');

-- ============================================
-- 9. 地铁站点
-- ============================================
INSERT INTO metro_station (id, name) VALUES
(1101, '安亭'),
(1102, '上海汽车城'),
(1103, '昌吉东路'),
(1104, '上海赛车场'),
(1105, '嘉定新城'),
(1106, '马陆'),
(1107, '南翔'),
(1108, '桃浦新村'),
(1109, '武威路'),
(1110, '祁连山路'),
(1111, '李子园'),
(1112, '上海西站'),
(1113, '真如'),
(1114, '枫桥路'),
(1115, '曹杨路'),
(1116, '隆德路'),
(1117, '江苏路'),
(1118, '交通大学'),
(1119, '徐家汇'),
(1401, '封浜'),
(1402, '乐秀路'),
(1403, '临洮路'),
(1404, '嘉怡路'),
(1405, '真新新村'),
(1406, '真如'),
(1407, '铜川路'),
(1408, '中宁路'),
(1409, '曹杨路'),
(1410, '武宁路'),
(1411, '武定路'),
(1412, '静安寺'),
(1413, '南京西路'),
(1414, '黄陂南路'),
(1415, '陆家嘴');

-- ============================================
-- 10. 线路-站点关联
-- ============================================

-- 11号线站点
INSERT INTO metro_line_station (line_id, station_id, seq) VALUES
('11', 1101, 1), ('11', 1102, 2), ('11', 1103, 3), ('11', 1104, 4),
('11', 1105, 5), ('11', 1106, 6), ('11', 1107, 7), ('11', 1108, 8),
('11', 1109, 9), ('11', 1110, 10), ('11', 1111, 11), ('11', 1112, 12),
('11', 1113, 13), ('11', 1114, 14), ('11', 1115, 15), ('11', 1116, 16),
('11', 1117, 17), ('11', 1118, 18), ('11', 1119, 19);

-- 14号线站点
INSERT INTO metro_line_station (line_id, station_id, seq) VALUES
('14', 1401, 1), ('14', 1402, 2), ('14', 1403, 3), ('14', 1404, 4),
('14', 1405, 5), ('14', 1406, 6), ('14', 1407, 7), ('14', 1408, 8),
('14', 1409, 9), ('14', 1410, 10), ('14', 1411, 11), ('14', 1412, 12),
('14', 1413, 13), ('14', 1414, 14), ('14', 1415, 15);

-- 提交确认
SELECT '所有初始数据插入完成！' AS status;
SELECT COUNT(*) AS schedule_count FROM commute_schedule;
SELECT COUNT(*) AS congestion_count FROM metro_congestion_profile;
SELECT COUNT(*) AS route_meta_count FROM commute_route_meta;
SELECT COUNT(*) AS destination_count FROM destination_travel_time;
SELECT COUNT(*) AS line_count FROM metro_line;
SELECT COUNT(*) AS station_count FROM metro_station;

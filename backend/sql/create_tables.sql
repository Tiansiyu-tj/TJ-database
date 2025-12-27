-- ============================================
-- 嘉定出行后端数据库建表脚本
-- 数据库名: jiading_commute
-- ============================================

-- 设置客户端字符集为 UTF-8
SET NAMES utf8mb4;
SET CHARACTER SET utf8mb4;
SET character_set_connection=utf8mb4;

-- 创建数据库（如果不存在）
CREATE DATABASE IF NOT EXISTS jiading_commute 
DEFAULT CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;

USE jiading_commute;

-- ============================================
-- 1. 校区出行时刻表（短驳/公交/教职班车）
-- ============================================
DROP TABLE IF EXISTS commute_schedule;
CREATE TABLE commute_schedule (
    id INT AUTO_INCREMENT PRIMARY KEY,
    campus VARCHAR(50) NOT NULL COMMENT '校区，如 jiading',
    route_key VARCHAR(50) NOT NULL COMMENT '路线标识：dz1/beian/bus822/teacher',
    day_type ENUM('weekday', 'weekend') NOT NULL COMMENT '工作日/周末',
    direction VARCHAR(50) NOT NULL COMMENT '方向：campusToStation/stationToCampus',
    departure_time TIME NOT NULL COMMENT '发车时间',
    INDEX idx_schedule_query (campus, route_key, day_type, direction)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='校区出行时刻表';

-- ============================================
-- 2. 地铁拥挤度曲线
-- ============================================
DROP TABLE IF EXISTS metro_congestion_profile;
CREATE TABLE metro_congestion_profile (
    id INT AUTO_INCREMENT PRIMARY KEY,
    line_id VARCHAR(10) NOT NULL COMMENT '线路号，如 11/14',
    hour INT NOT NULL COMMENT '小时(0-23)',
    congestion DECIMAL(3,2) NOT NULL COMMENT '拥挤度(0-1)',
    INDEX idx_line_hour (line_id, hour),
    UNIQUE KEY uk_line_hour (line_id, hour)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='地铁拥挤度曲线';

-- ============================================
-- 3. 路径元数据
-- ============================================
DROP TABLE IF EXISTS commute_route_meta;
CREATE TABLE commute_route_meta (
    line_key VARCHAR(20) PRIMARY KEY COMMENT '如 line11/line14',
    display_name VARCHAR(100) NOT NULL COMMENT '显示名称',
    color VARCHAR(10) NOT NULL COMMENT '颜色代码',
    default_metro_minutes INT NOT NULL COMMENT '默认地铁时间(分钟)',
    walk_steps INT NOT NULL COMMENT '步行步数',
    shuttle_key VARCHAR(50) COMMENT '接驳方式',
    description_template TEXT COMMENT '描述模板'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='路径元数据';

-- ============================================
-- 4. 终点站-线路时间对照
-- ============================================
DROP TABLE IF EXISTS destination_travel_time;
CREATE TABLE destination_travel_time (
    id INT AUTO_INCREMENT PRIMARY KEY,
    station_name VARCHAR(50) NOT NULL COMMENT '终点站名',
    line_key VARCHAR(20) NOT NULL COMMENT '线路如 line11/line14',
    travel_minutes INT NOT NULL COMMENT '行程时间(分钟)',
    UNIQUE KEY uk_station_line (station_name, line_key)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='终点站地铁时间';

-- ============================================
-- 5. 地铁线路
-- ============================================
DROP TABLE IF EXISTS metro_line_station;
DROP TABLE IF EXISTS metro_line;
CREATE TABLE metro_line (
    line_id VARCHAR(10) PRIMARY KEY COMMENT '线路编号',
    line_name VARCHAR(50) NOT NULL COMMENT '线路名称'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='地铁线路';

-- ============================================
-- 6. 地铁站点
-- ============================================
DROP TABLE IF EXISTS metro_station;
CREATE TABLE metro_station (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL COMMENT '站点名称'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='地铁站点';

-- ============================================
-- 7. 线路-站点关联表
-- ============================================
CREATE TABLE metro_line_station (
    line_id VARCHAR(10) NOT NULL,
    station_id INT NOT NULL,
    seq INT COMMENT '站点顺序',
    PRIMARY KEY (line_id, station_id),
    FOREIGN KEY (line_id) REFERENCES metro_line(line_id) ON DELETE CASCADE,
    FOREIGN KEY (station_id) REFERENCES metro_station(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='线路站点关联';

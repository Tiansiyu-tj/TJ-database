-- ============================================
-- CRUD 功能新增表
-- ============================================

-- 设置客户端字符集为 UTF-8
SET NAMES utf8mb4;
SET CHARACTER SET utf8mb4;
SET character_set_connection=utf8mb4;

USE jiading_commute;

-- 1. 用户收藏表
DROP TABLE IF EXISTS user_favorite;
CREATE TABLE user_favorite (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id VARCHAR(50) DEFAULT 'default' COMMENT '用户ID，默认为default',
    station_name VARCHAR(50) NOT NULL COMMENT '收藏的站点名',
    line_key VARCHAR(20) COMMENT '线路标识',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY uk_user_station (user_id, station_name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户收藏';

-- 2. 拥挤度反馈表
DROP TABLE IF EXISTS congestion_feedback;
CREATE TABLE congestion_feedback (
    id INT AUTO_INCREMENT PRIMARY KEY,
    line_id VARCHAR(10) NOT NULL COMMENT '线路号',
    hour INT NOT NULL COMMENT '小时(0-23)',
    reported_level ENUM('empty', 'normal', 'crowded', 'packed') NOT NULL COMMENT '拥挤等级',
    user_id VARCHAR(50) DEFAULT 'anonymous' COMMENT '用户ID',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_line_hour (line_id, hour)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='拥挤度反馈';

-- 插入一些示例收藏数据
INSERT INTO user_favorite (user_id, station_name, line_key) VALUES
('default', '真如', 'line11'),
('default', '徐家汇', 'line11');

SELECT '新表创建完成！' AS status;

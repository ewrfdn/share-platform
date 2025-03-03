-- 设置连接和客户端字符集
SET NAMES utf8mb4;
SET CHARACTER SET utf8mb4;
SET character_set_client = utf8mb4;
SET character_set_connection = utf8mb4;
SET character_set_results = utf8mb4;
SET collation_connection = utf8mb4_unicode_ci;

-- 创建数据表
CREATE TABLE IF NOT EXISTS roles (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    display_name VARCHAR(255) NOT NULL,
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL
)CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    role_id INTEGER NOT NULL,
    avatar VARCHAR(255),
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL
)CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS categories (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    display_name VARCHAR(255) NOT NULL,
    parent_id INTEGER,
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL
)CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS blobs (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    file_name VARCHAR(255) NOT NULL,
    file_path VARCHAR(255) NOT NULL,
    mime_type VARCHAR(255) NOT NULL,
    file_size BIGINT NOT NULL,
    sha256 VARCHAR(64) NOT NULL,
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL
)CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS materials (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    display_name VARCHAR(255) NOT NULL,
    category_ids VARCHAR(255) NOT NULL,
    blob_id INTEGER NOT NULL,
    description TEXT,
    cover VARCHAR(255),
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL,
    FOREIGN KEY (blob_id) REFERENCES blobs(id) 
)CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS comments (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    material_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    content TEXT NOT NULL,
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL,
    FOREIGN KEY (material_id) REFERENCES materials(id),
    FOREIGN KEY (user_id) REFERENCES users(id)
)CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- 插入角色数据
INSERT INTO roles (id, display_name, created_at, updated_at) VALUES
(1, '管理员', NOW(), NOW()),
(2, '老师', NOW(), NOW()),
(3, '学生', NOW(), NOW());

-- 插入管理员用户 (密码为 'admin123')
INSERT INTO users (username, password, role_id, created_at, updated_at) VALUES
('admin', 'pbkdf2:sha256:260000$V1wE5O9NLHtSzAQT$7ba850e237c212bc489a15c3d416ebd3aa7901b4e62c4814c275a19f8315fb62', 1, NOW(), NOW());

-- 插入示例分类数据
INSERT INTO categories (display_name, parent_id, created_at, updated_at) VALUES
('教学资料', NULL, NOW(), NOW()),
('课件', 1, NOW(), NOW()),
('教案', 1, NOW(), NOW()),
('试卷', 1, NOW(), NOW()),
('教学视频', NULL, NOW(), NOW());

-- 添加索引
ALTER TABLE users ADD INDEX idx_username (username);
ALTER TABLE materials ADD INDEX idx_blob_id (blob_id);
ALTER TABLE comments ADD INDEX idx_material_id (material_id);
ALTER TABLE comments ADD INDEX idx_user_id (user_id);
ALTER TABLE categories ADD INDEX idx_parent_id (parent_id);
-- 插入角色数据
INSERT INTO roles (id, display_name, created_at, updated_at) VALUES
(1, '管理员', NOW(), NOW()),
(2, '老师', NOW(), NOW()),
(3, '学生', NOW(), NOW());

-- 插入管理员用户 (密码为 'admin123')
INSERT INTO users (username, password, role_id, created_at, updated_at) VALUES
('admin', 'pbkdf2:sha256:260000$YOUR_SALT$YOUR_HASH', 1, NOW(), NOW()); 
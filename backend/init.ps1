# 创建目录用于存放初始化脚本
New-Item -ItemType Directory -Force -Path ".\mysql\init"

# 复制初始化脚本到指定目录
Copy-Item ".\backend\scripts\init_data.sql" -Destination ".\mysql\init"

# 运行 MySQL Docker 容器
docker run --name teaching-material-mysql `
    -p 3306:3306 `
    -e MYSQL_ROOT_PASSWORD=password `
    -e MYSQL_DATABASE=teaching_material `
    -e MYSQL_CHARSET=utf8mb4 `
    -e MYSQL_COLLATION=utf8mb4_unicode_ci `
    -v ${PWD}/mysql/init:/docker-entrypoint-initdb.d `
    -d mysql:8.0 `
    --character-set-server=utf8mb4 `
    --collation-server=utf8mb4_unicode_ci
# 检查是否在虚拟环境中，如果不在则激活
if (-not ($env:VIRTUAL_ENV)) {
    Write-Host "正在激活虚拟环境..." -ForegroundColor Green
    .\venv\Scripts\Activate.ps1
}

# 设置 Flask 环境变量
Write-Host "正在设置 Flask 环境变量..." -ForegroundColor Green
$env:FLASK_APP = "backend/app"
$env:FLASK_ENV = "development"
$env:FLASK_DEBUG = 1

# 创建上传目录
$uploadDir = "backend/uploads"
if (-not (Test-Path $uploadDir)) {
    Write-Host "创建上传目录..." -ForegroundColor Green
    New-Item -ItemType Directory -Force -Path $uploadDir
}

# 启动应用
Write-Host "正在启动 Flask 应用..." -ForegroundColor Green
Write-Host "应用将运行在 http://localhost:5000" -ForegroundColor Yellow
Write-Host "CORS 已配置允许来自以下源的请求：" -ForegroundColor Yellow
Write-Host "- http://localhost:3000" -ForegroundColor Yellow
Write-Host "- http://localhost:5173" -ForegroundColor Yellow

flask run --host=0.0.0.0 --port=5000 
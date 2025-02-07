# 设置执行策略（如果需要）
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process

# 创建虚拟环境目录
Write-Host "正在创建虚拟环境..." -ForegroundColor Green
python -m venv share_material_venv

# 激活虚拟环境
Write-Host "正在激活虚拟环境..." -ForegroundColor Green
.\share_material_venv\Scripts\Activate.ps1

# 升级 pip
Write-Host "正在升级 pip..." -ForegroundColor Green
python -m pip install --upgrade pip

# 安装依赖
Write-Host "正在安装项目依赖..." -ForegroundColor Green
pip install -r backend/requirements.txt

# 显示已安装的包
Write-Host "已安装的包列表：" -ForegroundColor Green
pip list

Write-Host "虚拟环境设置完成！" -ForegroundColor Green
Write-Host "使用 'deactivate' 命令可以退出虚拟环境" -ForegroundColor Yellow
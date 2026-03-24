# TheNEWs 安装脚本

此目录包含 TheNEWs 项目的快速安装和运行脚本。

## 脚本说明

| 脚本 | 平台 | 说明 |
|------|------|------|
| `install.sh` | Linux/Mac | 安装项目到 ~/TheNEWs |
| `run.sh` | Linux/Mac | 运行 TheNEWs |
| `install.bat` | Windows | 安装项目到 %USERPROFILE%\TheNEWs |
| `run.bat` | Windows | 运行 TheNEWs |
| `quick-install.sh` | Linux/Mac | 一键安装并运行 |

## 使用方法

### Linux/Mac

```bash
# 方式 1: 一键安装并运行
bash <(curl -s https://raw.githubusercontent.com/fezeryang/TheNEWs/master/scripts/quick-install.sh)

# 方式 2: 分步安装
curl -O https://raw.githubusercontent.com/fezeryang/TheNEWs/master/scripts/install.sh
chmod +x install.sh
./install.sh

# 方式 3: 克隆后使用本地脚本
git clone https://github.com/fezeryang/TheNEWs.git ~/TheNEWs
cd ~/TheNEWs
chmod +x scripts/*.sh
./scripts/install.sh
```

### Windows

```powershell
# 方式 1: PowerShell 一键安装
irm https://raw.githubusercontent.com/fezeryang/TheNEWs/master/scripts/quick-install.ps1 | iex

# 方式 2: 下载后运行
# 下载 install.bat 到本地，双击运行
```

## 环境要求

- Python 3.8+
- Git
- pip

## API Key

运行前需要设置 AI API Key：

```bash
# Linux/Mac
export AI_API_KEY="sk-xxxxxxxxxxxxx"

# Windows
set AI_API_KEY=sk-xxxxxxxxxxxxx
```

推荐使用 DeepSeek：https://platform.deepseek.com/api_keys

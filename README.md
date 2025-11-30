# Markdown 转 DOCX 文档生成器

一个基于 Flask + React 的现代化文档转换系统，支持将 Markdown 文件转换为 Word 文档（DOCX），并提供模板自定义功能。

## ✨ 功能特性

### 🔒 安全性
- ✅ **路径遍历保护** - 防止恶意文件路径攻击
- ✅ **文件类型验证** - 严格的文件格式和内容检查
- ✅ **文件大小限制** - 防止大文件攻击
- ✅ **二进制文件检测** - 防止上传非文本文件

### 🚀 核心功能
- 📝 **Markdown 转 DOCX** - 基于 Pandoc 的高质量转换
- 🎨 **模板支持** - 使用自定义 DOCX 模板美化输出
- 📱 **响应式设计** - 完美适配桌面和移动设备
- 🖱️ **拖拽上传** - 直观的文件上传体验

### 🛠️ 用户体验
- ⚡ **实时预览** - 上传后立即预览 Markdown 内容
- 📊 **状态反馈** - 详细的转换状态和错误提示
- 🌓 **深色模式** - 自动适配系统主题偏好
- 💾 **自动下载** - 转换完成后自动下载文档

## 📋 系统要求

### 基础依赖
- **Python 3.8+**
- **Node.js 16+**
- **Pandoc** - 核心转换引擎

### 安装 Pandoc

#### Windows
```bash
# 使用 winget
winget install JohnMacFarlane.Pandoc

# 或使用 chocolatey
choco install pandoc

# 或从官网下载安装包
# https://pandoc.org/installing.html
```

#### macOS
```bash
# 使用 Homebrew
brew install pandoc

# 使用 MacPorts
sudo port install pandoc
```

#### Linux
```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install pandoc

# CentOS/RHEL
sudo yum install pandoc

# Arch Linux
sudo pacman -S pandoc
```

## 🚀 快速开始

### 1. 克隆项目
```bash
git clone <repository-url>
cd DocGenerator
```

### 2. 后端设置 (Flask)

```bash
cd backend

# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 启动后端服务
python app.py
```

后端将在 `http://localhost:5000` 启动

### 3. 前端设置 (React)

```bash
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

前端将在 `http://localhost:5173` 启动

### 4. 验证安装
访问 `http://localhost:5173`，如果看到界面显示 "📝 Markdown 转 DOCX 工具"，说明安装成功。

## 📖 使用指南

### 基本使用

1. **上传文件**
   - 拖拽 Markdown 文件到上传区域
   - 或点击上传区域选择文件

2. **选择模板** (可选)
   - 从下拉菜单选择 DOCX 模板
   - 如不选择，将使用默认样式

3. **生成文档**
   - 点击 "⚡ 生成 DOCX" 按钮
   - 等待转换完成
   - 浏览器将自动下载生成的文档

### 模板管理

#### 添加自定义模板
1. 创建或准备一个 DOCX 文件作为模板
2. 将模板文件放入 `backend/templates_store/` 目录
3. 重启后端服务
4. 模板将自动出现在前端的模板选择列表中

#### 模板要求
- 格式：`.docx` 文件
- 文件名：只能包含字母、数字、点、下划线和连字符
- 位置：`backend/templates_store/` 目录

## 🔧 配置选项

### 环境变量

#### 后端配置
```bash
# 上传文件存储目录
UPLOAD_FOLDER=custom_upload_dir

# 模板文件目录
TEMPLATE_FOLDER=custom_template_dir

# 最大文件上传大小 (Flask 默认 16MB)
MAX_CONTENT_LENGTH=16777216  # 16MB
```

#### 前端配置
在 `frontend/src/App.jsx` 中修改：
```javascript
const API_BASE = "http://localhost:5000";  // 后端地址
```

## 🛠️ 开发指南

### 项目结构
```
DocGenerator/
├── backend/                # Flask 后端
│   ├── app.py             # 主应用文件
│   ├── requirements.txt   # Python 依赖
│   └── templates_store/   # DOCX 模板目录
├── frontend/              # React 前端
│   ├── src/
│   │   ├── App.jsx       # 主组件
│   │   ├── App.css       # 样式文件
│   │   └── main.jsx      # 入口文件
│   ├── package.json      # Node.js 依赖
│   └── vite.config.js    # Vite 配置
└── README.md             # 项目文档
```

### API 接口

#### 健康检查
```http
GET /api/health
```
响应：
```json
{
  "status": "ok",
  "pandoc_available": true
}
```

#### 获取模板列表
```http
GET /api/templates
```
响应：
```json
[
  {
    "name": "template1.docx",
    "path": "/path/to/template1.docx"
  }
]
```

#### 文档转换
```http
POST /api/convert
Content-Type: multipart/form-data

file: [Markdown 文件]
template: [可选，模板名称]
```

成功响应：
```
Content-Type: application/vnd.openxmlformats-officedocument.wordprocessingml.document
Content-Disposition: attachment; filename="document.docx"
[二进制 DOCX 文件]
```

错误响应：
```json
{
  "error": "错误描述",
  "details": "详细错误信息"
}
```

### 错误处理

#### 常见错误及解决方案

1. **Pandoc 不可用**
   - 错误：`Pandoc not found. Please install pandoc...`
   - 解决：安装 Pandoc 并确保其在 PATH 中

2. **文件类型错误**
   - 错误：`Only Markdown files (.md, .markdown) are allowed`
   - 解决：上传有效的 Markdown 文件

3. **文件过大**
   - 错误：`File size cannot exceed 10MB`
   - 解决：减小文件大小或调整限制

4. **模板不存在**
   - 错误：`Invalid template name`
   - 解决：确保模板文件存在于 templates_store 目录

## 🚀 部署指南

### 生产环境部署

#### 1. 使用 Docker
```dockerfile
# Dockerfile 示例
FROM python:3.9-slim

# 安装 Pandoc
RUN apt-get update && apt-get install -y pandoc

# 设置工作目录
WORKDIR /app

# 复制后端文件
COPY backend/requirements.txt .
RUN pip install -r requirements.txt

COPY backend/ .

# 暴露端口
EXPOSE 5000

CMD ["python", "app.py"]
```

#### 2. 使用 Nginx + uWSGI
```nginx
# /etc/nginx/sites-available/docgenerator
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

#### 3. 环境变量配置
```bash
# 生产环境
export FLASK_ENV=production
export UPLOAD_FOLDER=/var/uploads/docgen
export TEMPLATE_FOLDER=/var/templates/docgen
```

### 性能优化

#### 后端优化
- 使用 Redis 缓存转换结果
- 实现异步转换队列
- 配置负载均衡

#### 前端优化
- 代码分割和懒加载
- 图片优化和CDN
- 启用Gzip压缩

## 🐛 故障排除

### 常见问题

#### Q: 转换失败，提示 "Pandoc not found"
A: 检查 Pandoc 是否正确安装并在 PATH 中。运行 `pandoc --version` 验证。

#### Q: 文件上传后没有反应
A: 检查浏览器控制台是否有错误信息，确保后端服务正在运行。

#### Q: 模板选择列表为空
A: 确保 `templates_store` 目录存在且包含 `.docx` 文件。

#### Q: 下载的文件损坏
A: 检查服务器日志，可能是转换过程中出现错误。

### 日志查看
```bash
# 查看后端日志
tail -f /var/log/docgenerator/app.log

# 查看 Nginx 日志
tail -f /var/log/nginx/error.log
```

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request！

### 开发流程
1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

### 代码规范
- 遵循 PEP 8 (Python)
- 使用 ESLint (JavaScript)
- 编写单元测试
- 更新文档

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 🙏 致谢

- [Pandoc](https://pandoc.org/) - 强大的文档转换工具
- [Flask](https://flask.palletsprojects.com/) - 轻量级 Python Web 框架
- [React](https://reactjs.org/) - 用户界面构建库
- [Vite](https://vitejs.dev/) - 现代前端构建工具

## 📞 支持

如果您遇到问题或有建议，请：
- 创建 [GitHub Issue](https://github.com/your-repo/DocGenerator/issues)
- 发送邮件至 support@example.com

---

**⭐ 如果这个项目对您有帮助，请给我们一个 Star！**
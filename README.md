# 项目文件结构
.
├── app.py                      # Flask后端应用入口
├── uploads/                    # 临时存储上传文件的目录
├── outputs/                    # 存储转换后CSV文件的目录
└── templates/                  # HTML模板目录
    └── index.html              # 前端界面HTML

# 创建所需目录的命令
mkdir -p uploads outputs templates

# 安装所需依赖
pip install Flask werkzeug

# 运行应用
python app.py

```

现在我来说明一下这个基于Flask的TXT转CSV转换器的使用方法：

### 设置和运行
1. 首先创建项目目录结构：
```bash
mkdir -p txt_to_csv_flask/templates
mkdir -p txt_to_csv_flask/uploads
mkdir -p txt_to_csv_flask/outputs
cd txt_to_csv_flask
```

2. 将我提供的代码分别保存到相应文件中：
   - 后端代码保存为 `app.py`
   - 前端HTML模板保存为 `templates/index.html`

3. 安装依赖：
```bash
pip install Flask werkzeug
```

4. 启动应用：
```bash
python app.py
```

5. 应用将在 `http://0.0.0.0:5000` 运行，可以通过服务器IP地址访问

### 功能特点

1. **前后端分离设计**：
   - 前端使用HTML, CSS (Bootstrap), JavaScript实现用户界面
   - 后端使用Flask提供RESTful API

2. **用户界面功能**：
   - 文件上传界面
   - 分隔符选择（逗号、制表符、空格、自定义）
   - 转换进度显示
   - 结果下载功能
   - 错误提示

3. **API端点**：
   - `/api/convert` - 上传并转换文件
   - `/api/download/<filename>` - 下载转换后的CSV文件

4. **安全特性**：
   - 文件名安全处理
   - 文件大小限制
   - 临时文件管理

### 使用流程

1. 通过浏览器访问应用（例如 `http://服务器IP:5000`）
2. 在界面上选择要转换的TXT文件
3. 选择适当的分隔符（默认为逗号）
4. 点击"开始转换"按钮
5. 等待转换完成
6. 转换成功后，点击"下载CSV文件"获取结果

这个应用可以在没有图形界面的服务器上运行，用户通过网页浏览器与应用交互，完全避开了之前的显示错误问题。

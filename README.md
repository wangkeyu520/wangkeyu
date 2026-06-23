# Sunny Tea House AI评价生成器

一款基于AI的奶茶店评价生成工具，帮助顾客快速生成符合特定社交平台风格的评价内容。

## 功能特性

- ✅ 感受标签选择（服务好、出餐快、环境干净等）
- ✅ 多平台支持（Google英文评价、小红书种草风格）
- ✅ AI智能生成评价内容
- ✅ 一键复制评价内容
- ✅ 发布引导流程
- ✅ 精美的移动端H5界面
- ✅ Element Plus 组件库

## 技术栈

| 层级 | 技术 | 版本 |
|------|------|------|
| 前端 | Vue 3 | ^3.5.34 |
| UI组件库 | Element Plus | ^2.8.8 |
| 图标库 | @element-plus/icons-vue | ^2.3.1 |
| 构建工具 | Vite | ^8.0.12 |
| HTTP请求 | Axios | ^1.7.7 |
| 后端 | FastAPI | ^0.137.2 |
| HTTP客户端 | Requests | ^2.32.3 |
| 大模型 | 阿里云百炼 | qwen-plus |

## 项目结构

```
sunny-tea-review/
├── frontend/                # 前端项目
│   ├── src/
│   │   ├── components/      # Vue组件
│   │   │   ├── HomePage.vue      # 首页
│   │   │   ├── SelectPage.vue    # 选择页（感受+平台）
│   │   │   ├── GeneratePage.vue  # 生成页（加载状态）
│   │   │   └── PreviewPage.vue   # 预览页（评价展示）
│   │   ├── App.vue          # 主应用组件
│   │   ├── main.js          # 入口文件
│   │   └── style.css        # 全局样式
│   ├── index.html           # HTML模板
│   ├── vite.config.js       # Vite配置
│   ├── tailwind.config.js   # TailwindCSS配置
│   ├── postcss.config.js    # PostCSS配置
│   └── package.json         # 前端依赖
├── backend/                 # 后端项目
│   ├── main.py              # FastAPI主文件
│   └── requirements.txt     # Python依赖
├── start.bat                # 一键启动脚本（Windows）
└── README.md                # 项目说明
```

## 快速开始

### 方法一：一键启动（Windows）

双击运行 `start.bat` 脚本，自动完成环境配置和服务启动。

### 方法二：手动启动

#### 1. 安装后端依赖

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

#### 2. 安装前端依赖

```bash
cd frontend
npm install
```

#### 3. 启动后端服务

```bash
cd backend
python main.py
```

#### 4. 启动前端服务

```bash
cd frontend
npm run dev
```

#### 5. 访问应用

打开浏览器访问：http://localhost:5173

## API接口

### POST /api/generate-review

生成评价内容

**请求体**：
```json
{
  "feeling_tags": ["服务好", "饮品颜值高"],
  "platform": "xiaohongshu",
  "store_info": {
    "name": "Sunny Tea House",
    "location": "San Jose",
    "rating": 4.8
  }
}
```

**响应**：
```json
{
  "success": true,
  "review": {
    "content": "姐妹们！Sunny Tea House真的绝了🥤...",
    "platform": "xiaohongshu",
    "tags": ["服务好", "饮品颜值高"],
    "store_name": "Sunny Tea House",
    "location": "San Jose"
  }
}
```

### GET /api/health

健康检查

**响应**：
```json
{
  "status": "ok",
  "message": "服务正常运行"
}
```

## 用户流程

```
首页 → 感受选择 → 平台选择 → AI生成 → 评价预览 → 发布引导
```

## Element Plus 组件使用

| 组件 | 用途 | 页面 |
|------|------|------|
| el-avatar | 头像展示 | 首页、生成页 |
| el-badge | 徽章标记 | 首页、生成页 |
| el-card | 卡片容器 | 所有页面 |
| el-statistic | 数据统计 | 首页 |
| el-steps | 步骤条 | 首页、选择页 |
| el-checkbox-group | 多选组 | 选择页 |
| el-checkbox-button | 多选按钮 | 选择页 |
| el-radio-group | 单选组 | 选择页 |
| el-radio | 单选按钮 | 选择页 |
| el-progress | 进度条 | 生成页 |
| el-descriptions | 描述列表 | 生成页 |
| el-input | 输入框 | 预览页 |
| el-timeline | 时间轴 | 预览页 |
| el-dialog | 对话框 | 预览页 |
| el-result | 结果页 | 预览页 |
| el-message | 消息提示 | 全局 |
| el-button | 按钮 | 所有页面 |

## 注意事项

1. 需要有效的阿里云百炼API Key（已在代码中配置）
2. 确保网络连接正常，能访问阿里云API
3. 前端已配置代理，开发环境自动转发/api请求到后端
4. Element Plus 已配置中文语言包

## License

MIT License
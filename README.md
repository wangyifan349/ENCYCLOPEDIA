# ENCYCLOPEDIA 📝

> 一个基于 Flask后端 和本地 Markdown 文件存储的简易百科网站，支持词条创建、编辑、查看和基于最长公共子序列（LCS）算法的智能模糊搜索，页面使用 Bootstrap 5 美化，响应式设计，轻量且便于本地部署。

---

## ✨ 项目亮点

- 📁 **纯文件存储**  
  所有词条内容均以 Markdown 格式保存在本地 `entries` 文件夹，无需数据库，便于管理和备份。

- 🔍 **智能搜索**  
  使用最长公共子序列算法（LCS）计算关键词与词条名匹配度，实现模糊搜索返最相关词条列表。

- ⚙️ **全功能支持**  
  词条查看、创建、编辑、搜索，操作流畅，界面美观。

- 🎨 **Bootstrap 美化**  
  采用 Bootstrap 5 响应式框架，界面简洁现代，支持移动与桌面端。

- 🚀 **轻松部署**  
  Python + Flask，依赖少，快速搭建。

---

## 🚀 安装与运行

确保你已安装 Python 3.7+ 和 pip。

```bash
# 克隆项目
git clone https://github.com/wangyifan349/ENCYCLOPEDIA.git
cd ENCYCLOPEDIA

# 安装依赖
pip install -r requirements.txt

# 启动服务
python app.py

# 浏览器访问 http://127.0.0.1:5000
```

---

## 📦 依赖

- Flask==2.x
- Markdown==3.x

> 使用 `pip install -r requirements.txt` 一键安装。

---

## 📂 项目结构

```
ENCYCLOPEDIA/
├── app.py              # Flask 主程序，业务逻辑
├── entries/            # Markdown 词条文件夹，存放所有词条.md
├── templates/          # Jinja2 HTML 模板（Bootstrap 美化）
│   ├── layout.html
│   ├── index.html
│   ├── entry.html
│   ├── create.html
│   ├── edit.html
│   └── search.html
├── static/             # （可选）静态资源如 CSS、JS、图片等
├── requirements.txt    # 项目依赖列表
└── README.md           # 项目说明文档
```

---

## 📖 使用说明

- 主页浏览所有词条，点击词条名查看 Markdown 内容。
- 顶部搜索框输入关键词，得到匹配度最高的相关词条。
- 无匹配结果时，可快速创建新词条。
- 创建词条按钮快速新增内容。
- 词条详情页提供编辑入口，方便维护。

---

## 💡 开发建议

- 内容支持 Markdown 格式，可用各式在线编辑器撰写。
- 后续可增加认证、权限管理、数据库支持。
- LCS 搜索适合规模中小型项目，大数据可用全文搜索引擎替代。

---

## 📜 许可证

本项目基于 [GNU GPL v3](https://www.gnu.org/licenses/gpl-3.0.html) 许可证开源。

---

## 📫 联系方式

- GitHub: [wangyifan349](https://github.com/wangyifan349)  
- 邮箱: wangyifan1999@protonmail.com

---

感谢你的支持与使用！🎉  
期待 ENCYCLOPEDIA 成为你专属的轻量级百科伴侣。


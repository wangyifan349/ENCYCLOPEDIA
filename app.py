import os
from flask import Flask, render_template, request, redirect, url_for, flash
import markdown

# ------------------------------------------
# 应用初始化和配置
# ------------------------------------------
app = Flask(__name__)
app.secret_key = "请替换成你自己的密钥"  # 用于flash消息，生产时请用更安全值

ENTRY_DIR = "entries"  # 本地存储词条 Markdown 文件夹

if not os.path.exists(ENTRY_DIR):
    os.makedirs(ENTRY_DIR)

# ------------------------------------------
# 工具函数：列出所有词条
# ------------------------------------------
def list_entries():
    """
    返回已存在所有词条名称列表（无.md后缀），按字母序排序，不区分大小写
    """
    files = os.listdir(ENTRY_DIR)
    entries = [f[:-3] for f in files if f.endswith(".md")]
    return sorted(entries, key=str.lower)

# ------------------------------------------
# 工具函数：读取词条内容
# ------------------------------------------
def get_entry(title):
    """
    根据词条标题读取Markdown内容，未找到返回None
    """
    filename = os.path.join(ENTRY_DIR, f"{title}.md")
    if not os.path.exists(filename):
        return None
    with open(filename, "r", encoding="utf-8") as f:
        return f.read()

# ------------------------------------------
# 工具函数：保存词条内容
# ------------------------------------------
def save_entry(title, content):
    """
    保存词条内容到Markdown文件（覆盖写入）
    """
    filename = os.path.join(ENTRY_DIR, f"{title}.md")
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)

# ------------------------------------------
# 帮助函数：计算最长公共子序列（LCS）长度
# ------------------------------------------
def lcs_length(a, b):
    """
    计算字符串a和b的最长公共子序列长度，忽略大小写
    动态规划实现，时间复杂度O(len(a)*len(b))
    """
    m, n = len(a), len(b)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if a[i - 1].lower() == b[j - 1].lower():
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    return dp[m][n]

# ------------------------------------------
# 路由：首页 显示所有词条
# ------------------------------------------
@app.route("/")
def index():
    entries = list_entries()
    return render_template("index.html", entries=entries)

# ------------------------------------------
# 路由：查看词条详情
# ------------------------------------------
@app.route("/wiki/<string:title>")
def view_entry(title):
    content_md = get_entry(title)
    if content_md is None:
        flash(f"词条“{title}”不存在。您可以创建该词条。")
        return redirect(url_for("create_entry", title=title))
    content_html = markdown.markdown(content_md, extensions=["extra", "codehilite"])
    return render_template("entry.html", title=title, content=content_html)

# ------------------------------------------
# 路由：创建新词条（GET显示表单，POST提交保存）
# ------------------------------------------
@app.route("/create", methods=["GET", "POST"])
def create_entry():
    title_prefill = request.args.get("title", "")

    if request.method == "POST":
        title = request.form.get("title", "").strip()
        content = request.form.get("content", "")

        if not title:
            flash("词条名称不能为空。")
            return render_template("create.html", title=title, content=content)

        if get_entry(title) is not None:
            flash(f"词条“{title}”已存在，请选择其他名称。")
            return render_template("create.html", title=title, content=content)

        save_entry(title, content)
        flash(f"词条“{title}”创建成功。")
        return redirect(url_for("view_entry", title=title))

    return render_template("create.html", title=title_prefill, content="")

# ------------------------------------------
# 路由：编辑词条（GET显示编辑表单，POST保存修改）
# ------------------------------------------
@app.route("/edit/<string:title>", methods=["GET", "POST"])
def edit_entry(title):
    content_md = get_entry(title)
    if content_md is None:
        flash(f"词条“{title}”不存在，无法编辑。")
        return redirect(url_for("index"))

    if request.method == "POST":
        content = request.form.get("content", "")
        save_entry(title, content)
        flash(f"词条“{title}”已更新。")
        return redirect(url_for("view_entry", title=title))

    return render_template("edit.html", title=title, content=content_md)

# ------------------------------------------
# 路由：搜索词条（使用最长公共子序列模糊匹配）
# ------------------------------------------
@app.route("/search", methods=["GET"])
def search():
    query = request.args.get("q", "").strip()
    if not query:
        return redirect(url_for("index"))

    entries = list_entries()
    # 精确匹配直接跳转查看该词条
    if query in entries:
        return redirect(url_for("view_entry", title=query))

    # 计算每个词条和搜索关键词的LCS匹配度（归一到0~1）
    scored_entries = []
    for entry in entries:
        lcs_len = lcs_length(query, entry)
        score = lcs_len / len(query) if query else 0
        scored_entries.append((entry, score))

    # 过滤匹配度低于0.3的词条，提高相关性
    scored_entries = [e for e in scored_entries if e[1] >= 0.3]
    # 按匹配度降序排序
    scored_entries.sort(key=lambda x: x[1], reverse=True)
    # 取匹配度最高的前10个
    top_results = [e[0] for e in scored_entries[:10]]

    return render_template("search.html", query=query, results=top_results)

# ------------------------------------------
# Flask 应用运行入口（调试模式开启）
# ------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)

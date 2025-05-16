import os  # 导入处理文件和路径的模块
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, abort  # 导入Flask及相关模块
import markdown  # 导入Markdown渲染模块

# ------------------------------------------
# 应用初始化和配置
# ------------------------------------------
app = Flask(__name__)  # 创建Flask应用实例
app.secret_key = "请替换成你自己的密钥"  # 用于flash消息，发布时请使用安全密钥
ENTRY_DIR = "entries"  # 词条Markdown文件存放目录
if not os.path.exists(ENTRY_DIR):  # 判断目录是否存在
    os.makedirs(ENTRY_DIR)  # 不存在则创建目录
# ------------------------------------------
# 工具函数：列出所有词条
# ------------------------------------------
def list_entries():  # 定义列表词条函数
    files = os.listdir(ENTRY_DIR)  # 获取目录下所有文件名
    entries = []  # 初始化词条列表
    for f in files:  # 遍历文件列表
        ends_with_md = f.endswith(".md")  # 判断文件名是否以.md结尾
        if ends_with_md:  # 如果是Markdown文件
            entries.append(f[:-3])  # 去掉.md后缀，添加词条名
    # 排序时区分大小写，转为小写排序实现不区分大小写排序
    entries_sorted = sorted(entries, key=str.lower)  # 按忽略大小写排序
    return entries_sorted  # 返回排序后的词条列表
# ------------------------------------------
# 工具函数：读取词条内容
# ------------------------------------------
def get_entry(title):  # 根据词条名读取Markdown内容
    filename = os.path.join(ENTRY_DIR, f"{title}.md")  # 构造词条文件路径
    file_exists = os.path.exists(filename)  # 判断文件是否存在
    if not file_exists:  # 文件不存在则返回None
        return None
    with open(filename, "r", encoding="utf-8") as f:  # 打开文件，使用utf-8编码读取
        content = f.read()  # 读取文件全部内容
    return content  # 返回读取内容
# ------------------------------------------
# 工具函数：保存词条内容
# ------------------------------------------
def save_entry(title, content):  # 将词条内容保存成Markdown文件
    filename = os.path.join(ENTRY_DIR, f"{title}.md")  # 构造要保存的文件路径
    with open(filename, "w", encoding="utf-8") as f:  # 以写入模式打开文件，utf-8编码
        f.write(content)  # 写入内容，覆盖原有内容
# ------------------------------------------
# 帮助函数：计算最长公共子序列（LCS）长度
# ------------------------------------------
def lcs_length(a, b):  # 计算字符串a和b的最长公共子序列长度，忽略大小写
    m = len(a)  # 字符串a长度
    n = len(b)  # 字符串b长度
    dp = []  # 初始化二维列表dp
    for _ in range(m + 1):  # 外层循环，从0到m
        dp.append([0] * (n + 1))  # 每行初始化n+1个0
    i = 1  # 行从1开始
    while i <= m:  # 遍历a字符串每个字符
        j = 1  # 列从1开始
        while j <= n:  # 遍历b字符串每个字符
            if a[i - 1].lower() == b[j - 1].lower():  # 比较字符，忽略大小写
                dp[i][j] = dp[i - 1][j - 1] + 1  # 相等则当前点等于左上角+1
            else:
                # 不相等取左边和上边最大值
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
            j += 1  # 列递增
        i += 1  # 行递增
    return dp[m][n]  # 返回右下角值即最长公共子序列长度
# ------------------------------------------
# 路由：首页，显示全部词条
# ------------------------------------------
@app.route("/")  # 根路径访问
def index():
    entries = list_entries()  # 获取词条列表
    return render_template("index.html", entries=entries)  # 渲染首页模板并传递词条
# ------------------------------------------
# 路由：查看词条内容
# ------------------------------------------
@app.route("/wiki/<string:title>")  # 动态路由，词条标题作为参数
def view_entry(title):
    content_md = get_entry(title)  # 获取词条Markdown内容
    if content_md is None:  # 词条不存在时
        flash(f"词条“{title}”不存在。您可以创建该词条。")  # 闪现提示信息
        redirect_target = url_for("create_entry", title=title)  # 创建词条页面链接
        return redirect(redirect_target)  # 重定向跳转
    content_html = markdown.markdown(content_md, extensions=["extra", "codehilite"])  # Markdown 转 HTML，带扩展
    return render_template("entry.html", title=title, content=content_html)  # 渲染词条页面并传词条内容
# ------------------------------------------
# 路由：创建新词条（GET显示表单，POST提交保存）
# ------------------------------------------
@app.route("/create", methods=["GET", "POST"])  # 支持GET和POST方法
def create_entry():
    title_prefill = request.args.get("title", "")  # GET请求时，用于预填入标题
    method_is_post = (request.method == "POST")  # 判断请求是否POST
    if method_is_post:  # POST请求处理保存
        title = request.form.get("title", "").strip()  # 获取表单词条名称，去除首尾空格
        content = request.form.get("content", "")  # 获取内容
        title_is_empty = (not title)  # 判断标题是否为空
        if title_is_empty:  # 空标题提示并返回表单
            flash("词条名称不能为空。")  # 提示错误
            return render_template("create.html", title=title, content=content)  # 返回创建页面
        entry_exists = (get_entry(title) is not None)  # 判断词条是否已存在
        if entry_exists:  # 已存在提示
            flash(f"词条“{title}”已存在，请选择其他名称。")
            return render_template("create.html", title=title, content=content)
        save_entry(title, content)  # 保存新词条
        flash(f"词条“{title}”创建成功。")  # 提示成功
        return redirect(url_for("view_entry", title=title))  # 重定向跳转到新词条页面
    return render_template("create.html", title=title_prefill, content="")  # GET请求渲染空白创建页面
# ------------------------------------------
# 路由：编辑词条（GET显示编辑表单，POST保存修改）
# ------------------------------------------
@app.route("/edit/<string:title>", methods=["GET", "POST"])  # 支持GET和POST
def edit_entry(title):
    content_md = get_entry(title)  # 读取词条内容
    content_missing = (content_md is None)  # 判断是否存在
    if content_missing:  # 不存在则提示并返回首页
        flash(f"词条“{title}”不存在，无法编辑。")
        return redirect(url_for("index"))
    method_is_post = (request.method == "POST")  # 判断请求是否POST
    if method_is_post:  # POST时更新保存内容
        content = request.form.get("content", "")  # 获取修改后的内容
        save_entry(title, content)  # 保存覆盖原词条
        flash(f"词条“{title}”已更新。")  # 提示更新成功
        return redirect(url_for("view_entry", title=title))  # 重定向查看页面
    return render_template("edit.html", title=title, content=content_md)  # GET时渲染编辑页面并填充内容
# ------------------------------------------
# 路由：搜索词条（最长公共子序列模糊匹配）
# ------------------------------------------
@app.route("/search", methods=["GET"])  # 仅支持GET
def search():
    query = request.args.get("q", "").strip()  # 获取URL查询参数q，去除空白
    query_is_empty = (query == "")  # 判断是否为空
    if query_is_empty:  # 空查询跳转首页
        return redirect(url_for("index"))
    entries = list_entries()  # 获取所有词条列表
    query_in_entries = (query in entries)  # 是否精确匹配的词条
    if query_in_entries:  # 精确匹配直接跳转词条页面
        return redirect(url_for("view_entry", title=query))
    scored_entries = []  # 初始化列表存放词条和匹配度
    for entry in entries:  # 遍历所有词条
        lcs_len = lcs_length(query, entry)  # 计算LCS长度
        score = 0 if len(query) == 0 else lcs_len / len(query)  # 归一得分，防止除0
        scored_entries.append((entry, score))  # 添加元组 (词条名, 匹配分)
    filtered_entries = []  # 过滤匹配度不够的词条
    for e in scored_entries:  # 遍历评分列表
        if e[1] >= 0.3:  # 过滤阈值0.3
            filtered_entries.append(e)
    scored_entries_sorted = sorted(filtered_entries, key=lambda x: x[1], reverse=True)  # 按匹配度降序排序
    top_results = []  # 取最相关的前10个
    count = 0
    while count < 10 and count < len(scored_entries_sorted):
        top_results.append(scored_entries_sorted[count][0])
        count += 1
    return render_template("search.html", query=query, results=top_results)  # 渲染搜索结果页
# ------------------------------------------
# API接口：返回所有词条列表（JSON）
# ------------------------------------------
@app.route("/api/entries", methods=["GET"])  # 支持GET请求
def api_list_entries():
    entries = list_entries()  # 获取词条列表
    return jsonify({"entries": entries})  # 返回JSON格式响应
# ------------------------------------------
# API接口：返回指定词条内容（JSON）
# ------------------------------------------
@app.route("/api/entry/<string:title>", methods=["GET"])  # 动态路由，词条名参数
def api_get_entry(title):
    content = get_entry(title)  # 获取词条Markdown内容
    if content is None:  # 不存在词条返回404错误
        abort(404, description=f"词条“{title}”不存在。")
    return jsonify({"title": title, "content": content})  # 返回词条标题和Markdown内容JSON
# ------------------------------------------
# Flask应用启动入口
# ------------------------------------------
if __name__ == "__main__":  
    app.run(debug=False)

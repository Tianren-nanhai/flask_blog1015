from flask import Flask, render_template, request, redirect, url_for, abort

app = Flask(__name__)

# 暫時使用 list 儲存文章
posts = [
    {
        "id": 1,
        "title": "我的第一篇文章",
        "author": "小明",
        "content": "歡迎來到我的部落格！\n這是第一篇文章。"
    },

    {
        "id": 2,
        "title": "學習 Python Flask",
        "author": "小華",
        "content": "Flask 是一個輕量且容易上手的 Python Web 框架。"
    }
]


@app.route("/")
def index():
    return render_template("index.html", posts=posts)


@app.route("/post/<int:post_id>")
def show_post(post_id):
    # 根據文章 ID 找出文章
    post = next(
        (p for p in posts if p["id"] == post_id),
        None
    )

    if post is None:
        abort(404)

    return render_template("post.html", post=post)


@app.route("/new", methods=["GET", "POST"])
def new_post():
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        author = request.form.get("author", "").strip()
        content = request.form.get("content", "").strip()

        # 簡單的欄位驗證
        if not title or not author or not content:
            return render_template(
                "new_post.html",
                error="標題、作者及文章內容都必須填寫。"
            ), 400

        post = {
            "id": max((p["id"] for p in posts), default=0) + 1,
            "title": title,
            "author": author,
            "content": content
        }

        posts.append(post)

        return redirect(url_for("show_post", post_id=post["id"]))

    return render_template("new_post.html")


if __name__ == "__main__":
    app.run(debug=True)
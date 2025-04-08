from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
import os
import json

app = Flask(__name__)
app.secret_key = 'secret_key'
COMMENTS_FILE = 'comments.json'


def get_comments():
    if not os.path.exists(COMMENTS_FILE):
        return []

    with open(COMMENTS_FILE, 'r', encoding='utf-8') as f:
        try:
            return json.load(f)
        except json.decoder.JSONDecodeError:
            return []


def save_comment(name, text):
    comments = get_comments()
    comments.insert(0, {
        'name': name,
        'text': text,
        'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    })

    with open(COMMENTS_FILE, 'w', encoding='utf-8') as f:
        json.dump(comments, f, indent=2, ensure_ascii=False)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form.get('name')
        text = request.form.get('text')
        if name and text:
            save_comment(name, text)
        return redirect(url_for('index'))

    page = request.args.get('page', 1, type=int)
    per_page = 5
    all_comments = get_comments()

    start = (page - 1) * per_page
    end = start + per_page
    comments = all_comments[start:end]

    total_pages = (len(all_comments) + per_page - 1) // per_page

    return render_template(
        'index.html',
        comments=comments,
        page=page,
        total_pages=total_pages
    )


if __name__ == '__main__':
    app.run(debug=True)
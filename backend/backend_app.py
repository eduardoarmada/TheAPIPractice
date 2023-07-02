from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
]


def validate_data(data):
    """Validates the data of the posts that are to be added"""
    if "title" not in data or "content" not in data:
        return False
    return True


@app.route('/api/posts', methods=['GET', 'POST'])
def get_posts():
    if request.method == 'POST':
        if not validate_data(request.json):
            return jsonify("error: invalid data"), 400

        title = request.json.get('title', "Default title")
        content = request.json.get('content', "Default content")
        id_post = max([post['id'] for post in POSTS]) + 1
        POSTS.append({'id': id_post, 'title': title, 'content': content})

        return jsonify(POSTS)

    else:
        query_data = request.args
        posts = list(POSTS)
        if query_data.get('sort'):
            order = False
            if query_data.get('direction') == "asc":
                order = True
            posts = sorted(posts, key=lambda post: post[query_data.get('sort')].lower(), reverse=order)

        return jsonify(posts)


@app.route("/api/posts/<int:id_number>", methods=["DELETE"])
def delete_post(id_number):
    for post in POSTS:
        if post['id'] == id_number:
            del POSTS[POSTS.index(post)]
            return jsonify(f"message: Post with id {id_number} has been deleted successfully.")
    return jsonify(f"error: No post with id {id_number} was found"), 404


@app.route("/api/posts/<int:id_number>", methods=["PUT"])
def update_post(id_number):
    for post in POSTS:
        if post['id'] == id_number:
            updated_post = {'id': id_number, 'title': request.json.get('title', post['title']), 'content': request.json.get('content', post['content'])}
            POSTS[POSTS.index(post)] = updated_post
            return jsonify(updated_post)
    return jsonify(f"error: No post with id {id_number} was found"), 404


@app.route("/api/posts/search")
def search_post():
    query_data = request.args
    posts_that_match = []
    if query_data.get('title') or query_data.get('content'):
        for query in query_data.items():
            for post in POSTS:
                if query[1].lower() in post[query[0]].lower():
                    posts_that_match.append(post)
    return jsonify(posts_that_match)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)

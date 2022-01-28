from flask_app import app
from flask import render_template,redirect,request,session,flash
from flask_app.models.user import User
from flask_app.models.post import Post

@app.route('/post', methods=['POST'])
def post():
    if len(session) < 1:
        return redirect('/')
    if not Post.validate_post(request.form):
        return redirect('/dashboard')
    data = {
        "text": request.form['text'],
        "user_id": session['user_id']
    }
    return redirect('/post/' + str(Post.save(data)))

@app.route('/post/<post_id>')
def show(post_id):
    if len(session) < 1:
        return redirect('/')
    data = {"id": post_id}
    post = Post.get(data)
    return render_template("post.html", post = post)

@app.route('/post/<post_id>/delete')
def delete(post_id):
    if len(session) < 1:
        return redirect('/')
    data = {"id": post_id}
    Post.remove(data)
    return redirect('/dashboard')

@app.route('/post/<post_id>/edit')
def edit(post_id):
    if len(session) < 1:
        return redirect('/')
    data = {"id": post_id}
    post = Post.get(data)
    return render_template("edit.html", post = post)

@app.route('/post/<post_id>/update', methods=['POST'])
def update(post_id):
    if len(session) < 1:
        return redirect('/')
    if not Post.validate_post(request.form):
        return redirect('/post/' + str(post_id) +'/edit')
    data = {
        "id": post_id,
        "text": request.form['text']
    }
    Post.update(data)
    return redirect('/post/' + str(post_id))
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from models import db, User, Post, Comment, Follower
from datetime import timedelta

# Create a blueprint
api = Blueprint('api', __name__)

@api.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'User already exists'}), 400

    user = User(username=data['username'], email=data['email'])
    user.set_password(data['password'])
    db.session.add(user)
    db.session.commit()
    
    return jsonify({'message': 'User registered successfully'}), 201

@api.route('/login', methods=['POST'])

def login():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    
    if user and user.check_password(data['password']):
        token = create_access_token(identity=user.id, expires_delta=timedelta(days=1))
        return jsonify({'token': token}), 200
    else:
        return jsonify({'error': 'Invalid credentials'}), 401

@api.route('/post', methods=['POST'])
@jwt_required()
def create_post():
    user_id = get_jwt_identity()
    data = request.get_json()

    post = Post(title=data['title'], content=data['content'], image_url=data['image_url'], user_id=user_id)
    db.session.add(post)
    db.session.commit()

    return jsonify({'message': 'Post created successfully'}), 201

@api.route('/posts', methods=['GET'])
def get_posts():
    posts = Post.query.all()  # Fetch all posts from the database
    return jsonify([{'id': post.id, 'title': post.title, 'content': post.content, 'image_url': post.image_url, 'user_id': post.user_id} for post in posts]), 200

@api.route('/feed', methods=['GET'])
@jwt_required()
def get_feed():
    user_id = get_jwt_identity()
    followed_ids = [f.followed_id for f in Follower.query.filter_by(follower_id=user_id).all()]
    posts = Post.query.filter(Post.user_id.in_(followed_ids)).all()

    return jsonify([{'id': post.id, 'title': post.title, 'content': post.content} for post in posts]), 200

@api.route('/follow/<int:user_id>', methods=['POST'])
@jwt_required()
def follow_user(user_id):
    follower_id = get_jwt_identity()

    if Follower.query.filter_by(follower_id=follower_id, followed_id=user_id).first():
        return jsonify({'error': 'Already following this user'}), 400

    follow = Follower(follower_id=follower_id, followed_id=user_id)
    db.session.add(follow)
    db.session.commit()

    return jsonify({'message': 'User followed successfully'}), 201

@api.route('/comment', methods=['POST'])
@jwt_required()
def add_comment():
    user_id = get_jwt_identity()
    data = request.get_json()

    comment = Comment(content=data['content'], user_id=user_id, post_id=data['post_id'])
    db.session.add(comment)
    db.session.commit()

    return jsonify({'message': 'Comment added successfully'}), 201

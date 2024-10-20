from flask import Flask, request, jsonify
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from models import db, User, Post, Comment, Follower
from datetime import timedelta

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    # Initialize the database and migration
    db.init_app(app)
    migrate = Migrate(app, db)
    jwt = JWTManager(app)  # Initialize the JWT manager

    with app.app_context():
        # Create the database tables if they don't exist
        db.create_all()

        # Define your routes here
        @app.route('/register', methods=['POST'])
        def register():
            data = request.get_json()
            if User.query.filter_by(email=data['email']).first():
                return jsonify({'error': 'User already exists'}), 400

            user = User(username=data['username'], email=data['email'])
            user.set_password(data['password'])
            db.session.add(user)
            db.session.commit()
            
            return jsonify({'message': 'User registered successfully'}), 201

        @app.route('/login', methods=['POST'])
        def login():
            data = request.get_json()
            user = User.query.filter_by(email=data['email']).first()
            
            if user and user.check_password(data['password']):
                token = create_access_token(identity=user.id, expires_delta=timedelta(days=1))
                return jsonify({'token': token}), 200
            else:
                return jsonify({'error': 'Invalid credentials'}), 401

        @app.route('/post', methods=['POST'])
        @jwt_required()
        def create_post():
            user_id = get_jwt_identity()
            data = request.get_json()

            post = Post(title=data['title'], content=data['content'], image_url=data['image_url'], user_id=user_id)
            db.session.add(post)
            db.session.commit()

            return jsonify({'message': 'Post created successfully'}), 201

        @app.route('/posts', methods=['GET'])
        #@jwt_required()  # Optional: require authentication to view posts
        def get_posts():
            posts = Post.query.all()  # Fetch all posts from the database
            return jsonify([{'id': post.id, 'title': post.title, 'content': post.content, 'image_url': post.image_url, 'user_id': post.user_id} for post in posts]), 200

        # Add other routes as needed...

    return app

if __name__ == '__main__':
    app = create_app()  # Create an instance of the app
    app.run(debug=True)

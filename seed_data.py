from app import create_app, db  # Update this import based on your project structure
from app.models import User, Post, Comment, Follower  # Adjust based on your model names

app = create_app()

# Initialize the app context
with app.app_context():
    # Create initial users
    user1 = User(username='traveler1', email='traveler1@example.com', password='password1')
    user2 = User(username='traveler2', email='traveler2@example.com', password='password2')

    # Add users to the session
    db.session.add(user1)
    db.session.add(user2)

    # Commit to save the users
    db.session.commit()

    # Create initial posts
    post1 = Post(title='My Trip to the Grand Canyon', description='It was an amazing experience!', user_id=user1.id)
    post2 = Post(title='Exploring the Beaches of Hawaii', description='Sunshine and surf!', user_id=user2.id)

    # Add posts to the session
    db.session.add(post1)
    db.session.add(post2)

    # Commit to save the posts
    db.session.commit()

    # Create initial comments
    comment1 = Comment(content='Looks beautiful!', post_id=post1.id, user_id=user2.id)
    comment2 = Comment(content='I want to go there!', post_id=post2.id, user_id=user1.id)

    # Add comments to the session
    db.session.add(comment1)
    db.session.add(comment2)

    # Commit to save the comments
    db.session.commit()

    # Create initial followers
    follower1 = Follower(follower_id=user1.id, followed_id=user2.id)
    follower2 = Follower(follower_id=user2.id, followed_id=user1.id)

    # Add followers to the session
    db.session.add(follower1)
    db.session.add(follower2)

    # Commit to save the followers
    db.session.commit()

    print("Initial data inserted successfully!")

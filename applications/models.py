from datetime import datetime
from hashlib import md5

from flask_login import UserMixin, current_user
from applications.database import db
from applications.search import *
from flask import current_app as app


class SearchableMixin(object):
    @classmethod
    def search(cls, expression, page, per_page):
        ids, total = query_index(cls.__tablename__, expression, page, per_page)
        if total == 0:
            return cls.query.filter_by(id=0), 0
        when = []
        for i in range(len(ids)):
            when.append((ids[i], i))
        return cls.query.filter(cls.id.in_(ids)).order_by(
            db.case(when, value=cls.id)), total

    @classmethod
    def before_commit(cls, session):
        session._changes = {
            'add': list(session.new),
            'update': list(session.dirty),
            'delete': list(session.deleted)
        }

    @classmethod
    def after_commit(cls, session):
        for obj in session._changes['add']:
            if isinstance(obj, SearchableMixin):
                add_to_index(obj.__tablename__, obj)
        for obj in session._changes['update']:
            if isinstance(obj, SearchableMixin):
                add_to_index(obj.__tablename__, obj)
        for obj in session._changes['delete']:
            if isinstance(obj, SearchableMixin):
                remove_from_index(obj.__tablename__, obj)
        session._changes = None

    @classmethod
    def reindex(cls):
        for obj in cls.query:
            add_to_index(cls.__tablename__, obj)


db.event.listen(db.session, 'before_commit', SearchableMixin.before_commit)
db.event.listen(db.session, 'after_commit', SearchableMixin.after_commit)

followers = db.Table(
    'followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
)


class User(db.Model, UserMixin, SearchableMixin):
    __tablename__ = 'user'
    __searchable__ = ['username']
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    username = db.Column(db.String, unique=True, nullable=False)
    f_name = db.Column(db.String, nullable=False)
    l_name = db.Column(db.String)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    about_me = db.Column(db.String(140))
    imgProfile = db.Column(db.String(300))
    posts = db.relationship('Post', backref='author', lazy='dynamic', passive_deletes=True)
    # posts_liked = db.relationship('Likes', backref='user', lazy='dynamic', passive_deletes=True)
    followed = db.relationship(
        'User', secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref('followers', lazy='dynamic'), lazy='dynamic', passive_deletes=True)
    # comment = db.relationship('Comments', backref='author', lazy='dynamic', passive_deletes=True)

    def __repr__(self):
        return '<User: %s>' % self.username

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(digest, size)

    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)

    def is_following(self, user):
        return self.followed.filter(followers.c.followed_id == user.id).count() >= 0

    # def followed_posts(self):
    #     followed = Post.query.join(followers.c.followed_id == Post.id).filter(followers.c.followed_id == self.id)
    #     own = Post.query.filter_by(user_id=self.id).order_by(Post.timestamp.desc()).limit(1)
    #     return followed.union(own).order_by(Post.timestamp.desc())
    #
    # def like_post(self, post):
    #     if not self.post_like(post):
    #         like = Likes(user_id=self.id, post_id=post.p_id)
    #
    # def dislike_post(self, post):
    #     if self.post_liked(post):
    #         Likes.query.filter_by(user_id=self.id, post_id=post.id).delete()
    #
    # def post_liked(self, post):
    #     return Likes.query.filter(Likes.user_id == self.id, Likes.post_id == post.id).count() > 0


class Post(db.Model):
    __tablename__ = 'post'
    id = db.Column(db.Integer, primary_key=True)
    img = db.Column(db.String(300))
    description = db.Column(db.String)
    # timestamp = db.Column(db.DateTime, index=True, default=datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id", ondelete='CASCADE'))
    # likes = db.relationship('Likes', backref='likes', lazy='dynamic', passive_deletes=True)
    # comments = db.relationship('Comments', backref='comments', lazy='dynamic', passive_deletes=True)
    count_likes = db.Column(db.Integer)

    def __repr__(self):
        return '<Post {}>'.format(self.img)


# class Likes(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))
#     post_id = db.Column(db.Integer, db.ForeignKey('post.id', ondelete='CASCADE'))
#
#     def __repr__(self):
#         return '<Likes {}>'.format(self.id)

#
# class Comments(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))
#     post_id = db.Column(db.Integer, db.ForeignKey('post.id', ondelete='CASCADE'))
#     body = db.Column(db.String(500))
#     timestamp = db.Column(db.DateTime, index=True, default=datetime.now)

# class Followers(db.Model):
#     __tablename__ = 'followers'
#     follower_id = db.Column(db.Integer, foreign_key='user.id')
#     followed_id = db.Column(db.Integer, foreign_key='user.id')

# class Profile(db.Model):
#     __tablename__ = 'profile'
#     username = db.Column(db.String, primary_key=True)
#     bio = db.Column(db.String)
#     post = db.Column(db.String)

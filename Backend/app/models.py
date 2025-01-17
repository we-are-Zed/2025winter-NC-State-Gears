from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.mysql import *
from sqlalchemy_utils import EncryptedType


db = SQLAlchemy()
KEY = 'M4k3SqlLabGreatAg4in'


class User(db.Model):
    __tablename__ = 'user'

    id              = db.Column(BIGINT, primary_key=True, autoincrement=True)
    sid             = db.Column(VARCHAR(20), unique=True, nullable=False)
    username        = db.Column(VARCHAR(100), unique=True, nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'


class Group(db.Model):
    __tablename__ = 'group'

    id              = db.Column(BIGINT, primary_key=True, autoincrement=True)
    groupname       = db.Column(VARCHAR(100), unique=True, nullable=False)
    description     = db.Column(VARCHAR(255), nullable=True)


class UserGroup(db.Model):
    __tablename__ = 'user_group'

    id              = db.Column(BIGINT, primary_key=True, autoincrement=True)
    user_id         = db.Column(BIGINT, db.ForeignKey('user.id', ondelete='CASCADE'))
    group_id        = db.Column(BIGINT, db.ForeignKey('group.id', ondelete='CASCADE'))
    is_admin        = db.Column(INTEGER, default=0)

    def get_id(self):
        return self.id


class Polls(db.Model):
    __tablename__ = 'polls'
    # ownership control
    id              = db.Column(BIGINT, primary_key=True, autoincrement=True)
    user_id         = db.Column(BIGINT, db.ForeignKey('user.id', ondelete='CASCADE'))
    privilege       = db.Column(INTEGER, nullable=True) # RWX RWX: group, others
    # information
    title           = db.Column(VARCHAR(255), nullable=False)       # 标题
    count           = db.Column(INTEGER, nullable=True, default=0)  # 人数
    status          = db.Column(INTEGER, nullable=True, default=0)  # 状态: 未发布/发布/删除
    create_time     = db.Column(DATETIME, nullable=False)           # 创建时间
    expiration_time = db.Column(DATETIME, nullable=False)           # 截止时间
    public_time     = db.Column(DATETIME, nullable=True)

    def get_id(self):
        return self.id


class Section(db.Model):
    __tablename__ = 'section'
    # identification
    id              = db.Column(BIGINT, primary_key=True, autoincrement=True)
    poll_id         = db.Column(BIGINT, db.ForeignKey('polls.id', ondelete='CASCADE'), nullable=False)
    # information
    title           = db.Column(VARCHAR(255), nullable=False)
    description     = db.Column(VARCHAR(255), nullable=True)
    order_value     = db.Column(INTEGER, nullable=False)

    def get_id(self):
        return self.id


class Votes(db.Model):
    __tablename__ = 'votes'
    # identification
    id              = db.Column(BIGINT, primary_key=True, autoincrement=True)
    section_id      = db.Column(BIGINT, db.ForeignKey('polls.id', ondelete='CASCADE'), nullable=False)
    # information
    title           = db.Column(VARCHAR(255), nullable=False)
    vote_type       = db.Column(INTEGER, nullable=False)
    limit_count     = db.Column(INTEGER, nullable=False)
    order_value     = db.Column(INTEGER, nullable=False)

    def get_id(self):
        return self.id


class Choices(db.Model):
    __tablename__ = 'choices'
    # identification
    id              = db.Column(BIGINT, primary_key=True, autoincrement=True)
    vote_id         = db.Column(BIGINT, db.ForeignKey('votes.id', ondelete='CASCADE'), nullable=False)
    # information
    description     = db.Column(VARCHAR(255), nullable=True)
    choice_type     = db.Column(INTEGER, nullable=False)

    def get_id(self):
        return self.id


class UserChoice(db.Model):
    __tablename__ = 'user_choice'
    # identification
    id              = db.Column(BIGINT, primary_key=True, autoincrement=True)
    user_id         = db.Column(BIGINT, db.ForeignKey('user.id', ondelete='CASCADE'))
    choice_id       = db.Column(BIGINT, db.ForeignKey('choices.id', ondelete='CASCADE'))
    # information
    comment         = db.Column(VARCHAR(1024))
    order_value     = db.Column(INTEGER, nullable=False)
    is_choosed      = db.Column(INTEGER, default=0)

    def get_id(self):
        return self.id


class StarList(db.Model):
    __tablename__ = 'star_list'
    # information
    id              = db.Column(BIGINT, primary_key=True, autoincrement=True)
    user_id         = db.Column(BIGINT, db.ForeignKey('user.id', ondelete='CASCADE'))
    poll_id         = db.Column(BIGINT, db.ForeignKey('polls.id', ondelete='CASCADE'))


class VoteCount(db.Model):
    __tablename__ = 'vote_count'
    # information
    id              = db.Column(BIGINT, primary_key=True, autoincrement=True)
    choice_id       = db.Column(BIGINT, db.ForeignKey('choices.id', ondelete='CASCADE'))
    cnt             = db.Column(BIGINT, nullable=False, default=0)

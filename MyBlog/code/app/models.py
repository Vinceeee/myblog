import os
import hashlib
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask.ext.login import UserMixin
from . import db, login_manager

article_types = {'IT相关': ['编程语言', 'Linux','网络技术', '数据库'],
                 '漫漫人生': ['生活那些事', '学校那些事', '感情那些事'],
                 }


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    avatar_hash = db.Column(db.String(32))

    @staticmethod
    def insert_admin(email, username, password):
        if User.query.filter_by(email=email).first() and User.query.filter_by(username=username).first():
            user = User.query.filter_by(username=username).first()
        else:
            user = User(email=email, username=username, password=password)
        db.session.add(user)
        db.session.commit()

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.email is not None and self.avatar_hash is None:
            self.avatar_hash = hashlib.md5(
                    self.email.encode('utf-8')).hexdigest()

    # gravatar is for icon
    def gravatar(self, size=40, default='identicon', rating='g'):
        # if request.is_secure:
        #     url = 'https://secure.gravatar.com/avatar'
        # else:
        #     url = 'http://www.gravatar.com/avatar'
        url = 'http://gravatar.duoshuo.com/avatar'
        hash = self.avatar_hash or hashlib.md5(
            self.email.encode('utf-8')).hexdigest()
        return '{url}/{hash}?s={size}&d={default}&r={rating}'.format(
            url=url, hash=hash, size=size, default=default, rating=rating)

# callback function for flask-login extentsion
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Menu(db.Model):
    __tablename__ = 'menus'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    types = db.relationship('ArticleType', backref='menu', lazy='dynamic')
    order = db.Column(db.Integer, default=0, nullable=False)

    def sort_delete(self):
        for menu in Menu.query.order_by(Menu.order).offset(self.order).all():
            menu.order -= 1
            db.session.add(menu)

    @staticmethod
    def insert_menus():
        menus = article_types.keys()
        for name in menus:
            menu = Menu(name=name)
            db.session.add(menu)
            db.session.commit()
            menu.order = menu.id
            db.session.add(menu)
            db.session.commit()

    @staticmethod
    def return_menus():
        menus = [(m.id, m.name) for m in Menu.query.all()]
        menus.append((-1, u'不选择导航（该分类将单独成一导航）'))
        return menus

    def __repr__(self):
        return '<Menu %r>' % self.name


class ArticleTypeSetting(db.Model):
    __tablename__ = 'articleTypeSettings'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    protected = db.Column(db.Boolean, default=False)
    hide = db.Column(db.Boolean, default=False)
    types = db.relationship('ArticleType', backref='setting', lazy='dynamic')

    @staticmethod
    def insert_system_setting():
        system = ArticleTypeSetting(name='system', protected=True, hide=True)
        db.session.add(system)
        db.session.commit()

    @staticmethod
    def insert_default_settings():
        system_setting = ArticleTypeSetting(name='system', protected=True, hide=True)
        common_setting = ArticleTypeSetting(name='common', protected=False, hide=False)
        db.session.add(system_setting)
        db.session.add(common_setting)
        db.session.commit()

    @staticmethod
    def return_setting_hide():
        return [(2, u'公开'), (1, u'隐藏')]

    def __repr__(self):
        return '<ArticleTypeSetting %r>' % self.name


class ArticleType(db.Model):
    __tablename__ = 'articleTypes'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    introduction = db.Column(db.Text, default=None)
    articles = db.relationship('Article', backref='articleType', lazy='dynamic')
    menu_id = db.Column(db.Integer, db.ForeignKey('menus.id'), default=None)
    setting_id = db.Column(db.Integer, db.ForeignKey('articleTypeSettings.id'))

    @staticmethod
    def insert_system_articleType():
        articleType = ArticleType(name='未分类',
                                  introduction='系统默认分类，不可删除。',
                                  setting=ArticleTypeSetting.query.filter_by(protected=True).first()
                                  )
        db.session.add(articleType)
        db.session.commit()

    @staticmethod
    def insert_articleTypes():

        for key,values in article_types.items():
            menu = Menu.query.filter_by(name=key).first()
            for name in values:
                articleType = ArticleType(name=name,menu=menu,
                                      setting=ArticleTypeSetting(name=name))
                db.session.add(articleType)
            db.session.commit()

    @property
    def is_protected(self):
        if self.setting:
            return self.setting.protected
        else:
            return False

    @property
    def is_hide(self):
        if self.setting:
            return self.setting.hide
        else:
            return False
    # if the articleType does not have setting,
    # its is_hie and is_protected property will be False.

    def __repr__(self):
        return '<Type %r>' % self.name


class Source(db.Model):
    __tablename__ = 'sources'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    articles = db.relationship('Article', backref='source', lazy='dynamic')

    @staticmethod
    def insert_sources():
        sources = (u'原创',
                   u'转载',
                   u'翻译')
        for s in sources:
            source = Source.query.filter_by(name=s).first()
            if source is None:
                source = Source(name=s)
            db.session.add(source)
        db.session.commit()

    def __repr__(self):
        return '<Source %r>' % self.name


class Follow(db.Model):
    __tablename__ = 'follows'
    follower_id = db.Column(db.Integer, db.ForeignKey('comments.id'),
                           primary_key=True)
    followed_id = db.Column(db.Integer, db.ForeignKey('comments.id'),
                         primary_key=True)


class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    author_name = db.Column(db.String(64))
    author_email = db.Column(db.String(64))
    avatar_hash = db.Column(db.String(32))
    article_id = db.Column(db.Integer, db.ForeignKey('articles.id'))
    disabled = db.Column(db.Boolean, default=False)
    comment_type = db.Column(db.String(64), default='comment')
    reply_to = db.Column(db.String(128), default='notReply')

    followed = db.relationship('Follow',
                               foreign_keys=[Follow.follower_id],
                               backref=db.backref('follower', lazy='joined'),
                               lazy='dynamic',
                               cascade='all, delete-orphan')
    followers = db.relationship('Follow',
                               foreign_keys=[Follow.followed_id],
                               backref=db.backref('followed', lazy='joined'),
                               lazy='dynamic',
                               cascade='all, delete-orphan')

    def __init__(self, **kwargs):
        super(Comment, self).__init__(**kwargs)
        if self.author_email is not None and self.avatar_hash is None:
            self.avatar_hash = hashlib.md5(
                    self.author_email.encode('utf-8')).hexdigest()

    def gravatar(self, size=40, default='identicon', rating='g'):
        # if request.is_secure:
        #     url = 'https://secure.gravatar.com/avatar'
        # else:
        #     url = 'http://www.gravatar.com/avatar'
        url = 'http://gravatar.duoshuo.com/avatar'
        hash = self.avatar_hash or hashlib.md5(
            self.author_email.encode('utf-8')).hexdigest()
        return '{url}/{hash}?s={size}&d={default}&r={rating}'.format(
            url=url, hash=hash, size=size, default=default, rating=rating)

    @staticmethod
    def generate_fake(count=100):
        from random import randint
        # import forgery_py
        from faker import Faker

        f = Faker("zh_cn")

        article_count = Article.query.count()
        for i in range(count):
            a = Article.query.offset(randint(0, article_count - 1)).first()
            c = Comment(content= f.text(randint(15,100)),
                        timestamp= f.date_time_between_dates(datetime_start=a.create_time,datetime_end=datetime.utcnow()),
                        author_name= f.name(),
                        author_email= f.email(),
                        article=a)
            db.session.add(c)
        try:
            db.session.commit()
        except:
            db.session.rollback()

    @staticmethod
    def generate_fake_replies(count=100):
        from random import seed, randint
        from faker import Faker

        f = Faker("zh_cn")

        comment_count = Comment.query.count()
        for i in range(count):
            followed = Comment.query.offset(randint(0, comment_count - 1)).first()
            c = Comment(content=f.text(randint(15,100)),
                        timestamp= f.date_time_between_dates(datetime_start=followed.timestamp,datetime_end=datetime.utcnow()),
                        author_name= f.name(),
                        author_email= f.email(),
                        article=followed.article, comment_type='reply',
                        reply_to=followed.author_name)
            fo = Follow(follower=c, followed=followed)
            db.session.add(fo)
            db.session.commit()

    def is_reply(self):
        if self.followed.count() == 0:
            return False
        else:
            return True
    # to confirm whether the comment is a reply or not

    def followed_name(self):
        if self.is_reply():
            return self.followed.first().followed.author_name

class Article(db.Model):
    __tablename__ = 'articles'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), unique=True)
    content = db.Column(db.Text)
    summary = db.Column(db.Text)
    create_time = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    update_time = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    num_of_view = db.Column(db.Integer, default=0)
    articleType_id = db.Column(db.Integer, db.ForeignKey('articleTypes.id'))
    source_id = db.Column(db.Integer, db.ForeignKey('sources.id'))
    comments = db.relationship('Comment', backref='article', lazy='dynamic')

    def tojson(self):
        return {
            'title':self.title,
            'content': self.content,
            'summary': self.summary,
            'create_time': self.create_time,
            'update_time': self.update_time,
            'num_of_view':self.num_of_view
        }

    @staticmethod
    def generate_fake(count=100):
        from sqlalchemy.exc import IntegrityError
        from random import randint
        from faker import Faker

        f = Faker('zh_cn')

        articleType_count = ArticleType.query.count()
        source_count = Source.query.count()
        for i in range(count):
            aT = ArticleType.query.offset(randint(0, articleType_count - 1)).first()
            s = Source.query.offset(randint(0, source_count - 1)).first()
            a = Article(title= f.sentence(),
                        content= f.text(randint(100,800)),
                        create_time= f.past_datetime(start_date='-10d'),
                        summary= f.text(randint(20,200)),
                        num_of_view= randint(50,200),
                        articleType=aT, source=s)
            db.session.add(a)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()

    @staticmethod
    def add_view(article, db):
        article.num_of_view += 1
        db.session.add(article)
        db.session.commit()

    def __repr__(self):
        return '<Article %r>' % self.title




class BlogInfo(db.Model):
    __tablename__ = 'blog_info'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64))
    signature = db.Column(db.Text)
    navbar = db.Column(db.String(64))
    music_163_id = db.Column(db.Integer,default=29567189)

    @staticmethod
    def insert_blog_info():
        blog_mini_info = BlogInfo(title='Vinceeeeeeeeee',
                                  signature='年年岁岁花相似，岁岁年年人不同',
                                  navbar='inverse')
        db.session.add(blog_mini_info)
        db.session.commit()




class Plugin(db.Model):
    __tablename__ = 'plugins'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), unique=True)
    note = db.Column(db.Text, default='')
    content = db.Column(db.Text, default='')
    order = db.Column(db.Integer, default=0)
    disabled = db.Column(db.Boolean, default=False)

    @staticmethod
    def insert_system_plugin():
        plugin = Plugin(title=u'博客统计',
                        note=u'系统插件',
                        content='system_plugin',
			order=1)
        db.session.add(plugin)
        db.session.commit()

    def sort_delete(self):
        for plugin in Plugin.query.order_by(Plugin.order.asc()).offset(self.order).all():
            plugin.order -= 1
            db.session.add(plugin)

    def __repr__(self):
        return '<Plugin %r>' % self.title


class BlogView(db.Model):
    __tablename__ = 'blog_view'
    id = db.Column(db.Integer, primary_key=True)
    num_of_view = db.Column(db.BigInteger, default=0)

    @staticmethod
    def insert_view():
        view = BlogView(num_of_view=0)
        db.session.add(view)
        db.session.commit()

    @staticmethod
    def add_view(db,ip):
        from redis import Redis
        redis_cache = Redis(os.environ.get('REDIS_HOST') or '0.0.0.0')
        # redis_cache = Redis('redis')

        if not redis_cache.ttl(ip):
            redis_cache.set(ip,0,ex=36) # cache the ip address into redis , set expire time
            view = BlogView.query.first()
            view.num_of_view += 1
            db.session.add(view)
            db.session.commit()

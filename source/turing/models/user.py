# coding: utf-8

import time

from sqlalchemy import Column, Integer, Unicode, Boolean
from .role_code import RoleCode
from orm import Base


class User(Base):
    __tablename__ = 'user'
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8'
    }
    # 主键
    id = Column(Integer, nullable=False, primary_key=True)
    # 用户名
    username = Column(Unicode(255), nullable=False, unique=True)
    # 密码
    passwd = Column(Unicode(255), nullable=False)
    # 角色：
    # 2:管理员
    # 1:普通用户
    role = Column(Integer, nullable=False, default=0)
    # 是否被封禁
    forbidden = Column(Boolean, nullable=False, default=False)
    # 活跃时间
    active = Column(Integer, nullable=False, default=int(time.time()))
    # 生成token的时间
    token_time = Column(Integer, nullable=False, default=int(time.time()))
    # 创建时间
    created_at = Column(Integer, nullable=False, default=int(time.time()))

    KEY_ONLINE = 'online:{.id}'
    KEY_G_ONLINE = 'online'

    def __repr__(self):
        return 'user : [id=%s][role=%s]' % (self.id, self.role)


    @property
    def is_forbidden(self):
        return self.forbidden

    @property
    def is_admin(self):
        return self.role == RoleCode.OPERATOR

    @property
    def is_customer(self):
        return self.role == RoleCode.CONSUMER





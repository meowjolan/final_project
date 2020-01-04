# -*- encoding: utf-8 -*-
"""
@File    : Database.py.py
@Time    : 1/1/20 2:42 PM
@Author  : Guo Junnan
@Email   : 529931457@qq.com
@Software: PyCharm
"""

import mysql.connector
from datetime import datetime


class Database:
    def __init__(self):
        """
        初始化函数，建立数据库连接
        """
        self.config = {
            'host': '106.54.238.149',
            'user': 'Database2019',
            'password': 'Database2019',
            'db': 'MyZone'
        }

        self.con = mysql.connector.connect(**self.config)
        self.cur = self.con.cursor()


    def __del__(self):
        """
        销毁函数
        :return:
        """
        self.con.close()


    def get_user_by_id(self, id):
        """
        根据ID获取用户信息
        :param id: 用户名ID
        :return: (id, username, password, description)
        """
        query = '''
        select *
        from user 
        where id = {:10}
        '''.format(id)

        self.cur.execute(query)
        result = self.cur.fetchall()

        if result:
            return result[0]


    def get_max_id(self, table_name):
        """
        获取表中最大的id值
        :param table_name: 表名
        :return: max_id: 整数值，最大id值
        """
        query = """
        select max(id)
        from {}
        """.format(table_name)

        self.cur.execute(query)
        max_id = self.cur.fetchall()

        if max_id[0][0]:
            return int(max_id[0][0])
        else:
            return 0


    def add_user(self, username, password):
        """
        添加新用户
        :param username: 用户名
        :param password: 密码
        :return: 新用户的ID，整数
        """
        query = '''
        insert into user
        values ('{:10}', '{}', '{}', '{}')
        '''.format(self.get_max_id("user")+1, username, password,
                   "Cool guys! Write Nothing about thr introduction.")

        self.cur.execute(query)
        self.con.commit()

        return self.get_max_id("user")


    def validate_login(self, username, password):
        """
        用户登录验证
        :param username: 用户名
        :param password: 密码
        :return: 匹配的用户信息
        """
        query = '''
        select * 
        from user
        where name = \'{}\' and password = \'{}\'
        '''.format(username, password)

        self.cur.execute(query)
        result = self.cur.fetchall()

        if result:
            return result[0]


    def check_if_username_exist(self, username):
        """
        检查用户名是否存在
        :param username: 用户名
        :return: bool
        """
        query = '''
        select * 
        from user
        where name = '{}'
        '''.format(username)

        self.cur.execute(query)
        result = self.cur.fetchall()

        if result:
            return True
        else:
            return False


    def get_friends_info_by_id(self, user_id):
        """
        根据用户ID获取好友信息
        :param user_id: 用户ID
        :return: 信息元组列表
        """
        query = '''
        select *
        from user
        where id in (select friend_id
            from friend
            where id='{:10}')
        '''.format(user_id)

        self.cur.execute(query)
        result = self.cur.fetchall()

        return result


    def add_article(self, title, text, authority):
        """
        添加一篇文章
        :param title: 标题
        :param text: 正文
        :param authority: 权限
        :return: id: 文章id
        """
        id = self.get_max_id('article')+1
        time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        query = '''
        insert into article
        values ('{:10}', \'{}\', \'{}\', '{}', '{}')
        '''.format(id, title.replace('\'', '\\\''), text.replace('\'', '\\\''), time, authority)

        self.cur.execute(query)
        self.con.commit()

        return id


    def add_tag(self, tag_name):
        """
        添加tag，并返回对应id
        :param tag_name: 标签名
        :return: tag_id: 标签id
        """
        query = '''
        select id
        from tag
        where text = \'{}\'
        '''.format(tag_name)

        self.cur.execute(query)
        result = self.cur.fetchall()

        if result:
            # 已存在
            return result[0][0]
        else:
            # 添加标签
            tag_id = self.get_max_id('tag')+1

            query = '''
            insert into tag
            values (\'{:10}\', \'{}\')
            '''.format(tag_id, tag_name)

            self.cur.execute(query)
            self.con.commit()

            return tag_id


    def add_tag_article_id(self, article_id, tag_id):
        """
        添加文章和标签的映射
        :param article_id: 文章ID
        :param tag_id: 标签ID
        :return:
        """
        query = '''
        select *
        from arti_tag
        where arti_id = \'{:10}\' and tag_id = \'{:10}\'
        '''.format(article_id, tag_id)

        self.cur.execute(query)
        result = self.cur.fetchall()

        if not result:
            new_id = self.get_max_id('arti_tag') + 1
            query = '''
            insert into arti_tag
            values (\'{:10}\', \'{:10}\', \'{:10}\')
            '''.format(new_id, article_id, tag_id)

            self.cur.execute(query)
            self.con.commit()


    def add_user_article_id(self, article_id, user_id):
        """
        添加文章和作者的映射
        :param article_id: 文章ID
        :param user_id: 用户ID
        :return:
        """
        query = '''
        insert into arti_editor
        values (\'{:10}\', \'{:10}\')
        '''.format(article_id, user_id)

        self.cur.execute(query)
        self.con.commit()


    def get_article_by_id(self, article_id):
        """
        根据文章ID获取文章信息
        :param article_id: 文章ID
        :return: 信息元组
        """
        query = '''
        select article.id, article.title, article.text, article.time, article.authority, user.id, user.name
        from article, user, arti_editor
        where article.id = arti_editor.arti_id and 
            user.id = arti_editor.user_id and
            article.id = \'{:10}\'
        '''.format(article_id)

        self.cur.execute(query)
        result = self.cur.fetchone()

        return result


    def get_tag_name_by_article_id(self, article_id):
        """
        根据文章id获取相关标签列表
        :param article_id: 文章ID
        :return: 标签名字列表
        """
        query = '''
        select text
        from tag
        where id in (select tag_id
            from arti_tag
            where arti_id = \'{:10}\')
        '''.format(article_id)

        self.cur.execute(query)
        result = self.cur.fetchall()

        return [i[0] for i in result]


    def get_comment_by_article_id(self, article_id):
        """
        根据文章id获取相关评论
        :param article_id: 文章ID
        :return: 评论列表
        """
        query = '''
        select comment.id, comment.text, comment.time, user.id, user.name
        from comment, user, com_editor
        where comment.id = com_editor.com_id and 
            user.id = com_editor.user_id and
            comment.id in (select com_id
                from arti_com
                where arti_id = \'{:10}\')
        '''.format(article_id)

        self.cur.execute(query)
        result = self.cur.fetchall()

        return result


    def get_article_by_user_id(self, user_id):
        """
        根据用户ID获取相关文章
        :param user_id: 用户ID
        :return: 文章信息列表
        """
        query = """
        select *
        from article
        where id in (select arti_id
            from arti_editor
            where user_id = '{:10}')
        """.format(user_id)

        self.cur.execute(query)
        result = self.cur.fetchall()

        return result


    def add_comment(self, text):
        """
        添加评论
        :param text: 评论内容
        :return: id: 返回对应ID
        """
        id = self.get_max_id('comment')+1
        time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        query = '''
        insert into comment
        values ('{:10}', '{}', '{}')
        '''.format(id, text.replace('\'', '\\\''), time)

        self.cur.execute(query)
        self.con.commit()

        return id


    def add_comment_user_id(self, com_id, user_id):
        """
        添加评论和作者的映射
        :param com_id: 评论id
        :param user_id: 用户id
        :return:
        """
        query = '''
        insert into com_editor
        values ('{:10}', '{:10}')
        '''.format(com_id, user_id)

        self.cur.execute(query)
        self.con.commit()


    def add_article_comment_id(self, com_id, arti_id):
        """
        添加文章和评论的映射
        :param com_id: 评论ID
        :param arti_id: 文章ID
        :return:
        """
        query = '''
                insert into arti_com
                values ('{:10}', '{:10}')
                '''.format(com_id, arti_id)

        self.cur.execute(query)
        self.con.commit()


if __name__ == '__main__':
    # 测试数据库是否可以连接
    db = Database()
    db.add_user('manual', '123')
    print(db.get_user_by_id('2'))

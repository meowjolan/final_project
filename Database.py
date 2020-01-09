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

    def get_article_info(self):
        query = '''
        select *
        from tag
        '''
        self.cur.execute(query)
        result = self.cur.fetchall()
        if result:
            return result

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

    def add_user(self, username, password, introduction):
        """
        添加新用户
        :param username: 用户名
        :param password: 密码
        :return: 新用户的ID，整数
        """
        query = '''
        insert into user
        values ('{:10}', '{}', '{}', '{}')
        '''.format(self.get_max_id("user") + 1, username, password,
                   introduction)
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
        id = self.get_max_id('article') + 1
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
            tag_id = self.get_max_id('tag') + 1

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
        id = self.get_max_id('comment') + 1
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


    def get_article_tag_name(self,tag_name):
        query = """
        select article.id, article.title, article.text, article.time, article.authority
        from article,arti_tag,tag
        where tag.text = \'{:10}\' and
                arti_tag.tag_id = tag.id and
                arti_tag.arti_id = article.id
        """.format(tag_name)

        self.cur.execute(query)
        result = self.cur.fetchall()

        return result

    # contributed by Fengdp

    def add_moment(self, text, authority):
        """
        添加一篇朋友圈
        :param text: 正文
        :param authority: 权限
        :return: id: 文章id
        """
        id = self.get_max_id('moment') + 1
        time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        query = '''
        insert into moment
        values ('{:10}', \'{}\', '{}', '{}')
        '''.format(id, text.replace('\'', '\\\''), time, authority)

        self.cur.execute(query)
        self.con.commit()
        return id

    def add_tag_moment_id(self, moment_id, tag_id):
        """
        添加朋友圈和标签的映射
        :param moment_id: 朋友圈ID
        :param tag_id: 标签ID
        :return:
        """
        query = '''
        select *
        from mom_tag
        where mom_id = \'{:10}\' and tag_id = \'{:10}\'
        '''.format(moment_id, tag_id)

        self.cur.execute(query)
        result = self.cur.fetchall()

        if not result:
            new_id = self.get_max_id('mom_tag') + 1
            query = '''
            insert into mom_tag
            values (\'{:10}\', \'{:10}\', \'{:10}\')
            '''.format(new_id, moment_id, tag_id)

            self.cur.execute(query)
            self.con.commit()

    def add_user_moment_id(self, moment_id, user_id):
        """
        添加朋友圈和作者的映射
        :param moment_id: 朋友圈ID
        :param user_id: 用户ID
        :return:
        """
        query = '''
        insert into mom_editor
        values (\'{:10}\', \'{:10}\')
        '''.format(moment_id, user_id)

        self.cur.execute(query)
        self.con.commit()

    def get_moment_by_id(self, moment_id):
        """
        根据朋友圈ID获取朋友圈信息
        :param moment_id: 朋友圈ID
        :return: 信息元组
        """
        query = '''
        select moment.id, moment.text, moment.time, moment.authority, user.id, user.name
        from moment, user, mom_editor
        where moment.id = mom_editor.mom_id and 
            user.id = mom_editor.user_id and
            moment.id = \'{:10}\'
        '''.format(moment_id)

        self.cur.execute(query)
        result = self.cur.fetchone()

        return result

    def get_tag_name_by_moment_id(self, moment_id):
        """
        根据文章id获取相关标签列表
        :param moment_id: 文章ID
        :return: 标签名字列表
        """
        query = '''
        select text
        from tag
        where id in (select tag_id
            from mom_tag
            where mom_id = \'{:10}\')
        '''.format(moment_id)

        self.cur.execute(query)
        result = self.cur.fetchall()

        return [i[0] for i in result]

    def get_message_by_moment_id(self, moment_id):
        """
        根据文章id获取相关评论
        :param moment_id: 文章ID
        :return: 评论列表
        """
        query = '''
        select message.id, message.text, message.time, user.id, user.name
        from message, user, mess_editor
        where message.id = mess_editor.mess_id and 
            user.id = mess_editor.user_id and
            message.id in (select mess_id
                from mom_mess
                where mom_id = \'{:10}\')
        '''.format(moment_id)

        self.cur.execute(query)
        result = self.cur.fetchall()

        return result

    def get_moment_by_user_id(self, user_id):
        """
        根据用户ID获取相关文章
        :param user_id: 用户ID
        :return: 文章信息列表
        """
        query = """
        select *
        from moment
        where id in (select mom_id
            from mom_editor
            where user_id = '{:10}')
        """.format(user_id)

        self.cur.execute(query)
        result = self.cur.fetchall()

        return result

    def add_message(self, text):
        """
        添加评论
        :param text: 评论内容
        :return: id: 返回对应ID
        """
        id = self.get_max_id('message') + 1
        time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        query = '''
        insert into message
        values ('{:10}', '{}', '{}')
        '''.format(id, text.replace('\'', '\\\''), time)

        self.cur.execute(query)
        self.con.commit()

        return id

    def add_message_user_id(self, mess_id, user_id):
        """
        添加评论和作者的映射
        :param mess_id: 评论id
        :param user_id: 用户id
        :return:
        """
        query = '''
        insert into mess_editor
        values ('{:10}', '{:10}')
        '''.format(mess_id, user_id)

        self.cur.execute(query)
        self.con.commit()

    def add_moment_message_id(self, mess_id, mom_id):
        """
        添加文章和评论的映射
        :param mess_id: 评论ID
        :param mom_id: 文章ID
        :return:
        """
        query = '''
                insert into mom_mess
                values ('{:10}', '{:10}')
                '''.format(mess_id, mom_id)

        self.cur.execute(query)
        self.con.commit()

    def get_latest_article(self,user_id):
        """
         获取最近更新的一篇文章
         :return: 最近的一篇文章
        """
        query = '''
         select article.id, article.title, article.text, article.time, article.authority
         from article,arti_editor
         where article.id = arti_editor.arti_id and 
            arti_editor.user_id = user_id and 
            time >= all (select time
                from  article
                where arti_editor.user_id = {:10} and
                        arti_editor.arti_id = article.id)
         '''.format(user_id)

        self.cur.execute(query)
        result = self.cur.fetchall()

        return result[0]

    def get_latest_moment(self,user_id):
        """
         获取最近更新的一篇朋友圈
         :return: 最近的一篇朋友圈
        """
        query = '''
         select moment.id,moment.text, moment.time,moment.authority
         from moment,mom_editor
         where moment.id = mom_editor.mom_id and
            mom_editor.user_id = user_id and
            moment.time >= all (select time
                                from  moment,mom_editor
                                where moment.id = mom_editor.mom_id and
                                    mom_editor.user_id = {:10})
         '''.format(user_id)

        self.cur.execute(query)
        result = self.cur.fetchall()

        return result[0]

    def get_all_user_info(self):
        """
         获取所有用户信息
         :return: 所有用户信息
        """
        query = '''
         select user.id,user.name, user.password,user.introduction
         from user
         '''

        self.cur.execute(query)
        result = self.cur.fetchall()

        return result



if __name__ == '__main__':
    # 测试数据库是否可以连接
    db = Database()
    # db.update_db()
    for i in db.get_all_user_info():
        print(i)


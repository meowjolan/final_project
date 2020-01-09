from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, IntegerField
from wtforms.validators import DataRequired, Length, EqualTo, NumberRange


class LoginForm(FlaskForm):
    username = StringField('Username',
                           validators=[
                                DataRequired(message='Username must have 1-50 characters!'),
                                Length(1, 50, message='Username must have 1-50 characters!')
                           ],
                           render_kw={'placeholder': 'Username'})
    password = PasswordField('Password',
                             validators=[
                                 DataRequired(message='Password must have 1-50 characters!'),
                                 Length(1, 50, message='Password must have 1-50 characters!')
                             ],
                             render_kw={'placeholder': 'Password'}
                             )
    login = SubmitField('Login')


class RegisterForm(FlaskForm):
    username = StringField('Username',
                           validators=[
                                DataRequired(message='Username must have 1-50 characters!'),
                                Length(1, 50, message='Username must have 1-50 characters!')
                           ],
                           render_kw={'placeholder': 'Username'}
                           )
    password = PasswordField('Password',
                             validators=[
                                 DataRequired(message='Password must have 1-50 characters!'),
                                 Length(1, 50, message='Password must have 1-50 characters!')
                             ],
                             render_kw={'placeholder': 'Password'}
                             )
    repeat_password = PasswordField('Repeat Password',
                                    validators=[
                                        DataRequired(message='Password must have 1-50 characters!'),
                                        EqualTo('password', message='Passwords must match!'),
                                    ],
                                    render_kw={'placeholder': 'Password'}
                                    )
    introduction = TextAreaField('Introduction',
                         validators=[
                             DataRequired(message='Text cannot be empty!'),
                             Length(1, 500, message='The length of text cannot exceed 500!')
                         ],
                         render_kw={'placeholder': 'introduction'})

    register = SubmitField('Register')


class ArticleForm(FlaskForm):
    title = TextAreaField('title',
                          validators=[
                              DataRequired(message='Title cannot be empty!'),
                              Length(1, 100, message='The length of title cannot exceed 100!')
                          ],
                          render_kw={'placeholder': 'Title'})
    text = TextAreaField('text',
                         validators=[
                             DataRequired(message='Text cannot be empty!'),
                             Length(1, 10000, message='The length of text cannot exceed 10000!')
                         ],
                         render_kw={'placeholder': 'Text'})
    authority = TextAreaField('authority',
                              validators=[
                                  DataRequired(message='Authority cannot be empty!')
                              ])
    submit = SubmitField('Submit')


class CommentForm(FlaskForm):
    text = TextAreaField('text',
                         validators=[
                             DataRequired(message='Text cannot be empty!'),
                             Length(1, 400, message='The length of text cannot exceed 400!')
                         ],
                         render_kw={'placeholder': 'Text'})
    submit = SubmitField('Submit')


class MomentForm(FlaskForm):
    text = TextAreaField('text',
                         validators=[
                             DataRequired(message='Text cannot be empty!'),
                             Length(1, 10000, message='The length of text cannot exceed 10000!')
                         ],
                         render_kw={'placeholder': 'Text'})
    authority = TextAreaField('authority',
                              validators=[
                                  DataRequired(message='Authority cannot be empty!')
                              ])
    submit = SubmitField('Submit')


class MessageForm(FlaskForm):
    text = TextAreaField('text',
                         validators=[
                             DataRequired(message='Text cannot be empty!'),
                             Length(1, 400, message='The length of text cannot exceed 400!')
                         ],
                         render_kw={'placeholder': 'Text'})
    submit = SubmitField('Submit')


class SearchForm(FlaskForm):
    tag_name = StringField('Tag Name',
                            validators=[
                                DataRequired(message='It can\' be empty!'),
                                Length(1, 64)
                            ],
                            render_kw={'placeholder': 'Enter Tag Name...'}
                            )
    submit = SubmitField('Search')
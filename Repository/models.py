from django.db import models
from django.contrib.auth.models import User


class Weibo(models.Model):
    """所有微博"""

    wb_type_choices = (
        (0, 'new'),  # 新建
        (1, 'forward'),  # 转发
        (2, 'collect'),  # 收藏
    )
    wb_type = models.IntegerField(choices=wb_type_choices, default=0)  # 类型
    # 自关连,转发或新建
    forward_or_collect_from = models.ForeignKey('self', related_name="forward_or_collects", blank=True, null=True)

    user = models.ForeignKey('UserProfile')  # 所属用户

    text = models.CharField(max_length=140)  # 内容

    pictures_link_id = models.CharField(max_length=128, blank=True, null=True)  # 图片 blank admin可空 null数据字段可空

    video_link_id = models.CharField(max_length=128, blank=True, null=True)  # 视频

    perm_choice = ((0, 'public'),  # 公开
                   (1, 'private'),  # 朋友圈
                   (2, 'friends'))  # 粉丝
    perm = models.IntegerField(choices=perm_choice, default=0)  # 访问类型

    date = models.DateTimeField(auto_now_add=True)  # 时间

    def __str__(self):
        return self.text


class Topic(models.Model):
    """话题"""
    name = models.CharField(max_length=140)
    date = models.DateTimeField()

    def __str__(self):
        return self.name


class Category(models.Model):
    """微博分类"""

    name = models.CharField(max_length=32)

    def __str__(self):
        return self.name


class Comment(models.Model):
    """评论"""
    to_weibo = models.ForeignKey(Weibo)  # 评论哪一条微博

    p_comment = models.ForeignKey('self', related_name="child_comments", blank=True, null=True)  # 评论的哪一条评论

    user = models.ForeignKey('UserProfile')  # 用户

    comment_type_choices = ((0, 'comment'), (1, 'thumb_up'))  # 评论 类型 选择(0 评论, 1 点赞)

    comment_type = models.IntegerField(choices=comment_type_choices, default=0)  # 评论类型

    comment = models.CharField(max_length=140, blank=True, null=True)  # 评论

    date = models.DateTimeField(auto_created=True)

    def __str__(self):
        return self.comment


class Tags(models.Model):
    """标签"""
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    """用户信息"""

    user = models.OneToOneField(User)

    name = models.CharField(max_length=64)

    brief = models.CharField(max_length=140, blank=True, null=True)  # 简介

    sex_type = ((1, 'Male'), (0, 'Female'))
    sex = models.IntegerField(choices=sex_type, default=1)

    age = models.PositiveSmallIntegerField(blank=True, null=True)

    email = models.EmailField()

    tags = models.ManyToManyField(Tags)  # 标签

    head_img = models.ImageField()  # 头像

    follow_list = models.ManyToManyField('self', blank=True, related_name="my_followers", symmetrical=False)

    # registration_date = models.DateTimeField(auto_created=True)
    def __str__(self):
        return self.name

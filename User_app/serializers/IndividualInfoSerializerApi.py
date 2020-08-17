# -*- coding: utf-8 -*-
# @Time  : 2020/8/4 下午9:00
# @Author : 司云中
# @File : IndividualInfoSerializerApi.py
# @Software: Pycharm
from django.contrib.auth.models import User
from django.db import transaction, DataError, DatabaseError
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from User_app.models.user_models import Consumer
from User_app.validators import DRFUsernameValidator
from User_app.views.ali_card_ocr import Interface_identify
from e_mall.loggings import Logging

common_logger = Logging.logger('django')


class IndividualInfoSerializer(serializers.ModelSerializer):
    """个人信息序列化器"""

    # 覆盖model中的字段效果
    username = serializers.CharField(max_length=30,
                                     validators=[DRFUsernameValidator(), UniqueValidator(queryset=User.objects.all())])

    phone = serializers.CharField(max_length=11, source='consumer.phone', read_only=True)
    head_image = serializers.CharField(source='consumer.head_image', read_only=True)
    birthday = serializers.DateField(source='consumer.birthday', read_only=True)
    sex = serializers.CharField(source='consumer.get_sex_display', read_only=True)
    rank = serializers.CharField(source='consumer.get_rank_display', read_only=True)
    safety = serializers.IntegerField(source='consumer.safety', read_only=True)

    class Meta:
        model = User
        fields = ['username', 'phone', 'first_name', 'head_image', 'birthday', 'sex', 'rank', 'safety', 'last_login']
        # 继承ModelSerializer后，上面定义的自定义字段要显示使用read_only，不能放到read_only_fields中，没有效果
        read_only_fields = ['username', 'phone', 'head_image', 'birthday', 'sex', 'rank', 'groups']


class HeadImageSerializer(serializers.Serializer):
    """头像修改序列化器"""

    head_image = serializers.ImageField(write_only=True)

    @staticmethod
    def _upload(validated_data, storage):
        """上传用户新的头像"""
        head_image = validated_data.get('head_image')
        is_upload, file_information = storage.upload(filebuffer=head_image.read())  # 调用client进行文件上传
        return is_upload, file_information

    @staticmethod
    def _update(validated_data, remote_file_id, storage):
        """
        存在问题！！！
        更新用户头像，
        在用户保存头像后
        """
        head_image = validated_data.get('head_image')
        is_update, file_information = storage.update(bytes(head_image.read()), remote_file_id)
        return is_update

    def update_head_image(self, instance, validated_data, storage):
        """同步服务器和数据库的头像"""
        try:
            old_head_image = instance.head_image
            is_upload, file_information = self._upload(validated_data, storage)
            if not is_upload:
                return False
            file_id = file_information.get('Remote file_id').decode()
            instance.head_image = file_id
            instance.save(update_fields=['head_image', ])
        except Exception as e:
            common_logger.info(e)
            return False
        else:
            is_delete = storage.delete(old_head_image) if old_head_image else True  # 如果服务器上有就头像，就删除。
            return True if all([is_upload, is_delete]) else False  # 只有上传+修改+删除（可选）都成功后才返回True
        # return self._update(validated_data, 'group1/M00/00/00/wKgAaV85MnSAKwl7AA543lGjCZc0505542', storage)


class VerifyIdCardSerializer(serializers.ModelSerializer):
    """身份认证序列化器"""

    face = serializers.ImageField(max_length=50, allow_empty_file=False)  # 身份证前照
    back = serializers.ImageField(max_length=50, allow_empty_file=False)  # 身份正后照片

    def validate(self, attrs):
        """
        OCR识别身份正反
        验证阶段验证身份信息是否正确或是否已被验证
        """
        if self.context.get('request').user.first_name != '':
            raise serializers.ValidationError('身份已被认证过！')
        identify_instance_face = Interface_identify(attrs.get('face'), 'face')
        identify_instance_back = Interface_identify(attrs.get('back'), 'back')
        is_success = identify_instance_face.is_success and identify_instance_back.is_success  # 检查身份验证是否全部正确
        if is_success:
            OCR_attrs = {
                'first_name': identify_instance_face.get_detail('actual_name'),
                'sex': identify_instance_face.get_detail('sex'),
                'birthday': identify_instance_face.get_detail('birth'),
                'nationality': identify_instance_face.get_detail('nationality')
            }
            if User.objects.filter(first_name=identify_instance_face.get_detail('actual_name')).count() == 1:
                raise serializers.ValidationError('身份证已被认证过！')
            else:
                attrs.update(OCR_attrs)
                return attrs
        raise serializers.ValidationError('身份校验异常')

    def update(self, instance, validated_data):
        """更新身份信息"""
        first_name = validated_data.pop('first_name')  # 弹出first_name
        try:
            instance.user.first_name = first_name  # 更新user
            for key, value in validated_data.items():  # 更新Consumer
                setattr(instance, key, value)
            instance.user.save()
            instance.save()
        except Exception as e:
            common_logger.info(e)
            raise None
        else:
            return instance

    class Meta:
        model = User
        fields = ('first_name', 'face', 'back')
        read_only_fields = ('first_name',)

# -*- coding: utf-8 -*-
# @Time : 2020/5/25 19:43
# @Author : 司云中
# @File : order.py
# @Software: PyCharm

from Order_app.serializers.OrderSerializerApi import OrderBasicSerializer, PageSerializer, Page, \
    OrderCommoditySerializer, OrderAddressSerializer
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from e_mall.loggings import Logging
from e_mall.response_code import response_code
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

common_logger = Logging.logger('django')

order_logger = Logging.logger('order_')


class OrderBasicOperation(APIView):
    """订单基本浏览删除操作"""

    serializer_class = OrderBasicSerializer

    ultimate_class = PageSerializer

    page_class = Page

    # renderer_classes = [TemplateHTMLRenderer]  # django’s standard template rendering

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class
        return serializer_class(*args, **kwargs)

    def get_ultimate_serializer(self, *args, **kwargs):
        serializer_class = self.get_ultimate_serializer_class
        return serializer_class(*args, **kwargs)

    @property
    def get_serializer_class(self):
        return self.serializer_class

    @property
    def get_ultimate_serializer_class(self):
        return self.ultimate_class

    def get_order_and_page(self, user, **data):
        """获取某用户订单实例和总页大小"""
        return self.get_serializer_class().get_order_and_page(user, **data)

    @method_decorator(login_required(login_url='/consumer/login/'))
    def get(self, request):
        """获取该用户最近的订单"""
        user = request.user
        data = request.GET
        instances, pages = self.get_order_and_page(user, **data)
        page = Page(page=pages)
        serializer = self.get_ultimate_serializer(page, context={'serializer': self.get_serializer_class,
                                                                 'instances': instances})
        return Response(serializer.data)

    @method_decorator(login_required(login_url='/consumer/login/'))
    def post(self, request):
        """产生订单"""
        user = request.user
        data = request.data

    @method_decorator(login_required(login_url='/consumer/login/'))
    def delete(self, request):
        """删除订单"""
        data = request.data
        # 单删
        is_success = self.get_serializer_class().delete_order(**data)

        # 群删
        if is_success:
            return Response(response_code.delete_order_success)
        else:
            return Response(response_code.delete_address_error)


class OrderBuyNow(APIView):
    """订单跳转暂存操作"""
    serializer_address_class = OrderAddressSerializer
    serializer_commodity_class = OrderCommoditySerializer

    # renderer_classes = [TemplateHTMLRenderer]  # django’s standard template rendering

    @property
    def get_serializer_address_class(self):
        # 地址序列化类
        return self.serializer_address_class

    @property
    def get_serializer_commodity_class(self):
        # 商品序列化类
        return self.serializer_commodity_class

    @method_decorator(login_required(login_url='/consumer/login/'))
    def post(self, request):
        """
        session做中间件用于暂存交易商品基本信息（不包括money)
        解决ajax禁止定向的问题
        """

        # data = json.loads(request.body.decode('utf-8'))  # 解码 + 反序列化
        data = request.data
        try:
            request.session['commodity_list'] = data['commodity_list']
            request.session['counts_list'] = data['counts_list']
            common_logger.info(request.session['commodity_list'])
            common_logger.info(request.session['counts_list'])
            return Response({'code': 666})
        except Exception as e:
            order_logger.error(e)
            return Response({'code': -666})


class OrderCommitOperation(APIView):
    """生成初始订单操作"""

    serializer_commodity_class = OrderCommoditySerializer

    @property
    def get_serializer_class(self):
        return self.serializer_commodity_class

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class
        return serializer_class(*args, **kwargs)

    @staticmethod
    def context(request):
        """deliver extra parameters"""
        commodity_list = request.session['commodity_list']
        counts_list = request.session['counts_list']
        result = {}
        for commodity, counts in zip(commodity_list, counts_list):
            result[commodity] = counts
        return result

    @method_decorator(login_required(login_url='/consumer/login/'))
    def get(self, request):
        """get the commodity which consumer intend to buy"""
        # 序列化用户订单生成页获取商品信息
        try:
            commodity_list = request.session['commodity_list']
            instances = self.get_serializer_class.get_commodity(commodity_list)
            serializer = self.get_serializer(instances, context=self.context(request), many=True)
            return Response(serializer.data)
        except Exception as e:
            order_logger.error(e)
            return Response(None)

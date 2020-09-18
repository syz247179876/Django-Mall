"""
Django settings for e_mall project.

Generated by 'django-admin startproject' using Django 2.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""
import os
import datetime

# from django.conf.global_settings import EMAIL_HOST_USER

# Build paths inside the project like this: ostatistic_user_mouths.path.join(BASE_DIR, ...)
from celery.schedules import crontab

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'ruu2)x=u+^l3mx27$(9)q1sk)(55t1csx%41-90nt%w8dw_(&i'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'simpleui',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    # 'Remark_app',
    'Remark_app.apps.RemarkConfig',
    'Voucher_app.apps.VoucherAppConfig',
    'Shop_app',
    'Shopper_app',
    'User_app',
    'Order_app',
    'rest_framework',
    'mdeditor',
    'rest_framework_swagger',
    'mainsite',
    'Search_app',
    'Analysis_app',
    'Payment_app',
    # 'Analysis_app.apps.AnalysisAppConfig',      # 行为分析,这种方式注册app信号可能注册失败
    'haystack',
    'CommonModule_app'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

SITE_ID = 1

# 项目根路由
ROOT_URLCONF = 'e_mall.urls'

# django-rest-framework的配置
REST_FRAMEWORK = {
    # 接口框架实例，coreapi.Document的instance,swagger的
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.AutoSchema',
    # 全局添加jwt认证方式,所有视图请求都会调用该验证方法，对token进行认证，反解出生成user对象，赋给request.user
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
    ],
    'DEFAULT_THROTTLE_CLASSES': [  # 限流类
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ],
    'DEFAULT_THROTTLE_RATES': {  # 限流频率，利用redis存储
        'anon': '100/day',
        'user': '1000/day'
    },
    # 'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    # 'PAGE_SIZE': 50
}

JWT_AUTH = {
    # 配置jwt的过期时间,24小时存活周期
    'JWT_EXPIRATION_DELTA': datetime.timedelta(days=1),
    # 是否可以刷新
    'JWT_ALLOW_REFRESH': True,
    # 刷新的过期时间
    'JWT_REFRESH_EXPIRATION_DELTA': datetime.timedelta(days=7),
    # 是否添加到cookie中
    'JWT_AUTH_COOKIE': 'JwtToken',
}

HAYSTACK_CONNECTIONS = {
    # elasticSearch实现搜索引擎，不走DRF，直接请求索引库
    'default': {
        'ENGINE': 'haystack.backends.elasticsearch_backend.ElasticsearchSearchEngine',
        'URL': 'http://192.168.0.105:9200/',  # 此处为elasticsearch运行的服务器ip地址，端口号固定为9200
        'INDEX_NAME': 'shop',  # 指定elasticsearch建立的索引库的名称
    },
    # # whoosh搜索引擎的配置
    # 'default': {
    #     # 指定使用的搜索引擎
    #     'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
    #     # 指定索引文件存放位置
    #     'PATH': os.path.join(BASE_DIR, 'whoosh_index'),
    # }
}

# 新增的数据自动生成索引
HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'

# 设置每页显示的数目，默认为20，可以自己修改
HAYSTACK_SEARCH_RESULTS_PER_PAGE = 100

# the config of swagger doc

SWAGGER_SETTINGS = {
    # base style
    'SECURITY_DEFINITIONS': {
        "basic": {
            'type': 'basic'
        }
    },
    # 如果需要登录才能够查看接口文档, 登录的链接使用restframework自带的.
    # 'LOGIN_URL': 'rest_framework:login',
    # 'LOGOUT_URL': 'rest_framework:logout',
    # 'DOC_EXPANSION': None,
    # 'SHOW_REQUEST_HEADERS':True,
    # 'USE_SESSION_AUTH': True,
    # 'DOC_EXPANSION': 'list',
    # 接口文档中方法列表以首字母升序排列
    'APIS_SORTER': 'alpha',
    # 如果支持json提交, 则接口文档中包含json输入框
    'JSON_EDITOR': True,
    # 方法列表字母排序
    'OPERATIONS_SORTER': 'alpha',
    'VALIDATOR_URL': None,
}

# 重写后端认证类，所有的认证方法都会使用它,如果一个认证类失败
AUTHENTICATION_BACKENDS = ['e_mall.authentication_consumer.EmailOrUsername', 'e_mall.authentication_consumer.Phone']

# AUTH_USER_MODEL = 'Manager_app.Manager_user'

# 加密算法，默认取第一个
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
    'django.contrib.auth.hashers.BCryptPasswordHasher',
    'django.contrib.auth.hashers.SHA1PasswordHasher',
    'django.contrib.auth.hashers.MD5PasswordHasher',
    'django.contrib.auth.hashers.CryptPasswordHasher',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        # 'DIRS': ['vue_e_mall/dist'],  # 该目录是vue项目的名称
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'e_mall.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

# 数据库
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'e_mall_db',  # 数据库名
        'HOST': '127.0.0.1',
        'PORT': '3306',
        'USER': 'root',
        'PASSWORD': '123456'
    }
}

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

# 语言
LANGUAGES = [
    ('zh-Hans', 'Chinese'),
    ('en-us', 'English')
]

# 编码
LANGUAGE_CODE = 'zh-Hans'
# LANGUAGES_CODE = 'en-us'
# 时区
TIME_ZONE = 'Asia/Shanghai'

# 本地翻译文件路径
LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)
# 国际化
USE_I18N = True

# 本地化
USE_L10N = False

USE_TZ = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

# 静态文件路由
STATIC_URL = '/static/'

# 静态文件,用于没有uwsgi的时候
STATICFILES_DIRS = [
    # 替换反斜杠
    os.path.join(BASE_DIR, 'static').replace('\\', '/')
]

# STATIC_ROOT 用于部署时候将静态文件全部集中存放,根目录从盘区开始，所以尽量使用绝对路径
STATIC_ROOT = '/home/syz/E_mall/static/'

# celery 设置,用于实例化
# celery 中间人 redis://redis服务所在的ip地址:端口号/数据库号
BROKER_URL = 'redis://:123456@127.0.0.1:6379/0'
# BROKER_URL = [
#     'redis://192.168.0.105:6381/0',
#     'redis://192.168.0.105:6380/0',
#     'redis://192.168.0.105:6379/0'
# ]
# celery结果返回，可用于跟踪结果
CELERY_RESULT_BACKEND = 'redis://:123456@127.0.0.1:6379/1'
# CELERY_RESULT_BACKEND = ['redis://192.168.0.105:6381/1',
#                          'redis://192.168.0.105:6380/1',
#                          'redis://192.168.0.105:6379/1'
#                          ]

CELERY_TASK_SERIALIZER = 'json'

CELERY_RESULT_SERIALIZER = 'json'

# celery时区设置，使用settings中TIME_ZONE同样的时区
CELERY_TIME_ZONE = TIME_ZONE


CELERY_BEAT_SCHEDULE = {
    # 'every-day-statistic-login-times':{
    #     'task':'Anaylsis_app',
    #     'schedule':crontab(minute=0, hour=0)  # 每天0点执行
    # },
    'add-every-monday-morning':{
        'task': 'Analysis_app.tasks.statistic_login_times',
        'schedule': crontab(minute=0,hour=0),
        'args':(),
    },
    # 'add-every-monday-morning': {
    #     'task': 'Analysis_app.tasks.add',
    #     'schedule': 5.0,
    #     'args': (16, 16),
    # },

}

# 缓存
CACHES = {
    'redis':
        {
            'BACKEND': 'django_redis.cache.RedisCache',
            # 'LOCATION': 'redis://:123456@127.0.0.1:6379/2',
            'LOCATION': [
                'redis://192.168.0.105:6381/2',
                'redis://192.168.0.105:6380/2',
                'redis://192.168.0.105:6379/2'
            ],
            'OPTIONS': {
                'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            }
        },
    'analysis':    # 用于用户和商家行为分析
        {
            'BACKEND': 'django_redis.cache.RedisCache',
            # 'LOCATION': 'redis://:123456@127.0.0.1:6379/2',
            'LOCATION': [
                'redis://192.168.0.105:6381/3',
                'redis://192.168.0.105:6380/3',
                'redis://192.168.0.105:6379/3'
            ],
            'OPTIONS': {
                'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            }
        },
    'remark':    # 用于评论模块的缓存操作
        {
            'BACKEND': 'django_redis.cache.RedisCache',
            # 'LOCATION': 'redis://:123456@127.0.0.1:6379/2',
            'LOCATION': [
                'redis://192.168.0.105:6381/4',
                'redis://192.168.0.105:6380/4',
                'redis://192.168.0.105:6379/4'
            ],
            'OPTIONS': {
                'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            }
        },
    'default':
        {
            'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
            'LOCATION': '127.0.0.1:11211',
            'OPTIONS': {
                'server_max_value_length': 1024 * 1024 * 2,  # 支持对象的最大大小的容量
            }
        }
}

# 图片等媒体文件的url
MEDIA_URL = '/media/'  # 方便url使用的目录，与项目中的目录名不一样,同时也用于数据库存储的路径,要加上/来结尾

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')  # 用户上传的文件目录

# 重写User表

# AUTH_USER_MODEL = 'Shopper_app.Shoppers'

# 会话session设置
SESSION_ENGINE = 'django.contrib.sessions.backends.db'  # 引擎（默认）

# SESSION_ENGINE = 'django.contrib.sessions.backends.cache' # 使用redis存储session 

SESSION_COOKIE_NAME = "e_mall_sessionid"

# Session的cookie保存在浏览器上时的key，session根据此key来生成，如果不支持cookie，那么也就不支持session
# 浏览器关闭之后清除的是cookie所保存的服务器传下来的sessionid，而不是session，一旦请求头中的sessionid匹配不上服务器中的sessionid，则请求失败。
# 当session过期后，服务器才会传递一个新的session

SESSION_COOKIE_PATH = "/"  # Session的cookie保存的路径（默认）

SESSION_COOKIE_DOMAIN = None  # Session的cookie保存的域名（默认）

SESSION_COOKIE_SECURE = False  # 是否Https传输cookie（默认）

SESSION_COOKIE_HTTPONLY = True  # 是否Session的cookie只支持http传输（默认）

SESSION_COOKIE_AGE = 60 * 24 * 60  # Session的cookie失效日期（30min）（默认），和SESSION_EXPIRE_AT_BROWSER_CLOSE二选一

SESSION_EXPIRE_AT_BROWSER_CLOSE = True  # 是否关闭浏览器使得Session过期（默认）

SESSION_SAVE_EVERY_REQUEST = False  # 是否每次请求都保存Session，默认修改之后才保存

# 代理以及端口必须有
EMAIL_HOST = 'smtp.qq.com'  # 发送邮件的stmp服务器
EMAIL_PORT = 25  # stmp协议的端口号,本地使用

EMAIL_HOST_USER = '247179876@qq.com'  # 发送邮件的地址

# 本来填的自己的账号密码，但是不行的.
# EMAIL_HOST_PASSWORD =os.environ['PASSWORDD']

EMAIL_HOST_PASSWORD = 'mazstyfnbdbfbjhf'  # 发送邮件的授权码

# 这里的是前缀，也就是头
EMAIL_SUBJECT_PREFIX = u'[Sercheif]'

# TLS和SSL是互斥的
# TLS是安全传输层协议，是SSL3.0的升级版，它利用对称加密、公私钥不对称加密及其密钥交换算法，CA系统进行加密且可信任的信息传输
EMAIL_USE_TLS = True  # 是否使用TLS安全传输协议(用于在两个通信应用程序之间提供保密性和数据完整性。)
# SSLError [SSL：UNKNOWN_PROTOCOL] unknow如果出现，就将EMAIL_USE_SSL置为False

# SSL是安全套接层协议
# EMAIL_PORT = 465 搭配SSL
EMAIL_USE_SSL = False  # 使用安全ssl加密，qq企业邮箱要求使用

# 有这个就会显示是你的邮箱，别人收到的邮件中会有这个设定的名称

EMAIL_FROM = '拼夕夕商城<247179876@qq.com>'

X_FRAME_OPTIONS = 'SAMEORIGIN'

# 阿里云短信发送
ACCESS_KEY_ID = 'LTAI4GFNoVjYuDop2313wNYC'
ACCESS_KEY_SECRET = 'pKoWg1KrHvaHzMFQeIe3QtKNGovBdu'
REGION = 'cn-hangzhou'
SIGN_NAME = 'ACC商城'  # 短信签名

# 不同的短信模板
TEMPLATES_CODE_LOGIN = 'SMS_199795817'
TEMPLATES_CODE_REGISTER = 'SMS_199795814'
TEMPLATES_CODE_IDENTIFY = 'SMS_199805896'
TEMPLATES_CODE_MODIFY_PASSWORD = 'SMS_199805895'

# 阿里OCR的AppCode

ALI_APPCODE = '990dad198d304f8da8c0c599593f686c'

# 阿里OCR请求路径
ALI_OCR_URL = 'https://dm-51.data.aliyun.com/rest/160601/ocr/ocr_idcard.json'

# 异步网关协议应用
ASGI_APPLICATION = "e_mall.routing.application"
# 用于实现不同consumer间的通信，搭配redis作为存储后端
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": ['redis://:123456@127.0.0.1:6379/5'],
        },
    },
}

# 配置django文件存储为fdfs
DEFAULT_FILE_STORAGE = 'e_mall.storage.FastDFSStorage'

# FastDfs服务器地址
FDFS_URL = 'http://192.168.0.105:80'

# FastDfs的客户端路径
FDFS_CLIENT_CONF = '/etc/fdfs/client.conf'

# Home page address
SIMPLEUI_INDEX = '/'

# set the logo of backend
SIMPLEUI_LOGO = 'https://django-blog-syz.oss-cn-shanghai.aliyuncs.com/login.jpg'

# hide server information
SIMPLEUI_HOME_INFO = True

# default theme
SIMPLEUI_DEFAULT_THEME = 'layui.css'

# hide recent actions
SIMPLEUI_HOME_ACTION = True

# dir which storage the error file
BASE_DIR_LOG = os.path.join(BASE_DIR, 'Logs')

LOGGING = {
    'version': 1,  # the version fo logging system
    'disable_existing_loggers': True,  # forbid all loggers which already existed
    'formatters': {
        'verbose': {  # details, including levelname,asctime,moudle,funcName,process,thread,message
            'format': '%(levelname)s - %(asctime)s - %(module)s - %(funcName)s - %(process)d - %(thread)d - %(message)s',
        },
        'simple': {  # simple formatting
            'format': '%(levelname)s - %(funcName)s - %(message)s',
        },
        'sql': {
            'format': '%(asctime)s - %(message)s',
        }
    },
    'filters': {
        'require_debug_true': {  # write down when debug is True
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {  # handlers,this define three handler
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
        'consumer_handlers': {  # write the level error log into the error file
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'verbose',  # detail record
            'filename': os.path.join(BASE_DIR_LOG, 'consumer_error.log'),
            'maxBytes': 1024 * 1024 * 50,
            'backupCount': 3,  # number of backups
        },
        'shopper_handlers': {
            'level': 'ERROR',
            # 'filters': ['require_debug_true'],
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'verbose',
            'filename': os.path.join(BASE_DIR_LOG, 'shopper_error.log'),
            'maxBytes': 1024 * 1024 * 50,  # the most max value of number of each file
            'backupCount': 3,
        },
        'order_handlers': {
            'level': 'ERROR',
            # 'filters': ['require_debug_true'],
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'verbose',
            'filename': os.path.join(BASE_DIR_LOG, 'order_error.log'),
            'maxBytes': 1024 * 1024 * 50,
            'backupCount': 3,
        },
        'trolley_handlers': {
            'level': 'ERROR',
            # 'filters': ['require_debug_true'],
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'verbose',
            'filename': os.path.join(BASE_DIR_LOG, 'trolley_error.log'),
            'maxBytes': 1024 * 1024 * 50,
            'backupCount': 3,
        },
        'commodity_handlers': {
            'level': 'ERROR',
            # 'filters': ['require_debug_true'],
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'verbose',
            'filename': os.path.join(BASE_DIR_LOG, 'commodity_error.log'),
            'maxBytes': 1024 * 1024 * 50,
            'backupCount': 3,
        },
        'mainsite_handlers': {
            'level': 'ERROR',
            # 'filters': ['require_debug_true'],
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'verbose',
            'filename': os.path.join(BASE_DIR_LOG, 'mainsite_error.log'),
            'maxBytes': 1024 * 1024 * 50,
            'backupCount': 3,
        },
        'evaluate_handlers': {
            'level': 'ERROR',
            # 'filters': ['require_debug_true'],
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'verbose',
            'filename': os.path.join(BASE_DIR_LOG, 'evaluate_error.log'),
            'maxBytes': 1024 * 1024 * 50,
            'backupCount': 3,
        },
        'sql_console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'sql'
        }

    },
    'loggers': {  # define two recoder
        # default config of logger
        'django': {
            'handlers': ['console', ],
            'propagate': True,
            'level': 'INFO',
        },
        'consumer_': {
            'handlers': ['consumer_handlers', ],
            'propagate': False,  # whether transform to higher layer
            'level': 'ERROR',
        },
        'shopper_': {
            'handlers': ['shopper_handlers', ],
            'level': 'ERROR',
            'propagate': False,
        },
        'order_': {
            'handlers': ['order_handlers', ],
            'level': 'ERROR',
            'propagate': False,
        },
        'trolley_': {
            'handlers': ['trolley_handlers', ],
            'level': 'ERROR',
            'propagate': False,
        },
        'commodity_': {
            'handlers': ['commodity_handlers', ],
            'level': 'ERROR',
            'propagate': False,
        },
        'mainsite_': {
            'handlers': ['mainsite_handlers', ],
            'level': 'ERROR',
            'propagate': False,
        },
        'evaluate_': {
            'handlers': ['evaluate_handlers', ],
            'level': 'ERROR',
            'propagate': False,
        },
        # 'django.db.backends': {
        #     'handlers': ['sql_console', ],
        #     'propagate': True,
        #     'level': 'DEBUG',
        # },
    },
}

# 支付宝支付的配置
ALIPAY_APPID = '2021001165602567'

# windows,linux
APP_KEY_PUBLIC_PATH = os.path.join(BASE_DIR, 'Payment_app/keys/application_key_public.pem')

APP_KEY_PRIVATE_PATH = os.path.join(BASE_DIR, 'Payment_app/keys/application_key_private.pem')

ALIPAY_PUBLIC_KEY_PATH = os.path.join(BASE_DIR, 'Payment_app/keys/alipay_public.pem')

ALIPAY_DEBUG = True  # 使用沙箱环境
ALIPAY_SUBJECT = '吃货商城-订单支付'
ALIPAY_RETURN_URL = 'http://127.0.0.1:8000/payment/update-order-chsc-api/'
ALIPAY_GATE = 'https://openapi.alipaydev.com/gateway.do?'
ALIPAY_NOTIFY_URL = "http://127.0.0.1:8000/payment/payment-chsc-api/"

# print(os.path.join(BASE_DIR, 'Payment_app/keys/application_key.pem').replace('\\', '/'))
# create custom menu



# SIMPLEUI_CONFIG = {
#     'system_keep':False,
#     'menu_display':['订单管理','库存管理','卖家评论','信誉查看','店铺管理','商品管理','个人信息'],
#     'dynamic': False,
#     'menus': [{
#         'name': '订单管理',
#         'icon': 'fa fa-hand-peace-o',
#         'models': [{
#             'name': '一个月内的订单记录',
#             'icon': 'fa fa-line-chart',
#             'url': '/admin/'
#         }]
#     }, {
#         'name': '库存管理',
#         'icon': 'fa fa-truck',
#         'url': '/admin/',
#     }, {
#         'name': '卖家评论',
#         'icon': 'fa fa-handshake-o',
#         'models': [{
#             'name': '回复管理',
#             'url': '/admin/',
#             'icon': 'fa fa-handshake-o'
#         }]
#     }, {
#         'name': '信誉查看',
#         'icon': 'fa fa-diamond',
#         'url': '/admin',
#     }, {
#         'name': '店铺管理',
#         'icon': 'fa fa-database',
#         'url':'/admin/',
#     },{
#         'name': '商品管理',
#         'icon': 'fa fa-suitcase',
#         'url':'/admin/',
#     }, {
#         'name': '个人信息',
#         'icon': 'fa fa-user-o',
#         'models': [{
#             'name': '修改资料',
#             'url': '/admin/',
#             'icon': 'fa fa-id-card-o'
#         }, {
#             'name': '密码修改',
#             'icon': 'fa fa-id-card-o',
#             'url': '/admin/'
#         }]
#     }]
# }


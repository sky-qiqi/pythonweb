"""
Django 项目的设置文件。
由 'django-admin startproject' 使用 Django 2.0.3 生成。
"""

import os
from corsheaders.defaults import default_methods, default_headers

# 项目内部路径构建方式
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 快速启动开发设置 - 不适合生产环境
# 安全警告：在生产环境中，请务必保留密钥的秘密！
SECRET_KEY = '3r8%azo4sf)2yvl-!pa!lav)ao^6$_eoc_8bhmf-f8!^wypb)!'

# 安全警告：请勿在生产环境中开启调试模式！
DEBUG = True

ALLOWED_HOSTS = ['*'] # 允许所有主机访问，开发环境常用

# 应用定义
INSTALLED_APPS = [
    "simpleui",
    "corsheaders", # 跨域请求头应用
    'django.contrib.admin', # Django 管理后台
    'django.contrib.auth', # 认证系统
    'django.contrib.contenttypes', # 内容类型框架
    'django.contrib.sessions', # 会话管理
    'django.contrib.messages', # 消息框架
    'django.contrib.staticfiles', # 静态文件服务
    'movie', # 你的电影应用
    'index', # 你的索引应用
    'chat_api', # AI聊天API应用 [cite: 1]
    'rest_framework', # 如果你使用了Django REST Framework，请确保添加此行
]

CORS_ORIGIN_ALLOW_ALL = True # 允许所有来源的跨域请求
CORS_ALLOW_CREDENTIALS = True # 允许发送凭证（如cookies）
SESSION_COOKIE_SAMESITE = None # 关闭SameSite限制，为了跨域会话
CORS_ALLOW_METHODS = default_methods # 允许默认的HTTP方法（GET, POST等）
CORS_ALLOW_HEADERS = default_headers + ("access-token",) # 允许默认请求头，并额外允许"access-token"
CORS_ORIGIN_REGEX_WHITELIST = [] # 跨域来源正则白名单，此处为空表示不使用正则
APPEND_SLASH = True # 自动在URL末尾添加斜杠

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware", # CORS中间件，必须在所有其他中间件之前
    'django.middleware.security.SecurityMiddleware', # 安全相关中间件
    'django.contrib.sessions.middleware.SessionMiddleware', # 会话中间件
    'django.middleware.common.CommonMiddleware', # 常用中间件，处理不规范的URL等
    # 'django.middleware.csrf.CsrfViewMiddleware', # CSRF保护中间件，如果前端不发送CSRF token，可以注释掉
    'django.contrib.auth.middleware.AuthenticationMiddleware', # 认证中间件
    "middlewares.AccessTokenMiddleware", # 自定义AccessToken中间件
    "middlewares.JsonMiddleware", # 自定义Json中间件
    'django.contrib.messages.middleware.MessageMiddleware', # 消息中间件
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware', # X-Frame-Options中间件，防止点击劫持，如果需要嵌入iFrame可以注释掉
]

ROOT_URLCONF = 'movierecomend.urls' # 项目的URL配置文件

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": ["dist"], # 模板文件查找目录，此处指向 'dist' 目录
        "APP_DIRS": True, # 允许Django在应用目录中查找模板
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug", # 调试上下文处理器
                "django.template.context_processors.request", # 请求上下文处理器
                "django.contrib.auth.context_processors.auth", # 认证上下文处理器
                "django.contrib.messages.context_processors.messages", # 消息上下文处理器
            ],
        },
    },
]

WSGI_APPLICATION = 'movierecomend.wsgi.application' # WSGI应用程序入口

# 数据库配置
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # 使用SQLite3数据库
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'), # 数据库文件路径
    }
}

# 密码验证器
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

# 国际化设置
LANGUAGE_CODE = 'zh-hans' # 语言代码：简体中文

TIME_ZONE = 'Asia/Shanghai' # 时区：亚洲/上海

USE_I18N = True # 启用国际化

USE_L10N = True # 启用本地化

USE_TZ = False # 禁用时区支持（使用本地时间）

# 静态文件（CSS、JavaScript、图片）
STATIC_URL = '/static/' # 静态文件URL前缀，通常设置为'/static/'

# STATICFILES_DIRS 是 Django 查找额外的静态文件（除了应用内部的static/目录）的目录列表。
# 由于前端内容已删除，我们移除指向前端构建目录的配置。
# 如果你的项目根目录下有其他全局静态文件（如 'back/static/' 目录），可以在这里添加。
STATICFILES_DIRS = [
    # os.path.join(BASE_DIR, 'static'), # 示例：如果你的项目根目录有自定义的'static'文件夹，可以取消注释
]

MEDIA_URL = '/media/' # 媒体文件URL前缀
MEDIA_ROOT = os.path.join(BASE_DIR, "media") # 媒体文件存储的根目录
SIMPLEUI_HOME_INFO = False # simpleui 管理界面是否显示主页信息

# 解决Django 3.2+ 模型的自动主键警告
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# !!! 安全警告 !!!
# 将 API Key 存储在环境变量中，而不是直接写在代码中。
# 这里为了演示，直接写在这里，但在生产环境请务必使用环境变量！
# 例如: KIMI_API_KEY = os.environ.get('KIMI_API_KEY', '你的实际API Key')
# Volcano Engine (Doubao) API Configuration
VOLCANO_ENGINE_API_KEY = 'e6f6285f-7dd8-455c-ad46-239f805ddb54'
VOLCANO_ENGINE_API_URL = 'https://ark.cn-beijing.volces.com/api/v3/chat/completions'
VOLCANO_ENGINE_MODEL = 'doubao-1-5-thinking-vision-pro-250428'
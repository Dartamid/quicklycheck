from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-a*+0pf%1do#nu856&wipts%n2qb2z81tr=a-k!+(qkbyzg^(&h'

DEBUG = True

ALLOWED_HOSTS = ['*']

CORS_ORIGIN_ALLOW_ALL = True

THIRD_PARTY_APPS = [
    'django_json_widget',
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',
    'drf_spectacular'
]

LOCAL_APPS = [
    'checker.apps.CheckerConfig',
    'api.assessments.apps.AssessmentsConfig',
    'api.blanks.apps.BlanksConfig',
    'api.teachers.apps.TeachersConfig',
    'api.students.apps.StudentsConfig',
    'api.temps.apps.TempsConfig',
    'api.feedbacks.apps.FeedbacksConfig',
    'api.grades.apps.GradesConfig',
    'api.patterns.apps.PatternsConfig',
    'api.quizzes.apps.QuizzesConfig',
    'api.combined.apps.CombinedConfig',
    'api.apps.ApiConfig',
]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.postgres',
    *THIRD_PARTY_APPS,
    *LOCAL_APPS,
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'quicklycheck.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'quicklycheck.wsgi.application'

if DEBUG:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": 'django.db.backends.postgresql',
            "NAME": 'quicklycheck_db',
            "USER": 'quicklycheck_admin',
            "PASSWORD": 'Shavolmog3109',
            "HOST": 'rc1a-l6gsvm8pt8mh4wtp.mdb.yandexcloud.net',
            "PORT": '6432',
        }
    }


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

FILE_UPLOAD_HANDLERS = (
    'django.core.files.uploadhandler.TemporaryFileUploadHandler',
)

AUTHENTICATION_BACKENDS = [
    'api.teachers.backends.UserModelBackend'
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_RENDERER_CLASSES': (
        'djangorestframework_camel_case.render.CamelCaseJSONRenderer',
        'djangorestframework_camel_case.render.CamelCaseBrowsableAPIRenderer',
        # Any other renders
    ),

    'DEFAULT_PARSER_CLASSES': (
        # If you use MultiPartFormParser or FormParser, we also have a camel case version
        'djangorestframework_camel_case.parser.CamelCaseFormParser',
        'djangorestframework_camel_case.parser.CamelCaseMultiPartParser',
        'djangorestframework_camel_case.parser.CamelCaseJSONParser',
        # Any other parsers
    ),
}

SWAGGER_SETTINGS = {
    'USE_SESSION_AUTH': True,
    'LOGIN_URL': 'rest_framework:login',
    'LOGOUT_URL': 'rest_framework:logout',
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser',
        'rest_framework.parsers.JSONParser',
    ],
    'JSON_EDITOR': True,
}

SPECTACULAR_SETTINGS = {
    'TITLE': 'Quicklycheck API Management',
    'DESCRIPTION': 'Документация для Quicklycheck API.',
    'VERSION': '1.0.2b',
    'SERVE_INCLUDE_SCHEMA': True,
}

AUTH_USER_MODEL = 'teachers.User'

# STATICFILES_DIRS = [
#     BASE_DIR / "static",
# ]

LOGIN_REDIRECT_URL = 'index'

LANGUAGE_CODE = 'ru-ru'

TIME_ZONE = 'UTC+5'

USE_I18N = True

USE_TZ = True

STATIC_URL = '/static/'
MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

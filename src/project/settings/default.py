import environ

from django.urls import reverse_lazy


# ---------- Basic settings ----------

env = environ.Env()
root = environ.Path(__file__) - 3

BASE_DIR = root()
SECRET_KEY = env('SECRET_KEY')
DEBUG = env.bool('DEBUG', default=False)
SITE_ID = env.int('SITE_ID', default=1)
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=['localhost'])

ROOT_URLCONF = 'project.urls'
WSGI_APPLICATION = 'project.wsgi.application'

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

OMDB_API_URL = 'http://www.omdbapi.com/'
OMDB_API_KEY = env('OMDB_API_KEY', default='')

LOGIN_URL = reverse_lazy('admin:login')


# ---------- Applications ----------

LOCAL_APPS = [
    'project',
    'movie',
]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',
    'django_filters',
    'corsheaders',
    'drf_yasg',
] + LOCAL_APPS


# ---------- Static Files ----------

STATIC_URL = env('STATIC_URL', default='/static/')
STATIC_ROOT = env('STATIC_ROOT', default=(root - 2)('static'))
MEDIA_URL = env('MEDIA_URL', default='/media/')
MEDIA_ROOT = env('MEDIA_ROOT', default=(root - 2)('media'))

if not DEBUG:
    INSTALLED_APPS += ['django_s3_storage']
    DEFAULT_FILE_STORAGE = 'django_s3_storage.storage.S3Storage'
    STATICFILES_STORAGE = 'django_s3_storage.storage.StaticS3Storage'
    AWS_REGION = env('AWS_REGION')
    AWS_ACCESS_KEY_ID = env('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = env('AWS_SECRET_ACCESS_KEY')
    AWS_S3_BUCKET_NAME_STATIC = env('AWS_S3_BUCKET_NAME_STATIC')
    AWS_S3_BUCKET_AUTH_STATIC = False


# ---------- API Settings ----------


REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAdminUser',
    ),
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
    ),
    'ORDERING_PARAM': 'sort_by',
}


# ---------- Middleware ----------

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# ---------- Database ----------

DATABASES = {
    'default': env.db(
        default='postgres://postgres:postgres@postgres:5432/postgres'
    )
}


# ---------- Other ----------

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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


AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',  # noqa
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',  # noqa
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',  # noqa
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',  # noqa
    },
]

from core.settings import DEBUG

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

ON_TOP_APPS = [
    'corsheaders',
]

THIRD_PARTY_APPS = [
    'rest_framework',
    'simple_history',
    'cacheops',
    'django_filters'
]

LOCAL_APPS = [
    'user',
    'catalog',
    'post',
    'payment',
]

INSTALLED_APPS = ON_TOP_APPS + DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

if DEBUG:
    INSTALLED_APPS += ['django_extensions', 'drf_yasg']

DEFAULT_MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ON_TOP_MIDDLEWARE = ['corsheaders.middleware.CorsMiddleware', ]

THIRD_PARTY_MIDDLEWARE = ['simple_history.middleware.HistoryRequestMiddleware']

LOCAL_MIDDLEWARE = [
    'base.middleware.AuthMiddleware',
    # 'base.middleware.RequestResponseLogMiddleware',
]

MIDDLEWARE = ON_TOP_MIDDLEWARE + DEFAULT_MIDDLEWARE + THIRD_PARTY_MIDDLEWARE + LOCAL_MIDDLEWARE

ROOT_URLCONF = 'core.urls'

WSGI_APPLICATION = 'core.wsgi.application'

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

DEBUG = True
SECRET_KEY = 'aImQrd3sPlxm2s4ZfCgafxCPmj9ZeL5a'
ROOT_URLCONF = 'tests.testapp.urls'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

INSTALLED_APPS = (
    'modeltranslation',
    'modeltranslation_xliff',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.sites',
    'tests.testapp',
)

MIDDLEWARE = (
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

LANGUAGE_CODE = 'en-us'

LANGUAGES = [
    ('en-us', 'US English'),
    ('ru-ru', 'Russian')
]

USE_I18N = True
USE_L10N = True

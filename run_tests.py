#!/usr/bin/env python
# Thanks to django-extensions for the starting code
import sys
import shutil
import tempfile
from django.conf import settings
from django.core.management import call_command

def main():
    # Dynamically configure the Django settings with the minimum necessary to
    # get Django running tests
    INSTALLED_APPS = ['multigtfs']
    TEST_RUNNER = 'django.test.simple.DjangoTestSuiteRunner'
    
    # If django-nose is installed, use it
    # You can do things like ./run_tests.py --with-coverage
    try:
        from pkg_resources import WorkingSet, DistributionNotFound
        working_set = WorkingSet()
        working_set.require('django_nose')
    except ImportError:
        print 'setuptools not installed.  Weird.'
    except DistributionNotFound:
        print "django-nose not installed.  You'd like it."
    else:
        INSTALLED_APPS.append('django_nose')
        TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'\
    
    settings.configure(
        INSTALLED_APPS = INSTALLED_APPS,
        # Django replaces this, but it still wants it. *shrugs*
        DATABASE_ENGINE = 'django.db.backends.sqlite3',
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
            }
        },
        DEBUG = True,
        TEMPLATE_DEBUG = True,
        TEST_RUNNER = TEST_RUNNER
    )

    from django.test.utils import get_runner
    test_runner = get_runner(settings)(verbosity=2, interactive=True)
    failures = test_runner.run_tests(['multigtfs'])
    sys.exit(failures)


if __name__ == '__main__':
    main()
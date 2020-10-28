from django.apps import AppConfig, apps

# This function is inspired by djem's own adaptation [1] of Simon Charette's
# comment on Django ticket #7835 [2]:
# [1] https://github.com/oogles/djem/blob/ff5c8e5b81de8c92ce554b18d1cbf64cf9dc1f79/djem/utils/tests.py
# [2] https://code.djangoproject.com/ticket/7835#comment:46


def setup_test_app(package, label=None):
    """
    Setup a Django test app for the provided package to allow test-only models
    to be used.
    This function should be called from myapp.tests.__init__ like so:

        setup_test_app(__package__)

    Or, if a specific app label is required, like so:

        setup_test_app(__package__, 'mytests')

    Models defined within the package also require their app labels manually
    set to match, e.g.:

        class MyTestModel(models.Model):

            # ...

            class Meta:
                app_label = 'mytests'
    """

    #
    #

    if label is None:
        containing_app_config = apps.get_containing_app_config(package)
        label = containing_app_config.label

        # Only suffix the app label if it has not been already. This allows
        # duplicate entries to be detected and prevented. It may prevent the
        # use of an implicit label if the tests reside in an app that
        # legitimately ends with "_tests", but an explicit label can always be
        # used. Without this check, earlier entries are returned by
        # get_containing_app_config() and suffixed repeatedly.
        if not containing_app_config.label.endswith('_tests'):
            label = '{}_tests'.format(containing_app_config.label)

    if label in apps.app_configs:
        # An app with this label already exists, skip adding it. This is
        # necessary (vs raising an exception) as there are certain conditions
        # that can cause this function to be run multiple times (e.g. errors
        # during Django's initialisation can cause this).
        return

    app_config = AppConfig.create(package)
    app_config.apps = apps
    app_config.label = label

    apps.app_configs[label] = app_config

    app_config.import_models()

    apps.clear_cache()


# Use an explicit app label so as not to interfere with the tests of
# setup_test_app() itself (which test implicit app labels)
setup_test_app(__package__, 'api_test')

import django
from django.test import TestCase

from api.models.models import LAWMRegion


class LAWMRegionTest(TestCase):
    def test_name_attribute_returns_correct_object(self):
        region_name = "a name"
        region = LAWMRegion.objects.create(name=region_name)

        self.assertEqual(region.name, region_name)

    def test_name_attribute_is_ok(self):
        region_name = "a name"
        _ = LAWMRegion.objects.create(name=region_name)
        try:
            _ = LAWMRegion.objects.create(name=region_name)
            self.fail("Creating 2 regions with same name should raise an error.")
        except django.db.utils.IntegrityError:
            pass

# Internal libraries
from onclusiveml.serving.rest.testing import LoadTest


def test_load_test():

    test_load_test = LoadTest(settings=None)

    assert test_load_test.settings is None
    assert test_load_test.start_time == -1
    assert test_load_test.end_time == -1

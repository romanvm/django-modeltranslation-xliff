from modeltranslation_xliff import utils
from .data import TEST_DATA_EN, TEST_DATA_RU, XLIFF_EN, XLIFF_RU


def test_create_xliff():
    xliff = utils.create_xliff(TEST_DATA_EN)
    assert xliff == XLIFF_EN


def test_import_xliff():
    translation_data = utils.import_xliff(XLIFF_RU.encode('utf-8'))
    assert translation_data == TEST_DATA_RU

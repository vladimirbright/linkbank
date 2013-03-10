# -*- coding: utf-8 -*-


from django.test import TestCase
from django.test.client import RequestFactory


from bank.forms import LinkForm


class LinkFormTestCase(TestCase):

    def setUp(self):
        super(LinkFormTestCase, self).setUp()
        self.factory = RequestFactory()

    def test_check_encoding_existing_encoding_from_get(self):
        request = self.factory.get('/some/url/?encoding=cp1251')
        assert request.encoding is None
        request = LinkForm.check_encoding(request)
        assert request.encoding == 'cp1251'

    def test_check_encoding_existing_encoding_from_post(self):
        request = self.factory.post('/some/url/', data={'encoding': 'cp1251'})
        assert request.encoding is None
        request = LinkForm.check_encoding(request)
        assert request.encoding == 'cp1251'

    def test_check_encoding_non_existing_encoding_from_get(self):
        request = self.factory.get('/some/url/?encoding=cdddddddd')
        assert request.encoding is None
        request = LinkForm.check_encoding(request)
        assert request.encoding == LinkForm.DEFAULT_LINK_ENCODING

    def test_check_encoding_non_existing_encoding_from_post(self):
        request = self.factory.get('/some/url/', data={'encoding': 'cdddddddd'})
        assert request.encoding is None
        request = LinkForm.check_encoding(request)
        assert request.encoding == LinkForm.DEFAULT_LINK_ENCODING

    def test_check_encoding_without_encoding_param(self):
        request = self.factory.get('/some/url/')
        assert request.encoding is None
        request = LinkForm.check_encoding(request)
        assert request.encoding == LinkForm.DEFAULT_LINK_ENCODING

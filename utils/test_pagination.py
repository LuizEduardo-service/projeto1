from unittest import TestCase
from .pagination import make_pagination_range


class PaginationTest(TestCase):

    def test_make_pagination_range_returns_a_pagination_range(self):
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qtd_paginas=4,
            current_page=1
        )

        self.assertEqual(list(range(1,5)), pagination)

    def test_first_range_is_static_if_current_page_is_less_than_middle_page(self):
        ...
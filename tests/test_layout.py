# -*- coding: utf-8 -*-

import unittest

import simpleplotly as sp


class LayoutBuildersTest(unittest.TestCase):
    def setUp(self):
        self.test_layout = {}

    def test_shape_builder(self):
        expected = {'type': 'rect', 'x0': 2, 'x1': 3, 'xref': 'x', 'y0': 0, 'y1': 1, 'yref': 'paper'}
        shape_builder = sp.Shape(**expected)
        shape_builder(self.test_layout)
        self.assertDictEqual(self.test_layout['shapes'][0], expected)

    def test_annotation_builder(self):
        expected = {'text': 'some text', 'x': 2, 'xref': 'x', 'y': 3, 'yref': 'y'}
        annotation_builder = sp.Annotation(2, 3, 'some text')
        annotation_builder(self.test_layout)
        self.assertDictEqual(self.test_layout['annotations'][0], expected)

    def test_xaxis_builder(self):
        self.check_axis(sp.XAxis, 'xaxis')

    def test_yaxis_builder(self):
        self.check_axis(sp.YAxis, 'yaxis')

    def test_zaxis_builder(self):
        self.check_axis(sp.ZAxis, 'zaxis')

    def check_axis(self, axis_builder_func, axis_name):
        expected = {'autorange': True, 'showgrid': True, 'showline': False, 'title': 'test axis', 'zeroline': True}
        shape_builder = axis_builder_func('test axis')
        shape_builder(self.test_layout)
        self.assertDictEqual(self.test_layout[axis_name], expected)

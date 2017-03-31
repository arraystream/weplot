# -*- coding: utf-8 -*-

import unittest
import simpleplotly as sp
import plotly.graph_objs as go


class FigureHolderTest(unittest.TestCase):
    def test_can_update_layout(self):
        fh = sp.FigureHolder(go.Figure())
        fh.update_layout(barmode='group', title='test plot')
        self.assertDictEqual(fh.figure.layout, dict(barmode='group', title='test plot'))

        fh.drop_layout_key('barmode')
        self.assertDictEqual(fh.figure.layout, dict(title='test plot'))


class FigureBuilderTest(unittest.TestCase):
    def test_figure_builder_operations(self):
        pass

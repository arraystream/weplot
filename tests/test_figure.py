# -*- coding: utf-8 -*-

import unittest
import simpleplotly as sp
import plotly.graph_objs as go


class FigureHolderTest(unittest.TestCase):
    def test_can_update_layout(self):
        fh = sp.FigureHolder(go.Figure())
        layout = fh.figure.layout

        self.assertIsNone(layout.barmode)
        self.assertIsNone(layout.title)

        fh.update_layout(barmode='group', title='test plot')
        # self.assertDictEqual(fh.figure.layout._props, dict(barmode='group', title='test plot'))
        self.assertEqual(layout.barmode, 'group')
        self.assertEqual(layout.title, 'test plot')

        fh.drop_layout_key('barmode')
        self.assertIsNone(layout.barmode)
        self.assertEqual(layout.title, 'test plot')


class FigureBuilderTest(unittest.TestCase):
    def test_figure_builder_operations(self):
        pass

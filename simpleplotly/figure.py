# -*- coding: utf-8 -*-

import itertools

import plotly.graph_objs as go
from plotly import tools

from .layout import ElementBuilder
from .plot import AtomBuilder
from .subplot import SubPlotSpec, PlotCanvas



class FigureHolder(object):
    def __init__(self, figure):
        self.figure = figure

    def plot(self, mode='offline'):
        if mode == 'offline':
            import plotly.offline as py
            py.iplot(self.figure)
        else:
            raise ValueError('online not supported yet, please check later!')

    def update_layout(self, **kwargs):
        self.figure.layout.update(**kwargs)
        return self

    def drop_key_layout(self, key):
        if key in self.figure.layout:
            del self.figure.layout[key]
        return self


class FigureBuilder(object):
    def __init__(self, *builders):
        self.builders = list(builders)
        self.specs = [None for _ in range(len(builders))]
        self.layout = {}
        self.canvas = PlotCanvas()

    def __add__(self,fig_builder,default_layout='blank'):
        # new builder
        new_fig_builder = FigureBuilder()
        new_fig_builder.builders.extend(self.builders)
        new_fig_builder.builders.extend(fig_builder.builders)
        if default_layout=='left':
            new_fig_builder.layout=self.layout
        elif default_layout=='right':
            new_fig_builder.layout=fig_builder.layout
        else:
            new_fig_builder.layout={}
        return new_fig_builder


    def add(self, builder, row=None, col=None, row_span=1, col_span=1):
        if isinstance(builder, AtomBuilder):
            self.builders.append(builder)
            spec = self._validated_spec(row, col, row_span, col_span)
            if spec is not None:
                self.canvas.occupy_area(spec)
            self.specs.append(spec)
        elif isinstance(builder, ElementBuilder):
            builder(self.layout)
        else:
            raise ValueError('The type of builder is {} which is not known'.format(type(builder)))
        return self

    @staticmethod
    def _validated_spec(row, col, row_span, col_span):
        if row is None or col is None:
            return None
        else:
            return SubPlotSpec(row, col, row_span, col_span)

    def update_layout(self, **kwargs):
        self.layout.update(kwargs)
        return self

    def build(self):
        data = [b.data for b in self.builders]
        layout = {}
        for b in self.builders:
            layout.update(b.layout)
        layout.update(self.layout)
        return FigureHolder(go.Figure(data=data, layout=layout))

    def plot(self):
        self.build().plot()

    def build_subplot(self, print_grid=True, **kwargs):
        fig = tools.make_subplots(
            rows=self.canvas.max_rows, cols=self.canvas.max_cols,
            specs=self.canvas.make_plotly_spec(),
            print_grid=print_grid, **kwargs)

        for idx, builder in enumerate(self.builders):
            spec = self.specs[idx]
            fig.append_trace(builder.data, spec.r, spec.c)

        holder = FigureHolder(go.Figure(data=fig.data, layout=fig.layout))
        holder.update_layout(**self.layout)
        holder.drop_key_layout('xaxis').drop_key_layout('yaxis')
        return holder

    def subplot(self, row=None, col=None, print_grid=True, **kwargs):
        if col is not None and row is not None:
            self.specs = []
            self.canvas = PlotCanvas()
            for row, col in itertools.product(range(1, row + 1), range(1, col + 1)):
                spec = self._validated_spec(row, col, row_span=1, col_span=1)
                if spec is not None:
                    self.canvas.occupy_area(spec)
                self.specs.append(spec)
        self.build_subplot(print_grid=print_grid, **kwargs).plot()

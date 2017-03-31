# -*- coding: utf-8 -*-

import itertools

import plotly.graph_objs as go
from plotly import tools
import copy
from .layout import ElementBuilder
from .plot import AtomBuilder
from .subplot import SubPlotSpec, PlotCanvas


class FigureHolder(object):
    def __init__(self, figure):
        self.figure = figure

    def plot(self, filename=None):
        if filename is None:
            import plotly.offline as py
            py.iplot(self.figure)
        else:
            import plotly.plotly as py
            py.iplot(self.figure, filename=filename)

    def update_layout(self, **kwargs):
        self.figure.layout.update(**kwargs)
        return self

    def drop_layout_key(self, key):
        if key in self.figure.layout:
            del self.figure.layout[key]
        return self

    def save_image(self, filename, **kwargs):
        import plotly.plotly as py
        py.image.save_as(self.figure, filename=filename, **kwargs)


class FigureBuilder(object):
    def __init__(self):
        self.builders = []
        self.specs = []
        self.layout = {}
        self.canvas = PlotCanvas()

    def __add__(self, other_builder):
        return self.combine(other_builder)

    def combine(self, other_builder, layout=None):
        new_fig_builder = FigureBuilder()
        new_fig_builder.builders.extend(self.builders)
        new_fig_builder.builders.extend(other_builder.builders)
        if layout == 'left':
            new_fig_builder.layout = self.layout
        elif layout == 'right':
            new_fig_builder.layout = other_builder.layout
        elif layout is not None:
            raise ValueError('layout can only be left, right or None')
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
            fig.append_trace(copy.deepcopy(builder.data), spec.r, spec.c)

        holder = FigureHolder(go.Figure(data=fig.data, layout=fig.layout))
        holder.update_layout(**self.layout)
        holder.drop_layout_key('xaxis').drop_layout_key('yaxis')
        return holder

    def customize_spec(self, spec_list, is_replace=False):
        specs = []
        canvas = PlotCanvas()
        for one_spec in spec_list:
            if len(one_spec) == 2:
                spec = self._validated_spec(one_spec[0], one_spec[1], 1, 1)
            elif len(one_spec) == 4:
                spec = self._validated_spec(one_spec[0], one_spec[1], one_spec[2], one_spec[3])
            else:
                raise ValueError('spec in spec_list should be a list of len 2 or 4')
            canvas.occupy_area(spec)
            specs.append(spec)
        if is_replace:
            self.specs, self.canvas = specs, canvas
            return self
        else:
            return specs, canvas

    def subplot(self, row=None, col=None, print_grid=True, **kwargs):
        if col is not None and row is not None:
            new_builder = FigureBuilder()
            new_builder.builders = self.builders
            new_builder.layout = copy.deepcopy(self.layout)
            new_builder.specs, new_builder.canvas = self.customize_spec(list(itertools.product(range(1, row + 1),
                                                                                               range(1, col + 1))))
            new_builder.build_subplot(print_grid=print_grid, **kwargs).plot()
        else:
            self.build_subplot(print_grid=print_grid, **kwargs).plot()

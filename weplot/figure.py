import copy
import itertools

import plotly
import plotly.graph_objs as go
from plotly import tools

from .layout import ElementBuilder
from .plot import AtomBuilder
from .subplot import SubPlotSpec, PlotCanvas


class FigureHolder(object):
    def __init__(self, figure):
        self.figure = figure

    def plot(self, mode='offline', **plot_options):
        if mode == 'online':
            py = plotly.plotly
        elif mode == 'offline':
            py = plotly.offline
        else:
            raise ValueError('mode must be one of (online, offline)')

        return py.iplot(self.figure, **plot_options)

    def plot_online(self, **plot_options):
        return self.plot(mode='offline', **plot_options)

    def update_layout(self, **kwargs):
        self.figure.layout.update(**kwargs)
        return self

    def drop_layout_key(self, key):
        self.figure.layout.update(**{key: None})
        return self

    def to_image(self, filename, format=None, width=None, height=None, scale=None):
        plotly.plotly.image.save_as(self.figure, filename=filename, format=format, width=width, height=height, scale=scale)

    def to_json(self):
        import json
        return json.dumps(self.figure, cls=plotly.utils.PlotlyJSONEncoder)


def validated_spec(row, col, row_span, col_span):
    if row is None or col is None:
        return None
    else:
        return SubPlotSpec(row, col, row_span, col_span)


def canvas_from_specs(specs):
    canvas = PlotCanvas()
    for one_spec in specs:
        if len(one_spec) == 2:
            spec = validated_spec(one_spec[0], one_spec[1], 1, 1)
        elif len(one_spec) == 4:
            spec = validated_spec(one_spec[0], one_spec[1], one_spec[2], one_spec[3])
        else:
            raise ValueError('spec in specs should be of len 2 or 4')
        canvas.occupy_area(spec)
    return canvas


class FigureBuilder(object):
    def __init__(self):
        self.builders = []
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
            spec = validated_spec(row, col, row_span, col_span)
            self.canvas.occupy_area(spec)
        elif isinstance(builder, ElementBuilder):
            builder(self.layout)
        else:
            raise ValueError('The type of builder is {} which is not known'.format(type(builder)))
        return self

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
            spec = self.canvas.specs[idx]
            fig.append_trace(copy.deepcopy(builder.data), spec.r, spec.c)

        holder = FigureHolder(go.Figure(data=fig.data, layout=fig.layout))
        holder.update_layout(**self.layout)
        holder.drop_layout_key('xaxis').drop_layout_key('yaxis')
        return holder

    def subplot(self, row=None, col=None, print_grid=True, **kwargs):
        if col is not None and row is not None:
            new_builder = FigureBuilder()
            new_builder.builders = self.builders
            new_builder.layout = copy.deepcopy(self.layout)
            new_builder.canvas = canvas_from_specs(itertools.product(range(1, row + 1), range(1, col + 1)))
            new_builder.build_subplot(print_grid=print_grid, **kwargs).plot()
        else:
            self.build_subplot(print_grid=print_grid, **kwargs).plot()

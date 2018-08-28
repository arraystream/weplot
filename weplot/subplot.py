import itertools
from collections import namedtuple


class SubPlotSpec(namedtuple('SubPlotSpec', ['r', 'c', 'rs', 'cs'])):
    @property
    def row_end(self):
        return self.r + self.rs

    @property
    def col_end(self):
        return self.c + self.cs

    @property
    def location(self):
        return self.r, self.c

    @property
    def r_max(self):
        return self.row_end - 1

    @property
    def c_max(self):
        return self.col_end - 1

    def area_spec(self):
        area = {}
        for location in itertools.product(range(self.r, self.row_end), range(self.c, self.col_end)):
            area[location] = None
        anchor_spec = {}
        if self.rs > 1:
            anchor_spec['rowspan'] = self.rs
        if self.cs > 1:
            anchor_spec['colspan'] = self.cs
        area[self.location] = anchor_spec
        return area


class PlotCanvas(object):
    def __init__(self):
        self.canvas = {}
        self.specs = []
        self.max_rows = 1
        self.max_cols = 1

    def _expand(self, r_max, c_max):
        if r_max > self.max_rows:
            self.max_rows = r_max
        if c_max > self.max_cols:
            self.max_cols = c_max

    def occupy_area(self, spec):
        if spec is not None:
            self.canvas.update(spec.area_spec())
            self._expand(spec.r_max, spec.c_max)
        self.specs.append(spec)

    def make_plotly_spec(self):
        plotly_specs = []
        for r in range(1, self.max_rows + 1):
            row_spec = []
            for c in range(1, self.max_cols + 1):
                row_spec.append(self.canvas.get((r, c), {}))
            plotly_specs.append(row_spec)
        return plotly_specs

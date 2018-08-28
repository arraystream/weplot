from abc import ABC

from plotly import graph_objs as go


class AtomBuilder(ABC):
    def __init__(self, data=None, layout=None):
        if data is None:
            data = {}
        if layout is None:
            layout = {}
        self.data = data
        self.layout = layout


class Pie(AtomBuilder):
    def __init__(self, labels, values, **kwargs):
        super().__init__(data=go.Pie(labels=labels, values=values, **kwargs))


class Scatter(AtomBuilder):
    def __init__(self, x, y, mode='markers', **kwargs):
        super().__init__(data=go.Scatter(x=x, y=y, mode=mode, **kwargs))


class Line(AtomBuilder):
    def __init__(self, x, y, mode='lines', **kwargs):
        super().__init__(data=go.Scatter(x=x, y=y, mode=mode, **kwargs))


class Box(AtomBuilder):
    def __init__(self, y, **kwargs):
        super().__init__(data=go.Box(y=y, **kwargs))

    def horizontal(self):
        if 'x' in self.data:
            self.data.x, self.data.y = self.data.y, self.data.x
        else:
            self.data['x'] = self.data.y
            del self.data['y']
        self.data['orientation'] = 'h'
        return self


class Bar(AtomBuilder):
    def __init__(self, x, y, **kwargs):
        super().__init__(data=go.Bar(x=x, y=y, **kwargs))

    def horizontal(self):
        self.data.x, self.data.y = self.data.y, self.data.x
        self.data['orientation'] = 'h'
        return self


class Histogram(AtomBuilder):
    def __init__(self, x, **kwargs):
        super().__init__(data=go.Histogram(x=x, **kwargs))

    def xbins(self, start=None, end=None, size=None, bins=None):
        if start is None:
            start = min(self.data['x'])
        if end is None:
            end = max(self.data['x'])
        if size is None:
            if bins is None:
                raise ValueError('size and bins can not be both none')
            else:
                size = (end - start) / bins
        self.data['xbins'] = dict(start=start, end=end, size=size)
        self.data['autobinx'] = False
        return self


class Heatmap(AtomBuilder):
    def __init__(self, z, **kwargs):
        super().__init__(data=go.Heatmap(z=z, **kwargs))


class Scatter3D(AtomBuilder):
    def __init__(self, x, y, z, mode='markers', **kwargs):
        super().__init__(data=go.Scatter3d(x=x, y=y, z=z, mode=mode, **kwargs))


class Line3D(AtomBuilder):
    def __init__(self, x, y, z, mode='lines', **kwargs):
        super().__init__(data=go.Scatter3d(x=x, y=y, z=z, mode=mode, **kwargs))


class Surface(AtomBuilder):
    def __init__(self, z, **kwargs):
        super().__init__(data=go.Surface(z=z, **kwargs))

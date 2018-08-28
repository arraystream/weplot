import abc

from plotly import graph_objs as go


class ElementBuilder(abc.ABC):
    @abc.abstractmethod
    def __call__(self, layout):
        pass


class Shape(ElementBuilder):
    def __init__(self, x0, x1, y0=0, y1=1, type='rect', xref='x', yref='paper', **kwargs):
        self.shapes = dict(x0=x0, x1=x1, y0=y0, y1=y1, type=type, xref=xref, yref=yref)
        self.shapes.update(kwargs)

    def __call__(self, layout):
        if 'shapes' not in layout:
            layout['shapes'] = []
        layout['shapes'].append(self.shapes)


class Annotation(ElementBuilder):
    def __init__(self, x, y, text, xref='x', yref='y', **kwargs):
        self.annotations = dict(x=x, y=y, text=text, xref=xref, yref=yref)
        self.annotations.update(kwargs)

    def __call__(self, layout):
        if 'annotations' not in layout:
            layout['annotations'] = []
        layout['annotations'].append(self.annotations)


class AxisBuilder(ElementBuilder):
    def __init__(self, axis_factory, title, name, autorange=True, showgrid=True, showline=False, **kwargs):
        self.axis = dict(title=title, autorange=autorange, showgrid=showgrid, showline=showline)
        self.axis.update(kwargs)
        self.name = name
        self.axis_factory = axis_factory

    def axis_range(self, min, max):
        self.axis.update(dict(range=[min, max]))
        self.axis.update(dict(autorange=False))
        return self

    def to_log(self):
        self.axis.update(dict(type='log'))
        return self

    def __call__(self, layout):
        layout[self.name] = self.axis_factory(**self.axis)


class XAxis(AxisBuilder):
    def __init__(self, title, name='xaxis', autorange=True, showgrid=True, showline=False, **kwargs):
        super().__init__(go.layout.XAxis, name=name, title=title, autorange=autorange, showgrid=showgrid, showline=showline, **kwargs)


class YAxis(AxisBuilder):
    def __init__(self, title, name='yaxis', autorange=True, showgrid=True, showline=False, **kwargs):
        super().__init__(go.layout.YAxis, title=title, name=name, autorange=autorange, showgrid=showgrid, showline=showline, **kwargs)


class ZAxis(AxisBuilder):
    def __init__(self, title, name='zaxis', autorange=True, showgrid=True, showline=False, **kwargs):
        super().__init__(go.layout.scene.ZAxis, title=title, name=name, autorange=autorange, showgrid=showgrid, showline=showline, **kwargs)

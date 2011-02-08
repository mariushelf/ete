from PyQt4 import QtCore, QtGui
from qt4_gui import _NodeActions
from main import FACE_POSITIONS

class _ItemFaceItem(QtGui.QGraphicsRectItem):
    def __init__(self, face, node):
        QtGui.QGraphicsRectItem.__init__(self)
        self.node = node
    def paint(self, painter, option, index):
        return
        
class _TextFaceItem(QtGui.QGraphicsSimpleTextItem):
    def __init__(self, face, node, text):
        QtGui.QGraphicsSimpleTextItem.__init__(self, text)
        self.node = node

class _ImgFaceItem(QtGui.QGraphicsPixmapItem):
    def __init__(self, face, node):
        QtGui.QGraphicsPixmapItem.__init__(self)
        self.node = node

class _BackgroundFaceItem(QtGui.QGraphicsRectItem):
    def __init__(self, face, node):
        QtGui.QGraphicsRectItem.__init__(self)
        self.node = node

    def paint(self, painter, option, index):
        return

class _FaceGroupItem(QtGui.QGraphicsItem): # I resisted to name this FaceBookItem :) 
    def __init__(self, faces, node, column_widths={}, *args, **kargs):

        # This caused seg. faults. in some computers. No idea why.
        # QtGui.QGraphicsItem.__init__(self, *args, **kargs) 
        QtGui.QGraphicsItem.__init__(self)  

        self.node = node
        self.column2faces = faces
        self.column2size = {}
        
        # column_widths is a dictionary of min column size. Can be
        # used to reserve some space to specific columns
        self.set_min_column_widths(column_widths)

        self.w = 0
        self.h = 0
        # updates the size of this grid
        self.update_columns_size()

    def set_min_column_widths(self, column_widths):
        # column_widths is a dictionary of min column size. Can be
        # used to reserve some space to specific columns
        self.column_widths = column_widths
        self.columns = sorted(set(self.column2faces.keys() + self.column_widths.keys()))

    def paint(self, painter, option, index):
        return

    def boundingRect(self):
        return QtCore.QRectF(0,0, self.w, self.h)

    def get_size():
        return self.w, self.h

    def update_columns_size(self):
        self.column2size = {}
        for c in self.columns:
            faces = self.column2faces.get(c, [])
            height = 0
            width = 0
            for f in faces:
                f.node = self.node
                if f.type == "pixmap": 
                    f.update_pixmap()
                elif f.type == "item":
                    f.update_items()
                height += f._height() + f.margin_top + f.margin_bottom
                width = max(width, f._width() + f.margin_right + f.margin_left)
            width = max(width, self.column_widths.get(c, 0))
            self.column2size[c] = (width, height)
        self.w = sum([0]+[size[0] for size in self.column2size.itervalues()])
        self.h = max([0]+[size[1] for size in self.column2size.itervalues()])

    def render(self):
        x = 0
        for c in self.columns:
            faces = self.column2faces.get(c, [])
            w, h = self.column2size[c]
            # Starting y position. Center columns
            y = (self.h / 2) - (h/2)
            for f in faces:
                f.node = self.node
                if f.type == "text":
                    obj = _TextFaceItem(f, self.node, f.get_text())
                    font = QtGui.QFont(f.ftype, f.fsize)
                    obj.setFont(font)
                    obj.setBrush(QtGui.QBrush(QtGui.QColor(f.fgcolor)))
                    obj.setParentItem(self)
                    obj.setAcceptsHoverEvents(True)
                elif f.type == "item":
                    obj = _ItemFaceItem(f, self.node)
                    f.item.setParentItem(obj)
                    obj.setParentItem(self)
                else:
                    # Loads the pre-generated pixmap
                    obj = _ImgFaceItem(f, self.node, f.pixmap)
                    obj.setAcceptsHoverEvents(True)
                    obj.setParentItem(self)
                obj.setPos(x+ f.margin_left, y+f.margin_top)
                if f.opacity < 1:
                    obj.setOpacity(f.opacity)
                # Y position is incremented by the height of last face
                # in column
                y += f._height() + f.margin_top + f.margin_bottom
            # X position is incremented by the max width of the last
            # processed column.
            x += w

def update_node_faces(node, n2f):
    # Organize all faces of this node in FaceGroups objects
    # (tables of faces)
    faceblock = {}

    n2f[node] = faceblock
    for position in FACE_POSITIONS:
        if position in node.img_style["_faces"]:
            # The value of this is expected to be list of columns of faces
            # c2f = [ [f1, f2, f3], 
            #         [f4, f4]
            #       ]
            faceblock[position] = _FaceGroupItem(node.img_style["_faces"][position], node)
        else:
            faceblock[position] = _FaceGroupItem({}, node)
    return faceblock

def _leaf(node):
    collapsed = hasattr(node, "img_style") and not node.img_style["draw_descendants"]
    return collapsed or node.is_leaf()


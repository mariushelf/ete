import sys
import random
import cPickle

from ete_dev import Tree, faces, TreeImage, NodeStyleDict

def mylayout(node):
    # If node is a leaf, add the nodes name and a its scientific
    # name
    pass
    if node.is_leaf():
        faces.add_face_to_node(content, node, column=0, position="aligned")
        faces.add_face_to_node(content, node, column=1, position="aligned")
        faces.add_face_to_node(content, node, column=3, position="aligned")
    # else:
    #     faces.add_face_to_node(ud, node, column=1, position="branch-top")
    #     faces.add_face_to_node(ud, node, column=1, position="branch-top")
    #     faces.add_face_to_node(ud, node, column=1, position="branch-top")
    #     faces.add_face_to_node(ud, node, column=1, position="branch-top")
    #     faces.add_face_to_node(bd, node, column=1, position="branch-bottom")
    #     faces.add_face_to_node(bd, node, column=1, position="branch-bottom")
    #     faces.add_face_to_node(rs2, node, column=1, position="branch-right")
    #     faces.add_face_to_node(rs1, node, column=1, position="branch-right")
    #     faces.add_face_to_node(rs2, node, column=1, position="branch-right")
    #     faces.add_face_to_node(rs2, node, column=1, position="branch-right")
    #     faces.add_face_to_node(rs2, node, column=1, position="branch-right")
    #     faces.add_face_to_node(rs2, node, column=1, position="branch-right")

# Margins can now be set for any face
rs1 = faces.TextFace("branch-right1-with-margins", fsize=20, fgcolor="#009000")
rs1.margin_top = 10
rs1.margin_top = 50
rs1.margin_left = 40
rs1.margin_right = 40

rs2 = faces.TextFace("branch-right2", fsize=20, fgcolor="#009000")
rs3 = faces.TextFace("branch-right3", fsize=20, fgcolor="#009000")

# New face positions (branch-top and branch-bottom)
bd = faces.TextFace("branch-bottom", fsize=11, fgcolor="#909000")
ud = faces.TextFace("branch-top", fsize=6, fgcolor="#099000")

# And faces can also be used as headers or foot notes of aligned
# columns
t1 = faces.TextFace("header_up", fsize=11, fgcolor="#099000")
t2 = faces.TextFace("header_down", fsize=11, fgcolor="#099000")

fixed = faces.TextFace("FIXED", fsize=11, fgcolor="#099000")

# Attribute faces can now contain prefix and suffix fixed text
content = faces.AttrFace("name", fsize=12, fgcolor="#099000", text_prefix="name=(", text_suffix=")")
content.margin_right = 50
# Node style handling is no longer limited to layout functions. You
# can now create fixed node styles and use them many times, save them
# or even add them to nodes before drawing (this allows to save and
# reproduce an image composition)
style = NodeStyleDict()
style["fgcolor"] = "#ff0000"
style["shape"] = "square"
style["vt_line_color"] = "#ff0000"
# We add a face to the style. This face will be render in any node
# associated to the style.
#style.add_fixed_face(fixed, "branch-right", 0)

#ETE 2.1 has finally official support for TreeImageProperties, and
#object that can be used to set different general purpose image properties
I = TreeImage()

# You can add faces to the tree image (without any node
# associated). They will be used as headers and foot notes of the
# aligned columns (aligned faces)

I.aligned_header.add_face(t1, column = 0)
I.aligned_header.add_face(t1, 1)
I.aligned_header.add_face(t1, 2)
I.aligned_header.add_face(t1, 3)

I.aligned_foot.add_face(t2, column = 0)
I.aligned_foot.add_face(t2, 1)
I.aligned_foot.add_face(t2, 2)
I.aligned_foot.add_face(t2, 3)

t = Tree()
t.dist = 0
t.populate(int(sys.argv[1]))

# Bind the precomputed style to the root node 
t.img_style = style
# t.render("./test.svg", layout=mylayout, img_properties=I)
I.mode = "circular"
t.show(mylayout, img_properties=I)

sys.exit(0)

for n in t.traverse():
    n.img_style.clear()
    for k, v in n.img_style.iteritems():
        print k, v
    print 
    
#print style
cPickle.dump(t, open("test.pkl", "w"))
print "OK"
t = cPickle.load(open("test.pkl"))
print t
t.show(mylayout, img_properties=I)

t2 = t.copy()
t2.show(mylayout, img_properties=I)

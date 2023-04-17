from treelib import Tree
import os
import argparse


class Node():
    def __init__(self, id = -1, relname='rel', is_root=False, leaf_number = -1, is_leaf=False, direction='p', text='', parent=None):
        self.is_leaf = is_leaf
        self.relname = relname
        self.direction = direction
        self.text = text
        self.children = []
        self.parent = parent
        self.leaf_number = leaf_number
        self.is_root = is_root
        self.id = id
    
    def add_child(self, child):
        self.children.append(child)



def build_tree(t):
    elements = t.split()
    leaf_count = 0
    node_count = 0
    stack = []
    root = None
    for i in range(len(elements)):
        if elements[i] == '(':
            parent = None
            if len(stack) != 0:
                parent = stack[0]
            node_count += 1
            relname = elements[i+1]
            if relname == 'leaf':
                leaf_count += 1
                assert elements[i+2] == 't'
                seg_text = ''
                for j in range(i, len(elements)):
                    if elements[j] == ')':
                        break
                    if elements[j] in ['(', 'leaf', 't']:
                        continue
                    seg_text += ' ' + elements[j]
                node = Node(id = node_count, is_leaf=True, relname=seg_text, text=seg_text , leaf_number=leaf_count, parent=parent)
            else:
                node = Node(id = node_count, relname=elements[i+1], direction=elements[i+2], parent=parent)
            if parent is not None:
                parent.add_child(node)
            stack.insert(0, node)
            if root is None:
                root = stack[0]
        elif elements[i] == ')':
            stack.pop(0)
        else:
            continue
    return root



def traverse_tree(qud_tree, tree, node_count=1):
    parent_id = 'root'
    if tree.parent:
        parent_id = tree.parent.id
    qud_tree.create_node(str(node_count) + ' ' + tree.relname, tree.id, parent=parent_id)
    node_count = 0
    for child in tree.children:
        node_count += 1
        traverse_tree(qud_tree, child, node_count)



def traverse_tree_moved(qud_tree, tree, node_count=1):
    parent_id = 'root'
    if tree.parent:
        parent_id = tree.parent.id
    # TODO: Read from .seg_text attribute for leaf cases
    qud_tree.create_node(str(node_count) + " " + tree.relname, tree.id, parent=parent_id)
    
    dummy_node = Node(relname='satellite', is_leaf=False, parent=tree, id=str(tree.id) + '_dummy') 
    if tree.direction == 'l':
        sat = tree.children.pop(1)
        tree.children.insert(1, dummy_node)
        sat.parent = dummy_node
        dummy_node.children.append(sat)
    elif tree.direction == 'r':
        sat = tree.children.pop(0)
        tree.children.insert(0, dummy_node)
        sat.parent = dummy_node
        dummy_node.children.append(sat)
    node_count = 0
    for child in tree.children:
        node_count += 1
        traverse_tree_moved(qud_tree, child, node_count)



def write_qud_to_file_with_nesting(tree, fname):
    qud_tree = Tree()
    qud_tree.create_node("root", "root")
    traverse_tree_moved(qud_tree=qud_tree, tree=tree)
    if os.path.exists(fname):
        os.remove(fname)
    qud_tree.save2file(fname)
    return



def write_qud_to_file_without_nesting(tree, fname):
    qud_tree = Tree()
    qud_tree.create_node("root", "root")
    traverse_tree(qud_tree=qud_tree, tree=tree)
    if os.path.exists(fname):
        os.remove(fname)
    qud_tree.save2file(fname)
    return

def create_qud_tree_without_nesting(tree):
    qud_tree = Tree()
    qud_tree.create_node("root", "root")
    traverse_tree(qud_tree=qud_tree, tree=tree)
    return qud_tree



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Specify the path to the parenthetical rst trees')
    parser.add_argument('in_path', type=str)
    parser.add_argument('out_path', type=str)
    args = parser.parse_args()
    fnames = os.listdir(f"{args.in_path}")
    if not os.path.exists(args.out_path):
        raise Exception("Output path does not exist")
    
    if not os.path.exists(f"./{args.out_path}/nested"):
        os.mkdir(f"./{args.out_path}/nested")
    if not os.path.exists(f"./{args.out_path}/unnested"):
        os.mkdir(f"./{args.out_path}/unnested")

    for fname in fnames:
        if fname.endswith("tree"):
            with open(f"{args.in_path}/{fname}") as f:
                content = f.readlines()
                assert len(content) == 1,  "More lines than expected; one line expected per file and tree. Please look at the .tree samples in rst/parenthetical"
                tree_str = content[-1]
                tree = build_tree(tree_str)
                qud_name = fname.replace(".tree", ".qud")
                write_qud_to_file_without_nesting(tree, f'./qud-output/unnested/{qud_name}')
                write_qud_to_file_with_nesting(tree, f'./qud-output/nested/{qud_name}')

from treelib import Tree
import os
import argparse
from convert_rst2qud import * 


if __name__ == "__main__":
    # here, use this path as the in_path: rst/parenthetical
    parser = argparse.ArgumentParser(description='Specify the path to the parenthetical rst trees')
    parser.add_argument('in_path', type=str)
    args = parser.parse_args()
    fnames = os.listdir(f"{args.in_path}")
    for fname in fnames:
        if fname.endswith("tree"):
            with open(f"{args.in_path}/{fname}") as f:
                # read the parenthetical from file
                content = f.readlines()
                tree_str = content[-1]
                # build the tree
                rst_tree = build_tree(tree_str)
                # convert the tree. The output object is a treelib object. You use it for comparison. 
                converted_tree = create_qud_tree_without_nesting(rst_tree)
                

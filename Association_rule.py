import csv
from collections import defaultdict

# -------------------- FP-Growth Core Functions --------------------

class TreeNode:
    def __init__(self, name, count, parent):
        self.name = name
        self.count = count
        self.parent = parent
        self.children = {}
        self.nodeLink = None

    def increment(self, count):
        self.count += count


def update_header(node, target):
    while node.nodeLink is not None:
        node = node.nodeLink
    node.nodeLink = target


def update_tree(items, tree, header_table, count):
    first_item = items[0]
    if first_item in tree.children:
        tree.children[first_item].increment(count)
    else:
        new_node = TreeNode(first_item, count, tree)
        tree.children[first_item] = new_node

        if header_table[first_item][1] is None:
            header_table[first_item][1] = new_node
        else:
            update_header(header_table[first_item][1], new_node)

    if len(items) > 1:
        update_tree(items[1:], tree.children[first_item], header_table, count)


def create_tree(dataset, min_support):
    header_table = defaultdict(int)

    for transaction in dataset:
        for item in transaction:
            header_table[item] += dataset[transaction]

    header_table = {k: [v, None] for k, v in header_table.items() if v >= min_support}
    if len(header_table) == 0:
        return None, None

    tree = TreeNode("Null", 1, None)

    for transaction, count in dataset.items():
        local_items = {}
        for item in transaction:
            if item in header_table:
                local_items[item] = header_table[item][0]
        if local_items:
            ordered_items = [item[0] for item in sorted(local_items.items(), key=lambda x: -x[1])]
            update_tree(ordered_items, tree, header_table, count)

    return tree, header_table


def ascend_tree(node, path):
    if node.parent is not None:
        path.append(node.name)
        ascend_tree(node.parent, path)


def find_prefix_path(base_pat, node):
    cond_pats = {}
    while node is not None:
        path = []
        ascend_tree(node, path)
        if len(path) > 1:
            cond_pats[frozenset(path[1:])] = node.count
        node = node.nodeLink
    return cond_pats


def mine_tree(tree, header_table, min_support, prefix, freq_itemsets):
    sorted_items = [item[0] for item in sorted(header_table.items(), key=lambda x: x[1][0])]
    for base_pat in sorted_items:
        new_freq_set = prefix.copy()
        new_freq_set.add(base_pat)
        freq_itemsets[frozenset(new_freq_set)] = header_table[base_pat][0]
        cond_patt_bases = find_prefix_path(base_pat, header_table[base_pat][1])
        cond_tree, cond_header = create_tree(cond_patt_bases, min_support)
        if cond_header is not None:
            mine_tree(cond_tree, cond_header, min_support, new_freq_set, freq_itemsets)

# -------------------- Data & Utility Functions --------------------

def create_initial_dataset(data):
    dataset = {}
    for transaction in data:
        dataset[frozenset(transaction)] = dataset.get(frozenset(transaction), 0) + 1
    return dataset

def save_to_csv(data, filename, headers):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        writer.writerows(data)

custom_rules = [
    ({"Linear Algebra"}, {"Advance mathematics"}),
    ({"Linear Algebra", "Advance mathematics"}, {"Discrete mathematics"}),
    ({"C Language"}, {"Python programming"}),
    ({"C Language"}, {"Data Structures"}),
    ({"Advance mathematics"}, {"Data Structures", "Discrete mathematics"}),
    ({"C Language", "Python programming"}, {"Data Structures"}),
    ({"Python programming", "Data Structures"}, {"Discrete mathematics"}),
]

# -------------------- Input: Simulated Dataset --------------------

dataset = [
    ['Advance mathematics', 'Linear Algebra', 'Discrete mathematics', 'Data Structures'],
    ['Linear Algebra', 'Discrete mathematics'],
    ['Advance mathematics', 'Linear Algebra', 'Discrete mathematics'],
    ['Advance mathematics', 'Linear Algebra', 'Discrete mathematics', 'C Language'],
    ['Linear Algebra', 'Advance mathematics', 'Discrete mathematics'],
    ['Advance mathematics', 'Linear Algebra', 'Discrete mathematics', 'Data Structures', 'C Language'],
    ['Advance mathematics', 'Linear Algebra', 'Discrete mathematics', 'C Language'],
    ['Advance mathematics', 'Linear Algebra', 'Discrete mathematics'],
    ['Advance mathematics', 'Discrete mathematics', 'Data Structures'],
    ['C Language', 'Python programming', 'Data Structures'],
    ['C Language', 'Python programming', 'Data Structures'],
    ['Advance mathematics', 'Discrete mathematics', 'Data Structures'],
    ['C Language', 'Python programming', 'Data Structures'],
]

init_dataset = create_initial_dataset(dataset)

min_support = 2  # minimum support threshold

# -------------------- Run FP-Growth --------------------

fp_tree, header_table = create_tree(init_dataset, min_support)

frequent_itemsets = {}
if fp_tree is not None and header_table is not None:
    mine_tree(fp_tree, header_table, min_support, set(), frequent_itemsets)
else:
    print("No frequent itemsets found with the given minimum support.")


print("Frequent itemsets with their supports:")
for itemset, support in frequent_itemsets.items():
    print(set(itemset), support)

# -------------------- Save Frequent Itemsets to CSV --------------------

frequent_itemsets_list = [
    [', '.join(sorted(list(itemset))), support] for itemset, support in frequent_itemsets.items()
]

save_to_csv(frequent_itemsets_list, 'data/Frequent_Itemsets.csv',
            ['Frequent Itemset', 'Support'])

print("Frequent itemsets saved to 'data/Frequent_Itemsets.csv'")

# -------------------- Confidence Calculation --------------------

confidence_results = []

for antecedent, consequent in custom_rules:
    union = antecedent.union(consequent)
    support_union = frequent_itemsets.get(frozenset(union), 0)
    support_antecedent = frequent_itemsets.get(frozenset(antecedent), 0)

    if support_antecedent == 0:
        confidence = 0.0
    else:
        confidence = support_union / support_antecedent

    confidence_results.append([
        ', '.join(antecedent),
        ', '.join(consequent),
        round(confidence, 3)
    ])

# -------------------- Save Results --------------------

save_to_csv(confidence_results, 'data/FP_Image_Association_Confidence.csv',
            ['Antecedent', 'Consequent', 'Confidence'])

print("Confidence values saved to 'data/FP_Image_Association_Confidence.csv'")

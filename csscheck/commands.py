from csscheck.utils import check_included, display_list

def show_selectors_for_rule(mapping, rule, exact = False):
    if exact:
        display_list('Selectors for which "%s" is applied:' % rule,
                     mapping.get(rule, []))
        return

    for r in mapping:
        if check_included(rule, r):
            display_list('Selectors for which "%s" is applied:' % r,
                         mapping[r])

def show_rules_for_selector(mapping, selector, exact=False):
    if exact:
        display_list('Rules applied for "%s":' % selector,
                     mapping.get(selector, []))
        return

    for s in mapping:
        if check_included(selector, s):
            display_list('Rules applied for "%s":' % s,
                         mapping[s])

def show_multi_use(mapping):
    mapping_items = sorted(mapping.items(),
                       key = lambda m: len(m[1]),
                       reverse = True)

    for rule, selectors in mapping_items:
        if len(selectors) < 2 or not rule:
            continue
    
        display_list('Rule "%s" -  used %s times:' % (rule, len(selectors)),
                     selectors)

import os
import cssutils
import optparse

from csscheck.utils import dual_list_to_dict, endswith
from csscheck import commands

def build_css_file(path, css_files_ext = None):
    """ Returns a string containing all CSS
    files concatenated.
    """
    if css_files_ext is None:
        css_files_ext = ['.css', '.css.dtml']

    if path is None:
        path = '.'

    rules = ""
    for path, folders, filenames in os.walk(path):
        for filename in filenames:
            if not endswith(filename, css_files_ext):
                continue

            rules += open(path + os.sep + filename).read()

    return rules

def build_mappings(content):
    """  Builds the mapping dictionnaries rule_to_selectors and selector_to_rules
    form the content file.

    >>> build_mapping('')
    {}, {}

    >>> content = """
    ... my_selector {
    ...   display: none;
    ... }
    ... """
    >>> build_mapping(content)
    {'display: none;': ['my_selector']}, {'my_selector': ['display: none;']}

    >>> content = """
    ... my_selector {
    ...   display: none;
    ...   text-align: left;
    ... }
    ... another_selector {
    ...   text-align: left;
    ...   display: block;
    ... }
    ... """

    >>> build_mapping(content)
    {'display: none;': ['my_selector'],
     'display: block;': ['another_selector'],
     'text-align: left': ['my_selector, 'another_selector']},
    {'my_selector': ['display: none;', 'text-align: left;'],
     'another_selector': ['display: block;', 'text-align: left;'],
    }
    """
    sheet = cssutils.CSSParser(loglevel='CRITICAL').parseString(content, validate = False)
    rule_to_selectors = {}
    selector_to_rules = {}

    for rule in sheet.cssRules:
        try:
            selectors = [s.selectorText for s in rule.selectorList]
            applied = [r.strip() for r in rule.style.cssText.split('\n')]
        except AttributeError:
            # Might be a comment.
            continue

        dual_list_to_dict(rule_to_selectors, applied, selectors)
        dual_list_to_dict(selector_to_rules, selectors, applied)

    return rule_to_selectors, selector_to_rules


def main():
    parser = optparse.OptionParser()
    parser.add_option('-d', '--dir', dest='CSS_PATH', help='Directory where CSS files are stored')
    parser.add_option('-r', '--rule', dest='RULE', help='Rule to check')
    parser.add_option('-R', '--exact_rule', dest='EXACT_RULE', help='Rule to check (exact rule)')
    parser.add_option('-s', '--selector', dest='SELECTOR', help='Selector to check')
    parser.add_option('-S', '--exact_selector', dest='EXACT_SELECTOR', help='Selector to check (exact selector)')
    (options, args) = parser.parse_args()

    base_folder = options.CSS_PATH
    rules = build_css_file(base_folder)
    rule_to_selectors, selector_to_rules = build_mappings(rules)

    if options.RULE:
        commands.show_rules_for_selector(rule_to_selectors, options.RULE)
        return

    if options.EXACT_RULE:
        commands.show_rules_for_selector(rule_to_selectors,
                                         options.EXACT_RULE,
                                         exact = True)
        return

    if options.SELECTOR:
        commands.show_selectors_for_rule(selector_to_rules,
                                         options.SELECTOR)
        return

    if options.EXACT_SELECTOR:
        commands.show_selectors_for_rule(selector_to_rules,
                                         options.EXACT_SELECTOR,
                                         exact = True)
        return

    commands.show_multi_use(rule_to_selectors)

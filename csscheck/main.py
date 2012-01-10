import os
import cssutils
import optparse

from csscheck.utils import dual_list_to_dict, endswith
from csscheck import commands

def build_css_file(path, css_files_ext = None):
    """ Returns a string containing all CSS
    files concatenated.

    We first need a clean way to find the exact path of the samples directory.
    Once again this is some code stolen from Reinout or Maurits van Rees:
     - Reinout: http://reinout.vanrees.org/
     - Maurits: http://maurits.vanrees.org/
    >>> here = lambda *x: os.path.join(os.path.abspath(os.path.dirname(__file__)), *x)

    The samples directory list some simple CSS files and sub-directories:
    >>> print build_css_file(here('samples'))
    /* samples/file1.css */
    * {
        margin: 0px;
        padding: 0px;
    }/* samples/file2.css */
    .body {
        width: 800px;
    }
    <BLANKLINE>
    .footer {
        width: 800px;
    }/* This is a DTML file as used by Plone/Zope */
    <BLANKLINE>
    /* <dtml-with base_properties> (do not remove this :) */
    /* <dtml-call "REQUEST.set('portal_url', portal_url())"> (not this either :) */
    <BLANKLINE>
    body {
      font: &dtml-REALfontBaseSize; <dtml-var fontFamily>;
      background-color: &dtml-backgroundColor;;
      color: &dtml-fontColor;;
      margin: 0;
      padding: 0;
    }
    <BLANKLINE>
    /* </dtml-with> *//* A CSS file located in a sub-directory */
    <BLANKLINE>
    .overlay .close {
            background-image:url('overlay_close.png');
            position:absolute;
            left: -15px;
            top: -15px;
            cursor:pointer;
            height:35px;
            width:35px;
    }


    We can also specify custom extensions:
    >>> print build_css_file(here('samples'), ['.py'])
    # This Python file will not be read if we do not specify '.py' as a CSS extension.
    <BLANKLINE>

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
    """
    Builds the mapping dictionnaries rule_to_selectors and selector_to_rules
    form the content file.

    >>> build_mappings('')
    ({}, {})

    >>> content = 'my_selector {display: none; }'

    >>> build_mappings(content)
    ({u'display: none': [u'my_selector']}, {u'my_selector': [u'display: none']})

    >>> content = 'my_selector {display: none; text-align: left;}'
    >>> content += 'another_selector {text-align: left; display: block;}'
    >>> build_mappings(content)
    ({u'text-align: left': [u'my_selector', u'another_selector'],
      u'display: block': [u'another_selector'],
      u'display: none': [u'my_selector']},
     {u'my_selector': [u'display: none', u'text-align: left'],
      u'another_selector': [u'text-align: left', u'display: block']})
    """
    sheet = cssutils.CSSParser(loglevel='CRITICAL').parseString(content, validate = False)
    rule_to_selectors = {}
    selector_to_rules = {}

    for rule in sheet.cssRules:
        try:
            selectors = [s.selectorText for s in rule.selectorList]
            applied = [r.strip().replace(';', '') for r in rule.style.cssText.split('\n')]
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
        commands.show_selectors_for_rule(rule_to_selectors, options.RULE)
        return

    if options.EXACT_RULE:
        commands.show_selectors_for_rule(rule_to_selectors,
                                         options.EXACT_RULE,
                                         exact = True)
        return

    if options.SELECTOR:
        commands.show_rules_for_selector(selector_to_rules,
                                         options.SELECTOR)
        return

    if options.EXACT_SELECTOR:
        commands.show_rules_for_selector(selector_to_rules,
                                         options.EXACT_SELECTOR,
                                         exact = True)
        return

    commands.show_multi_use(rule_to_selectors)

if __name__ == '__main__':
    main()

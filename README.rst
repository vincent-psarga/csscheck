CSS check
=========

CSS check is a Python library/command line meant to help CSS
developers.

The main use is to see which CSS rule are applied to more than one
element in all your CSS files.

Install
-------

The tool can be installed using easy_install::

  easy_install csscheck


You can then define an alias to run the tool (in your .bashrc or
.profile file)::

  alias css_check="python -m csscheck.main"

If you have a buildout with the ``bin`` flder contained in your path,
you can add this part::

  [css_check]
  recipe = zc.recipe.egg
  eggs = csscheck

That will automatically create a new executable ``cs_check`` in the
``bin`` folder of your buildout.

Usage
-----

When you simply run the ``css_check`` command created earlier, it will
seek for all CSS files in the current directory (and sub-directories)
and provide the list of CSS rules applied to more than one element.
For example::

  Rule "display: block" -  used 4 times:
  ______________________________________
   - header
   - nav
   - article
   - footer


  Rule "background: #008BCD;" -  used 3 times:
  ____________________________________________
   - #main > header
   - #main > nav > ul > li
   - #main > footer


You can also specify the directory in which the CSS files must be
checked, using the ``-d`` option::

  css_check -d media/green_theme


You can also check for which elements a CSS rule is applied. To do so,
you can use the ``-r`` or ``--rule=`` option.
For example::

  css_check  --rule="display: block"


Those options will check all rules that contain the one you asked
for. So if you run ``css_check -r background``, the output will
be::

  Selectors for which "background: #F60;" is applied:
  ___________________________________________________
   - #main > header > nav
  
  
  Selectors for which "background: #89BEFC;" is applied:
  ______________________________________________________
   - body
  
  
  Selectors for which "background: #008BCD;" is applied:
  ______________________________________________________
   - #main > header
   - #main > nav > ul > li
   - #main > footer


You can use a strict rule checking using the ``-R`` or
``--exact_rule`` option. In that case, you'll get an exact
match. Running ``css_check -R background`` will not give any
result.

The tool also allows to know which rules are applied to a selector,
using the ``-s`` or ``--selector`` option.
For example, running ``css_check -s footer`` will output all
rules applied for selectors containing the work ``footer``::

  Rules applied for "#main > footer a:hover":
  ___________________________________________
   - text-decoration: underline
  
  
  Rules applied for "#main > footer a":
  _____________________________________
   - color: #FFF
  
  
  Rules applied for "#main > footer li":
  ______________________________________
   - display: inline


Once again, you can specify the exact selector, using options ``-S``
or ``--exact_selector``.
Running the command ``css_check -S footer`` will only output
this::

  Rules applied for "footer":
  ___________________________
   - display: block


The option used to specify the CSS directory is compatible with all
other options. The other options can't be mixed (you can't specify a
selector and a rule for example).



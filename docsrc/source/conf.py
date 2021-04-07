# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys
from pygit2 import Repository

sys.path.insert(0, os.path.abspath('../../pyblazing'))
sys.setrecursionlimit(1500)

# -- Project information -----------------------------------------------------

project = 'BlazingSQL'
copyright = '2020, BlazingDB, Inc'
author = 'BlazingDB, Inc.'

# import blazingsql  # isort:skip

# # version = '%s r%s' % (pandas.__version__, svn_version())
# version = str(blazingsql.__version__)

# # The full version, including alpha/beta/rc tags.
# release = version

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
language = "en"

# detect version
repo = Repository('./')
head = repo.head
git_branch = head.name.replace('/refs/heads/','')

# The full version, including alpha/beta/rc tags
version = 'latest'
if 'branch-' in git_branch:
    version = git_branch.replace('branch-','')
    release = f'v{version}'
else:
    release = version
print('Version: ' + version + ' Release: ' + release)

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = ['recommonmark',
                "sphinx_multiversion",
                'sphinx.ext.extlinks',
                'sphinx.ext.todo',
                'sphinx.ext.autodoc',
                'sphinx.ext.autosummary',
                'breathe',
                'exhale'
                ]

autosummary_generate = True 
autosummary_imported_members = False

# Setup the exhale extension
exhale_args = {
    # These arguments are required
    "containmentFolder":     "./xml",
    "rootFileName":          "library_root.rst",
    "rootFileTitle":         "Library API",
    "doxygenStripFromPath":  "..",
    # Suggested optional arguments
    "createTreeView":        True,
    # TIP: if using the sphinx-bootstrap-theme, you need
    #"treeViewIsBootstrap": True
    "exhaleExecutesDoxygen": True,
    "exhaleUseDoxyfile": True
}

# Setup the breathe extension
breathe_projects = {
    "BlazingSQL Engine": "./xml"
}
breathe_default_project = "BlazingSQL Engine"

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# Tell sphinx what the primary language being documented is.
primary_domain = 'py'

# Tell sphinx what the pygments highlight language should be.
highlight_language = 'py'

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['build', 'Thumbs.db', '.DS_Store']


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'sphinx_book_theme'

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = "sphinx"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

html_css_files = [
    "css/getting_started.css",
    "css/blazingsql.css",
    "css/theme.css",
    "css/pandas.css"
]
# The name of an image file (relative to this directory) to place at the top
# of the sidebar.
html_logo = "_static/icons/svg/blazingsql_logo.svg"

html_favicon = "_static/icons/blazingsql-icon.ico"

# If false, no module index is generated.
html_use_modindex = True

html_theme_options = {
    "twitter_url": "https://twitter.com/blazingsql"
    , "repository_url": "https://github.com/BlazingDB/blazingsql"
    , "use_repository_button": True
    , "use_issues_button": True
    , "search_bar_position": "sidebar"
    , "search_bar_text": "Search BlazingSQL Docs"
    , "show_prev_next": True
    , 'body_max_width': '1200px'
    , "use_edit_page_button": True
    , "external_links": [
        # {"name": "BlazingSQL", "url": "https://blazingsql.com"}
    ]
    , "show_toc_level": "3"
    , "navigation_with_keys": True
}

extlinks = {'io': (f'https://github.com/rapidsai/cudf/tree/branch-{version}/cpp/src/%s',
                      'cuIO ')}

html_context = {
    "github_user": "blazingdb",
    "github_repo": "blazingsql",
    "github_version": "feedback",
    "doc_path": "docsrc/source",
}

html_sidebars = {
    "**": ["versioning.html","sidebar-search-bs.html","sbt-sidebar-nav.html", "sbt-sidebar-footer.html"]
}
# Override tags for sphinx multiversion
smv_tag_whitelist = None

# Include branch version and main branch for sphinx multiversion
smv_branch_whitelist = r'^(branch.|main).*$'

# Multiversion realease
smv_released_pattern = r'^(tags/v.*|heads/branch.*)$'

# Multiversion configure remote
smv_remote_whitelist = r'^origin/branch-.*$'

def skip(app, what, name, obj, would_skip, options):
    if name == "__init__":
        return True
    elif name[0] == '_':
        return True
    return would_skip

import sphinx  # isort:skip
from sphinx.util import rpartition  # isort:skip
from sphinx.ext.autodoc import (  # isort:skip
    AttributeDocumenter,
    Documenter,
    MethodDocumenter,
)
from sphinx.ext.autosummary import Autosummary  # isort:skip


class AccessorDocumenter(MethodDocumenter):
    """
    Specialized Documenter subclass for accessors.
    """

    objtype = "accessor"
    directivetype = "method"

    # lower than MethodDocumenter so this is not chosen for normal methods
    priority = 0.6

    def format_signature(self):
        # this method gives an error/warning for the accessors, therefore
        # overriding it (accessor has no arguments)
        return ""


class AccessorLevelDocumenter(Documenter):
    """
    Specialized Documenter subclass for objects on accessor level (methods,
    attributes).
    """

    # This is the simple straightforward version
    # modname is None, base the last elements (eg 'hour')
    # and path the part before (eg 'Series.dt')
    # def resolve_name(self, modname, parents, path, base):
    #     modname = 'pandas'
    #     mod_cls = path.rstrip('.')
    #     mod_cls = mod_cls.split('.')
    #
    #     return modname, mod_cls + [base]
    def resolve_name(self, modname, parents, path, base):
        if modname is None:
            if path:
                mod_cls = path.rstrip(".")
            else:
                mod_cls = None
                # if documenting a class-level object without path,
                # there must be a current class, either from a parent
                # auto directive ...
                mod_cls = self.env.temp_data.get("autodoc:class")
                # ... or from a class directive
                if mod_cls is None:
                    mod_cls = self.env.temp_data.get("py:class")
                # ... if still None, there's no way to know
                if mod_cls is None:
                    return None, []
            # HACK: this is added in comparison to ClassLevelDocumenter
            # mod_cls still exists of class.accessor, so an extra
            # rpartition is needed
            modname, accessor = rpartition(mod_cls, ".")
            modname, cls = rpartition(modname, ".")
            parents = [cls, accessor]
            # if the module name is still missing, get it like above
            if not modname:
                modname = self.env.temp_data.get("autodoc:module")
            if not modname:
                if sphinx.__version__ > "1.3":
                    modname = self.env.ref_context.get("py:module")
                else:
                    modname = self.env.temp_data.get("py:module")
            # ... else, it stays None, which means invalid
        return modname, parents + [base]


class AccessorAttributeDocumenter(AccessorLevelDocumenter, AttributeDocumenter):
    objtype = "accessorattribute"
    directivetype = "attribute"

    # lower than AttributeDocumenter so this is not chosen for normal
    # attributes
    priority = 0.6


class AccessorMethodDocumenter(AccessorLevelDocumenter, MethodDocumenter):
    objtype = "accessormethod"
    directivetype = "method"

    # lower than MethodDocumenter so this is not chosen for normal methods
    priority = 0.6


class AccessorCallableDocumenter(AccessorLevelDocumenter, MethodDocumenter):
    """
    This documenter lets us removes .__call__ from the method signature for
    callable accessors like Series.plot
    """

    objtype = "accessorcallable"
    directivetype = "method"

    # lower than MethodDocumenter; otherwise the doc build prints warnings
    priority = 0.5

    def format_name(self):
        return MethodDocumenter.format_name(self).rstrip(".__call__")

def rstjinja(app, docname, source):
    """
    Render our pages as a jinja template for fancy templating goodness.
    """
    # https://www.ericholscher.com/blog/2016/jul/25/integrating-jinja-rst-sphinx/
    # Make sure we're outputting HTML
    if app.builder.format != "html":
        return
    src = source[0]
    rendered = app.builder.templates.render_string(src, app.config.html_context)
    source[0] = rendered

def setup(app):
    app.add_js_file("js/d3.v3.min.js")
    app.connect("autodoc-skip-member", skip)
    # app.connect("source-read", rstjinja)
    # app.connect("autodoc-process-docstring", remove_flags_docstring)
    # app.connect("autodoc-process-docstring", process_class_docstrings)
    # app.connect("autodoc-process-docstring", process_business_alias_docstrings)
    app.add_autodocumenter(AccessorDocumenter)
    app.add_autodocumenter(AccessorAttributeDocumenter)
    app.add_autodocumenter(AccessorMethodDocumenter)
    app.add_autodocumenter(AccessorCallableDocumenter)

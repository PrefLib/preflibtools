# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line, and also
# from the environment for the first two.
SPHINXOPTS    	?=
SPHINXBUILD		?= sphinx-build
SOURCEDIR     	= source
LOCALBUILDDIR	= build
GITHUBBUILDDIR	= ../docs

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(LOCALBUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help Makefile

# To produced the docs for the github pages
github:
	touch "$(GITHUBBUILDDIR)/.nojekyll"
	@$(SPHINXBUILD) -b html "$(SOURCEDIR)" "$(GITHUBBUILDDIR)" $(SPHINXOPTS) $(O)
githubclean:
	@$(SPHINXBUILD) -M clean "$(SOURCEDIR)" "$(GITHUBBUILDDIR)" $(SPHINXOPTS) $(O)

html:
	@$(SPHINXBUILD) -b html "$(SOURCEDIR)" "$(LOCALBUILDDIR)" $(SPHINXOPTS) $(O)
# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(LOCALBUILDDIR)" $(SPHINXOPTS) $(O)
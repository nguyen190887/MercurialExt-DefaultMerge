# default-merge is an extension used to merge the code from 'default' branch to a given branch.
# The purpose of this extension is to reduce effort to update, then merge, then update to another branch.
# This would help development team perform 'daily merge with default' task faster.

# Documentation on writing mecurial extensions and using their api and hooks:
# http://mercurial.selenic.com/wiki/WritingExtensions
# http://mercurial.selenic.com/wiki/MercurialApi
# http://mercurial.selenic.com/wiki/Hook
# http://www.selenic.com/hg/help/hgrc
# http://hgbook.red-bean.com/read/handling-repository-events-with-hooks.html
# and of course the mercurial source code (specifically files commands.py, localrepo.py, context.py, ui.py, hg.py, util.py and bookmarks.py)

"""defaultmerge

To merge code from 'default' branch to a given branch.
"""
from mercurial import commands, extensions, util, hg, ui
repo = hg.repository(ui.ui(), path=".")

def repomerge(ui, node = None):
    """perform merge code action
    """
    currentCtx = repo[None].parents()[0]
    # ui.write(currentCtx.description())
    currentRev = currentCtx.rev()
    ui.write('Updating to revision %s \n' % node)
    hg.updaterepo(repo, node, True)
    defaultRev = repo['default'].rev()
    ui.write('Merging with default revision %s \n' % defaultRev)
    hg.merge(repo, defaultRev)
    ui.write('Committing after merge... \n')
    repo.commit('Story: B-12345 | Merge with default') #TODO: enter story name based on ctx.description()
    ui.write('Revert to original revision %s \n' % currentRev)
    hg.update(repo, currentRev)


cmdtable = {
    'repo-merge': (repomerge, [], 'Auto merge from default to given repository.')
}
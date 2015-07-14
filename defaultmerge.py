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
import re
from mercurial.i18n import _
from mercurial import cmdutil, hg, ui
# repo = hg.repository(ui.ui(), path=".")

cmdtable = {}
command = cmdutil.command(cmdtable)

def getMergeDescription(parentDesc):
    '''Returns merge description - e.g. Story: 12345 | Merge to default
    '''
    match = re.search('^((BugId: [0-9]+ \|)|(Story: B-[0-9]+ \|)|(Epic: E-[0-9]+ \|))', parentDesc)
    return match.group(0) + ' Merge with default'

@command("domerge",
         [
          ('r', 'rev', [], _('revision to merge'))],
          _('hg domerge [-r] REV...'))
def domergecmd(ui, repo, *revs, **opts):
    node = (list(revs) + opts.get('rev'))[0]
    originalCtx = repo[None].parents()[0]
    originalRev = originalCtx.rev()

    ui.write('Updating to revision %s \n' % node)
    hg.updaterepo(repo, node, True)
    defaultRev = repo['default'].rev()
    
    ui.write('Merging with default revision %s \n' % defaultRev)
    hg.merge(repo, defaultRev)

    #TODO: handle conflict case
    
    ui.write('Committing after merge... \n')
    commitMsg = getMergeDescription(repo[None].parents()[0].description())
    
    ui.write('   Commit message: %s \n' % commitMsg)
    repo.commit(commitMsg)

    if (originalRev != repo[None].parents()[0].parents()[0].rev()): # update to original rev in case branches are different
        ui.write('Updating to original revision %s \n' % originalRev)
        hg.update(repo, originalRev)

    return 0
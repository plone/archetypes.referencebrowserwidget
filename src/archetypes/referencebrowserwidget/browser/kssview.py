from kss.core import KSSView

class KSSMoveReferencesView(KSSView):

    idpat = 'ref-%s-%s'
    kssattrpat = "kssattr-pos-%s kssattr-length-%s kssattr-field-%s"

    def _move(self, pos, newpos, length, field):
        currid = self.idpat % (field, pos)
        newid = self.idpat % (field, newpos)

        selector = 'li#' + currid

        core = self.getCommandSet('core')
        if pos > newpos:
            core.moveNodeBefore(selector, newid)
            core.setAttribute('li#' + newid, 'id', currid)
            core.setAttribute(selector, 'id', newid)
        else:
            core.moveNodeAfter(selector, newid)
            core.setAttribute(selector, 'id', newid)
            core.setAttribute('li#' + newid, 'id', currid)

        # fix kss-attributes of changed items
        for htmlid, p in zip([currid, newid], [pos, newpos]):
            kssattr = self.kssattrpat % (p, length, field)

            core.setAttribute('li#%s img.moveUp' % htmlid,
                              'class',
                              'moveUp %s' % kssattr)
            core.setAttribute('li#%s img.moveDown' % htmlid,
                              'class',
                              "moveDown %s" % kssattr)

    def moveUp(self, pos, length, field):
        if pos:
            pos = int(pos)
            self._move(pos, pos-1, length, field)

        return self.render()

    def moveDown(self, pos, length, field):
        pos = int(pos)
        if pos < int(length)-1:
            self._move(pos, pos+1, length, field)

        return self.render()


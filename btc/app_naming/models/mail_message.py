from odoo import api, fields, models, _

class MailCreationUpd(models.AbstractModel):
    _inherit = "mail.thread"
    _description = "Update Mail Message Creation"

    @api.model
    def _creation_message(self):
        """ Get the creation message to log into the chatter at the record's creation.
        :returns: The message's body to log.
        """
        self.ensure_one()
        doc_name = self.env['ir.model']._get(self._name).name

        if self._name == 'purchase.order':
            doc_name = ('Check In Documentation')

        return _('%s created', doc_name)

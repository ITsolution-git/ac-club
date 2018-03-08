# -*- coding: utf-8 -*-

from odoo import models, fields, api
import odoo.addons.decimal_precision as dp

class HotelRoomType(models.Model):

    _name = "hotel.room.type"
    _description = "Room Type"

    name = fields.Char('Name', size=64, required=True)

class HotelFloor(models.Model):

    _name = "hotel.floor"
    _description = "Floor"

    name = fields.Char('Floor Name', size=64, required=True, index=True)
    sequence = fields.Integer('Sequence', size=64, index=True)

class HotelRoom(models.Model):

    _name = 'hotel.room'
    _description = 'Hotel Room'

    name = fields.Char('Name', index=True, required=True, translate=True)

    '''product_id = fields.Many2one('product.product', 'Product_id',
                                 required=True, delegate=True,
                                 ondelete='cascade') '''

    floor_id = fields.Many2one('hotel.floor', 'Floor No',
                               help='At which floor the room is located.')

    '''max_adult = fields.Integer('Max Adult')
    max_child = fields.Integer('Max Child')'''

    categ_id = fields.Many2one('hotel.room.type', string='Room Category',
                               required=True)
    room_amenities = fields.Many2many('hotel.room.amenities', 'temp_tab',
                                      'room_amenities', 'rcateg_id',
                                      string='Room Amenities',
                                      help='List of room amenities. ')
    status = fields.Selection([('available', 'Available'),
                               ('occupied', 'Occupied')],
                              'Status', default='available')
    capacity = fields.Integer('Capacity', required=True)
    num_of_room = fields.Integer('Number Of Rooms')

    ''' room_line_ids = fields.One2many('folio.room.line', 'room_id',
                                    string='Room Reservation Line')
    product_manager = fields.Many2one('res.users', string='Product Manager')'''

    image_medium = fields.Binary(
        "Medium-sized image", attachment=True,
        help="Medium-sized image of the product. It is automatically "
             "resized as a 128x128px image, with aspect ratio preserved, "
             "only when the image exceeds one of those sizes. Use this field in form views or some kanban views.")


    price = fields.Float('Price per Day')
    area = fields.Float('Room Area')

    description = fields.Text(
        'Description', translate=True,
        help="")

    @api.constrains('capacity')
    def check_capacity(self):
        for room in self:
            if room.capacity <= 0:
                raise ValidationError(_('Room capacity must be more than 0'))

    '''@api.onchange('isroom')
    def isroom_change(self): 
        # Based on isroom, status will be updated.
        # ----------------------------------------
        # @param self: object pointer

        if self.isroom is False:
            self.status = 'occupied'
        if self.isroom is True:
            self.status = 'available'

    @api.multi
    def write(self, vals):
        """
        Overrides orm write method.
        @param self: The object pointer
        @param vals: dictionary of fields value.
        """
        if 'isroom' in vals and vals['isroom'] is False:
            vals.update({'color': 2, 'status': 'occupied'})
        if 'isroom'in vals and vals['isroom'] is True:
            vals.update({'color': 5, 'status': 'available'})
        ret_val = super(HotelRoom, self).write(vals)
        return ret_val

    @api.multi
    def set_room_status_occupied(self):
        """
        This method is used to change the state
        to occupied of the hotel room.
        ---------------------------------------
        @param self: object pointer
        """
        return self.write({'isroom': False, 'color': 2})

    @api.multi
    def set_room_status_available(self):
        """
        This method is used to change the state
        to available of the hotel room.
        ---------------------------------------
        @param self: object pointer
        """
        return self.write({'isroom': True, 'color': 5})
    '''

class HotelRoomAmenitiesType(models.Model):

    _name = 'hotel.room.amenities.type'
    _description = 'amenities Type'

    name = fields.Char('Name', size=64, required=True)
    amenity_id = fields.Many2one('hotel.room.amenities.type', 'Category')
    child_id = fields.One2many('hotel.room.amenities.type', 'amenity_id',
                               'Child Categories')

    @api.multi
    def name_get(self):
        def get_names(cat):
            """ Return the list [cat.name, cat.amenity_id.name, ...] """
            res = []
            while cat:
                res.append(cat.name)
                cat = cat.amenity_id
            return res
        return [(cat.id, " / ".join(reversed(get_names(cat)))) for cat in self]

    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        if not args:
            args = []
        if name:
            # Be sure name_search is symetric to name_get
            category_names = name.split(' / ')
            parents = list(category_names)
            child = parents.pop()
            domain = [('name', operator, child)]
            if parents:
                names_ids = self.name_search(' / '.join(parents), args=args,
                                             operator='ilike', limit=limit)
                category_ids = [name_id[0] for name_id in names_ids]
                if operator in expression.NEGATIVE_TERM_OPERATORS:
                    categories = self.search([('id', 'not in', category_ids)])
                    domain = expression.OR([[('amenity_id', 'in',
                                              categories.ids)], domain])
                else:
                    domain = expression.AND([[('amenity_id', 'in',
                                               category_ids)], domain])
                for i in range(1, len(category_names)):
                    domain = [[('name', operator,
                                ' / '.join(category_names[-1 - i:]))], domain]
                    if operator in expression.NEGATIVE_TERM_OPERATORS:
                        domain = expression.AND(domain)
                    else:
                        domain = expression.OR(domain)
            categories = self.search(expression.AND([domain, args]),
                                     limit=limit)
        else:
            categories = self.search(args, limit=limit)
        return categories.name_get()

class HotelRoomAmenities(models.Model):

    _name = 'hotel.room.amenities'
    _description = 'Room amenities'

    product_id = fields.Many2one('product.product', 'Product Category',
                                 required=True, delegate=True,
                                 ondelete='cascade')
    categ_id = fields.Many2one('hotel.room.amenities.type',
                               string='Amenities Category', required=True)

    quantity = fields.Integer('Sequence', default=1, required=True)


class HotelServiceType(models.Model):

    _name = "hotel.service.type"
    _description = "Service Type"

    name = fields.Char('Service Name', size=64, required=True)
    service_id = fields.Many2one('hotel.service.type', 'Service Category')
    child_id = fields.One2many('hotel.service.type', 'service_id',
                               'Child Categories')

    @api.multi
    def name_get(self):
        def get_names(cat):
            """ Return the list [cat.name, cat.service_id.name, ...] """
            res = []
            while cat:
                res.append(cat.name)
                cat = cat.service_id
            return res
        return [(cat.id, " / ".join(reversed(get_names(cat)))) for cat in self]

    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        if not args:
            args = []
        if name:
            # Be sure name_search is symetric to name_get
            category_names = name.split(' / ')
            parents = list(category_names)
            child = parents.pop()
            domain = [('name', operator, child)]
            if parents:
                names_ids = self.name_search(' / '.join(parents), args=args,
                                             operator='ilike', limit=limit)
                category_ids = [name_id[0] for name_id in names_ids]
                if operator in expression.NEGATIVE_TERM_OPERATORS:
                    categories = self.search([('id', 'not in', category_ids)])
                    domain = expression.OR([[('service_id', 'in',
                                              categories.ids)], domain])
                else:
                    domain = expression.AND([[('service_id', 'in',
                                               category_ids)], domain])
                for i in range(1, len(category_names)):
                    domain = [[('name', operator,
                                ' / '.join(category_names[-1 - i:]))], domain]
                    if operator in expression.NEGATIVE_TERM_OPERATORS:
                        domain = expression.AND(domain)
                    else:
                        domain = expression.OR(domain)
            categories = self.search(expression.AND([domain, args]),
                                     limit=limit)
        else:
            categories = self.search(args, limit=limit)
        return categories.name_get()


class HotelServices(models.Model):

    _name = 'hotel.services'
    _description = 'Hotel Services and its charges'

    product_id = fields.Many2one('product.product', 'Service_id',
                                 required=True, ondelete='cascade',
                                 delegate=True)
    categ_id = fields.Many2one('hotel.service.type', string='Service Category',
                               required=True)


class Card(models.Model):

    _name = 'hotel.card'
    _description = 'Hotel Room Cards and Member Cards'

    card_id = fields.Char('Card ID', required=True)
    balance = fields.Float('Cost', default=0, digits=dp.get_precision('Product Price'))
    type = fields.Selection([
        ('room', 'Room Card'),
        ('member', 'Member Card')], 'Category Type', default='room',
        help="")
    active = fields.Boolean(default=True) 
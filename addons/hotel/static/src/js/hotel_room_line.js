odoo.define('hotel.hotel_room_line', function (require) {
	"use strict";
	var form_widget = require('web.form_widgets');
	var core = require('web.core');
	// const io = require('socket.io-client');
	var _t = core._t;
	var QWeb = core.qweb;
	var socket = io('http://localhost:31556');
	var NotificationManager = require('web.notification').NotificationManager;
	console.log("socket connect!");

	form_widget.WidgetButton.include({
		on_click: function() {
			if(this.node.attrs.custom === "issue_card"){
				if (this.field_manager.datarecord.state == "sale" || this.field_manager.datarecord.state == "draft"){
					socket.emit('issue_card', this.field_manager.datarecord);
				} else {
					if (!this.connection_notification) {
						this.notification_manager = new NotificationManager(this);
						this.notification_manager.appendTo(this.$el);
					}
					this.connection_notification = this.notification_manager.warn(
						_t('Folio must be confirmed for sale.'),
						_t('please make this folio \'sale\'...'),
						false
					);
				}
				return;
			}
			else if (this.node.attrs.custom === "delete_card") {
				socket.emit('delete_card', this.field_manager.datarecord);
				return;
			}
			else if(this.node.attrs.custom === "issue_card_hr"){
				socket.emit('issue_card_hr', this.field_manager.datarecord);
			}
			else if(this.node.attrs.custom === "delete_card_hr"){
				socket.emit('delete_card_hr', this.field_manager.datarecord);
			}
			else if(this.node.attrs.custom === "issue_card_customer"){
				socket.emit('issue_card_hr', this.field_manager.datarecord);
			}
			else if(this.node.attrs.custom === "delete_card_customer"){
				socket.emit('delete_card_hr', this.field_manager.datarecord);
			}
			this._super();
		},
	});
});

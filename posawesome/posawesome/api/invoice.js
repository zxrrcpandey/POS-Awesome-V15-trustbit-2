// Copyright (c) 2021 Youssef Restom and contributors
// For license information, please see license.txt

frappe.ui.form.on('Sales Invoice', {
    setup: function (frm) {
        frm.set_query("posa_delivery_charges", function (doc) {
            return {
                filters: { 'company': doc.company, 'disabled': 0 }
            };
        });
    },
});

// Sales Invoice Item - UOM Discount Feature
frappe.ui.form.on('Sales Invoice Item', {
    item_code: function(frm, cdt, cdn) {
        setTimeout(() => {
            let row = locals[cdt][cdn];
            if (row.item_code && row.uom) {
                apply_uom_discount_to_invoice_item(frm, row);
            }
        }, 500);
    },
    uom: function(frm, cdt, cdn) {
        setTimeout(() => {
            let row = locals[cdt][cdn];
            if (row.item_code && row.uom) {
                apply_uom_discount_to_invoice_item(frm, row);
            }
        }, 300);
    },
    qty: function(frm, cdt, cdn) {
        setTimeout(() => {
            let row = locals[cdt][cdn];
            if (row.item_code && row.uom) {
                apply_uom_discount_to_invoice_item(frm, row);
            }
        }, 300);
    }
});

function apply_uom_discount_to_invoice_item(frm, row) {
    frappe.call({
        method: 'posawesome.posawesome.api.posapp.get_item_uom_discount_for_cart',
        args: {
            item_code: row.item_code,
            uom: row.uom,
            qty: Math.abs(row.qty || 1)
        },
        callback: function(r) {
            if (r.message && flt(r.message) > 0) {
                let discount_percentage = flt(r.message);
                if (flt(row.discount_percentage) !== discount_percentage) {
                    frappe.model.set_value(row.doctype, row.name, 'discount_percentage', discount_percentage);
                    frappe.show_alert({
                        message: __('UOM Discount Applied: {0}% for {1}', [discount_percentage, row.uom]),
                        indicator: 'green'
                    }, 3);
                }
            }
        }
    });
}
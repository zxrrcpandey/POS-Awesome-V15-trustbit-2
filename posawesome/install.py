# Copyright (c) 2026, Trustbit Software and contributors
# For license information, please see license.txt

import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields


def after_install():
    create_item_uom_discount_custom_fields()
    create_sales_invoice_uom_discount_script()
    show_discount_column_in_invoice_items()


def create_item_uom_discount_custom_fields():
    """Create custom fields for Item UOM Discount feature."""
    custom_fields = {
        "Item": [
            {
                "fieldname": "posa_item_uom_discount_section",
                "label": "POS UOM Discount",
                "fieldtype": "Section Break",
                "insert_after": "barcodes",
                "collapsible": 1,
            },
            {
                "fieldname": "posa_item_uom_discounts",
                "label": "Item UOM Discounts",
                "fieldtype": "Table",
                "options": "Item UOM Discount",
                "insert_after": "posa_item_uom_discount_section",
                "description": "Configure automatic discounts based on UOM selection in POS",
            },
        ],
        "POS Profile": [
            {
                "fieldname": "posa_use_item_uom_discount",
                "label": "Apply Item UOM Discount",
                "fieldtype": "Check",
                "insert_after": "posa_allow_zero_rated_items",
                "description": "When enabled, discounts configured in Item's 'POS UOM Discount' section will be automatically applied",
            },
        ],
    }
    create_custom_fields(custom_fields, update=True)
    frappe.db.commit()


def create_sales_invoice_uom_discount_script():
    """Create Client Script for Sales Invoice UOM Discount."""
    script_name = "Sales Invoice UOM Discount"

    # Check if script already exists
    if frappe.db.exists("Client Script", script_name):
        return

    script_code = """
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
"""

    doc = frappe.get_doc({
        "doctype": "Client Script",
        "name": script_name,
        "dt": "Sales Invoice",
        "view": "Form",
        "enabled": 1,
        "script": script_code
    })
    doc.insert(ignore_permissions=True)
    frappe.db.commit()


def show_discount_column_in_invoice_items():
    """Show discount and rate columns in Sales Invoice Item table for better visibility."""
    from frappe.custom.doctype.property_setter.property_setter import make_property_setter

    # Show price_list_rate (Rate Before Discount) in list view
    make_property_setter("Sales Invoice Item", "price_list_rate", "in_list_view", 1, "Check", for_doctype=False)
    make_property_setter("Sales Invoice Item", "price_list_rate", "columns", 2, "Int", for_doctype=False)

    # Show discount_percentage in list view
    make_property_setter("Sales Invoice Item", "discount_percentage", "in_list_view", 1, "Check", for_doctype=False)
    make_property_setter("Sales Invoice Item", "discount_percentage", "columns", 1, "Int", for_doctype=False)

    # Show rate (Rate After Discount) in list view
    make_property_setter("Sales Invoice Item", "rate", "in_list_view", 1, "Check", for_doctype=False)
    make_property_setter("Sales Invoice Item", "rate", "columns", 2, "Int", for_doctype=False)

    # Show amount (Total) in list view
    make_property_setter("Sales Invoice Item", "amount", "in_list_view", 1, "Check", for_doctype=False)
    make_property_setter("Sales Invoice Item", "amount", "columns", 2, "Int", for_doctype=False)

    # Set column widths for item_code and qty
    make_property_setter("Sales Invoice Item", "item_code", "columns", 3, "Int", for_doctype=False)
    make_property_setter("Sales Invoice Item", "qty", "columns", 1, "Int", for_doctype=False)

    # Hide warehouse to save space
    make_property_setter("Sales Invoice Item", "warehouse", "in_list_view", 0, "Check", for_doctype=False)

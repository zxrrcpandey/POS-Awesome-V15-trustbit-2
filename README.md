<div align="center">
    <img src="https://frappecloud.com/files/pos.png" height="128">
    <h2>POS AWESOME</h2>
</div>

#### An open-source Point of Sale for [Erpnext](https://github.com/frappe/erpnext) using [Vue.js](https://github.com/vuejs/vue) and [Vuetify](https://github.com/vuetifyjs/vuetify) (VERSION 15 Support)

---

### Main Features

1. Supports Erpnext Version 15
2. Supports Multi-Currency Transactions.
    Customers can be invoiced in different currencies
    Exchange Rate is fetched automatically based on selected currency
    Invoices made with posawesome display Grand Total in both base and selected currency in erpnext.

3. User-friendly and provides a good user experience and speed of use
4. The cashier can either use list view or card view during sales transactions. Card view shows the images of the items
5. Supports enqueue invoice submission after printing the receipt for faster processing
6. Supports batch & serial numbering
7. Supports batch-based pricing
8. Supports UOM-specific barcode and pricing
9. Supports sales of scale (weighted) products
10. Ability to make returns from POS
11. Supports Making returns for either cash or customer credit
12. Supports using customer credit notes for payment
13. Supports credit sales
14. Allows the user to choose a due date for credit sales
15. Supports customer loyalty points
16. Shortcut keys
17. Supports Customer Discount
18. Supports POS Offers
19. Auto-apply batches for bundle items
20. Search and add items by Serial Number
21. Create Sales Orders from POS directly
22. Supports template items with variants
23. Supports multiple languages
24. Supports Mpesa mobile payment
25. POS Coupons
26. Supports Referral Code
27. Supports Customer and Customer Group price list
28. Supports Sales Person
29. Supports Delivery Charges
30. Search and add items by Batch Number
31. Accept new payments from customers against existing invoices
32. Payments Reconciliation
33. A lot more bug fixes from the version 14

---

### Trustbit Customizations (v2.0)

This fork includes additional features and improvements by Trustbit Software:

#### Item UOM Discount Feature
Automatically apply discounts based on Unit of Measure (UOM) and quantity tiers.

**How it works:**
- Configure discounts in Item master under "UOM Discounts" table
- Set UOM, Discount Percentage, Min Qty, and Max Qty for each tier
- Discount automatically applies when item is added to cart
- Discount updates when quantity changes (manual entry or +/- buttons)
- Discount updates when UOM changes
- Multiple quantity tiers supported (e.g., 5% for 1-10 units, 10% for 11-50 units)

**Setup:**
1. Enable "Use Item UOM Discount" in POS Profile
2. Add discount entries in Item master > UOM Discounts table
3. Run `bench --site [site] migrate` after installation

**Bulk Upload UOM Discounts:**

Since `Item UOM Discount` is a child table, use one of these methods:

*Method 1: Via bench console*
```python
# bench --site [site] console
import frappe

discounts = [
    {"item": "ITEM-001", "uom": "Nos", "discount": 5, "min": 1, "max": 10},
    {"item": "ITEM-001", "uom": "Nos", "discount": 10, "min": 11, "max": 0},
]

for d in discounts:
    frappe.get_doc({
        "doctype": "Item UOM Discount",
        "parent": d["item"],
        "parenttype": "Item",
        "parentfield": "posa_item_uom_discounts",
        "uom": d["uom"],
        "discount_percentage": d["discount"],
        "min_qty": d["min"],
        "max_qty": d["max"]
    }).db_insert()

frappe.db.commit()
```

*Method 2: From CSV file*
```python
import frappe, csv

with open('/path/to/discounts.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        frappe.get_doc({
            "doctype": "Item UOM Discount",
            "parent": row["item_code"],
            "parenttype": "Item",
            "parentfield": "posa_item_uom_discounts",
            "uom": row["uom"],
            "discount_percentage": float(row["discount_percentage"]),
            "min_qty": float(row.get("min_qty", 0)),
            "max_qty": float(row.get("max_qty", 0))
        }).db_insert()

frappe.db.commit()
```

CSV format:
```csv
item_code,uom,discount_percentage,min_qty,max_qty
ITEM-001,Nos,5,1,10
ITEM-001,Nos,10,11,0
ITEM-002,Box,15,1,0
```

> **Note:** `max_qty = 0` means no upper limit (unlimited)

#### Product Bundle Improvements
- Non-sales items in Product Bundles can now be sold through POS
- Automatic validation bypass for bundle component items
- Works with background job submission

#### Optional Reference Details
- Reference Number and Reference Name fields are now optional in payment dialog
- Enable via "Add Reference Details" setting in POS Profile

#### Print Improvements
- Print opens in background tab to avoid blocking POS
- Popup blocker detection with user-friendly message
- Automatic print dialog trigger

#### Customer Form Improvements
- Default country changed to India for new customers
- Improved address handling

#### Total Discount Display
- Shows total item discount amount in payment summary
- Excludes offer items from discount calculation

#### Bug Fixes
- Fixed UOM discount not applying when using +/- quantity buttons
- Fixed UOM discount not updating when quantity falls outside tier range
- Fixed multiple quantity tier discount selection (highest applicable tier)
- Product Bundle items validation bypass for submit and background jobs

### How to Install

#### Self Hosting (Trustbit Fork):

1. `bench get-app https://github.com/zxrrcpandey/POS-Awesome-V15-trustbit-2`
2. `bench setup requirements`
3. `bench build --app posawesome`
4. `bench restart`
5. `bench --site [your.site.name] install-app posawesome`
6. `bench --site [your.site.name] migrate`

#### Post-Installation Setup:

1. Run the install script to create custom fields:
   ```bash
   bench --site [your.site.name] execute posawesome.install.after_install
   ```

2. Configure POS Profile:
   - Enable "Use Item UOM Discount" for UOM-based discounts
   - Enable "Add Reference Details" for optional reference fields

---

### How To Use:

[POS Awesome Wiki](https://github.com/yrestom/POS-Awesome/wiki)

---

### Shortcuts:

- `CTRL or CMD + S` open payments
- `CTRL or CMD + X` submit payments
- `CTRL or CMD + D` remove the first item from the top
- `CTRL or CMD + A` expand the first item from the top
- `CTRL or CMD + E` focus on discount field

---

### Dependencies:

- [Frappe](https://github.com/frappe/frappe)
- [Erpnext](https://github.com/frappe/erpnext)
- [Vue.js](https://github.com/vuejs/vue)
- [Vuetify.js](https://github.com/vuetifyjs/vuetify)

---

### Contributing

1. [Issue Guidelines](https://github.com/frappe/erpnext/wiki/Issue-Guidelines)
2. [Pull Request Requirements](https://github.com/frappe/erpnext/wiki/Contribution-Guidelines)

---

### License

GNU/General Public License (see [license.txt](https://github.com/yrestom/POS-Awesome/blob/master/license.txt))

The POS Awesome code is licensed as GNU General Public License (v3)

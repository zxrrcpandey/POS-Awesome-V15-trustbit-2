# Changelog

All notable changes to POS Awesome (Trustbit Fork) will be documented in this file.

## [2.0.0] - 2026-02-02

### Added

#### Item UOM Discount Feature
- New `Item UOM Discount` child table DocType for configuring UOM-based discounts
- Custom field `posa_uom_discounts` (Table) added to Item master
- Custom field `posa_use_item_uom_discount` (Check) added to POS Profile
- API endpoint `get_item_uom_discount_for_cart` for fetching applicable discounts
- API endpoint `get_item_uom_discounts` for fetching all UOM discounts for an item
- Automatic discount application when:
  - Item is added to cart
  - Quantity is changed (manual entry)
  - Quantity is changed (+/- buttons)
  - UOM is changed
- Support for quantity tiers (min_qty, max_qty)
- Multiple discount entries per UOM supported
- Discount automatically cleared when quantity falls outside tier range
- Sales Invoice form also supports UOM discount via doctype_js hook

#### Product Bundle Improvements
- `bypass_sales_item_validation_for_bundles()` function to allow non-sales items in bundles
- `restore_bundle_items_flags()` function to restore original item flags
- Bypass applied in `update_invoice()`, `submit_invoice()`, and `submit_in_background_job()`

#### Optional Reference Details
- Reference Number field made optional in payment dialog
- Reference Name field made optional in payment dialog
- Enable via `custom_add_reference_details` in POS Profile

#### Print Improvements
- Print now opens in background tab (`_blank` target)
- Popup blocker detection with user-friendly alert
- Automatic `window.print()` trigger in print window

#### Payment Summary Enhancements
- `total_items_discount_amount` computed property shows total discount
- Excludes offer items from discount calculation
- Displays in payment summary section

### Changed
- Default country changed from Pakistan to India in UpdateCustomer.vue
- `add_one()` method now async and applies UOM discount
- `subtract_one()` method now async and applies UOM discount
- `handleQtyChange()` method added for qty input changes

### Fixed
- UOM discount not applying when using +/- quantity buttons
- UOM discount not updating when quantity changes via manual input
- UOM discount not clearing when quantity falls outside tier range
- Multiple quantity tier discount selection (now selects highest applicable tier)
- Product Bundle items failing validation when `is_sales_item` is unchecked
- Product Bundle validation in background job submission

### Technical Details

#### New Files Created
- `posawesome/doctype/item_uom_discount/item_uom_discount.json`
- `posawesome/doctype/item_uom_discount/item_uom_discount.py`
- `posawesome/doctype/item_uom_discount/__init__.py`
- `posawesome/install.py`

#### Files Modified
- `posawesome/api/posapp.py` - Added UOM discount APIs and bundle bypass functions
- `posawesome/api/invoice.js` - Added Sales Invoice UOM discount triggers
- `posawesome/hooks.py` - Added doctype_js hook for invoice.js
- `posawesome/public/js/posapp/components/pos/Invoice.vue` - UOM discount integration
- `posawesome/public/js/posapp/components/pos/Payments.vue` - Print improvements, discount display
- `posawesome/public/js/posapp/components/pos/UpdateCustomer.vue` - Default country change

#### Custom Fields Added (via install.py)
- `Item.posa_uom_discounts` - Table for UOM discounts
- `POS Profile.posa_use_item_uom_discount` - Enable/disable feature

---

## Previous Versions

For changes before the Trustbit fork, see the original [POS Awesome repository](https://github.com/yrestom/POS-Awesome).

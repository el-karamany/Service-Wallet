# Service Wallet — Odoo Module

A module for IT consultancies to manage prepaid support hour packs and customer service wallets.

---

## Features

- Mark products as **Prepaid Support Packs** with configurable hours
- Automatically credit customer wallet upon **Sales Order confirmation**
- Full **transaction history** per customer (credits & debits)
- **Log Support wizard** to deduct hours with insufficient balance protection
- Wallet visibility restricted to **authorized users** via security groups

---

## Installation

1. Clone or copy the `service_wallet` folder into your Odoo `custom-addons` directory
2. Restart the Odoo server
3. Enable developer mode
4. Go to **Apps** → Update Apps List
5. Search for **Service Wallet** and install

---

## Dependencies

- `base`
- `sale`
- `product`
- `contacts`

---

## Usage

### Setting Up a Support Pack Product
1. Go to **Sales → Products**
2. Open or create a product
3. Check **Prepaid Pack** checkbox
4. Set the **Pack Hours** value (e.g. `10`)

### Selling a Support Pack
1. Create a Sales Order with a Prepaid Pack product
2. Confirm the order
3. The customer's wallet is automatically credited with the pack hours

### Viewing a Customer's Wallet
1. Go to **Contacts** → open any customer
2. The **Remaining Hours** field shows the current balance
3. Click the **Wallet Transactions** smart button to see full history

### Logging Support Hours
1. Go to **Contacts → Wallet Transactions → Log Support**
2. Select the customer, enter a description and hours spent
3. Click **Confirm** — hours are deducted from the customer's wallet

---

## Assumptions

The following decisions were made where the requirements were intentionally left open to interpretation:

### 1. Hours credited on Sales Order confirmation — not invoice payment
Hours are added to the customer wallet at the moment the Sales Order is confirmed (`action_confirm`).

> **Alternative:** Hours could alternatively be credited upon invoice payment by overriding `account.move.action_post()` instead. This approach would be more appropriate for businesses that require payment before service delivery begins. This would also require adding `account` to the module dependencies.

### 2. Fractional hours are supported
The `hours_spent` field in the Log Support wizard is a `Float`, allowing fractional values (e.g. `0.5`, `1.25`).

### 3. Access restricted to a dedicated security group
Wallet fields (`remaining_hours`, smart button, transaction tab) are only visible to users in the **Service Wallet Transaction User** group. Partner creation and general usage is unaffected for all other users. Computed fields use `sudo()` internally to avoid access errors during recomputation.

### 4. Log Support is a standalone menu action
The Log Support wizard is accessible from **Contacts → Wallet Transactions → Log Support** and is not tied to a specific partner form. The engineer selects the customer inside the wizard. This was chosen because support engineers typically log work after the fact, not from within a client record.

### 5. Transactions are immutable
All transaction records are created as read-only. There is no edit or delete capability exposed through the UI. This preserves the integrity of the wallet balance, which is computed directly from transaction history.

### 6. `remaining_hours` is not stored
The field is computed on-the-fly using `read_group` for performance. It is not stored in the database, meaning it cannot be used as a filter or group-by in list views by default. `store=True` can be enabled if searchability is required.

---

## Module Structure

```
service_wallet/
├── __init__.py
├── __manifest__.py
├── models/
│   ├── __init__.py
│   ├── product_template.py
│   ├── res_partner.py
│   ├── sale_order.py
│   └── service_wallet_transaction.py
├── wizard/
│   ├── __init__.py
│   ├── log_support_wizard.py
│   └── log_support_wizard_views.xml
├── views/
│   ├── product_template_views.xml
│   ├── res_partner_views.xml
│   └── service_wallet_transaction_views.xml
├── security/
│   ├── groups.xml
│   └── ir.model.access.csv
```

---

## Author

**Omar El-Karamany**

---

## License

LGPL-3

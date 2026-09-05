Document: 30-Week Wedding Planner (Fillable PDF)
Format notes: Designed as print-ready, fillable PDF with named form fields. Page size: A4 and US Letter variations. Two accent colors: #2B7A78 (teal) and #F2C57C (warm gold). Clear sans-serif headings, serif body optional. Margins: 0.7" (print safe).

Page 1 — Cover / Title
- Static text: "Editable 30-Week Wedding Planner"
- Form fields: bride_name, partner_name, wedding_date (MM/DD/YYYY), wedding_location, planner_name
- Subtext: "Fillable PDF + Editable Spreadsheet Included"

Page 2 — Key Dates & Contacts
- Fields: wedding_date_display (derived), rehearsal_date, ceremony_time, reception_time
- Contact block repeated (3x): contact_role_{1..3}, contact_name_{1..3}, contact_phone_{1..3}, contact_email_{1..3}

Page 3 — 30-Week Timeline Overview (two-page spread if needed)
- Intro: short explanation: "High-level view: one row per week. Enter your wedding date at top to map weeks automatically."
- Table columns (fillable field names): week_no, week_start_date_{n}, week_end_date_{n}, week_focus_{n}, task_1_{n}, task_2_{n}, task_3_{n}
- Rows: Weeks 30 down to 1 (or 1 to 30 depending on layout)
- Each row has 3–6 short action slots and a priority dropdown field (priority_{n}) with values: High/Medium/Low

Pages 4–12 — Monthly Overview Pages (one page per month as needed)
- Header field: month_name_{m}
- Fields: month_top_goal_1_{m} .. month_top_goal_5_{m}
- Notes area: month_notes_{m}

Pages 13–(repeating) — Weekly Checklist (repeatable template)
- Header fields: week_label (e.g., "Week 12: 3/10–3/16"), main_focus
- Checklist rows (12 per page): checklist_item_{i}, checklist_status_{i} (checkbox), checklist_notes_{i}
- Quick mini-timers: estimated_hours_{i}

Single-page inserts (each printable separately):
- Vendor Contact & Payments Tracker (vendor_name, vendor_role, vendor_contact, contract_signed (Y/N), deposit_amount, deposit_date, balance_amount, balance_due_date, notes)
- Budget Snapshot: category_{i}, budgeted_{i}, actual_{i}, remaining_{i} (formulas not in PDF; fields for manual entry)
- Day-of Timeline (page): time_{t}, activity_{t}, location_{t}, contact_{t}

Footer on every page: small field for "last_updated_date" and page numbering.

Accessibility & UX
- All form fields have readable labels and tooltip/help text (e.g., "Enter full name: Bride or Partner").
- Fonts sized for legibility when printed.
- Export: include both titled form fields and a flattened print-ready version.

Notes for production: Ensure field names match spreadsheet column names for mapping/import: bride_name, wedding_date, week_no, week_start_date_1..30, task_1_1..task_3_30, vendor_name_1..20, budget_category_1..20. Provide both A4 and Letter PDF files using same named fields.
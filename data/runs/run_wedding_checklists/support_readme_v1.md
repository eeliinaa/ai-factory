Internal Support / Reviewer Checklist (Human final reviewer)

Manual steps to complete before publishing/listing:
1) Replace 'INSERT_GOOGLE_SHEET_LINK_HERE' in vendor-contacts_google-sheet_instructions.txt and delivery_notes_v1.md with the actual share link.
2) Test the fillable PDF: Open vendor-contact-sheet__fillable_A4_USLetter_v1.pdf in Adobe Reader, fill fields, save, and verify saved data persists.
3) Confirm PDF print layouts for A4 and US Letter match margins and are not clipped.
4) Verify example-filled PDF contains no real vendor data; ensure sample labels read 'Example'.
5) Prepare final preview images: replace placeholder PNGs with designer-supplied PNGs sized 2000x1333.
6) Run packaging script to create week-of-day-of-wedding-kit_final_bundle_v1.zip and update final_manifest_v1.json with actual size_bytes values.
7) Re-run Technical QA to confirm zip creation and file size alignment.
8) Approve Etsy title, description, and tags, then pass to listing uploader for manual listing.

Acceptance criteria: All required files pass fillable/form tests, manifest matches actual files, preview images final, and ZIP contains no extraneous or executable files.
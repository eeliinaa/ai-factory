AI prompts and generation parameters — versioned record

Prompt A — Generate role micro-checklist items
Context slice: target audience = engaged couples + bridal party; tone = clear, calm, action-oriented; constraints = 4 sections per role, 6–10 lines each
Prompt:
"Create a compact, one-page micro-checklist for the {ROLE} for a wedding day. Divide into four sections: '24 hrs before', 'Morning', 'At ceremony', 'Vendor handoff'. Provide 6–10 short checklist items per section. Use action verbs and avoid full sentences where possible. Include a final 'Contacts & Notes' block. Return plain text formatted for direct placement into a template."
Model params: model=gpt-4, temperature=0.2, max_tokens=400

Prompt B — Draft Etsy listing description
Context slice: buyer pain points = day-of chaos, unclear responsibilities; product = printable + editable Canva templates; constraints = 400–800 words, headings: Overview, What's Included, How to Use, Format & Sizes, License, FAQs
Prompt:
"Write an Etsy product description for a role-based wedding day checklist bundle. Use headings and be concise. Highlight printable PDFs, editable Canva templates, mobile PNGs, and quick customization. Include a short FAQ and license note."
Model params: model=gpt-4, temperature=0.3, max_tokens=900

Prompt C — Preview captions
Context slice: short promotional captions for each Etsy preview image, 80–160 characters each
Prompt:
"For each preview image (hero, close-up, example-filled, mobile mockup, Canva editor), write a 90–140 character caption emphasizing benefit and CTA."
Model params: model=gpt-3.5-turbo, temperature=0.25, max_tokens=200

Notes: Store model, temperature, and prompt templates for future regeneration. Keep prompts minimal and attach the context slice used (audience, tone, constraints).
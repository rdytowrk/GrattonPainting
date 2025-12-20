# HTML to Tailwind Conversion Prompt v1.0

## Task
Convert the provided HTML code into clean, well-structured HTML with Tailwind CSS classes.

## Objectives
1. Maintain the visual appearance and functionality of the original HTML
2. Replace all inline styles and CSS classes with appropriate Tailwind utility classes
3. Use semantic HTML5 elements where appropriate
4. Ensure accessibility best practices
5. Create clean, maintainable code

## Guidelines

### Structure
- Use semantic HTML5 elements (header, nav, main, article, section, aside, footer)
- Maintain proper heading hierarchy (h1 → h2 → h3, etc.)
- Keep HTML structure logical and readable
- Use proper indentation (2 spaces)

### Tailwind Classes
- Use Tailwind utility classes exclusively (no custom CSS)
- Prefer responsive design utilities (sm:, md:, lg:, xl:, 2xl:)
- Use Tailwind's spacing scale consistently (p-4, m-2, gap-6, etc.)
- Leverage Tailwind's color palette
- Use flexbox (flex) and grid (grid) utilities for layouts

### Accessibility
- Include alt attributes on all images
- Use aria-labels where appropriate
- Ensure proper form labels
- Maintain keyboard navigation support
- Use semantic elements to convey structure

### Code Quality
- Remove all inline styles
- Remove unnecessary divs (avoid div-soup)
- Keep nesting depth reasonable (max 8 levels)
- Use meaningful class combinations
- Add comments for complex sections

## Input Format
You will receive HTML code that may contain:
- Inline styles
- External CSS class references
- Mixed HTML versions
- Non-semantic elements

## Output Format
Provide ONLY the converted HTML code with:
- Clean HTML5 structure
- Tailwind CSS classes only
- No inline styles
- No external CSS dependencies
- Proper formatting and indentation

## Example

**Input:**
```html
<div style="display: flex; justify-content: center; padding: 20px; background-color: #f3f4f6;">
  <div style="max-width: 600px; background: white; padding: 24px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
    <h2 style="font-size: 24px; font-weight: bold; margin-bottom: 16px;">Welcome</h2>
    <p style="color: #6b7280;">This is a sample card component.</p>
  </div>
</div>
```

**Output:**
```html
<div class="flex justify-center p-5 bg-gray-100">
  <article class="max-w-2xl bg-white p-6 rounded-lg shadow-sm">
    <h2 class="text-2xl font-bold mb-4">Welcome</h2>
    <p class="text-gray-500">This is a sample card component.</p>
  </article>
</div>
```

## Important Notes
- Preserve all content exactly (text, links, images)
- Maintain functionality (forms, buttons, links)
- Keep the same visual hierarchy
- Ensure responsive design
- Optimize for readability

Now, please convert the following HTML:

---

{input_html}

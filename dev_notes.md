# AI Dev Notes (.prompt/dev_notes.md)

Utlized the AI to help build the basic skeleton for my files and also to ensure my nav was consistent across
all files.
Had AI help with styling and then went in and customized as I saw fit.

prompt 1: can you give me code for the main class where instead of having an image of my resume, layout my resume as text
Output: I've now created a text-based resume layout with a professional design that matches your website's theme. The resume is organized into sections:

Education
Professional Experience
Technical Skills
Certifications
The layout uses your existing color scheme and styling, with some additional styles specific to the resume sections. Each section is clearly divided and styled with:

Section headers in your accent color
Clean typography with proper spacing
Responsive design that works on all screen sizes
Card-like appearance that matches your site's aesthetic
You can now customize the content by replacing the placeholder text in the HTML with your actual:

Educational background
Work experience
Technical skills
Certifications
The layout will automatically adjust to the content you add, and all the styling is consistent with your website's theme.

Accepted

prompt 2: can you help make my two project images the same size
output: Your two project images will now appear at the same size (320px by 200px) with consistent styling. You can adjust these dimensions in the .project-img CSS class if you want a different size. The object-fit: cover; property ensures the images fill the area without distortion.

Accepted

Prompt 3: can you make complete starter files for a personal website that includes a home page, about me, my resume, projects, and contact info with a form that follows these requirements: Add a form on the contact.html page. - Fields: - First Name (required) - Last Name (required) - Email
Address (required, valid format) - Password (required, min 8 characters) - Confirm Password (required,
must match Password) - Use attributes: required, type, pattern, minlength. - Show clear error messages
(using HTML or minimal JavaScript). - Redirect to a Thank You page (thankyou.html) after submission. -
Accessibility requirement: All inputs must have labels connected with for and id. Add alt text for any
images

Awesome—here’s a complete starter you can use and customize to meet every requirement in your Assignment 5 brief (multi-page site, consistent nav, responsive CSS, accessible form with validation, and AI-log template).

What’s inside

index.html, about.html, resume.html, projects.html, contact.html, thankyou.html

styles.css (global responsive theme + layout)

script.js (mobile nav + form validation + redirect to thankyou.html)

.prompt/dev_notes.md (AI prompts log + reflection template)

/images/ placeholders (profile-placeholder.jpg, project1-placeholder.jpg, project2-placeholder.jpg, resume-placeholder.pdf)

README.md with quick instructions

Somewhat accepted, I made changes so it didn't need a javascript file and was purely HTML and CSS based.

Reflection:
Using AI as a coding partner saved time on repetitive scaffolding. I generated initial page structures, CSS utilities, and form patterns in minutes, then iterated instead of starting from scratch. The model also surfaced edge cases (labels, alt text, focus states) I might have missed under time pressure. However, AI made mistakes: it sometimes suggested non-semantic markup, inconsistent class names, and unnecessary JavaScript for simple behaviors. It also hallucinated attributes and mixed design tokens, creating inconsistencies I had to unwind.

I balanced assistance with deliberate review. After each suggestion, I read the code carefully and made sure align the styles with my own preferences. I inputted my own content and saved time on having to make the actual basic structure. When AI output was not aligned well enough with what I was hoping to achieve, I would change the prompt by being more specific and smaller in scoper. 

ALLOWED_TEMPLATES = {
    'users': ["name", "email", "age"]
}

def is_template_vaild(headers, template):
    allowed_templates = ALLOWED_TEMPLATES.get(template)
    return True if allowed_templates and headers == allowed_templates else allowed_templates

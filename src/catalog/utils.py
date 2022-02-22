def slugify(name: str) -> str:
    name = name.lower()
    non_url_safe = ['"', '#', '$', '%', '&', '+',
                    ',', '/', ':', ';', '=', '?',
                    '@', '[', '\\', ']', '^', '`',
                    '{', '|', '}', '~', "'"]
    non_safe = [c for c in name.lower() if c in non_url_safe]
    if non_safe:
        for c in non_safe:
            name = name.replace(c, '')

    slug = '-'.join(name.split())
    return slug

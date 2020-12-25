def md_code(content, lang="xl"):
    return f"```{lang}\n{content}```"


def md_inline_code(content):
    return f"`{content}`"


def pad(message="", fill=" ", align="<", width="1"):
    align = ">" if align == "start" else "<"
    return '{message:{fill}{align}{width}}'.format(message=message, fill=fill, align=align, width=width)


def diff_month(d1, d2):
    return (d1.year - d2.year) * 12 + d1.month - d2.month

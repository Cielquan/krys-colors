import re

regex = re.sub(
    r"""(?ax)^[^a-z0-9]{1,5}(.*?)
(?:something)?(?# inline comment)@\#\S|\.
(?:\.(?P<precision>0|(?!0)\d+))?
(?x).*\d\[\]\xAD\123$""",
    r"\1",
    "string",
)

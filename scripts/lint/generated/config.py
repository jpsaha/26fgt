import re

# ============================================================
# Generated-file patterns
# ============================================================

FILE_FIELD_RE = re.compile(
    r'\bfile:\s*"([^"]+)"'
)

CONTENT_INCLUDE_RE = re.compile(
    r'#include\s+"\.\./content/([^"]+)"'
)

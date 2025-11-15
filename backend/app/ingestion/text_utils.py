def clean_text(s: str) -> str:
    """
    Remove NUL bytes and control characters that PostgreSQL rejects.
    """
    if not s:
        return ""

    # Remove NUL bytes
    s = s.replace("\x00", "")

    # Remove most non-printable control chars (except newline/tab/carriage return)
    s = "".join(
        ch for ch in s
        if ord(ch) >= 32 or ch in "\n\r\t"
    )

    return s.strip()

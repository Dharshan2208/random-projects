from email.header import decode_header

def clean_subject(subject):
    if subject is None:
        return "(No Subject)"

    try:
        # Decode if subject is encoded like =?utf-8?q?...?=
        decoded_parts = decode_header(subject)
        clean_parts = []

        for part, encoding in decoded_parts:
            if isinstance(part, bytes):
                clean_parts.append(part.decode(encoding or "utf-8", errors="ignore"))
            else:
                clean_parts.append(part)

        #remove newlines and control chars
        clean_subject = ''.join(clean_parts).strip()
        clean_subject = clean_subject.replace('\r', ' ').replace('\n', ' ')
        return clean_subject if clean_subject else "(No Subject)"
    except Exception as e:
        return f"(Invalid Subject: {e})"

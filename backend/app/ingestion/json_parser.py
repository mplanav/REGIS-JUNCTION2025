import json

def parse_json_into_chunks(file_bytes):
    chunks = []

    try:
        data = json.loads(file_bytes)

        for page in data.get("pages", []):
            page_num = page.get("page")

            for p in page.get("paragraphs", []):
                text = (p or "").strip()
                if not text:
                    continue

                chunks.append({
                    "text": text,
                    "article_ref": f"page_{page_num}"
                })

        return chunks

    except Exception as e:
        print(f"[JSON PARSER ERROR] {e}")
        return []

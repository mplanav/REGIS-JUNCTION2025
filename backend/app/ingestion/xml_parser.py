from lxml import etree
from ingestion.text_utils import clean_text


def parse_xml_into_chunks(file_bytes):
    """
    Parses an XML file and extracts text chunks.
    Returns a list of dicts: { "text": ..., "article_ref": ... }
    """

    chunks = []

    try:
        root = etree.fromstring(file_bytes)

        # Example structure:
        # <page number="1">
        #   <paragraph>Some text...</paragraph>
        # </page>
        for page in root.findall(".//page"):
            page_number = page.get("number") or "unknown"

            for para in page.findall(".//paragraph"):
                raw_text = para.text or ""
                cleaned_text = clean_text(raw_text)

                if not cleaned_text:
                    continue

                chunks.append({
                    "text": cleaned_text,
                    "article_ref": f"page_{page_number}",
                })

        return chunks

    except Exception as e:
        print(f"[XML PARSER ERROR] {e}")
        return []

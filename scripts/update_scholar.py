import re
import sys
from datetime import datetime

SCHOLAR_ID = 'OZCvoU4AAAAJ'
FILES = ['index.html', 'rakib-website/index.html']

try:
    from scholarly import scholarly

    print(f"Fetching Scholar profile: {SCHOLAR_ID}")
    author = scholarly.search_author_id(SCHOLAR_ID)

    citations = author.get('citedby', 0)
    hindex    = author.get('hindex', 0)
    i10index  = author.get('i10index', 0)
    print(f"  citations={citations}  h-index={hindex}  i10={i10index}")

    if citations >= 1000:
        c_display = f"{citations // 1000}k+"
    else:
        c_display = f"{citations}+"

    now = datetime.now().strftime('%Y-%m')

    for filepath in FILES:
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            original = content

            # Update Citations stat cell
            content = re.sub(
                r'(<div class="stat-num">)[^<]*(<sup>\+</sup></div><div class="stat-lbl">Citations</div>)',
                rf'\g<1>{c_display}\2',
                content
            )

            # Update Last updated date
            content = re.sub(r'Last updated: \d{4}-\d{2}', f'Last updated: {now}', content)

            if content != original:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"  Updated {filepath}")
            else:
                print(f"  No changes in {filepath}")

        except FileNotFoundError:
            print(f"  Skipping {filepath} (not found)")

    print("Done.")

except Exception as e:
    print(f"Error: {e}", file=sys.stderr)
    sys.exit(1)

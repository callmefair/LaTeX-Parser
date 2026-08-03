from urllib.parse import urlparse
import requests
import re

class WikiError(Exception): pass

class NotWikipediaURL(WikiError):
    def __init__(self, url: str):
        self.url = url
        super().__init__(f"위키피디아 주소가 아닙니다: {url}")

class WikiPageNotFound(WikiError):
    def __init__(self, title: str):
        self.title = title
        super().__init__(f"문서를 찾을 수 없습니다: {title}")

class WikiFetchFailed(WikiError):
    def __init__(self, title: str, reason: str):
        self.title = title
        self.reason = reason
        super().__init__(f"위키피디아 요청 실패 ({title}): {reason}")

class NoFormulaFound(WikiError):
    def __init__(self, url: str):
        self.url = url
        super().__init__(f"블록 수식이 없는 문서입니다: {url}")

HEADERS = {
    "User-Agent": "LaTeX-Parser/1.0 (https://github.com/callmefair/LaTeX-Parser; 7kong@naver.com)"
}

def get_title(url):
    parsed_url = urlparse(url)
    api_url = parsed_url.scheme + "://" + parsed_url.netloc + "/w/api.php"
    title = parsed_url.path.rstrip("/").split("/")[-1]
    return (title, api_url)

def fetch_address(url):
    title, api_url = get_title(url)
    params = {
        "action": "parse",
        "page": title,
        "prop": "wikitext",
        "format": "json",
        "formatversion": 2,
    }

    try:
        response = requests.get(api_url, headers = HEADERS, params=params, timeout=20)
        response.raise_for_status()
    except requests.exceptions.RequestException as err:
        raise WikiFetchFailed(title, str(err)) from err
    
    data = response.json()
    if "error" in data:
        raise WikiPageNotFound(title)
    
    return data["parse"]["wikitext"]

def header_divide(text):
    block_formula = []
    for m in re.finditer(r'<math([^>]*)>(.*?)</math>', text, re.DOTALL):
        attrs, _ = m.group(1), m.group(2)
        is_block = 'display="block"' in attrs or text[:m.start()].rstrip().endswith(":")
        if is_block:
            block_formula.append(m)
    header_by_equal = list(re.finditer(r"^(={2,6})\s*(.*?)\s*\1\s*$", text, re.MULTILINE))

    sections = []

    first_end = header_by_equal[0].start() if header_by_equal else len(text)
    sections.append((0, first_end, "THIS IS THE FIRST SECTION"))

    dict_list = []
    for idx, match in enumerate(header_by_equal):
        header_start = match.start()
        header_end = header_by_equal[idx + 1].start() if idx + 1 < len(header_by_equal) else len(text)
        header_name = match.group(2).strip()
        sections.append((header_start, header_end, header_name))

    for start, end, name in sections:
        formula_list = []
        for match2 in block_formula:
            if start <= match2.start() < end:
                formula_list.append(match2.group(2))
        if not formula_list:
            continue
        dict_list.append({
            "section": name,
            "formulas": formula_list,
        })
    
    return dict_list

def get_latex(url: str) -> dict:
    parsed_url = urlparse(url)
    if not parsed_url.netloc.endswith("wikipedia.org"):
        raise NotWikipediaURL(url)
    wikitext = fetch_address(url)
    sections = header_divide(wikitext)
    if not sections:
        raise NoFormulaFound(url)
    return sections

if __name__ == "__main__":
    cases = [
        ("정상 문서",      "https://en.wikipedia.org/wiki/Darboux_integral"),
        ("위키 아님",      "https://www.google.com/search?q=darboux"),
        ("없는 문서",      "https://en.wikipedia.org/wiki/Asdfgh_not_real_12345"),
        ("수식 없는 문서", "https://en.wikipedia.org/wiki/Coffee"),
    ]
    for name, url in cases:
        print(f"--- {name} ---")
        try:
            sections = get_latex(url)
            for s in sections:
                print(f"  [{s['section']}] 수식 {len(s['formulas'])}개")
            print("  첫 수식:", sections[0]["formulas"][0][:70])
 
        except WikiError as e:
            print(f"  {type(e).__name__}: {e}")
        except Exception as e:
            print(f"  [예상 못 한 예외] {type(e).__name__}: {e}")
        print()

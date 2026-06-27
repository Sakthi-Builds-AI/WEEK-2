# ============================================================
#   NAMMA VIVASAYAM - Powered by SAKTHI AI
#   Step 1 (Final): Playwright Deep Scraper
# ============================================================

from playwright.sync_api import sync_playwright
import time

BASE_URL  = "https://www.tn.gov.in"
LIST_URL  = "https://www.tn.gov.in/scheme_list.php?dep_id=Mg=="

NOISE_KEYWORDS = [
    "screen reader", "accessibility", "text to speech", "skip to",
    "home government", "governor", "chief minister", "council of ministers",
    "mla profile", "state profile", "departments", "districts",
    "policy notes", "citizen charter", "circulars", "announcements",
    "online services", "contact", "copyright", "last updated",
    "designed by", "sitemap", "feedback", "disclaimer",
    "தமிழ்நாடு அரசு", "தமிழ்த்தாய்", "நல்லாறு"
]

def is_noise(text):
    return any(kw in text.lower() for kw in NOISE_KEYWORDS)

def load_tn_schemes():
    print("🌾 Namma Vivasayam | SAKTHI AI")
    print("📥 Deep scraping all TN scheme detail pages...")
    print("=" * 55)

    all_documents = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page    = browser.new_page()

        # Step 1: Get all scheme links from list page
        print("🔗 Fetching scheme links...")
        page.goto(LIST_URL)
        page.wait_for_timeout(3000)

        links = page.eval_on_selector_all(
            'a[href]',
            'els => els.map(e => ({text: e.innerText.trim(), href: e.href}))'
        )

        scheme_links = [
            (l["text"], l["href"])
            for l in links
            if "scheme_details.php" in l["href"] and len(l["text"]) > 5
        ]

        print(f"✅ Found {len(scheme_links)} scheme pages to scrape\n")

        # Step 2: Visit each scheme detail page
        for i, (name, url) in enumerate(scheme_links):
            print(f"[{i+1}/{len(scheme_links)}] Scraping: {name[:55]}...")
            try:
                page.goto(url)
                page.wait_for_timeout(2000)

                # Get all visible text
                content = page.inner_text("body")
                lines   = content.split("\n")

                # Clean lines
                clean_lines = []
                for line in lines:
                    line = line.strip()
                    if len(line) < 30:
                        continue
                    if is_noise(line):
                        continue
                    clean_lines.append(line)

                if clean_lines:
                    # Combine into one rich document per scheme
                    full_text = f"Scheme Name: {name}\n" + "\n".join(clean_lines)
                    all_documents.append(full_text)
                    print(f"   ✅ Got {len(clean_lines)} lines")
                else:
                    print(f"   ⚠️  No content found")

            except Exception as e:
                print(f"   ❌ Error: {e}")

            time.sleep(0.5)

        browser.close()

    print(f"\n✅ Total scheme documents scraped: {len(all_documents)}")
    return all_documents

if __name__ == "__main__":
    data = load_tn_schemes()
    print("\n--- Preview: First 2 Full Scheme Documents ---")
    for i, item in enumerate(data[:2]):
        print(f"\n[{i+1}]\n{item[:500]}")
        print("=" * 55)
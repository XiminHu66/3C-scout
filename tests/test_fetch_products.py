import importlib.util
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).resolve().parents[1] / "scripts" / "fetch_products.py"
SPEC = importlib.util.spec_from_file_location("fetch_products", MODULE_PATH)
fetch_products = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(fetch_products)


class FeedParserTests(unittest.TestCase):
    def test_rss_deal_extracts_price_discount_image_and_merchant(self):
        payload = b"""<?xml version="1.0"?>
        <rss version="2.0"><channel><item>
          <title>USB-C desktop dock now $69.99, was $99.99 (30% off)</title>
          <link>https://example.com/deal/1</link>
          <pubDate>Tue, 25 Aug 2026 08:00:00 GMT</pubDate>
          <description><![CDATA[<p>A compact 10G hub for a clean desk setup.</p>
          <img src="https://images.example.com/dock.jpg" />
          <a href="https://www.amazon.com/dp/TEST">Buy it</a>]]></description>
        </item></channel></rss>"""
        entries = fetch_products.extract_entries(payload)
        source = {"name": "Fixture Deals", "stream": "deals", "language": "en", "trust": 8}
        item = fetch_products.build_item(entries[0], source)
        self.assertIsNotNone(item)
        self.assertEqual(item["category"], "桌面")
        self.assertEqual(item["price"], "$69.99")
        self.assertEqual(item["original_price"], "$99.99")
        self.assertEqual(item["discount_percent"], 30)
        self.assertEqual(item["product_url"], "https://www.amazon.com/dp/TEST")
        self.assertEqual(item["image_url"], "https://images.example.com/dock.jpg")

    def test_atom_new_product_is_classified(self):
        payload = b"""<?xml version="1.0" encoding="utf-8"?>
        <feed xmlns="http://www.w3.org/2005/Atom"><entry>
          <title>New handheld gaming controller announced</title>
          <link rel="alternate" href="https://example.com/new-controller" />
          <updated>2026-08-25T12:00:00Z</updated>
          <summary>A compact controller for Steam Deck and PC gaming.</summary>
        </entry></feed>"""
        entries = fetch_products.extract_entries(payload)
        source = {"name": "Fixture New", "stream": "new", "language": "en", "trust": 7}
        item = fetch_products.build_item(entries[0], source)
        self.assertIsNotNone(item)
        self.assertEqual(item["stream"], "new")
        self.assertEqual(item["category"], "游戏")
        self.assertGreater(item["relevance_score"], 10)


if __name__ == "__main__":
    unittest.main()

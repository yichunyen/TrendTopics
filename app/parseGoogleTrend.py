import xml.etree.ElementTree as ET
import os

def parse_google_trends(xml_data):
    """
    Parses Google Trends XML data and extracts the title from each item.

    Args:
        xml_data: A string containing the XML data.

    Returns:
        A list of strings, where each string is a trend title.
    """
    try:
        ns = {
            'ht': 'https://trends.google.com/trending/rss'
        }

        root = ET.fromstring(xml_data)
    
        trends_list = []
        items = root.findall('.//item')
        for item in items:
            entry = {
                'title': item.findtext('title'),
                'traffic': item.findtext('ht:approx_traffic', namespaces=ns),
                'news': []
            }

            news_elements = item.findall('ht:news_item', ns)
            for news in news_elements:
                news_detail = {
                    'n_title': news.findtext('ht:news_item_title', namespaces=ns),
                    'n_source': news.findtext('ht:news_item_source', namespaces=ns),
                    'n_url': news.findtext('ht:news_item_url', namespaces=ns),
                }
                entry['news'].append(news_detail)

            trends_list.append(entry)
        return trends_list
    except ET.ParseError as e:
        # Raise a ValueError to be handled by the caller, e.g., the Flask app.
        raise ValueError(f"Failed to parse XML data: {e}") from e

def main():
    """
    Main function to parse a local Google Trends XML file when run directly.
    """
    try:
        # The script is in 'app/', so we navigate to the parent directory for the XML file.
        app_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(app_dir)
        xml_file_path = os.path.join(project_root, 'trendFakeData.xml')

        if not os.path.exists(xml_file_path):
             print(f"Error: File not found at '{xml_file_path}'")
             return

        with open(xml_file_path, 'r', encoding='utf-8') as f:
            xml_content = f.read()

        print(f"--- Analyzing local file: {xml_file_path} ---")
        results = parse_google_trends(xml_content)

        if results:
            for index, trend in enumerate(results, 1):
                if trend['news']:
                    print(f"# {index} {trend['title']} {trend['traffic']}")
                    for n_idx, news in enumerate(trend['news'], 1):
                        print(f"  [{n_idx}] {news['n_title']}")
                        print(f"      {news['n_url']}")
                else:
                    print(f"# {index} {trend['title']} {trend['traffic']} N/A")
        else:
            print("No titles found. The XML may be empty or have an unexpected structure.")
        print("-------------------------------------------------")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()

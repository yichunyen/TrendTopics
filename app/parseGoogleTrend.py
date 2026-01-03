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
        root = ET.fromstring(xml_data)
        titles = []
        # Find all 'item' elements in the XML and get the 'title' from each.
        for item in root.findall('.//item'):
            title = item.find('title')
            if title is not None and title.text:
                titles.append(title.text.strip())
        return titles
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
        titles = parse_google_trends(xml_content)

        if titles:
            print("Extracted Titles:")
            for i, title in enumerate(titles, 1):
                print(f"{i}. {title}")
        else:
            print("No titles found. The XML may be empty or have an unexpected structure.")
        print("-------------------------------------------------")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()

"""
Taiwan National Calendar - Fetch national holidays from government open data
政府資料開放平臺 - 政府行政機關辦公日曆表
資料集：https://data.gov.tw/dataset/123662
"""

import logging
import csv
import io
import requests
import urllib3

# Suppress SSL warnings for local development
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

logger = logging.getLogger(__name__)


def get_national_calendar_events(year):
    """
    Fetch Taiwan national holidays from government open data platform.
    資料來源：新北市政府人事處 - 政府行政機關辦公日曆表(2017-2026)
    
    Args:
        year (int): The year to fetch calendar data for
        
    Returns:
        list: List of holiday events with date, name, and other details
    """
    # 政府資料開放平臺 - 新北市政府提供的CSV資料
    # 資料集編號：308dcd75-6434-45bc-a95f-584da4fed251
    # 資料集網址：https://data.gov.tw/dataset/123662
    csv_url = "https://data.ntpc.gov.tw/api/datasets/308dcd75-6434-45bc-a95f-584da4fed251/csv/file"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    }
    
    try:
        logger.info(f"Fetching national calendar data for year {year}")
        response = requests.get(csv_url, headers=headers, timeout=30, verify=False)
        response.raise_for_status()
        
        # Parse CSV content
        csv_content = response.content.decode('utf-8-sig')  # BOM handling
        csv_reader = csv.DictReader(io.StringIO(csv_content))
        
        # Filter events for the specified year
        events = []
        for row in csv_reader:
            # Check if the date field contains the year
            if 'date' in row and row['date'].startswith(str(year)):
                events.append({
                    'date': row.get('date', ''),
                    'year': row.get('year', ''),
                    'name': row.get('name', ''),
                    'isholiday': row.get('isholiday', ''),
                    'holidaycategory': row.get('holidaycategory', ''),
                    'description': row.get('description', '')
                })
        
        logger.info(f"Successfully fetched {len(events)} calendar events for {year}")
        return events
            
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to fetch national calendar data: {e}")
        raise Exception(f"Failed to fetch national calendar: {e}")
    except Exception as e:
        logger.error(f"Failed to parse calendar data: {e}")
        raise Exception(f"Failed to parse calendar data: {e}")

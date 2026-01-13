"""
Google Trends Taiwan Daily Trending Topics Fetcher
Fetches trending topics from Google Trends and sends to Slack
"""

import os
import logging
from datetime import datetime
from zoneinfo import ZoneInfo

from flask import Flask, jsonify
import requests

# Import the shared parser function
from parseGoogleTrend import parse_google_trends

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)


def get_taiwan_trending_topics():
    """Fetch trending topics from Google Trends RSS feed for Taiwan."""
    # Google Trends RSS feed for Taiwan
    rss_url = "https://trends.google.com/trending/rss?geo=TW"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'application/rss+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7',
    }
    
    try:
        response = requests.get(rss_url, headers=headers, timeout=30)
        response.raise_for_status()
        
        # Use the imported parser to extract topics from the RSS feed content
        topics = parse_google_trends(response.content)
        
        if topics:
            logger.info(f"Found {len(topics)} trending topics via RSS feed")
            return topics[:20]
        else:
            logger.warning("No topics found in RSS feed")
            return []
            
    except requests.exceptions.RequestException as e:
        logger.error(f"RSS feed request failed: {e}")
        raise Exception(f"Failed to fetch RSS feed: {e}")
    except ValueError as e: # Catch parsing errors from our function
        logger.error(f"Failed to parse RSS XML: {e}")
        raise Exception(f"Failed to parse RSS feed: {e}")


def send_to_slack(topics: list):
    """Send trending topics to Slack channel via webhook."""
    webhook_url = os.environ.get('SLACK_WEBHOOK_URL')
    
    if not webhook_url:
        raise ValueError("SLACK_WEBHOOK_URL environment variable is not set")
    
    # Get current time in Taiwan timezone
    taiwan_tz = ZoneInfo('Asia/Taipei')
    current_time = datetime.now(taiwan_tz).strftime('%Y-%m-%d %H:%M')
    sections = ''
    
    if topics:
        for index, trend in enumerate(topics, 1):
            if trend['news'] and len(trend['news']) > 0:
                sections += f"# {index} {trend['title']} ({trend['traffic']})\n"
                for n_idx, news in enumerate(trend['news'], 1):
                    sections += f"- {news['n_title']} {news['n_url']}\n\n"
            else:
                sections += f"# {index} {trend['title']} ({trend['traffic']}) - N/A\n\n"
    else:
        sections += "目前沒有找到熱門關鍵字\n"
    
    # logger.info(f"Preparing to send {len(topics)} topics to Slack")

    # Format the message
    if topics:
        message = {
            "blocks": [
                {
                    "type": "header",
                    "text": {
                        "type": "plain_text",
                        "text": "🔥 台灣 Google Trends 熱門關鍵字",
                        "emoji": True
                    }
                },
                {
                    "type": "context",
                    "elements": [
                        {
                            "type": "plain_text",
                            "text": f"📅 {current_time} (近 24 小時)",
                            "emoji": True
                        }
                    ]
                },
                {
                    "type": "divider"
                },
                {
                    "type": "context",
                    "elements": [
                        {
                            "type": "mrkdwn",
                            "text": sections
                        }
                    ]
                }
            ]
        }
    else:
        message = {
            "text": f"📅 {current_time}\n目前沒有找到熱門關鍵字"
        }
    
    response = requests.post(
        webhook_url,
        json=message,
        headers={'Content-Type': 'application/json'},
        timeout=30
    )
    
    if response.status_code != 200:
        raise ValueError(f"Slack API error: {response.status_code} - {response.text}")
    
    logger.info("Successfully sent message to Slack")
    return True


def fetch_trends():
    """Main function to fetch trends and send to Slack."""
    topics = get_taiwan_trending_topics()
    send_to_slack(topics)
    return topics


@app.route('/fetch-trends', methods=['POST', 'GET'])
def fetch_trends_endpoint():
    """HTTP endpoint for Cloud Scheduler to trigger."""
    try:
        topics = fetch_trends()
        return jsonify({
            "status": "success",
            "topics_count": len(topics),
            "topics": topics[:10]  # Return first 10 in response
        }), 200
    except Exception as e:
        logger.error(f"Error in fetch_trends_endpoint: {e}")
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({"status": "healthy"}), 200


@app.route('/', methods=['GET'])
def root():
    """Root endpoint."""
    return jsonify({
        "service": "Google Trends Taiwan Fetcher",
        "endpoints": ["/fetch-trends", "/health"]
    }), 200


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=False)

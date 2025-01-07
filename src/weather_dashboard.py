import os
import json
import boto3
import requests
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

class WeatherDashboard:
    def __init__(self):
        self.api_key = os.getenv('OPENWEATHER_API_KEY')
        self.bucket_name = os.getenv('AWS_BUCKET_NAME')
        self.s3_client = boto.client('s3')

    def create_bucket_if_not_exists(self):
        """Create S3 bucket if one does not exist"""
        try:
            self.s3_client.head_bucket(Bucket=self.bucket_name)
        except:
            print(f"Creating bucket {self.bucket_name}")
        try:
            self.s3_client.create_bucket(Bucket=self.bucket_name)
            print(f"Successfully created bucket {self.bucket_name}")
        except Exception as e:
            print(f"Error creating bucket: {e}")

    def fetch_weather(self, city):
        """Fetch weather data from OpenWeather API"""
        base_url = "http://api.openweathermap.org/data/2.5/weather"
        params = {
            "q": city,
            "appid": self.api_key,
            "units": "imperial"
        }

        try:
            response = requests.get(base_url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching weather data: {e}")
            return None

    def save_to_s3(self, weather_data, city):
        """Save weather data to S3 Bucket"""
        if not weather_data:
            return False


def main():


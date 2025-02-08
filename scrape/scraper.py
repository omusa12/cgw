import requests
from datetime import datetime, timedelta
import json
import os
import time

class CanadaGeneralScraper:
    def __init__(self):
        self.base_url = "https://canadageneral.ca"
        self.login_url = f"{self.base_url}/login"
        self.search_url = f"{self.base_url}/search/contracts"
        self.session = requests.Session()
        
        # Create directory for storing JSON files if it doesn't exist
        self.output_dir = "scraped_data"
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def login(self, username, password):
        """Handle login to the website"""
        try:
            # First get the login page to capture any CSRF token if needed
            login_page = self.session.get(self.login_url)
            login_page.raise_for_status()

            # Prepare login data
            login_data = {
                "username": username,
                "password": password
            }

            # Attempt login
            response = self.session.post(self.login_url, data=login_data)
            response.raise_for_status()

            # Check if login was successful (you might need to adjust this based on the actual response)
            if "login" in response.url.lower():
                raise Exception("Login failed. Please check credentials.")

            print("Login successful!")
            return True

        except Exception as e:
            print(f"Login error: {str(e)}")
            return False

    def scrape_data(self, start_date, end_date, interval_days=1):
        """
        Scrape data between start and end dates with specified interval
        """
        current_date = datetime.strptime(start_date, "%Y-%m-%d")
        end_datetime = datetime.strptime(end_date, "%Y-%m-%d")

        while current_date <= end_datetime:
            interval_end = min(current_date + timedelta(days=interval_days), end_datetime)
            
            # Format dates for the request
            from_date = current_date.strftime("%Y-%m-%d")
            to_date = interval_end.strftime("%Y-%m-%d")
            
            # Prepare request parameters
            params = {
                "from": from_date,
                "to": to_date
            }

            try:
                # Make the request
                response = self.session.get(self.search_url, params=params)
                response.raise_for_status()
                
                # Parse JSON response
                data = response.json()
                
                # Save the data
                filename = f"contracts_{from_date}_to_{to_date}.json"
                filepath = os.path.join(self.output_dir, filename)
                
                with open(filepath, 'w') as f:
                    json.dump(data, f, indent=4)
                
                print(f"Successfully saved data for period {from_date} to {to_date}")
                
                # Add a small delay between requests to be polite
                time.sleep(2)

            except Exception as e:
                print(f"Error scraping data for period {from_date} to {to_date}: {str(e)}")

            # Move to next interval
            current_date = interval_end + timedelta(days=1)

def main():
    # Initialize scraper
    scraper = CanadaGeneralScraper()
    
    # Login credentials
    username = "johndimeck@canadageneral.ca"
    password = "Nkc980f"
    
    # Perform login
    if not scraper.login(username, password):
        print("Failed to login. Exiting...")
        return
    
    # Define date range from today back to 2017-11-01
    #end_date = datetime.now().strftime("%Y-%m-%d")
    end_date = "2019-06-15"
    start_date = "2019-06-08"
    
    print(f"Starting scrape from {end_date} back to {start_date}")
    print("Data will be saved in weekly intervals")
    
    # Start scraping
    scraper.scrape_data(start_date, end_date)

if __name__ == "__main__":
    main()

from playwright.async_api import async_playwright
import pandas as pd
import asyncio
import logging
import random
import time
import csv
import os
from datetime import datetime, timedelta

# Configure logging
# logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


# Random delay function to mimic human behavior
def random_delay(min_delay=1, max_delay=3):
    delay = random.uniform(min_delay, max_delay)
    logging.info(f"Taking a short nap for {delay:.2f} seconds..")
    time.sleep(delay)

async def scrape_enam_trade_data(file_name=None):
    # Use a relative path based on the project structure
    if file_name is None:
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        file_name = os.path.join(base_dir, "data", "enam_trade_data.csv")
    # Ensure the directory exists
    os.makedirs(os.path.dirname(file_name), exist_ok=True)
    # Ensure the CSV file exists and has headers
    if not os.path.exists(file_name):
        columns = [
            "State",
            "APMC",
            "Commodity",
            "Min Price (Rs.)",
            "Modal Price (Rs.)",
            "Max Price (Rs.)",
            "Arrivals",
            "Traded Quantity",
            "Unit",
            "Date",
            "APMC_Selected",
            "Commodity_Selected"
        ]
        with open(file_name, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(columns)
        logging.info(f"Created a new file: {file_name} with headers.")

    async with async_playwright() as p:
        # Launch browser with a custom user-agent to avoid detection
        browser = await p.chromium.launch(headless=True)  # headless=False to see the browser
        context = await browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36")
        page = await context.new_page()
        logging.info("Navigating to the eNAM trade data dashboard...")

        await page.goto("https://enam.gov.in/web/dashboard/trade-data")
        random_delay()

        # Wait for the state dropdown to load
        await page.wait_for_selector("#min_max_state")

        # Get all state options
        states = await page.query_selector_all("#min_max_state option")
        logging.info(f"Found {len(states) - 1} states to iterate through.")

        # Iterate through each state (skipping the placeholder option)
        for state in states[1:]:
            state_value = await state.get_attribute("value")
            state_label = await state.inner_text()
            logging.info(f"Selecting state: {state_label} (Value: {state_value})")

            # Select the state
            await page.select_option("#min_max_state", value=state_value)
            random_delay()

            # Log the selected state
            logging.info(f"Selected state: {state_label}")

            apmcs = await page.query_selector_all("#min_max_apmc option")
            logging.info(f"Found {len(apmcs) - 1} APMC options to scrape")

            for apmc in apmcs[1:]:  # Skip the first option (placeholder)
                apmc_value = await apmc.get_attribute("value")
                apmc_label = await apmc.inner_text()
                logging.info(f"Scraping data for APMC: {apmc_label} (Value: {apmc_value})")
                random_delay()

                await page.select_option("#min_max_apmc", value=apmc_value)
                await page.wait_for_timeout(1000)

            

                random_delay()

                # Click refresh
                await page.click("#refresh")
                logging.info("Clicked the refresh button. Waiting for the table to load...")
                await page.wait_for_timeout(3000)  # Wait for table to load

                # Scrape the table
                rows = await page.query_selector_all("table tbody tr")
                logging.info(f"Found {len(rows)} rows of data for {apmc_label}. Starting to scrape...")

                # Write each row immediately after scraping
                with open(file_name, mode="a", newline="", encoding="utf-8") as file:
                    writer = csv.writer(file)
                    for row in rows:
                        cells = await row.query_selector_all("td")
                        if cells:
                            row_data = await asyncio.gather(*[cell.inner_text() for cell in cells])
                            row_data.extend([apmc_label, state_label])
                            writer.writerow(row_data)

                logging.info(f"Appended {len(rows)} rows to {file_name} for APMC: {apmc_label}")

        logging.info("Scraping completed. Closing the browser.")
        await browser.close()


if __name__ == "__main__":
    logging.info("Starting the eNAM trade data scraper. Buckle up!")
    asyncio.run(scrape_enam_trade_data())
    logging.info("The data is saved.")

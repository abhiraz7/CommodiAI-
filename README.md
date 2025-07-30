# APMC Scraper Project

This project consists of two main components: an agricultural data website and a scraper for collecting agricultural market data.

## Project Structure

```
apmc-scraper-project
├── agri-data-website
│   ├── app.py
│   ├── templates
│   │   └── index.html
│   └── requirements.txt
├── scraper
│   └── APMC_Scraper.py
├── data
│   └── agri_data.csv
└── README.md
```

## Components

### agri-data-website

- **app.py**: The main application file that initializes a Flask app, loads agricultural data from a CSV file, and renders it in an HTML template.
- **templates/index.html**: The HTML template used by the Flask app to display the agricultural data.
- **requirements.txt**: Lists the dependencies required for the agri-data-website, including Flask and pandas.

### scraper

- **APMC_Scraper.py**: Contains the code for the APMC scraper, responsible for scraping agricultural market data from specified sources and saving it in a structured format.

### data

- **agri_data.csv**: Contains the agricultural data in CSV format, used by both the agri-data-website and the scraper.

## Setup Instructions

1. Clone the repository to your local machine.
2. Navigate to the `agri-data-website` directory and install the required dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Run the Flask application:
   ```
   python app.py
   ```
4. Navigate to the `scraper` directory to run the APMC scraper:
   ```
   python APMC_Scraper.py
   ```

## Usage Guidelines

- Access the agri-data-website by visiting `http://127.0.0.1:5000` in your web browser.
- The scraper can be configured to scrape data from various sources as needed. Ensure that the output format is compatible with the existing CSV structure.
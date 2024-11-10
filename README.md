# Real Estate Web Scraper

This project is a web scraping application designed to extract real estate listings from the website Properati Argentina. It is built using the Scrapy framework, a popular tool for scalable web scraping in Python.

## Project Structure

- `ProperatiScraper/`: Main folder containing the Scrapy project.
  - `run_ProperatiSpider.py`: Entry point script to run the spider.
  - `ProperatiScraper/spiders/Properati_spider.py`: Main spider file where the scraping logic is implemented.
  - `ProperatiScraper/settings.py`: Configuration file for Scrapy settings (e.g., export format, logging).
  - `auxiliares/`: Folder containing auxiliary resources (e.g., text files with manual run notes).
- `info_util/`: Folder with additional resources or notes (`recursos.txt`).

## Key Features

1. **Data Extraction**:
   - The spider extracts real estate listings from Properati Argentina, including details such as title, price, location, and property attributes.

2. **Logging**:
   - Logs are generated and saved to track scraping progress and issues, with a custom logging format for improved readability.

3. **Data Export**:
   - Extracted data is automatically saved to a CSV file in a structured format, organized by date (e.g., `archivos_scrapeo/2024-11/properati_2024-11-10.csv`).

4. **Robust Error Handling**:
   - The scraper handles cases where listings may be incomplete or inaccessible, and limits the number of failed requests.

## Properati_spider.py

The `Properati_spider.py` file contains the main scraping logic of the project. Here is an overview of its key components:

- **Spider Configuration**:
  - The spider is named `ProperatiSpider` and is configured to start scraping from the base URL `https://www.properati.com.ar`.
  - It includes a custom logging setup to save log files with detailed information about each run.

- **Data Extraction Process**:
  - The spider iterates over the listings on Properati and extracts key information such as:
    - Title of the property
    - Price
    - Location (address, neighborhood, and city)
    - Property type (e.g., apartment, house)
    - Additional attributes (e.g., number of rooms, bathrooms, size)

- **Handling Missing Data**:
  - The spider checks if listings contain missing or incomplete information. If a listing lacks essential data, it is counted towards a predefined limit of allowed missing data points.

- **File Saving and Output**:
  - The extracted data is saved in CSV format in the `archivos_scrapeo` folder. The file is named based on the current date (e.g., `properati_2024-11-10.csv`).
  - The spider creates directories for the current month if they do not already exist.

- **Error and Logging Handling**:
  - Custom logging is configured using the `colorlog` package to format logs with color-coded messages.
  - Logs are stored in the `log_files` directory, allowing for easy access and debugging of the scraping process.

- **Future Improvements**:
  - The script has several pending tasks, including:
    - Adding detailed docstrings for better code documentation.
    - Including additional print statements for improved runtime feedback.

## Usage

1. **Setup**:
   - Ensure you have Python and Scrapy installed (`pip install scrapy`).
   - Navigate to the project directory.

2. **Run the Spider**:
   ```bash
   python run_ProperatiSpider.py

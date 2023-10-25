# **football_db**
A pipeline built to scrape Brazil and Argentina league's results and stats and serve them into a dashboard.

![logo](logo.jfif "Logo")

# **Summary**
- Mage.ai orchestrated
- Scrapes **Transfermarkt** daily
- Loads data to **Data Lake**
- Inserts into database with constraints and QCs
- Version controlled database for security
- RUST API (REST API built on Rust)
- Neo4j integration

# **Architechture and System Design**
## **Why we chose Mage?**
Easier to setup than Airflow. For the job I wanted, Mage was good enough.

## **Scraping**
Used BeautifulSoup4 (bs4) for this. No need for IP rotation as time between request was quite spaced. No need for extra safety precautions.

## **Data Lake**
Using Google's Cloud Storage in union with Google Big Query.

## **Data Model of Database**
Our Data Model is shown above:
![main_db](main_db.PNG "Main Model")

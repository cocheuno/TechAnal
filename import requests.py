import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import re

# URL of the website to scrape
url = 'http://books.toscrape.com/catalogue/category/books/mystery_3/index.html'

# Send a GET request to the website
response = requests.get(url)

# Parse the HTML content of the page using BeautifulSoup
soup = BeautifulSoup(response.text, 'html.parser')

# Find the section that contains the mystery book listings
# This selector might need adjustments based on the website's structure
book_section = soup.find_all('li', class_='col-xs-6 col-sm-4 col-md-3 col-lg-3')

books_data = []

for book in book_section:
    # Extract book title
    title = book.find('h3').find('a')['title']
    
    # Extract book price and remove unwanted characters
    price = book.find('p', class_='price_color').text
    price = re.sub(r'[^0-9.]', '', price)  # Remove everything except digits and dot
    price = float(price)
    
    # Assuming stock availability and number sold per day are available as data attributes
    # These selectors might need adjustments
    stock = int(book.find('p', class_='instock availability').get('data-stock', 0))  # Default to 0 if not found
    sold_per_day = int(book.find('p', class_='instock availability').get('data-sold-per-day', 0))  # Default to 0 if not found
    
    books_data.append({
        'title': title,
        'price': price,
        'stock': stock,
        'sold_per_day': sold_per_day
    })

import numpy as np

# Calculate the average and median price of the books
average_price = np.mean([book['price'] for book in books_data])
median_price = np.median([book['price'] for book in books_data])

# Calculate the total number of books sold per day
total_sold_per_day = sum([book['sold_per_day'] for book in books_data])

print(f"Average Price: £{average_price:.2f}")
print(f"Median Price: £{median_price:.2f}")
print(f"Total Sold Per Day: {total_sold_per_day}")

for book in books_data:
    print(f"Title: {book['title']}, Average Price: £{book['price']:.2f}, Median Price: £{median_price:.2f}, Stock: {book['stock']}, Total Sold in a Week: {book['sold_per_day'] * 7}")


# Assuming we have a list of total books sold each day for a week
daily_sales = [sum(book['sold_per_day'] for book in books_data) for _ in range(7)]  # Simplified for illustration

days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

plt.figure(figsize=(10, 6))
plt.bar(days, daily_sales, color='skyblue')
plt.xlabel('Day of the Week')
plt.ylabel('Total Books Sold')
plt.title('Total Number of Mystery Books Sold Each Day in a Week')
plt.show()


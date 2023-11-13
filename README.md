# Product Listing Site

## Description

This is a dynamic web application designed for listing and browsing various products. It's an ideal platform for small to medium businesses looking to showcase their products online. Key features include user authentication, product search, category-based filtering, and an intuitive user interface.

## Installation

To set up this project locally, follow these steps:

1. Clone the repository:

   ```bash
   git clone https://github.com/BAXTOR95/product_listing_site.git
   ```

2. Navigate to the project directory:

   ```bash
   cd product_listing_site
   ```

3. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Run the Django migrations to set up your database:

   ```bash
   python manage.py migrate
   ```

5. Run the populate_db command to populate your database with data from <https://fakestoreapi.com/docs>:

   ```bash
   python manage.py populate_db
   ```

6. Start the development server:

   ```bash
   python manage.py runserver
   ```

7. Open <http://127.0.0.1:8000/> in your browser to view the site

## Usage

After setting up the project, you can:

- Register a new user account or log in.
- Browse through the listed products.
- Use the report functionality to show the purchases of a particular product and the total revenue for a given date range.
- Purchased a product (requires user to be logged in).

## Technologies Used

- Django: A high-level Python Web framework that encourages rapid development and clean, pragmatic design.
- SQLite: Used as the default database for development.
- HTML/CSS: For structuring and styling the web pages.
- Bootstrap: For responsive design and pre-designed components.

## Demo

Link to a live demo or screenshots.

## License

Distributed under the MIT License. See LICENSE for more information.

## Contact

For any queries or suggestions, feel free to reach out to me at <brian.arriaga@gmail.com>.

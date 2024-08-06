# eShop - Your Ultimate Tech Destination

Welcome to eShop, an advanced student project built using Django 5.0.6. This project demonstrates a fully-functional e-commerce platform that provides users with a seamless shopping experience for the latest tech gadgets and accessories.

## Table of Contents
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [Running the Project](#running-the-project)
- [Creating a Superuser](#creating-a-superuser)
- [Admin Panel Usage](#admin-panel-usage)
- [Project Structure](#project-structure)
- [Custom Management Commands](#custom-management-commands)
- [Frontend](#frontend)
- [Notes](#notes)
- [License](#license)

## Features
- User authentication (register, login, logout)
- Product browsing by categories
- Detailed product pages with user reviews
- Shopping cart functionality
- User wishlist
- Secure checkout process
- Order tracking and management
- Search functionality
- Newsletter subscription
- Responsive design for mobile and desktop

## Technologies Used
- Django 5.0.6
- Python 3.x
- HTML5
- Tailwind CSS
- JavaScript (with Alpine.js for interactivity)
- SQLite (default database)

## Installation
To get started with eShop, follow these steps:

1. **Clone the repository:**
    ```sh
    git clone https://github.com/zimNMM/ecommerce.git
    cd ecommerce
    ```

2. **Set up a virtual environment (optional but recommended):**
    ```sh
    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the required packages:**
    ```sh
    pip install -r requirements.txt
    ```

## Running the Project
1. **Apply the migrations:**
    ```sh
    python3 manage.py migrate
    ```

2. **Run the development server:**
    ```sh
    python3 manage.py runserver
    ```

3. Open your browser and navigate to `http://127.0.0.1:8000` to see the eShop homepage.

## Creating a Superuser
To access the admin panel and manage the store's data:

1. **Create the superuser:**
    ```sh
    python3 manage.py createsuperuser
    ```
    Follow the prompts to set up your superuser account.

2. **Access the admin panel:**
    Navigate to `http://127.0.0.1:8000/admin` and log in with the superuser credentials.

## Admin Panel Usage
In the admin panel, you can manage various aspects of the e-commerce platform:

- **Categories**: Create and manage product categories.
- **Products**: Add new products to the store. The `product_id` is generated automatically. Required fields:
  - Category
  - Name
  - Price
  - Quantity
  - Image
- **Orders**: View and manage customer orders.
- **Reviews**: Monitor and moderate product reviews from customers.
- **Payments**: Review payment details for orders.
- **Users**: Manage user accounts and permissions.

## Project Structure
- `shop/`: Main application directory
  - `models.py`: Database models
  - `views.py`: View functions
  - `forms.py`: Form classes
  - `admin.py`: Admin panel configurations
- `ecommerce/`: Settings and URLs
  - `urls.py`: URL patterns
- `templates/`: HTML templates
- `static/`: Static files (CSS, JavaScript, images)

## Custom Management Commands
- `python3 manage.py mark_as_shipped`: Generates tracking IDs for processing orders and marks them as shipped.

## Frontend
The frontend is built using HTML templates styled with Tailwind CSS. Key pages include:
- Home page
- Product listing and details
- Shopping cart
- Checkout process
- User registration and login
- Order confirmation and details

## Notes
- **Media Files**: Ensure the `media` directory is set up correctly to store uploaded product images. The `MEDIA_URL` and `MEDIA_ROOT` settings in `settings.py` handle this.
- **Decorators**: Custom decorators like `login_required_user` and `redirect_authenticated_user` are used to manage access control for various views.
- **Forms**: The project uses Django's ModelForm for handling forms related to `Order`, `Payment`, `Contact`, and `NewsletterSubscription`.
---

This project serves as an excellent starting point for students and developers interested in building modern e-commerce web applications using Django. Feel free to explore, modify, and extend the code to suit your needs. If you encounter any issues or have questions, please refer to the Django documentation or seek help from the community.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.


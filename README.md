# eShop - Your Ultimate Tech Destination

Welcome to eShop, a student project built using Django 5.0.6. This project is an e-commerce platform that provides users with a seamless shopping experience for the latest tech gadgets and accessories.

## Table of Contents
- [Installation](#installation)
- [Running the Project](#running-the-project)
- [Creating a Superuser](#creating-a-superuser)
- [Admin Panel Usage](#admin-panel-usage)
- [Notes](#notes)

## Installation

To get started with eShop, follow these steps:

1. **Clone the repository:**
    ```sh
    git clone https://github.com/zimNMM/ecommerce.git
    cd ecommerce
    ```

2. **Install the required packages:**
    Ensure you have `pip` installed and run:
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

To access the admin panel and manage the store's data, you need to create a superuser:

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
- **Products**: Add new products to the store. Note that the `product_id` is generated automatically. You need to provide:
  - Category
  - Name
  - Price
  - Quantity
  - Image

- **Orders**: View and manage customer orders.
- **Reviews**: Monitor product reviews from customers.
- **Payments**: Review payment details.

## Notes

- **Media Files**: Ensure the `media` directory is set up correctly to store uploaded product images. The `MEDIA_URL` and `MEDIA_ROOT` settings in `settings.py` handle this.

- **Decorators**: Custom decorators like `login_required_user` and `redirect_authenticated_user` are used to manage access control for various views.

- **Templates**: The HTML templates are styled using Tailwind CSS and include various pages like:
  - Home
  - Product listing and details
  - Cart and checkout
  - User registration and login
  - Order confirmation and details

- **Forms**: The project uses Django's ModelForm for handling forms related to `Order`, `Payment`, `Contact`, and `NewsletterSubscription`.

---

This project is an excellent starting point for students and developers interested in building modern e-commerce web applications using Django. Feel free to explore and modify the code to suit your needs. If you encounter any issues, please refer to the Django documentation or seek help from the community.

Happy coding!


# jua
E-Commerce Website Readme

Introduction

Welcome to our E-Commerce Website powered by Flask! This web application provides a robust platform for online shopping, allowing users to browse products, add them to their cart, and securely complete transactions.

Features

User Authentication: Secure user registration and login functionality.
Product Catalog: Browse a diverse range of products with detailed descriptions and images.
Shopping Cart: Add products to your cart, review items, and proceed to checkout.
Order Management: Track your order history and view order details.
Admin Panel: Manage products, orders, and user accounts through an intuitive admin interface.
Installation

Clone the Repository:
bash
Copy code
git clone https://github.com/juanmz1/jua.git
cd e-commerce-flask
Create a Virtual Environment:
Copy code
python -m venv venv
Activate the Virtual Environment:
On Windows:
Copy code
venv\Scripts\activate
On macOS/Linux:
bash
Copy code
source venv/bin/activate
Install Dependencies:
Copy code
pip install -r requirements.txt
Configure Environment Variables:
Create a .env file in the root directory and set the following variables:
makefile
Copy code
SECRET_KEY=your_secret_key
DATABASE_URI=your_database_uri
Initialize the Database:
csharp
Copy code
flask db init
flask db migrate
flask db upgrade
Run the Application:
arduino
Copy code
flask run
Visit http://127.0.0.1:5000 in your browser to access the website.
Usage

Access the website and explore products.
Create an account or log in to manage your cart and place orders.
Admins can access the admin panel at /admin to manage products, orders, and users.
Contributing

We welcome contributions! Feel free to open issues, submit pull requests, or provide feedback.

License

This project is licensed under the MIT License.

Thank you for choosing our E-Commerce Website powered by Flask! If you have any questions or encounter issues, please don't hesitate to reach out.

Happy shopping! 🛍️

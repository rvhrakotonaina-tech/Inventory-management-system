# Inventory Management System

A web-based inventory management system built with Python Flask and MySQL, featuring product tracking, supplier management, and sales monitoring.

## Features

- 📦 Product management (CRUD operations)
- 🏭 Supplier management
- 💰 Sales tracking
- 📊 Dashboard with key metrics
- 🔍 Search and filter functionality
- 📱 Responsive design

## Prerequisites

- Python 3.8+
- MySQL Server
- pip (Python package manager)

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/inventory-management-system.git
   cd inventory-management-system
   ```

2. **Create and activate a virtual environment**
   ```bash
   python -m venv venv
   .\venv\Scripts\activate  # On Windows
   # or
   source venv/bin/activate  # On macOS/Linux
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up the database**
   - Create a new MySQL database named `inventory_db`
   - Import the database schema from `database/schema.sql`

5. **Configure environment variables**
   - Copy `.env.example` to `.env`
   - Update the database credentials in `.env`
   ```env
   DB_HOST=localhost
   DB_USER=your_username
   DB_PASSWORD=your_password
   DB_NAME=inventory_db
   SECRET_KEY=your-secret-key-here
   ```

6. **Run the application**
   ```bash
   python app.py
   ```

7. **Access the application**
   Open your browser and go to `http://localhost:5000`

## Project Structure

```
inventory-management-system/
├── app.py                # Main application file
├── requirements.txt      # Python dependencies
├── .env                  # Environment variables (ignored by git)
├── .gitignore            # Git ignore file
├── README.md             # This file
├── static/               # Static files (CSS, JS, images)
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── main.js
├── templates/            # HTML templates
│   ├── base.html
│   ├── index.html
│   ├── products.html
│   ├── sales.html
│   └── suppliers.html
└── database/
    └── schema.sql        # Database schema
```

## Contributing

1. Fork the repository
2. Create a new branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

Distributed under the MIT License. See `LICENSE` for more information.

## Contact

Hyacinthe Venceslas R. - [my_twitter](https://twitter.com/@Hrakotonaina) - rvhrakotonaina@gmail.com

Project Link: [https://github.com/you/inventory-management-system](https://github.com/rvhrakotonaina-tech/inventory-management-system)

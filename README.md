
# Long Chau Pharmacy Management System (LC-PMS)

An object-oriented, web-based pharmacy management system for streamlining the daily operations of Long Chau Pharmacy.

---

## Table of Contents

* [Key Features](#key-features)
* [Tech Stack](#tech-stack)
* [Setup Instructions](#setup-instructions)
* [Usage Guide](#usage-guide)

---

## Key Features

* **User Authentication**: Login & roles (Customer, Pharmacist, Manager, Admin, WarehouseStaff)
* **Order Management**: Place/view/process orders for both prescription and non-prescription products
* **Prescription Validation**: Pharmacist review and approval flows

---

## Tech Stack

* **Backend:** Python 3.10+, Django
* **Frontend:** Django Templates, Bootstrap CSS
* **Database:** SQLite (default, in development)
* **Dependency Management:** Pipenv (`Pipfile`, `Pipfile.lock`)
* **Version Control:** Git

---

## Setup Instructions

**Works on Windows, macOS, and Linux!**

### 1. Prerequisites

* **Python 3.10+** ([download](https://www.python.org/downloads/))
* **Pipenv**

  ```bash
  pip install pipenv
  ```
* **Git**

### 2. Clone the Repository

```bash
git clone https://github.com/<username>/<repo-name>.git
cd <repo-name>/pharmacy_rebuild
```

### 3. Install Dependencies

```bash
pipenv install
```

### 4. Activate the Virtual Environment

```bash
pipenv shell
```

### 5. Apply Database Migrations

(If you want a fresh database, delete `db.sqlite3` before this step.)

```bash
python manage.py migrate
```

### 6. Create an Admin User

```bash
python manage.py createsuperuser
```

### 7. Run the Development Server

```bash
python manage.py runserver
```

Open [http://127.0.0.1:8000/](http://127.0.0.1:8000/) in your browser.

---

## Usage Guide

* **Customers:**
  Register/login, browse products, place orders, upload/view prescriptions, check order history.

* **Pharmacists:**
  Login to review/validate prescriptions, process walk-in orders, see queues/history.

* **Managers/Admins:**
  Inventory control, staff/role management, access basic reports.

---


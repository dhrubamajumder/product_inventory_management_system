#  POS Inventory Management System

## Dashboard
---
## USER SETTING
### 👤 users

```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQE,
    password TEXT NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 🎭 roles
```sql
CREATE TABLE roles (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL
);
```

### 🔐 permissions
```sql
CREATE TABLE permissions (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL
);
```

### 🔗 role_permissions
```sql
CREATE TABLE role_permissions (
    role_id INT REFERENCES roles(id) ON DELETE CASCADE,
    permission_id INT REFERENCES permissions(id) ON DELETE CASCADE,
    PRIMARY KEY (role_id, permission_id)
);
```

### 🔗 user_roles
```sql
CREATE TABLE user_roles (
    user_id INT REFERENCES users(id) ON DELETE CASCADE,
    role_id INT REFERENCES roles(id) ON DELETE CASCADE,
    PRIMARY KEY (user_id, role_id)
);
```
## BASIC SETTING
### 🚚 suppliers
```sql
CREATE TABLE suppliers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(150),
    phone VARCHAR(20),
    address TEXT
);
```


### 👥 customers
```sql
CREATE TABLE customers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(150),
    email VARCHAR(100),
    phone VARCHAR(20),
    address TEXT,
    note TEXT
);
```


### 💸 expense_categories
```sql
CREATE TABLE expense_categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100)
);
```


### 💰 income_categories
```sql
CREATE TABLE income_categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100)
);
```

### ⚙️ settings (Company info) ( key value pear )
```sql
CREATE TABLE settings (
    id SERIAL PRIMARY KEY,
    setting_key VARCHAR(100) UNIQUE NOT NULL,
    setting_value TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## PRODUCT SETTINGS
### 🗂️ categories
```sql
CREATE TABLE categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100)
);
```


### 📦 products
```sql
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    category_id INT REFERENCES categories(id),
    name VARCHAR(150),
    sku VARCHAR(50),
    price NUMERIC(10,2),
    stock INT DEFAULT 0
);
```

## PURCHASE
### 🧾 purchases
```sql
CREATE TABLE purchases (
    id SERIAL PRIMARY KEY,
    supplier_id INT REFERENCES suppliers(id),
    total_amount NUMERIC(10,2),
    purchase_date DATE DEFAULT CURRENT_DATE
    purchase_payment VARCHAR(20)
);
```

### 📦 purchase_items
```sql
CREATE TABLE purchase_items (
    id SERIAL PRIMARY KEY, 
    purchase_id INT REFERENCES purchases(id) ON DELETE CASCADE,
    product_id INT REFERENCES products(id),
    quantity INT,
    price NUMERIC(10,2),
    

);
```


### 🔄 purchase_returns
```sql
CREATE TABLE purchase_returns (
    id SERIAL PRIMARY KEY,
    purchase_id INT REFERENCES purchases(id),
    amount NUMERIC(10,2), 
    return_date DATE DEFAULT CURRENT_DATE,
    purchase_return_payment VARCHAR(20)
);
```

## COLLECT ORDER / SALES
### 🧾 orders
```sql
CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    table_number VARCHAR(20),
    order_type VARCHAR(20),
    customer_id INT REFERENCES c ustomers(id),
    grand_total NUMERIC(10,2),
    discount NUMERIC(10,2),
    payable_amount NUMERIC(10,2),
    paid_amount NUMERIC(10,2),
    change_amount NUMERIC(10,2),
    status VARCHAR(20) DEFAULT 'pending',
    fund VARCHAR(20)
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 🛒 order_items
```sql
CREATE TABLE order_items (
    id SERIAL PRIMARY KEY,
    order_id INT REFERENCES orders(id) ON DELETE CASCADE,
    product_id INT REFERENCES products(id),
    quantity INT,
    price NUMERIC(10,2),
    total_price NUMERIC(10,2)
);
```

## FINANCE
### 💸 expenses
```sql
CREATE TABLE expenses (
    id SERIAL PRIMARY KEY,
    category_id INT REFERENCES expense_categories(id),
    amount NUMERIC(10,2),
    note TEXT,
    expense_date DATE DEFAULT CURRENT_DATE
);
```

### 💰 other_income
```sql
CREATE TABLE other_income (
    id SERIAL PRIMARY KEY,
    category_id INT REFERENCES income_categories(id),
    amount NUMERIC(10,2),
    note TEXT,
    income_date DATE DEFAULT CURRENT_DATE
);
```

### 🧾 supplier_payments
```sql
CREATE TABLE supplier_payments (
    id SERIAL PRIMARY KEY,
    supplier_id INT REFERENCES suppliers(id),
    amount NUMERIC(10,2),
    payment_date DATE DEFAULT CURRENT_DATE
);
```
### customer payment
```sql
CREATE TABLE customer_payments (
    id SERIAL PRIMARY KEY,
    customer_id INT REFERENCES customer(id),
    amount NUMERIC(10,2),
    payment_date DATE DEFAULT CURRENT_DATE
);
```

# Stock Report
 ### stock 
```sql
CREATE TABLE stock (
    id SERIAL PRIMARY KEY,
    product_id INT REFERENCES product(id),
    quantity INT
    unit_cost NUMERIC(10,2)
);
```
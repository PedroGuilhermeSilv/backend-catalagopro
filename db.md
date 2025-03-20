Table users {
  id uuid [pk]
  name varchar
  email varchar [unique]
  password_hash varchar
  role user_role
  created_at timestamp
  updated_at timestamp

  indexes {
    email [unique]
  }
}

Table stores {
  id uuid [pk]
  owner_id uuid [ref: > users.id]
  name varchar
  slug varchar [unique]
  logo_url varchar
  description text
  address text
  whatsapp_number varchar
  created_at timestamp
  updated_at timestamp

  indexes {
    slug [unique]
  }
}

Table store_hours {
  id uuid [pk]
  store_id uuid [ref: > stores.id]
  day_of_week day_enum
  open_time time
  close_time time
  is_closed boolean
}

Table categories {
  id uuid [pk]
  store_id uuid [ref: > stores.id]
  name varchar
  description text
  order_index int
  created_at timestamp
  updated_at timestamp
}

Table products {
  id uuid [pk]
  store_id uuid [ref: > stores.id]
  category_id uuid [ref: > categories.id]
  name varchar
  description text
  image_url varchar
  in_stock int
  is_available boolean
  created_at timestamp
  updated_at timestamp

  indexes {
    (store_id, category_id)
  }
}

Table product_prices {
  id uuid [pk]
  product_id uuid [ref: > products.id]
  size_id uuid [ref: > sizes.id, null]
  price decimal
  created_at timestamp
  updated_at timestamp
}

Table sizes {
  id uuid [pk]
  store_id uuid [ref: > stores.id]
  name varchar
  description text
  created_at timestamp
  updated_at timestamp
}

Table orders {
  id uuid [pk]
  store_id uuid [ref: > stores.id]
  customer_name varchar
  customer_email varchar
  customer_phone varchar
  status order_status
  notes text
  total_amount decimal
  created_at timestamp
  updated_at timestamp

  indexes {
    (store_id, created_at)
  }
}

Table order_items {
  id uuid [pk]
  order_id uuid [ref: > orders.id]
  product_id uuid [ref: > products.id]
  size_id uuid [ref: > sizes.id, null]
  quantity int
  unit_price decimal
  subtotal decimal
  notes text

  indexes {
    order_id
  }
}

Table store_staff {
  id uuid [pk]
  store_id uuid [ref: > stores.id]
  user_id uuid [ref: > users.id]
  role staff_role
  created_at timestamp
  updated_at timestamp
}

Table menu_views {
  id uuid [pk]
  store_id uuid [ref: > stores.id]
  viewed_at timestamp
  ip_address varchar
  user_agent varchar

  indexes {
    (store_id, viewed_at)
  }
}

Table promotions {
  id uuid [pk]
  store_id uuid [ref: > stores.id]
  name varchar
  description text
  discount_type discount_enum
  discount_value decimal
  start_date timestamp
  end_date timestamp
  is_active boolean
  created_at timestamp
  updated_at timestamp
}

Table promotion_products {
  id uuid [pk]
  promotion_id uuid [ref: > promotions.id]
  product_id uuid [ref: > products.id]
}

Enum user_role {
  admin
  customer
}

Enum staff_role {
  manager
  staff
  cashier
}

Enum order_status {
  new
  preparing
  ready
  delivered
  cancelled
}

Enum day_enum {
  monday
  tuesday
  wednesday
  thursday
  friday
  saturday
  sunday
}

Enum discount_enum {
  percentage
  fixed_amount
}

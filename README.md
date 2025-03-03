# Documentação de Rotas: Input/Output

## 1. Rotas Públicas (Frontend)

### GET /
**Input:** Nenhum
**Output:**
```typescript
{
  featuredStores: {
    id: string
    name: string
    logo: string
    description: string
  }[]
}
```

### GET /signup
**Input (Form):**
```typescript
{
  name: string
  email: string
  password: string
  storeName: string
}
```
**Output:** Redirecionamento para `/store/[storeId]/admin/dashboard`

### GET /login
**Input (Form):**
```typescript
{
  email: string
  password: string
}
```
**Output:** Redirecionamento para `/store/[storeId]/admin/dashboard`

### GET /store/[storeId]/menu
**Input:**
```typescript
{
  storeId: string
}
```
**Output:**
```typescript
{
  store: {
    id: string
    name: string
    logo: string
    description: string
    address: string
    openingHours: Record<string, string>
    isOpen: boolean
  }
  menu: {
    id: number
    name: string
    price: number | Record<string, number>
    description: string
    category: string
    image: string
    sizes?: string[]
    inStock: number
  }[]
}
```

### GET /store/[storeId]/menu/checkout
**Input:**
```typescript
{
  storeId: string
  cart: {
    id: number
    name: string
    price: number
    quantity: number
    size?: string
  }[]
}
```
**Output:**
```typescript
{
  orderSummary: {
    items: {
      name: string
      quantity: number
      size?: string
      price: number
    }[]
    total: number
  }
}
```

### GET /store/[storeId]/menu/checkout-wpp
**Input:**
```typescript
{
  storeId: string
  customerInfo: {
    name: string
    email: string
    notes?: string
  }
  order: {
    items: {
      name: string
      quantity: number
      size?: string
      price: number
    }[]
    total: number
  }
}
```
**Output:** Redirecionamento para WhatsApp com mensagem formatada

## 2. Rotas Administrativas (Frontend)

### GET /store/[storeId]/admin/dashboard
**Input:**
```typescript
{
  storeId: string
}
```
**Output:**
```typescript
{
  statistics: {
    totalOrders: number
    todayOrders: number
    revenue: {
      daily: number
      weekly: number
      monthly: number
    }
    popularItems: {
      name: string
      quantity: number
    }[]
  }
  recentOrders: Order[]
}
```

### GET /store/[storeId]/admin/menu
**Input:**
```typescript
{
  storeId: string
}
```
**Output:**
```typescript
{
  menuItems: {
    id: number
    name: string
    price: number | Record<string, number>
    description: string
    category: string
    image: string
    sizes?: string[]
    inStock: number
  }[]
  categories: string[]
}
```

### GET /store/[storeId]/admin/orders
**Input:**
```typescript
{
  storeId: string
  filter?: {
    status: 'new' | 'preparing' | 'ready' | 'delivered'
    dateRange?: {
      start: Date
      end: Date
    }
  }
}
```
**Output:**
```typescript
{
  orders: {
    id: number
    customerName: string
    customerEmail: string
    items: {
      name: string
      quantity: number
      size?: string
      price: number
    }[]
    total: number
    status: 'new' | 'preparing' | 'ready' | 'delivered'
    createdAt: Date
    notes?: string
  }[]
}
```

## 3. Rotas da API

### GET /api/store/[storeId]
**Input:**
```typescript
{
  storeId: string
}
```
**Output:**
```typescript
{
  id: string
  name: string
  logo: string
  description: string
  address: string
  openingHours: Record<string, string>
  whatsappNumber: string
}
```

### PUT /api/store/[storeId]
**Input:**
```typescript
{
  storeId: string
  data: {
    name?: string
    logo?: string
    description?: string
    address?: string
    openingHours?: Record<string, string>
    whatsappNumber?: string
  }
}
```
**Output:**
```typescript
{
  success: boolean
  store: Store
}
```

### GET /api/store/[storeId]/menu
**Input:**
```typescript
{
  storeId: string
  category?: string
  search?: string
}
```
**Output:**
```typescript
{
  items: MenuItem[]
  categories: string[]
}
```

### POST /api/store/[storeId]/menu
**Input:**
```typescript
{
  storeId: string
  item: {
    name: string
    price: number | Record<string, number>
    description: string
    category: string
    image: string
    sizes?: string[]
    inStock: number
  }
}
```
**Output:**
```typescript
{
  success: boolean
  item: MenuItem
}
```

### PUT /api/store/[storeId]/menu/[id]
**Input:**
```typescript
{
  storeId: string
  itemId: number
  data: {
    name?: string
    price?: number | Record<string, number>
    description?: string
    category?: string
    image?: string
    sizes?: string[]
    inStock?: number
  }
}
```
**Output:**
```typescript
{
  success: boolean
  item: MenuItem
}
```

### DELETE /api/store/[storeId]/menu/[id]
**Input:**
```typescript
{
  storeId: string
  itemId: number
}
```
**Output:**
```typescript
{
  success: boolean
}
```

### GET /api/store/[storeId]/orders
**Input:**
```typescript
{
  storeId: string
  status?: 'new' | 'preparing' | 'ready' | 'delivered'
  startDate?: Date
  endDate?: Date
}
```
**Output:**
```typescript
{
  orders: Order[]
  pagination: {
    total: number
    page: number
    pageSize: number
  }
}
```

### POST /api/store/[storeId]/orders
**Input:**
```typescript
{
  storeId: string
  order: {
    customerName: string
    customerEmail: string
    items: {
      id: number
      quantity: number
      size?: string
    }[]
    notes?: string
  }
}
```
**Output:**
```typescript
{
  success: boolean
  order: Order
  whatsappRedirectUrl?: string
}
```

### PUT /api/store/[storeId]/orders/[id]
**Input:**
```typescript
{
  storeId: string
  orderId: number
  data: {
    status?: 'new' | 'preparing' | 'ready' | 'delivered'
    notes?: string
  }
}
```
**Output:**
```typescript
{
  success: boolean
  order: Order
}
```

### POST /api/auth/login
**Input:**
```typescript
{
  email: string
  password: string
}
```
**Output:**
```typescript
{
  success: boolean
  token: string
  user: {
    id: string
    name: string
    email: string
    storeId?: string
    role: 'admin' | 'staff'
  }
}
```

### POST /api/auth/signup
**Input:**
```typescript
{
  name: string
  email: string
  password: string
  storeName: string
}
```
**Output:**
```typescript
{
  success: boolean
  token: string
  user: {
    id: string
    name: string
    email: string
    storeId: string
    role: 'admin'
  }
  store: {
    id: string
    name: string
  }
}
```

### POST /api/auth/logout
**Input:** Token no header de autorização
**Output:**
```typescript
{
  success: boolean
}
```

Cada rota inclui:
- Validação de dados
- Tratamento de erros
- Respostas de erro padronizadas
- Autenticação quando necessária
- Rate limiting
- Logs de acesso

Códigos de status HTTP apropriados são retornados para cada operação:
- 200: Sucesso
- 201: Criado
- 400: Erro de validação
- 401: Não autorizado
- 403: Proibido
- 404: Não encontrado
- 500: Erro interno

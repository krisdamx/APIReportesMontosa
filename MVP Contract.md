# Sales Analytics API
## MVP Contract v1.1

## Objetivo

La API permite:

- Autenticar usuarios.
- Importar información mediante archivos CSV.
- Consultar el historial de cargas.
- Obtener información analítica para el Dashboard Ejecutivo.

La Base de Datos es la única fuente de verdad.

Los archivos CSV representan únicamente el mecanismo de importación de información.

---

# Autenticación

Todas las peticiones requieren JWT excepto el Login.

Header requerido

```
Authorization: Bearer {token}
```

---

# Authentication

## Login

POST /auth/login

Request

```json
{
    "username": "admin",
    "password": "123456"
}
```

Response

```json
{
    "access_token": "...",
    "token_type": "bearer"
}
```

---

## Usuario autenticado

GET /auth/me

Response

```json
{
    "id": 1,
    "username": "admin",
    "nombre": "Administrador"
}
```

---

## Logout

POST /auth/logout

Response

```json
{
    "message": "Sesión cerrada correctamente."
}
```

---

# Upload

## Subir archivo

POST /upload

Content-Type

```
multipart/form-data
```

Body

```
file : CSV
```

Response

```json
{
    "id": 5,
    "filename": "DIA5.csv",
    "records": 8376,
    "duplicates": 18,
    "status": "COMPLETED",
    "processingTime": 7469
}
```

---

# Files

## Historial de cargas

GET /files

Response

```json
[
    {
        "id": 5,
        "nombre_original": "DIA5.csv",
        "total_registros": 8376,
        "status": "COMPLETED",
        "created_at": "2026-07-29T23:30:48"
    }
]
```

---

## Detalle de una carga

GET /files/{id}

Response

```json
{
    "id": 5,
    "nombre_original": "DIA5.csv",
    "extension": ".csv",
    "mime_type": "text/csv",
    "file_size": 2470326,
    "total_registros": 8376,
    "processing_time_ms": 7469,
    "status": "COMPLETED",
    "created_at": "2026-07-29T23:30:48"
}
```

Reglas

- Solo el usuario propietario puede consultar sus archivos.
- Si el archivo no existe o pertenece a otro usuario se devuelve 404.

---

# Dashboard

## Objetivo

El Dashboard consulta la información almacenada en la Base de Datos.

Los archivos únicamente sirven para importar información.

Toda la información del Dashboard es filtrable.

---

# Dashboard Summary

GET /dashboard/summary

Obtiene los principales indicadores ejecutivos.

Query Parameters

| Parámetro | Tipo | Requerido |
|-----------|------|-----------|
| fechaInicio | date | No |
| fechaFin | date | No |
| fabricante | string | No |
| marca | string | No |
| plaza | string | No |
| canal | string | No |
| compania | string | No |
| cliente | string | No |
| producto | string | No |
| presentacion | string | No |
| sabor | string | No |
| clasificacion | string | No |
| anio | int | No |

Response

```json
{
    "ventas":1254632.54,
    "clientes":1258,
    "cf":985.32,
    "hlt":754.61,
    "cajas":8452,
    "pedidos":853,
    "ticketPromedio":1470.73
}
```

---

# Dashboard Analytics

GET /dashboard/analytics

Endpoint genérico para construir todas las gráficas y tablas del Dashboard.

---

## Query Parameters

### Métricas

Permite solicitar una o varias métricas.

```
metrics=ventas
```

```
metrics=ventas,hlt,cajas
```

Métricas soportadas

- ventas
- importeBruto
- hlt
- cf
- cajas
- clientes
- pedidos
- ticketPromedio
- productosVendidos

---

### Agrupaciones

Permite agrupar por uno o varios niveles.

Ejemplos

```
groupBy=marca
```

```
groupBy=fabricante
```

```
groupBy=plaza
```

```
groupBy=plaza,canal
```

```
groupBy=marca,producto
```

Agrupaciones soportadas

- fabricante
- marca
- plaza
- canal
- cliente
- producto
- presentacion
- sabor
- clasificacion
- compania
- fecha
- mes
- anio

---

### Función de agregación

```
aggregate=sum
```

Valores soportados

- sum
- avg
- count
- max
- min

---

### Ordenamiento

```
orderBy=ventas
```

```
order=asc
```

```
order=desc
```

---

### Límite de resultados

```
limit=10
```

---

### Totales

```
includeTotals=true
```

---

### Filtros

Todos los filtros son opcionales.

| Parámetro |
|------------|
| fechaInicio |
| fechaFin |
| fabricante |
| marca |
| plaza |
| canal |
| compania |
| cliente |
| producto |
| presentacion |
| sabor |
| clasificacion |
| anio |

---

## Ejemplos

Ventas por Marca

```
GET /dashboard/analytics?metrics=ventas&groupBy=marca
```

Ventas por Plaza

```
GET /dashboard/analytics?metrics=ventas&groupBy=plaza
```

Ventas por Canal

```
GET /dashboard/analytics?metrics=ventas&groupBy=canal
```

Ventas por Fabricante

```
GET /dashboard/analytics?metrics=ventas&groupBy=fabricante
```

HLT por Marca

```
GET /dashboard/analytics?metrics=hlt&groupBy=marca
```

CF por Canal

```
GET /dashboard/analytics?metrics=cf&groupBy=canal
```

Top 10 Productos

```
GET /dashboard/analytics?metrics=ventas&groupBy=producto&limit=10
```

Ventas por Plaza y Canal

```
GET /dashboard/analytics?metrics=ventas,hlt,cajas&groupBy=plaza,canal
```

Comparativo por Año

```
GET /dashboard/analytics?metrics=ventas&groupBy=anio
```

Evolución Mensual

```
GET /dashboard/analytics?metrics=ventas&groupBy=mes
```

---

## Response

```json
{
    "metadata": {
        "metrics": [
            "ventas",
            "hlt",
            "cajas"
        ],
        "groupBy": [
            "plaza",
            "canal"
        ],
        "records": 8
    },
    "totals": {
        "ventas": 1250000,
        "hlt": 852,
        "cajas": 4200
    },
    "data": [
        {
            "plaza": "COSAMALOAPAN",
            "canal": "DETALLE",
            "ventas": 125000,
            "hlt": 850,
            "cajas": 4200
        },
        {
            "plaza": "VERACRUZ",
            "canal": "TDC",
            "ventas": 98000,
            "hlt": 620,
            "cajas": 3100
        }
    ]
}
```

---

# Dashboard Catalogs

GET /dashboard/catalogs

Obtiene todos los catálogos necesarios para construir los filtros del Dashboard.

Response

```json
{
    "fabricantes": [],
    "marcas": [],
    "plazas": [],
    "canales": [],
    "companias": [],
    "clientes": [],
    "productos": [],
    "presentaciones": [],
    "sabores": [],
    "clasificaciones": [],
    "anios": []
}
```

---

# Códigos HTTP

| Código | Descripción |
|---------|-------------|
| 200 | Operación exitosa |
| 201 | Recurso creado |
| 400 | Petición inválida |
| 401 | No autenticado |
| 403 | Acceso denegado |
| 404 | Recurso no encontrado |
| 422 | Error de validación |
| 500 | Error interno del servidor |

---

# Flujo General

```
Login
    │
    ▼
Obtener JWT
    │
    ▼
Subir CSV
    │
    ▼
Consultar Historial
    │
    ▼
Seleccionar filtros
    │
    ▼
Consultar Summary
    │
    ▼
Consultar Analytics
    │
    ▼
Visualizar Dashboard
```

---

# Estado del MVP

## Implementado

- ✅ Login
- ✅ Auth Me
- ✅ Logout
- ✅ Upload CSV
- ✅ Historial de archivos
- ✅ Detalle de archivo

## En Desarrollo

- 🚧 Dashboard Summary
- 🚧 Dashboard Analytics
- 🚧 Dashboard Catalogs

---

# Notas

- Todos los endpoints del Dashboard consultan directamente la Base de Datos.
- Los archivos CSV únicamente representan el proceso de importación (ETL).
- El endpoint **/dashboard/analytics** será la base para todas las tablas y gráficas del Dashboard Ejecutivo.
- El objetivo del contrato es evitar la creación de endpoints específicos para cada visualización y mantener una API flexible y escalable.
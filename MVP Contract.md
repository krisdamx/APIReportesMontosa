# Sales Analytics API
## MVP Contract v1.0

## Objetivo

La API permite:

- Autenticar usuarios.
- Importar información mediante archivos CSV.
- Consultar el historial de cargas.
- Obtener información analítica para el Dashboard.

La Base de Datos es la fuente de verdad.

Los archivos únicamente representan el mecanismo de importación de información.

---

# Autenticación

Todas las peticiones requieren JWT excepto el Login.

Header requerido:

Authorization: Bearer {token}

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

# Uploads

## Subir archivo

POST /upload

Content-Type

multipart/form-data

Body

file : CSV

Response

```json
{
    "id": 5,
    "filename": "DIA5.csv",
    "records": 8376,
    "status": "COMPLETED"
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

No consulta directamente los archivos CSV.

Toda la información es filtrable.

---

## Dashboard Summary

GET /dashboard/summary

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

Response

```json
{
    "ventas": 1254632.54,
    "clientes": 1258,
    "cf": 985.32,
    "hlt": 754.61,
    "cajas": 8452
}
```

---

## Dashboard Analytics

GET /dashboard/analytics

Endpoint utilizado para alimentar todas las gráficas.

Query Parameters

| Parámetro | Tipo |
|-----------|------|
| metric | string |
| groupBy | string |
| fechaInicio | date |
| fechaFin | date |
| fabricante | string |
| marca | string |
| plaza | string |
| canal | string |
| compania | string |
| producto | string |

Ejemplos

Ventas por Marca

```
GET /dashboard/analytics?metric=ventas&groupBy=marca
```

Ventas por Fabricante

```
GET /dashboard/analytics?metric=ventas&groupBy=fabricante
```

Ventas por Plaza

```
GET /dashboard/analytics?metric=ventas&groupBy=plaza
```

CF por Canal

```
GET /dashboard/analytics?metric=cf&groupBy=canal
```

HLT por Marca

```
GET /dashboard/analytics?metric=hlt&groupBy=marca
```

Response

```json
[
    {
        "label": "Peñafiel",
        "value": 125462.52
    },
    {
        "label": "Bonafont",
        "value": 98541.33
    }
]
```

---

## Catálogos

GET /dashboard/catalogs

Obtiene los datos necesarios para poblar todos los filtros del Dashboard.

Response

```json
{
    "fabricantes": [],
    "marcas": [],
    "plazas": [],
    "canales": [],
    "companias": [],
    "productos": [],
    "presentaciones": [],
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
| 404 | Recurso no encontrado |
| 500 | Error interno |

---

# Flujo General

Login

↓

Obtener JWT

↓

Subir CSV

↓

Consultar Historial

↓

Seleccionar filtros

↓

Consultar Dashboard

↓

Visualizar gráficas

---

# Estado del MVP

## Implementado

- Login
- Auth Me
- Logout
- Upload CSV
- Historial de archivos
- Detalle de archivo

## Pendiente

- Dashboard Summary
- Dashboard Analytics
- Dashboard Catalogs

# Sales Analytics API

## MVP Contract v2.0

> Documento actualizado con el estado actual del backend.

------------------------------------------------------------------------

# Objetivo

La API permite:

-   Autenticar usuarios.
-   Importar archivos CSV.
-   Consultar historial de cargas.
-   Consultar información ejecutiva mediante Dashboard.
-   Obtener catálogos para filtros.
-   Construir cualquier gráfica o tabla mediante un único endpoint de
    Analytics.

La Base de Datos es la única fuente de verdad.

Los archivos CSV representan únicamente el proceso de importación (ETL).

------------------------------------------------------------------------

# Autenticación

Todas las peticiones requieren JWT excepto Login.

Header:

``` http
Authorization: Bearer {token}
```

------------------------------------------------------------------------

# Authentication

## Login

`POST /auth/login`

### Request

``` json
{
  "username":"admin",
  "password":"123456"
}
```

### Response

``` json
{
  "access_token":"...",
  "token_type":"bearer"
}
```

------------------------------------------------------------------------

## Usuario autenticado

`GET /auth/me`

``` json
{
  "id":1,
  "username":"admin",
  "nombre":"Administrador"
}
```

------------------------------------------------------------------------

## Logout

`POST /auth/logout`

``` json
{
  "message":"Sesión cerrada correctamente."
}
```

------------------------------------------------------------------------

# Upload

## Subir archivo

`POST /upload`

Content-Type:

``` text
multipart/form-data
```

Body

``` text
file : CSV
```

Respuesta

``` json
{
  "id":5,
  "filename":"DIA5.csv",
  "records":8376,
  "duplicates":18,
  "status":"COMPLETED",
  "processingTime":7469
}
```

------------------------------------------------------------------------

# Files

## Historial

`GET /files`

## Detalle

`GET /files/{id}`

Reglas:

-   Sólo el propietario puede consultar el archivo.
-   Si no existe devuelve 404.

------------------------------------------------------------------------

# Dashboard

Todos los endpoints consultan directamente la Base de Datos.

Los filtros disponibles son:

  Parámetro
  ---------------
  fechaInicio
  fechaFin
  fabricante
  marca
  plaza
  canal
  compania
  producto
  presentacion
  sabor
  clasificacion
  anio

> **Cliente ya no forma parte de los filtros del Dashboard.**

------------------------------------------------------------------------

# Dashboard Catalogs

`GET /dashboard/catalogs`

Obtiene todos los catálogos para construir los filtros.

``` json
{
  "fabricantes":[],
  "marcas":[],
  "plazas":[],
  "canales":[],
  "companias":[],
  "productos":[],
  "presentaciones":[],
  "sabores":[],
  "clasificaciones":[],
  "anios":[]
}
```

Notas:

-   Los productos devuelven:
    -   label = descripcion_producto
    -   value = producto
-   Se eliminan valores vacíos y "#N/D".

------------------------------------------------------------------------

# Dashboard Summary

`GET /dashboard/summary`

## Response

``` json
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

------------------------------------------------------------------------

# Dashboard Analytics

`GET /dashboard/analytics`

Endpoint genérico para construir todas las tablas y gráficas.

## Parámetros

### metrics

-   ventas
-   importeBruto
-   hlt
-   cf
-   cajas
-   clientes
-   pedidos
-   ticketPromedio
-   productosVendidos

Ejemplos

``` text
metrics=ventas
metrics=ventas,hlt,cajas
```

### groupBy

-   fabricante
-   marca
-   plaza
-   canal
-   producto
-   presentacion
-   sabor
-   clasificacion
-   compania
-   fecha
-   mes
-   anio

### aggregate

Actualmente soportado:

``` text
sum
```

(Reservado para futuras versiones: avg, count, min, max.)

### orderBy

``` text
orderBy=ventas
```

### order

``` text
asc
desc
```

### limit

``` text
limit=10
```

### includeTotals

``` text
true
false
```

## Ejemplos

``` text
GET /dashboard/analytics?metrics=ventas&groupBy=marca

GET /dashboard/analytics?metrics=ventas,hlt,cajas&groupBy=plaza,canal

GET /dashboard/analytics?metrics=ventas&groupBy=mes

GET /dashboard/analytics?metrics=ticketPromedio&groupBy=canal

GET /dashboard/analytics?metrics=ventas&groupBy=producto&limit=10
```

## Response

``` json
{
  "metadata":{
    "metrics":["ventas"],
    "groupBy":["marca"],
    "records":44
  },
  "totals":{
    "ventas":88190194.22
  },
  "data":[
    {
      "marca":"BONAFONT BOTELLA",
      "ventas":12102580.50
    }
  ]
}
```

------------------------------------------------------------------------

# Reglas de negocio

-   Todos los endpoints del Dashboard consultan la Base de Datos.
-   Los CSV sólo sirven para importar información.
-   Analytics es el único endpoint requerido para tablas y gráficas.
-   Summary utiliza exactamente los mismos filtros que Analytics.
-   Los totales respetan los filtros aplicados.
-   ticketPromedio = ventas / pedidos.

------------------------------------------------------------------------

# Códigos HTTP

  Código   Descripción
  -------- ---------------------
  200      OK
  201      Creado
  400      Solicitud inválida
  401      No autenticado
  403      Prohibido
  404      No encontrado
  422      Error de validación
  500      Error interno

------------------------------------------------------------------------

# Estado del MVP

## Implementado

-   ✅ Login
-   ✅ Auth Me
-   ✅ Logout
-   ✅ Upload CSV
-   ✅ Historial de archivos
-   ✅ Detalle de archivos
-   ✅ Dashboard Catalogs
-   ✅ Dashboard Summary
-   ✅ Dashboard Analytics

## Pendientes

-   Optimización de consultas (\>20 s en datasets grandes).
-   Soporte completo para aggregate (avg, count, min, max).
-   Documentación OpenAPI definitiva.

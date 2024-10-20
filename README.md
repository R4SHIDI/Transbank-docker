
![Logo Duoc](https://upload.wikimedia.org/wikipedia/commons/thumb/a/aa/Logo_DuocUC.svg/2560px-Logo_DuocUC.svg.png)

# Proyecto Ferremas DUOC 


Proyecto realizado por alumnos de DUOC UC Plaza Norte, Chile. Correspondiente a la asignatura Integración de Plataformas bajo el caso Ferremas.

## Autores

- [@carlos_aravena](https://www.github.com/craravenav)
- [@pablo_olmos](https://www.github.com/reykred)
- [@alex_patino](https://www.github.com/r4shidi)

## Instrucciones Deployment[^1]

Debe tener instalado [**Docker Desktop**](https://www.docker.com/products/docker-desktop/) y funcionando el servicio Docker.

Primer Paso, clonar el proyecto:

```bash
  git clone https://github.com/craravenav/ferremas_integracion.git
```

Segundo paso, ir a la ruta del proyecto clonado

```bash
  cd ferremas_integracion
```

Tercer paso, Ejecutar el comando de docker para crear las imagenes y contenedores.

```bash
  docker compose up -d
```

Esto generará los servicios de API y Portal Web Utilizados para las 3 API's solicitadas.

> [!IMPORTANT]
> Para las API's sin Front se utilizara el Workspace de Postman al cual fue agregado.

![Worskpace Postman](https://i.imgur.com/hyqkQLk.png)


# Instrucciones de uso de API's

## API Banco Central
<details>

<summary> Ver API Banco Central</summary>

![Logo Bcentral](https://i.imgur.com/WVHDX7G.png)

Esta api permite ingresar cualquier monto en valor USD para que te entregue de vuelta el valor transformado usando el valor dolar del día.

#### Conversor Moneda USD a CLP

```http
  GET /usdtoclp?usd=${valor}
```

>| Parameter | Type     | Description                |
>| :-------- | :------- | :------------------------- |
>| `valor` | `string` | **Requerido** monto en dolares |

</details>

## API Conectada a Azure SQL Server
<details>
 
<summary> Ver API Conectada a SQL</summary>

![SQL Azure](https://i.imgur.com/Twbsbc1.png)

## **IMPORTANTE**
**Debido a que la Base SQL es bajo demanda tras realizar la primera petición se debe esperar un tiempo 20 a 30 seg para que la Base de datos levante los servicios y ejecutar nuevamente la petición.**

#### [GET] Lista todos los productos

```
  GET /producto?all
```

#### [GET] Lista los productos en base a un ID

```
  GET /producto?id=${id}
```

>| Parameter | Type     | Description                |
>| :-------- | :------- | :------------------------- |
>| `id` | `string` | **Requerido** id del producto a buscar |

#### [GET] Lista los productos en base a una Marca de Producto

```
  GET /producto?marca=${nombre}
```

>| Parameter | Type     | Description                |
>| :-------- | :------- | :------------------------- |
>| `nombre` | `string` | **Requerido** Nombre de la marca del producto a buscar |

#### [POST] Agrega un Producto (Requiere Body tipo JSON) [POSTMAN]

```
  POST /producto
```

Estructura de atributos del JSON

>| Parameter | Type     | Description                |
>| :-------- | :------- | :------------------------- |
>| `codigo_producto` | `string` | **Requerido** Código del producto que se va a Agregar |
>| `nombre` | `string` | Nombre del producto |
>| `codigo_marca` | `string` | Código de la marca del producto |
>| `marca` | `string` | Nombre de la marca del producto |
>| `categoria` | `string` | Categoria del producto |

Ejemplo:

```
{
    "categoria": "Taladro",
    "codigo_marca": "BOS-00100",
    "codigo_producto": "FER-000001",
    "marca": "Bosch",
    "nombre": "Taladro Percutor Editado"
}
```

#### [PUT] Edita un Producto (Requiere Body tipo JSON) [POSTMAN]

```
  PUT /producto
```

Estructura de atributos del JSON

>| Parameter | Type     | Description                |
>| :-------- | :------- | :------------------------- |
>| `codigo_producto` | `string` | **Requerido** Código del producto que se va a Agregar |
>| `nombre` | `string` | Nombre del producto |
>| `codigo_marca` | `string` | Código de la marca del producto |
>| `marca` | `string` | Nombre de la marca del producto |
>| `categoria` | `string` | Categoria del producto |

Ejemplo:

```
{
    "categoria": "Taladro EDITADO",
    "codigo_marca": "BOS-00101",
    "codigo_producto": "FER-000001",
    "marca": "Bosch",
    "nombre": "Taladro Percutor"
}
```

#### [DELETE] Elimina un producto en base a un ID

```
  DELETE /producto?id=${id}
```

>| Parameter | Type     | Description                |
>| :-------- | :------- | :------------------------- |
>| `id` | `string` | **Requerido** id del producto a buscar |


</details>

## API Transbank

<details>

<summary> Ver API Transbank</summary>

![Logo Transbank](https://publico.transbank.cl/o/fragmentos-theme/images/logo_transbank_color.svg)

**Ir al Carrito de Compras ->** [http:localhost:9100/portal-web/carro-compras.html](http://localhost:9100/portal-web/carro-compras.html) y seguir el flujo de pago de una transacción comun y corriente con transbank utilizando las tarjetas de pruebas descritas a continuación.


### Tarjetas de prueba Transbank

>| Tipo Tarjeta | Atributo    | Valor              |
>| :-------- | :------- | :------------------------- |
>| `DEBITO` | Numero | 4051 8856 0044 6623 |
>| | CVV |123|
>| | Fecha expiración |Cualquier fecha posterior al día|

>| Tipo Tarjeta | Atributo    | Valor              |
>| :-------- | :------- | :------------------------- |
>| `CREDITO` | Numero | 5186 0595 5959 0568 |
>| | CVV |123|
>| | Fecha expiración |Cualquier fecha posterior al día|

</details>


[^1]: Se debe ejecutar primero que cualquier API las instrucciones de deployment del apartado  **Instrucciones Deployment**


# Transbank-docker

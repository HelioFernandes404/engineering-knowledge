# Projeto Java

Implementação de um micro-serviço para uma API de cartorio:

## Índice da documentação

_Link do collection postman:_ [**Postman** **collection**](cartórios.postman_collection.json)

- [Atribuicaos](#Atribuicaos)
  - [Listagem paginada](#listagem-paginada)
  - [Inclusão de novo registro](#inclusão-de-novo-registro)
  - [Alteração de registro por ID](#alteração-de-registro-por-id)
  - [Exclusão de registro por ID](#exclusão-de-registro-por-id)
- [Cartorios](#Cartorios)
    - [Listagem paginada](#listagem-paginada-1)
    - [Inclusão de novo registro](#inclusão-de-novo-registro-1)
    - [Alteração de registro por ID](#alteração-de-registro-por-id-1)
    - [Exclusão de registro por ID](#exclusão-de-registro-por-id-1)
- [Situacaos](#Situacaos)
    - [Listagem paginada](#listagem-paginada-2)
    - [Inclusão de novo registro](#inclusão-de-novo-registro-2)
    - [Alteração de registro por ID](#alteração-de-registro-por-id-2)
    - [Exclusão de registro por ID](#exclusão-de-registro-por-id-2)
---
## Atribuicaos

#### Listagem paginada

**(GET)** http://localhost:9564/atribuicoes

-   Paginação:

    -   `page`: Número indicando qual a paginação. São retornados, no máximo, 10 resultados por página.
    `?page=2` => Pula os **primeiros 10** 

- response Body 

```json
{
  "content": [
    {
      "id": "ATR_CERTIDOES",
      "nome": "Emissão de Certidões"
    },
    {
      "id": "ATR_NOTARIA",
      "nome": "Notarização de Documentos"
    },
    {
      "id": "ATR_PROCESSOS",
      "nome": "Processos Judiciais"
    },
    {
      "id": "ATR_REGISTRO",
      "nome": "Registro de Imóveis"
    }
  ],
  "pageable": {
    "sort": {
      "sorted": true,
      "unsorted": false,
      "empty": false
    },
    "offset": 0,
    "pageSize": 10,
    "pageNumber": 0,
    "unpaged": false,
    "paged": true
  },
  "last": true,
  "totalPages": 1,
  "totalElements": 4,
  "size": 10,
  "number": 0,
  "sort": {
    "sorted": true,
    "unsorted": false,
    "empty": false
  },
  "numberOfElements": 4,
  "first": true,
  "empty": false
}
```

-   Status 200 (OK):

---

#### Consulta por ID 

**(GET**) http://localhost:9564/atribuicoes/{id}

- response Body

```json
{
  "id": "ATR_CERTIDOES",
  "nome": "Emissão de Certidões",
  "situacao": true
}
```

-   Status 200 (OK):

---

#### Inclusão de novo registro

**(POST)** http://localhost:9564/atribuicoes

- request Body

```json
{
  "id": "nova atribuicoes",
  "nome": "nova atribuicoes",
  "situacao": true
}
```

-   Status 201 (Created)

---

#### Alteração de registro por ID

**(PUT)** http://localhost:9564/atribuicoes/{id}

- request Body

```json
{
  "id": "nova atribuicoes",
  "nome": "nova atribuicoes",
  "situacao": true
}

```

-   Status 200 (OK):

---

#### Exclusão de registro por ID

**(DELETE)** http://localhost:9564/atribuicoes/{id}

- response Body

```json

```

-   Status 204 (No Content)

---

## Cartorios
#### Listagem paginada

**(GET)** http://localhost:9564/cartorios

-   Paginação:

    -   `page`: Número indicando qual a paginação. São retornados, no máximo, 10 resultados por página.
        `?page=2` => Pula os **primeiros 10**

- response Body

```json
{
    "content": [
        {
            "id": 1,
            "nome": "Cartório Central"
        },
        {
            "id": 2,
            "nome": "Cartório Novo Sol"
        }
    ],
    "pageable": {
        "sort": {
            "sorted": true,
            "unsorted": false,
            "empty": false
        },
        "offset": 0,
        "pageSize": 10,
        "pageNumber": 0,
        "unpaged": false,
        "paged": true
    },
    "last": true,
    "totalPages": 1,
    "totalElements": 2,
    "size": 10,
    "number": 0,
    "sort": {
        "sorted": true,
        "unsorted": false,
        "empty": false
    },
    "numberOfElements": 2,
    "first": true,
    "empty": false
}
```

-   Status 200 (OK):

---

#### Consulta por ID

**(GET**) http://localhost:9564/cartorios/{id}

- response Body

```json
{
    "id": 1,
    "nome": "Cartório Central",
    "observacao": "Oferece serviços de registro, notarização e emissão de certidões.",
    "situacao": {
        "id": "SIT_ATIVO",
        "nome": "Ativo"
    },
    "atribuicoes": [
        {
            "id": "ATR_REGISTRO",
            "nome": "Registro de Imóveis",
            "situacao": true
        },
        {
            "id": "ATR_NOTARIA",
            "nome": "Notarização de Documentos",
            "situacao": true
        },
        {
            "id": "ATR_CERTIDOES",
            "nome": "Emissão de Certidões",
            "situacao": true
        },
        {
            "id": "ATR_PROCESSOS",
            "nome": "Processos Judiciais",
            "situacao": true
        }
    ]
}
```

-   Status 200 (OK):

---

#### Inclusão de novo registro

**(POST)** http://localhost:9564/cartorios

- request Body

```json
{
    "nome": "Cartório new",
    "observacao": "Oferece serviços de registro, notarização e emissão de certidões.",
    "situacao": {
        "id": "SIT_ATIVO"
    },
    "atribuicoes": [
        {
            "id": "ATR_REGISTRO"
        },
        {
            "id": "ATR_NOTARIA"
        },
        {
            "id": "ATR_CERTIDOES"
        },
        {
            "id": "ATR_PROCESSOS"
        }
    ]
}
```

-   Status 201 (Created)

---

#### Alteração de registro por ID

**(PUT)** http://localhost:9564/cartorios/{id}

- request Body

```json
{
    "nome": "Cartório NEW PUT",
    "observacao": "Oferece serviços de registro, notarização e emissão de certidões.",
    "situacao": {
        "id": "SIT_ATIVO"
    },
    "atribuicoes": [
        {
            "id": "ATR_REGISTRO"
        },
        {
            "id": "ATR_NOTARIA"
        }
    ]
}
```

-   Status 200 (OK):

---

#### Exclusão de registro por ID

**(DELETE)** http://localhost:9564/cartorios/{id}

- response Body

```json

```

-   Status 204 (No Content)

---

<br> 

## Situacaos
#### Listagem paginada

**(GET)** http://localhost:9564/situacaos

-   Paginação:

    -   `page`: Número indicando qual a paginação. São retornados, no máximo, 10 resultados por página.
        `?page=2` => Pula os **primeiros 10**

- response Body

```json
{
    "content": [
        {
            "id": "SIT_ATIVO",
            "nome": "Ativo"
        },
        {
            "id": "SIT_BLOQUEADO",
            "nome": "Bloqueado"
        }
    ],
    "pageable": {
        "sort": {
            "sorted": true,
            "unsorted": false,
            "empty": false
        },
        "offset": 0,
        "pageSize": 10,
        "pageNumber": 0,
        "unpaged": false,
        "paged": true
    },
    "last": true,
    "totalPages": 1,
    "totalElements": 2,
    "size": 10,
    "number": 0,
    "sort": {
        "sorted": true,
        "unsorted": false,
        "empty": false
    },
    "numberOfElements": 2,
    "first": true,
    "empty": false
}
```

-   Status 200 (OK):

---

#### Consulta por ID

**(GET**) http://localhost:9564/situacaos/{id}

- response Body

```json
{
    "id": "SIT_ATIVO",
    "nome": "Ativo"
}
```

-   Status 200 (OK):

---

#### Inclusão de novo registro

**(POST)** http://localhost:9564/situacaos

- request Body

```json
{
    "id": "SIT_VAZIO",
    "nome": "vazio"
}
```

-   Status 201 (Created)

---

#### Alteração de registro por ID

**(PUT)** http://localhost:9564/situacaos/{id}

- request Body

```json
{
    "id": "SIT_ATIVO",
    "nome": "novo Ativo"
}
```

-   Status 200 (OK):

---

#### Exclusão de registro por ID

**(DELETE)** http://localhost:9564/situacaos/{id}

- response Body

```json

```

-   Status 204 (No Content)

---

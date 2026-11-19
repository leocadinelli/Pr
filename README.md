# 📍 API de Localidades — Municípios do Brasil (IBGE)

Documentação técnica para consumo do endpoint público de **Municípios** da API de Serviços de Dados do Instituto Brasileiro de Geografia e Estatística (IBGE).

---

## 🔗 Endpoint Principal

```http
GET https://servicodados.ibge.gov.br/api/v1/localidades/municipios
```

* **Autenticação:** Não requer chave de API (*API Key*), token ou cadastro.
* **Formato de Resposta:** `application/json` (UTF-8)
* **Retorno:** Lista completa contendo todos os municípios brasileiros e suas divisões geográficas oficiais.

---

## ⚙️ Parâmetros de Consulta (*Query Parameters*)

Os parâmetros são opcionais e podem ser utilizados de forma isolada ou combinada na URL:

| Parâmetro | Tipo | Obrigatório | Valores Aceitos | Descrição |
| :--- | :--- | :--- | :--- | :--- |
| `orderBy` | `string` | Não | `nome` | Por padrão, os municípios são ordenados pela propriedade `id` (identificador numérico). Ao utilizar `orderBy=nome`, os resultados passam a ser ordenados alfabeticamente pelo nome do município. |
| `view` | `string` | Não | `nivelado` | Define o modo de visualização do JSON. Por padrão, reflete a hierarquia aninhada das localidades. Com `view=nivelado`, todas as propriedades são renderizadas no mesmo nível (estrutura plana), ideal para exportação em tabelas e CSV. |

---

## 🚀 Requisições

### 1. Consulta padrão (ordenada por `id` e hierárquica)
```http
GET https://servicodados.ibge.gov.br/api/v1/localidades/municipios
```
Retorna os municípios a partir do menor código IBGE (ex.: `1100015 - Alta Floresta D'Oeste`) com objetos aninhados.

## 📦 Respostas da API

### Status `200 OK` — Um array de municípios

#### Schema (Estrutura Padrão)
```json
[
  {
    "id": "number — Identificador do município",
    "nome": "string — Nome do município",
    "microrregiao": {
      "id": "number — Identificador da microrregião",
      "nome": "string — Nome da microrregião",
      "mesorregiao": {
        "id": "number — Identificador da mesorregião",
        "nome": "string — Nome da mesorregião",
        "UF": {
          "id": "number — Identificador da UF",
          "sigla": "string — Sigla da UF",
          "nome": "string — Nome da UF",
          "regiao": {
            "id": "number — Identificador da grande região",
            "sigla": "string — Sigla da grande região",
            "nome": "string — Nome da grande região"
          }
        }
      }
    },
    "regiao-imediata": {
      "id": "number — Identificador da região imediata",
      "nome": "string — Nome da região imediata",
      "regiao-intermediaria": {
        "id": "number — Identificador da região intermediária",
        "nome": "string — Nome da região intermediária",
        "UF": {
          "id": "number",
          "sigla": "string",
          "nome": "string",
          "regiao": {
            "id": "number",
            "sigla": "string",
            "nome": "string"
          }
        }
      }
    }
  }
]
```



## 💻 Exemplo de Uso em Python

```python
import requests

URL = "https://servicodados.ibge.gov.br/api/v1/localidades/municipios"
PARAMETROS = {
    "orderBy": "nome",
    "view": "nivelado"
}

response = requests.get(URL, params=PARAMETROS, timeout=15)
response.raise_for_status()

municipios = response.json()
print(f"Total de municípios encontrados: {len(municipios)}")
print(f"Primeiro município: {municipios[0]['municipio-nome']} - {municipios[0]['UF-sigla']}")
```


## 2. Base de Dados Aberta — Estabelecimentos CNES (DATASUS / OpenDataSUS)

### 🔗 URL do Recurso (Download Direto S3)

```http
GET https://s3.sa-east-1.amazonaws.com/ckan.saude.gov.br/CNES/cnes_estabelecimentos_json.zip
```

* **Fonte Oficial:** Cadastro Nacional de Estabelecimentos de Saúde (CNES) — Portal de Dados Abertos do SUS (Ministério da Saúde).
* **Autenticação:** Não requer chave de API (*API Key*), token ou cadastro (acesso público via AWS S3).
* **Formato de Entrega:** Arquivo compactado `.zip` contendo a base completa em formato `.json` (UTF-8).
* **Frequência de Atualização:** Atualizado periodicamente pelo Ministério da Saúde.
* **Parâmetros de Consulta:** Não aceita *query parameters* (trata-se de um arquivo estático compactado para extração em lote/ETL).

### 🗂️ Principais Campos do JSON (Dicionário Resumido)

Cada objeto dentro do arquivo JSON extraído representa um estabelecimento de saúde cadastrado no Brasil (público, privado ou conveniado):

| Campo | Tipo | Descrição |
| :--- | :--- | :--- |
| `CO_CNES` | `string` / `number` | Código nacional único de 7 dígitos do estabelecimento no CNES. |
| `CO_UNIDADE` | `string` | Código identificador interno da unidade (concatenação do código do município + CNES). |
| `NO_RAZAO_SOCIAL` | `string` | Razão social oficial do estabelecimento ou mantenedora. |
| `NO_FANTASIA` | `string` | Nome fantasia da unidade de saúde. |
| `NU_CNPJ` / `NU_CNPJ_MANTENEDORA` | `string` | CNPJ do estabelecimento ou de sua entidade mantenedora. |
| `CO_MUNICIPIO_GESTOR` | `string` / `number` | Código IBGE de **6 dígitos** (sem o dígito verificador) do município gestor. |
| `CO_ESTADO_GESTOR` | `string` / `number` | Código IBGE de 2 dígitos da Unidade Federativa (UF). |
| `NO_LOGRADOURO` / `NU_ENDERECO` | `string` | Endereço físico e número do estabelecimento. |
| `NO_BAIRRO` / `CO_CEP` | `string` | Bairro e Código de Endereçamento Postal (CEP). |
| `NU_LATITUDE` / `NU_LONGITUDE` | `string` / `number` | Coordenadas geográficas de geolocalização da unidade. |
| `TP_UNIDADE` / `CO_TIPO_ESTABELECIMENTO` | `string` | Código do tipo de unidade/estabelecimento (ex.: UBS, Hospital Geral, Clínica). |
| `TP_GESTAO` | `string` | Tipo de gestão (`M` = Municipal, `E` = Estadual, `D` = Dupla, `S` = Sem gestão). |
| `DT_ATUALIZACAO` | `string` | Data da última atualização cadastral no SCNES. |
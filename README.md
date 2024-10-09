cat <<EOF > README.md
# Weather API Project

## Descrição

Este projeto consiste em uma API RESTful desenvolvida com **FastAPI** que extrai dados climáticos da **WeatherAPI.com**, armazena esses dados em um banco de dados **PostgreSQL** e fornece endpoints para consultar esses dados. A aplicação é conteinerizada com **Docker** para facilitar a implantação e inclui testes automatizados com **pytest**.

## Tecnologias Utilizadas

- **Linguagem:** Python 3.12
- **Framework:** FastAPI
- **Banco de Dados:** PostgreSQL
- **ORM:** SQLAlchemy
- **Autenticação de API:** WeatherAPI.com
- **Conteinerização:** Docker, Docker Compose
- **Testes:** pytest, httpx
- **CI/CD:** GitHub Actions
- **Versionamento:** Git, GitHub

## Configuração e Execução

### Pré-requisitos

- **Docker** e **Docker Compose** instalados
- Conta no [WeatherAPI.com](https://www.weatherapi.com/) para obter a chave de API

### Passo a Passo

1. **Clonar o Repositório:**

    ```bash
    git clone https://github.com/seu_usuario/weather_api_project.git
    cd weather_api_project
    ```

2. **Configurar as Variáveis de Ambiente:**

    Crie um arquivo `.env` na raiz do projeto com o seguinte conteúdo:

    ```env
    DATABASE_URL=postgresql://aleserra:sua_senha_segura@db:5432/api_projeto
    WEATHERAPI_KEY=292c5f7764e04ceda70201000240910
    ```

    **⚠️ Atenção:** Nunca compartilhe seu arquivo `.env` publicamente. Ele está incluído no `.gitignore` para proteger suas informações sensíveis.

3. **Rodar a Aplicação com Docker Compose:**

    ```bash
    docker-compose up --build
    ```

    Isso iniciará os serviços **PostgreSQL** e a **API**.

4. **Executar o Script de Extração:**

    Em um novo terminal, execute:

    ```bash
    docker exec -it meu_projeto_api-web-1 python data_extractor/extractor.py
    ```

    **Substitua** `meu_projeto_api-web-1` pelo nome real do contêiner `web` (encontrado com `docker ps`).

5. **Executar os Testes Automatizados:**

    ```bash
    docker exec -it meu_projeto_api-web-1 pytest
    ```

6. **Acessar a API:**

    - **API:** [http://localhost:8000](http://localhost:8000)
    - **Documentação Interativa (Swagger):** [http://localhost:8000/docs](http://localhost:8000/docs)

## Endpoints da API

### Weather

- **GET /weather/**: Lista todos os registros climáticos.
- **GET /weather/{weather_id}**: Detalhes de um registro específico.
- **GET /weather/city/{city_name}**: Lista todos os registros climáticos para uma cidade específica.

## Exemplos de Requisições e Respostas

### Obter Dados Climáticos de uma Cidade

**Requisição:**

```http
GET /weather/city/São Paulo HTTP/1.1
Host: localhost:8000

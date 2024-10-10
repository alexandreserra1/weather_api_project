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
- Conta no [GitHub](https://github.com/) para hospedar o repositório

### Passo a Passo

1. **Clonar o Repositório:**

    ```bash
    git clone https://github.com/alexandreserra1/weather_api_project.git
    cd weather_api_project
    ```

2. **Configurar as Variáveis de Ambiente:**

    Crie um arquivo `.env` na raiz do projeto com o seguinte 
    **Atenção:** Nunca compartilhe seu arquivo `.env` publicamente. Ele está incluído no `.gitignore` para proteger suas informações sensíveis.

3. **Criar o Arquivo `.gitignore`:**

    Certifique-se de que seu arquivo `.gitignore` contenha as seguintes entradas para proteger arquivos sensíveis e desnecessários:

    ```gitignore
    # Python
    __pycache__/
    *.py[cod]
    *$py.class

    # Ambientes Virtuais
    venv/
    .env
    env/
    ENV/
    env.bak/
    venv.bak/

    # Docker
    # Remova as linhas abaixo se Dockerfile e docker-compose.yml NÃO contiverem informações sensíveis
    Dockerfile
    docker-compose.yml
    docker-compose.override.yml

    # Logs
    *.log

    # Testes
    .cache
    .pytest_cache/
    .coverage
    coverage.xml

    # Migrações
    alembic.ini
    alembic/

    # IDEs
    .vscode/
    .idea/
    *.sublime-project
    *.sublime-workspace

    # OS
    .DS_Store
    Thumbs.db

    # Secrets
    *.env
    ```

    **⚠️ Importante:**
    
    - **Dockerfiles e docker-compose.yml:**
      - **Se** contiverem informações sensíveis (como senhas ou tokens), **mantenha-os no `.gitignore`**.
      - **Se não** contiverem informações sensíveis, **remova** as linhas correspondentes do `.gitignore` para que esses arquivos sejam versionados corretamente.
    
    - **Arquivos Sensíveis:**
      - **Nunca** compartilhe arquivos `.env` publicamente. Eles já estão protegidos pelo `.gitignore`.

4. **Rodar a Aplicação com Docker Compose:**

    Inicie os serviços **PostgreSQL** e a **API** com o seguinte comando:

    ```bash
    docker-compose up --build
    ```

    Isso iniciará os contêineres necessários. A API estará acessível em [http://localhost:8000](http://localhost:8000).

5. **Executar o Script de Extração:**

    Em um novo terminal, execute o script que extrai os dados climáticos:

    ```bash
    docker exec -it meu_projeto_api-web-1 python data_extractor/extractor.py
    ```

    **Substitua** `meu_projeto_api-web-1` pelo nome real do contêiner `web` (encontrado com `docker ps`).

6. **Executar os Testes Automatizados:**

    Execute os testes automatizados com o seguinte comando:

    ```bash
    docker exec -it meu_projeto_api-web-1 pytest
    ```

7. **Acessar a API:**

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
```
### Comandos para Verificação

    **Conectar-se ao Banco de Dados para Verificar os Dados:**


**docker exec -it meu_projeto_api-db-1 psql -U aleserra -d api_projeto**

Dentro do psql:
```http
SELECT * FROM weather LIMIT 5;
\q
```
**Iniciar o Servidor da API Localmente (Se Necessário):**


```http
uvicorn app.main:app --reload
```
Ou, via Docker:


```http
docker-compose up --build
```

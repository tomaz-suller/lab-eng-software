# Monitoramento de Aviões
Repositório para projeto Django desenvolvido durante Laboratório de Engenharia de Software (PCS3643)

## Informações do Grupo

| Nome                  | NUSP      |
|-----------------------|-----------|
| Eric Oliveira Gomes   | 11806642  |
| João Pedro Aras       | 11803545  |
| Tomaz Maia Suller     | 11803649  |

Grupo 2


## Instalação
As seguintes instruções foram pensadas para sistemas Windows.
É necessário ter configurado um ambiente previamente com Python>=3.6 e Git.
Em seguida:
    
1. Clonar o repositório
    ```
    git clone https://github.com/tomaz-suller/lab-eng-software.git
    ```
2. Criar ambiente virtual com venv
    ```
    python -m venv env
    ```
3. Ativar o ambiente virtual
    ```
    .\env\bin\activate # Ou .\env\scripts\activate
    ```
4. Instalar os requisitos de Python em `requirements/production.txt`
    ```
    pip install -r requirements/production.txt
    ```

## Uso
É necessário iniciar o servidor para então acessar a página.
1. Realizar migração do banco de dados
```
python manage.py migrate
```
2. Iniciar o servidor Django
```
python manage.py runserver
```
3. Acessar a página [`localhost:8000/FIRST`](http://localhost:8000/FIRST).

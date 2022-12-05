# Monitoramento de Aviões
Repositório para projeto Django desenvolvido durante Laboratório de Engenharia de Software (PCS3643)

## Informações do Grupo

| Nome                  | NUSP      |
|-----------------------|-----------|
| Eric Oliveira Gomes   | 11806642  |
| João Pedro Aras       | 11803545  |
| Tomaz Maia Suller     | 11803649  |

Grupo 2

## Uso

### Instalação
É necessário ter configurado um ambiente previamente com Python>=3.9 e Git.
Em seguida:

1. Clonar o repositório
    ```
    git clone https://github.com/tomaz-suller/lab-eng-software.git
    ```
2. Criar ambiente virtual com venv
    ```
    python -m venv env
    ```
3. Ativar o ambiente virtual.

    * Em sistemas Windows:
        ```
        .\env\bin\activate # Ou .\env\scripts\activate
        ```

    * Em sistmas UNIX-like (como macOS ou Linux):
        ```bash
        source env/bin/activate
        ```

4. Instalar os requisitos de Python em `requirements/production.txt`
    ```
    pip install -r requirements/production.txt
    ```

### Inicialização do Banco de Dados
Antes de executar a aplicação, é necessário realizar a configuração do banco de dados realizando _migrations_:
```
python manage.py migrate
```

Dumps do banco de dados estão disponívels no repositório para fornecer dados padrão e facilitar testes de navegação.
Existem dois dumps que podem ser carregados:
* `db_min.json`, que contém usuários e grupos com permissões pré-definidas mas não contém nenhum registro no sistema de monitoração de voos;
* `db.json`, que contém usuários e grupos, e registros padrão de voos.
Um dump pode ser carregado usando o comando `loaddata`. Por exemplo, para carregar `db.json`, é necessário executar:
```
python manage.py loaddata db.json
```

### Acesso ao sistema

Com os dados importados, é necessário iniciar o servidor:
```
python manage.py runserver
```

Em seguida, na página raiz (acessível em geral por `localhost:8000` ou `127.0.0.1:8000`) selecione o item "Login".
Nessa opção, pode-se autenticar com os usuários:

| Usuário           | Senha                 | Permissões                            |
|-------------------|-----------------------|---------------------------------------|
| `piloto`          | `senha-do-piloto`     | Movimentações e alguns itens do CRUD  |
| `gerente`         | `senha-do-gerente`    | Movimentações, relatórios e CRUD      |
| `operador`        | `senha-do-operador`   | CRUD                                  |
| `torre`           | `senha-da-torre`      | Movimentações                         |
| `funcionario`     | `senha-do-func`       | Movimentações                         |

Além desses usuários, existe o super-usuário de administração do sistema, que tem acesso a todas as suas funcionalidades. Seu usuário é `admin` e senha, `admin`.

De acordo com o usuário autenticado, as opções disponíveis mudam no menu principal.

#### Desbloqueio após senha incorretas

Após 3 tentativas incorretas de login, o acesso ao sistema é bloqueado. Para desbloqueá-lo é necessário parar o servidor em execução e executar o comando
```
python manage.py axes_reset
```
Em seguida, é possível reiniciar o servidor e continuar a usar o serviço.



## Desenvolvimento
Existem requisitos de Python adicionais para desenvolvimento, que devem ser instaldos de `requirements/development.txt`:
```
pip install -r requirements/development.txt
```

Além disso, este projeto usa [`pre-commit`](https://pre-commit.com/) para executar ferramentas de controle de qualidade, que deve ser habilitado após sua instalação:
```
pre-commit install
```

É recomendado ainda configurar o seu editor de texto para realizar lint dos arquivos usando `flake8` automaticamente. Para o Visual Studio Code, instruções estão disponíveis na [documentação](https://code.visualstudio.com/docs/python/linting#_flake8).

### Modificação nos modelos
A cada modificação nos arquivos de especificação, é necessário gerar movas _migrations_:
```
python manage.py makemigrations
```

### Testes
Testes são executados automaticamente a cada commit na branch `main` por integração contínua via GitHub Actions.
Eles também podem ser executados localmente:
```
python manage.py test
```

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
3. Ativar o ambiente virtual.

    * Em sistemas Windows:
        ```
        .\env\bin\activate # Ou .\env\scripts\activate
        ```

    * Em sistmas UNIX-like (como macOS ou Linux):
        ```bash
        source venv/bin/activate
        ```

4. Instalar os requisitos de Python em `requirements/production.txt`
    ```
    pip install -r requirements/production.txt
    ```

### Inicialização
Antes de executar a aplicação, é necessário realizar a configuração do banco de dados realizando _migrations_:
```
python manage.py migrate
``` 

### Teste de navegação
Inicialmente, é necessário carregar o dump disponível no repositório para carregar os usuários de teste:
```
python manage.py loaddata db.json
```

Para realizar o teste de navegação, a página raíz (index) deve ser acessada após iniciar o servidor com:
```
python manage.py runserver
```

Em seguida selecione o item "Login". Nessa opção, pode-se autenticar com os usuários:
- Usuário: **piloto**. Senha: **senha-do-piloto**. Tem acesso apenas a movimentações e alguns itens do CRUD.
- Usuário: **gerente**. Senha: **senha-do-gerente**. Tem acesso a alguns itens do CRUD, movimentações e relatórios.
- Usuário: **admin**. Senha: **admin**. Super-usuário de administração do sistema, tem acesso a todas as funcionalidades do sistema.

De acordo com o usuário autenticado, as opções disponíveis mudam no menu principal.

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

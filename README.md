<h1 align="center">Checknews - Plataforma de detecção de fake news - TCC da pós de desenvolvimento web</h1>

[![Python Version][python-image]][python-url]


## Orientações
1. Gere um ambiente virtual e baixe as dependências do projeto: `pip3.8 install -r requirements.txt` _Em caso de dúvidas, consulte este [artigo sobre ambiente virtual][ambiente-url]._
2. No terminal execute: `cd checknews_frontend`
3. Para executar o projeto: `python3.8 manage.py runserver`
4. Para aplicar as alterações do seu modelo: `python3.8 manage.py makemigrations` e, em seguida `python3.8 manage.py migrate`
5. Testes no shell django: `python3.8 manage.py shell` 


# Testes

Para executar os testes, execute: `python3.8 manage.py test`

[ambiente-url]: https://tutorial.djangogirls.org/pt/django_installation/
[python-url]: https://www.python.org/downloads/release/python-3810/
[python-image]: https://img.shields.io/badge/python-v3.8.10-blue

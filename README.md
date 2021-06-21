# desafio-serasa
Repositório para o desafio de programação para a vaga no programa de formação Serasa - Proway

Pré-requisito: Ter o python instalado (vesrões 3.7+) no computador, link para download: https://www.python.org

Para checar a versão do python, digite na linha de comando:

```python --version```

## Como rodar o programa
### Windows:

Instalar a biblioteca virtualenv:

```pip install virtualenv```

Enquanto estiver dentro do diretório desafio-serasa, crie um ambiente virtual:

```py -3 -m venv venv```

Após a criação do ambiente, ative-o:

```venv\Scripts\activate```

Após a ativação, o prompt de comando deve mostrar, à esquerda da linha de comando, o seguinte: ```(venv) ```

Se o ambiente estiver propriamente inicializado, instale os requerimentos para o sistema

```pip install -r requirements.txt```

Por fim, comece a rodar a aplicação:

```python run.py```

Para desativar o ambiente virtual, digite o seguinte comando:

```deactivate```

Para acessar o site da aplicação, você deve copiar o link que for mostrado no CMD.

### Linux/macOS:

Instalar a biblioteca virtualenv:

```pip install virtualenv```

Enquanto estiver dentro do diretório desafio-serasa, crie um ambiente virtual:

```python3 -m venv venv```

Após a criação do ambiente, ative-o:

```. venv/bin/activate```

Após a ativação, o prompt de comando deve mostrar, à esquerda da linha de comando, o seguinte: ```(venv) ```

Se o ambiente estiver propriamente inicializado, instale os requerimentos para o sistema

```pip install -r requirements.txt```

Por fim, comece a rodar a aplicação:

```python run.py```

Para desativar o ambiente virtual, digite o seguinte comando:

```deactivate```

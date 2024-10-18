# Informações do Aluno

**Aluno:** Adriano Madureira dos Santos
**Matrícula:** 202400480018

# Dependências do Projeto

Python Versão 3.8 ou mais atual instalada no sistema. A versão pode ser verificada por meio de:
```bash
python --version
```
Para clonar este repositório do Github, utilize:

```bash
git clone https://github.com/Adrianomadureira1/pta
```

Todas os pacotes e dependências de projeto utilizadas para desenvolver estão informadas no arquivo **requirements.txt** na pasta raiz do repositório. Caso tenha preferência por ambiente virtual (não obrigatório), este pode ser construído por meio de:

```bash
python -m venv venv
source venv/bin/activate  # Para Linux
venv\Scripts\activate  # Para Windows
```

As dependências do projeto podem ser instaladas a partir da raiz do projeto por meio de:

```bash
pip install -r requirements.txt
```

# Execução do PTA

Primeiramente, inicie o processo servidor por meio do seguinte comando na pasta raiz do repositório: 
```bash
python pta-server/pta-server.py
```
O processo cliente de código fornecido pode ser executado pelo seguinte comando na pasta raiz:

```bash
python pta-client.py 127.0.0.1 11550 user1
```

Com o servidor em estado de operação e o Pytest instalado no ambiente virtual, é possível executar todos os testes elaborados para o PTA por meio do comando abaixo na pasta raiz:
```bash
pytest -vv
```
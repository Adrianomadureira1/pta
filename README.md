# Estrutura do Projeto

- ./pta-client.py: Refere-se a implementação do socket cliente.
- ./pta-server/pta-server.py: Refere-se a implementação do socket servidor.

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

Execute o processo servidor por meio do comando: 
```bash
python pta-server/pta-server.py
```
Execute o processo cliente por meio do comando:

```bash
python pta-client.py
```
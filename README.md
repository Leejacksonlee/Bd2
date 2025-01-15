Este projeto permite realizar recomendações de filmes com base em sinopses fornecidas pelo usuário, utilizando a tecnologia de embeddings e o banco de dados vetorial Qdrant. O modelo transforma sinopses em embeddings vetoriais, armazena esses embeddings no Qdrant e permite que o usuário faça consultas para obter filmes relacionados a partir de uma sinopse.

## Requisitos

Este projeto requer algumas bibliotecas e ferramentas para funcionar corretamente. Você precisará de:

1. **Qdrant**: Banco de dados vetorial para armazenamento e busca de embeddings.
2. **Sentence Transformers**: Biblioteca para transformar sinopses em embeddings vetoriais.
3. **Ollama**: Utilizado para interagir com um modelo de chat que recomenda filmes.

### Dependências no `requirements.txt`

- `sentence-transformers==3.3.1`
- `qdrant-client==1.12.2`
- `ollama==0.4.4`
- `numpy==2.2.0`

## Passos para Rodar o Projeto

### 1. Preparar o Ambiente

Antes de rodar o projeto, você precisa garantir que tem o ambiente configurado corretamente.

#### 1.1 Instalar Docker

Certifique-se de ter o Docker instalado e rodando na sua máquina. Caso não tenha o Docker, baixe e instale-o [aqui](https://www.docker.com/get-started).

#### 1.2 Rodar o Qdrant

Execute o comando a seguir no terminal para iniciar o container do Qdrant (certifique-se de que o Docker está rodando):

```bash
docker run -p 6333:6333 -p 6334:6334 -v /qdrant_storage:/qdrant/storage:z qdrant/qdrant
```

Isso irá rodar o Qdrant no seu ambiente local, mapeando as portas 6333 e 6334 para permitir a comunicação com o banco de dados.

#### 1.3 Criar e Ativar um Ambiente Virtual (opcional, mas recomendado)

Você pode criar um ambiente virtual para gerenciar as dependências do projeto.

```bash
python -m venv venv
source venv/bin/activate  # Para Linux/macOS
venv\Scripts\activate  # Para Windows
```

#### 1.4 Instalar Dependências

Com o ambiente virtual ativado, instale as dependências necessárias:

```bash
pip install -r requirements.txt
```

### 2. Preparar os Arquivos de Dados

Certifique-se de que o arquivo `filmes.json` esteja presente no diretório do projeto. Este arquivo contém as informações sobre os filmes, como título, sinopse, gênero, diretor e nota. Um exemplo de como ele deve ser formatado está abaixo:

```json
[
    {
        "id": "1",
        "titulo": "A Origem",
        "sinopse": "Um ladrão que rouba segredos corporativos por meio da tecnologia de compartilhamento de sonhos recebe a tarefa inversa de plantar uma ideia na mente de um CEO.",
        "genero": ["Ação", "Ficção Científica", "Suspense"],
        "diretor": "Christopher Nolan",
        "nota": 8.8
    },
    ...
]
```

### 3. Rodar o Código

#### 3.1 Rodar o Script `data.py`

Este script vai preparar e carregar os dados dos filmes no Qdrant. Ele irá:

1. Conectar ao servidor Qdrant.
2. Criar uma coleção no Qdrant chamada `movies_collection`.
3. Gerar embeddings para as sinopses dos filmes usando o modelo `SentenceTransformer`.
4. Inserir os dados dos filmes na coleção.

Execute o script `data.py`:

```bash
python data.py
```

Isso irá carregar os filmes e suas sinopses no banco de dados Qdrant.

#### 3.2 Rodar o Script `main.py`

O script `main.py` será responsável por interagir com o usuário. Ele fará as seguintes ações:

1. Solicitar uma sinopse ou pergunta ao usuário.
2. Converter a entrada do usuário em um embedding de vetor.
3. Buscar no Qdrant os filmes mais semelhantes à sinopse fornecida.
4. Gerar um prompt que será enviado ao modelo de chat (Ollama) para recomendar o melhor filme com base nos resultados da busca.
5. Exibir a resposta do assistente com a recomendação.

Para rodar o `main.py`, execute:

```bash
python main.py
```

Digite uma sinopse de filme ou uma pergunta relacionada aos filmes. Por exemplo:

```
O que você gostaria de saber? (digite '/sair' para finalizar): Filme de ficção científica com ação e suspense.
```

O assistente irá então buscar filmes que correspondem a essa descrição e recomendar o melhor com base na sinopse.

### 4. Finalizando o Programa

Para sair do programa, basta digitar `exit` quando solicitado.

## Estrutura de Arquivos

A estrutura de arquivos do projeto deve ser semelhante a:

```
/seu-diretorio-do-projeto
├── data.py
├── main.py
├── filmes.json
├── requirements.txt
└── README.md
```

## Notas Finais

- Este projeto requer que o Qdrant esteja rodando localmente. Certifique-se de que o Docker esteja funcionando e o Qdrant esteja acessível na porta `6333`.
- O código está configurado para trabalhar com embeddings de 384 dimensões, utilizando o modelo `all-MiniLM-L6-v2` da biblioteca `sentence-transformers`.
- A interação com o modelo de chat (Ollama) depende de uma chave de API válida e do modelo `llama3.2`. Certifique-se de ter a configuração adequada para esse serviço.

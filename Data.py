import time
import json
from sentence_transformers import SentenceTransformer  # Para gerar embeddings das sinopses
from qdrant_client.models import Distance, VectorParams  # Para definir parâmetros do vetor
from qdrant_client.models import PointStruct  # Para estruturar os pontos de dados (filmes)
from qdrant_client import QdrantClient  # Para interagir com o banco de dados Qdrant

# Conexão com o cliente Qdrant, usando a URL do servidor local
client = QdrantClient(url="http://localhost:6333")

# Criação de uma coleção no Qdrant para armazenar os dados dos filmes
client.create_collection(
    collection_name="movies_collection",  # Nome da coleção
    vectors_config=VectorParams(size=384, distance=Distance.DOT),  # Configuração do vetor (dimensão e tipo de distância)
)

# Inicialização do modelo de transformação de sentença para gerar embeddings a partir das sinopses dos filmes
sentenceTransformer = SentenceTransformer('all-MiniLM-L6-v2')

# Carregamento dos dados de filmes a partir de um arquivo JSON
with open("filmes.json", "r", encoding="utf-8") as file:
    movies = json.load(file)  # Carrega o arquivo JSON que contém informações sobre os filmes

# Inicialização de uma lista para armazenar os pontos de dados que serão inseridos no Qdrant
points_movies = []

# Loop para processar cada filme e gerar o embedding a partir da sua sinopse
for idx, movie in enumerate(movies):
    sinopse = movie["sinopse"]  # Acessa a sinopse do filme
    embedding = sentenceTransformer.encode(sinopse)  # Gera o embedding da sinopse do filme
    points_movies.append(PointStruct(id=idx, vector=embedding, payload=movie))  # Cria um ponto no Qdrant com o ID, embedding e os dados do filme

# Inserção dos pontos de dados (filmes) na coleção do Qdrant
operation_info = client.upsert(
    collection_name="movies_collection",  # Nome da coleção onde os dados serão inseridos
    wait=True,  # Aguarda a operação ser concluída antes de prosseguir
    points=points_movies,  # Lista de pontos de dados (filmes com embeddings)
)

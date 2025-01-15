from ollama import chat  # Para interagir com o modelo de chat
from ollama import ChatResponse  # Para lidar com a resposta do modelo de chat
from sentence_transformers import SentenceTransformer  # Para gerar embeddings a partir de texto
from qdrant_client import QdrantClient  # Para interagir com o banco de dados Qdrant

# Conexão com o cliente Qdrant, utilizando a URL do servidor local
cliente = QdrantClient(url="http://localhost:6333")

# Inicialização do modelo de transformação de sentença para gerar embeddings a partir de texto
sentenceTransformer = SentenceTransformer("all-MiniLM-L6-v2")

# Loop contínuo para interação com o usuário
while True:
    # Solicita ao usuário uma pergunta ou sinopse para procurar filmes relacionados
    texto = input("Qual filme você quer assistir? (digite '/exit' para finalizar): ")
    
    # Condicional para sair do loop quando o usuário digitar 'exit'
    if texto.lower() == 'exit':
        print("Fim do programa.")
        break
        
    # Realiza uma busca no banco de dados Qdrant utilizando o texto fornecido pelo usuário
    hits = cliente.search(
        collection_name="movies_collection",  # Nome da coleção onde os dados de filmes estão armazenados
        query_vector=sentenceTransformer.encode(texto).tolist(),  # Converte o texto do usuário em um vetor de embedding
        limit=3  # Limita o número de resultados retornados para 3 filmes
    )
    
    # Criação do prompt para enviar ao assistente de chat com base na sinopse fornecida
    prompt = "Você é um assistente que ajuda a encontrar filmes com base em uma sinopse. O usuário forneceu a seguinte descrição:\n"
    prompt += f"\n**Sinopse fornecida:** {texto}\n"
    prompt += "\nAqui estão os filmes que podem corresponder a essa sinopse:\n"
        
    # Adiciona os filmes encontrados à resposta do prompt, incluindo informações como título, sinopse, gênero, diretor e nota
    for idx, hit in enumerate(hits):
        titulo = hit.payload["titulo"]  # Título do filme
        sinopse = hit.payload["sinopse"]  # Sinopse do filme
        genero = hit.payload["genero"]  # Gênero do filme
        diretor = hit.payload["diretor"]  # Diretor do filme
        nota = hit.payload["nota"]  # Nota do filme
        
        # Formatação dos dados de cada filme para incluir no prompt
        prompt += f"\nFilme {idx}:\n"
        prompt += f"**Título:** {titulo}\n"
        prompt += f"**Sinopse do filme:** {sinopse}\n"
        prompt += f"**Gênero:** {genero}\n"
        prompt += f"**Diretor:** {diretor}\n"
        prompt += f"**Nota:** {nota}\n"
        
    # Adiciona a pergunta final ao prompt para o assistente: qual é a melhor recomendação com base nos filmes encontrados?
    prompt += "\nCom base nas informações acima, pode recomendar o melhor filme para o usuário? Responda de forma clara e útil."

    # Exibe o prompt gerado, que será enviado ao modelo de chat
    print(prompt)
    
    # Envia o prompt gerado para o modelo de chat, solicitando uma resposta com base nas informações fornecidas
    response: ChatResponse = chat(model='llama3.2', messages=[{'role': 'user', 'content': prompt}])
    
    # Exibe a resposta do assistente com a recomendação
    print(f"Resposta do assistente: {response.message.content}")

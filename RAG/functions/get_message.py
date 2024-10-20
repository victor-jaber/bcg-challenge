from configparser import ConfigParser
from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings

from functions.data_cleaning import cleaning_user_query
from functions.utils import database_connection, get_dir_config
from functions.embedding import embedding_func


def get_embeddings(text, model, openai_api_key):
    '''
    Function to transform a string into a vector of numbers
    '''
    embedding = OpenAIEmbeddings(model=model,
                                openai_api_key = openai_api_key
                                )
    emb = embedding_func(embedding, text)
    return emb


def retrive_similar_docs(query_embedding, conn, limit=10):
    '''
    Retrieve similar documents based on user input.
    The search is done using cosine similarity
    '''
    cur = conn.cursor()
    query = f"""
        SELECT content, embedding <=> {query_embedding} as cos_sim FROM 
            (
            SELECT 
                content, embedding
            FROM
            silver.enfrentamento_nacional t1
            LEFT JOIN gold.enfrentamento_nacional t2 ON (t1.page_number = t2.page_number)

            UNION 

            SELECT 
                content, embedding
            FROM
            silver.plano_curitiba t1
            LEFT JOIN gold.plano_curitiba t2 ON (t1.page_number = t2.page_number)

            UNION 


            SELECT 
                content, embedding
            FROM
            silver.plano_agro t1
            LEFT JOIN gold.plano_agro t2 ON (t1.page_number = t2.page_number)

            UNION 

            SELECT 
                content, embedding
            FROM
            silver.plano_nacional t1
            LEFT JOIN gold.plano_nacional t2 ON (t1.page_number = t2.page_number)

            UNION 

            SELECT 
                content, embedding
            FROM
            silver.plano_sp t1
            LEFT JOIN gold.plano_sp t2 ON (t1.page_number = t2.page_number)

            UNION 

            SELECT 
                content, embedding
            FROM
            silver.plano_federal t1
            LEFT JOIN gold.plano_federal t2 ON (t1.page_number = t2.page_number)

            UNION 

            SELECT 
                content, embedding
            FROM
            silver.plano_itabirito t1
            LEFT JOIN gold.plano_itabirito t2 ON (t1.page_number = t2.page_number)

            UNION 

            SELECT 
                content, embedding
            FROM
            silver.plano_joao_pessoa t1
            LEFT JOIN gold.plano_joao_pessoa t2 ON (t1.page_number = t2.page_number)
            )
        ORDER BY (embedding <=> {query_embedding}) LIMIT {limit}
        """
    cur.execute(query)
    top_docs = cur.fetchall()
    return top_docs


def get_completion_from_messages(messages, openai_api_key):
    '''
    Model return from system message.
    '''
    llm = ChatOpenAI(model="gpt-4o-mini",
                     openai_api_key = openai_api_key,
                     max_tokens=8000,
                     temperature=0.6,
                     top_p=0.7)
    return llm.invoke(messages)


def process_input_with_retrieval(user_query, logger):
    '''
    Returns the model response to the user query
    '''
    # Connects to the database
    conn = database_connection("datalake.db")

    # Processing and cleaning data in the user query
    user_query = cleaning_user_query(user_query)
    logger.info('Processing and cleaning data from the user query completed successfully')
    
    # Get the parameters for the model
    ini_config = get_dir_config()
    config = ConfigParser()
    config.read(ini_config, encoding="utf8")

    openai_api_key =  config['EMBEDDING']['OPEN_API_KEY']
    model = config['EMBEDDING']['MODEL']

    # Transforms the user query into a vector
    emb = get_embeddings(user_query, model, openai_api_key)
    logger.info('Transformed the user query into a float vector')

    # Retrieve similar documents based on user input
    related_docs = retrive_similar_docs(emb, conn, limit=3)
    logger.info('Retrieved similar documents based on user input')

    # Ensure there are at least one document
    if len(related_docs) == 0:
        logger.info('No documents relevant to the question were found')
        return "Desculpe, não foram encontrados documentos relevantes para a sua pergunta"
    
    # Defines the system message and generates the model return
    system_message = f"""
        Você é um assistente de inteligência artificial desenhado para apoiar gestores municipais em uma ampla gama de atividades, desde responder simples perguntas até prover explicações profundas e discussões sobre como construir um plano de adaptação climática para um município.
        Você não deve em nenhuma circustância inventar coisas, e deve simplesmente dizer ao usuário que não sabe quando não souber.
        
        Você deve fornecer ações práticas para realizar o planejamento climático do munícipio solicitado, por ordem de prioridade em termos de facilidade de implementação e impacto.
        Justifique suas ações com base nos documentos apresentados abaixo do munícipio e outros documentos da sua base de dados.
        Sempre que possível, dê exemplos factuais das ações sugeridas que foram implementas em outras cidades.
        Documento 1: {related_docs[0]}
        Documento 2: {related_docs[1]}
        Documento 3: {related_docs[2]}
    """

    messages = [("system", system_message, ), ("human", user_query), ]

    final_response = get_completion_from_messages(messages, openai_api_key)
    
    # Handle empty responses
    if not final_response.content:
        logger.info('Could not generate a response')
        return "Desculpe, não foi possível gerar uma resposta. Por favor, tente novamente."
    
    logger.info('Final response generated successfully')
    return final_response.content

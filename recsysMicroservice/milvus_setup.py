from pymilvus import DataType, MilvusClient, connections, Collection
import pandas as pd
import os

def setup():

    posts_df = pd.read_parquet('./Notebooks/posts.parquet.gzip')

    posts_data = posts_df[['id', 'bert_descr_vector', 'tfidf_descr_vector', 'image_vector', 'tags_vector']]
    
    posts_data = posts_data.to_dict(orient='records')
    
    for post in posts_data:
        for vector_name in ['bert_descr_vector', 'tfidf_descr_vector', 'image_vector', 'tags_vector']:
            post[vector_name] = post[vector_name].tolist()

    milvus_host = os.getenv("MILVUS_HOST", "localhost")
    milvus_port = os.getenv("MILVUS_PORT", "19530")
    connections.connect(
        alias="default", 
        host=milvus_host,
        port=milvus_port
    )

    m_client = MilvusClient("http://{}:{}".format(milvus_host, milvus_port))

    if m_client.has_collection('post'):
        m_client.drop_collection('post')

    if m_client.has_collection('user'):
        m_client.drop_collection('user')


    post_schema = MilvusClient.create_schema(
        auto_id=False,
        enable_dynamic_field=False,
    )

    user_schema = MilvusClient.create_schema(
        auto_id=False,
        enable_dynamic_field=False,
    )

    post_schema.add_field(field_name="id", datatype=DataType.INT64, is_primary=True)

    user_schema.add_field(field_name="id", datatype=DataType.INT64, is_primary=True)
    user_schema.add_field(field_name="weight_count", datatype=DataType.INT64)

    for vector_name in ['bert_descr_vector', 'tfidf_descr_vector', 'image_vector', 'tags_vector']:
        post_schema.add_field(field_name=vector_name, datatype=DataType.FLOAT_VECTOR, dim=len(posts_data[0][vector_name]))
        user_schema.add_field(field_name=vector_name, datatype=DataType.FLOAT_VECTOR, dim=len(posts_data[0][vector_name]))
        


    user_index_params = m_client.prepare_index_params()
    post_index_params = m_client.prepare_index_params()

    for index_params in [user_index_params, post_index_params]:
        
        for vector_name in ['bert_descr_vector', 'tfidf_descr_vector', 'image_vector', 'tags_vector']:
            
            index_params.add_index(
                field_name="id",
                index_type="STL_SORT"
            )
            
            index_params.add_index(
                field_name=vector_name, 
                index_type="IVF_FLAT",
                metric_type="COSINE",
                params={ "nlist": 128 }
            )


    m_client.create_collection(
        collection_name="post",
        schema=post_schema,
        index_params=post_index_params
    )


    m_client.create_collection(
        collection_name="user",
        schema=user_schema,
        index_params=user_index_params
    )

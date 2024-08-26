from typing import List
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from qdrant_client import QdrantClient
from qdrant_client.http.models import FieldCondition, Filter, MatchValue
from sqlalchemy.ext.asyncio import AsyncSession
from db.models import DayCountry, Fragment
import countrydle.crud as ccrud
from .vectorize import get_embedding
from qdrant_client.http.exceptions import UnexpectedResponse


def split_document(content: str) -> List[Document]:
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, chunk_overlap=150, length_function=len
    )

    fragments = text_splitter.create_documents([content])
    return fragments


def get_points(client: QdrantClient, collection_name: str, ids: list[int]):
    try:
        # Try to get the point by its ID
        points = client.retrieve(collection_name=collection_name, ids=ids)
        return points
    except UnexpectedResponse:
        return []


def search_matches(
    client: QdrantClient,
    collection_name: str,
    query_vector: list,
    country_id: int = None,
    limit: int = 5,
):
    search_result = client.search(
        query_filter=Filter(
            must=[
                FieldCondition(
                    key="country_id",
                    match=MatchValue(
                        value=country_id,
                    ),
                )
            ]
        ),
        collection_name=collection_name,
        query_vector=query_vector,
        limit=limit,
    )

    return search_result


def get_fragments_matching_question(
    question: str, day: DayCountry, collection_name: str, session: AsyncSession
) -> list[Fragment]:
    query = question
    query_vector = get_embedding(query)

    points: list = search_matches(
        collection_name=collection_name,
        query_vector=query_vector,
        country_id=day.country_id,
    )
    points.sort(key=lambda x: int(x.id))

    fragments = []
    for point in points:
        fragment = ccrud.get_fragment(int(point.id), session)
        fragments.append(fragment)

    return fragments

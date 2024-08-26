import logging
import os
from pathlib import Path
from typing import List

import countrydle.crud as ccrud
from db.models import Country, Document, Fragment
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, PointStruct, VectorParams
from sqlalchemy.ext.asyncio import AsyncSession

from .utils import get_points

load_dotenv()

EMBEDDING_SIZE = int(os.getenv("EMBEDDING_SIZE"))
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL")

QDRANT_HOST = os.getenv("QDRANT_HOST")
QDRANT_PORT = int(os.getenv("QDRANT_PORT"))
COLLECTION_NAME = os.getenv("COLLECTION_NAME")

client: QdrantClient = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)


async def init_qdrant(session: AsyncSession):
    if client.collection_exists(COLLECTION_NAME):
        return

    snapshot_path = Path("/qdrant/snapshots/countries/countries-base.snapshot")
    if snapshot_path.exists():
        print("Loading QDRANT snapshot!")
        client.recover_snapshot(COLLECTION_NAME, location=snapshot_path)
        return

    client.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(size=EMBEDDING_SIZE, distance=Distance.COSINE),
    )

    await populate_qdrant(session)


async def populate_qdrant(session: AsyncSession):
    countries: List[Country] = await ccrud.get_all_countries(session)
    num_c = len(countries)
    for i, country in enumerate(countries):
        logging.info(f"Country {i+1}/{num_c}: {country.name}")
        doc: Document = await ccrud.get_doc_for_country(country.id, session)
        fragments: List[Fragment] = await ccrud.get_fragments(doc.id, session)
        ids = [fragment.id for fragment in fragments]
        points = []

        if len(get_points(client, COLLECTION_NAME, ids)) == len(ids):
            continue

        for fragment in fragments:

            embedding = fragment.embedding

            point = PointStruct(
                id=fragment.id,
                vector=embedding,
                payload={
                    "country_id": country.id,
                    "country_name": country.name,
                    "fragment_text": fragment.text,
                },
            )
            points.append(point)
        if points:
            client.upsert(collection_name=COLLECTION_NAME, points=points)


def get_qdrant_client():
    """Returns the initialized Qdrant client."""
    return client


def close_qdrant_client():
    """Closes the Qdrant client if it's open."""
    global client
    if client:
        client.close()

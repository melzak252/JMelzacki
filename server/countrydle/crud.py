import csv
import logging

import qdrant
import qdrant.utils as qutils
from db.models import Country, Document, Fragment
from db.repositories.country import CountryRepository
from sqlalchemy.ext.asyncio import AsyncSession


async def populate_countries(session: AsyncSession):
    c_rep = CountryRepository(session)
    countries = await c_rep.get_all_countries()

    if countries:
        return

    return
    with open("data/countries.csv", "r", encoding="utf8") as f:
        reader = csv.DictReader(f, fieldnames=["name", "official_name", "wiki_page"])
        next(reader)

        for i, row in enumerate(reader):
            fragments = []

            country = Country(
                name=row["name"],
                official_name=row["official_name"],
                wiki=row["wiki_page"],
                md_file=f"data/pages/{row['name']}.md",
            )

            logging.info(f"Country {i+1}: {country.name}")

            # Read the markdown content for the country
            with open(country.md_file, encoding="utf8") as md_file:
                md_content = md_file.read()

            doc = Document(country=country, content=md_content)

            doc_fragments = qutils.split_document(md_content)

            for fragment in doc_fragments:
                frag = Fragment(
                    document=doc,
                    text=fragment.page_content,
                    embedding=qutils.get_embedding(
                        fragment.page_content, qdrant.EMBEDDING_MODEL
                    ),
                )
                fragments.append(frag)

            print(
                f"Adding country {country.name}+document, and {len(fragments)} fragments to DB"
            )

            session.add(country)
            session.add(doc)
            session.add_all(fragments)

            try:
                await session.commit()  # Commit the transaction

            except Exception as ex:
                await session.rollback()
                raise ex
    try:
        await session.commit()  # Commit the transaction

    except Exception as ex:
        await session.rollback()
        raise ex

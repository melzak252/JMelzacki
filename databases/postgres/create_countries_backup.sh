pg_dump -U postgres -d guess_country -t countries -f countries_dump.sql
pg_dump -U postgres -d guess_country -t documents -f countries_dump_docs.sql
pg_dump -U postgres -d guess_country -t fragments -f countries_dump_frag.sql
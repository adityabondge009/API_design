from fastapi import FastAPI, Query
from sqlalchemy import create_engine, text
from typing import List, Optional
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Gutendex API is running"}

DATABASE_URL = "postgresql://postgres:1234a@localhost:5432/gutendex"

engine = create_engine(DATABASE_URL)
app = FastAPI(title="Gutenberg Books API")

PAGE_SIZE = 25

@app.get("/books")
def get_books(
    page: int = 1,
    ids: Optional[List[int]] = Query(None, alias="id"),
    language: Optional[List[str]] = None,
    mime: Optional[List[str]] = None,
    topic: Optional[List[str]] = None,
    author: Optional[List[str]] = None,
    title: Optional[List[str]] = None,
):
    filters = []
    params = {}

    if ids:
        filters.append("b.id = ANY(:ids)")
        params["ids"] = ids

    if language:
        filters.append("l.code = ANY(:langs)")
        params["langs"] = language

    if mime:
        filters.append("f.mime_type = ANY(:mimes)")
        params["mimes"] = mime

    if author:
        filters.append(
            "(" + " OR ".join([f"a.name ILIKE :author{i}" for i in range(len(author))]) + ")"
        )
        for i, a in enumerate(author):
            params[f"author{i}"] = f"%{a}%"

    if title:
        filters.append(
            "(" + " OR ".join([f"b.title ILIKE :title{i}" for i in range(len(title))]) + ")"
        )
        for i, t in enumerate(title):
            params[f"title{i}"] = f"%{t}%"

    if topic:
        topic_conditions = []
        for i, t in enumerate(topic):
            topic_conditions.append(f"(s.name ILIKE :topic{i} OR bs.name ILIKE :topic{i})")
            params[f"topic{i}"] = f"%{t}%"
        filters.append("(" + " OR ".join(topic_conditions) + ")")

    where_clause = " AND ".join(filters) if filters else "TRUE"

    query = text(f"""
        SELECT DISTINCT b.id, b.title, b.download_count AS downloads,
               a.name AS author,
               l.code AS language,
               array_agg(DISTINCT s.name) AS subjects,
               array_agg(DISTINCT bs.name) AS bookshelves,
               json_agg(json_build_object('mime', f.mime_type, 'url', f.url)) AS links
        FROM books_book b
        LEFT JOIN books_book_authors ba ON b.id = ba.book_id
        LEFT JOIN books_author a ON ba.author_id = a.id
        LEFT JOIN books_language l ON b.language_id = l.id
        LEFT JOIN books_book_subjects bsj ON b.id = bsj.book_id
        LEFT JOIN books_subject s ON bsj.subject_id = s.id
        LEFT JOIN books_book_bookshelves bb ON b.id = bb.book_id
        LEFT JOIN books_bookshelf bs ON bb.bookshelf_id = bs.id
        LEFT JOIN books_format f ON f.book_id = b.id
        WHERE {where_clause}
        GROUP BY b.id, a.name, l.code
        ORDER BY downloads DESC
        LIMIT :limit OFFSET :offset
    """)

    count_query = text(f"SELECT COUNT(*) FROM books_book b WHERE {where_clause}")

    params["limit"] = PAGE_SIZE
    params["offset"] = (page - 1) * PAGE_SIZE

    with engine.connect() as conn:
        result = conn.execute(query, params).mappings().all()
        total = conn.execute(count_query, params).scalar()

    return {
        "count": total,
        "page": page,
        "page_size": PAGE_SIZE,
        "results": [dict(r) for r in result]
    }


class GoogleBookApi:
    """Datos y metadatos necesarios para la interacción con el api de google books"""

    url = 'https://www.googleapis.com/books/v1/volumes?'
    """Url para hacer request al api"""

    google_atributos = {
        'titulo': 'intitle',
        'autor': 'inauthor',
        'catergorias': 'subject',
        'editor': 'inpublisher',
        'descripcion': 'q',
    }
    """Atributos que se pueden usar en la búsqueda"""

    atributos_book = [
        'id',
        'title',
        'authors',
        'publisher',
        'publishedDate',
        'description',
        'categories',
    ]
    """Atributos que se desean mostrar en el resultado"""

    rename_atributos = {
        "id": "id",
        "title": "titulo",
        "authors": "autor",
        "categories": "categorias",
        "publisher": "editor",
        "publishedDate": "fecha_publicacion",
        "description": "descripcion",
    }
    """Nombres por lo cuales se cambiaran los atributos originales."""

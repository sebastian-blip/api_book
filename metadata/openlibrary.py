class OpenLibraryApi:
    """Clase con los datos y metadatos para interactuar con el api de open"""

    open_atributos = {
        'titulo': 'title',
        'autor': 'author',
        'catergorias': 'subject',
        'editor': 'publisher',
        'descripcion': 'q',
        'fecha_publicacion': 'publish_date',
    }
    """Atributos que se pueden usar en la búsqueda"""

    atributos_book = [
        'key',
        'title',
        'publish_date',
        'publisher',
        'language',
        'author_name',
        'subject',
    ]
    """Atributos que se desean mostrar en el resultado"""

    url = (
        f'https://openlibrary.org/search.json?fields={",".join(atributos_book)}'
    )
    """Url para hacer request al api"""

    rename_atributos = {
        "key": "id",
        "title": "titulo",
        "author_name": "autor",
        "subject": "categorias",
        "publisher": "editor",
        "publish_date": "fecha_publicacion",
        "description": 'descripcion',
    }
    """Nombres por lo cuales se cambiaran los atributos originales."""

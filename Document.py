
class Document_Object():
    """
    This class is used to store documents by title, url and abstract
    """
    def __init__(self, id, url, text) -> None:
        self.id = id
        self.url = url
        self.text = text

    def __str__(self) -> str:
        return f'Doc-{self.id}:{{ URL: {self.url}\nText: {self.text} }}\n'
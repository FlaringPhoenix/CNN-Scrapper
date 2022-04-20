class Article:
    def __init__(self, id, headline, author, description):
        self.id = id;
        self.headline = headline
        self.author = author
        self.description = description

    def raw(self):
        return {
            "id": self.id,
            "headline": self.headline,
            "author": self.author,
            "description": self.description
        }
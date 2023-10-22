class UnknownError(Exception):
    def __init__(self, mensagem="Unknown error"):
        super().__init__(mensagem)

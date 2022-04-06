from http import HTTPStatus


class wrongKeysError(Exception):
    def __init__(self, allowed_keys, wrong_keys) -> None:
        self.message = {
            "available_keys": list(allowed_keys),
            "wrong_keys_sended": list(wrong_keys),
        }, HTTPStatus.UNPROCESSABLE_ENTITY


class missingKeysError(Exception):
    def __init__(self, allowed_keys, missing_keys) -> None:
        self.message = {
            "available_keys": list(allowed_keys),
            "wrong_keys_sended": list(missing_keys),
        }, HTTPStatus.UNPROCESSABLE_ENTITY


# class wrongKeysError(Exception):
#     def __init__(self) -> None:
#         self.message = {'error': 'The list is empty!'}
#         super().__init__(self.message)

# class missingKeysError(Exception):
#     def __init__(self, cpf) -> None:
#         self.message = {'error': f'CPF {cpf} already exists!'}
#         super().__init__(self.message)

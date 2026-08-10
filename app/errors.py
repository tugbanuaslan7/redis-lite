class RedisLiteError(Exception):

    def __init__(self, code, message):
        super().__init__(message)
        self.code = code
        self.message = message


class UnknownCommandError(RedisLiteError):

    def __init__(self):
        super().__init__(
            code = "UNKNOWN_COMMAND",
            message = "Komut desteklenmiyor."
        )

class InvalidArgumentCountError(RedisLiteError):

    def __init__(self):
        super().__init__(
            code = "INVALID_ARGUMENT_COUNT",
            message = "Argüman sayısı sözleşmeye uymuyor."
        )

class InvalidArgumentError(RedisLiteError):

    def __init__(self):
        super().__init__(
            code = "INVALID_ARGUMENT",
            message = "Skor veya sayı gibi bir argüman parse edilemiyor."
        )

class KeyNotFoundError(RedisLiteError):

    def __init__(self):
        super().__init__(
            code = "KEY_NOT_FOUND",
            message = "İstenen anahtar veya alan bulunamadı; komuta göre null sonuç da tercih edilebilir."
        )

class WrongTypeError(RedisLiteError):

    def __init__(self):
        super().__init__( 
            code = "WRONG_TYPE", 
            message = "Anahtar başka bir veri tipiyle oluşturulmuş."
        )


class InternalError(RedisLiteError):

    def __init__(self):
        super().__init__(
            code = "INTERNAL_ERROR",
            message = "Beklenmeyen uygulama hatası."
        )
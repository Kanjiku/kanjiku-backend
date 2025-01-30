from enum import StrEnum


class SignMethod(StrEnum):
    """Class which represents different Signing Methods for JWT decoding

    This class contains several Values each representing an algorithm used for encoding and decoding JWTs.

    Supported Methods:
        * Symetric
            * HS256
            * HS384
            * HS512
    """

    HS256 = "HS256"
    HS384 = "HS384"
    HS512 = "HS512"

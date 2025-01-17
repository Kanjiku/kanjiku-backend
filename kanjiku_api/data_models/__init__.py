"""This Submodule contains all required datamodels.

Logically you can group them by the following groups:

* User and auth related models
* Blog system related
* manga related

Perhaps we should consider creating more submodules. But that would require some thinking :(
"""

from ._page import Page
from ._chapter import Chapter
from ._manga import Manga
from ._identity_token import IdentityToken
from ._refresh_token import RefreshToken
from ._reset_token import ResetToken
from ._user import User
from ._image import Image


__all__ = [
    "Page",
    "Chapter",
    "Manga",
    "IdentityToken",
    "RefreshToken",
    "ResetToken",
    "User",
    "Image",
]
__models__ = [
    Page,
    Chapter,
    Manga,
    IdentityToken,
    RefreshToken,
    ResetToken,
    User,
    Image,
]

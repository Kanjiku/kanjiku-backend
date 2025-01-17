from enum import StrEnum


class SettingKey(StrEnum):
    """These are keys which are allowed for dynamic configuration entrys."""

    Favicon = "Favicon"
    """Config key for the favicon"""
    Logo = "Logo"
    """Config key for the site logo"""
    TeamMemberRole = "TeamMemberRole"
    """This role will be the indicator for team members."""
    SupporterRole = "SupporterRole"
    """This role will be the indicator for supporters."""
    AccessLog:str = "AccessLog"
    """Should the sanic access Log be enabled?"""
    Debug:str = "Debug"
    """Is the Debug mode enabled?"""

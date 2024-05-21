from enum import Enum


class SettingKeys(Enum):
    """These are keys which are allowed for dynamic configuration entrys.
    """
    Favicon = "Favicon"
    """Config key for the favicon"""
    Logo = "Logo"
    """Config key for the site logo"""
    TeamMemberRole = "TeamMemberRole"
    """This role will be the indicator for team members."""
    SupporterRole = "SupporterRole"
    """This role will be the indicator for supporters."""

import pydantic


class Command(pydantic.BaseModel):  # type: ignore[misc]
    """Basic command class."""

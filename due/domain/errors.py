class DueError(Exception):
    """Base error for the due CLI."""


class ConfigError(DueError):
    """Error related to configuration."""


class MarkdownParseError(DueError):
    """Error while parsing a Markdown file."""

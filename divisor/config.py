import yaml
from dataclasses import dataclass
from typing import Optional

@dataclass
class SiteMetadata:
    title: str
    theme: str
    github_repository_url: str
    github_pages_url: str
    description: str = "Website created with fonte.wiki and Divisor"
    custom_domain: Optional[str] = None

@dataclass
class ContentMapping:
    home_page_source: str
    destination_folder: str
    media_destination_folder: str
    subpages_folder: Optional[str] = None

@dataclass
class Config:
    site_metadata: SiteMetadata
    source_repository: str
    content_mapping: ContentMapping

def load_config(path: str = "config.yml") -> Config:
    """Loads the configuration from a YAML file."""
    with open(path, "r") as f:
        data = yaml.safe_load(f)
    return Config(
        site_metadata=SiteMetadata(**data["site_metadata"]),
        source_repository=data["source_repository"],
        content_mapping=ContentMapping(**data["content_mapping"]),
    )

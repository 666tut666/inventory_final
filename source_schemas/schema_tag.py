from typing import Optional

from pydantic import BaseModel


class ExternalDocs(BaseModel):
    description: Optional[str] = None
    url: str


class MetadataTag(BaseModel):
    name: str
    description: Optional[str] = None
    external_docs: Optional[ExternalDocs] = None

    class Config:
        allow_population_by_field_name = True
        fields = {"external_docs": {"alias": "externalDocs"}}

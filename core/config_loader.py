import yaml
from pydantic import BaseModel, HttpUrl, ValidationError, validator
from typing import List
from core.logger import logger

class Locator(BaseModel):
    by: str
    value: str
    
    @validator('by')
    def validate_by(cls, v):
        allowed = {'id', 'name', 'xpath', 'css_selector', 'class_name', 'tag_name', 'link_text', 'partial_link_text'}

        if v not in allowed:
            raise ValueError(f"Invalid locator type: '{v}'. Supported types are: {allowed}")
        return v
    
class Field(BaseModel):
    locator: Locator
    value: str
    type: str = "text"  # Default type: text, chechbox, radio, dropdown

class SubmitButton(BaseModel):
    locator: Locator

class FormConfig(BaseModel):
    url: HttpUrl
    fields: List[Field]
    submit_button: SubmitButton

    class Config:
        arbitrary_types_allowed = True

def load_config(path: str) -> FormConfig:
    try:
        with open (path, 'r') as f:
            raw = yaml.safe_load(f)
        return FormConfig(**raw)
    
    except FileNotFoundError:
        logger.error(f"Confog file not found: {path}")
        raise 
    except ValidationError as e:
        logger.error(f"Config validation error: {e}")
        raise
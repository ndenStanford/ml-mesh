class Request(BaseModel):
    content: str
    entities: Optional[list] = None
    lang: str = 'en'
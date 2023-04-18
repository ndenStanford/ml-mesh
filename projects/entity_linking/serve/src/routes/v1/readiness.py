
router = APIRouter(
    prefix="/ready",
)

@router.post("", status_code=status.HTTP_200_OK)
@router.post("/", status_code=status.HTTP_200_OK)
async def readycheck():  
    text = "I love living in England."
    lang = 'en'
    entities = [{"text": "England"}]
    result = get_entity_linking(text, lang, entities)
    if result[0].get("text") == 'England' and result[0].get("wiki_link") == 'https://www.wikidata.org/wiki/Q21':
        return "OK"
    else:
        raise HTTPException(
            status_code=status.HTTP_500???, detail='API not ready')"
        )
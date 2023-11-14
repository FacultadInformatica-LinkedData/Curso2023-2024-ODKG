from wikidata.client import Client

# Crea un cliente de Wikidata
CLIENT = Client()


def obtain_desc_img(qualifier: str):
    description = None
    img_url = None
    
    entity = CLIENT.get(qualifier, load=True)

    description = entity.description

    image_prop = CLIENT.get('P18')
    image = entity.get(image_prop, None)
    if image:
        img_url = image.image_url

    return description, img_url

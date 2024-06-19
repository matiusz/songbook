import emoji
import aiofiles
import json

from .codings import deUTF8
from .loggerSetup import logging

logger = logging.getLogger(__name__)
def remove_emojis(s):
  return ''.join(c for c in s if c not in emoji.EMOJI_DATA)

async def getCategoriesConfig(categoryDictFile, songbookDict, allowEmojis = False):
    try:
        async with aiofiles.open(categoryDictFile, "rb") as configFile:
            configFileText = deUTF8(await configFile.read())
            if not allowEmojis:
                configFileText = remove_emojis(configFileText)
            cats_dict = json.loads(configFileText)

    except FileNotFoundError:
        logger.warning("Category titles mapping file not found")
        cats_dict = {cat: cat for cat in sorted(
            songbookDict.keys())}
    return cats_dict

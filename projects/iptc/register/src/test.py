# Standard Library
import json
# from src.settings import PromptBackendAPISettings
from typing import Dict

# 3rd party libraries
import pandas as pd
import requests
import asyncio
import aiohttp
import logging
import time
from utils_test import *

# Configure logging
logging.basicConfig(filename='iptc_enrichment.log', 
                    level=logging.INFO, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logger = logging.getLogger(__name__)

df=pd.read_csv("sample_iptc_dataset.csv")
# df.rename(columns={"article_headline":"title","article_text":"content"},inplace=True)

# logger.info('='*20)
# features_df=df.iloc[100:200]
# start = time.time()
# df_label=iptc_first_level_on_demand_feature_view(features_df)
# logger.info(df_label)
# logger.info('{} samples'.format(len(features_df)))
# logger.info(time.time() - start)

logger.info('='*20)
features_df=df.iloc[300:]
start = time.time()
df_label=iptc_first_level_on_demand_feature_view_2(features_df)
logger.info(df_label)
df_label.to_csv('df_label_asyncio.csv')
logger.info('{} samples'.format(len(features_df)))
logger.info(time.time() - start)
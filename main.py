import json
import logging
import sys
import time
from typing import List

import requests
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv('API_KEY')
API_URL = os.getenv('API_URL')
MASKS = os.getenv('MASKS').split(',')

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    stream=sys.stdout,
)
logger = logging.getLogger(__name__)


class SimpleLoginClient:
    def __init__(self, api_key: str, api_url: str):
        self.api_key = api_key
        self.api_url = api_url
        self.headers = {'Authentication': self.api_key}

    def get_aliases(self, page_id: int = 0) -> List[dict]:
        params = {'page_id': page_id}
        logger.info(f'Requesting aliases for page {page_id}')
        try:
            response = requests.get(
                f'{self.api_url}/v2/aliases',
                headers=self.headers,
                params=params,
                timeout=10,
            )
            response.raise_for_status()
            logger.info(f'Successfully retrieved aliases for page {page_id}')
        except requests.exceptions.HTTPError as err:
            logger.error(f'Error retrieving aliases for page {page_id}: {err}')
            return []
        except requests.exceptions.RequestException as err:
            logger.error(f'Request exception: {err}')
            return []
        return response.json().get('aliases', [])

    def delete_alias(self, alias_id: int) -> dict:
        logger.info(f'Attempting to delete alias ID: {alias_id}')
        try:
            response = requests.delete(
                f'{self.api_url}/aliases/{alias_id}',
                headers=self.headers,
                timeout=10,
            )
            response.raise_for_status()
            logger.info(f'Successfully deleted alias ID: {alias_id}')
        except requests.exceptions.HTTPError as err:
            logger.error(f'Error deleting alias ID {alias_id}: {err}')
            return {}
        except requests.exceptions.RequestException as err:
            logger.error(f'Request exception: {err}')
            return {}
        return response.json()


def is_matching_alias(email: str, masks: List[str]) -> bool:
    for mask in masks:
        if email.startswith(mask):
            return True
    return False


def delete_aliases_by_mask(client: SimpleLoginClient, masks: List[str]):
    page_id = 0
    total_deleted = 0
    deleted_aliases = []
    while True:
        aliases = client.get_aliases(page_id)
        if not aliases:
            if page_id == 0:
                logger.info('No aliases found.')
            else:
                logger.info('No more aliases to process.')
            break

        for alias in aliases:
            email = alias['email']
            if is_matching_alias(email, masks):
                logger.info(f'Alias {email} matches mask. Deleting...')
                result = client.delete_alias(alias['id'])
                if result.get('deleted'):
                    logger.info(f'Alias {email} successfully deleted.')
                    total_deleted += 1
                    deleted_aliases.append(email)
                else:
                    logger.error(
                        f'Failed to delete alias {email}. Response: {result}'
                    )
            else:
                logger.info(f'Alias {email} does not match any mask.')

            time.sleep(1)

        page_id += 1
        logger.info(f'Moving to the next page: {page_id}')

    logger.info(f'Total aliases deleted: {total_deleted}')
    logger.info(f'Pages processed: {page_id}')

    result = {
        'deleted_aliases': deleted_aliases,
        'total_deleted': total_deleted,
        'pages_processed': page_id,
    }
    with open('deletion_result.json', 'w') as f:
        json.dump(result, f, indent=4)
    logger.info('Deletion results saved to deletion_result.json')


if __name__ == '__main__':
    logger.info('Starting alias deletion process...')
    client = SimpleLoginClient(API_KEY, API_URL)
    delete_aliases_by_mask(client, MASKS)
    logger.info('Alias deletion process completed.')

import re

from starlette.exceptions import HTTPException


def reject_bad_fields(body, array_to_check):
    for item in array_to_check:
        current_str = re.search(fr'\"{item}\"', body)
        try:
            raise HTTPException(
                status_code=400,
                detail=f'Field {current_str.group()} are not acceptable for creation dossier',
            )
        except AttributeError:
            pass


def reject_bad_fields_filtering(url, array_to_check):
    for item in array_to_check:
        current_str = re.search(fr'{item}', str(url))
        try:
            raise HTTPException(
                status_code=400,
                detail=f'Field {current_str.group()} are not acceptable for filtering dossier',
            )
        except AttributeError:
            pass

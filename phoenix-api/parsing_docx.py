ARRAY_OF_FIELDS_APARTMENT_SALE = [
    'living_area',
    'sale_price',
    'number_of_bathrooms',
    'number_of_bedrooms',
    'condition',
    'energy_label',
    'building_year',
    'address',
    'email',
]

ARRAY_OF_FIELDS_APARTMENT_RENT = [
    'living_area',
    'rent_price',
    'number_of_bathrooms',
    'number_of_bedrooms',
    'condition',
    'energy_label',
    'building_year',
    'address',
    'email',
]


def docx_replace_one_regex(doc_obj, regex, replace):
    for p in doc_obj.paragraphs:
        if p.text.strip().lower().split():
            inline = p.runs
            # Loop added to work with runs (strings with same style)
            for i in range(len(inline)):
                text = regex.sub(str(replace).strip(), inline[i].text)
                inline[i].text = text

    for table in doc_obj.tables:
        for row in table.rows:
            for cell in row.cells:
                docx_replace_one_regex(cell, regex, str(replace).strip())

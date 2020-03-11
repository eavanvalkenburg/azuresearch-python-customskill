import logging
import json
# import pandas as pd
from typing import Callable
import azure.functions as func


def main(req: func.HttpRequest, categories: func.InputStream) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    categories_dict = eval(categories.read().decode('utf-8'))

    def get_categories(data: dict) -> dict:
        return {"categories": [term["category"] for term in categories_dict if term["term"] in data["subwords"]]}

    values = req.params.get('values')
    if not values:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            values = req_body.get('values')

    if values:
        ###### PANDAS version ######
        ## uses map on a dataframe, might be slower for small sets.
        ## do not forget to enable the import of pandas.
        # df = pd.DataFrame(values)
        # df['data'] = df['data'].map(get_categories)
        # values_out = df.to_dict('records')
        
        ###### PYTHON version ######
        ## uses list comprehension on the input, might be slower for large sets.
        values_out = [{"recordId": x["recordId"], "data": get_categories(x["data"])} for x in values]

        return func.HttpResponse(body=json.dumps({ "values": values_out}), mimetype="application/json")
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )

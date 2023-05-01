from typing import List, Dict
import json
import uvicorn
from fastapi import FastAPI
from fastapi import responses
from nltk.tree import *
from utils import SwappingGroup
from utils import (find_groups_of_nodes_for_swapping, create_new_paraphrase)

app = FastAPI()


@app.get("/paraphrase")
async def root(tree: str, limit: int = 20):
    """
    GET, function
    query parameters:
        tree: str (required) – syntax tree in the form of a string
        limit: int (optional , default: 20) - the maximum number of paraphrased texts to be returned
    response: a list of paraphrased trees in JSON format
    """

    swapping_list: List[SwappingGroup] = []
    output_dict: Dict[str, str] = {}
    paraphrase: List[Dict[str, str]] = []

    # validate input tree
    try:
        # create input Tree object
        input_tree = Tree.fromstring(tree)
    except ValueError as e:
        err = e.__str__()
        answer = f'InvalidInput. {err}'
        response = responses.Response(content=answer, status_code=400)
        return response

    # find groups of nodes, that can be swapped
    swapping_list = find_groups_of_nodes_for_swapping(input_tree)

    # get paraphrases
    paraphrase = create_new_paraphrase(tree, swapping_list, limit)

    # convert to JSON answer
    answer_dict = {
        "paraphrases": paraphrase,
    }
    answer_json = json.dumps(answer_dict, indent=4)

    # create response and return
    response = responses.Response(content=answer_json)
    response.headers['content-type'] = 'application/json'

    return response


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

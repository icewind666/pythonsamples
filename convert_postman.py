import json

METHOD_HEADER = '## {}'
METHOD_BLOCK_HEADER = '#### {}'
METHOD_BLOCK_BODY = ' '


def load_postman_collection(collection_file):
    """
    Loads json from exported postman collection
    :param collection_file:
    :return:
    """
    json_data = json.load(open(collection_file, 'r', encoding="UTF-8"))
    if json_data is not None:
        return json_data['item']
    else:
        print('cant read json file!')
    pass


def get_markdown_for_method(method_info):
    """
    Returns markdown for given method structure
    :param method_info:
    :return:
    """


    pass



if __name__ == '__main__':
    collection_json = load_postman_collection('Containers-New.json')

    for item in collection_json:
        name = item['name']
        request = item['request']
        response = item['response']  # optional

        print(item)




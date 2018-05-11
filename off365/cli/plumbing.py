'''
Here you find the "plumbing" commands for working with MS Graph API.
'''

from .common import arg, command, get_api, handle_response, get_input_docs
import pyaml

@command('get',
         arg('endpoint', help="endpoint, e.g. users/USER@TENANT.onmicrosoft.com/memberOf"),
         arg('param', nargs="*", help="parameters like foo=bar"),
         )
def cmd_get(config, endpoint, param):
    api = get_api(config)
    response = api.get(endpoint, get_input_docs(param, key="no-stdin")[0])
    return handle_response(response)

@command('post',
         arg('endpoint', help="endpoint, e.g. users"),
         arg('--key', '-k', help="name of key in record"),
         arg('--exclude', '-e', help="exclude given items (comma-separated), can be there multiple times", action="append"),
         arg('param', nargs="*", help="parameters like foo=bar or '-' for "),
         )
def cmd_post(config, endpoint, param, key=None, exclude=[]):
    """post is usually used for creating some object, you can either pass
    command line arguments or you can pass "-" and do input via YAML from
    stdin.
    """
    api = get_api(config)
    if exclude is None:
        exclude = []
    _exclude = ",".join(exclude).split(",")

    responses = []

    for doc in get_input_docs(param, key=key):
        endpoint.format(**doc)
        for item in _exclude:
            if item in doc:
                del doc[item]

        logger.debug("endpoint: %s", endpoint)
        logger.debug("doc: %s", doc)

        responses.append(api.post(endpoint, doc))

    handle_response(responses)


@command('delete',
         arg('endpoint', help="endpoint, e.g. users/USER@TENANT.onmicrosoft.com"),
         arg('param', nargs="*", help="parameters like foo=bar or '-' for "),
         )
def cmd_delete(config, endpoint, param):
    api = get_api(config)
    response = api.delete(endpoint, get_input_docs(param))
    handle_response(response)


@command('patch',
         arg('endpoint', help="endpoint, e.g. users/USER@TENANT.onmicrosoft.com"),
         arg('param', nargs="*", help="parameters like foo=bar or '-' for "),
         )
def cmd_patch(config, endpoint, param):
    api = get_api(config)

    docs = get_input_docs(param)

    responses = []
    for doc in docs:
        response = api.patch(endpoint, doc)
        responses.append(response)

    handle_response(responses)


@command('put',
         arg('endpoint', help="endpoint, e.g. users/USER@TENANT.onmicrosoft.com"),
         arg('--content-type', '-t', help="content-type of the input"),
         arg('files', nargs="*", help="parameters like foo=bar or '-' for "),
         )
def cmd_put(config, endpoint, files):
    # if - conten-type must be given
    # else guess mime type from file_name
    pass

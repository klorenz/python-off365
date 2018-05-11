from ..config import get_config, get_api, read_config_file, write_config_file
from argdeco import CommandDecorator, arg, mutually_exclusive, opt
from ..util import get_input_docs, f
import pyaml

command = CommandDecorator(
    arg('--config', '-c', help="configuration to use", default="default"),
    arg("--debug", action="store_true", help="turn on debug mode"),
)

def make_response_dict(response, verbose=False):
    result = {
        "status_code": response.status_code,
        #"headers": response.headers,
        "content_type": response.headers.get('content-type'),
        "content_length": response.headers.get('content-length'),
        "encoding": response.encoding or 'utf-8',
        "content": response.content
    }

    pprint.pprint(result)
    if verbose:
        result['headers'] = response.headers

    return result


def handle_response(response, quiet=False, verbose=False):
    if isinstance(response, list):
        assert len(response) == 1, "Response list not yet supported"
        response = response[0]

    try:
        result = response.json()
    except:
        result = make_response_dict(response)

    if verbose:
        # result = {"request": { "headers", response.request.headers}
        #
        # add request and response
        #
        pass

    if not quiet:
        pyaml.p(result)

    if 200 <= int(response.status_code) < 300:
        return 0
    else:
        return 1

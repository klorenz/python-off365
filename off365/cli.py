from .config import get_config, get_api
from argdeco import CommandDecorator, arg
from .util import f, get_input_docs
import config
from .resource import get_fields

import logging
logging.basicConfig()
logger = logging.getLogger('off365')

import yaml, pyaml, pprint, sys

def is_collection(name):
    """compare with https://developer.microsoft.com/en-us/graph/docs/api-reference/v1.0/resources/user"""

    return name in [
        'assignedLicenses', 'assignedPlans', 'businessPhones', 'imAddresses',
        'interests', 'provisionedPlans', 'proxyAddresses', 'responsibilities',
        'schools', 'skills'
    ]


def is_userPrincipalName(name):
    return '@' in name and name.endswith('.onmicrosoft.com')

def show_user(api, userPrincipalName):
    userPrincipalName = api.getUserPrincipalName(userPrincipalName)
    data = api.get(f("users/{userPrincipalName}")).json()
    pyaml.p(data)

def create_users(api, confirm, userPrincipalName, *args):
    """
    see https://developer.microsoft.com/en-us/graph/docs/api-reference/v1.0/api/user_post_users

      {
        "accountEnabled": true,
        "displayName": "displayName-value",
        "mailNickname": "mailNickname-value",
        "userPrincipalName": "upn-value@tenant-value.onmicrosoft.com",
        "passwordProfile" : {
        "forceChangePasswordNextSignIn": true,
            "password": "password-value"
        }
      }

    """

    entries = get_input_docs(args, keyName="userPrincipalName",
        key=userPrincipalName, is_key=lambda n: '@' in n,
        is_collection=is_collection)

    results = []
    for e in entries:
        if 'password' in e:
            if 'forceChangePasswordNextSignIn' in e:
                forceChange = e['forceChangePasswordNextSignIn']
                del e['forceChangePasswordNextSignIn']
            else:
                forceChange = True

            e['passwordProfile'] = {
                'forceChangePasswordNextSignIn': forceChange,
                'password': e['password']
            }

            del e['password']

        if confirm:
            # returns 201 Created on success
            results += api.post("users", e)
        else:
            results.append(e)

    return check_results(confirm, results, type)

command = CommandDecorator(
    arg('--config', '-C', help="configuration to use", default="default"),
    arg("--debug", "-d", action="store_true", help="turn on debug mode"),
    )


@command("config",
        arg("--client-id", help="client_id", required=True),
        arg("--client-secret", help="client_secret"),
        arg("--tenant", help="e.g. mycompany.onmicrosoft.com", required=True),
        arg("--redirect-uri", help="redirect URI as specified in platforms section.  E.g. http://localhost/<appname>", required=True),
        arg("--state", help="some state", default="12345"),
        arg("--username", help="username to connect"),
        )
def cmd_config(config, client_id, client_secret, tenant, redirect_uri, state, username):
    """Write a configuration to config repo.  You have to do this at least for 'default'.

    If you provide a username, you will be prompted for the password
    """
    cfg = read_config_file()
    cfg[config] = {
        'client_id': client_id,
        'client_secret': client_secret,
        'tenant': tenant,
        'redirect_uri': redirect_uri,
        'state': state
    }

    if username:
        import getpass
        cfg[config]['username'] = username
        cfg[config]['password'] = getpass.getpass()

    write_config_file(cfg)

@command('get',
    arg('endpoint', help="endpoint, e.g. users/USER@TENANT.onmicrosoft.com/memberOf"),
    arg('param', nargs="*", help="parameters like foo=bar"),
)
def cmd_get(config, endpoint, param):
    api = get_api(config)
    response = api.get(endpoint, get_input_docs(param, key="no-stdin")[0])
    return handle_response(response)

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
        #result = {"request": { "headers", response.request.headers}
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

plans_command = command.add_subcommands("plans", help="Commands to manage plans")
@plans_command("ls",
    arg("product", nargs="?", help="list only plans of given product"),
#    arg("--guid", , help="list only plans of given product"),
)
def cmd_plans_ls(config, product):
    from .service_plans import SERVICE_PLANS
    pyaml.p(SERVICE_PLANS['skus_by_string_id'])

# products_command = command.add_subcommands("product", help="commands to manage products")
# @products_command("assign")
#     arg("product", help="product to assign"),
#     arg("")

users_command = command.add_subcommands("users", help="Commands to manage users")

@users_command("fields",
#    arg("--list-fields", help="show fields, which are available in lists")
)
def cmd_users_fields(config):
    list_exclude = """aboutMe, birthday, hireDate, interests, mySite,
        pastProjects, preferredName, responsibilities, schools, skills,
        mailboxSettings""".replace(",", '').split()

    fields = sorted(get_fields('user'))
    pyaml.p(fields)

@users_command("ls",
    arg("--all-fields", "-a", help="get all fields for a user ($select=...)", action="store_true"),
    arg("--select", "-s", help="get all fields for a user ($select=...)", action="store_true"),
    arg("--filter", "-f", help="filter query ($filter=)"),
    arg('param', nargs="*", help="parameters like $select=x,y,z"),
    )
def cmd_users_ls(config, all_fields, select, filter, param):
    params = get_input_docs(param)[0]
    if all:
        params['$select'] = ",".join(get_fields('user'))

    if filter:
        params['$filter'] = filter

    # see https://developer.microsoft.com/en-us/graph/docs/api-reference/v1.0/api/user_list
    exclude = """aboutMe, birthday, hireDate, interests, mySite,
        pastProjects, preferredName, responsibilities, schools, skills,
        mailboxSettings""".replace(",", '').split()
    select = []
    for field in params['$select'].split(","):
        if field not in exclude:
            select.append(field)
    params['$select'] = ",".join(select)

    api = get_api(config)

    data = api.get("users", params).json()
    pyaml.p(data)


@users_command("assign",
    arg("--filter", "-f", help="filter query ($filter=)"),
)
def cmd_users_assign(config, filter):
    params = get_input_docs(param)[0]

    if filter:
        params['$filter'] = filter


@users_command("show",
    arg("--all-fields", "-a", help="get all fields for a user ($select=...)", action="store_true"),
    arg("--select", "-s", help="get all fields for a user ($select=...)", action="store_true"),
    arg('user', nargs="*", help="users to show"),
    )
def cmd_users_show(config, all_fields, select, param):
    params = get_input_docs(param)[0]
    if all:
        params['$select'] = ",".join(get_fields('user'))

    api = get_api(config)

    for p in param:
        data = api.get("users/"+p, params).json()
    pyaml.p(data)

# @command('users',
#     arg("--all", "-a", help="get all fields for a user ($select=...)", action="store_true"),
#     arg("--filter", "-f", help="filter query ($filter=)"),
#     arg('command', help="list or create"),
#     arg('attr', nargs="*", help="attributes like foo=bar"),
#     )
# def cmd_users(config, command, attr):
#     """
#     You can list or create users.
#
#     # List Users
#
#     # Create Users
#
#     You can either pass YAML (or JSON) documents via stdin or you can specify
#     user attributes at commandline.
#
#     If you pass multiple JSON/YAML documents, it is assumed you use
#     userPrincipalName (USER@TENANT.onmicrosoft.com) as the key for your user
#     entries.
#
#     You can lookup all possible attributes at
#     https://developer.microsoft.com/en-us/graph/docs/api-reference/v1.0/resources/user
#
#     Passing a password is special.  You can pass the values of passwordProfile
#     directly along with other values.  Passing "password" is enough. this
#     will make the user to change his PW at first login.
#     """
#     api = get_api(config)
#
#     if command == 'list':
#         data = api.get("users").json()
#         pyaml.p(data)
#
#     elif command == 'show':
#         show_user(api, *attr)
#
#     elif command == 'create':
#         create_users(api, confirm, *attr)

@command('groups')
def cmd_groups(config):
    api = get_api(config)
    data = api.get("groups").json()
    pyaml.p(data)


def main(argv=None):
    def config_factory(args, **kwargs):
        if args.debug:
            log = logging.getLogger()
            log.setLevel(logging.DEBUG)

        # you can access arguments globally from config
        print("set args (config)")
        config.args = args
        params = vars(args).copy()

        # handled debug
        del params['debug']
        del params['action']

        return [], params

    try:
        return command.execute(argv, compile=config_factory)
    except StandardError as e:
        if not hasattr(config, 'args') or config.args.debug:
            import traceback
            traceback.print_exc()
            return 1
        print(u"%s" % e).encode('utf-8')
        return 1

#@                        IN TXT     "google-site-verification=AyZKNg426MibWozr9ipX20-otJwd6R5GdOOOFEa9FS4"
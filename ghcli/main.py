import click
import datetime
import fnmatch
import json
import logging
import requests

api_url = 'https://api.github.com'

LOG = logging.getLogger(__name__)


@click.group()
@click.option('--debug', 'loglevel', flag_value='DEBUG')
@click.option('--verbose', 'loglevel', flag_value='INFO')
@click.option('--quiet', 'loglevel', flag_value='WARNING', default=True)
@click.option('--credentials', '-c', 'creds', type=click.File(mode='r'))
@click.pass_context
def github(ctx, loglevel, creds):
    logging.basicConfig(level=loglevel)
    ctx.obj = requests.Session()

    if creds:
        _creds = json.load(creds)
        if 'token' in _creds:
            ctx.obj.headers['Authorization'] = 'token {token}'.format(**_creds)


@github.group()
def repo():
    pass


def get_paginated(sess, url, params):
    page = 1
    data = []

    _params = {'per-page': 100}
    _params.update(params)
    while True:
        LOG.debug('request page %d from %s', page, url)
        _params['page'] = page
        res = sess.get(url, params=_params)
        try:
            res.raise_for_status()
        except requests.HTTPError as err:
            raise click.ClickException(str(err))

        if not res.json():
            break

        data.extend(res.json())

        page += 1

    return data


def parse_iso8601(val):
    return datetime.datetime.strptime(val, "%Y-%m-%dT%H:%M:%SZ")


@repo.command(name='ls')
@click.option('--data-in', '-I', type=click.File(mode='r'))
@click.option('--data-out', '-O', type=click.File(mode='w'))
@click.option('-u', '--user')
@click.option('-o', '--org')
@click.option('--forks/--no-forks', default=None)
@click.option('-r', '--reverse', is_flag=True)
@click.option('-s', '--sort',
              type=click.Choice(['created', 'updated', 'pushed']))
@click.option('--url', 'show_url', is_flag=True)
@click.option('--format', '-f', '_format')
@click.option(
    '-t', '--type', 'repo_type',
    type=click.Choice(['owner', 'member', 'public', 'private',
                       'forks', 'sources']))
@click.option('--public', 'visibility', flag_value='public')
@click.option('--private', 'visibility', flag_value='private')
@click.argument('patterns', nargs=-1)
@click.pass_context
def lsrepo(ctx, data_in, data_out, user, org,
           forks, reverse, sort, show_url, _format,
           repo_type, visibility, patterns):
    sess = ctx.obj

    if user:
        url = '{}/users/{}/repos'.format(api_url, user)
    elif org:
        url = '{}/orgs/{}/repos'.format(api_url, org)
    else:
        url = '{}/user/repos'.format(api_url)

    params = {}

    if visibility:
        params['visibility'] = visibility
    if repo_type:
        params['type'] = repo_type
    if sort:
        params['sort'] = sort

    if data_in:
        repos = json.load(data_in)
    else:
        repos = get_paginated(sess, url, params)

    LOG.info('found %s repositories from api', len(repos))

    if forks is False:
        repos = [repo for repo in repos if not repo['fork']]
    elif forks is True:
        repos = [repo for repo in repos if repo['fork']]

    if reverse:
        repos = reversed(repos)

    if patterns:
        repos = [repo for repo in repos
                 if any(
                         fnmatch.fnmatch(repo['name'], pattern)
                         for pattern in patterns
                 )]

    LOG.info('found %s repositories after filtering', len(repos))

    if data_out:
        json.dump(repos, data_out, indent=2)

    for repo in repos:
        if _format:
            print(_format.format(**repo))
        elif show_url:
            print(repo['name'], repo['html_url'])
        else:
            print(repo['name'])


if __name__ == '__main__':
    github()

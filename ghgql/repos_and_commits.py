"""
Repos and commits report.

For a given repo owner and option start data, get all commits for all repos
under that the owner.

While paging of either repos or commits is possible, it is not possible in the
API handle the outer and inner paging at the same time. So the approach here is
to build up a list of repos to query and using paging and a cursor for each to
get their commits. When there is nothing to get from a repo, it falls away and
can be replaced by another. Note that the total number of repos should not be so
high that the request fails. Querying 100 repos (and 100 commits each) is very
likely to fail based on tests, therefore a lower count is used.

Jinja templating is used to build up the GQL query neatly.

The GQL "fragment" syntax is used in order to limit the total size of the query
text, as the long list of fields needed for each repo is defined once in the
fragment.

Note that no JSON data is supplied in the request. Since a fragment cannot
accept arguments. It was not tested yet whether a fragment can get the "global"
arguments. But since the whole query is built from scratch on each request based
on required repos, it is easy to substitute in values that would normally be in
the JSON data payload like "owner".
"""
from jinja2 import Template

import lib


TEMPLATE_DIR = lib.APP_DIR / 'templates'
QUERY_PATH = TEMPLATE_DIR / 'repos_and_commits.gql'


def render(template, owner, repos, since, dry_run=False):
    return template.render(
        owner=owner,
        repos=repos,
        since=since,
        dry_run=dry_run
    )


def main():
    since_input = '2019-08-01'

    since = lib.timestamp(since_input) if since_input else None
    owner = 'michaelcurrin'
    repo_names = ['twitterverse', 'aggre-git']

    repos = [{'name': name, 'cursor': None} for name in repo_names]

    template = lib.read_template(QUERY_PATH)
    print(render(template, owner, repos, since))


if __name__ == '__main__':
    main()

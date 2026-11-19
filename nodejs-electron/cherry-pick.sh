#!/bin/sh
set -e

if ! [ -z "$(git status --untracked-files=no --porcelain)" ]; then
  git status
  echo
  echo "Working directory not clean."
  exit 1
fi

head="$(git rev-parse HEAD)"

list=""
for arg in "$@"; do
    if [ $(git rev-parse "$arg" | wc -l) == "1" ]; then
        list="$list $(git rev-parse "$arg")"
    else
        list="$list $(git rev-list --reverse $(git rev-parse "$@"))"
    fi
done

for commit in $list; do
    echo "Cherry pick: $commit"
    git branch -f _rewrite $commit
    FILTER_BRANCH_SQUELCH_WARNING=1 \
        git filter-branch -f \
        --tree-filter "mv chromium.spec nodejs-electron.spec;
        sed -i -e '/%changelog/,//d' \
            -e '/^Version:/d' \
            -e '/^Release:/d' \
            nodejs-electron.spec;
        rm -f chromium.conf chromium-browser.sh chromium-browser.desktop sources
        " \
        '_rewrite~2.._rewrite'
    ver=$(git show $commit:chromium.spec | grep '^Version' | cut -d: -f2 | tr -d " " | sed 's/\./ /g')
    sources="$(git show $commit:sources)"
    echo "  Chromium version: $ver"
    set -- $ver

    set +e
    git cherry-pick --allow-empty --empty=keep _rewrite
    ret=$?
    echo "Ret: $ret"
    set -e
    sed -i \
        -e "s/^%global chromium_major .*/%global chromium_major $1/" \
        -e "s/^%global chromium_branch .*/%global chromium_branch $3/" \
        -e "s/^%global chromium_minor .*/%global chromium_minor $4/" \
        nodejs-electron.spec
    (head -n 1 sources; echo "$sources") > sources.new
    mv sources.new sources
    if [ "$ret" = 0 ]; then
        git add nodejs-electron.spec sources
        git commit --amend --allow-empty
        parent=$(git rev-parse 'HEAD^1^{tree}')
        new=$(git rev-parse 'HEAD^{tree}')
        if [ "$new" = "$parent" ]; then
            echo "Skipping commit $commit (empty after processing)"
            git reset --hard HEAD\^
            continue
        fi
    else
        git status
        exit $ret
    fi
done

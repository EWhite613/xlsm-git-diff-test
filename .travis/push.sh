#!/bin/sh

setup_git() {
  git config --global user.email "ericwhite613@gmail.com"
  git config --global user.name "Eric White"
}


publish_gh_pages() {
  git checkout -b gh-pages -set-upstream origin gh-pages
  git pull
  rm -rf `ls -a | grep -vE '\.gitignore|\.git|node_modules|bower_components|(^[.]{1,2}/?$)'` && git add -A && git commit -m "initial gh-pages commit"
  git branch -r
  git checkout dev
  git fetch
  ember github-pages:commit --message "[ci skip] Update gh-pages"
  git push --set-upstream origin gh-pages
}

setup_git
publish_gh_pages

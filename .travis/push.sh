#!/bin/sh

setup_git() {
  git config --global user.email "ericwhite613@gmail.com"
  git config --global user.name "Eric White"
  git clone --branch=$branch $repo
  git checkout $sha1
}


publish_gh_pages() {
  git checkout dev
  ember install ember-cli-github-pages
  git commit -am "[ci skip] install github-pages"
  ember github-pages:commit --message "[ci skip] Update gh-pages"
  git push
}
setup_git
publish_gh_pages
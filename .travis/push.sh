#!/bin/sh

setup_git() {
  git config --global user.email "ericwhite613@gmail.com"
  git config --global user.name "Eric White"
}


publish_gh_pages() {
  git fetch
  git checkout gh-pages 
  git branch -r
  git checkout dev
  ember github-pages:commit --message "[ci skip] Update gh-pages"
  git push --set-upstream origin gh-pages
}

setup_git
publish_gh_pages

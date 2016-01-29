#!/bin/sh

setup_git() {
  git config --global user.email "ericwhite613@gmail.com"
  git config --global user.name "Eric White"
}


publish_gh_pages() {
  git push origin --delete gh-pages
  git checkout --orphan gh-pages 
  rm -rf `ls -a | grep -vE '\.gitignore|\.git|node_modules|bower_components|(^[.]{1,2}/?$)'`
  git add -A
  git commit -m "initial gh-pages commit"
  git branch -r
  git checkout dev
  ember install ember-cli-github-pages
  npm install
  git commit -am "[ci skip] install github-pages"
  ember github-pages:commit --message "[ci skip] Update gh-pages"
  git push
}
setup_git
publish_gh_pages
#!/bin/sh

setup_git() {
  git clone --branch=dev https://github.com/EWhite613/xlsm-git-diff-test.git
  cd xlsm-git-diff-test/
  git config --global user.email "ericwhite613@gmail.com"
  git config --global user.name "Eric White"
  git config credential.helper "store --file=.git/credentials"
  echo "https://${GH_TOKEN}:@github.com" > .git/credentials
  git fetch origin
  git checkout -b gh-pages origin/gh-pages
  git checkout dev
  
}


publish_gh_pages() {
  ember install ember-cli-github-pages
  git commit -am "[ci skip] install github-pages"
  npm install && bower install
  ember github-pages:commit --message "[ci skip] Update gh-pages"
  git push
}
setup_git
publish_gh_pages
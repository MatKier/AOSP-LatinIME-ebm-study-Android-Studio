# Update LatinIME submodule to latest AOSP LatinIME Master (https://android.googlesource.com/platform/packages/inputmethods/LatinIME/)

1. git pull
1. git remote add upstream https://android.googlesource.com/platform/packages/inputmethods/LatinIME/
1. git fetch upstream
1. git checkout master
1. git rebase upstream/master
1. git push --force-with-lease origin master

# Initial Setup
## Create git repo and pus LatinIME source
* mkdir working_dir
* cd working_dir
* git clone https://android.googlesource.com/platform/packages/inputmethods/LatinIME LatinIME
* cd LatinIME
* create "AOSP-LatinIME-for-explicit-behavior-modification-study" github repo
* git remote set-url origin https://github.com/MatKier/AOSP-LatinIME-for-explicit-behavior-modification-study.git
* add gitignore
* git commit -m "added gitignore"
* git push -u origin master

## Create the Android Studio Project
* mkdir AOSP-LatinIME-ebm-study-Android-Studio
* cd AOSP-LatinIME-ebm-study-Android-Studio
* git clone https://github.com/iwo/LatinIME-Android-Studio.git .
* create "AOSP-LatinIME-ebm-study-Android-Studio" github repo
* git remote set-url origin https://github.com/MatKier/AOSP-LatinIME-ebm-study-Android-Studio.git
* update gitignore
* update build.gradle
  * add https://maven.google.com/ jcenter() and google() to repositories
  * update gradle classpath
  * add google-services to classpath
* update app/build.gradle
  * update compileSdkVersion, buildToolsVersion, minSdkVersion, and targetSdkVersion
  * add jniLibs.srcDirs = ['../app/src/main/jniLibs'] to sourceSets
  * uppdate dependencies
* get libjni_latinime.so libs
  * pre built or by compiling the complete AOSP 
  * put the libs in app/src/jiLibs
* git submodule add https://android.googlesource.com/platform/frameworks/opt/inputmethodcommon
* git submodule add https://github.com/MatKier/AOSP-LatinIME-for-explicit-behavior-modification-study.git LatinIME
* cd LatinIME
* git checkout master
* cd ..
* git commit -m "added submodules and jniLibs"
* git push -u origin master

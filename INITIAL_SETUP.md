# Initial Setup
## Create git repo and pull LatinIME source
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
  * add https://maven.google.com/, jcenter() and google() to repositories
  * update gradle classpath
  * add google-services to classpath
* update app/build.gradle
  * update compileSdkVersion, buildToolsVersion, minSdkVersion, and targetSdkVersion
  * add jniLibs.srcDirs = ['../app/src/main/jniLibs'] to sourceSets
  * uppdate dependencies
* get libjni_latinime.so libs
  * pre built or by compiling from the AOSP (see "Building libjni_latinime.so")
  * put the libs in app/src/jiLibs
* git submodule add https://android.googlesource.com/platform/frameworks/opt/inputmethodcommon
* git submodule add https://github.com/MatKier/AOSP-LatinIME-for-explicit-behavior-modification-study.git LatinIME
* cd LatinIME
* git checkout master
* cd ..
* git commit -m "added submodules and jniLibs"
* git push -u origin master

## Building libjni_latinime.so
* Basically follow these instructions: https://source.android.com/setup/build/initializing
* In short (for only building the library and not the complete AOSP): 
  * Setup the Build Environment & Tools:
```
sudo apt-get update
sudo apt install git
sudo apt install python2.7 python-pip
sudo apt-get install openjdk-8-jdk

sudo update-alternatives --config java
sudo update-alternatives --config javac

sudo apt-get install git-core gnupg flex bison gperf build-essential zip curl zlib1g-dev gcc-multilib g++-multilib libc6-dev-i386 lib32ncurses5-dev x11proto-core-dev libx11-dev lib32z-dev libgl1-mesa-dev libxml2-utils xsltproc unzip
```
  * Install Repo and Download the Source (around 80Gb):
  ```
mkdir ~/bin
PATH=~/bin:$PATH

curl https://storage.googleapis.com/git-repo-downloads/repo > ~/bin/repo
chmod a+x ~/bin/repo

mkdir WORKING_DIRECTORY
cd WORKING_DIRECTORY

git config --global user.name "Your Name"
git config --global user.email "you@example.com"

repo init -u https://android.googlesource.com/platform/manifest

repo sync
```
  * Building:
    * choose Platform with lunch (aosp_arm-eng, aosp_arm64-eng, aosp_x86-eng, aosp_x86_64-eng)
  ```
make clobber

source build/envsetup.sh

cd packages/inputmethods/LatinIME/native/jni

lunch aosp_arm64-eng

mma
```
  * libjni_latinime.so now sits in out/target/product/generic_arm64/system/lib64
  

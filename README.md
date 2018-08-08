# Gradle build for AOSP-LatinIME-for-explicit-behavior-modification-study (Android Keyboard for Keystrokebiometrics study)
This Project is based on the LatinIME Android Keyboard (ttps://android.googlesource.com/platform/packages/inputmethods/LatinIME) and Iwo Banaś' (https://github.com/iwo/LatinIME-Android-Studio) Gradle build configuration.
The LatinIME was modified in two ways: 
1. It contains a logger class for logging all Keyevents (up&down including all interesting properties) to csv files 
2. It contains activities which are used for a behavior biometrics user study

The aim of this project and the corresponding user study is to check if (and how well) people can actively control their typing behavior regarding the following properties: key offset, hold time, flight time and touch area.


## How to build AOSP-LatinIME-ebm-study-Android-Studio
1. Clone build configuration & submodules recursively:

        git clone --recurse-submodules -j8 https://github.com/MatKier/AOSP-LatinIME-ebm-study-Android-Studio.git
1. Import project into Android Studio
1. Download necessary Android SDK and Build Tools
1. Sync Gradle Files
        1. File -> Sync Project with Gradle Files
        1. Right Click on build.gradle -> Synchronize 'build.gradle'
1. Rebuild Project

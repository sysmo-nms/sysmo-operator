Release cycle
=============

This file is an action remainder for the core development team. It is of no interest for users.

### Description
- Windows installers are build with AppVeyor service (see .appveyor.yml),
- Linux repositories are filled with OpenSuse OpenBuildService (see support/pkgs/obs/*). Linux build must be manualy triggered by "make packages".

### Where is the current "unstable" release

* As windows installer, only available for authorized users (devel team) as a draft release of name "CURRENT": [https://github.com/sysmo-nms/sysmo-operator/releases](https://github.com/sysmo-nms/sysmo-operator/releases). We may in the future make this release public but tagged as "prerelease". It is rebuilt at each git push.
* As packages for linux at [https://software.opensuse.org/download.html?project=home%3Asysmo%3Aunstable&package=sysmo-operator](https://software.opensuse.org/download.html?project=home%3Asysmo%3Aunstable&package=sysmo-operator), wich is publicly available for linux users. It is rebuild at each manual call to "make packages" (you must have write permission on the build.opensuse.org repo home:sysmo).

# STEP1 Promoting the actual "unstable" build

* Log in on github.com and promote the CURRENT release the actual version (set in CMakeList.txt). It will create a new tag (do not forget to "git pull" from your machine to update the tag),
* Run the support/pkgs/obs/promote.sh script that will promote the OBS build and publish to the repository.

The release is now available as:
* Windows installer on the github latest release: [https://github.com/sysmo-nms/sysmo-operator/releases/latest](https://github.com/sysmo-nms/sysmo-operator/releases/latest).
* Packages are available througth RPM or DEB repositories for various linux distributions at OpenSuze OpenBuildService (OBS): [https://software.opensuse.org/download.html?project=home%3Asysmo&package=sysmo-operator](https://software.opensuse.org/download.html?project=home%3Asysmo&package=sysmo-operator). (Can take some time before complete)

# STEP2 Rebuild the windows bundle
Once the release is built:
* Upgrade the OPERATOR_VERION and BUNDLE_VERSION in [bundle.cmd](https://github.com/sysmo-nms/bundle).
* Push it and wait for appveyor build,
* Publish the CURRENT release to the new bundle version.

The Windows installer bundle is available at: [https://github.com/sysmo-nms/bundle/releases/latest](https://github.com/sysmo-nms/bundle/releases/latest).

# STEP3 Finalysing

* Modify the $OPERATOR_VERSION variable in CMakelist.txt,
* Run cmake. this action will configure relevant files with the new version value,
* Commit the changes,
* Run the support/packages/obs/update.sh script that will push newly configurated files to OBS.

After some commits (at least one to create the "CURRENT" draft release on github), you can promote another build (STEP1).

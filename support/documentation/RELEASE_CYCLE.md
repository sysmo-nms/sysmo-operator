Release cycle
=============

This file is an action remainder for the core development team. It is of no interest for users.

### Description
- Windows installers are build with AppVeyor service (see .appveyor.yml),
- Linux repositories are filled with OpenSuse OpenBuildService (see support/pkgs/obs/*). Linux build must be manualy triggered by support/pkgs/obs/forcerun.sh.

### Where is the current "unstable" release

* As windows installer, only available for authorized users (devel team) as a draft release of name "CURRENT": [https://github.com/sysmo-nms/sysmo-operator/releases](https://github.com/sysmo-nms/sysmo-operator/releases). We may in the future make this release public but tagged as "prerelease". It is rebuilt at each git push.
* As packages for linux at [https://software.opensuse.org/download.html?project=home%3Asysmo%3Aunstable&package=sysmo-operator](https://software.opensuse.org/download.html?project=home%3Asysmo%3Aunstable&package=sysmo-operator), wich is publicly available for linux users. It is rebuild at each manual call to support/pkgs/obs/forcerun.sh.

# STEP1 Promoting the actual "unstable" build

* Log in on github.com and promote the CURRENT release the actual version (set in CMakeList.txt). It will create a new tag (do not forget to "git pull" from your machine to update the tag),
* Run the support/pkgs/obs/forcerun.sh script that will build the current revision,
* Run the support/pkgs/obs/promote.sh script that will promote the build from "unstable" to regular.

The release is now available as:
* Windows installer on the github latest release: [https://github.com/sysmo-nms/sysmo-operator/releases/latest](https://github.com/sysmo-nms/sysmo-operator/releases/latest).
* Packages are available througth RPM or DEB repositories for various linux distributions at OpenSuze OpenBuildService (OBS): [https://software.opensuse.org/download.html?project=home%3Asysmo&package=sysmo-operator](https://software.opensuse.org/download.html?project=home%3Asysmo&package=sysmo-operator).


# STEP2 Finalysing

* Modify the $OPERATOR_VERSION variable in CMakelist.txt,
* Run cmake. this action will configure relevant files with the new version value,
* Commit the changes,
* Run the support/pkgs/obs/update.sh script that will push newly configurated files to OBS.

After some commits (at least one to create the "CURRENT" draft release on github, and trigger a rebuild on OBS), you can promote another build (STEP1).

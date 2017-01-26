Release cycle
=============

This file is an action remainder for the core development team. It is of no interest for users.

### Description
- Windows installers are build with AppVeyor service (see .appveyor.yml),
- Linux repositories are filled with OpenSuse OpenBuildService (see support/packages/obs/*). Linux "unstable" builds must be manualy triggered by "make packages".

## About OBS builds

The only file modified on OBS that is elligible for revision, is the "_service" file wich describe how to download (git clone) patch and build the source. The OBS "_service" file is located at "support/packages/obs/_service" wich is build with "./configure" from "support/packages/obs/_service.in". It will allways contains the "${OPERATOR_VERSION}" defined in "CMakeLists.txt".

* A call to "support/packages/obs/update_unstable.sh" will commit and push the actual "support/packages/obs/_service" to the OBS "unstable" repository. Typicaly used after an OPERATOR_VERSION bump.
* A call to "support/packages/obs/update_stable.sh" will commit and push the actual "support/packages/obs/_service" to the OBS "stable" repository. Typicaly used for publishing the actual OPERATOR_VERSION release.
* A call to "make packages" will force a rebuild on OBS "unstable" with the latest repo commit. Typicaly used to publish the latest commit to the "unstable" repository.

### Where is the current "unstable" release

* A windows installer, only available for authorized users (devel team) as a draft release of name "CURRENT": [https://github.com/sysmo-nms/sysmo-operator/releases](https://github.com/sysmo-nms/sysmo-operator/releases). We may in the future make this release public but tagged as "prerelease". It is rebuilt at each git push.
* A packages for linux at [https://software.opensuse.org/download.html?project=home%3Asysmo%3Aunstable&package=sysmo-operator](https://software.opensuse.org/download.html?project=home%3Asysmo%3Aunstable&package=sysmo-operator), wich is publicly available for linux users. It is rebuild at each manual call to "make packages" (you must have write permission on the build.opensuse.org repo home:sysmo).

# STEP1 Promoting the "CURRENT"/"unstable" build

* Log in on github.com and promote the CURRENT release the actual version (set in CMakeList.txt). It will create a new tag,
* Run the support/packages/obs/update_stable.sh script that will push the new _service file to the "stable" repository. It can take some time before the build complete.

The release is now available as:
* Windows installer on the github latest release: [https://github.com/sysmo-nms/sysmo-operator/releases/latest](https://github.com/sysmo-nms/sysmo-operator/releases/latest).
* Packages are available througth RPM or DEB repositories for various linux distributions at OpenSuze OpenBuildService (OBS): [https://software.opensuse.org/download.html?project=home%3Asysmo&package=sysmo-operator](https://software.opensuse.org/download.html?project=home%3Asysmo&package=sysmo-operator).

# STEP2 Rebuild the windows bundle
Once the release is built:
* Upgrade the OPERATOR_VERION and BUNDLE_VERSION in the [bundle.cmd](https://github.com/sysmo-nms/bundle).
* Push and wait for appveyor build,
* Publish the CURRENT release to the new bundle version.

The Windows installer bundle is available at: [https://github.com/sysmo-nms/bundle/releases/latest](https://github.com/sysmo-nms/bundle/releases/latest).

# STEP3 Finalysing

* Modify the $OPERATOR_VERSION variable in CMakelist.txt,
* Run ./configure. this action will configure relevant files with the new version value,
* Commit the changes,
* Run the support/packages/obs/update_unstable.sh script that will push newly configurated files to the OBS "unstable" repository.

After some commits, you can promote another build (STEP1).

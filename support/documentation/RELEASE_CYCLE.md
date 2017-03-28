Release cycle
=============

This file is an action remainder for the core development team. It is of no interest for users.

# **Step1** Promoting the "CURRENT" *sysmo-operator* version

1. Be sure that you have **commited the changes** you want to be part of the release, and the **AppVeyor build is up to date**.
2. On github.com **promote the CURRENT release** the actual version (set in CMakeList.txt). It will create a new tag,
3. **Run the support/packages/obs/update_stable.sh** script that will push the new _service file to the "stable" repository. 

The release is now available as:
* *Windows installer* on the github latest release: [https://github.com/sysmo-nms/sysmo-operator/releases/latest](https://github.com/sysmo-nms/sysmo-operator/releases/latest).
* Packages are available througth *RPM or DEB* repositories for various linux distributions at OpenSuze OpenBuildService (OBS): [https://software.opensuse.org/download.html?project=home%3Asysmo&package=sysmo-operator](https://software.opensuse.org/download.html?project=home%3Asysmo&package=sysmo-operator).


# **Step2** Rebuild the windows *bundle*

Once the release is promoted (Step1->2):
1. Upgrade the **OPERATOR_VERSION and BUNDLE_VERSION** in the [bundle.cmd](https://github.com/sysmo-nms/bundle).
2. **Push and wait** for appveyor build to finish,
3. Once the appveyor build is finished, **Publish the CURRENT** release to the new bundle version.

The Windows installer bundle is available at: [https://github.com/sysmo-nms/bundle/releases/latest](https://github.com/sysmo-nms/bundle/releases/latest).


# **Step3** Preparing the next *sysmo-operator* release

1. Modify the $OPERATOR_VERSION variable in CMakelist.txt,
2. Run ./bootstrap.sh, will configure relevant files with the new version value,
3. Commit the changes,
4. Push,
5. As soon as the appveyor build this commit, you can release again (see **Step1**),


# **Step4** Working with current instable *sysmo-operator* build

1. Run the **support/packages/obs/update_unstable.sh** script that will push newly configurated files to the OBS "unstable" repository.
2. Each time you want to update the "unstable" repository, just run **make package**,
3. Wait for the build to finish (see [the unstable build](https://build.opensuse.org/project/show/home:sysmo:unstable),
4. Run (for exemple) "yum clean all & yum update", to install the *sysmo-operator* of the latest master branch commit.


## About repositories
- Windows installers are build with AppVeyor service (see .appveyor.yml),
- Linux repositories are filled with OpenSuse OpenBuildService (see support/packages/obs/*). Linux "unstable" builds must be manualy triggered by "make packages".


## About OBS builds
- obs unstable [admin interface](https://build.opensuse.org/project/show/home:sysmo:unstable)
- obs unstable [repository page](https://software.opensuse.org//download.html?project=home%3Asysmo%3Aunstable&package=sysmo-operator)
- obs stable [admin interface](https://build.opensuse.org/project/show/home:sysmo)
- obs stable [repository page](https://software.opensuse.org//download.html?project=home%3Asysmo&package=sysmo-operator)

The only file modified on OBS that is elligible for revision, is the "_service" file wich describe how to download (git clone) patch and build the source. The OBS "_service" file is located at "support/packages/obs/_service" wich is build with "./configure" from "support/packages/obs/_service.in". It will allways contains the "${OPERATOR_VERSION}" defined in "CMakeLists.txt".

* A call to "make packages" will force a rebuild on OBS "unstable" with the latest repo commit. Typicaly used to publish the latest commit to the "unstable" repository.
* A call to "support/packages/obs/update_unstable.sh" will commit and push the actual "support/packages/obs/_service" to the OBS "unstable" repository. Typicaly used after an OPERATOR_VERSION bump.
* A call to "support/packages/obs/update_stable.sh" will commit and push the actual "support/packages/obs/_service" to the OBS "stable" repository. Typicaly used for publishing the actual OPERATOR_VERSION release.


### Where is the current "unstable" release

* A windows installer, only available for authorized users (devel team) as a draft release of name "CURRENT": [https://github.com/sysmo-nms/sysmo-operator/releases](https://github.com/sysmo-nms/sysmo-operator/releases). We may in the future make this release public but tagged as "prerelease". It is rebuilt at each git push.
* A packages for linux at [https://software.opensuse.org/download.html?project=home%3Asysmo%3Aunstable&package=sysmo-operator](https://software.opensuse.org/download.html?project=home%3Asysmo%3Aunstable&package=sysmo-operator), wich is publicly available for linux users. It is rebuild at each manual call to "make packages" (you must have write permission on the build.opensuse.org repo home:sysmo).



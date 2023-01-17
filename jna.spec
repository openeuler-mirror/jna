Name:           jna
Version:        4.5.1
Release:        8
Summary:        Pure Java access to native libraries
License:        (LGPLv2 or ASL 2.0) and ASL 2.0
URL:            https://github.com/java-native-access/jna/
Source0:        https://github.com/java-native-access/jna/archive/4.5.1.tar.gz
# Package list for prebuild
Source1:        package-list
# Add RPM_LD_FLAGS for adapt build
Patch0000:      0001-Adapt-build.patch
# MODIFIED FROM UPSTREAM - we rip out all sorts of gunk here that is
# unnecessary when JNA is properly installed with the OS.
Patch0001:      0002-Load-system-library.patch
# The X11 tests currently segfault; overall I think the X11 JNA stuff is just a
# Really Bad Idea, for relying on AWT internals, using the X11 API at all,
# and using a complex API like X11 through JNA just increases the potential
# for problems.
Patch0002:      0003-Tests-headless.patch
# Adds --allow-script-in-comments arg to javadoc to avoid error
Patch0003:      0004-Fix-javadoc-build.patch
# Avoid generating duplicate manifest entry
Patch0004:      0005-Fix-duplicate-manifest-entry.patch
# Remove Werror flag for build
Patch0005:      0006-Remove-Werror.patch
BuildRequires:  make javapackages-local libffi-devel ant ant-junit gcc
BuildRequires:  junit libX11-devel libXt-devel reflections
Requires:       libffi
Provides:       jna-contrib = %{version}-%{release}
Obsoletes:      jna-contrib < %{version}-%{release}

%description
JNA provides Java programs easy access to native shared libraries without
writing anything but Java code - no JNI or native code is required.

%package        help
Summary:        Help docs for jna
BuildArch:      noarch
Provides:       jna-javadoc = %{version}-%{release}
Obsoletes:      jna-javadoc < %{version}-%{release}

%description    help
This package contains the help docs for jna.

%prep
%autosetup -n jna-%{version} -p1

cp %{SOURCE1} .
chmod -Rf a+rX,u+w,g-w,o-w .
sed -i 's|@LIBDIR@|%{_libdir}/jna|' src/com/sun/jna/Native.java
sed s,'<include name="junit.jar"/>,&<include name="reflections.jar"/>,' -i build.xml
build-jar-repository -s -p lib junit reflections ant
cp lib/native/aix-ppc64.jar lib/clover.jar

%build
ant -Dcompatibility=1.6 -Dplatform.compatibility=1.6 -Dcflags_extra.native="%{optflags}" -Ddynlink.native=true native dist
find contrib -name build | xargs rm -rf

%install
install -D -m 755 build/native*/libjnidispatch.so %{buildroot}%{_libdir}/jna/libjnidispatch.so

%mvn_file :jna jna jna/jna %{_javadir}/jna
%mvn_package :jna-platform contrib
%mvn_alias :jna-platform :platform
%mvn_artifact pom-jna.xml build/jna-min.jar
%mvn_artifact pom-jna-platform.xml contrib/platform/dist/jna-platform.jar
%mvn_install -J doc/javadoc

%files -f .mfiles -f .mfiles-contrib
%doc OTHERS TODO
%license LICENSE LGPL2.1 AL2.0
%{_libdir}/jna

%files help -f .mfiles-javadoc
%doc README.md CHANGES.md

%changelog
* Tue Jan 17 2023 caodongxia <caodongxia@h-partners.com> - 4.5.1-8
- Add source package-list

* Wed Jun 2 2021 wulei <wulei80@huawei.com> - 4.5.1-7
- fixes failed: gcc: command not found

* Tue Mar 3 2020 chenli <chenli147@huawei.com> - 4.5.1-6
- Fixed URL

* Fri Nov 22 2019 sunguoshuai <sunguoshuai@huawei.com> - 4.5.1-5
- Package init.

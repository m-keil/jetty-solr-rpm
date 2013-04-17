%define _prefix /opt/solr
%define _logprefix /var/log/solr
%define _javaprefix /usr/lib/jvm
%define _collection_name collection1

Name:			jetty-solr
Version:		%{sver}
Release:		1%{?dist}
Summary:		Solr
License:		GPL
URL:			http://lucene.apache.org/solr/
Source:			http://www.us.apache.org/dist/lucene/solr/%{version}/solr-%{version}.tgz
Source1:                http://download.eclipse.org/jetty/%{jver}/dist/jetty-distribution-%{jver}.tar.gz
Source2:		jetty
Patch0:			jetty.xml-remove_requestlog.patch
Patch1:			jetty-requestlog.xml-change_filename.patch
Patch2:			jetty-logging.xml-change_filename.patch
BuildRoot:		%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
Requires(pre):		shadow-utils
Requires(post):		chkconfig
Requires(preun):	chkconfig
Requires(preun):	initscripts
Requires(postun):	initscripts
Requires:		java7 => 1:1.7.0

%description
%{summary}
%prep
%setup -q -n solr-%{version}
%patch0 -p0
%setup -q -D -T -b 1 -n jetty-distribution-%{jver}
%patch1 -p0
%patch2 -p0

%build

%install
rm -rf $RPM_BUILD_ROOT
%__install -d "%{buildroot}%{_prefix}"
cp -p $RPM_BUILD_DIR/solr-%{version}/*.txt "%{buildroot}%{_prefix}"
cp -pr $RPM_BUILD_DIR/solr-%{version}/contrib "%{buildroot}%{_prefix}"
cp -pr $RPM_BUILD_DIR/solr-%{version}/dist "%{buildroot}%{_prefix}"
cp -pr $RPM_BUILD_DIR/solr-%{version}/docs "%{buildroot}%{_prefix}"
cp -pr $RPM_BUILD_DIR/solr-%{version}/licenses "%{buildroot}%{_prefix}"
%__install -d "%{buildroot}%{_prefix}/jetty-solr"
cp -pr $RPM_BUILD_DIR/solr-%{version}/example/* "%{buildroot}%{_prefix}/jetty-solr"
%if "%{_collection_name}" == "collection1"
# no need to rename
%else
mv "%{buildroot}%{_prefix}/jetty-solr/solr/collection1" "%{buildroot}%{_prefix}/jetty-solr/solr/%{_collection_name}"
%endif
%__install -d "%{buildroot}%{_prefix}"/jetty-solr/solr/"%{_collection_name}"/data
%__install -d "%{buildroot}%{_prefix}"/jetty-solr/solr/lib
%__install -d "%{buildroot}"/etc/default
%__install -d "%{buildroot}"/etc/init.d
%__install -d "%{buildroot}%{_logprefix}"
%__install -D -m0644  "%{SOURCE2}" %{buildroot}/etc/default/jetty
%__install -D -m0755  $RPM_BUILD_DIR/jetty-distribution-%{jver}/bin/jetty.sh %{buildroot}/etc/init.d/jetty-solr
%__install -D -m0644  $RPM_BUILD_DIR/jetty-distribution-%{jver}/etc/jetty-logging.xml %{buildroot}%{_prefix}/jetty-solr/etc/jetty-logging.xml
%__install -D -m0644  $RPM_BUILD_DIR/jetty-distribution-%{jver}/etc/jetty-requestlog.xml %{buildroot}%{_prefix}/jetty-solr/etc/jetty-requestlog.xml
sed -i "s|JETTY_HOME_REPLACE|%{_prefix}|g" "%{buildroot}/etc/default/jetty"
sed -i "s|JETTY_LOGS_REPLACE|%{_logprefix}|g" "%{buildroot}/etc/default/jetty"
sed -i "s|JAVA_HOME_REPLACE|%{_javaprefix}|g" "%{buildroot}/etc/default/jetty"
sed -i "s|./logs|%{_logprefix}|g" "%{buildroot}%{_prefix}/jetty-solr/etc/jetty-logging.xml"
sed -i "s|./logs|%{_logprefix}|g" "%{buildroot}%{_prefix}/jetty-solr/etc/jetty-requestlog.xml"
sed -i "s|./logs/solr%u.log|%{_logprefix}/solr-%g.log|g" "%{buildroot}%{_prefix}/jetty-solr/etc/logging.properties"
sed -i "$ a\ \n# keep 5 files \njava.util.logging.FileHandler.count = 5\n \n# append to existing \njava.util.logging.FileHandler.append = true" "%{buildroot}%{_prefix}/jetty-solr/etc/logging.properties"
sed -i "s|./logs|%{_logprefix}|g" "%{buildroot}%{_prefix}/jetty-solr/etc/jetty.xml"
%if "%{_collection_name}" == "collection1"
# no need to rename
%else
sed -i "s|collection1|%{_collection_name}|g" "%{buildroot}/etc/default/jetty"
sed -i "s|collection1|%{_collection_name}|g" "%{buildroot}%{_prefix}/jetty-solr/solr/solr.xml"
%endif

%clean
rm -rf $RPM_BUILD_ROOT



%files
%defattr(-,solr,solr,-)
%attr(0755,solr,solr) %dir %{_prefix}
%attr(0755,solr,solr) %dir %{_logprefix}
%doc
%{_prefix}/contrib
%{_prefix}/dist
%{_prefix}/docs
%{_prefix}/jetty-solr
%{_prefix}/licenses
%{_prefix}/CHANGES.txt
%{_prefix}/LICENSE.txt
%{_prefix}/NOTICE.txt
%{_prefix}/README.txt
%{_prefix}/SYSTEM_REQUIREMENTS.txt
%attr(0755,root,root) /etc/init.d/jetty-solr
%attr(0644,root,root) /etc/default/jetty

%pre
getent group solr >/dev/null || groupadd -r solr
getent passwd solr >/dev/null || \
    useradd -r -g solr -d %{_prefix}/jetty-solr -s /bin/bash \
    -c "Solr User" solr
exit 0

%post
chkconfig --add jetty-solr
echo "Installation complete."

%preun
if [ $1 = 0 ] ; then
   service jetty-solr stop >/dev/null 2>&1 || :
   chkconfig --del jetty-solr
fi

%postun
if [ "$1" -ge "1" ] ; then
   service jetty-solr restart >/dev/null 2>&1 || :
fi

%changelog
* Wed Apr 17 2013 Boogie Shafer <boogieshafer@yahoo.com>
- make collection name configurable
- build using 4.2.1 solr binary release
- change default installation location to /opt/solr
- pull jetty init script and logging configs from jetty 8.x distribution

* Mon Mar 25 2013 Boogie Shafer <boogieshafer@yahoo.com>
- adjust version for 4.2.0 

* Wed Feb 20 2013 Boogie Shafer <boogieshafer@yahoo.com>
- change path to data directory to place it under collection1
- adjust logging settings for solr

* Tue Feb 12 2013 Boogie Shafer <boogieshafer@yahoo.com>
- edits to configure jetty logging

* Tue Jan 29 2013 Boogie Shafer <boogieshafer@yahoo.com>
- edits for 4.1.0 solr using bundled jetty and zookeeper

* Tue Jan 18 2012 Jean-Francois Roche <jfroche@affinitic.be>
- Initial implementation

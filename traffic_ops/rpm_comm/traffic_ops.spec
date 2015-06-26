#
# Copyright 2015 Comcast Cable Communications Management, LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# RPM spec file for Traffic Ops (tm).
#

%define TRAFFIC_OPS_USER trafops
%define TRAFFIC_OPS_GROUP trafops
%define TRAFFIC_OPS_LOG_DIR /var/log/traffic_ops
%define PACKAGE traffic_ops

# %define PACKAGEDIR %{prefix}

Name: %{PACKAGE}
Version: %{traffic_ops_version}
Release: %{traffic_ops_build}%{?dist}
Summary: Traffic Ops UI to control a CDN
Group: Applications/System
License: ASL 2.0
URL: http://traffic-control-cdn.net
# The source for this package was pulled from uptream's vcs. Use the following
# commands to generate the tarball:
# git clone https://github.com/Comcast/traffic_control.git
# cd %_sourcedir
# tar -czf %_sourcedir/traffic_ops-%{traffic_ops_version}-%{traffic_ops_version}.%{hosttype}.tar.gz ./*
Source0: %{PACKAGE}-%{traffic_ops_version}-%{traffic_ops_build}.%{hosttype}.tar.gz
#Patch0:
BuildArch: %{hosttype}

BuildRoot: %{buildroot}

#BuildRequires:

Requires: expat-devel, mod_ssl, mkisofs, libpcap-devel mysql, mysql-server, openssl, perl-DBI, perl-DBD-MySQL, perl-Digest-SHA1, perl-WWW-Curl
Requires(pre): /usr/sbin/useradd, /usr/bin/getent
Requires(postun): /usr/sbin/userdel


%description
Installs %{PACKAGE}.

%build

%prep

%setup

%install
   if [ -d $RPM_BUILD_ROOT ]; then
      %__rm -rf $RPM_BUILD_ROOT
   fi

   if [ ! -d $RPM_BUILD_ROOT/%{PACKAGE} ]; then
      %__mkdir -p $RPM_BUILD_ROOT/%{PACKAGE}
   fi

   %__cp -R $RPM_BUILD_DIR/%{PACKAGE}-%{traffic_ops_version}/* $RPM_BUILD_ROOT/%{PACKAGE}

   if [ ! -d $RPM_BUILD_ROOT/%{PACKAGE}/app/public/CRConfig-Snapshots ]; then
      %__mkdir -p $RPM_BUILD_ROOT/%{PACKAGE}/app/public/CRConfig-Snapshots
   fi
   if [ ! -d $RPM_BUILD_ROOT/%{PACKAGE}/app/public/routing ]; then
      %__mkdir -p $RPM_BUILD_ROOT/%{PACKAGE}/app/public/routing
   fi

%pre
    /usr/bin/getent group %{TRAFFIC_OPS_GROUP} || /usr/sbin/groupadd -r %{TRAFFIC_OPS_GROUP}
    /usr/bin/getent passwd %{TRAFFIC_OPS_USER} || /usr/sbin/useradd -r -d %{PACKAGEDIR} -s /sbin/nologin %{TRAFFIC_OPS_USER} -g %{TRAFFIC_OPS_GROUP}
    if [ -d %{PACKAGEDIR}/app/conf ]; then
      #echo -e "\nBacking up config files.\n"
     if [ -f /var/tmp/traffic_ops-backup.tar ]; then
        %__rm /var/tmp/traffic_ops-backup.tar
     fi
     cd %{PACKAGEDIR} && tar cf /var/tmp/traffic_ops-backup.tar app/public/*Snapshots app/public/routing  app/conf app/db/dbconf.yml app/local app/cpanfile.snapshot
    fi

    # upgrade
    if [ "$1" == "2" ]; then
   service traffic_ops stop
    fi

%post

    %__cp %{PACKAGEDIR}/etc/init.d/traffic_ops /etc/init.d/traffic_ops
     %__cp %{PACKAGEDIR}/etc/logrotate.d/traffic_ops /etc/logrotate.d/traffic_ops
     %__cp %{PACKAGEDIR}/etc/logrotate.d/traffic_ops_access /etc/logrotate.d/traffic_ops_access
    %__chown root:root /etc/init.d/traffic_ops
    %__chown root:root /etc/logrotate.d/traffic_ops
    %__chown root:root /etc/logrotate.d/traffic_ops_access
    %__chmod +x /etc/init.d/traffic_ops
    %__chmod +x %{PACKAGEDIR}/install/bin/*
    /sbin/chkconfig --add traffic_ops 
   
    %__mkdir -p %{TRAFFIC_OPS_LOG_DIR}

    if [ -f /var/tmp/traffic_ops-backup.tar ]; then
      echo -e "\nRestoring config files.\n"
      cd %{PACKAGEDIR} && tar xf /var/tmp/traffic_ops-backup.tar
    fi

    # install
    if [ "$1" = "1" ]; then
      # see postinstall, the .reconfigure file triggers init().
      /bin/touch %{PACKAGEDIR}/.reconfigure
      echo -e "\nRun /opt/traffic_ops/install/bin/postinstall from the root home directory to complete the install.\n"
    fi

    # upgrade
    if [ "$1" == "2" ]; then
          /opt/traffic_ops/install/bin/migratedb
        echo -e "\nUpgrade complete.\n\n"
       echo -e "\nRun /opt/traffic_ops/install/bin/postinstall from the root home directory to complete the update.\n"
        echo -e "To start Traffic Ops:  service traffic_ops start\n";
        echo -e "To stop Traffic Ops:   service traffic_ops stop\n\n";
    fi
    /bin/chown -R %{TRAFFIC_OPS_USER}:%{TRAFFIC_OPS_GROUP} %{PACKAGEDIR}
    /bin/chown -R %{TRAFFIC_OPS_USER}:%{TRAFFIC_OPS_GROUP} %{TRAFFIC_OPS_LOG_DIR}

%postun

if [ "$1" = "0" ]; then
   # this is an uninstall
   %__rm -rf %{PACKAGEDIR}
   %__rm /etc/init.d/traffic_ops
    /usr/bin/getent passwd %{TRAFFIC_OPS_USER} || /usr/sbin/userdel %{TRAFFIC_OPS_USER} 
    /usr/bin/getent group %{TRAFFIC_OPS_GROUP} || /usr/sbin/groupdel %{TRAFFIC_OPS_GROUP}
fi
service traffic_ops stop
#/usr/sbin/groupdel %{TRAFFIC_OPS_GROUP}

%clean

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{PACKAGEDIR}/app/bin/*
%config(noreplace)/opt/traffic_ops/app/conf/*
%{PACKAGEDIR}/install/*
%{PACKAGEDIR}/app/*
%{PACKAGEDIR}/etc/*
%{PACKAGEDIR}/doc/*

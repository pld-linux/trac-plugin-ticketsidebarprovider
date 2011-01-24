%define		trac_ver	0.11
%define		plugin		ticketsidebarprovider
Summary:	Plugin for Trac to add content to the ticket sidebar
Name:		trac-plugin-%{plugin}
Version:	0.0
Release:	1
License:	GPL
Group:		Applications/WWW
Source0:	http://trac-hacks.org/changeset/latest/ticketsidebarproviderplugin?old_path=/&filename=%{plugin}-%{version}&format=zip#/%{plugin}-%{version}.zip
# Source0-md5:	b1c643b7844392b4bc7d79fee010978a
URL:		http://trac-hacks.org/wiki/TicketSidebarProviderPlugin
BuildRequires:	python-devel
BuildRequires:	python-modules
BuildRequires:	python-setuptools
BuildRequires:	rpm-pythonprov
BuildRequires:	sed >= 4.0
BuildRequires:	unzip
Requires:	trac >= %{trac_ver}
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Allows the addition of content to the right of the ticket
(div[@id='content'], by convention).

%prep
%setup -qc
mv ticketsidebarproviderplugin/%{trac_ver}/* .

# do not autoload this
mv ticketsidebarprovider/example.py .
sed -i -e '/from example import SampleTicketSidebarProvider/d' ticketsidebarprovider/__init__.py

%build
%{__python} setup.py build
%{__python} setup.py egg_info

ver=$(awk '$1 == "Version:" {print $2}' *.egg-info/PKG-INFO)
test "$ver" = %{version}

%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install \
	--single-version-externally-managed \
	--optimize 2 \
	--root=$RPM_BUILD_ROOT

%py_postclean

%clean
rm -rf $RPM_BUILD_ROOT

# NOTE: no post registration needed, plugin not used directly

%files
%defattr(644,root,root,755)
%doc example.py
%{py_sitescriptdir}/%{plugin}
%{py_sitescriptdir}/TicketSidebarProvider-*.egg-info

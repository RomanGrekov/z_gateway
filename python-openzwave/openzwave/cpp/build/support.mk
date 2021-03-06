#The Major Version Number
VERSION_MAJ	?= 1
#The Minor Version Number
VERSION_MIN ?= 1

#the build type we are making (release or debug)
BUILD	?= release
#the prefix to install the library into
PREFIX	?= /usr/local


#The Location of the svnversion command for determining the repository version
SVNVERSION := $(shell which svnversion)
#the System we are building on
UNAME  := $(shell uname -s)
#the location of Doxygen to generate our api documentation
DOXYGEN := $(shell which doxygen)
#the machine type we are building on (i686 or x86_64)
MACHINE := $(shell uname -m)
#the location of xmllink for checking our config files
XMLLINT := $(shell which xmllint)
#temp directory to build our tarfile for make dist target
TMP     := /tmp
#pkg-config binary for package config files
PKGCONFIG := $(shell which pkg-config)
#svn binary for doing a make dist export
SVN		:= $(shell which svn)
# if svnversion is not installed, then set the revision to 0
ifeq ($(SVNVERSION),)
VERSION_REV ?= 0
else
VERSION_REV ?= $(shell $(SVNVERSION) $(top_srcdir)|awk -F'[^0-9]*' '$$0=$$1')
endif
ifeq ($(VERSION_REV),)
VERSION_REV ?= 0
endif
# version number to use on the shared library
VERSION := $(VERSION_MAJ).$(VERSION_MIN)

# support Cross Compiling options
CC     := $(CROSS_COMPILE)gcc
CXX    := $(CROSS_COMPILE)g++
LD     := $(CROSS_COMPILE)g++
ifeq ($(UNAME),Darwin)
AR     := libtool -static -o 
RANLIB := ranlib
else
AR     := $(CROSS_COMPILE)ar rc
RANLIB := $(CROSS_COMPILE)ranlib
endif
SED    := sed


#determine if we are release or debug Build and set appropriate flags
ifeq ($(BUILD), release)
CFLAGS	+= -c $(RELEASE_CFLAGS)
LDFLAGS	+= $(RELEASE_LDFLAGS)
else
CFLAGS	+= -c $(DEBUG_CFLAGS)
LDFLAGS	+= $(DEBUG_LDFLAGS)
endif

#if /lib64 exists, then setup x86_64 library path to lib64 (good indication if a linux has /lib and lib64). 
#Else, if it doesnt, then set as /lib. This is used in the make install target 
ifeq ($(wildcard /lib64),)
instlibdir.x86_64 = /lib/
else
instlibdir.x86_64 = /lib64/
endif
instlibdir.default   = /lib/

#our actual install location for the library
ifneq ($(instlibdir.$(MACHINE)),)
instlibdir ?= $(PREFIX)$(instlibdir.$(MACHINE))
else
instlibdir ?= $(PREFIX)$(instlibdir.default)
endif

sysconfdir ?= $(PREFIX)/etc/openzwave/
includedir ?= $(PREFIX)/include/openzwave/
docdir ?= $(PREFIX)/share/doc/openzwave-$(VERSION).$(VERSION_REV)

top_builddir ?= $(CURDIR)
export top_builddir

OBJDIR = $(top_builddir)/.lib
DEPDIR = $(top_builddir)/.dep




$(OBJDIR)/%.o : %.cpp
	@echo "Building $(notdir $@)"
	@$(CXX) $(CFLAGS) $(INCLUDES) -o $@ $<

$(OBJDIR)/%.o : %.c
	@echo "Building $(notdir $@)"	
	@$(CC) $(CFLAGS) $(INCLUDES) -o $@ $<

$(DEPDIR)/%.d : %.cpp
	@set -e; rm -f $@; \
	$(CXX) -MM $(INCLUDES) $< > $@.$$$$; \
	$(SED) 's,\($*\)\.o[ :]*,\1.o $@ : ,g' < $@.$$$$ > $@; \
	rm -f $@.$$$$

$(DEPDIR)/%.d : %.c
	@set -e; rm -f $@; \
	$(CXX) -MM $(INCLUDES) $< > $@.$$$$; \
	$(SED) 's,\($*\)\.o[ :]*,\1.o $@ : ,g' < $@.$$$$ > $@; \
	rm -f $@.$$$$

dummy := $(shell test -d $(OBJDIR) || mkdir -p $(OBJDIR))
dummy := $(shell test -d $(DEPDIR) || mkdir -p $(DEPDIR))

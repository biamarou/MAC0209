SRCDIR 	  := src
CLASSDIR  := class
PWD       := $(shell pwd)

SRC       := $(wildcard $(SRCDIR)/*.java)
CLASS     := $(patsubst $(SRCDIR)/%.java, $(CLASSDIR)/%.class, $(SRC))

CLASSD    := $(wildcard $(PWD)/*.class)
SRCD      := $(wildcard $(PWD)/*.java)

MYCLASSPATH := $(CLASSPATH):./lib/osp.jar
JC        := javac 
MV		  := mv
JCFLAGS   := -d $(CLASSDIR) -cp $(MYCLASSPATH)

.PHONY: compile 
compile: $(CLASS)

$(CLASS): $(SRC) | $(CLASSDIR)
	$(JC) $(JCFLAGS) $^

.PHONY: init
init: $(SRCDIR) $(CLASSDIR)

$(SRCDIR) $(CLASSDIR):
	mkdir -p $@

.PHONY: organize
organize: init
		-$(MV) $(CLASSD) $(CLASSDIR)
		-$(MV) $(SRCD) $(SRCDIR)

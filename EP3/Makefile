SRCDIR 	  := src
CLASSDIR  := class
PWD       := $(shell pwd)

SRC       := $(wildcard $(SRCDIR)/*.java)
CLASS     := $(patsubst $(SRCDIR)/%.java, $(CLASSDIR)/%.class, $(SRC))

CLASSD    := $(wildcard $(PWD)/*.class)
SRCD      := $(wildcard $(PWD)/*.java)

JC        := javac 
MV		  := mv
JCFLAGS   := -d $(CLASSDIR) -cp $(CLASSPATH)

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

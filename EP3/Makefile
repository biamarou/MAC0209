SRCDIR 	  := src
OBJDIR    := obj
PWD       := $(shell pwd)

SRC       := $(wildcard $(SRCDIR)/*.java)
CLASS     := $(patsubst $(SRCDIR)/%.java, $(OBJDIR)/%.class, $(SRC))

CLASSD    := $(wildcard $(PWD)/*.class)
SRCD      := $(wildcard $(PWD)/*.java)

MYCLASSPATH := $(CLASSPATH):./lib/osp.jar
JC        := javac 
MV		  := mv
JCFLAGS   := -d $(OBJDIR) -cp $(MYCLASSPATH)

.PHONY: compile 
compile: $(CLASS)

$(CLASS): $(SRC) | $(OBJDIR)
	$(JC) $(JCFLAGS) $^

.PHONY: init
init: $(SRCDIR) $(OBJDIR)

$(SRCDIR) $(OBJDIR):
	mkdir -p $@

.PHONY: organize
organize: init
		-$(MV) $(CLASSD) $(OBJDIR)
		-$(MV) $(SRCD) $(SRCDIR)

.PHONY: clean
clean:
	rm -rf $(OBJDIR)

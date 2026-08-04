# Re-prepare FEP water spheres at a chosen sphere radius.
#
#   make <radius>                 # all 16 canonical targets
#   make <radius> jacs            # JACS subset (8 targets)
#   make <radius> merck           # Merck subset (8 targets)
#   make <radius> cmet eg5 ...    # explicit targets
#
# REPS sets the setupFEP replicate count (-R); it defaults to 10 (the baseline).
# REPARAM=1 regenerates all ligand/cofactor parameters with qparams. Optional
# QPARAMS_ARGS are passed to every qparams call, including PFKFB3 cofactors.
# Use '-ff openff-2.2.1.offxml -am1bcc' for the settings in the "doing more with less"
# paper or just leave it be, since it's how these parameters were originally generated.
#
# Examples:
#   make 20            make 20 jacs            make 30 cmet
#   make 20 REPS=3     make 20 jacs REPS=3     # 3 replicates for faster turnover
#
# Each run writes perturbations/<target>-<radius>A/ from the 25 A baseline, with
# protein.pdb + water.pdb regenerated at <radius> and the .sh scripts patched so
# the directory is submission-ready. See reprep.py for details.

ENV ?= qligfep_new
REPS ?= 10
OVERWRITE ?= 0
REPARAM ?= 0
QPARAMS_ARGS ?=
FIRST := $(firstword $(MAKECMDGOALS))
OVERWRITE_ARG := $(if $(filter 1 yes true,$(OVERWRITE)),--force,)
REPARAM_ARG := $(if $(filter 1 yes true,$(REPARAM)),\
	--reparameterize --qparams-args "$(QPARAMS_ARGS)",)

.PHONY: help FORCE
help:
	@echo "Usage: make <radius> [jacs|merck|all|<target>...] [REPS=N]"
	@echo "  make 20              # all 16 targets at 20 A, 10 replicates"
	@echo "  make 20 jacs         # JACS subset"
	@echo "  make 30 cmet eg5     # specific targets"
	@echo "  make 20 REPS=3       # 3 replicates instead of 10"
	@echo "  make 20 cmet REPARAM=1  # regenerate ligand parameters"
	@echo "  make 20 pfkfb3 REPARAM=1 QPARAMS_ARGS='-ff openff-2.2.1.offxml -am1bcc'"
	@echo "  make 20 cmet OVERWRITE=1  # replace an existing unsubmitted variant"

# Numeric radius and subset words all arrive as goals; funnel them to the driver
# once (on the first goal) and hand it the full goal list to parse. The FORCE
# prerequisite stops make from treating a goal that matches an existing target
# directory (e.g. `cmet`) as "up to date" and skipping the recipe.
%: FORCE
	@if [ "$@" = "$(FIRST)" ]; then \
		micromamba run -n "$(ENV)" python "$(CURDIR)/reprep.py" \
			$(MAKECMDGOALS) --reps "$(REPS)" $(OVERWRITE_ARG) $(REPARAM_ARG); \
	fi

FORCE:

override KERNEL_SRC := $(patsubst kernel/platform/kernel-$(TARGET_KERNEL_VERSION)/%,%,$(TARGET_KERNEL_SOURCE))

# Native header generation needs a source-root prefix for relative output paths.
ifeq ($(filter /%,$(OUT_DIR)),)
override KERNEL_BUILD_OUT_PREFIX := $(abspath .)/
endif

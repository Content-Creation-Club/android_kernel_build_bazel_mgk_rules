ifneq ($(strip $(BOOT_KERNEL_MODULES)),)
mgk_android_path := $(call my-dir)
mgk_depmod := $(TARGET_OUT_INTERMEDIATES)/KERNEL_TOOLS/depmod

$(mgk_depmod): PRIVATE_CHECKER := $(abspath $(mgk_android_path))/depmod.py
$(mgk_depmod): $(mgk_android_path)/depmod.py $(HOST_OUT_EXECUTABLES)/depmod
	@mkdir -p $(dir $@)
	$(hide) printf '%s\n' '#!/bin/sh' \
	    'exec python3 "$(PRIVATE_CHECKER)" --depmod "$(abspath $(HOST_OUT_EXECUTABLES))/depmod" --stage "$(abspath $(KERNEL_DEPMOD_STAGING_DIR))" --preloaded "$(abspath $(KERNEL_VENDOR_RAMDISK_MODULES_OUT))/lib/modules" -- "$$@"' > $@
	$(hide) chmod +x $@

DEPMOD := $(mgk_depmod)
endif

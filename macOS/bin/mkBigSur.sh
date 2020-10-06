#!/usr/bin/env bash
#
# Create bootable installation media from macOS Big Sur and install a new
# Virtualbox VM. 
#
# Usage: `basename $0` <name_of_vm>
#
# Info: After code completes disable networking on the machine in order to
# complete the install. Afterward, you may enable networking.
#
# Author: Justin Cook <jhcook@secnix.com>

set -o errexit
set -o errtrace
set -o nounset

VM_NAME="$1"

VBOXMANAGE="/usr/local/bin/VBoxManage"
VM_BASE_FL="${HOME}/VirtualBox VMs/${VM_NAME}"

CREATEINSM="/Applications/Install macOS Big Sur Beta.app/Contents/Resources/createinstallmedia"

trap on_exit err SIGINT

function on_exit {
  sudo rm -f /var/tmp/BigSur* || /usr/bin/true
  "${VBOXMANAGE}" unregistervm "${VM_NAME}" || /usr/bin/true
  rm -fr "${VM_BASE_FL}"
}

# https://www.wikigain.com/create-macos-big-sur-iso-image/
function create_image {

  # Create an empty disk image
  sudo /usr/bin/hdiutil create -o /var/tmp/BigSur -size 16384m \
  -volname BigSur -layout SPUD -fs HFS+J

  # Mount the disk image to /Volumes/BigSur
  sudo /usr/bin/hdiutil attach /var/tmp/BigSur.dmg -noverify \
  -mountpoint /Volumes/BigSur

  # Make the disk image bootable
  sudo "${CREATEINSM}" --volume /Volumes/BigSur --nointeraction

  # Unmount the Disk Image
  /usr/bin/hdiutil eject -force /Volumes/Install\ macOS\ Big\ Sur\ Beta

  # Convert and rename the Disk Image to ISO
  /usr/bin/hdiutil convert /var/tmp/BigSur.dmg -format UDTO -o /var/tmp/BigSur
  test -f /var/tmp/BigSur.iso && sudo rm /var/tmp/BigSur.iso
  #chflags -f nouchg /var/tmp/BigSur.cdr
  sudo mv -v /var/tmp/BigSur.cdr /var/tmp/BigSur.iso
  sudo rm -fv /var/tmp/BigSur.dmg
}

function create_vm {

  # Create VM
  ${VBOXMANAGE} createvm --name "${VM_NAME}" \
  --ostype "MacOS_64" --register --basefolder "${VM_BASE_FL}"

  # Settings that will work with keyboard and mouse
  ${VBOXMANAGE} modifyvm "${VM_NAME}" \
  --memory 16384 \
  --vram 128 \
  --acpi on \
  --ioapic on \
  --cpus 2 \
  --firmware efi64 \
  --mouse usbtablet \
  --chipset ich9 \
  --usbehci on \
  --keyboard usb

  # Create SATA Controller/disk and attach
  ${VBOXMANAGE} createhd --filename "${VM_BASE_FL}/${VM_NAME}.vdi" \
  --size 128000 --format VDI
  ${VBOXMANAGE} storagectl "${VM_NAME}" --name "SATA Controller" \
  --add sata --controller IntelAhci 
  ${VBOXMANAGE} storageattach "${VM_NAME}" --storagectl "SATA Controller" \
  --port 0 --device 0 --type hdd --medium "${VM_BASE_FL}/${VM_NAME}.vdi"
  ${VBOXMANAGE} storageattach "${VM_NAME}" --storagectl "SATA Controller" \
  --port 1 --device 0 --type dvddrive --medium "/var/tmp/BigSur.iso"

  # https://www.wikigain.com/how-to-install-macos-big-sur-on-virtualbox-on-windows-pc/

  ${VBOXMANAGE} modifyvm "${VM_NAME}" \
  --cpuidset 00000001 000106e5 00100800 0098e3fd bfebfbff
  ${VBOXMANAGE} setextradata "${VM_NAME}" \
  "VBoxInternal/Devices/efi/0/Config/DmiSystemProduct" "iMac19,1"
  ${VBOXMANAGE} setextradata "${VM_NAME}" \
  "VBoxInternal/Devices/efi/0/Config/DmiSystemVersion" "1.0"
  ${VBOXMANAGE} setextradata "${VM_NAME}" \
  "VBoxInternal/Devices/efi/0/Config/DmiBoardProduct" "Mac-AA95B1DDAB278B95"
  ${VBOXMANAGE} setextradata "${VM_NAME}" \
  "VBoxInternal/Devices/smc/0/Config/DeviceKey" \
  "ourhardworkbythesewordsguardedpleasedontsteal(c)AppleComputerInc"
  ${VBOXMANAGE} setextradata "${VM_NAME}" \
  "VBoxInternal/Devices/smc/0/Config/GetKeyFromRealSMC" 1
}

sudo whoami >/dev/null 2>&1

if [ ! -f /var/tmp/BigSur.iso ]
then
  create_image
fi

create_vm

# Start VM
${VBOXMANAGE} startvm "${VM_NAME}" --type headless

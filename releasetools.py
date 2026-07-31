#
# Copyright (C) 2022 The LineageOS Project
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import common
import re

def FullOTA_InstallEnd(info):
  OTA_InstallEnd(info)
  return

def IncrementalOTA_InstallEnd(info):
  OTA_InstallEnd(info)
  return

def AddImage(info, basename, dest):
  name = basename
  data = info.input_zip.read("IMAGES/" + basename)
  common.ZipWriteStr(info.output_zip, name, data)
  info.script.AppendExtra('package_extract_file("%s", "%s");' % (name, dest))

def AddImageRadio(info, basename, *dests):
  name = basename
  if ("RADIO/" + basename) in info.input_zip.namelist():
    data = info.input_zip.read("RADIO/" + basename)
    common.ZipWriteStr(info.output_zip, name, data)
    for dest in dests:
      info.script.Print("Patching {} image unconditionally...".format(dest.split('/')[-1]))
      info.script.AppendExtra('package_extract_file("%s", "%s");' % (name, dest))

def SetEmmcWritable(info, path):
  info.script.AppendExtra(
      'assert(run_program("/sbin/sh", "-c", "echo 0 > %s") == 0);' % path
  )

def OTA_InstallEnd(info):
  info.script.Print("Patching firmware images...")
  AddImage(info, "vbmeta.img", "/dev/block/by-name/vbmeta")
  AddImage(info, "vbmeta_system.img", "/dev/block/by-name/vbmeta_system")
  AddImage(info, "vbmeta_vendor.img", "/dev/block/by-name/vbmeta_vendor")
  AddImage(info, "dtbo.img", "/dev/block/by-name/dtbo")

  AddImageRadio(info, "lk.img", "/dev/block/by-name/lk", "/dev/block/by-name/lk2")
  AddImageRadio(info, "logo.img", "/dev/block/by-name/logo")
  AddImageRadio(info, "md1img.img", "/dev/block/by-name/md1img")

  SetEmmcWritable(info, "/sys/block/mmcblk0boot0/force_ro")
  SetEmmcWritable(info, "/sys/block/mmcblk0boot1/force_ro")
  AddImageRadio(info, "preloader_emmc.img", "/dev/block/by-name/mmcblk0boot0", "/dev/block/by-name/mmcblk0boot1")
  AddImageRadio(info, "scp.img", "/dev/block/by-name/scp1", "/dev/block/by-name/scp2")
  AddImageRadio(info, "spmfw.img", "/dev/block/by-name/spmfw")
  AddImageRadio(info, "sspm.img", "/dev/block/by-name/sspm_1", "/dev/block/by-name/sspm_2")
  AddImageRadio(info, "tee.img", "/dev/block/by-name/tee1", "/dev/block/by-name/tee2")
  return

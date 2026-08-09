#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
改造 20：移除「附庸边境压制」（Magister Modmod for FfH2 / CvGameCoreDLL.dll 二进制补丁）

原理
----
CvPlot::calculateCulturalOwner() 在判定非城市地块归属时，会把「文化最高玩家」所臣服
的宗主队伍的城市也放进候选名单，并给自家城市 +5 优先级惩罚（BtS 原版逻辑，MNAI/MM
原样继承），结果是附庸靠近宗主城市的地块被宗主吞并。

本补丁把「队伍不同 → 去查 isVassal」这条支路直接改成「队伍不同 → 跳过这座城」，
等价于原版中根本没有这条附庸规则。后面的 add eax,5 因此只会对同队城市统一生效，
相对顺序不变，自动失效。

补丁点（文件偏移 = RVA，因为 .text 的 VirtualAddress 与 PointerToRawData 均为 0x1000）
------------------------------------------------------------------------------
  0x00207FFE   8B 0D 28 68 55 10   mov ecx, dword ptr [0x10556828]   ; GET_TEAM(...)
        ↓
  0x00207FFE   EB 67 90 90 90 90   jmp 0x10208067 ; + 4×nop         ; 直接 continue

目标文件
--------
  <MM>\Assets\CvGameCoreDLL.dll
  原版 sha256 04eeb7bba7ca81ecbce2e4c0a92dbb44804db2271401b7fe2cffcf9e5686e21e (6,111,232 B)
  补丁 sha256 866597a31cf23c18944ca4df07010b960579fa51dc395ef918bad71c9a306876 (6,111,232 B)

用法
----
  python patch_vassal_border.py <原版DLL> <输出DLL>        # 打补丁
  python patch_vassal_border.py --revert <补丁DLL> <输出>  # 还原
"""
import sys, hashlib

OFF = 0x207FFE
ORIG = bytes.fromhex('8b0d28685510')
NEW = bytes.fromhex('eb6790909090')
SHA_ORIG = '04eeb7bba7ca81ecbce2e4c0a92dbb44804db2271401b7fe2cffcf9e5686e21e'
SHA_NEW = '866597a31cf23c18944ca4df07010b960579fa51dc395ef918bad71c9a306876'


def main(argv):
    revert = '--revert' in argv
    argv = [a for a in argv if a != '--revert']
    if len(argv) != 3:
        print(__doc__)
        return 1
    src, dst = argv[1], argv[2]
    data = bytearray(open(src, 'rb').read())
    have, want, put = bytes(data[OFF:OFF + 6]), (NEW if revert else ORIG), (ORIG if revert else NEW)
    if have != want:
        print('ABORT: 偏移 0x%06X 处不是预期字节。期望 %s，实际 %s' % (OFF, want.hex(), have.hex()))
        print('       这个 DLL 可能不是 MM 那一版，或已经被改过。')
        return 2
    data[OFF:OFF + 6] = put
    open(dst, 'wb').write(data)
    sha = hashlib.sha256(bytes(data)).hexdigest()
    print('写出 %s（%d 字节）' % (dst, len(data)))
    print('sha256 %s  %s' % (sha, '✓' if sha == (SHA_ORIG if revert else SHA_NEW) else '⚠ 与预期不符'))
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))

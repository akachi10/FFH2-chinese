# Rampage 静态验证

## 定位与边界

本页提供从仓库根目录可执行的只读检查。命令面向 zsh/bash；除临时目录外不写项目文件。

最重要的边界：**XML well-formed 只证明 XML 语法可解析，不证明 Schema 语义、Type/资源引用完整、DLL/XML/Python 一致、游戏能加载或玩法正确。** Rampage 是覆盖包，仓库中缺少的引用可能由外部 FFH2 基线提供；必须在合并后的 Windows staging 再验证。

这些命令是检查方法，不记录本次结果。结果进入[环境状态](../ops/status.md)或专门执行报告。

## 0. 执行前提

```bash
cd /absolute/path/to/ffh2-mods-ba
git rev-parse --show-toplevel
git rev-parse HEAD
command -v rg xmllint file shasum perl ruby
```

记录输出和退出码。若仓库根目录、提交或工具不明确，停止后续结论。

## 1. 仓库与文件清单

```bash
git status --short
find Rampage/Assets/XML -type f -name '*.xml' | LC_ALL=C sort
find Rampage/Assets/python -type f -name '*.py' | LC_ALL=C sort
find Rampage/Assets/src/CvGameCoreDLL.041o -type f | LC_ALL=C sort
```

证明：检查对象、未提交文件和各层输入可枚举。限制：文件存在不代表由游戏加载；`Rampage` 是仓库重点而非用户机器运行态证明。

## 2. XML well-formed

```bash
find Rampage/Assets/XML -type f -name '*.xml' -print0 \
  | xargs -0 xmllint --noout
```

退出码为 0 只说明这些文件分别 well-formed。它不执行 Civ4 的 XDR Schema 语义验证，不检查 XML Type、文本键、资源路径、枚举顺序，也不验证外部基线文件。

如需对历史代码线做同类比较，逐目录执行并分别记录，禁止把四条代码线的总结果当作 Rampage 结果。

## 3. Schema 引用盘点

```bash
tmpdir=$(mktemp -d)
trap 'rm -rf "$tmpdir"' EXIT

rg -o 'x-schema:[^"[:space:]]+' Rampage/Assets/XML \
  | sed 's/.*x-schema://' \
  | LC_ALL=C sort -u > "$tmpdir/schema-referenced.txt"

find Rampage/Assets/XML -type f -name '*.xml' -exec basename {} \; \
  | LC_ALL=C sort -u > "$tmpdir/xml-basenames.txt"

comm -23 "$tmpdir/schema-referenced.txt" "$tmpdir/xml-basenames.txt"
```

输出是“覆盖包中没有同名文件的 Schema 引用”候选清单。它是合并基线核对输入，不是自动 FAIL。每项应在 Windows 合并目标中定位，并确认文件版本与对应数据匹配。

## 4. UnitClass → Unit Type 定向审计

```bash
tmpdir=$(mktemp -d)
trap 'rm -rf "$tmpdir"' EXIT

perl -0777 -ne '
  while (m{<UnitInfo\b.*?</UnitInfo>}sg) {
    $b=$&;
    print "$1\n" if $b =~ m{<Type>\s*([^<]+?)\s*</Type>}s;
  }
' Rampage/Assets/XML/Units/CIV4UnitInfos.xml \
  | LC_ALL=C sort -u > "$tmpdir/unit-types.txt"

perl -0777 -ne '
  while (m{<DefaultUnit>\s*([^<]+?)\s*</DefaultUnit>}sg) {
    $v=$1; $v =~ s/^\s+|\s+$//g; print "$v\n";
  }
' Rampage/Assets/XML/Units/CIV4UnitClassInfos.xml \
  | LC_ALL=C sort -u > "$tmpdir/default-unit-refs.txt"

comm -23 "$tmpdir/default-unit-refs.txt" "$tmpdir/unit-types.txt"
```

证明：列出 Rampage 覆盖包内 `DefaultUnit` 无本地 `UnitInfo` 定义的候选。限制：外部 FFH2 基线可能提供这些 Type；还需检查空白字符、模块化 XML、`NONE` 等约定和产品可达性。该模式应按变更面扩展到 UnitClass、BuildingClass、Promotion、Spell、Text key 等引用，不能声称一个脚本覆盖所有 Civ4 XML 关系。

## 5. 跨层名称契约

先从变更定义一个受审标识集合，再查生产方和消费者。示例：

```bash
for id in COMMERCE_FOOD combatLogCalc combatLogHit combatLogMiss; do
  echo "=== $id ==="
  rg -n --fixed-strings "$id" \
    Rampage/Assets/XML \
    Rampage/Assets/src/CvGameCoreDLL.041o \
    Rampage/Assets/python || true
done

rg -n \
  -e '^#define PY.*Module' \
  -e 'callFunction\(' \
  Rampage/Assets/src/CvGameCoreDLL.041o/CvDefines.h \
  Rampage/Assets/src/CvGameCoreDLL.041o/CvDllPythonEvents.cpp
```

逐项人工核对；固定字段、方法、事件和 UI 入口的索引见[跨层接口契约](../api/README.md)：

- XML 字段名、顺序与 `CvInfos` 读取一致。
- C++ enum、Cy* 暴露和 Python enum 的标识/序号一致。
- 宿主/C++ 模块名、函数名、事件标签、参数顺序与 Python 消费方一致。
- C++/Python 引用的文本键存在，格式化参数数量和顺序一致。
- XML/Python 资源路径在合并目标存在并可被宿主识别。

`rg` 只能证明字符串出现或未出现，不能证明语义、参数形状、枚举数值或运行可达性。

## 6. Python 2.4 兼容面与导入盘点

```bash
rg -n '^[[:blank:]]*(from[[:blank:]]+[^[:blank:]]+[[:blank:]]+import|import[[:blank:]]+)' \
  Rampage/Assets/python

rg -n \
  -e '^[[:blank:]]*print[[:blank:]]+[^()]' \
  -e '\.has_key\(' \
  -e '\bxrange\(' \
  -e 'except[[:blank:]]+[^:]+,[[:blank:]]*[A-Za-z_][A-Za-z0-9_]*[[:blank:]]*:' \
  -e '<>' \
  Rampage/Assets/python
```

第一条用于把导入分类为覆盖包本地、BtS/FFH2 基线、嵌入式 `CvPythonExtensions` 或未知；第二条盘点 Python 2 语法/惯用法，避免误用现代解释器。

**不得把 `python3 -m py_compile` 作为门禁。** Python 3 对合法的 Python 2.4 代码报错，只能证明代码不兼容 Python 3。若有匹配的 Python 2.4 环境，可做语法编译；宿主专有模块的导入闭包和回调仍必须在游戏内验证。

## 7. 高风险状态与边界源码审计

以下检查用于确认需要 Windows 定向场景的源码结构。零匹配或变量未被后续消费只能标记为静态候选风险，不能证明当前加载 DLL 已出现对应行为。

```bash
src=Rampage/Assets/src/CvGameCoreDLL.041o

rg -n \
  -e 'm_iFood' \
  -e 'm_iFoodPerTurn' \
  -e '^void CvPlayer::(read|write)' \
  "$src/CvPlayer.h" "$src/CvPlayer.cpp" \
  "$src/CyPlayer.cpp" "$src/CyPlayerInterface1.cpp"

sed -n '/^void CvPlayer::read/,/^void CvPlayer::write/p' "$src/CvPlayer.cpp" \
  | rg -n 'm_iFood|m_iFoodPerTurn' || true
sed -n '/^void CvPlayer::write/,/^void CvPlayer::createGreatPeople/p' "$src/CvPlayer.cpp" \
  | rg -n 'm_iFood|m_iFoodPerTurn' || true

sed -n '3449,3572p' "$src/CvUnit.cpp" \
  | rg -n 'iActualUnitWithCargo|iLandUnitCost|iFlyingUnitCost'
sed -n '1834,1870p' "$src/CvCity.cpp"
sed -n '1790,2000p' "$src/CvUnit.cpp" \
  | rg -n 'iDefenderAttackCount|iAttackerAttackCount|changeDamage|isDead'
```

当前源码的判读重点：

- `m_iFood`、`m_iFoodPerTurn` 在 `CvPlayer::read/write` 范围内没有匹配；`m_iFoodPerTurn` 只见归零、读取和只读桥接，未见 setter、change 或其他赋值入口。候选风险是存读档保留与非零修正来源未知，不是已经证明读档归零。
- `iActualUnitWithCargo` 在累计运输者与可防守货物成本后未被后续容量判断读取。候选风险是货物可能未增加容量占用，不是已经证明可超容进入。
- `CvCity::canTrain` 的候选 `UnitPlotCost` 只参与非零判断，现有占用比较未显式加上候选成本。候选风险是临界训练可能放行，不是已经证明完成后超容。
- `CvUnit::resolveCombat` 在同一循环中先执行防守方掷骰、再执行攻击方掷骰，最后检查双方死亡。候选风险是先被致死的攻击方可能仍反击，不是已经证明日志或伤害实际发生。

符号位置与运行场景分别对照[跨层接口契约](../api/README.md)和[运行验收指南](./runtime-acceptance.md)。

## 8. DLL 与构建元数据

```bash
file Rampage/Assets/CvGameCoreDLL.dll
shasum -a 256 Rampage/Assets/CvGameCoreDLL.dll

rg -n \
  -e '^(TOOLKIT|PSDK|CIVINSTALL|GLOBALBOOST|GLOBALPYTHON|YOURMOD)[[:space:]]*=' \
  -e '^(Debug|Release)(:|_)' \
  Rampage/Assets/src/CvGameCoreDLL.041o/Makefile

rg -n --fixed-strings 'CvGameCoreDLL.vcxproj' \
  Rampage/Assets/src/CvGameCoreDLL.041o/CvGameCoreDLL.sln

for f in \
  Rampage/Assets/src/CvGameCoreDLL.041o/CvGameCoreDLL.vcproj \
  Rampage/Assets/src/CvGameCoreDLL.041o/CvGameCoreDLL.vcxproj; do
  if test -e "$f"; then echo "PRESENT $f"; else echo "ABSENT $f"; fi
done
```

证明：二进制格式/身份和声明构建入口可盘点。限制：PE32、哈希稳定或 Makefile 可读均不证明 ABI 兼容、源码同源、链接成功或游戏已加载该 DLL。

Windows 构建必须另存 `cl.exe`、`link.exe`、`rc.exe`、`nmake` 版本和完整 clean Debug/Release 日志；命令见[运行验收指南](./runtime-acceptance.md)与[服务生命周期](../ops/services.md)。

## 9. 覆盖脚本与资源风险

```bash
nl -ba Rampage/installpatch.bat
rg -n -i \
  -e 'xcopy|copy|streak2|yourmod|civinstall|mod=' \
  Rampage/installpatch.bat \
  Rampage/Assets/src/CvGameCoreDLL.041o/Makefile \
  Rampage/Assets/src/CvGameCoreDLL.041o/*.user

rg -n -i '\.(tga|dds|nif|kfm|wav|mp3)(</[^>]+>|["[:space:]])' \
  Rampage/Assets/XML Rampage/Assets/python Rampage/Assets/res
```

这些命令暴露相对目标、历史机器名和资源引用候选。资源引用需规范化路径后在“完整基线 + 覆盖包”的 staging 中检查；覆盖包本地缺失不自动判失败，大小写匹配也不能替代 Civ4 资源装载验证。

## 10. Markdown 相对链接

```bash
ruby -e '
bad = []
["README.md", *Dir["docs/**/*.md"]].each do |file|
  File.read(file).scan(/\[[^\]]*\]\(([^)]+)\)/).flatten.each do |target|
    next if target =~ %r{\A(?:https?://|mailto:|#)}
    path = target.sub(/#.*\z/, "")
    next if path.empty?
    resolved = File.expand_path(path, File.dirname(file))
    bad << "#{file}: #{target}" unless File.exist?(resolved)
  end
end
puts bad
exit(bad.empty? ? 0 : 1)
'
```

证明：根 `README.md` 与 `docs/**/*.md` 中的普通相对 Markdown 文件链接指向现存路径。限制：不验证锚点、渲染器差异、动态链接或文档内容正确性。

## 静态层退出条件

- 所有预期 XML 均完成 well-formed 检查，失败文件有原始错误证据。
- 受变更影响的 Schema、Type、枚举、模块/函数、事件、文本和资源引用均有双向核对记录。
- 每个“覆盖包内缺失”已分类为合并基线依赖或未解决风险；未经合并目标验证不得升级为运行结论。
- DLL、源码提交、构建元数据和部署输入身份已记录。
- 任何结论都明确写出不能由静态层证明的上层事项。

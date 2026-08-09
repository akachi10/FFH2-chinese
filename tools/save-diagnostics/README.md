# Civ4 坏单位内存扫描器

用途、配置、完整流程和修复限制见 `docs/ops/save-load-diagnostics.md`。

只读扫描：

```powershell
python tools\save-diagnostics\scan_civ4_units.py --pid <PID>
```

工具默认读取同目录 `config.json`，选择配置日志目录中最新的 `save-load-*.log`，并把 JSON 报告写入配置的报告目录。

除非已经备份存档并用日志确认唯一的 `owner + unit ID`，不要使用 `--repair-type`。修复模式必须同时传入 `--repair-owner` 和 `--repair-id`，且只负责把坏对象临时恢复为可删除状态。

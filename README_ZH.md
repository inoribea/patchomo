# Patchomo

简体中文 | [English](README.md)

> NetPatch Firewall Groups → Clash 规则集转换器

自动抓取 [NetPatch Firewall](https://github.com/netpatch/groups_for_netpatch_firewall) 分组规则，转换为 Clash rule-provider 格式，每日自动更新。

## ⚠️ 免责声明

> [!CAUTION]
> **禁止违规传播**
> 
> 禁止任何形式的转载或发布至 🇨🇳 中国大陆境内的任何公共平台。

> [!WARNING]
> **合规使用警告**
> 
> 本项目仅供技术交流与学习，中国大陆用户请严格遵守《中华人民共和国网络安全法》及相关法律法规。

## 功能特性

- 🔄 **每日自动更新** - GitHub Actions 每日 UTC 00:00 自动运行
- 📦 **Release 发布** - 从 [Releases](https://github.com/inoribea/patchomo/releases) 下载即用规则集
- 🌍 **200+ 国家 IP** - 完整的国家/地区 IP 规则集
- 🛡️ **广告过滤** - 内置广告/恶意软件/追踪域名规则

## 快速开始

### 下载规则集

访问 [Releases](https://github.com/inoribea/patchomo/releases) 下载最新版本：
- `rulesets-YYYY-MM-DD.tar.gz` - Tarball 压缩包
- `rulesets-YYYY-MM-DD.zip` - ZIP 压缩包

### 在 Clash 中使用

解压后在 Clash 配置中引用：

```yaml
rule-providers:
  amt:
    type: file
    behavior: classical
    path: ./ruleset/amt.yaml

  bdc:
    type: file
    behavior: classical
    path: ./ruleset/bdc.yaml

  CN:
    type: file
    behavior: classical
    path: ./ruleset/CN.yaml

rules:
  - RULE-SET,amt,REJECT
  - RULE-SET,bdc,PROXY
  - RULE-SET,CN,DIRECT
  - MATCH,PROXY
```

## 可用规则集

### 域名规则集

| 规则集 | 说明 | 来源 |
|--------|------|------|
| `amt.yaml` | 广告/恶意软件/追踪域名 | amt.txt |
| `bdc.yaml` | Bypass Domain Categories | bdc.txt |

### 国家 IP 规则集

所有国家/地区代码均可用（200+）：
- `CN.yaml` - 中国
- `US.yaml` - 美国
- `JP.yaml` - 日本
- `HK.yaml` - 香港
- `TW.yaml` - 台湾
- `SG.yaml` - 新加坡
- ... 等

## 数据来源

- **域名列表**: [NetPatch Firewall Groups](https://github.com/netpatch/groups_for_netpatch_firewall)
- **国家 IP**: RIR 数据库 (RIPE, APNIC, ARIN, LACNIC, AFRINIC)

## 项目结构

```
patchomo/
├── scripts/
│   └── convert.py          # 转换脚本
├── .github/
│   └── workflows/
│       └── update.yml      # 每日更新工作流
└── README.md
```

注意：`output/` 目录由 GitHub Actions 自动生成，通过 Releases 分发。

## 本地运行

```bash
git clone https://github.com/inoribea/patchomo.git
cd patchomo
python scripts/convert.py
```

## 更新频率

- **自动更新**: 每日 UTC 00:00
- **手动触发**: GitHub Actions → "Run workflow"

## 许可证

- 数据：遵循 [NetPatch Firewall Groups](https://github.com/netpatch/groups_for_netpatch_firewall) 原始许可证
- 脚本：MIT 许可证

## 致谢

- [NetPatch](https://github.com/netpatch) - 原始数据源
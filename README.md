# Patchomo

> NetPatch Firewall Groups → Clash Rule Provider Converter

自动抓取 [NetPatch Firewall](https://github.com/netpatch/groups_for_netpatch_firewall) 分组规则，并定期转换为 Clash 规则集格式。

## ⚠️ 免责声明

> [!CAUTION]
> **禁止违规传播**
> 
> 禁止任何形式的转载或发布至 🇨🇳 中国大陆境内的任何公共平台。
> <br>Any form of reprinting or posting to the 🇨🇳 mainland platform is prohibited.

> [!WARNING]
> **合规使用警告**
> 
> 本项目仅供技术交流与学习，中国大陆用户请严格遵守《中华人民共和国网络安全法》及相关法律法规。
> <br>Mainland China users please abide by the laws and regulations of your country.

## 功能特性

- 🔄 **自动更新** - GitHub Actions 每日自动同步
- 📦 **双格式输出** - YAML ruleset + 经典文本格式
- 🌍 **国家 IP 规则** - 支持所有国家/地区 IP 段
- 🛡️ **广告/恶意软件域名** - amt.txt + bdc.txt 转换

## 使用方法

### 在 Clash 配置中引用

```yaml
rule-providers:
  amt:
    type: http
    behavior: classical
    url: "https://raw.githubusercontent.com/YOUR_USERNAME/patchomo/main/output/ruleset/amt.yaml"
    path: ./ruleset/amt.yaml
    interval: 86400

  bdc:
    type: http
    behavior: classical
    url: "https://raw.githubusercontent.com/YOUR_USERNAME/patchomo/main/output/ruleset/bdc.yaml"
    path: ./ruleset/bdc.yaml
    interval: 86400

  # 国家 IP 规则示例
  CN:
    type: http
    behavior: classical
    url: "https://raw.githubusercontent.com/YOUR_USERNAME/patchomo/main/output/ruleset/CN.yaml"
    path: ./ruleset/CN.yaml
    interval: 86400

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

所有国家/地区代码均可用，如：
- `CN.yaml` - 中国大陆 IP
- `US.yaml` - 美国 IP
- `JP.yaml` - 日本 IP
- `HK.yaml` - 香港 IP
- ... 等 200+ 国家/地区

完整列表见 [output/INDEX.md](output/INDEX.md)

## 数据来源

- **域名列表**: [netpatch/groups_for_netpatch_firewall](https://github.com/netpatch/groups_for_netpatch_firewall)
  - `amt.txt` - Ad/Malware/Tracking domains
  - `bdc.txt` - Bypass Domain Categories
- **国家 IP**: RIR 数据 (RIPE, APNIC, ARIN, LACNIC, AFRINIC)

## 项目结构

```
patchomo/
├── scripts/
│   └── convert.py          # 转换脚本
├── output/                  # 输出目录
│   ├── ruleset/            # YAML 规则集
│   ├── classic/            # 经典文本格式
│   └── INDEX.md           # 规则集索引
├── .github/
│   └── workflows/
│       └── update.yml      # 自动更新工作流
└── README.md
```

## 本地运行

```bash
# 克隆仓库
git clone https://github.com/YOUR_USERNAME/patchomo.git
cd patchomo

# 运行转换脚本
python scripts/convert.py

# 输出在 output/ 目录
```

## 更新频率

- **自动更新**: 每日 UTC 00:00
- **手动触发**: GitHub Actions → "Update Rulesets" → "Run workflow"
- **源数据更新**: 随上游仓库同步

## 许可证

本项目数据来源于 [NetPatch Firewall Groups](https://github.com/netpatch/groups_for_netpatch_firewall)，遵循其原始许可证。

转换脚本采用 MIT 许可证。

## 致谢

- [NetPatch](https://github.com/netpatch) - 原始数据源
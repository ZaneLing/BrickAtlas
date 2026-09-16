## D3 双叶运河开启桥

### 模块识别（h3-bascule-canal-gate-identify）

高亮的维修模块对应哪个 ID？

能力：模块识别；形式：single-choice；证据：model-state。

- A：drive-cartridge
- B：quay
- C：tower-left
- D：tower-right

```json
{
  "input": {
    "moduleNames": [
      {
        "id": "quay",
        "name": "Canal quay and foundations"
      },
      {
        "id": "tower-left",
        "name": "West bridge tower"
      },
      {
        "id": "tower-right",
        "name": "East bridge tower"
      },
      {
        "id": "west-deck",
        "name": "West bascule deck"
      },
      {
        "id": "east-deck",
        "name": "East bascule deck"
      },
      {
        "id": "drive-cartridge",
        "name": "Bascule drive cartridge"
      }
    ]
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 部件计数（h3-bascule-canal-gate-count）

模块 drive-cartridge 有多少个可视零件？

能力：部件计数；形式：single-choice；证据：model-state。

- A：2
- B：3
- C：1
- D：5

```json
{
  "input": {
    "parts": [
      {
        "id": "v0001",
        "moduleId": "quay",
        "shape": "plate",
        "color": "#c9aa7a"
      },
      {
        "id": "v0002",
        "moduleId": "quay",
        "shape": "plate",
        "color": "#c9aa7a"
      },
      {
        "id": "v0003",
        "moduleId": "quay",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "v0004",
        "moduleId": "quay",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "v0005",
        "moduleId": "quay",
        "shape": "plate",
        "color": "#c9aa7a"
      },
      {
        "id": "v0006",
        "moduleId": "quay",
        "shape": "plate",
        "color": "#c9aa7a"
      },
      {
        "id": "v0007",
        "moduleId": "quay",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "v0008",
        "moduleId": "quay",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "v0009",
        "moduleId": "quay",
        "shape": "plate",
        "color": "#c9aa7a"
      },
      {
        "id": "v0010",
        "moduleId": "quay",
        "shape": "plate",
        "color": "#c9aa7a"
      },
      {
        "id": "v0011",
        "moduleId": "quay",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "v0012",
        "moduleId": "quay",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "v0013",
        "moduleId": "quay",
        "shape": "plate",
        "color": "#c9aa7a"
      },
      {
        "id": "v0014",
        "moduleId": "quay",
        "shape": "plate",
        "color": "#c9aa7a"
      },
      {
        "id": "v0015",
        "moduleId": "quay",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "v0016",
        "moduleId": "quay",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "v0017",
        "moduleId": "quay",
        "shape": "plate",
        "color": "#c9aa7a"
      },
      {
        "id": "v0018",
        "moduleId": "quay",
        "shape": "plate",
        "color": "#c9aa7a"
      },
      {
        "id": "v0019",
        "moduleId": "quay",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "v0020",
        "moduleId": "quay",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "v0021",
        "moduleId": "quay",
        "shape": "plate",
        "color": "#c9aa7a"
      },
      {
        "id": "v0022",
        "moduleId": "quay",
        "shape": "plate",
        "color": "#c9aa7a"
      },
      {
        "id": "v0023",
        "moduleId": "quay",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "v0024",
        "moduleId": "quay",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "v0025",
        "moduleId": "quay",
        "shape": "plate",
        "color": "#c9aa7a"
      },
      {
        "id": "v0026",
        "moduleId": "quay",
        "shape": "plate",
        "color": "#c9aa7a"
      },
      {
        "id": "v0027",
        "moduleId": "quay",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "v0028",
        "moduleId": "quay",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "v0029",
        "moduleId": "quay",
        "shape": "plate",
        "color": "#2878b8"
      },
      {
        "id": "v0030",
        "moduleId": "quay",
        "shape": "plate",
        "color": "#2878b8"
      },
      {
        "id": "v0031",
        "moduleId": "quay",
        "shape": "plate",
        "color": "#2878b8"
      },
      {
        "id": "v0032",
        "moduleId": "quay",
        "shape": "plate",
        "color": "#2878b8"
      },
      {
        "id": "v0033",
        "moduleId": "quay",
        "shape": "plate",
        "color": "#2878b8"
      },
      {
        "id": "v0034",
        "moduleId": "quay",
        "shape": "plate",
        "color": "#2878b8"
      },
      {
        "id": "v0035",
        "moduleId": "quay",
        "shape": "plate",
        "color": "#2878b8"
      },
      {
        "id": "v0036",
        "moduleId": "quay",
        "shape": "plate",
        "color": "#2878b8"
      },
      {
        "id": "v0037",
        "moduleId": "quay",
        "shape": "plate",
        "color": "#2878b8"
      },
      {
        "id": "v0038",
        "moduleId": "quay",
        "shape": "plate",
        "color": "#2878b8"
      },
      {
        "id": "v0039",
        "moduleId": "quay",
        "shape": "plate",
        "color": "#2878b8"
      },
      {
        "id": "v0040",
        "moduleId": "quay",
        "shape": "plate",
        "color": "#2878b8"
      },
      {
        "id": "v0041",
        "moduleId": "quay",
        "shape": "plate",
        "color": "#2878b8"
      },
      {
        "id": "v0042",
        "moduleId": "quay",
        "shape": "plate",
        "color": "#2878b8"
      },
      {
        "id": "v0043",
        "moduleId": "quay",
        "shape": "plate",
        "color": "#2878b8"
      },
      {
        "id": "v0044",
        "moduleId": "quay",
        "shape": "plate",
        "color": "#2878b8"
      },
      {
        "id": "v0045",
        "moduleId": "quay",
        "shape": "plate",
        "color": "#2878b8"
      },
      {
        "id": "v0046",
        "moduleId": "quay",
        "shape": "plate",
        "color": "#2878b8"
      },
      {
        "id": "v0047",
        "moduleId": "tower-left",
        "shape": "brick",
        "color": "#edf1f2"
      },
      {
        "id": "v0048",
        "moduleId": "tower-left",
        "shape": "brick",
        "color": "#edf1f2"
      },
      {
        "id": "v0049",
        "moduleId": "tower-left",
        "shape": "brick",
        "color": "#edf1f2"
      },
      {
        "id": "v0050",
        "moduleId": "tower-left",
        "shape": "brick",
        "color": "#edf1f2"
      },
      {
        "id": "v0051",
        "moduleId": "tower-left",
        "shape": "brick",
        "color": "#edf1f2"
      },
      {
        "id": "v0052",
        "moduleId": "tower-left",
        "shape": "brick",
        "color": "#edf1f2"
      },
      {
        "id": "v0053",
        "moduleId": "tower-left",
        "shape": "brick",
        "color": "#edf1f2"
      },
      {
        "id": "v0054",
        "moduleId": "tower-left",
        "shape": "brick",
        "color": "#edf1f2"
      },
      {
        "id": "v0055",
        "moduleId": "tower-left",
        "shape": "brick",
        "color": "#edf1f2"
      },
      {
        "id": "v0056",
        "moduleId": "tower-left",
        "shape": "brick",
        "color": "#edf1f2"
      },
      {
        "id": "v0057",
        "moduleId": "tower-left",
        "shape": "brick",
        "color": "#edf1f2"
      },
      {
        "id": "v0058",
        "moduleId": "tower-left",
        "shape": "brick",
        "color": "#edf1f2"
      },
      {
        "id": "v0059",
        "moduleId": "tower-left",
        "shape": "brick",
        "color": "#edf1f2"
      },
      {
        "id": "v0060",
        "moduleId": "tower-left",
        "shape": "brick",
        "color": "#edf1f2"
      },
      {
        "id": "v0061",
        "moduleId": "tower-left",
        "shape": "brick",
        "color": "#edf1f2"
      },
      {
        "id": "v0062",
        "moduleId": "tower-left",
        "shape": "brick",
        "color": "#edf1f2"
      },
      {
        "id": "v0063",
        "moduleId": "tower-left",
        "shape": "brick",
        "color": "#edf1f2"
      },
      {
        "id": "v0064",
        "moduleId": "tower-left",
        "shape": "brick",
        "color": "#edf1f2"
      },
      {
        "id": "v0065",
        "moduleId": "tower-left",
        "shape": "brick",
        "color": "#edf1f2"
      },
      {
        "id": "v0066",
        "moduleId": "tower-left",
        "shape": "brick",
        "color": "#edf1f2"
      },
      {
        "id": "v0067",
        "moduleId": "tower-left",
        "shape": "brick",
        "color": "#edf1f2"
      },
      {
        "id": "v0068",
        "moduleId": "tower-left",
        "shape": "brick",
        "color": "#edf1f2"
      },
      {
        "id": "v0069",
        "moduleId": "tower-left",
        "shape": "brick",
        "color": "#edf1f2"
      },
      {
        "id": "v0070",
        "moduleId": "tower-left",
        "shape": "brick",
        "color": "#edf1f2"
      },
      {
        "id": "v0071",
        "moduleId": "tower-left",
        "shape": "arch",
        "color": "#8c99a3"
      },
      {
        "id": "v0072",
        "moduleId": "tower-left",
        "shape": "arch",
        "color": "#8c99a3"
      },
      {
        "id": "v0073",
        "moduleId": "tower-left",
        "shape": "slope",
        "color": "#173b63"
      },
      {
        "id": "v0074",
        "moduleId": "tower-right",
        "shape": "brick",
        "color": "#edf1f2"
      },
      {
        "id": "v0075",
        "moduleId": "tower-right",
        "shape": "brick",
        "color": "#edf1f2"
      },
      {
        "id": "v0076",
        "moduleId": "tower-right",
        "shape": "brick",
        "color": "#edf1f2"
      },
      {
        "id": "v0077",
        "moduleId": "tower-right",
        "shape": "brick",
        "color": "#edf1f2"
      },
      {
        "id": "v0078",
        "moduleId": "tower-right",
        "shape": "brick",
        "color": "#edf1f2"
      },
      {
        "id": "v0079",
        "moduleId": "tower-right",
        "shape": "brick",
        "color": "#edf1f2"
      },
      {
        "id": "v0080",
        "moduleId": "tower-right",
        "shape": "brick",
        "color": "#edf1f2"
      },
      {
        "id": "v0081",
        "moduleId": "tower-right",
        "shape": "brick",
        "color": "#edf1f2"
      },
      {
        "id": "v0082",
        "moduleId": "tower-right",
        "shape": "brick",
        "color": "#edf1f2"
      },
      {
        "id": "v0083",
        "moduleId": "tower-right",
        "shape": "brick",
        "color": "#edf1f2"
      },
      {
        "id": "v0084",
        "moduleId": "tower-right",
        "shape": "brick",
        "color": "#edf1f2"
      },
      {
        "id": "v0085",
        "moduleId": "tower-right",
        "shape": "brick",
        "color": "#edf1f2"
      },
      {
        "id": "v0086",
        "moduleId": "tower-right",
        "shape": "brick",
        "color": "#edf1f2"
      },
      {
        "id": "v0087",
        "moduleId": "tower-right",
        "shape": "brick",
        "color": "#edf1f2"
      },
      {
        "id": "v0088",
        "moduleId": "tower-right",
        "shape": "brick",
        "color": "#edf1f2"
      },
      {
        "id": "v0089",
        "moduleId": "tower-right",
        "shape": "brick",
        "color": "#edf1f2"
      },
      {
        "id": "v0090",
        "moduleId": "tower-right",
        "shape": "brick",
        "color": "#edf1f2"
      },
      {
        "id": "v0091",
        "moduleId": "tower-right",
        "shape": "brick",
        "color": "#edf1f2"
      },
      {
        "id": "v0092",
        "moduleId": "tower-right",
        "shape": "brick",
        "color": "#edf1f2"
      },
      {
        "id": "v0093",
        "moduleId": "tower-right",
        "shape": "brick",
        "color": "#edf1f2"
      },
      {
        "id": "v0094",
        "moduleId": "tower-right",
        "shape": "brick",
        "color": "#edf1f2"
      },
      {
        "id": "v0095",
        "moduleId": "tower-right",
        "shape": "brick",
        "color": "#edf1f2"
      },
      {
        "id": "v0096",
        "moduleId": "tower-right",
        "shape": "brick",
        "color": "#edf1f2"
      },
      {
        "id": "v0097",
        "moduleId": "tower-right",
        "shape": "brick",
        "color": "#edf1f2"
      },
      {
        "id": "v0098",
        "moduleId": "tower-right",
        "shape": "arch",
        "color": "#8c99a3"
      },
      {
        "id": "v0099",
        "moduleId": "tower-right",
        "shape": "arch",
        "color": "#8c99a3"
      },
      {
        "id": "v0100",
        "moduleId": "tower-right",
        "shape": "slope",
        "color": "#173b63"
      },
      {
        "id": "v0101",
        "moduleId": "west-deck",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "v0102",
        "moduleId": "west-deck",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "v0103",
        "moduleId": "west-deck",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "v0104",
        "moduleId": "west-deck",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "v0105",
        "moduleId": "west-deck",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "v0106",
        "moduleId": "west-deck",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "v0107",
        "moduleId": "west-deck",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "v0108",
        "moduleId": "west-deck",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "v0109",
        "moduleId": "west-deck",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "v0110",
        "moduleId": "west-deck",
        "shape": "beam",
        "color": "#f2bf3c"
      },
      {
        "id": "v0111",
        "moduleId": "west-deck",
        "shape": "beam",
        "color": "#f2bf3c"
      },
      {
        "id": "v0112",
        "moduleId": "west-deck",
        "shape": "beam",
        "color": "#f2bf3c"
      },
      {
        "id": "v0113",
        "moduleId": "west-deck",
        "shape": "beam",
        "color": "#f2bf3c"
      },
      {
        "id": "v0114",
        "moduleId": "west-deck",
        "shape": "beam",
        "color": "#f2bf3c"
      },
      {
        "id": "v0115",
        "moduleId": "west-deck",
        "shape": "beam",
        "color": "#f2bf3c"
      },
      {
        "id": "v0116",
        "moduleId": "west-deck",
        "shape": "beam",
        "color": "#f2bf3c"
      },
      {
        "id": "v0117",
        "moduleId": "west-deck",
        "shape": "beam",
        "color": "#f2bf3c"
      },
      {
        "id": "v0118",
        "moduleId": "west-deck",
        "shape": "beam",
        "color": "#f2bf3c"
      },
      {
        "id": "v0119",
        "moduleId": "west-deck",
        "shape": "beam",
        "color": "#f2bf3c"
      },
      {
        "id": "v0120",
        "moduleId": "west-deck",
        "shape": "gear",
        "color": "#e8792e"
      },
      {
        "id": "v0121",
        "moduleId": "east-deck",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "v0122",
        "moduleId": "east-deck",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "v0123",
        "moduleId": "east-deck",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "v0124",
        "moduleId": "east-deck",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "v0125",
        "moduleId": "east-deck",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "v0126",
        "moduleId": "east-deck",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "v0127",
        "moduleId": "east-deck",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "v0128",
        "moduleId": "east-deck",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "v0129",
        "moduleId": "east-deck",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "v0130",
        "moduleId": "east-deck",
        "shape": "beam",
        "color": "#f2bf3c"
      },
      {
        "id": "v0131",
        "moduleId": "east-deck",
        "shape": "beam",
        "color": "#f2bf3c"
      },
      {
        "id": "v0132",
        "moduleId": "east-deck",
        "shape": "beam",
        "color": "#f2bf3c"
      },
      {
        "id": "v0133",
        "moduleId": "east-deck",
        "shape": "beam",
        "color": "#f2bf3c"
      },
      {
        "id": "v0134",
        "moduleId": "east-deck",
        "shape": "beam",
        "color": "#f2bf3c"
      },
      {
        "id": "v0135",
        "moduleId": "east-deck",
        "shape": "beam",
        "color": "#f2bf3c"
      },
      {
        "id": "v0136",
        "moduleId": "east-deck",
        "shape": "beam",
        "color": "#f2bf3c"
      },
      {
        "id": "v0137",
        "moduleId": "east-deck",
        "shape": "beam",
        "color": "#f2bf3c"
      },
      {
        "id": "v0138",
        "moduleId": "east-deck",
        "shape": "beam",
        "color": "#f2bf3c"
      },
      {
        "id": "v0139",
        "moduleId": "east-deck",
        "shape": "beam",
        "color": "#f2bf3c"
      },
      {
        "id": "v0140",
        "moduleId": "east-deck",
        "shape": "gear",
        "color": "#e8792e"
      },
      {
        "id": "v0141",
        "moduleId": "drive-cartridge",
        "shape": "gear",
        "color": "#e8792e"
      },
      {
        "id": "v0142",
        "moduleId": "drive-cartridge",
        "shape": "axle",
        "color": "#c6cdd2"
      }
    ]
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 颜色识别（h3-bascule-canal-gate-color）

零件 v0141 的颜色值是什么？

能力：颜色识别；形式：single-choice；证据：model-state。

- A：#e8792e
- B：#2878b8
- C：#d43a32
- D：#f2bf3c

```json
{
  "input": {
    "part": {
      "id": "v0141",
      "moduleId": "drive-cartridge",
      "shape": "gear",
      "size": [
        1.6,
        0.55,
        1.6
      ],
      "position": [
        0,
        0,
        0
      ],
      "rotation": [
        0.7071067811865475,
        0,
        0,
        0.7071067811865476
      ],
      "color": "#e8792e"
    }
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 三维位置（h3-bascule-canal-gate-position）

模块 drive-cartridge 的世界包围盒中心是什么？

能力：三维位置；形式：single-choice；证据：model-state。

- A：[-7.4,3.905,0]
- B：[7.4,3.905,0]
- C：[-7.4,2.8000000000000003,-3.5999999999999996]
- D：[0,0.40750000000000003,0]

```json
{
  "input": {
    "centers": {
      "quay": [
        0,
        0.40750000000000003,
        0
      ],
      "tower-left": [
        -7.4,
        3.905,
        0
      ],
      "tower-right": [
        7.4,
        3.905,
        0
      ],
      "west-deck": [
        -2.8000000000000003,
        1.3624999999999998,
        0
      ],
      "east-deck": [
        2.8000000000000003,
        1.3624999999999998,
        0
      ],
      "drive-cartridge": [
        -7.4,
        2.8000000000000003,
        -3.5999999999999996
      ]
    }
  },
  "answer": {
    "choiceId": "C"
  }
}
```

### 关节类型（h3-bascule-canal-gate-joint-type）

west-deck-hinge 采用什么约束类型？

能力：关节类型；形式：single-choice；证据：model-state。

- A：revolute
- B：fixed
- C：prismatic
- D：spring

```json
{
  "input": {
    "joint": {
      "id": "west-deck-hinge",
      "name": "west-deck hinge",
      "type": "revolute",
      "parent": "tower-left",
      "child": "west-deck",
      "anchorParent": [
        2.1999999999999997,
        -2.4049999999999994,
        0
      ],
      "anchorChild": [
        -2.4000000000000004,
        0.13749999999999996,
        0
      ],
      "axis": [
        0,
        0,
        1
      ],
      "limits": [
        0,
        1.25
      ]
    }
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 直接连接（h3-bascule-canal-gate-parent）

drive-cartridge 的直接父模块集合是什么？

能力：直接连接；形式：single-choice；证据：model-state。

- A：["drive-cartridge"]
- B：[]
- C：["quay","tower-left","tower-right","west-deck","east-deck","drive-cartridge"]
- D：["tower-left"]

```json
{
  "input": {
    "joints": [
      {
        "id": "tower--1-foot-a",
        "name": "Tower footing A",
        "type": "fixed",
        "parent": "quay",
        "child": "tower-left",
        "anchorParent": [
          -7.4,
          0.1925,
          -2
        ],
        "anchorChild": [
          0,
          -3.3049999999999997,
          -2
        ]
      },
      {
        "id": "tower--1-foot-b",
        "name": "Tower footing B",
        "type": "fixed",
        "parent": "quay",
        "child": "tower-left",
        "anchorParent": [
          -7.4,
          0.1925,
          2
        ],
        "anchorChild": [
          0,
          -3.3049999999999997,
          2
        ]
      },
      {
        "id": "tower-1-foot-a",
        "name": "Tower footing A",
        "type": "fixed",
        "parent": "quay",
        "child": "tower-right",
        "anchorParent": [
          7.4,
          0.1925,
          -2
        ],
        "anchorChild": [
          0,
          -3.3049999999999997,
          -2
        ]
      },
      {
        "id": "tower-1-foot-b",
        "name": "Tower footing B",
        "type": "fixed",
        "parent": "quay",
        "child": "tower-right",
        "anchorParent": [
          7.4,
          0.1925,
          2
        ],
        "anchorChild": [
          0,
          -3.3049999999999997,
          2
        ]
      },
      {
        "id": "west-deck-hinge",
        "name": "west-deck hinge",
        "type": "revolute",
        "parent": "tower-left",
        "child": "west-deck",
        "anchorParent": [
          2.1999999999999997,
          -2.4049999999999994,
          0
        ],
        "anchorChild": [
          -2.4000000000000004,
          0.13749999999999996,
          0
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          0,
          1.25
        ]
      },
      {
        "id": "east-deck-hinge",
        "name": "east-deck hinge",
        "type": "revolute",
        "parent": "tower-right",
        "child": "east-deck",
        "anchorParent": [
          -2.1999999999999997,
          -2.4049999999999994,
          0
        ],
        "anchorChild": [
          2.4000000000000004,
          0.13749999999999996,
          0
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          0,
          1.25
        ]
      },
      {
        "id": "drive-lock",
        "name": "Drive cartridge lock",
        "type": "fixed",
        "parent": "tower-left",
        "child": "drive-cartridge",
        "anchorParent": [
          0,
          -1.1049999999999995,
          -3.5999999999999996
        ],
        "anchorChild": [
          0,
          0,
          0
        ]
      }
    ]
  },
  "answer": {
    "choiceId": "D"
  }
}
```

### 基座识别（h3-bascule-canal-gate-anchor）

哪些模块被声明为固定基座？

能力：基座识别；形式：single-choice；证据：model-state。

- A：["quay","tower-left","tower-right","west-deck","east-deck","drive-cartridge"]
- B：["drive-cartridge"]
- C：["quay"]
- D：[]

```json
{
  "input": {
    "modules": [
      {
        "id": "quay",
        "name": "Canal quay and foundations",
        "role": "foundation",
        "anchored": true,
        "mass": 28,
        "position": [
          0,
          0.40750000000000003,
          0
        ],
        "rotation": [
          0,
          0,
          0,
          1
        ]
      },
      {
        "id": "tower-left",
        "name": "West bridge tower",
        "role": "tower",
        "anchored": false,
        "mass": 10,
        "position": [
          -7.4,
          3.9049999999999994,
          0
        ],
        "rotation": [
          0,
          0,
          0,
          1
        ]
      },
      {
        "id": "tower-right",
        "name": "East bridge tower",
        "role": "tower",
        "anchored": false,
        "mass": 10,
        "position": [
          7.4,
          3.9049999999999994,
          0
        ],
        "rotation": [
          0,
          0,
          0,
          1
        ]
      },
      {
        "id": "west-deck",
        "name": "West bascule deck",
        "role": "moving-deck",
        "anchored": false,
        "mass": 2,
        "position": [
          -2.8,
          1.3625,
          0
        ],
        "rotation": [
          0,
          0,
          0,
          1
        ]
      },
      {
        "id": "east-deck",
        "name": "East bascule deck",
        "role": "moving-deck",
        "anchored": false,
        "mass": 2,
        "position": [
          2.8,
          1.3625,
          0
        ],
        "rotation": [
          0,
          0,
          0,
          1
        ]
      },
      {
        "id": "drive-cartridge",
        "name": "Bascule drive cartridge",
        "role": "service-module",
        "anchored": false,
        "mass": 2,
        "position": [
          -7.4,
          2.8000000000000003,
          -3.5999999999999996
        ],
        "rotation": [
          0,
          0,
          0,
          1
        ]
      }
    ]
  },
  "answer": {
    "choiceId": "C"
  }
}
```

### 接口计数（h3-bascule-canal-gate-degree）

drive-cartridge 连接几个声明关节？平行关节分别计数。

能力：接口计数；形式：single-choice；证据：model-state。

- A：0
- B：3
- C：1
- D：2

```json
{
  "input": {
    "joints": [
      {
        "id": "tower--1-foot-a",
        "name": "Tower footing A",
        "type": "fixed",
        "parent": "quay",
        "child": "tower-left",
        "anchorParent": [
          -7.4,
          0.1925,
          -2
        ],
        "anchorChild": [
          0,
          -3.3049999999999997,
          -2
        ]
      },
      {
        "id": "tower--1-foot-b",
        "name": "Tower footing B",
        "type": "fixed",
        "parent": "quay",
        "child": "tower-left",
        "anchorParent": [
          -7.4,
          0.1925,
          2
        ],
        "anchorChild": [
          0,
          -3.3049999999999997,
          2
        ]
      },
      {
        "id": "tower-1-foot-a",
        "name": "Tower footing A",
        "type": "fixed",
        "parent": "quay",
        "child": "tower-right",
        "anchorParent": [
          7.4,
          0.1925,
          -2
        ],
        "anchorChild": [
          0,
          -3.3049999999999997,
          -2
        ]
      },
      {
        "id": "tower-1-foot-b",
        "name": "Tower footing B",
        "type": "fixed",
        "parent": "quay",
        "child": "tower-right",
        "anchorParent": [
          7.4,
          0.1925,
          2
        ],
        "anchorChild": [
          0,
          -3.3049999999999997,
          2
        ]
      },
      {
        "id": "west-deck-hinge",
        "name": "west-deck hinge",
        "type": "revolute",
        "parent": "tower-left",
        "child": "west-deck",
        "anchorParent": [
          2.1999999999999997,
          -2.4049999999999994,
          0
        ],
        "anchorChild": [
          -2.4000000000000004,
          0.13749999999999996,
          0
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          0,
          1.25
        ]
      },
      {
        "id": "east-deck-hinge",
        "name": "east-deck hinge",
        "type": "revolute",
        "parent": "tower-right",
        "child": "east-deck",
        "anchorParent": [
          -2.1999999999999997,
          -2.4049999999999994,
          0
        ],
        "anchorChild": [
          2.4000000000000004,
          0.13749999999999996,
          0
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          0,
          1.25
        ]
      },
      {
        "id": "drive-lock",
        "name": "Drive cartridge lock",
        "type": "fixed",
        "parent": "tower-left",
        "child": "drive-cartridge",
        "anchorParent": [
          0,
          -1.1049999999999995,
          -3.5999999999999996
        ],
        "anchorChild": [
          0,
          0,
          0
        ]
      }
    ]
  },
  "answer": {
    "choiceId": "C"
  }
}
```

### 局部改色（h3-bascule-canal-gate-recolor）

仅将 v0141 改成 #e8792e，其他零件不变。选择正确补丁。

能力：局部改色；形式：single-choice；证据：model-state。

- A：{"id":"v0141","color":"#e8792e"}
- B：{"id":"v0142","color":"#e8792e"}
- C：{"id":"v0141","color":"#2878b8"}
- D：{"id":"*","color":"#e8792e"}

```json
{
  "input": {
    "part": {
      "id": "v0141",
      "moduleId": "drive-cartridge",
      "shape": "gear",
      "size": [
        1.6,
        0.55,
        1.6
      ],
      "position": [
        0,
        0,
        0
      ],
      "rotation": [
        0.7071067811865475,
        0,
        0,
        0.7071067811865476
      ],
      "color": "#e8792e"
    }
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 补装部件（h3-bascule-canal-gate-add）

模块 drive-cartridge 缺失零件 v0141。选择与目标清单一致的补装描述。

能力：补装部件；形式：single-choice；证据：model-state。

- A：{"id":"v0141","moduleId":"quay","shape":"gear","size":[1.6,0.55,1.6],"position":[0,0,0],"rotation":[0.7071067811865475,0,0,0.7071067811865476],"color":"#e8792e"}
- B：{"id":"v0141","moduleId":"drive-cartridge","shape":"gear","size":[3,3,3],"position":[0,0,0],"rotation":[0.7071067811865475,0,0,0.7071067811865476],"color":"#e8792e"}
- C：{"id":"v0141","moduleId":"drive-cartridge","shape":"gear","size":[1.6,0.55,1.6],"position":[0,0,0],"rotation":[0.7071067811865475,0,0,0.7071067811865476],"color":"#000000"}
- D：{"id":"v0141","moduleId":"drive-cartridge","shape":"gear","size":[1.6,0.55,1.6],"position":[0,0,0],"rotation":[0.7071067811865475,0,0,0.7071067811865476],"color":"#e8792e"}

```json
{
  "input": {
    "targetPart": {
      "id": "v0141",
      "moduleId": "drive-cartridge",
      "shape": "gear",
      "size": [
        1.6,
        0.55,
        1.6
      ],
      "position": [
        0,
        0,
        0
      ],
      "rotation": [
        0.7071067811865475,
        0,
        0,
        0.7071067811865476
      ],
      "color": "#e8792e"
    },
    "existingIds": [
      "v0001",
      "v0002",
      "v0003",
      "v0004",
      "v0005",
      "v0006",
      "v0007",
      "v0008",
      "v0009",
      "v0010",
      "v0011",
      "v0012",
      "v0013",
      "v0014",
      "v0015",
      "v0016",
      "v0017",
      "v0018",
      "v0019",
      "v0020",
      "v0021",
      "v0022",
      "v0023",
      "v0024",
      "v0025",
      "v0026",
      "v0027",
      "v0028",
      "v0029",
      "v0030",
      "v0031",
      "v0032",
      "v0033",
      "v0034",
      "v0035",
      "v0036",
      "v0037",
      "v0038",
      "v0039",
      "v0040",
      "v0041",
      "v0042",
      "v0043",
      "v0044",
      "v0045",
      "v0046",
      "v0047",
      "v0048",
      "v0049",
      "v0050",
      "v0051",
      "v0052",
      "v0053",
      "v0054",
      "v0055",
      "v0056",
      "v0057",
      "v0058",
      "v0059",
      "v0060",
      "v0061",
      "v0062",
      "v0063",
      "v0064",
      "v0065",
      "v0066",
      "v0067",
      "v0068",
      "v0069",
      "v0070",
      "v0071",
      "v0072",
      "v0073",
      "v0074",
      "v0075",
      "v0076",
      "v0077",
      "v0078",
      "v0079",
      "v0080",
      "v0081",
      "v0082",
      "v0083",
      "v0084",
      "v0085",
      "v0086",
      "v0087",
      "v0088",
      "v0089",
      "v0090",
      "v0091",
      "v0092",
      "v0093",
      "v0094",
      "v0095",
      "v0096",
      "v0097",
      "v0098",
      "v0099",
      "v0100",
      "v0101",
      "v0102",
      "v0103",
      "v0104",
      "v0105",
      "v0106",
      "v0107",
      "v0108",
      "v0109",
      "v0110",
      "v0111",
      "v0112",
      "v0113",
      "v0114",
      "v0115",
      "v0116",
      "v0117",
      "v0118",
      "v0119",
      "v0120",
      "v0121",
      "v0122",
      "v0123",
      "v0124",
      "v0125",
      "v0126",
      "v0127",
      "v0128",
      "v0129",
      "v0130",
      "v0131",
      "v0132",
      "v0133",
      "v0134",
      "v0135",
      "v0136",
      "v0137",
      "v0138",
      "v0139",
      "v0140",
      "v0142"
    ]
  },
  "answer": {
    "choiceId": "D"
  }
}
```

### 安全拆除（h3-bascule-canal-gate-remove）

按声明依赖图，当前可以先拆哪些叶模块？

能力：安全拆除；形式：single-choice；证据：model-state。

- A：[]
- B：["quay","tower-left","tower-right","west-deck","east-deck","drive-cartridge"]
- C：["drive-cartridge","east-deck","west-deck"]
- D：["quay"]

```json
{
  "input": {
    "joints": [
      {
        "id": "tower--1-foot-a",
        "name": "Tower footing A",
        "type": "fixed",
        "parent": "quay",
        "child": "tower-left",
        "anchorParent": [
          -7.4,
          0.1925,
          -2
        ],
        "anchorChild": [
          0,
          -3.3049999999999997,
          -2
        ]
      },
      {
        "id": "tower--1-foot-b",
        "name": "Tower footing B",
        "type": "fixed",
        "parent": "quay",
        "child": "tower-left",
        "anchorParent": [
          -7.4,
          0.1925,
          2
        ],
        "anchorChild": [
          0,
          -3.3049999999999997,
          2
        ]
      },
      {
        "id": "tower-1-foot-a",
        "name": "Tower footing A",
        "type": "fixed",
        "parent": "quay",
        "child": "tower-right",
        "anchorParent": [
          7.4,
          0.1925,
          -2
        ],
        "anchorChild": [
          0,
          -3.3049999999999997,
          -2
        ]
      },
      {
        "id": "tower-1-foot-b",
        "name": "Tower footing B",
        "type": "fixed",
        "parent": "quay",
        "child": "tower-right",
        "anchorParent": [
          7.4,
          0.1925,
          2
        ],
        "anchorChild": [
          0,
          -3.3049999999999997,
          2
        ]
      },
      {
        "id": "west-deck-hinge",
        "name": "west-deck hinge",
        "type": "revolute",
        "parent": "tower-left",
        "child": "west-deck",
        "anchorParent": [
          2.1999999999999997,
          -2.4049999999999994,
          0
        ],
        "anchorChild": [
          -2.4000000000000004,
          0.13749999999999996,
          0
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          0,
          1.25
        ]
      },
      {
        "id": "east-deck-hinge",
        "name": "east-deck hinge",
        "type": "revolute",
        "parent": "tower-right",
        "child": "east-deck",
        "anchorParent": [
          -2.1999999999999997,
          -2.4049999999999994,
          0
        ],
        "anchorChild": [
          2.4000000000000004,
          0.13749999999999996,
          0
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          0,
          1.25
        ]
      },
      {
        "id": "drive-lock",
        "name": "Drive cartridge lock",
        "type": "fixed",
        "parent": "tower-left",
        "child": "drive-cartridge",
        "anchorParent": [
          0,
          -1.1049999999999995,
          -3.5999999999999996
        ],
        "anchorChild": [
          0,
          0,
          0
        ]
      }
    ],
    "modules": [
      "quay",
      "tower-left",
      "tower-right",
      "west-deck",
      "east-deck",
      "drive-cartridge"
    ]
  },
  "answer": {
    "choiceId": "C"
  }
}
```

### 替换选择（h3-bascule-canal-gate-replace）

在成本上限内选择刚度最大的替换件；并列选成本低者，再并列选ID字典序最小者。

能力：替换选择；形式：single-choice；证据：model-state。

- A：stock-1
- B：stock-2
- C：stock-3
- D：stock-0

```json
{
  "input": {
    "alternatives": [
      {
        "id": "stock-0",
        "cost": 8,
        "stiffness": 9,
        "mass": 1.3
      },
      {
        "id": "stock-1",
        "cost": 8,
        "stiffness": 5,
        "mass": 1.9
      },
      {
        "id": "stock-2",
        "cost": 8,
        "stiffness": 9,
        "mass": 1
      },
      {
        "id": "stock-3",
        "cost": 6,
        "stiffness": 6,
        "mass": 1.9
      }
    ],
    "maxCost": 7
  },
  "answer": {
    "choiceId": "C"
  }
}
```

### 平移纠偏（h3-bascule-canal-gate-translate）

观察到相对目标的平移误差 delta，选择补偿平移。

能力：平移纠偏；形式：single-choice；证据：model-state。

- A：[0,2,0]
- B：[-3,0,2]
- C：[3,0,-2]
- D：[0,0,0]

```json
{
  "input": {
    "delta": [
      3,
      0,
      -2
    ],
    "target": "drive-cartridge"
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 姿态纠偏（h3-bascule-canal-gate-rotate）

选择从当前yaw到目标yaw的最短有符号旋转；恰好180°时使用-180°。

能力：姿态纠偏；形式：single-choice；证据：model-state。

- A：90
- B：-180
- C：180
- D：0

```json
{
  "input": {
    "module": "drive-cartridge",
    "currentYaw": 315,
    "targetYaw": 135
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 下一步放置（h3-bascule-canal-gate-next-module）

已完成给定前缀，选择所有前置依赖已满足的下一模块集合。

能力：下一步放置；形式：single-choice；证据：model-state。

- A：["quay"]
- B：["drive-cartridge","east-deck","west-deck"]
- C：[]
- D：["quay","tower-left","tower-right"]

```json
{
  "input": {
    "prefix": [
      "quay",
      "tower-left",
      "tower-right"
    ],
    "joints": [
      {
        "id": "tower--1-foot-a",
        "name": "Tower footing A",
        "type": "fixed",
        "parent": "quay",
        "child": "tower-left",
        "anchorParent": [
          -7.4,
          0.1925,
          -2
        ],
        "anchorChild": [
          0,
          -3.3049999999999997,
          -2
        ]
      },
      {
        "id": "tower--1-foot-b",
        "name": "Tower footing B",
        "type": "fixed",
        "parent": "quay",
        "child": "tower-left",
        "anchorParent": [
          -7.4,
          0.1925,
          2
        ],
        "anchorChild": [
          0,
          -3.3049999999999997,
          2
        ]
      },
      {
        "id": "tower-1-foot-a",
        "name": "Tower footing A",
        "type": "fixed",
        "parent": "quay",
        "child": "tower-right",
        "anchorParent": [
          7.4,
          0.1925,
          -2
        ],
        "anchorChild": [
          0,
          -3.3049999999999997,
          -2
        ]
      },
      {
        "id": "tower-1-foot-b",
        "name": "Tower footing B",
        "type": "fixed",
        "parent": "quay",
        "child": "tower-right",
        "anchorParent": [
          7.4,
          0.1925,
          2
        ],
        "anchorChild": [
          0,
          -3.3049999999999997,
          2
        ]
      },
      {
        "id": "west-deck-hinge",
        "name": "west-deck hinge",
        "type": "revolute",
        "parent": "tower-left",
        "child": "west-deck",
        "anchorParent": [
          2.1999999999999997,
          -2.4049999999999994,
          0
        ],
        "anchorChild": [
          -2.4000000000000004,
          0.13749999999999996,
          0
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          0,
          1.25
        ]
      },
      {
        "id": "east-deck-hinge",
        "name": "east-deck hinge",
        "type": "revolute",
        "parent": "tower-right",
        "child": "east-deck",
        "anchorParent": [
          -2.1999999999999997,
          -2.4049999999999994,
          0
        ],
        "anchorChild": [
          2.4000000000000004,
          0.13749999999999996,
          0
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          0,
          1.25
        ]
      },
      {
        "id": "drive-lock",
        "name": "Drive cartridge lock",
        "type": "fixed",
        "parent": "tower-left",
        "child": "drive-cartridge",
        "anchorParent": [
          0,
          -1.1049999999999995,
          -3.5999999999999996
        ],
        "anchorChild": [
          0,
          0,
          0
        ]
      }
    ],
    "modules": [
      "quay",
      "tower-left",
      "tower-right",
      "west-deck",
      "east-deck",
      "drive-cartridge"
    ]
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 库存核算（h3-bascule-canal-gate-inventory）

备件库有 6 件，替换模块需 2 件，还剩多少？

能力：库存核算；形式：single-choice；证据：model-state。

- A：5
- B：3
- C：7
- D：4

```json
{
  "input": {
    "available": 6,
    "required": 2
  },
  "answer": {
    "choiceId": "D"
  }
}
```

### 子装配边界（h3-bascule-canal-gate-boundary）

隔离 drive-cartridge 需要断开哪些边界关节？

能力：子装配边界；形式：single-choice；证据：model-state。

- A：["west-deck-hinge"]
- B：["drive-lock"]
- C：[]
- D：["tower--1-foot-a","tower--1-foot-b","tower-1-foot-a","tower-1-foot-b","west-deck-hinge","east-deck-hinge","drive-lock"]

```json
{
  "input": {
    "joints": [
      {
        "id": "tower--1-foot-a",
        "name": "Tower footing A",
        "type": "fixed",
        "parent": "quay",
        "child": "tower-left",
        "anchorParent": [
          -7.4,
          0.1925,
          -2
        ],
        "anchorChild": [
          0,
          -3.3049999999999997,
          -2
        ]
      },
      {
        "id": "tower--1-foot-b",
        "name": "Tower footing B",
        "type": "fixed",
        "parent": "quay",
        "child": "tower-left",
        "anchorParent": [
          -7.4,
          0.1925,
          2
        ],
        "anchorChild": [
          0,
          -3.3049999999999997,
          2
        ]
      },
      {
        "id": "tower-1-foot-a",
        "name": "Tower footing A",
        "type": "fixed",
        "parent": "quay",
        "child": "tower-right",
        "anchorParent": [
          7.4,
          0.1925,
          -2
        ],
        "anchorChild": [
          0,
          -3.3049999999999997,
          -2
        ]
      },
      {
        "id": "tower-1-foot-b",
        "name": "Tower footing B",
        "type": "fixed",
        "parent": "quay",
        "child": "tower-right",
        "anchorParent": [
          7.4,
          0.1925,
          2
        ],
        "anchorChild": [
          0,
          -3.3049999999999997,
          2
        ]
      },
      {
        "id": "west-deck-hinge",
        "name": "west-deck hinge",
        "type": "revolute",
        "parent": "tower-left",
        "child": "west-deck",
        "anchorParent": [
          2.1999999999999997,
          -2.4049999999999994,
          0
        ],
        "anchorChild": [
          -2.4000000000000004,
          0.13749999999999996,
          0
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          0,
          1.25
        ]
      },
      {
        "id": "east-deck-hinge",
        "name": "east-deck hinge",
        "type": "revolute",
        "parent": "tower-right",
        "child": "east-deck",
        "anchorParent": [
          -2.1999999999999997,
          -2.4049999999999994,
          0
        ],
        "anchorChild": [
          2.4000000000000004,
          0.13749999999999996,
          0
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          0,
          1.25
        ]
      },
      {
        "id": "drive-lock",
        "name": "Drive cartridge lock",
        "type": "fixed",
        "parent": "tower-left",
        "child": "drive-cartridge",
        "anchorParent": [
          0,
          -1.1049999999999995,
          -3.5999999999999996
        ],
        "anchorChild": [
          0,
          0,
          0
        ]
      }
    ],
    "target": "drive-cartridge"
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 最小干预（h3-bascule-canal-gate-no-op）

当前模块颜色已满足指令，且无需改变位姿。最少需要几次编辑？

能力：最小干预；形式：single-choice；证据：model-state。

- A：2
- B：0
- C：1

```json
{
  "input": {
    "module": "drive-cartridge"
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 全过程依赖（h3-bascule-canal-gate-prefix）

给定候选顺序，首次违反前置依赖的步骤是？从 0 编号，-1 表示没有违反。

能力：全过程依赖；形式：single-choice；证据：support-graph。

- A：1
- B：5
- C：0
- D：-1

```json
{
  "input": {
    "order": [
      "tower-right",
      "quay",
      "tower-left",
      "drive-cartridge",
      "west-deck",
      "east-deck"
    ],
    "joints": [
      {
        "id": "tower--1-foot-a",
        "name": "Tower footing A",
        "type": "fixed",
        "parent": "quay",
        "child": "tower-left",
        "anchorParent": [
          -7.4,
          0.1925,
          -2
        ],
        "anchorChild": [
          0,
          -3.3049999999999997,
          -2
        ]
      },
      {
        "id": "tower--1-foot-b",
        "name": "Tower footing B",
        "type": "fixed",
        "parent": "quay",
        "child": "tower-left",
        "anchorParent": [
          -7.4,
          0.1925,
          2
        ],
        "anchorChild": [
          0,
          -3.3049999999999997,
          2
        ]
      },
      {
        "id": "tower-1-foot-a",
        "name": "Tower footing A",
        "type": "fixed",
        "parent": "quay",
        "child": "tower-right",
        "anchorParent": [
          7.4,
          0.1925,
          -2
        ],
        "anchorChild": [
          0,
          -3.3049999999999997,
          -2
        ]
      },
      {
        "id": "tower-1-foot-b",
        "name": "Tower footing B",
        "type": "fixed",
        "parent": "quay",
        "child": "tower-right",
        "anchorParent": [
          7.4,
          0.1925,
          2
        ],
        "anchorChild": [
          0,
          -3.3049999999999997,
          2
        ]
      },
      {
        "id": "west-deck-hinge",
        "name": "west-deck hinge",
        "type": "revolute",
        "parent": "tower-left",
        "child": "west-deck",
        "anchorParent": [
          2.1999999999999997,
          -2.4049999999999994,
          0
        ],
        "anchorChild": [
          -2.4000000000000004,
          0.13749999999999996,
          0
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          0,
          1.25
        ]
      },
      {
        "id": "east-deck-hinge",
        "name": "east-deck hinge",
        "type": "revolute",
        "parent": "tower-right",
        "child": "east-deck",
        "anchorParent": [
          -2.1999999999999997,
          -2.4049999999999994,
          0
        ],
        "anchorChild": [
          2.4000000000000004,
          0.13749999999999996,
          0
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          0,
          1.25
        ]
      },
      {
        "id": "drive-lock",
        "name": "Drive cartridge lock",
        "type": "fixed",
        "parent": "tower-left",
        "child": "drive-cartridge",
        "anchorParent": [
          0,
          -1.1049999999999995,
          -3.5999999999999996
        ],
        "anchorChild": [
          0,
          0,
          0
        ]
      }
    ]
  },
  "answer": {
    "choiceId": "C"
  }
}
```

### 连续维修路径（h3-bascule-canal-gate-access）

根据实际 Rapier shape cast 记录，选择全部无碰撞路径。

能力：连续维修路径；形式：multiple-choice；证据：Rapier。

- A：path-1
- B：path-2
- C：path-0

```json
{
  "input": {
    "paths": [
      {
        "id": "path-0",
        "start": [
          13.15,
          2.8000000000000003,
          -3.5999999999999996
        ],
        "end": [
          -7.4,
          2.8000000000000003,
          -3.5999999999999996
        ],
        "halfExtents": [
          0.18,
          0.18,
          0.18
        ],
        "clear": true,
        "timeOfImpact": null
      },
      {
        "id": "path-1",
        "start": [
          -7.4,
          11.1,
          -3.5999999999999996
        ],
        "end": [
          -7.4,
          2.8000000000000003,
          -3.5999999999999996
        ],
        "halfExtents": [
          0.18,
          0.18,
          0.18
        ],
        "clear": true,
        "timeOfImpact": null
      },
      {
        "id": "path-2",
        "start": [
          -7.4,
          2.8000000000000003,
          9.2
        ],
        "end": [
          -7.4,
          2.8000000000000003,
          -3.5999999999999996
        ],
        "halfExtents": [
          0.18,
          0.18,
          0.18
        ],
        "clear": false,
        "timeOfImpact": 0.4937499761581421
      }
    ],
    "simulator": "stud-inclusive conservative cuboids; anchored base; force-limited position servos; no clutch/material calibration"
  },
  "answer": {
    "choiceIds": [
      "A",
      "C"
    ]
  }
}
```

### 支撑反事实（h3-bascule-canal-gate-counterfactual）

移除指定模块后，哪些其余模块失去到任一基座的关节路径？不包含被移除模块本身。

能力：支撑反事实；形式：single-choice；证据：support-graph。

- A：[]
- B：["quay","tower-left","tower-right","west-deck","east-deck","drive-cartridge"]
- C：["drive-cartridge","west-deck"]
- D：["tower-left"]

```json
{
  "input": {
    "removed": "tower-left",
    "roots": [
      "quay"
    ],
    "joints": [
      {
        "id": "tower--1-foot-a",
        "name": "Tower footing A",
        "type": "fixed",
        "parent": "quay",
        "child": "tower-left",
        "anchorParent": [
          -7.4,
          0.1925,
          -2
        ],
        "anchorChild": [
          0,
          -3.3049999999999997,
          -2
        ]
      },
      {
        "id": "tower--1-foot-b",
        "name": "Tower footing B",
        "type": "fixed",
        "parent": "quay",
        "child": "tower-left",
        "anchorParent": [
          -7.4,
          0.1925,
          2
        ],
        "anchorChild": [
          0,
          -3.3049999999999997,
          2
        ]
      },
      {
        "id": "tower-1-foot-a",
        "name": "Tower footing A",
        "type": "fixed",
        "parent": "quay",
        "child": "tower-right",
        "anchorParent": [
          7.4,
          0.1925,
          -2
        ],
        "anchorChild": [
          0,
          -3.3049999999999997,
          -2
        ]
      },
      {
        "id": "tower-1-foot-b",
        "name": "Tower footing B",
        "type": "fixed",
        "parent": "quay",
        "child": "tower-right",
        "anchorParent": [
          7.4,
          0.1925,
          2
        ],
        "anchorChild": [
          0,
          -3.3049999999999997,
          2
        ]
      },
      {
        "id": "west-deck-hinge",
        "name": "west-deck hinge",
        "type": "revolute",
        "parent": "tower-left",
        "child": "west-deck",
        "anchorParent": [
          2.1999999999999997,
          -2.4049999999999994,
          0
        ],
        "anchorChild": [
          -2.4000000000000004,
          0.13749999999999996,
          0
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          0,
          1.25
        ]
      },
      {
        "id": "east-deck-hinge",
        "name": "east-deck hinge",
        "type": "revolute",
        "parent": "tower-right",
        "child": "east-deck",
        "anchorParent": [
          -2.1999999999999997,
          -2.4049999999999994,
          0
        ],
        "anchorChild": [
          2.4000000000000004,
          0.13749999999999996,
          0
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          0,
          1.25
        ]
      },
      {
        "id": "drive-lock",
        "name": "Drive cartridge lock",
        "type": "fixed",
        "parent": "tower-left",
        "child": "drive-cartridge",
        "anchorParent": [
          0,
          -1.1049999999999995,
          -3.5999999999999996
        ],
        "anchorChild": [
          0,
          0,
          0
        ]
      }
    ],
    "modules": [
      "quay",
      "tower-left",
      "tower-right",
      "west-deck",
      "east-deck",
      "drive-cartridge"
    ]
  },
  "answer": {
    "choiceId": "C"
  }
}
```

### 冲击响应读数（h3-bascule-canal-gate-dynamic）

Rapier 实际采样轨迹中的最大平移位移是多少？按四位小数报告。

能力：冲击响应读数；形式：single-choice；证据：Rapier。

- A：0
- B：1.0025
- C：0.0025
- D：0.2025

```json
{
  "input": {
    "trace": [
      {
        "time": 0.008333333333333333,
        "displacement": 0.0025396946590478422
      },
      {
        "time": 0.10833333333333334,
        "displacement": 1.3509586871407461e-7
      },
      {
        "time": 0.20833333333333334,
        "displacement": 1.3512573993068597e-7
      },
      {
        "time": 0.30833333333333335,
        "displacement": 1.351556822015709e-7
      },
      {
        "time": 0.4083333333333333,
        "displacement": 1.3518605079809729e-7
      },
      {
        "time": 0.5083333333333333,
        "displacement": 1.3521546726735775e-7
      },
      {
        "time": 0.6083333333333333,
        "displacement": 1.3522791597608827e-7
      },
      {
        "time": 0.7083333333333334,
        "displacement": 1.3522791597608827e-7
      },
      {
        "time": 0.8083333333333333,
        "displacement": 1.3522791597608827e-7
      },
      {
        "time": 0.9083333333333333,
        "displacement": 1.3522791597608827e-7
      },
      {
        "time": 1,
        "displacement": 1.3522791597608827e-7
      }
    ],
    "impulse": [
      10,
      1.8,
      3.5
    ],
    "nominalDrift": 0.0019236627831057305,
    "scope": "采样轨迹极值，非连续时间极值；不代表实物安全阈值"
  },
  "answer": {
    "choiceId": "C"
  }
}
```

### 关节限位推理（h3-bascule-canal-gate-kinematic）

下列目标位置/角度中哪些在关节声明限位内（含边界）？

能力：关节限位推理；形式：multiple-choice；证据：model-state。

- A：-0.5
- B：1.75
- C：0
- D：0.625

```json
{
  "input": {
    "joint": "west-deck-hinge",
    "limits": [
      0,
      1.25
    ],
    "units": "radians"
  },
  "answer": {
    "choiceIds": [
      "C",
      "D"
    ]
  }
}
```

### 约束故障诊断（h3-bascule-canal-gate-diagnosis）

已检测到端点和约束类型如下，选择匹配的全部关节。

能力：约束故障诊断；形式：multiple-choice；证据：model-state。

- A：tower--1-foot-a
- B：tower--1-foot-b
- C：tower-1-foot-a
- D：drive-lock

```json
{
  "input": {
    "endpoints": [
      "tower-left",
      "drive-cartridge"
    ],
    "type": "fixed",
    "joints": [
      {
        "id": "tower--1-foot-a",
        "name": "Tower footing A",
        "type": "fixed",
        "parent": "quay",
        "child": "tower-left",
        "anchorParent": [
          -7.4,
          0.1925,
          -2
        ],
        "anchorChild": [
          0,
          -3.3049999999999997,
          -2
        ]
      },
      {
        "id": "tower--1-foot-b",
        "name": "Tower footing B",
        "type": "fixed",
        "parent": "quay",
        "child": "tower-left",
        "anchorParent": [
          -7.4,
          0.1925,
          2
        ],
        "anchorChild": [
          0,
          -3.3049999999999997,
          2
        ]
      },
      {
        "id": "tower-1-foot-a",
        "name": "Tower footing A",
        "type": "fixed",
        "parent": "quay",
        "child": "tower-right",
        "anchorParent": [
          7.4,
          0.1925,
          -2
        ],
        "anchorChild": [
          0,
          -3.3049999999999997,
          -2
        ]
      },
      {
        "id": "tower-1-foot-b",
        "name": "Tower footing B",
        "type": "fixed",
        "parent": "quay",
        "child": "tower-right",
        "anchorParent": [
          7.4,
          0.1925,
          2
        ],
        "anchorChild": [
          0,
          -3.3049999999999997,
          2
        ]
      },
      {
        "id": "west-deck-hinge",
        "name": "west-deck hinge",
        "type": "revolute",
        "parent": "tower-left",
        "child": "west-deck",
        "anchorParent": [
          2.1999999999999997,
          -2.4049999999999994,
          0
        ],
        "anchorChild": [
          -2.4000000000000004,
          0.13749999999999996,
          0
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          0,
          1.25
        ]
      },
      {
        "id": "east-deck-hinge",
        "name": "east-deck hinge",
        "type": "revolute",
        "parent": "tower-right",
        "child": "east-deck",
        "anchorParent": [
          -2.1999999999999997,
          -2.4049999999999994,
          0
        ],
        "anchorChild": [
          2.4000000000000004,
          0.13749999999999996,
          0
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          0,
          1.25
        ]
      },
      {
        "id": "drive-lock",
        "name": "Drive cartridge lock",
        "type": "fixed",
        "parent": "tower-left",
        "child": "drive-cartridge",
        "anchorParent": [
          0,
          -1.1049999999999995,
          -3.5999999999999996
        ],
        "anchorChild": [
          0,
          0,
          0
        ]
      }
    ]
  },
  "answer": {
    "choiceIds": [
      "D"
    ]
  }
}
```

### 主动检查收益（h3-bascule-canal-gate-information-gain）

均匀先验四个世界，选择信息增益/成本最大的全部检查。

能力：主动检查收益；形式：multiple-choice；证据：finite-world。

- A：query-2
- B：query-0
- C：query-1

```json
{
  "input": {
    "queries": [
      {
        "id": "query-0",
        "cost": 2,
        "returns": [
          0,
          0,
          1,
          1
        ]
      },
      {
        "id": "query-1",
        "cost": 3,
        "returns": [
          0,
          1,
          2,
          3
        ]
      },
      {
        "id": "query-2",
        "cost": 1,
        "returns": [
          0,
          0,
          0,
          1
        ]
      }
    ],
    "module": "drive-cartridge",
    "worlds": [
      "normal",
      "jammed",
      "reversed",
      "loose"
    ]
  },
  "answer": {
    "choiceIds": [
      "A"
    ]
  }
}
```

### 不确定性与弃答（h3-bascule-canal-gate-abstention）

所有相容世界是否允许同一个后续动作？选择继续执行或请求检查。

能力：不确定性与弃答；形式：single-choice；证据：finite-world。

- A：commit
- B：inspect

```json
{
  "input": {
    "worlds": [
      {
        "id": "w0",
        "action": "continue"
      },
      {
        "id": "w1",
        "action": "continue"
      }
    ]
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 观测后信念更新（h3-bascule-canal-gate-posterior）

均匀先验，得到给定观测后，jammed 世界的后验概率是多少？

能力：观测后信念更新；形式：single-choice；证据：finite-world。

- A：0.5
- B：0.25
- C：0
- D：0.3333333333333333

```json
{
  "input": {
    "module": "drive-cartridge",
    "worlds": [
      "normal",
      "jammed",
      "reversed",
      "loose"
    ],
    "observationByWorld": [
      "positive",
      "positive",
      "positive",
      "positive"
    ],
    "observed": "positive"
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 多目标工程权衡（h3-bascule-canal-gate-pareto）

最小成本、最小质量、最大刚度，选择完整非支配集合。

能力：多目标工程权衡；形式：multiple-choice；证据：model-state。

- A：stock-0
- B：stock-1
- C：stock-2
- D：stock-3

```json
{
  "input": {
    "alternatives": [
      {
        "id": "stock-0",
        "cost": 8,
        "stiffness": 9,
        "mass": 1.3
      },
      {
        "id": "stock-1",
        "cost": 8,
        "stiffness": 5,
        "mass": 1.9
      },
      {
        "id": "stock-2",
        "cost": 8,
        "stiffness": 9,
        "mass": 1
      },
      {
        "id": "stock-3",
        "cost": 6,
        "stiffness": 6,
        "mass": 1.9
      }
    ]
  },
  "answer": {
    "choiceIds": [
      "C",
      "D"
    ]
  }
}
```

### 依赖装配（h3-bascule-canal-gate-assembly）

提交 actionIds。执行公开前置条件与效果，达到所有目标且不超过预算；允许交换独立动作。

能力：依赖装配；形式：actions；证据：state-machine。


```json
{
  "input": {
    "initialFacts": [],
    "initialModules": [],
    "actions": [
      {
        "id": "place:quay",
        "label": "安装 quay",
        "requires": [],
        "forbids": [
          "present:quay"
        ],
        "adds": [
          "present:quay"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "quay",
          "visible": true
        }
      },
      {
        "id": "place:tower-right",
        "label": "安装 tower-right",
        "requires": [
          "present:quay",
          "present:quay"
        ],
        "forbids": [
          "present:tower-right"
        ],
        "adds": [
          "present:tower-right"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "tower-right",
          "visible": true
        }
      },
      {
        "id": "place:drive-cartridge",
        "label": "安装 drive-cartridge",
        "requires": [
          "present:tower-left"
        ],
        "forbids": [
          "present:drive-cartridge"
        ],
        "adds": [
          "present:drive-cartridge"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "drive-cartridge",
          "visible": true
        }
      },
      {
        "id": "place:east-deck",
        "label": "安装 east-deck",
        "requires": [
          "present:tower-right"
        ],
        "forbids": [
          "present:east-deck"
        ],
        "adds": [
          "present:east-deck"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "east-deck",
          "visible": true
        }
      },
      {
        "id": "place:west-deck",
        "label": "安装 west-deck",
        "requires": [
          "present:tower-left"
        ],
        "forbids": [
          "present:west-deck"
        ],
        "adds": [
          "present:west-deck"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "west-deck",
          "visible": true
        }
      },
      {
        "id": "place:tower-left",
        "label": "安装 tower-left",
        "requires": [
          "present:quay",
          "present:quay"
        ],
        "forbids": [
          "present:tower-left"
        ],
        "adds": [
          "present:tower-left"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "tower-left",
          "visible": true
        }
      }
    ],
    "goalFacts": [
      "present:quay",
      "present:tower-left",
      "present:tower-right",
      "present:drive-cartridge",
      "present:west-deck",
      "present:east-deck"
    ],
    "budget": 6,
    "semantics": "requires must hold; forbids must be absent; effects apply in order; unit action cost"
  },
  "answer": {
    "actionIds": [
      "place:quay",
      "place:tower-right",
      "place:east-deck",
      "place:tower-left",
      "place:drive-cartridge",
      "place:west-deck"
    ]
  }
}
```

### 依赖拆解（h3-bascule-canal-gate-disassembly）

提交 actionIds。执行公开前置条件与效果，达到所有目标且不超过预算；允许交换独立动作。

能力：依赖拆解；形式：actions；证据：state-machine。


```json
{
  "input": {
    "initialFacts": [
      "present:quay",
      "present:tower-left",
      "present:tower-right",
      "present:west-deck",
      "present:east-deck",
      "present:drive-cartridge"
    ],
    "initialModules": [
      "quay",
      "tower-left",
      "tower-right",
      "west-deck",
      "east-deck",
      "drive-cartridge"
    ],
    "actions": [
      {
        "id": "remove:west-deck",
        "label": "拆除 west-deck",
        "requires": [
          "present:west-deck"
        ],
        "forbids": [],
        "adds": [
          "removed:west-deck"
        ],
        "deletes": [
          "present:west-deck"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "west-deck",
          "visible": false
        }
      },
      {
        "id": "remove:east-deck",
        "label": "拆除 east-deck",
        "requires": [
          "present:east-deck"
        ],
        "forbids": [],
        "adds": [
          "removed:east-deck"
        ],
        "deletes": [
          "present:east-deck"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "east-deck",
          "visible": false
        }
      },
      {
        "id": "remove:tower-left",
        "label": "拆除 tower-left",
        "requires": [
          "present:tower-left"
        ],
        "forbids": [
          "present:west-deck",
          "present:drive-cartridge"
        ],
        "adds": [
          "removed:tower-left"
        ],
        "deletes": [
          "present:tower-left"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "tower-left",
          "visible": false
        }
      },
      {
        "id": "remove:quay",
        "label": "拆除 quay",
        "requires": [
          "present:quay"
        ],
        "forbids": [
          "present:tower-left",
          "present:tower-left",
          "present:tower-right",
          "present:tower-right"
        ],
        "adds": [
          "removed:quay"
        ],
        "deletes": [
          "present:quay"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "quay",
          "visible": false
        }
      },
      {
        "id": "remove:tower-right",
        "label": "拆除 tower-right",
        "requires": [
          "present:tower-right"
        ],
        "forbids": [
          "present:east-deck"
        ],
        "adds": [
          "removed:tower-right"
        ],
        "deletes": [
          "present:tower-right"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "tower-right",
          "visible": false
        }
      },
      {
        "id": "remove:drive-cartridge",
        "label": "拆除 drive-cartridge",
        "requires": [
          "present:drive-cartridge"
        ],
        "forbids": [],
        "adds": [
          "removed:drive-cartridge"
        ],
        "deletes": [
          "present:drive-cartridge"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "drive-cartridge",
          "visible": false
        }
      }
    ],
    "goalFacts": [
      "removed:east-deck",
      "removed:west-deck",
      "removed:drive-cartridge",
      "removed:tower-right",
      "removed:tower-left",
      "removed:quay"
    ],
    "budget": 6,
    "semantics": "requires must hold; forbids must be absent; effects apply in order; unit action cost"
  },
  "answer": {
    "actionIds": [
      "remove:west-deck",
      "remove:east-deck",
      "remove:tower-right",
      "remove:drive-cartridge",
      "remove:tower-left",
      "remove:quay"
    ]
  }
}
```

### 承载维修（h3-bascule-canal-gate-service-repair）

提交 actionIds。执行公开前置条件与效果，达到所有目标且不超过预算；允许交换独立动作。

能力：承载维修；形式：actions；证据：state-machine。


```json
{
  "input": {
    "initialFacts": [
      "fault:drive-cartridge",
      "closed:drive-cartridge"
    ],
    "initialModules": [
      "quay",
      "tower-left",
      "tower-right",
      "west-deck",
      "east-deck",
      "drive-cartridge"
    ],
    "actions": [
      {
        "id": "open:drive-cartridge",
        "label": "open drive-cartridge",
        "requires": [
          "done:support:drive-cartridge"
        ],
        "forbids": [
          "done:open:drive-cartridge"
        ],
        "adds": [
          "done:open:drive-cartridge"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "drive-cartridge"
        }
      },
      {
        "id": "replace:drive-cartridge",
        "label": "replace drive-cartridge",
        "requires": [
          "done:remove:drive-cartridge"
        ],
        "forbids": [
          "done:replace:drive-cartridge"
        ],
        "adds": [
          "done:replace:drive-cartridge"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "drive-cartridge",
          "visible": true
        }
      },
      {
        "id": "close:drive-cartridge",
        "label": "close drive-cartridge",
        "requires": [
          "done:verify:drive-cartridge"
        ],
        "forbids": [
          "done:close:drive-cartridge"
        ],
        "adds": [
          "done:close:drive-cartridge"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "drive-cartridge"
        }
      },
      {
        "id": "release:drive-cartridge",
        "label": "release drive-cartridge",
        "requires": [
          "done:close:drive-cartridge"
        ],
        "forbids": [
          "done:release:drive-cartridge"
        ],
        "adds": [
          "done:release:drive-cartridge",
          "repaired:drive-cartridge"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "drive-cartridge"
        }
      },
      {
        "id": "support:drive-cartridge",
        "label": "support drive-cartridge",
        "requires": [
          "fault:drive-cartridge"
        ],
        "forbids": [
          "done:support:drive-cartridge"
        ],
        "adds": [
          "done:support:drive-cartridge"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "drive-cartridge"
        }
      },
      {
        "id": "verify:drive-cartridge",
        "label": "verify drive-cartridge",
        "requires": [
          "done:replace:drive-cartridge"
        ],
        "forbids": [
          "done:verify:drive-cartridge"
        ],
        "adds": [
          "done:verify:drive-cartridge"
        ],
        "deletes": [
          "fault:drive-cartridge"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "drive-cartridge"
        }
      },
      {
        "id": "remove:drive-cartridge",
        "label": "remove drive-cartridge",
        "requires": [
          "done:open:drive-cartridge"
        ],
        "forbids": [
          "done:remove:drive-cartridge"
        ],
        "adds": [
          "done:remove:drive-cartridge"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "drive-cartridge",
          "visible": false
        }
      }
    ],
    "goalFacts": [
      "repaired:drive-cartridge"
    ],
    "budget": 7,
    "semantics": "requires must hold; forbids must be absent; effects apply in order; unit action cost"
  },
  "answer": {
    "actionIds": [
      "support:drive-cartridge",
      "open:drive-cartridge",
      "remove:drive-cartridge",
      "replace:drive-cartridge",
      "verify:drive-cartridge",
      "close:drive-cartridge",
      "release:drive-cartridge"
    ]
  }
}
```

### 复合编辑验证（h3-bascule-canal-gate-compound-edit）

提交 actionIds。执行公开前置条件与效果，达到所有目标且不超过预算；允许交换独立动作。

能力：复合编辑验证；形式：actions；证据：state-machine。


```json
{
  "input": {
    "initialFacts": [
      "fault:drive-cartridge",
      "closed:drive-cartridge"
    ],
    "initialModules": [
      "quay",
      "tower-left",
      "tower-right",
      "west-deck",
      "east-deck",
      "drive-cartridge"
    ],
    "actions": [
      {
        "id": "open:drive-cartridge",
        "label": "open drive-cartridge",
        "requires": [
          "done:support:drive-cartridge"
        ],
        "forbids": [
          "done:open:drive-cartridge"
        ],
        "adds": [
          "done:open:drive-cartridge"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "drive-cartridge"
        }
      },
      {
        "id": "close:drive-cartridge",
        "label": "close drive-cartridge",
        "requires": [
          "done:verify:drive-cartridge"
        ],
        "forbids": [
          "done:close:drive-cartridge"
        ],
        "adds": [
          "done:close:drive-cartridge"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "drive-cartridge"
        }
      },
      {
        "id": "recolor:drive-cartridge",
        "label": "recolor drive-cartridge",
        "requires": [
          "done:open:drive-cartridge"
        ],
        "forbids": [
          "done:recolor:drive-cartridge"
        ],
        "adds": [
          "done:recolor:drive-cartridge"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "drive-cartridge",
          "color": "#ea7635"
        }
      },
      {
        "id": "release:drive-cartridge",
        "label": "release drive-cartridge",
        "requires": [
          "done:close:drive-cartridge"
        ],
        "forbids": [
          "done:release:drive-cartridge"
        ],
        "adds": [
          "done:release:drive-cartridge",
          "repaired:drive-cartridge"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "drive-cartridge"
        }
      },
      {
        "id": "support:drive-cartridge",
        "label": "support drive-cartridge",
        "requires": [
          "fault:drive-cartridge"
        ],
        "forbids": [
          "done:support:drive-cartridge"
        ],
        "adds": [
          "done:support:drive-cartridge"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "drive-cartridge"
        }
      },
      {
        "id": "verify:drive-cartridge",
        "label": "verify drive-cartridge",
        "requires": [
          "done:recolor:drive-cartridge"
        ],
        "forbids": [
          "done:verify:drive-cartridge"
        ],
        "adds": [
          "done:verify:drive-cartridge"
        ],
        "deletes": [
          "fault:drive-cartridge"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "drive-cartridge"
        }
      }
    ],
    "goalFacts": [
      "repaired:drive-cartridge"
    ],
    "budget": 6,
    "semantics": "requires must hold; forbids must be absent; effects apply in order; unit action cost"
  },
  "answer": {
    "actionIds": [
      "support:drive-cartridge",
      "open:drive-cartridge",
      "recolor:drive-cartridge",
      "verify:drive-cartridge",
      "close:drive-cartridge",
      "release:drive-cartridge"
    ]
  }
}
```

### 跨区域联合维修（h3-bascule-canal-gate-multi-fault）

提交 actionIds。执行公开前置条件与效果，达到所有目标且不超过预算；允许交换独立动作。

能力：跨区域联合维修；形式：actions；证据：state-machine。


```json
{
  "input": {
    "initialFacts": [
      "fault:west-deck",
      "closed:west-deck",
      "fault:east-deck",
      "closed:east-deck",
      "fault:drive-cartridge",
      "closed:drive-cartridge"
    ],
    "initialModules": [
      "quay",
      "tower-left",
      "tower-right",
      "west-deck",
      "east-deck",
      "drive-cartridge"
    ],
    "actions": [
      {
        "id": "remove:west-deck",
        "label": "remove west-deck",
        "requires": [
          "done:open:west-deck"
        ],
        "forbids": [
          "done:remove:west-deck"
        ],
        "adds": [
          "done:remove:west-deck"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "west-deck",
          "visible": false
        }
      },
      {
        "id": "open:drive-cartridge",
        "label": "open drive-cartridge",
        "requires": [
          "done:support:drive-cartridge"
        ],
        "forbids": [
          "done:open:drive-cartridge"
        ],
        "adds": [
          "done:open:drive-cartridge"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "drive-cartridge"
        }
      },
      {
        "id": "close:west-deck",
        "label": "close west-deck",
        "requires": [
          "done:verify:west-deck"
        ],
        "forbids": [
          "done:close:west-deck"
        ],
        "adds": [
          "done:close:west-deck"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "west-deck"
        }
      },
      {
        "id": "remove:east-deck",
        "label": "remove east-deck",
        "requires": [
          "done:open:east-deck"
        ],
        "forbids": [
          "done:remove:east-deck"
        ],
        "adds": [
          "done:remove:east-deck"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "east-deck",
          "visible": false
        }
      },
      {
        "id": "replace:east-deck",
        "label": "replace east-deck",
        "requires": [
          "done:remove:east-deck"
        ],
        "forbids": [
          "done:replace:east-deck"
        ],
        "adds": [
          "done:replace:east-deck"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "east-deck",
          "visible": true
        }
      },
      {
        "id": "replace:drive-cartridge",
        "label": "replace drive-cartridge",
        "requires": [
          "done:remove:drive-cartridge"
        ],
        "forbids": [
          "done:replace:drive-cartridge"
        ],
        "adds": [
          "done:replace:drive-cartridge"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "drive-cartridge",
          "visible": true
        }
      },
      {
        "id": "replace:west-deck",
        "label": "replace west-deck",
        "requires": [
          "done:remove:west-deck"
        ],
        "forbids": [
          "done:replace:west-deck"
        ],
        "adds": [
          "done:replace:west-deck"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "west-deck",
          "visible": true
        }
      },
      {
        "id": "close:drive-cartridge",
        "label": "close drive-cartridge",
        "requires": [
          "done:verify:drive-cartridge"
        ],
        "forbids": [
          "done:close:drive-cartridge"
        ],
        "adds": [
          "done:close:drive-cartridge"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "drive-cartridge"
        }
      },
      {
        "id": "release:west-deck",
        "label": "release west-deck",
        "requires": [
          "done:close:west-deck"
        ],
        "forbids": [
          "done:release:west-deck"
        ],
        "adds": [
          "done:release:west-deck",
          "repaired:west-deck"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "west-deck"
        }
      },
      {
        "id": "verify:east-deck",
        "label": "verify east-deck",
        "requires": [
          "done:replace:east-deck"
        ],
        "forbids": [
          "done:verify:east-deck"
        ],
        "adds": [
          "done:verify:east-deck"
        ],
        "deletes": [
          "fault:east-deck"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "east-deck"
        }
      },
      {
        "id": "release:east-deck",
        "label": "release east-deck",
        "requires": [
          "done:close:east-deck"
        ],
        "forbids": [
          "done:release:east-deck"
        ],
        "adds": [
          "done:release:east-deck",
          "repaired:east-deck"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "east-deck"
        }
      },
      {
        "id": "support:west-deck",
        "label": "support west-deck",
        "requires": [
          "fault:west-deck"
        ],
        "forbids": [
          "done:support:west-deck"
        ],
        "adds": [
          "done:support:west-deck"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "west-deck"
        }
      },
      {
        "id": "support:east-deck",
        "label": "support east-deck",
        "requires": [
          "fault:east-deck"
        ],
        "forbids": [
          "done:support:east-deck"
        ],
        "adds": [
          "done:support:east-deck"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "east-deck"
        }
      },
      {
        "id": "release:drive-cartridge",
        "label": "release drive-cartridge",
        "requires": [
          "done:close:drive-cartridge"
        ],
        "forbids": [
          "done:release:drive-cartridge"
        ],
        "adds": [
          "done:release:drive-cartridge",
          "repaired:drive-cartridge"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "drive-cartridge"
        }
      },
      {
        "id": "open:west-deck",
        "label": "open west-deck",
        "requires": [
          "done:support:west-deck"
        ],
        "forbids": [
          "done:open:west-deck"
        ],
        "adds": [
          "done:open:west-deck"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "west-deck"
        }
      },
      {
        "id": "verify:west-deck",
        "label": "verify west-deck",
        "requires": [
          "done:replace:west-deck"
        ],
        "forbids": [
          "done:verify:west-deck"
        ],
        "adds": [
          "done:verify:west-deck"
        ],
        "deletes": [
          "fault:west-deck"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "west-deck"
        }
      },
      {
        "id": "open:east-deck",
        "label": "open east-deck",
        "requires": [
          "done:support:east-deck"
        ],
        "forbids": [
          "done:open:east-deck"
        ],
        "adds": [
          "done:open:east-deck"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "east-deck"
        }
      },
      {
        "id": "support:drive-cartridge",
        "label": "support drive-cartridge",
        "requires": [
          "fault:drive-cartridge"
        ],
        "forbids": [
          "done:support:drive-cartridge"
        ],
        "adds": [
          "done:support:drive-cartridge"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "drive-cartridge"
        }
      },
      {
        "id": "close:east-deck",
        "label": "close east-deck",
        "requires": [
          "done:verify:east-deck"
        ],
        "forbids": [
          "done:close:east-deck"
        ],
        "adds": [
          "done:close:east-deck"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "east-deck"
        }
      },
      {
        "id": "verify:drive-cartridge",
        "label": "verify drive-cartridge",
        "requires": [
          "done:replace:drive-cartridge"
        ],
        "forbids": [
          "done:verify:drive-cartridge"
        ],
        "adds": [
          "done:verify:drive-cartridge"
        ],
        "deletes": [
          "fault:drive-cartridge"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "drive-cartridge"
        }
      },
      {
        "id": "remove:drive-cartridge",
        "label": "remove drive-cartridge",
        "requires": [
          "done:open:drive-cartridge"
        ],
        "forbids": [
          "done:remove:drive-cartridge"
        ],
        "adds": [
          "done:remove:drive-cartridge"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "drive-cartridge",
          "visible": false
        }
      }
    ],
    "goalFacts": [
      "repaired:west-deck",
      "repaired:east-deck",
      "repaired:drive-cartridge"
    ],
    "budget": 21,
    "semantics": "requires must hold; forbids must be absent; effects apply in order; unit action cost"
  },
  "answer": {
    "actionIds": [
      "support:west-deck",
      "support:east-deck",
      "open:west-deck",
      "remove:west-deck",
      "replace:west-deck",
      "verify:west-deck",
      "close:west-deck",
      "release:west-deck",
      "open:east-deck",
      "remove:east-deck",
      "replace:east-deck",
      "verify:east-deck",
      "support:drive-cartridge",
      "open:drive-cartridge",
      "close:east-deck",
      "release:east-deck",
      "remove:drive-cartridge",
      "replace:drive-cartridge",
      "verify:drive-cartridge",
      "close:drive-cartridge",
      "release:drive-cartridge"
    ]
  }
}
```

### 多工位资源调度（h3-bascule-canal-gate-scheduling）

为所有工单提交整数 starts，满足先后关系、独占工位及截止时间。

能力：多工位资源调度；形式：schedule；证据：resource-schedule。


```json
{
  "input": {
    "jobs": [
      {
        "id": "job-0",
        "module": "quay",
        "duration": 3,
        "resource": "test-bench",
        "after": []
      },
      {
        "id": "job-1",
        "module": "tower-left",
        "duration": 1,
        "resource": "technician",
        "after": []
      },
      {
        "id": "job-2",
        "module": "tower-right",
        "duration": 3,
        "resource": "test-bench",
        "after": [
          "job-0"
        ]
      },
      {
        "id": "job-3",
        "module": "west-deck",
        "duration": 2,
        "resource": "technician",
        "after": [
          "job-1"
        ]
      },
      {
        "id": "job-4",
        "module": "east-deck",
        "duration": 2,
        "resource": "test-bench",
        "after": [
          "job-2"
        ]
      },
      {
        "id": "job-5",
        "module": "drive-cartridge",
        "duration": 3,
        "resource": "technician",
        "after": [
          "job-3"
        ]
      }
    ],
    "deadline": 8
  },
  "answer": {
    "starts": {
      "job-0": 0,
      "job-1": 0,
      "job-2": 3,
      "job-3": 1,
      "job-4": 6,
      "job-5": 3
    }
  }
}
```

### 检查后条件策略（h3-bascule-canal-gate-policy）

提交一个检查及 observation→action 决策表，在所有相容世界中采取正确动作。

能力：检查后条件策略；形式：policy；证据：finite-world。


```json
{
  "input": {
    "module": "drive-cartridge",
    "worlds": [
      {
        "id": "normal",
        "action": "tighten"
      },
      {
        "id": "loose",
        "action": "replace"
      },
      {
        "id": "jammed",
        "action": "continue"
      }
    ],
    "budget": 2,
    "queries": [
      {
        "id": "visual",
        "cost": 1,
        "returns": {
          "normal": "same",
          "loose": "same",
          "jammed": "other"
        }
      },
      {
        "id": "probe",
        "cost": 2,
        "returns": {
          "normal": "signal-0",
          "loose": "signal-1",
          "jammed": "signal-2"
        }
      },
      {
        "id": "thermal",
        "cost": 3,
        "returns": {
          "normal": "same",
          "loose": "same",
          "jammed": "other"
        }
      }
    ]
  },
  "answer": {
    "queryId": "probe",
    "decisions": {
      "signal-0": "tighten",
      "signal-1": "replace",
      "signal-2": "continue"
    }
  }
}
```

### 局部坐标变换（h3-bascule-canal-gate-local-frame）

将模块局部点通过给定四元数与平移转换为世界点，保留五位小数。

能力：局部坐标变换；形式：single-choice；证据：model-state。

- A：[-6.4,3.8,-1.6]
- B：[-7.4,2.8,-2.6]
- C：[1,0,0]
- D：[-6.4,2.8,-3.6]

```json
{
  "input": {
    "localPoint": [
      1,
      0,
      0
    ],
    "rotationXYZW": [
      0,
      0.7071067811865476,
      0,
      -0.7071067811865475
    ],
    "translation": [
      -7.4,
      2.8000000000000003,
      -3.5999999999999996
    ]
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 正交视图投影（h3-bascule-canal-gate-projection）

按公开视图坐标约定，选择该世界点投影后的二维坐标。

能力：正交视图投影；形式：single-choice；证据：model-state。

- A：[9,4]
- B：[4,5]
- C：[0,0]
- D：[-5,9]

```json
{
  "input": {
    "view": "side",
    "point": [
      4,
      9,
      -5
    ],
    "convention": "front=(x,y), side=(z,y), top=(x,z)"
  },
  "answer": {
    "choiceId": "D"
  }
}
```

### 空间相对关系（h3-bascule-canal-gate-relative-order）

比较B相对A在指定世界轴上的模块原点坐标。

能力：空间相对关系；形式：single-choice；证据：model-state。

- A：less
- B：equal
- C：greater

```json
{
  "input": {
    "A": {
      "id": "quay",
      "position": [
        0,
        0.40750000000000003,
        0
      ]
    },
    "B": {
      "id": "drive-cartridge",
      "position": [
        -7.4,
        2.8000000000000003,
        -3.5999999999999996
      ]
    },
    "axis": "y"
  },
  "answer": {
    "choiceId": "C"
  }
}
```

### 约束自由度（h3-bascule-canal-gate-joint-axis）

仅考虑这一声明约束，不计闭环、马达与限位激活，保留多少相对运动自由度？弹簧仅施力、不消除自由度。

能力：约束自由度；形式：single-choice；证据：model-state。

- A：3
- B：6
- C：0
- D：1

```json
{
  "input": {
    "joint": {
      "id": "tower-1-foot-b",
      "name": "Tower footing B",
      "type": "fixed",
      "parent": "quay",
      "child": "tower-right",
      "anchorParent": [
        7.4,
        0.1925,
        2
      ],
      "anchorChild": [
        0,
        -3.3049999999999997,
        2
      ]
    }
  },
  "answer": {
    "choiceId": "C"
  }
}
```

### 维修间隙预算（h3-bascule-canal-gate-clearance-margin）

给定理想直槽净宽、工具宽度、单侧安全余量，工具是否满足横向间隙要求？

能力：维修间隙预算；形式：single-choice；证据：model-state。

- A：blocked
- B：feasible

```json
{
  "input": {
    "module": "drive-cartridge",
    "aperture": 0.71,
    "toolWidth": 0.55,
    "eachSideMargin": 0.05
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 载荷力矩（h3-bascule-canal-gate-load-moment）

绕给定原点的载荷力矩r×F是多少？采用右手系，忽略其他力。

能力：载荷力矩；形式：single-choice；证据：model-state。

- A：[0,0,9]
- B：[0,0,0]
- C：[0,-3,0]
- D：[0,0,-9]

```json
{
  "input": {
    "module": "drive-cartridge",
    "lever": [
      3,
      2,
      0
    ],
    "force": [
      0,
      -3,
      0
    ],
    "units": "scene-length × force"
  },
  "answer": {
    "choiceId": "D"
  }
}
```

### 非均匀先验更新（h3-bascule-canal-gate-weighted-posterior）

先验权重未归一化，观测只保留normal和jammed，求jammed后验概率。

能力：非均匀先验更新；形式：single-choice；证据：finite-world。

- A：0.6666666666666666
- B：0.4
- C：0
- D：1

```json
{
  "input": {
    "module": "drive-cartridge",
    "worlds": [
      "normal",
      "jammed",
      "loose"
    ],
    "weights": [
      2,
      4,
      4
    ],
    "compatible": [
      "normal",
      "jammed"
    ]
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 风险最小决策（h3-bascule-canal-gate-expected-loss）

继续运行期望损失=p×failureLoss，预防维修损失=repairCost，选择损失较低者；并列选继续。

能力：风险最小决策；形式：single-choice；证据：finite-world。

- A：continue
- B：repair

```json
{
  "input": {
    "faultProbability": 0.8,
    "repairCost": 2,
    "failureLoss": 13,
    "module": "drive-cartridge"
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 轨迹阈值判定（h3-bascule-canal-gate-trace-threshold）

实际采样轨迹中是否有位移严格超过给定阈值？只评价采样点。

能力：轨迹阈值判定；形式：single-choice；证据：Rapier。

- A：exceeded
- B：within

```json
{
  "input": {
    "trace": [
      {
        "time": 0.008333333333333333,
        "displacement": 0.0025396946590478422
      },
      {
        "time": 0.10833333333333334,
        "displacement": 1.3509586871407461e-7
      },
      {
        "time": 0.20833333333333334,
        "displacement": 1.3512573993068597e-7
      },
      {
        "time": 0.30833333333333335,
        "displacement": 1.351556822015709e-7
      },
      {
        "time": 0.4083333333333333,
        "displacement": 1.3518605079809729e-7
      },
      {
        "time": 0.5083333333333333,
        "displacement": 1.3521546726735775e-7
      },
      {
        "time": 0.6083333333333333,
        "displacement": 1.3522791597608827e-7
      },
      {
        "time": 0.7083333333333334,
        "displacement": 1.3522791597608827e-7
      },
      {
        "time": 0.8083333333333333,
        "displacement": 1.3522791597608827e-7
      },
      {
        "time": 0.9083333333333333,
        "displacement": 1.3522791597608827e-7
      },
      {
        "time": 1,
        "displacement": 1.3522791597608827e-7
      }
    ],
    "threshold": 0.0030476335908574104
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 安全联锁维修（h3-bascule-canal-gate-guarded-repair）

从给定故障状态提交动作序列，满足联锁、独占工具、终态及预算。不要跳过验证。

能力：安全联锁维修；形式：actions；证据：state-machine。


```json
{
  "input": {
    "actions": [
      {
        "id": "skip-inspection",
        "label": "跳过检查",
        "requires": [
          "tool:free"
        ],
        "forbids": [],
        "adds": [
          "unverified"
        ],
        "deletes": [
          "tool:free"
        ],
        "cost": 0
      },
      {
        "id": "release:drive-cartridge",
        "label": "release drive-cartridge",
        "requires": [
          "done:relock:drive-cartridge"
        ],
        "forbids": [
          "done:release:drive-cartridge"
        ],
        "adds": [
          "done:release:drive-cartridge",
          "ready:drive-cartridge",
          "tool:free"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "drive-cartridge"
        }
      },
      {
        "id": "relock:drive-cartridge",
        "label": "relock drive-cartridge",
        "requires": [
          "done:verify:drive-cartridge"
        ],
        "forbids": [
          "done:relock:drive-cartridge"
        ],
        "adds": [
          "done:relock:drive-cartridge"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "drive-cartridge"
        }
      },
      {
        "id": "verify:drive-cartridge",
        "label": "verify drive-cartridge",
        "requires": [
          "done:replace:drive-cartridge"
        ],
        "forbids": [
          "done:verify:drive-cartridge"
        ],
        "adds": [
          "done:verify:drive-cartridge"
        ],
        "deletes": [
          "fault:drive-cartridge",
          "misaligned:drive-cartridge"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "drive-cartridge"
        }
      },
      {
        "id": "replace:drive-cartridge",
        "label": "replace drive-cartridge",
        "requires": [
          "done:unlock:drive-cartridge"
        ],
        "forbids": [
          "done:replace:drive-cartridge"
        ],
        "adds": [
          "done:replace:drive-cartridge"
        ],
        "deletes": [],
        "cost": 2,
        "visual": {
          "moduleId": "drive-cartridge"
        }
      },
      {
        "id": "unlock:drive-cartridge",
        "label": "unlock drive-cartridge",
        "requires": [
          "done:support:drive-cartridge"
        ],
        "forbids": [
          "done:unlock:drive-cartridge"
        ],
        "adds": [
          "done:unlock:drive-cartridge"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "drive-cartridge"
        }
      },
      {
        "id": "support:drive-cartridge",
        "label": "support drive-cartridge",
        "requires": [
          "done:isolate:drive-cartridge"
        ],
        "forbids": [
          "done:support:drive-cartridge"
        ],
        "adds": [
          "done:support:drive-cartridge"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "drive-cartridge"
        }
      },
      {
        "id": "isolate:drive-cartridge",
        "label": "isolate drive-cartridge",
        "requires": [
          "tool:free",
          "fault:drive-cartridge"
        ],
        "forbids": [
          "done:isolate:drive-cartridge"
        ],
        "adds": [
          "done:isolate:drive-cartridge"
        ],
        "deletes": [
          "tool:free"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "drive-cartridge"
        }
      }
    ],
    "initialFacts": [
      "tool:free",
      "fault:drive-cartridge"
    ],
    "initialModules": [
      "quay",
      "tower-left",
      "tower-right",
      "west-deck",
      "east-deck",
      "drive-cartridge"
    ],
    "goalFacts": [
      "ready:drive-cartridge"
    ],
    "absentFacts": [
      "unverified"
    ],
    "budget": 8
  },
  "answer": {
    "actionIds": [
      "isolate:drive-cartridge",
      "support:drive-cartridge",
      "unlock:drive-cartridge",
      "replace:drive-cartridge",
      "verify:drive-cartridge",
      "relock:drive-cartridge",
      "release:drive-cartridge"
    ]
  }
}
```

### 失败状态回退（h3-bascule-canal-gate-rollback）

从给定故障状态提交动作序列，满足联锁、独占工具、终态及预算。不要跳过验证。

能力：失败状态回退；形式：actions；证据：state-machine。


```json
{
  "input": {
    "actions": [
      {
        "id": "skip-inspection",
        "label": "跳过检查",
        "requires": [
          "tool:free"
        ],
        "forbids": [],
        "adds": [
          "unverified"
        ],
        "deletes": [
          "tool:free"
        ],
        "cost": 0
      },
      {
        "id": "resume:drive-cartridge",
        "label": "resume drive-cartridge",
        "requires": [
          "done:verify:drive-cartridge"
        ],
        "forbids": [
          "done:resume:drive-cartridge"
        ],
        "adds": [
          "done:resume:drive-cartridge",
          "ready:drive-cartridge",
          "tool:free"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "drive-cartridge"
        }
      },
      {
        "id": "verify:drive-cartridge",
        "label": "verify drive-cartridge",
        "requires": [
          "done:align:drive-cartridge"
        ],
        "forbids": [
          "done:verify:drive-cartridge"
        ],
        "adds": [
          "done:verify:drive-cartridge"
        ],
        "deletes": [
          "fault:drive-cartridge",
          "misaligned:drive-cartridge"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "drive-cartridge"
        }
      },
      {
        "id": "align:drive-cartridge",
        "label": "align drive-cartridge",
        "requires": [
          "done:undo:drive-cartridge"
        ],
        "forbids": [
          "done:align:drive-cartridge"
        ],
        "adds": [
          "done:align:drive-cartridge"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "drive-cartridge",
          "visible": true
        }
      },
      {
        "id": "undo:drive-cartridge",
        "label": "undo drive-cartridge",
        "requires": [
          "done:isolate:drive-cartridge"
        ],
        "forbids": [
          "done:undo:drive-cartridge"
        ],
        "adds": [
          "done:undo:drive-cartridge"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "drive-cartridge",
          "visible": false
        }
      },
      {
        "id": "isolate:drive-cartridge",
        "label": "isolate drive-cartridge",
        "requires": [
          "tool:free",
          "fault:drive-cartridge"
        ],
        "forbids": [
          "done:isolate:drive-cartridge"
        ],
        "adds": [
          "done:isolate:drive-cartridge"
        ],
        "deletes": [
          "tool:free"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "drive-cartridge"
        }
      }
    ],
    "initialFacts": [
      "tool:free",
      "fault:drive-cartridge",
      "misaligned:drive-cartridge"
    ],
    "initialModules": [
      "quay",
      "tower-left",
      "tower-right",
      "west-deck",
      "east-deck",
      "drive-cartridge"
    ],
    "goalFacts": [
      "ready:drive-cartridge"
    ],
    "absentFacts": [
      "unverified"
    ],
    "budget": 5
  },
  "answer": {
    "actionIds": [
      "isolate:drive-cartridge",
      "undo:drive-cartridge",
      "align:drive-cartridge",
      "verify:drive-cartridge",
      "resume:drive-cartridge"
    ]
  }
}
```

### 共享工具协同维修（h3-bascule-canal-gate-resource-repair）

从给定故障状态提交动作序列，满足联锁、独占工具、终态及预算。不要跳过验证。

能力：共享工具协同维修；形式：actions；证据：state-machine。


```json
{
  "input": {
    "actions": [
      {
        "id": "skip-inspection",
        "label": "跳过检查",
        "requires": [
          "tool:free"
        ],
        "forbids": [],
        "adds": [
          "unverified"
        ],
        "deletes": [
          "tool:free"
        ],
        "cost": 0
      },
      {
        "id": "release:drive-cartridge",
        "label": "release drive-cartridge",
        "requires": [
          "done:relock:drive-cartridge"
        ],
        "forbids": [
          "done:release:drive-cartridge"
        ],
        "adds": [
          "done:release:drive-cartridge",
          "ready:drive-cartridge",
          "tool:free"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "drive-cartridge"
        }
      },
      {
        "id": "relock:drive-cartridge",
        "label": "relock drive-cartridge",
        "requires": [
          "done:verify:drive-cartridge"
        ],
        "forbids": [
          "done:relock:drive-cartridge"
        ],
        "adds": [
          "done:relock:drive-cartridge"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "drive-cartridge"
        }
      },
      {
        "id": "verify:drive-cartridge",
        "label": "verify drive-cartridge",
        "requires": [
          "done:replace:drive-cartridge"
        ],
        "forbids": [
          "done:verify:drive-cartridge"
        ],
        "adds": [
          "done:verify:drive-cartridge"
        ],
        "deletes": [
          "fault:drive-cartridge",
          "misaligned:drive-cartridge"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "drive-cartridge"
        }
      },
      {
        "id": "replace:drive-cartridge",
        "label": "replace drive-cartridge",
        "requires": [
          "done:unlock:drive-cartridge"
        ],
        "forbids": [
          "done:replace:drive-cartridge"
        ],
        "adds": [
          "done:replace:drive-cartridge"
        ],
        "deletes": [],
        "cost": 2,
        "visual": {
          "moduleId": "drive-cartridge"
        }
      },
      {
        "id": "unlock:drive-cartridge",
        "label": "unlock drive-cartridge",
        "requires": [
          "done:support:drive-cartridge"
        ],
        "forbids": [
          "done:unlock:drive-cartridge"
        ],
        "adds": [
          "done:unlock:drive-cartridge"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "drive-cartridge"
        }
      },
      {
        "id": "support:drive-cartridge",
        "label": "support drive-cartridge",
        "requires": [
          "done:isolate:drive-cartridge"
        ],
        "forbids": [
          "done:support:drive-cartridge"
        ],
        "adds": [
          "done:support:drive-cartridge"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "drive-cartridge"
        }
      },
      {
        "id": "isolate:drive-cartridge",
        "label": "isolate drive-cartridge",
        "requires": [
          "tool:free",
          "fault:drive-cartridge"
        ],
        "forbids": [
          "done:isolate:drive-cartridge"
        ],
        "adds": [
          "done:isolate:drive-cartridge"
        ],
        "deletes": [
          "tool:free"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "drive-cartridge"
        }
      },
      {
        "id": "release:east-deck",
        "label": "release east-deck",
        "requires": [
          "done:relock:east-deck"
        ],
        "forbids": [
          "done:release:east-deck"
        ],
        "adds": [
          "done:release:east-deck",
          "ready:east-deck",
          "tool:free"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "east-deck"
        }
      },
      {
        "id": "relock:east-deck",
        "label": "relock east-deck",
        "requires": [
          "done:verify:east-deck"
        ],
        "forbids": [
          "done:relock:east-deck"
        ],
        "adds": [
          "done:relock:east-deck"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "east-deck"
        }
      },
      {
        "id": "verify:east-deck",
        "label": "verify east-deck",
        "requires": [
          "done:replace:east-deck"
        ],
        "forbids": [
          "done:verify:east-deck"
        ],
        "adds": [
          "done:verify:east-deck"
        ],
        "deletes": [
          "fault:east-deck",
          "misaligned:east-deck"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "east-deck"
        }
      },
      {
        "id": "replace:east-deck",
        "label": "replace east-deck",
        "requires": [
          "done:unlock:east-deck"
        ],
        "forbids": [
          "done:replace:east-deck"
        ],
        "adds": [
          "done:replace:east-deck"
        ],
        "deletes": [],
        "cost": 2,
        "visual": {
          "moduleId": "east-deck"
        }
      },
      {
        "id": "unlock:east-deck",
        "label": "unlock east-deck",
        "requires": [
          "done:support:east-deck"
        ],
        "forbids": [
          "done:unlock:east-deck"
        ],
        "adds": [
          "done:unlock:east-deck"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "east-deck"
        }
      },
      {
        "id": "support:east-deck",
        "label": "support east-deck",
        "requires": [
          "done:isolate:east-deck"
        ],
        "forbids": [
          "done:support:east-deck"
        ],
        "adds": [
          "done:support:east-deck"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "east-deck"
        }
      },
      {
        "id": "isolate:east-deck",
        "label": "isolate east-deck",
        "requires": [
          "tool:free",
          "fault:east-deck"
        ],
        "forbids": [
          "done:isolate:east-deck"
        ],
        "adds": [
          "done:isolate:east-deck"
        ],
        "deletes": [
          "tool:free"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "east-deck"
        }
      },
      {
        "id": "release:west-deck",
        "label": "release west-deck",
        "requires": [
          "done:relock:west-deck"
        ],
        "forbids": [
          "done:release:west-deck"
        ],
        "adds": [
          "done:release:west-deck",
          "ready:west-deck",
          "tool:free"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "west-deck"
        }
      },
      {
        "id": "relock:west-deck",
        "label": "relock west-deck",
        "requires": [
          "done:verify:west-deck"
        ],
        "forbids": [
          "done:relock:west-deck"
        ],
        "adds": [
          "done:relock:west-deck"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "west-deck"
        }
      },
      {
        "id": "verify:west-deck",
        "label": "verify west-deck",
        "requires": [
          "done:replace:west-deck"
        ],
        "forbids": [
          "done:verify:west-deck"
        ],
        "adds": [
          "done:verify:west-deck"
        ],
        "deletes": [
          "fault:west-deck",
          "misaligned:west-deck"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "west-deck"
        }
      },
      {
        "id": "replace:west-deck",
        "label": "replace west-deck",
        "requires": [
          "done:unlock:west-deck"
        ],
        "forbids": [
          "done:replace:west-deck"
        ],
        "adds": [
          "done:replace:west-deck"
        ],
        "deletes": [],
        "cost": 2,
        "visual": {
          "moduleId": "west-deck"
        }
      },
      {
        "id": "unlock:west-deck",
        "label": "unlock west-deck",
        "requires": [
          "done:support:west-deck"
        ],
        "forbids": [
          "done:unlock:west-deck"
        ],
        "adds": [
          "done:unlock:west-deck"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "west-deck"
        }
      },
      {
        "id": "support:west-deck",
        "label": "support west-deck",
        "requires": [
          "done:isolate:west-deck"
        ],
        "forbids": [
          "done:support:west-deck"
        ],
        "adds": [
          "done:support:west-deck"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "west-deck"
        }
      },
      {
        "id": "isolate:west-deck",
        "label": "isolate west-deck",
        "requires": [
          "tool:free",
          "fault:west-deck"
        ],
        "forbids": [
          "done:isolate:west-deck"
        ],
        "adds": [
          "done:isolate:west-deck"
        ],
        "deletes": [
          "tool:free"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "west-deck"
        }
      },
      {
        "id": "release:tower-right",
        "label": "release tower-right",
        "requires": [
          "done:relock:tower-right"
        ],
        "forbids": [
          "done:release:tower-right"
        ],
        "adds": [
          "done:release:tower-right",
          "ready:tower-right",
          "tool:free"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "tower-right"
        }
      },
      {
        "id": "relock:tower-right",
        "label": "relock tower-right",
        "requires": [
          "done:verify:tower-right"
        ],
        "forbids": [
          "done:relock:tower-right"
        ],
        "adds": [
          "done:relock:tower-right"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "tower-right"
        }
      },
      {
        "id": "verify:tower-right",
        "label": "verify tower-right",
        "requires": [
          "done:replace:tower-right"
        ],
        "forbids": [
          "done:verify:tower-right"
        ],
        "adds": [
          "done:verify:tower-right"
        ],
        "deletes": [
          "fault:tower-right",
          "misaligned:tower-right"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "tower-right"
        }
      },
      {
        "id": "replace:tower-right",
        "label": "replace tower-right",
        "requires": [
          "done:unlock:tower-right"
        ],
        "forbids": [
          "done:replace:tower-right"
        ],
        "adds": [
          "done:replace:tower-right"
        ],
        "deletes": [],
        "cost": 2,
        "visual": {
          "moduleId": "tower-right"
        }
      },
      {
        "id": "unlock:tower-right",
        "label": "unlock tower-right",
        "requires": [
          "done:support:tower-right"
        ],
        "forbids": [
          "done:unlock:tower-right"
        ],
        "adds": [
          "done:unlock:tower-right"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "tower-right"
        }
      },
      {
        "id": "support:tower-right",
        "label": "support tower-right",
        "requires": [
          "done:isolate:tower-right"
        ],
        "forbids": [
          "done:support:tower-right"
        ],
        "adds": [
          "done:support:tower-right"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "tower-right"
        }
      },
      {
        "id": "isolate:tower-right",
        "label": "isolate tower-right",
        "requires": [
          "tool:free",
          "fault:tower-right"
        ],
        "forbids": [
          "done:isolate:tower-right"
        ],
        "adds": [
          "done:isolate:tower-right"
        ],
        "deletes": [
          "tool:free"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "tower-right"
        }
      }
    ],
    "initialFacts": [
      "tool:free",
      "fault:tower-right",
      "fault:west-deck",
      "fault:east-deck",
      "fault:drive-cartridge"
    ],
    "initialModules": [
      "quay",
      "tower-left",
      "tower-right",
      "west-deck",
      "east-deck",
      "drive-cartridge"
    ],
    "goalFacts": [
      "ready:tower-right",
      "ready:west-deck",
      "ready:east-deck",
      "ready:drive-cartridge"
    ],
    "absentFacts": [
      "unverified"
    ],
    "budget": 32
  },
  "answer": {
    "actionIds": [
      "isolate:drive-cartridge",
      "support:drive-cartridge",
      "unlock:drive-cartridge",
      "replace:drive-cartridge",
      "verify:drive-cartridge",
      "relock:drive-cartridge",
      "release:drive-cartridge",
      "isolate:east-deck",
      "support:east-deck",
      "unlock:east-deck",
      "replace:east-deck",
      "verify:east-deck",
      "relock:east-deck",
      "release:east-deck",
      "isolate:west-deck",
      "support:west-deck",
      "unlock:west-deck",
      "replace:west-deck",
      "verify:west-deck",
      "relock:west-deck",
      "release:west-deck",
      "isolate:tower-right",
      "support:tower-right",
      "unlock:tower-right",
      "replace:tower-right",
      "verify:tower-right",
      "relock:tower-right",
      "release:tower-right"
    ]
  }
}
```

### 预算约束检查策略（h3-bascule-canal-gate-budget-policy）

提交预算内、对所有相容世界均正确的检查决策表。

能力：预算约束检查策略；形式：policy；证据：finite-world。


```json
{
  "input": {
    "module": "drive-cartridge",
    "worlds": [
      {
        "id": "nominal",
        "action": "continue"
      },
      {
        "id": "fault",
        "action": "replace"
      }
    ],
    "queries": [
      {
        "id": "visual",
        "cost": 2,
        "returns": {
          "nominal": "clear",
          "fault": "alert"
        }
      },
      {
        "id": "probe",
        "cost": 0,
        "returns": {
          "nominal": "clear",
          "fault": "clear"
        }
      },
      {
        "id": "thermal",
        "cost": 3,
        "returns": {
          "nominal": "clear",
          "fault": "alert"
        }
      }
    ],
    "budget": 2
  },
  "answer": {
    "queryId": "visual",
    "decisions": {
      "clear": "continue",
      "alert": "replace"
    }
  }
}
```

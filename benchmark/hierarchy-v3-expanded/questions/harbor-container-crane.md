## D3 港口集装箱起重机

### 模块识别（h3-harbor-container-crane-identify）

高亮的维修模块对应哪个 ID？

能力：模块识别；形式：single-choice；证据：model-state。

- A：dock-base
- B：gantry
- C：hoist
- D：trolley

```json
{
  "input": {
    "moduleNames": [
      {
        "id": "dock-base",
        "name": "Harbor rail foundation"
      },
      {
        "id": "gantry",
        "name": "Twin-tower crane gantry"
      },
      {
        "id": "trolley",
        "name": "Traversing trolley"
      },
      {
        "id": "hoist",
        "name": "Hoist and hook block"
      },
      {
        "id": "container",
        "name": "Intermodal container"
      }
    ]
  },
  "answer": {
    "choiceId": "D"
  }
}
```

### 部件计数（h3-harbor-container-crane-count）

模块 trolley 有多少个可视零件？

能力：部件计数；形式：single-choice；证据：model-state。

- A：6
- B：4
- C：8
- D：5

```json
{
  "input": {
    "parts": [
      {
        "id": "v0001",
        "moduleId": "dock-base",
        "shape": "plate",
        "color": "#2878b8"
      },
      {
        "id": "v0002",
        "moduleId": "dock-base",
        "shape": "plate",
        "color": "#2878b8"
      },
      {
        "id": "v0003",
        "moduleId": "dock-base",
        "shape": "plate",
        "color": "#2878b8"
      },
      {
        "id": "v0004",
        "moduleId": "dock-base",
        "shape": "plate",
        "color": "#2878b8"
      },
      {
        "id": "v0005",
        "moduleId": "dock-base",
        "shape": "plate",
        "color": "#2878b8"
      },
      {
        "id": "v0006",
        "moduleId": "dock-base",
        "shape": "plate",
        "color": "#2878b8"
      },
      {
        "id": "v0007",
        "moduleId": "dock-base",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "v0008",
        "moduleId": "dock-base",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "v0009",
        "moduleId": "dock-base",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "v0010",
        "moduleId": "dock-base",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "v0011",
        "moduleId": "dock-base",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "v0012",
        "moduleId": "dock-base",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "v0013",
        "moduleId": "dock-base",
        "shape": "plate",
        "color": "#2878b8"
      },
      {
        "id": "v0014",
        "moduleId": "dock-base",
        "shape": "plate",
        "color": "#2878b8"
      },
      {
        "id": "v0015",
        "moduleId": "dock-base",
        "shape": "plate",
        "color": "#2878b8"
      },
      {
        "id": "v0016",
        "moduleId": "dock-base",
        "shape": "plate",
        "color": "#2878b8"
      },
      {
        "id": "v0017",
        "moduleId": "dock-base",
        "shape": "plate",
        "color": "#2878b8"
      },
      {
        "id": "v0018",
        "moduleId": "dock-base",
        "shape": "plate",
        "color": "#2878b8"
      },
      {
        "id": "v0019",
        "moduleId": "dock-base",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "v0020",
        "moduleId": "dock-base",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "v0021",
        "moduleId": "dock-base",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "v0022",
        "moduleId": "dock-base",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "v0023",
        "moduleId": "dock-base",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "v0024",
        "moduleId": "dock-base",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "v0025",
        "moduleId": "dock-base",
        "shape": "plate",
        "color": "#2878b8"
      },
      {
        "id": "v0026",
        "moduleId": "dock-base",
        "shape": "plate",
        "color": "#2878b8"
      },
      {
        "id": "v0027",
        "moduleId": "dock-base",
        "shape": "plate",
        "color": "#2878b8"
      },
      {
        "id": "v0028",
        "moduleId": "dock-base",
        "shape": "plate",
        "color": "#2878b8"
      },
      {
        "id": "v0029",
        "moduleId": "dock-base",
        "shape": "plate",
        "color": "#2878b8"
      },
      {
        "id": "v0030",
        "moduleId": "dock-base",
        "shape": "plate",
        "color": "#2878b8"
      },
      {
        "id": "v0031",
        "moduleId": "dock-base",
        "shape": "beam",
        "color": "#c6cdd2"
      },
      {
        "id": "v0032",
        "moduleId": "dock-base",
        "shape": "beam",
        "color": "#c6cdd2"
      },
      {
        "id": "v0033",
        "moduleId": "dock-base",
        "shape": "beam",
        "color": "#c6cdd2"
      },
      {
        "id": "v0034",
        "moduleId": "dock-base",
        "shape": "beam",
        "color": "#c6cdd2"
      },
      {
        "id": "v0035",
        "moduleId": "dock-base",
        "shape": "beam",
        "color": "#c6cdd2"
      },
      {
        "id": "v0036",
        "moduleId": "dock-base",
        "shape": "beam",
        "color": "#c6cdd2"
      },
      {
        "id": "v0037",
        "moduleId": "dock-base",
        "shape": "beam",
        "color": "#c6cdd2"
      },
      {
        "id": "v0038",
        "moduleId": "dock-base",
        "shape": "beam",
        "color": "#c6cdd2"
      },
      {
        "id": "v0039",
        "moduleId": "dock-base",
        "shape": "beam",
        "color": "#c6cdd2"
      },
      {
        "id": "v0040",
        "moduleId": "dock-base",
        "shape": "beam",
        "color": "#c6cdd2"
      },
      {
        "id": "v0041",
        "moduleId": "dock-base",
        "shape": "beam",
        "color": "#c6cdd2"
      },
      {
        "id": "v0042",
        "moduleId": "dock-base",
        "shape": "beam",
        "color": "#c6cdd2"
      },
      {
        "id": "v0043",
        "moduleId": "dock-base",
        "shape": "beam",
        "color": "#c6cdd2"
      },
      {
        "id": "v0044",
        "moduleId": "dock-base",
        "shape": "beam",
        "color": "#c6cdd2"
      },
      {
        "id": "v0045",
        "moduleId": "dock-base",
        "shape": "beam",
        "color": "#c6cdd2"
      },
      {
        "id": "v0046",
        "moduleId": "dock-base",
        "shape": "beam",
        "color": "#c6cdd2"
      },
      {
        "id": "v0047",
        "moduleId": "dock-base",
        "shape": "beam",
        "color": "#c6cdd2"
      },
      {
        "id": "v0048",
        "moduleId": "dock-base",
        "shape": "beam",
        "color": "#c6cdd2"
      },
      {
        "id": "v0049",
        "moduleId": "dock-base",
        "shape": "beam",
        "color": "#c6cdd2"
      },
      {
        "id": "v0050",
        "moduleId": "dock-base",
        "shape": "beam",
        "color": "#c6cdd2"
      },
      {
        "id": "v0051",
        "moduleId": "dock-base",
        "shape": "beam",
        "color": "#c6cdd2"
      },
      {
        "id": "v0052",
        "moduleId": "dock-base",
        "shape": "beam",
        "color": "#c6cdd2"
      },
      {
        "id": "v0053",
        "moduleId": "dock-base",
        "shape": "beam",
        "color": "#c6cdd2"
      },
      {
        "id": "v0054",
        "moduleId": "dock-base",
        "shape": "beam",
        "color": "#c6cdd2"
      },
      {
        "id": "v0055",
        "moduleId": "gantry",
        "shape": "beam",
        "color": "#f2bf3c"
      },
      {
        "id": "v0056",
        "moduleId": "gantry",
        "shape": "beam",
        "color": "#f2bf3c"
      },
      {
        "id": "v0057",
        "moduleId": "gantry",
        "shape": "beam",
        "color": "#f2bf3c"
      },
      {
        "id": "v0058",
        "moduleId": "gantry",
        "shape": "beam",
        "color": "#f2bf3c"
      },
      {
        "id": "v0059",
        "moduleId": "gantry",
        "shape": "beam",
        "color": "#f2bf3c"
      },
      {
        "id": "v0060",
        "moduleId": "gantry",
        "shape": "beam",
        "color": "#f2bf3c"
      },
      {
        "id": "v0061",
        "moduleId": "gantry",
        "shape": "beam",
        "color": "#f2bf3c"
      },
      {
        "id": "v0062",
        "moduleId": "gantry",
        "shape": "beam",
        "color": "#f2bf3c"
      },
      {
        "id": "v0063",
        "moduleId": "gantry",
        "shape": "beam",
        "color": "#f2bf3c"
      },
      {
        "id": "v0064",
        "moduleId": "gantry",
        "shape": "beam",
        "color": "#f2bf3c"
      },
      {
        "id": "v0065",
        "moduleId": "gantry",
        "shape": "beam",
        "color": "#f2bf3c"
      },
      {
        "id": "v0066",
        "moduleId": "gantry",
        "shape": "beam",
        "color": "#f2bf3c"
      },
      {
        "id": "v0067",
        "moduleId": "gantry",
        "shape": "beam",
        "color": "#f2bf3c"
      },
      {
        "id": "v0068",
        "moduleId": "gantry",
        "shape": "beam",
        "color": "#f2bf3c"
      },
      {
        "id": "v0069",
        "moduleId": "gantry",
        "shape": "beam",
        "color": "#f2bf3c"
      },
      {
        "id": "v0070",
        "moduleId": "gantry",
        "shape": "beam",
        "color": "#f2bf3c"
      },
      {
        "id": "v0071",
        "moduleId": "gantry",
        "shape": "beam",
        "color": "#f2bf3c"
      },
      {
        "id": "v0072",
        "moduleId": "gantry",
        "shape": "beam",
        "color": "#f2bf3c"
      },
      {
        "id": "v0073",
        "moduleId": "gantry",
        "shape": "beam",
        "color": "#f2bf3c"
      },
      {
        "id": "v0074",
        "moduleId": "gantry",
        "shape": "beam",
        "color": "#f2bf3c"
      },
      {
        "id": "v0075",
        "moduleId": "gantry",
        "shape": "beam",
        "color": "#f2bf3c"
      },
      {
        "id": "v0076",
        "moduleId": "gantry",
        "shape": "beam",
        "color": "#f2bf3c"
      },
      {
        "id": "v0077",
        "moduleId": "gantry",
        "shape": "beam",
        "color": "#f2bf3c"
      },
      {
        "id": "v0078",
        "moduleId": "gantry",
        "shape": "beam",
        "color": "#f2bf3c"
      },
      {
        "id": "v0079",
        "moduleId": "gantry",
        "shape": "beam",
        "color": "#26323b"
      },
      {
        "id": "v0080",
        "moduleId": "gantry",
        "shape": "beam",
        "color": "#26323b"
      },
      {
        "id": "v0081",
        "moduleId": "gantry",
        "shape": "beam",
        "color": "#26323b"
      },
      {
        "id": "v0082",
        "moduleId": "gantry",
        "shape": "beam",
        "color": "#26323b"
      },
      {
        "id": "v0083",
        "moduleId": "gantry",
        "shape": "beam",
        "color": "#26323b"
      },
      {
        "id": "v0084",
        "moduleId": "gantry",
        "shape": "beam",
        "color": "#26323b"
      },
      {
        "id": "v0085",
        "moduleId": "gantry",
        "shape": "beam",
        "color": "#f2bf3c"
      },
      {
        "id": "v0086",
        "moduleId": "gantry",
        "shape": "beam",
        "color": "#f2bf3c"
      },
      {
        "id": "v0087",
        "moduleId": "gantry",
        "shape": "beam",
        "color": "#f2bf3c"
      },
      {
        "id": "v0088",
        "moduleId": "gantry",
        "shape": "beam",
        "color": "#f2bf3c"
      },
      {
        "id": "v0089",
        "moduleId": "gantry",
        "shape": "beam",
        "color": "#f2bf3c"
      },
      {
        "id": "v0090",
        "moduleId": "gantry",
        "shape": "beam",
        "color": "#f2bf3c"
      },
      {
        "id": "v0091",
        "moduleId": "gantry",
        "shape": "beam",
        "color": "#f2bf3c"
      },
      {
        "id": "v0092",
        "moduleId": "gantry",
        "shape": "beam",
        "color": "#f2bf3c"
      },
      {
        "id": "v0093",
        "moduleId": "gantry",
        "shape": "beam",
        "color": "#f2bf3c"
      },
      {
        "id": "v0094",
        "moduleId": "gantry",
        "shape": "beam",
        "color": "#f2bf3c"
      },
      {
        "id": "v0095",
        "moduleId": "gantry",
        "shape": "beam",
        "color": "#f2bf3c"
      },
      {
        "id": "v0096",
        "moduleId": "gantry",
        "shape": "beam",
        "color": "#f2bf3c"
      },
      {
        "id": "v0097",
        "moduleId": "gantry",
        "shape": "beam",
        "color": "#f2bf3c"
      },
      {
        "id": "v0098",
        "moduleId": "gantry",
        "shape": "beam",
        "color": "#f2bf3c"
      },
      {
        "id": "v0099",
        "moduleId": "gantry",
        "shape": "beam",
        "color": "#f2bf3c"
      },
      {
        "id": "v0100",
        "moduleId": "gantry",
        "shape": "beam",
        "color": "#f2bf3c"
      },
      {
        "id": "v0101",
        "moduleId": "gantry",
        "shape": "beam",
        "color": "#f2bf3c"
      },
      {
        "id": "v0102",
        "moduleId": "gantry",
        "shape": "beam",
        "color": "#f2bf3c"
      },
      {
        "id": "v0103",
        "moduleId": "gantry",
        "shape": "beam",
        "color": "#f2bf3c"
      },
      {
        "id": "v0104",
        "moduleId": "gantry",
        "shape": "beam",
        "color": "#f2bf3c"
      },
      {
        "id": "v0105",
        "moduleId": "gantry",
        "shape": "beam",
        "color": "#f2bf3c"
      },
      {
        "id": "v0106",
        "moduleId": "gantry",
        "shape": "beam",
        "color": "#f2bf3c"
      },
      {
        "id": "v0107",
        "moduleId": "gantry",
        "shape": "beam",
        "color": "#f2bf3c"
      },
      {
        "id": "v0108",
        "moduleId": "gantry",
        "shape": "beam",
        "color": "#f2bf3c"
      },
      {
        "id": "v0109",
        "moduleId": "gantry",
        "shape": "window",
        "color": "#79c7d8"
      },
      {
        "id": "v0110",
        "moduleId": "trolley",
        "shape": "panel",
        "color": "#e8792e"
      },
      {
        "id": "v0111",
        "moduleId": "trolley",
        "shape": "wheel",
        "color": "#101820"
      },
      {
        "id": "v0112",
        "moduleId": "trolley",
        "shape": "wheel",
        "color": "#101820"
      },
      {
        "id": "v0113",
        "moduleId": "trolley",
        "shape": "wheel",
        "color": "#101820"
      },
      {
        "id": "v0114",
        "moduleId": "trolley",
        "shape": "wheel",
        "color": "#101820"
      },
      {
        "id": "v0115",
        "moduleId": "hoist",
        "shape": "axle",
        "color": "#26323b"
      },
      {
        "id": "v0116",
        "moduleId": "hoist",
        "shape": "gear",
        "color": "#f2bf3c"
      },
      {
        "id": "v0117",
        "moduleId": "hoist",
        "shape": "beam",
        "color": "#26323b"
      },
      {
        "id": "v0118",
        "moduleId": "container",
        "shape": "panel",
        "color": "#d43a32"
      },
      {
        "id": "v0119",
        "moduleId": "container",
        "shape": "panel",
        "color": "#d43a32"
      },
      {
        "id": "v0120",
        "moduleId": "container",
        "shape": "panel",
        "color": "#d43a32"
      },
      {
        "id": "v0121",
        "moduleId": "container",
        "shape": "panel",
        "color": "#d43a32"
      },
      {
        "id": "v0122",
        "moduleId": "container",
        "shape": "panel",
        "color": "#d43a32"
      },
      {
        "id": "v0123",
        "moduleId": "container",
        "shape": "panel",
        "color": "#d43a32"
      },
      {
        "id": "v0124",
        "moduleId": "container",
        "shape": "panel",
        "color": "#d43a32"
      },
      {
        "id": "v0125",
        "moduleId": "container",
        "shape": "panel",
        "color": "#d43a32"
      },
      {
        "id": "v0126",
        "moduleId": "container",
        "shape": "panel",
        "color": "#d43a32"
      }
    ]
  },
  "answer": {
    "choiceId": "D"
  }
}
```

### 颜色识别（h3-harbor-container-crane-color）

零件 v0110 的颜色值是什么？

能力：颜色识别；形式：single-choice；证据：model-state。

- A：#e8792e
- B：#2878b8
- C：#d43a32
- D：#f2bf3c

```json
{
  "input": {
    "part": {
      "id": "v0110",
      "moduleId": "trolley",
      "shape": "panel",
      "size": [
        2.2,
        0.7,
        3.4
      ],
      "position": [
        0,
        0.18750000000000006,
        0
      ],
      "rotation": [
        0,
        0,
        0,
        1
      ],
      "color": "#e8792e"
    }
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 三维位置（h3-harbor-container-crane-position）

模块 trolley 的世界包围盒中心是什么？

能力：三维位置；形式：single-choice；证据：model-state。

- A：[0,7.9125,0]
- B：[0,0.6799999999999999,0]
- C：[0,4.837103069057987,-0.6625000000000005]
- D：[0.30000000000000004,5.530897433389777,0]

```json
{
  "input": {
    "centers": {
      "dock-base": [
        0,
        0.6799999999999999,
        0
      ],
      "gantry": [
        0,
        4.837103069057987,
        -0.6625000000000005
      ],
      "trolley": [
        0,
        7.9125,
        0
      ],
      "hoist": [
        0.30000000000000004,
        5.530897433389777,
        0
      ],
      "container": [
        0,
        2.15,
        0
      ]
    }
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 关节类型（h3-harbor-container-crane-joint-type）

trolley-rail 采用什么约束类型？

能力：关节类型；形式：single-choice；证据：model-state。

- A：prismatic
- B：fixed
- C：revolute
- D：spring

```json
{
  "input": {
    "joint": {
      "id": "trolley-rail",
      "name": "Trolley rail",
      "type": "prismatic",
      "parent": "gantry",
      "child": "trolley",
      "anchorParent": [
        0,
        3.2628969309420137,
        0.6625000000000003
      ],
      "anchorChild": [
        0,
        0.18750000000000006,
        0
      ],
      "axis": [
        1,
        0,
        0
      ],
      "limits": [
        -3.8,
        3.8
      ]
    }
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 直接连接（h3-harbor-container-crane-parent）

trolley 的直接父模块集合是什么？

能力：直接连接；形式：single-choice；证据：model-state。

- A：["dock-base","gantry","trolley","hoist","container"]
- B：["gantry"]
- C：["trolley"]
- D：[]

```json
{
  "input": {
    "joints": [
      {
        "id": "gantry-foot-a",
        "name": "Left foundation clamp",
        "type": "fixed",
        "parent": "dock-base",
        "child": "gantry",
        "anchorParent": [
          -4.2,
          0.020000000000000046,
          0
        ],
        "anchorChild": [
          -4.2,
          -4.137103069057987,
          0.6625000000000003
        ]
      },
      {
        "id": "gantry-foot-b",
        "name": "Right foundation clamp",
        "type": "fixed",
        "parent": "dock-base",
        "child": "gantry",
        "anchorParent": [
          4.2,
          0.020000000000000046,
          0
        ],
        "anchorChild": [
          4.2,
          -4.137103069057987,
          0.6625000000000003
        ]
      },
      {
        "id": "trolley-rail",
        "name": "Trolley rail",
        "type": "prismatic",
        "parent": "gantry",
        "child": "trolley",
        "anchorParent": [
          0,
          3.2628969309420137,
          0.6625000000000003
        ],
        "anchorChild": [
          0,
          0.18750000000000006,
          0
        ],
        "axis": [
          1,
          0,
          0
        ],
        "limits": [
          -3.8,
          3.8
        ]
      },
      {
        "id": "hoist-slide",
        "name": "Vertical hoist carriage",
        "type": "prismatic",
        "parent": "trolley",
        "child": "hoist",
        "anchorParent": [
          0.3,
          -0.012499999999999956,
          0
        ],
        "anchorChild": [
          0,
          2.3691025666102217,
          0
        ],
        "axis": [
          0,
          1,
          0
        ],
        "limits": [
          -4.2,
          0
        ]
      },
      {
        "id": "hook-latch",
        "name": "Container hook latch",
        "type": "fixed",
        "parent": "hoist",
        "child": "container",
        "anchorParent": [
          -0.3,
          -1.8308974333897785,
          0
        ],
        "anchorChild": [
          0,
          1.55,
          0
        ]
      }
    ]
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 基座识别（h3-harbor-container-crane-anchor）

哪些模块被声明为固定基座？

能力：基座识别；形式：single-choice；证据：model-state。

- A：["trolley"]
- B：["dock-base"]
- C：[]
- D：["dock-base","gantry","trolley","hoist","container"]

```json
{
  "input": {
    "modules": [
      {
        "id": "dock-base",
        "name": "Harbor rail foundation",
        "role": "foundation",
        "anchored": true,
        "mass": 24,
        "position": [
          0,
          0.6799999999999999,
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
        "id": "gantry",
        "name": "Twin-tower crane gantry",
        "role": "load-frame",
        "anchored": false,
        "mass": 14,
        "position": [
          0,
          4.837103069057987,
          -0.6625000000000003
        ],
        "rotation": [
          0,
          0,
          0,
          1
        ]
      },
      {
        "id": "trolley",
        "name": "Traversing trolley",
        "role": "actuator",
        "anchored": false,
        "mass": 3,
        "position": [
          0,
          7.9125,
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
        "id": "hoist",
        "name": "Hoist and hook block",
        "role": "service-module",
        "anchored": false,
        "mass": 2,
        "position": [
          0.3,
          5.530897433389778,
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
        "id": "container",
        "name": "Intermodal container",
        "role": "payload",
        "anchored": false,
        "mass": 7,
        "position": [
          0,
          2.15,
          0
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
    "choiceId": "B"
  }
}
```

### 接口计数（h3-harbor-container-crane-degree）

trolley 连接几个声明关节？平行关节分别计数。

能力：接口计数；形式：single-choice；证据：model-state。

- A：4
- B：2
- C：3
- D：1

```json
{
  "input": {
    "joints": [
      {
        "id": "gantry-foot-a",
        "name": "Left foundation clamp",
        "type": "fixed",
        "parent": "dock-base",
        "child": "gantry",
        "anchorParent": [
          -4.2,
          0.020000000000000046,
          0
        ],
        "anchorChild": [
          -4.2,
          -4.137103069057987,
          0.6625000000000003
        ]
      },
      {
        "id": "gantry-foot-b",
        "name": "Right foundation clamp",
        "type": "fixed",
        "parent": "dock-base",
        "child": "gantry",
        "anchorParent": [
          4.2,
          0.020000000000000046,
          0
        ],
        "anchorChild": [
          4.2,
          -4.137103069057987,
          0.6625000000000003
        ]
      },
      {
        "id": "trolley-rail",
        "name": "Trolley rail",
        "type": "prismatic",
        "parent": "gantry",
        "child": "trolley",
        "anchorParent": [
          0,
          3.2628969309420137,
          0.6625000000000003
        ],
        "anchorChild": [
          0,
          0.18750000000000006,
          0
        ],
        "axis": [
          1,
          0,
          0
        ],
        "limits": [
          -3.8,
          3.8
        ]
      },
      {
        "id": "hoist-slide",
        "name": "Vertical hoist carriage",
        "type": "prismatic",
        "parent": "trolley",
        "child": "hoist",
        "anchorParent": [
          0.3,
          -0.012499999999999956,
          0
        ],
        "anchorChild": [
          0,
          2.3691025666102217,
          0
        ],
        "axis": [
          0,
          1,
          0
        ],
        "limits": [
          -4.2,
          0
        ]
      },
      {
        "id": "hook-latch",
        "name": "Container hook latch",
        "type": "fixed",
        "parent": "hoist",
        "child": "container",
        "anchorParent": [
          -0.3,
          -1.8308974333897785,
          0
        ],
        "anchorChild": [
          0,
          1.55,
          0
        ]
      }
    ]
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 局部改色（h3-harbor-container-crane-recolor）

仅将 v0110 改成 #e8792e，其他零件不变。选择正确补丁。

能力：局部改色；形式：single-choice；证据：model-state。

- A：{"id":"v0111","color":"#e8792e"}
- B：{"id":"v0110","color":"#2878b8"}
- C：{"id":"*","color":"#e8792e"}
- D：{"id":"v0110","color":"#e8792e"}

```json
{
  "input": {
    "part": {
      "id": "v0110",
      "moduleId": "trolley",
      "shape": "panel",
      "size": [
        2.2,
        0.7,
        3.4
      ],
      "position": [
        0,
        0.18750000000000006,
        0
      ],
      "rotation": [
        0,
        0,
        0,
        1
      ],
      "color": "#e8792e"
    }
  },
  "answer": {
    "choiceId": "D"
  }
}
```

### 补装部件（h3-harbor-container-crane-add）

模块 trolley 缺失零件 v0110。选择与目标清单一致的补装描述。

能力：补装部件；形式：single-choice；证据：model-state。

- A：{"id":"v0110","moduleId":"trolley","shape":"panel","size":[3,3,3],"position":[0,0.18750000000000006,0],"rotation":[0,0,0,1],"color":"#e8792e"}
- B：{"id":"v0110","moduleId":"trolley","shape":"panel","size":[2.2,0.7,3.4],"position":[0,0.18750000000000006,0],"rotation":[0,0,0,1],"color":"#000000"}
- C：{"id":"v0110","moduleId":"trolley","shape":"panel","size":[2.2,0.7,3.4],"position":[0,0.18750000000000006,0],"rotation":[0,0,0,1],"color":"#e8792e"}
- D：{"id":"v0110","moduleId":"dock-base","shape":"panel","size":[2.2,0.7,3.4],"position":[0,0.18750000000000006,0],"rotation":[0,0,0,1],"color":"#e8792e"}

```json
{
  "input": {
    "targetPart": {
      "id": "v0110",
      "moduleId": "trolley",
      "shape": "panel",
      "size": [
        2.2,
        0.7,
        3.4
      ],
      "position": [
        0,
        0.18750000000000006,
        0
      ],
      "rotation": [
        0,
        0,
        0,
        1
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
      "v0126"
    ]
  },
  "answer": {
    "choiceId": "C"
  }
}
```

### 安全拆除（h3-harbor-container-crane-remove）

按声明依赖图，当前可以先拆哪些叶模块？

能力：安全拆除；形式：single-choice；证据：model-state。

- A：["container"]
- B：["dock-base"]
- C：[]
- D：["dock-base","gantry","trolley","hoist","container"]

```json
{
  "input": {
    "joints": [
      {
        "id": "gantry-foot-a",
        "name": "Left foundation clamp",
        "type": "fixed",
        "parent": "dock-base",
        "child": "gantry",
        "anchorParent": [
          -4.2,
          0.020000000000000046,
          0
        ],
        "anchorChild": [
          -4.2,
          -4.137103069057987,
          0.6625000000000003
        ]
      },
      {
        "id": "gantry-foot-b",
        "name": "Right foundation clamp",
        "type": "fixed",
        "parent": "dock-base",
        "child": "gantry",
        "anchorParent": [
          4.2,
          0.020000000000000046,
          0
        ],
        "anchorChild": [
          4.2,
          -4.137103069057987,
          0.6625000000000003
        ]
      },
      {
        "id": "trolley-rail",
        "name": "Trolley rail",
        "type": "prismatic",
        "parent": "gantry",
        "child": "trolley",
        "anchorParent": [
          0,
          3.2628969309420137,
          0.6625000000000003
        ],
        "anchorChild": [
          0,
          0.18750000000000006,
          0
        ],
        "axis": [
          1,
          0,
          0
        ],
        "limits": [
          -3.8,
          3.8
        ]
      },
      {
        "id": "hoist-slide",
        "name": "Vertical hoist carriage",
        "type": "prismatic",
        "parent": "trolley",
        "child": "hoist",
        "anchorParent": [
          0.3,
          -0.012499999999999956,
          0
        ],
        "anchorChild": [
          0,
          2.3691025666102217,
          0
        ],
        "axis": [
          0,
          1,
          0
        ],
        "limits": [
          -4.2,
          0
        ]
      },
      {
        "id": "hook-latch",
        "name": "Container hook latch",
        "type": "fixed",
        "parent": "hoist",
        "child": "container",
        "anchorParent": [
          -0.3,
          -1.8308974333897785,
          0
        ],
        "anchorChild": [
          0,
          1.55,
          0
        ]
      }
    ],
    "modules": [
      "dock-base",
      "gantry",
      "trolley",
      "hoist",
      "container"
    ]
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 替换选择（h3-harbor-container-crane-replace）

在成本上限内选择刚度最大的替换件；并列选成本低者，再并列选ID字典序最小者。

能力：替换选择；形式：single-choice；证据：model-state。

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
        "cost": 4,
        "stiffness": 9,
        "mass": 1.7
      },
      {
        "id": "stock-1",
        "cost": 3,
        "stiffness": 7,
        "mass": 0.7
      },
      {
        "id": "stock-2",
        "cost": 5,
        "stiffness": 8,
        "mass": 1.1
      },
      {
        "id": "stock-3",
        "cost": 6,
        "stiffness": 7,
        "mass": 1.9
      }
    ],
    "maxCost": 8
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 平移纠偏（h3-harbor-container-crane-translate）

观察到相对目标的平移误差 delta，选择补偿平移。

能力：平移纠偏；形式：single-choice；证据：model-state。

- A：[0,0,0]
- B：[0,2,0]
- C：[-3,0,2]
- D：[3,0,-2]

```json
{
  "input": {
    "delta": [
      3,
      0,
      -2
    ],
    "target": "trolley"
  },
  "answer": {
    "choiceId": "C"
  }
}
```

### 姿态纠偏（h3-harbor-container-crane-rotate）

选择从当前yaw到目标yaw的最短有符号旋转；恰好180°时使用-180°。

能力：姿态纠偏；形式：single-choice；证据：model-state。

- A：45
- B：0
- C：90
- D：-45

```json
{
  "input": {
    "module": "trolley",
    "currentYaw": 45,
    "targetYaw": 0
  },
  "answer": {
    "choiceId": "D"
  }
}
```

### 下一步放置（h3-harbor-container-crane-next-module）

已完成给定前缀，选择所有前置依赖已满足的下一模块集合。

能力：下一步放置；形式：single-choice；证据：model-state。

- A：[]
- B：["dock-base","gantry","trolley"]
- C：["hoist","container"]
- D：["hoist"]

```json
{
  "input": {
    "prefix": [
      "dock-base",
      "gantry",
      "trolley"
    ],
    "joints": [
      {
        "id": "gantry-foot-a",
        "name": "Left foundation clamp",
        "type": "fixed",
        "parent": "dock-base",
        "child": "gantry",
        "anchorParent": [
          -4.2,
          0.020000000000000046,
          0
        ],
        "anchorChild": [
          -4.2,
          -4.137103069057987,
          0.6625000000000003
        ]
      },
      {
        "id": "gantry-foot-b",
        "name": "Right foundation clamp",
        "type": "fixed",
        "parent": "dock-base",
        "child": "gantry",
        "anchorParent": [
          4.2,
          0.020000000000000046,
          0
        ],
        "anchorChild": [
          4.2,
          -4.137103069057987,
          0.6625000000000003
        ]
      },
      {
        "id": "trolley-rail",
        "name": "Trolley rail",
        "type": "prismatic",
        "parent": "gantry",
        "child": "trolley",
        "anchorParent": [
          0,
          3.2628969309420137,
          0.6625000000000003
        ],
        "anchorChild": [
          0,
          0.18750000000000006,
          0
        ],
        "axis": [
          1,
          0,
          0
        ],
        "limits": [
          -3.8,
          3.8
        ]
      },
      {
        "id": "hoist-slide",
        "name": "Vertical hoist carriage",
        "type": "prismatic",
        "parent": "trolley",
        "child": "hoist",
        "anchorParent": [
          0.3,
          -0.012499999999999956,
          0
        ],
        "anchorChild": [
          0,
          2.3691025666102217,
          0
        ],
        "axis": [
          0,
          1,
          0
        ],
        "limits": [
          -4.2,
          0
        ]
      },
      {
        "id": "hook-latch",
        "name": "Container hook latch",
        "type": "fixed",
        "parent": "hoist",
        "child": "container",
        "anchorParent": [
          -0.3,
          -1.8308974333897785,
          0
        ],
        "anchorChild": [
          0,
          1.55,
          0
        ]
      }
    ],
    "modules": [
      "dock-base",
      "gantry",
      "trolley",
      "hoist",
      "container"
    ]
  },
  "answer": {
    "choiceId": "D"
  }
}
```

### 库存核算（h3-harbor-container-crane-inventory）

备件库有 13 件，替换模块需 5 件，还剩多少？

能力：库存核算；形式：single-choice；证据：model-state。

- A：8
- B：9
- C：7
- D：11

```json
{
  "input": {
    "available": 13,
    "required": 5
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 子装配边界（h3-harbor-container-crane-boundary）

隔离 trolley 需要断开哪些边界关节？

能力：子装配边界；形式：single-choice；证据：model-state。

- A：["gantry-foot-a","gantry-foot-b","trolley-rail","hoist-slide","hook-latch"]
- B：["trolley-rail"]
- C：["hoist-slide","trolley-rail"]
- D：[]

```json
{
  "input": {
    "joints": [
      {
        "id": "gantry-foot-a",
        "name": "Left foundation clamp",
        "type": "fixed",
        "parent": "dock-base",
        "child": "gantry",
        "anchorParent": [
          -4.2,
          0.020000000000000046,
          0
        ],
        "anchorChild": [
          -4.2,
          -4.137103069057987,
          0.6625000000000003
        ]
      },
      {
        "id": "gantry-foot-b",
        "name": "Right foundation clamp",
        "type": "fixed",
        "parent": "dock-base",
        "child": "gantry",
        "anchorParent": [
          4.2,
          0.020000000000000046,
          0
        ],
        "anchorChild": [
          4.2,
          -4.137103069057987,
          0.6625000000000003
        ]
      },
      {
        "id": "trolley-rail",
        "name": "Trolley rail",
        "type": "prismatic",
        "parent": "gantry",
        "child": "trolley",
        "anchorParent": [
          0,
          3.2628969309420137,
          0.6625000000000003
        ],
        "anchorChild": [
          0,
          0.18750000000000006,
          0
        ],
        "axis": [
          1,
          0,
          0
        ],
        "limits": [
          -3.8,
          3.8
        ]
      },
      {
        "id": "hoist-slide",
        "name": "Vertical hoist carriage",
        "type": "prismatic",
        "parent": "trolley",
        "child": "hoist",
        "anchorParent": [
          0.3,
          -0.012499999999999956,
          0
        ],
        "anchorChild": [
          0,
          2.3691025666102217,
          0
        ],
        "axis": [
          0,
          1,
          0
        ],
        "limits": [
          -4.2,
          0
        ]
      },
      {
        "id": "hook-latch",
        "name": "Container hook latch",
        "type": "fixed",
        "parent": "hoist",
        "child": "container",
        "anchorParent": [
          -0.3,
          -1.8308974333897785,
          0
        ],
        "anchorChild": [
          0,
          1.55,
          0
        ]
      }
    ],
    "target": "trolley"
  },
  "answer": {
    "choiceId": "C"
  }
}
```

### 最小干预（h3-harbor-container-crane-no-op）

当前模块颜色已满足指令，且无需改变位姿。最少需要几次编辑？

能力：最小干预；形式：single-choice；证据：model-state。

- A：0
- B：1
- C：2
- D：5

```json
{
  "input": {
    "module": "trolley"
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 全过程依赖（h3-harbor-container-crane-prefix）

给定候选顺序，首次违反前置依赖的步骤是？从 0 编号，-1 表示没有违反。

能力：全过程依赖；形式：single-choice；证据：support-graph。

- A：-1
- B：2
- C：4
- D：1

```json
{
  "input": {
    "order": [
      "dock-base",
      "trolley",
      "gantry",
      "hoist",
      "container"
    ],
    "joints": [
      {
        "id": "gantry-foot-a",
        "name": "Left foundation clamp",
        "type": "fixed",
        "parent": "dock-base",
        "child": "gantry",
        "anchorParent": [
          -4.2,
          0.020000000000000046,
          0
        ],
        "anchorChild": [
          -4.2,
          -4.137103069057987,
          0.6625000000000003
        ]
      },
      {
        "id": "gantry-foot-b",
        "name": "Right foundation clamp",
        "type": "fixed",
        "parent": "dock-base",
        "child": "gantry",
        "anchorParent": [
          4.2,
          0.020000000000000046,
          0
        ],
        "anchorChild": [
          4.2,
          -4.137103069057987,
          0.6625000000000003
        ]
      },
      {
        "id": "trolley-rail",
        "name": "Trolley rail",
        "type": "prismatic",
        "parent": "gantry",
        "child": "trolley",
        "anchorParent": [
          0,
          3.2628969309420137,
          0.6625000000000003
        ],
        "anchorChild": [
          0,
          0.18750000000000006,
          0
        ],
        "axis": [
          1,
          0,
          0
        ],
        "limits": [
          -3.8,
          3.8
        ]
      },
      {
        "id": "hoist-slide",
        "name": "Vertical hoist carriage",
        "type": "prismatic",
        "parent": "trolley",
        "child": "hoist",
        "anchorParent": [
          0.3,
          -0.012499999999999956,
          0
        ],
        "anchorChild": [
          0,
          2.3691025666102217,
          0
        ],
        "axis": [
          0,
          1,
          0
        ],
        "limits": [
          -4.2,
          0
        ]
      },
      {
        "id": "hook-latch",
        "name": "Container hook latch",
        "type": "fixed",
        "parent": "hoist",
        "child": "container",
        "anchorParent": [
          -0.3,
          -1.8308974333897785,
          0
        ],
        "anchorChild": [
          0,
          1.55,
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

### 连续维修路径（h3-harbor-container-crane-access）

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
          9.95,
          7.9125,
          0
        ],
        "end": [
          0,
          7.9125,
          0
        ],
        "halfExtents": [
          0.18,
          0.18,
          0.18
        ],
        "clear": false,
        "timeOfImpact": 0.5693007111549377
      },
      {
        "id": "path-1",
        "start": [
          0,
          12.45,
          0
        ],
        "end": [
          0,
          7.9125,
          0
        ],
        "halfExtents": [
          0.18,
          0.18,
          0.18
        ],
        "clear": false,
        "timeOfImpact": 0.9961434006690979
      },
      {
        "id": "path-2",
        "start": [
          0,
          7.9125,
          8.9
        ],
        "end": [
          0,
          7.9125,
          0
        ],
        "halfExtents": [
          0.18,
          0.18,
          0.18
        ],
        "clear": false,
        "timeOfImpact": 0.6960674524307251
      }
    ],
    "simulator": "stud-inclusive conservative cuboids; anchored base; force-limited position servos; no clutch/material calibration"
  },
  "answer": {
    "choiceIds": []
  }
}
```

### 支撑反事实（h3-harbor-container-crane-counterfactual）

移除指定模块后，哪些其余模块失去到任一基座的关节路径？不包含被移除模块本身。

能力：支撑反事实；形式：single-choice；证据：support-graph。

- A：[]
- B：["dock-base","gantry","trolley","hoist","container"]
- C：["container","hoist","trolley"]
- D：["gantry"]

```json
{
  "input": {
    "removed": "gantry",
    "roots": [
      "dock-base"
    ],
    "joints": [
      {
        "id": "gantry-foot-a",
        "name": "Left foundation clamp",
        "type": "fixed",
        "parent": "dock-base",
        "child": "gantry",
        "anchorParent": [
          -4.2,
          0.020000000000000046,
          0
        ],
        "anchorChild": [
          -4.2,
          -4.137103069057987,
          0.6625000000000003
        ]
      },
      {
        "id": "gantry-foot-b",
        "name": "Right foundation clamp",
        "type": "fixed",
        "parent": "dock-base",
        "child": "gantry",
        "anchorParent": [
          4.2,
          0.020000000000000046,
          0
        ],
        "anchorChild": [
          4.2,
          -4.137103069057987,
          0.6625000000000003
        ]
      },
      {
        "id": "trolley-rail",
        "name": "Trolley rail",
        "type": "prismatic",
        "parent": "gantry",
        "child": "trolley",
        "anchorParent": [
          0,
          3.2628969309420137,
          0.6625000000000003
        ],
        "anchorChild": [
          0,
          0.18750000000000006,
          0
        ],
        "axis": [
          1,
          0,
          0
        ],
        "limits": [
          -3.8,
          3.8
        ]
      },
      {
        "id": "hoist-slide",
        "name": "Vertical hoist carriage",
        "type": "prismatic",
        "parent": "trolley",
        "child": "hoist",
        "anchorParent": [
          0.3,
          -0.012499999999999956,
          0
        ],
        "anchorChild": [
          0,
          2.3691025666102217,
          0
        ],
        "axis": [
          0,
          1,
          0
        ],
        "limits": [
          -4.2,
          0
        ]
      },
      {
        "id": "hook-latch",
        "name": "Container hook latch",
        "type": "fixed",
        "parent": "hoist",
        "child": "container",
        "anchorParent": [
          -0.3,
          -1.8308974333897785,
          0
        ],
        "anchorChild": [
          0,
          1.55,
          0
        ]
      }
    ],
    "modules": [
      "dock-base",
      "gantry",
      "trolley",
      "hoist",
      "container"
    ]
  },
  "answer": {
    "choiceId": "C"
  }
}
```

### 冲击响应读数（h3-harbor-container-crane-dynamic）

Rapier 实际采样轨迹中的最大平移位移是多少？按四位小数报告。

能力：冲击响应读数；形式：single-choice；证据：Rapier。

- A：0
- B：1.0043
- C：0.0043
- D：0.2043

```json
{
  "input": {
    "trace": [
      {
        "time": 0.008333333333333333,
        "displacement": 0.004321440985635097
      },
      {
        "time": 0.10833333333333334,
        "displacement": 0.000012183335378857263
      },
      {
        "time": 0.20833333333333334,
        "displacement": 0.0000016690599142641242
      },
      {
        "time": 0.30833333333333335,
        "displacement": 0.0000016692234428857258
      },
      {
        "time": 0.4083333333333333,
        "displacement": 0.0000016692038024236008
      },
      {
        "time": 0.5083333333333333,
        "displacement": 0.000001669214048148673
      },
      {
        "time": 0.6083333333333333,
        "displacement": 0.0000016692183299248337
      },
      {
        "time": 0.7083333333333334,
        "displacement": 0.0000016692183299248337
      },
      {
        "time": 0.8083333333333333,
        "displacement": 0.0000016692183299248337
      },
      {
        "time": 0.9083333333333333,
        "displacement": 0.0000016692183299248337
      },
      {
        "time": 1,
        "displacement": 0.0000016692183299248337
      }
    ],
    "impulse": [
      10,
      1.8,
      3.5
    ],
    "nominalDrift": 0.0014294624339031383,
    "scope": "采样轨迹极值，非连续时间极值；不代表实物安全阈值"
  },
  "answer": {
    "choiceId": "C"
  }
}
```

### 关节限位推理（h3-harbor-container-crane-kinematic）

下列目标位置/角度中哪些在关节声明限位内（含边界）？

能力：关节限位推理；形式：multiple-choice；证据：model-state。

- A：0
- B：-4.3
- C：4.3
- D：-3.8

```json
{
  "input": {
    "joint": "trolley-rail",
    "limits": [
      -3.8,
      3.8
    ],
    "units": "scene units"
  },
  "answer": {
    "choiceIds": [
      "A",
      "D"
    ]
  }
}
```

### 约束故障诊断（h3-harbor-container-crane-diagnosis）

已检测到端点和约束类型如下，选择匹配的全部关节。

能力：约束故障诊断；形式：multiple-choice；证据：model-state。

- A：trolley-rail
- B：hook-latch
- C：gantry-foot-a
- D：gantry-foot-b

```json
{
  "input": {
    "endpoints": [
      "hoist",
      "container"
    ],
    "type": "fixed",
    "joints": [
      {
        "id": "gantry-foot-a",
        "name": "Left foundation clamp",
        "type": "fixed",
        "parent": "dock-base",
        "child": "gantry",
        "anchorParent": [
          -4.2,
          0.020000000000000046,
          0
        ],
        "anchorChild": [
          -4.2,
          -4.137103069057987,
          0.6625000000000003
        ]
      },
      {
        "id": "gantry-foot-b",
        "name": "Right foundation clamp",
        "type": "fixed",
        "parent": "dock-base",
        "child": "gantry",
        "anchorParent": [
          4.2,
          0.020000000000000046,
          0
        ],
        "anchorChild": [
          4.2,
          -4.137103069057987,
          0.6625000000000003
        ]
      },
      {
        "id": "trolley-rail",
        "name": "Trolley rail",
        "type": "prismatic",
        "parent": "gantry",
        "child": "trolley",
        "anchorParent": [
          0,
          3.2628969309420137,
          0.6625000000000003
        ],
        "anchorChild": [
          0,
          0.18750000000000006,
          0
        ],
        "axis": [
          1,
          0,
          0
        ],
        "limits": [
          -3.8,
          3.8
        ]
      },
      {
        "id": "hoist-slide",
        "name": "Vertical hoist carriage",
        "type": "prismatic",
        "parent": "trolley",
        "child": "hoist",
        "anchorParent": [
          0.3,
          -0.012499999999999956,
          0
        ],
        "anchorChild": [
          0,
          2.3691025666102217,
          0
        ],
        "axis": [
          0,
          1,
          0
        ],
        "limits": [
          -4.2,
          0
        ]
      },
      {
        "id": "hook-latch",
        "name": "Container hook latch",
        "type": "fixed",
        "parent": "hoist",
        "child": "container",
        "anchorParent": [
          -0.3,
          -1.8308974333897785,
          0
        ],
        "anchorChild": [
          0,
          1.55,
          0
        ]
      }
    ]
  },
  "answer": {
    "choiceIds": [
      "B"
    ]
  }
}
```

### 主动检查收益（h3-harbor-container-crane-information-gain）

均匀先验四个世界，选择信息增益/成本最大的全部检查。

能力：主动检查收益；形式：multiple-choice；证据：finite-world。

- A：query-1
- B：query-0
- C：query-2

```json
{
  "input": {
    "queries": [
      {
        "id": "query-0",
        "cost": 3,
        "returns": [
          0,
          0,
          1,
          1
        ]
      },
      {
        "id": "query-1",
        "cost": 1,
        "returns": [
          0,
          1,
          2,
          3
        ]
      },
      {
        "id": "query-2",
        "cost": 2,
        "returns": [
          0,
          0,
          0,
          1
        ]
      }
    ],
    "module": "trolley",
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

### 不确定性与弃答（h3-harbor-container-crane-abstention）

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

### 观测后信念更新（h3-harbor-container-crane-posterior）

均匀先验，得到给定观测后，jammed 世界的后验概率是多少？

能力：观测后信念更新；形式：single-choice；证据：finite-world。

- A：0.5
- B：0
- C：0.25
- D：0.3333333333333333

```json
{
  "input": {
    "module": "trolley",
    "worlds": [
      "normal",
      "jammed",
      "reversed",
      "loose"
    ],
    "observationByWorld": [
      "positive",
      "negative",
      "negative",
      "positive"
    ],
    "observed": "negative"
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 多目标工程权衡（h3-harbor-container-crane-pareto）

最小成本、最小质量、最大刚度，选择完整非支配集合。

能力：多目标工程权衡；形式：multiple-choice；证据：model-state。

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
        "cost": 4,
        "stiffness": 9,
        "mass": 1.7
      },
      {
        "id": "stock-1",
        "cost": 3,
        "stiffness": 7,
        "mass": 0.7
      },
      {
        "id": "stock-2",
        "cost": 5,
        "stiffness": 8,
        "mass": 1.1
      },
      {
        "id": "stock-3",
        "cost": 6,
        "stiffness": 7,
        "mass": 1.9
      }
    ]
  },
  "answer": {
    "choiceIds": [
      "A",
      "B",
      "D"
    ]
  }
}
```

### 依赖装配（h3-harbor-container-crane-assembly）

提交 actionIds。执行公开前置条件与效果，达到所有目标且不超过预算；允许交换独立动作。

能力：依赖装配；形式：actions；证据：state-machine。


```json
{
  "input": {
    "initialFacts": [],
    "initialModules": [],
    "actions": [
      {
        "id": "place:trolley",
        "label": "安装 trolley",
        "requires": [
          "present:gantry"
        ],
        "forbids": [
          "present:trolley"
        ],
        "adds": [
          "present:trolley"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "trolley",
          "visible": true
        }
      },
      {
        "id": "place:gantry",
        "label": "安装 gantry",
        "requires": [
          "present:dock-base",
          "present:dock-base"
        ],
        "forbids": [
          "present:gantry"
        ],
        "adds": [
          "present:gantry"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "gantry",
          "visible": true
        }
      },
      {
        "id": "place:dock-base",
        "label": "安装 dock-base",
        "requires": [],
        "forbids": [
          "present:dock-base"
        ],
        "adds": [
          "present:dock-base"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "dock-base",
          "visible": true
        }
      },
      {
        "id": "place:container",
        "label": "安装 container",
        "requires": [
          "present:hoist"
        ],
        "forbids": [
          "present:container"
        ],
        "adds": [
          "present:container"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "container",
          "visible": true
        }
      },
      {
        "id": "place:hoist",
        "label": "安装 hoist",
        "requires": [
          "present:trolley"
        ],
        "forbids": [
          "present:hoist"
        ],
        "adds": [
          "present:hoist"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "hoist",
          "visible": true
        }
      }
    ],
    "goalFacts": [
      "present:dock-base",
      "present:gantry",
      "present:trolley",
      "present:hoist",
      "present:container"
    ],
    "budget": 5,
    "semantics": "requires must hold; forbids must be absent; effects apply in order; unit action cost"
  },
  "answer": {
    "actionIds": [
      "place:dock-base",
      "place:gantry",
      "place:trolley",
      "place:hoist",
      "place:container"
    ]
  }
}
```

### 依赖拆解（h3-harbor-container-crane-disassembly）

提交 actionIds。执行公开前置条件与效果，达到所有目标且不超过预算；允许交换独立动作。

能力：依赖拆解；形式：actions；证据：state-machine。


```json
{
  "input": {
    "initialFacts": [
      "present:dock-base",
      "present:gantry",
      "present:trolley",
      "present:hoist",
      "present:container"
    ],
    "initialModules": [
      "dock-base",
      "gantry",
      "trolley",
      "hoist",
      "container"
    ],
    "actions": [
      {
        "id": "remove:hoist",
        "label": "拆除 hoist",
        "requires": [
          "present:hoist"
        ],
        "forbids": [
          "present:container"
        ],
        "adds": [
          "removed:hoist"
        ],
        "deletes": [
          "present:hoist"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "hoist",
          "visible": false
        }
      },
      {
        "id": "remove:container",
        "label": "拆除 container",
        "requires": [
          "present:container"
        ],
        "forbids": [],
        "adds": [
          "removed:container"
        ],
        "deletes": [
          "present:container"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "container",
          "visible": false
        }
      },
      {
        "id": "remove:gantry",
        "label": "拆除 gantry",
        "requires": [
          "present:gantry"
        ],
        "forbids": [
          "present:trolley"
        ],
        "adds": [
          "removed:gantry"
        ],
        "deletes": [
          "present:gantry"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "gantry",
          "visible": false
        }
      },
      {
        "id": "remove:dock-base",
        "label": "拆除 dock-base",
        "requires": [
          "present:dock-base"
        ],
        "forbids": [
          "present:gantry",
          "present:gantry"
        ],
        "adds": [
          "removed:dock-base"
        ],
        "deletes": [
          "present:dock-base"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "dock-base",
          "visible": false
        }
      },
      {
        "id": "remove:trolley",
        "label": "拆除 trolley",
        "requires": [
          "present:trolley"
        ],
        "forbids": [
          "present:hoist"
        ],
        "adds": [
          "removed:trolley"
        ],
        "deletes": [
          "present:trolley"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "trolley",
          "visible": false
        }
      }
    ],
    "goalFacts": [
      "removed:container",
      "removed:hoist",
      "removed:trolley",
      "removed:gantry",
      "removed:dock-base"
    ],
    "budget": 5,
    "semantics": "requires must hold; forbids must be absent; effects apply in order; unit action cost"
  },
  "answer": {
    "actionIds": [
      "remove:container",
      "remove:hoist",
      "remove:trolley",
      "remove:gantry",
      "remove:dock-base"
    ]
  }
}
```

### 承载维修（h3-harbor-container-crane-service-repair）

提交 actionIds。执行公开前置条件与效果，达到所有目标且不超过预算；允许交换独立动作。

能力：承载维修；形式：actions；证据：state-machine。


```json
{
  "input": {
    "initialFacts": [
      "fault:trolley",
      "closed:trolley"
    ],
    "initialModules": [
      "dock-base",
      "gantry",
      "trolley",
      "hoist",
      "container"
    ],
    "actions": [
      {
        "id": "verify:trolley",
        "label": "verify trolley",
        "requires": [
          "done:replace:trolley"
        ],
        "forbids": [
          "done:verify:trolley"
        ],
        "adds": [
          "done:verify:trolley"
        ],
        "deletes": [
          "fault:trolley"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "trolley"
        }
      },
      {
        "id": "close:trolley",
        "label": "close trolley",
        "requires": [
          "done:verify:trolley"
        ],
        "forbids": [
          "done:close:trolley"
        ],
        "adds": [
          "done:close:trolley"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "trolley"
        }
      },
      {
        "id": "support:trolley",
        "label": "support trolley",
        "requires": [
          "fault:trolley"
        ],
        "forbids": [
          "done:support:trolley"
        ],
        "adds": [
          "done:support:trolley"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "trolley"
        }
      },
      {
        "id": "release:trolley",
        "label": "release trolley",
        "requires": [
          "done:close:trolley"
        ],
        "forbids": [
          "done:release:trolley"
        ],
        "adds": [
          "done:release:trolley",
          "repaired:trolley"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "trolley"
        }
      },
      {
        "id": "replace:trolley",
        "label": "replace trolley",
        "requires": [
          "done:remove:trolley"
        ],
        "forbids": [
          "done:replace:trolley"
        ],
        "adds": [
          "done:replace:trolley"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "trolley",
          "visible": true
        }
      },
      {
        "id": "remove:trolley",
        "label": "remove trolley",
        "requires": [
          "done:open:trolley"
        ],
        "forbids": [
          "done:remove:trolley"
        ],
        "adds": [
          "done:remove:trolley"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "trolley",
          "visible": false
        }
      },
      {
        "id": "open:trolley",
        "label": "open trolley",
        "requires": [
          "done:support:trolley"
        ],
        "forbids": [
          "done:open:trolley"
        ],
        "adds": [
          "done:open:trolley"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "trolley"
        }
      }
    ],
    "goalFacts": [
      "repaired:trolley"
    ],
    "budget": 7,
    "semantics": "requires must hold; forbids must be absent; effects apply in order; unit action cost"
  },
  "answer": {
    "actionIds": [
      "support:trolley",
      "open:trolley",
      "remove:trolley",
      "replace:trolley",
      "verify:trolley",
      "close:trolley",
      "release:trolley"
    ]
  }
}
```

### 复合编辑验证（h3-harbor-container-crane-compound-edit）

提交 actionIds。执行公开前置条件与效果，达到所有目标且不超过预算；允许交换独立动作。

能力：复合编辑验证；形式：actions；证据：state-machine。


```json
{
  "input": {
    "initialFacts": [
      "fault:trolley",
      "closed:trolley"
    ],
    "initialModules": [
      "dock-base",
      "gantry",
      "trolley",
      "hoist",
      "container"
    ],
    "actions": [
      {
        "id": "verify:trolley",
        "label": "verify trolley",
        "requires": [
          "done:recolor:trolley"
        ],
        "forbids": [
          "done:verify:trolley"
        ],
        "adds": [
          "done:verify:trolley"
        ],
        "deletes": [
          "fault:trolley"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "trolley"
        }
      },
      {
        "id": "close:trolley",
        "label": "close trolley",
        "requires": [
          "done:verify:trolley"
        ],
        "forbids": [
          "done:close:trolley"
        ],
        "adds": [
          "done:close:trolley"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "trolley"
        }
      },
      {
        "id": "support:trolley",
        "label": "support trolley",
        "requires": [
          "fault:trolley"
        ],
        "forbids": [
          "done:support:trolley"
        ],
        "adds": [
          "done:support:trolley"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "trolley"
        }
      },
      {
        "id": "recolor:trolley",
        "label": "recolor trolley",
        "requires": [
          "done:open:trolley"
        ],
        "forbids": [
          "done:recolor:trolley"
        ],
        "adds": [
          "done:recolor:trolley"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "trolley",
          "color": "#ea7635"
        }
      },
      {
        "id": "release:trolley",
        "label": "release trolley",
        "requires": [
          "done:close:trolley"
        ],
        "forbids": [
          "done:release:trolley"
        ],
        "adds": [
          "done:release:trolley",
          "repaired:trolley"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "trolley"
        }
      },
      {
        "id": "open:trolley",
        "label": "open trolley",
        "requires": [
          "done:support:trolley"
        ],
        "forbids": [
          "done:open:trolley"
        ],
        "adds": [
          "done:open:trolley"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "trolley"
        }
      }
    ],
    "goalFacts": [
      "repaired:trolley"
    ],
    "budget": 6,
    "semantics": "requires must hold; forbids must be absent; effects apply in order; unit action cost"
  },
  "answer": {
    "actionIds": [
      "support:trolley",
      "open:trolley",
      "recolor:trolley",
      "verify:trolley",
      "close:trolley",
      "release:trolley"
    ]
  }
}
```

### 跨区域联合维修（h3-harbor-container-crane-multi-fault）

提交 actionIds。执行公开前置条件与效果，达到所有目标且不超过预算；允许交换独立动作。

能力：跨区域联合维修；形式：actions；证据：state-machine。


```json
{
  "input": {
    "initialFacts": [
      "fault:trolley",
      "closed:trolley",
      "fault:hoist",
      "closed:hoist",
      "fault:container",
      "closed:container"
    ],
    "initialModules": [
      "dock-base",
      "gantry",
      "trolley",
      "hoist",
      "container"
    ],
    "actions": [
      {
        "id": "release:hoist",
        "label": "release hoist",
        "requires": [
          "done:close:hoist"
        ],
        "forbids": [
          "done:release:hoist"
        ],
        "adds": [
          "done:release:hoist",
          "repaired:hoist"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "hoist"
        }
      },
      {
        "id": "verify:trolley",
        "label": "verify trolley",
        "requires": [
          "done:replace:trolley"
        ],
        "forbids": [
          "done:verify:trolley"
        ],
        "adds": [
          "done:verify:trolley"
        ],
        "deletes": [
          "fault:trolley"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "trolley"
        }
      },
      {
        "id": "support:hoist",
        "label": "support hoist",
        "requires": [
          "fault:hoist"
        ],
        "forbids": [
          "done:support:hoist"
        ],
        "adds": [
          "done:support:hoist"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "hoist"
        }
      },
      {
        "id": "open:container",
        "label": "open container",
        "requires": [
          "done:support:container"
        ],
        "forbids": [
          "done:open:container"
        ],
        "adds": [
          "done:open:container"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "container"
        }
      },
      {
        "id": "release:container",
        "label": "release container",
        "requires": [
          "done:close:container"
        ],
        "forbids": [
          "done:release:container"
        ],
        "adds": [
          "done:release:container",
          "repaired:container"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "container"
        }
      },
      {
        "id": "close:trolley",
        "label": "close trolley",
        "requires": [
          "done:verify:trolley"
        ],
        "forbids": [
          "done:close:trolley"
        ],
        "adds": [
          "done:close:trolley"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "trolley"
        }
      },
      {
        "id": "support:trolley",
        "label": "support trolley",
        "requires": [
          "fault:trolley"
        ],
        "forbids": [
          "done:support:trolley"
        ],
        "adds": [
          "done:support:trolley"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "trolley"
        }
      },
      {
        "id": "replace:hoist",
        "label": "replace hoist",
        "requires": [
          "done:remove:hoist"
        ],
        "forbids": [
          "done:replace:hoist"
        ],
        "adds": [
          "done:replace:hoist"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "hoist",
          "visible": true
        }
      },
      {
        "id": "remove:hoist",
        "label": "remove hoist",
        "requires": [
          "done:open:hoist"
        ],
        "forbids": [
          "done:remove:hoist"
        ],
        "adds": [
          "done:remove:hoist"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "hoist",
          "visible": false
        }
      },
      {
        "id": "verify:hoist",
        "label": "verify hoist",
        "requires": [
          "done:replace:hoist"
        ],
        "forbids": [
          "done:verify:hoist"
        ],
        "adds": [
          "done:verify:hoist"
        ],
        "deletes": [
          "fault:hoist"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "hoist"
        }
      },
      {
        "id": "remove:container",
        "label": "remove container",
        "requires": [
          "done:open:container"
        ],
        "forbids": [
          "done:remove:container"
        ],
        "adds": [
          "done:remove:container"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "container",
          "visible": false
        }
      },
      {
        "id": "support:container",
        "label": "support container",
        "requires": [
          "fault:container"
        ],
        "forbids": [
          "done:support:container"
        ],
        "adds": [
          "done:support:container"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "container"
        }
      },
      {
        "id": "replace:container",
        "label": "replace container",
        "requires": [
          "done:remove:container"
        ],
        "forbids": [
          "done:replace:container"
        ],
        "adds": [
          "done:replace:container"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "container",
          "visible": true
        }
      },
      {
        "id": "release:trolley",
        "label": "release trolley",
        "requires": [
          "done:close:trolley"
        ],
        "forbids": [
          "done:release:trolley"
        ],
        "adds": [
          "done:release:trolley",
          "repaired:trolley"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "trolley"
        }
      },
      {
        "id": "close:hoist",
        "label": "close hoist",
        "requires": [
          "done:verify:hoist"
        ],
        "forbids": [
          "done:close:hoist"
        ],
        "adds": [
          "done:close:hoist"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "hoist"
        }
      },
      {
        "id": "verify:container",
        "label": "verify container",
        "requires": [
          "done:replace:container"
        ],
        "forbids": [
          "done:verify:container"
        ],
        "adds": [
          "done:verify:container"
        ],
        "deletes": [
          "fault:container"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "container"
        }
      },
      {
        "id": "open:hoist",
        "label": "open hoist",
        "requires": [
          "done:support:hoist"
        ],
        "forbids": [
          "done:open:hoist"
        ],
        "adds": [
          "done:open:hoist"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "hoist"
        }
      },
      {
        "id": "replace:trolley",
        "label": "replace trolley",
        "requires": [
          "done:remove:trolley"
        ],
        "forbids": [
          "done:replace:trolley"
        ],
        "adds": [
          "done:replace:trolley"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "trolley",
          "visible": true
        }
      },
      {
        "id": "close:container",
        "label": "close container",
        "requires": [
          "done:verify:container"
        ],
        "forbids": [
          "done:close:container"
        ],
        "adds": [
          "done:close:container"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "container"
        }
      },
      {
        "id": "remove:trolley",
        "label": "remove trolley",
        "requires": [
          "done:open:trolley"
        ],
        "forbids": [
          "done:remove:trolley"
        ],
        "adds": [
          "done:remove:trolley"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "trolley",
          "visible": false
        }
      },
      {
        "id": "open:trolley",
        "label": "open trolley",
        "requires": [
          "done:support:trolley"
        ],
        "forbids": [
          "done:open:trolley"
        ],
        "adds": [
          "done:open:trolley"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "trolley"
        }
      }
    ],
    "goalFacts": [
      "repaired:trolley",
      "repaired:hoist",
      "repaired:container"
    ],
    "budget": 21,
    "semantics": "requires must hold; forbids must be absent; effects apply in order; unit action cost"
  },
  "answer": {
    "actionIds": [
      "support:hoist",
      "support:trolley",
      "support:container",
      "open:container",
      "remove:container",
      "replace:container",
      "verify:container",
      "open:hoist",
      "remove:hoist",
      "replace:hoist",
      "verify:hoist",
      "close:hoist",
      "release:hoist",
      "close:container",
      "release:container",
      "open:trolley",
      "remove:trolley",
      "replace:trolley",
      "verify:trolley",
      "close:trolley",
      "release:trolley"
    ]
  }
}
```

### 多工位资源调度（h3-harbor-container-crane-scheduling）

为所有工单提交整数 starts，满足先后关系、独占工位及截止时间。

能力：多工位资源调度；形式：schedule；证据：resource-schedule。


```json
{
  "input": {
    "jobs": [
      {
        "id": "job-0",
        "module": "dock-base",
        "duration": 3,
        "resource": "test-bench",
        "after": []
      },
      {
        "id": "job-1",
        "module": "gantry",
        "duration": 2,
        "resource": "technician",
        "after": []
      },
      {
        "id": "job-2",
        "module": "trolley",
        "duration": 2,
        "resource": "test-bench",
        "after": [
          "job-0"
        ]
      },
      {
        "id": "job-3",
        "module": "hoist",
        "duration": 2,
        "resource": "technician",
        "after": [
          "job-1"
        ]
      },
      {
        "id": "job-4",
        "module": "container",
        "duration": 1,
        "resource": "test-bench",
        "after": [
          "job-2"
        ]
      }
    ],
    "deadline": 6
  },
  "answer": {
    "starts": {
      "job-0": 0,
      "job-1": 0,
      "job-2": 3,
      "job-3": 2,
      "job-4": 5
    }
  }
}
```

### 检查后条件策略（h3-harbor-container-crane-policy）

提交一个检查及 observation→action 决策表，在所有相容世界中采取正确动作。

能力：检查后条件策略；形式：policy；证据：finite-world。


```json
{
  "input": {
    "module": "trolley",
    "worlds": [
      {
        "id": "normal",
        "action": "replace"
      },
      {
        "id": "loose",
        "action": "continue"
      },
      {
        "id": "jammed",
        "action": "tighten"
      }
    ],
    "budget": 3,
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
          "normal": "same",
          "loose": "same",
          "jammed": "other"
        }
      },
      {
        "id": "thermal",
        "cost": 3,
        "returns": {
          "normal": "signal-0",
          "loose": "signal-1",
          "jammed": "signal-2"
        }
      }
    ]
  },
  "answer": {
    "queryId": "thermal",
    "decisions": {
      "signal-0": "replace",
      "signal-1": "continue",
      "signal-2": "tighten"
    }
  }
}
```

### 局部坐标变换（h3-harbor-container-crane-local-frame）

将模块局部点通过给定四元数与平移转换为世界点，保留五位小数。

能力：局部坐标变换；形式：single-choice；证据：model-state。

- A：[0,8.1,-1]
- B：[1,0.1875,0]
- C：[1,8.1,0]
- D：[1,9.1,0]

```json
{
  "input": {
    "localPoint": [
      1,
      0.18750000000000006,
      0
    ],
    "rotationXYZW": [
      0,
      0.7071067811865475,
      0,
      0.7071067811865476
    ],
    "translation": [
      0,
      7.9125,
      0
    ]
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 正交视图投影（h3-harbor-container-crane-projection）

按公开视图坐标约定，选择该世界点投影后的二维坐标。

能力：正交视图投影；形式：single-choice；证据：model-state。

- A：[9,4]
- B：[4,5]
- C：[0,0]
- D：[4,-5]

```json
{
  "input": {
    "view": "top",
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

### 空间相对关系（h3-harbor-container-crane-relative-order）

比较B相对A在指定世界轴上的模块原点坐标。

能力：空间相对关系；形式：single-choice；证据：model-state。

- A：greater
- B：less
- C：equal

```json
{
  "input": {
    "A": {
      "id": "dock-base",
      "position": [
        0,
        0.6799999999999999,
        0
      ]
    },
    "B": {
      "id": "container",
      "position": [
        0,
        2.15,
        0
      ]
    },
    "axis": "z"
  },
  "answer": {
    "choiceId": "C"
  }
}
```

### 约束自由度（h3-harbor-container-crane-joint-axis）

仅考虑这一声明约束，不计闭环、马达与限位激活，保留多少相对运动自由度？弹簧仅施力、不消除自由度。

能力：约束自由度；形式：single-choice；证据：model-state。

- A：0
- B：1
- C：3
- D：6

```json
{
  "input": {
    "joint": {
      "id": "gantry-foot-b",
      "name": "Right foundation clamp",
      "type": "fixed",
      "parent": "dock-base",
      "child": "gantry",
      "anchorParent": [
        4.2,
        0.020000000000000046,
        0
      ],
      "anchorChild": [
        4.2,
        -4.137103069057987,
        0.6625000000000003
      ]
    }
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 维修间隙预算（h3-harbor-container-crane-clearance-margin）

给定理想直槽净宽、工具宽度、单侧安全余量，工具是否满足横向间隙要求？

能力：维修间隙预算；形式：single-choice；证据：model-state。

- A：feasible
- B：blocked

```json
{
  "input": {
    "module": "trolley",
    "aperture": 0.79,
    "toolWidth": 0.55,
    "eachSideMargin": 0.1
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 载荷力矩（h3-harbor-container-crane-load-moment）

绕给定原点的载荷力矩r×F是多少？采用右手系，忽略其他力。

能力：载荷力矩；形式：single-choice；证据：model-state。

- A：[0,-3,0]
- B：[0,0,-9]
- C：[0,0,9]
- D：[0,0,0]

```json
{
  "input": {
    "module": "trolley",
    "lever": [
      3,
      3,
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
    "choiceId": "B"
  }
}
```

### 非均匀先验更新（h3-harbor-container-crane-weighted-posterior）

先验权重未归一化，观测只保留normal和jammed，求jammed后验概率。

能力：非均匀先验更新；形式：single-choice；证据：finite-world。

- A：1
- B：0.7142857142857143
- C：0.45454545454545453
- D：0

```json
{
  "input": {
    "module": "trolley",
    "worlds": [
      "normal",
      "jammed",
      "loose"
    ],
    "weights": [
      2,
      5,
      4
    ],
    "compatible": [
      "normal",
      "jammed"
    ]
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 风险最小决策（h3-harbor-container-crane-expected-loss）

继续运行期望损失=p×failureLoss，预防维修损失=repairCost，选择损失较低者；并列选继续。

能力：风险最小决策；形式：single-choice；证据：finite-world。

- A：repair
- B：continue

```json
{
  "input": {
    "faultProbability": 0.2,
    "repairCost": 6,
    "failureLoss": 13,
    "module": "trolley"
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 轨迹阈值判定（h3-harbor-container-crane-trace-threshold）

实际采样轨迹中是否有位移严格超过给定阈值？只评价采样点。

能力：轨迹阈值判定；形式：single-choice；证据：Rapier。

- A：within
- B：exceeded

```json
{
  "input": {
    "trace": [
      {
        "time": 0.008333333333333333,
        "displacement": 0.004321440985635097
      },
      {
        "time": 0.10833333333333334,
        "displacement": 0.000012183335378857263
      },
      {
        "time": 0.20833333333333334,
        "displacement": 0.0000016690599142641242
      },
      {
        "time": 0.30833333333333335,
        "displacement": 0.0000016692234428857258
      },
      {
        "time": 0.4083333333333333,
        "displacement": 0.0000016692038024236008
      },
      {
        "time": 0.5083333333333333,
        "displacement": 0.000001669214048148673
      },
      {
        "time": 0.6083333333333333,
        "displacement": 0.0000016692183299248337
      },
      {
        "time": 0.7083333333333334,
        "displacement": 0.0000016692183299248337
      },
      {
        "time": 0.8083333333333333,
        "displacement": 0.0000016692183299248337
      },
      {
        "time": 0.9083333333333333,
        "displacement": 0.0000016692183299248337
      },
      {
        "time": 1,
        "displacement": 0.0000016692183299248337
      }
    ],
    "threshold": 0.005185729182762116
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 安全联锁维修（h3-harbor-container-crane-guarded-repair）

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
        "id": "release:trolley",
        "label": "release trolley",
        "requires": [
          "done:relock:trolley"
        ],
        "forbids": [
          "done:release:trolley"
        ],
        "adds": [
          "done:release:trolley",
          "ready:trolley",
          "tool:free"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "trolley"
        }
      },
      {
        "id": "relock:trolley",
        "label": "relock trolley",
        "requires": [
          "done:verify:trolley"
        ],
        "forbids": [
          "done:relock:trolley"
        ],
        "adds": [
          "done:relock:trolley"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "trolley"
        }
      },
      {
        "id": "verify:trolley",
        "label": "verify trolley",
        "requires": [
          "done:replace:trolley"
        ],
        "forbids": [
          "done:verify:trolley"
        ],
        "adds": [
          "done:verify:trolley"
        ],
        "deletes": [
          "fault:trolley",
          "misaligned:trolley"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "trolley"
        }
      },
      {
        "id": "replace:trolley",
        "label": "replace trolley",
        "requires": [
          "done:unlock:trolley"
        ],
        "forbids": [
          "done:replace:trolley"
        ],
        "adds": [
          "done:replace:trolley"
        ],
        "deletes": [],
        "cost": 2,
        "visual": {
          "moduleId": "trolley"
        }
      },
      {
        "id": "unlock:trolley",
        "label": "unlock trolley",
        "requires": [
          "done:support:trolley"
        ],
        "forbids": [
          "done:unlock:trolley"
        ],
        "adds": [
          "done:unlock:trolley"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "trolley"
        }
      },
      {
        "id": "support:trolley",
        "label": "support trolley",
        "requires": [
          "done:isolate:trolley"
        ],
        "forbids": [
          "done:support:trolley"
        ],
        "adds": [
          "done:support:trolley"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "trolley"
        }
      },
      {
        "id": "isolate:trolley",
        "label": "isolate trolley",
        "requires": [
          "tool:free",
          "fault:trolley"
        ],
        "forbids": [
          "done:isolate:trolley"
        ],
        "adds": [
          "done:isolate:trolley"
        ],
        "deletes": [
          "tool:free"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "trolley"
        }
      }
    ],
    "initialFacts": [
      "tool:free",
      "fault:trolley"
    ],
    "initialModules": [
      "dock-base",
      "gantry",
      "trolley",
      "hoist",
      "container"
    ],
    "goalFacts": [
      "ready:trolley"
    ],
    "absentFacts": [
      "unverified"
    ],
    "budget": 8
  },
  "answer": {
    "actionIds": [
      "isolate:trolley",
      "support:trolley",
      "unlock:trolley",
      "replace:trolley",
      "verify:trolley",
      "relock:trolley",
      "release:trolley"
    ]
  }
}
```

### 失败状态回退（h3-harbor-container-crane-rollback）

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
        "id": "resume:trolley",
        "label": "resume trolley",
        "requires": [
          "done:verify:trolley"
        ],
        "forbids": [
          "done:resume:trolley"
        ],
        "adds": [
          "done:resume:trolley",
          "ready:trolley",
          "tool:free"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "trolley"
        }
      },
      {
        "id": "verify:trolley",
        "label": "verify trolley",
        "requires": [
          "done:align:trolley"
        ],
        "forbids": [
          "done:verify:trolley"
        ],
        "adds": [
          "done:verify:trolley"
        ],
        "deletes": [
          "fault:trolley",
          "misaligned:trolley"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "trolley"
        }
      },
      {
        "id": "align:trolley",
        "label": "align trolley",
        "requires": [
          "done:undo:trolley"
        ],
        "forbids": [
          "done:align:trolley"
        ],
        "adds": [
          "done:align:trolley"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "trolley",
          "visible": true
        }
      },
      {
        "id": "undo:trolley",
        "label": "undo trolley",
        "requires": [
          "done:isolate:trolley"
        ],
        "forbids": [
          "done:undo:trolley"
        ],
        "adds": [
          "done:undo:trolley"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "trolley",
          "visible": false
        }
      },
      {
        "id": "isolate:trolley",
        "label": "isolate trolley",
        "requires": [
          "tool:free",
          "fault:trolley"
        ],
        "forbids": [
          "done:isolate:trolley"
        ],
        "adds": [
          "done:isolate:trolley"
        ],
        "deletes": [
          "tool:free"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "trolley"
        }
      }
    ],
    "initialFacts": [
      "tool:free",
      "fault:trolley",
      "misaligned:trolley"
    ],
    "initialModules": [
      "dock-base",
      "gantry",
      "trolley",
      "hoist",
      "container"
    ],
    "goalFacts": [
      "ready:trolley"
    ],
    "absentFacts": [
      "unverified"
    ],
    "budget": 5
  },
  "answer": {
    "actionIds": [
      "isolate:trolley",
      "undo:trolley",
      "align:trolley",
      "verify:trolley",
      "resume:trolley"
    ]
  }
}
```

### 共享工具协同维修（h3-harbor-container-crane-resource-repair）

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
        "id": "release:container",
        "label": "release container",
        "requires": [
          "done:relock:container"
        ],
        "forbids": [
          "done:release:container"
        ],
        "adds": [
          "done:release:container",
          "ready:container",
          "tool:free"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "container"
        }
      },
      {
        "id": "relock:container",
        "label": "relock container",
        "requires": [
          "done:verify:container"
        ],
        "forbids": [
          "done:relock:container"
        ],
        "adds": [
          "done:relock:container"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "container"
        }
      },
      {
        "id": "verify:container",
        "label": "verify container",
        "requires": [
          "done:replace:container"
        ],
        "forbids": [
          "done:verify:container"
        ],
        "adds": [
          "done:verify:container"
        ],
        "deletes": [
          "fault:container",
          "misaligned:container"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "container"
        }
      },
      {
        "id": "replace:container",
        "label": "replace container",
        "requires": [
          "done:unlock:container"
        ],
        "forbids": [
          "done:replace:container"
        ],
        "adds": [
          "done:replace:container"
        ],
        "deletes": [],
        "cost": 2,
        "visual": {
          "moduleId": "container"
        }
      },
      {
        "id": "unlock:container",
        "label": "unlock container",
        "requires": [
          "done:support:container"
        ],
        "forbids": [
          "done:unlock:container"
        ],
        "adds": [
          "done:unlock:container"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "container"
        }
      },
      {
        "id": "support:container",
        "label": "support container",
        "requires": [
          "done:isolate:container"
        ],
        "forbids": [
          "done:support:container"
        ],
        "adds": [
          "done:support:container"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "container"
        }
      },
      {
        "id": "isolate:container",
        "label": "isolate container",
        "requires": [
          "tool:free",
          "fault:container"
        ],
        "forbids": [
          "done:isolate:container"
        ],
        "adds": [
          "done:isolate:container"
        ],
        "deletes": [
          "tool:free"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "container"
        }
      },
      {
        "id": "release:hoist",
        "label": "release hoist",
        "requires": [
          "done:relock:hoist"
        ],
        "forbids": [
          "done:release:hoist"
        ],
        "adds": [
          "done:release:hoist",
          "ready:hoist",
          "tool:free"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "hoist"
        }
      },
      {
        "id": "relock:hoist",
        "label": "relock hoist",
        "requires": [
          "done:verify:hoist"
        ],
        "forbids": [
          "done:relock:hoist"
        ],
        "adds": [
          "done:relock:hoist"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "hoist"
        }
      },
      {
        "id": "verify:hoist",
        "label": "verify hoist",
        "requires": [
          "done:replace:hoist"
        ],
        "forbids": [
          "done:verify:hoist"
        ],
        "adds": [
          "done:verify:hoist"
        ],
        "deletes": [
          "fault:hoist",
          "misaligned:hoist"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "hoist"
        }
      },
      {
        "id": "replace:hoist",
        "label": "replace hoist",
        "requires": [
          "done:unlock:hoist"
        ],
        "forbids": [
          "done:replace:hoist"
        ],
        "adds": [
          "done:replace:hoist"
        ],
        "deletes": [],
        "cost": 2,
        "visual": {
          "moduleId": "hoist"
        }
      },
      {
        "id": "unlock:hoist",
        "label": "unlock hoist",
        "requires": [
          "done:support:hoist"
        ],
        "forbids": [
          "done:unlock:hoist"
        ],
        "adds": [
          "done:unlock:hoist"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "hoist"
        }
      },
      {
        "id": "support:hoist",
        "label": "support hoist",
        "requires": [
          "done:isolate:hoist"
        ],
        "forbids": [
          "done:support:hoist"
        ],
        "adds": [
          "done:support:hoist"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "hoist"
        }
      },
      {
        "id": "isolate:hoist",
        "label": "isolate hoist",
        "requires": [
          "tool:free",
          "fault:hoist"
        ],
        "forbids": [
          "done:isolate:hoist"
        ],
        "adds": [
          "done:isolate:hoist"
        ],
        "deletes": [
          "tool:free"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "hoist"
        }
      },
      {
        "id": "release:trolley",
        "label": "release trolley",
        "requires": [
          "done:relock:trolley"
        ],
        "forbids": [
          "done:release:trolley"
        ],
        "adds": [
          "done:release:trolley",
          "ready:trolley",
          "tool:free"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "trolley"
        }
      },
      {
        "id": "relock:trolley",
        "label": "relock trolley",
        "requires": [
          "done:verify:trolley"
        ],
        "forbids": [
          "done:relock:trolley"
        ],
        "adds": [
          "done:relock:trolley"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "trolley"
        }
      },
      {
        "id": "verify:trolley",
        "label": "verify trolley",
        "requires": [
          "done:replace:trolley"
        ],
        "forbids": [
          "done:verify:trolley"
        ],
        "adds": [
          "done:verify:trolley"
        ],
        "deletes": [
          "fault:trolley",
          "misaligned:trolley"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "trolley"
        }
      },
      {
        "id": "replace:trolley",
        "label": "replace trolley",
        "requires": [
          "done:unlock:trolley"
        ],
        "forbids": [
          "done:replace:trolley"
        ],
        "adds": [
          "done:replace:trolley"
        ],
        "deletes": [],
        "cost": 2,
        "visual": {
          "moduleId": "trolley"
        }
      },
      {
        "id": "unlock:trolley",
        "label": "unlock trolley",
        "requires": [
          "done:support:trolley"
        ],
        "forbids": [
          "done:unlock:trolley"
        ],
        "adds": [
          "done:unlock:trolley"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "trolley"
        }
      },
      {
        "id": "support:trolley",
        "label": "support trolley",
        "requires": [
          "done:isolate:trolley"
        ],
        "forbids": [
          "done:support:trolley"
        ],
        "adds": [
          "done:support:trolley"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "trolley"
        }
      },
      {
        "id": "isolate:trolley",
        "label": "isolate trolley",
        "requires": [
          "tool:free",
          "fault:trolley"
        ],
        "forbids": [
          "done:isolate:trolley"
        ],
        "adds": [
          "done:isolate:trolley"
        ],
        "deletes": [
          "tool:free"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "trolley"
        }
      },
      {
        "id": "release:gantry",
        "label": "release gantry",
        "requires": [
          "done:relock:gantry"
        ],
        "forbids": [
          "done:release:gantry"
        ],
        "adds": [
          "done:release:gantry",
          "ready:gantry",
          "tool:free"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "gantry"
        }
      },
      {
        "id": "relock:gantry",
        "label": "relock gantry",
        "requires": [
          "done:verify:gantry"
        ],
        "forbids": [
          "done:relock:gantry"
        ],
        "adds": [
          "done:relock:gantry"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "gantry"
        }
      },
      {
        "id": "verify:gantry",
        "label": "verify gantry",
        "requires": [
          "done:replace:gantry"
        ],
        "forbids": [
          "done:verify:gantry"
        ],
        "adds": [
          "done:verify:gantry"
        ],
        "deletes": [
          "fault:gantry",
          "misaligned:gantry"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "gantry"
        }
      },
      {
        "id": "replace:gantry",
        "label": "replace gantry",
        "requires": [
          "done:unlock:gantry"
        ],
        "forbids": [
          "done:replace:gantry"
        ],
        "adds": [
          "done:replace:gantry"
        ],
        "deletes": [],
        "cost": 2,
        "visual": {
          "moduleId": "gantry"
        }
      },
      {
        "id": "unlock:gantry",
        "label": "unlock gantry",
        "requires": [
          "done:support:gantry"
        ],
        "forbids": [
          "done:unlock:gantry"
        ],
        "adds": [
          "done:unlock:gantry"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "gantry"
        }
      },
      {
        "id": "support:gantry",
        "label": "support gantry",
        "requires": [
          "done:isolate:gantry"
        ],
        "forbids": [
          "done:support:gantry"
        ],
        "adds": [
          "done:support:gantry"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "gantry"
        }
      },
      {
        "id": "isolate:gantry",
        "label": "isolate gantry",
        "requires": [
          "tool:free",
          "fault:gantry"
        ],
        "forbids": [
          "done:isolate:gantry"
        ],
        "adds": [
          "done:isolate:gantry"
        ],
        "deletes": [
          "tool:free"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "gantry"
        }
      }
    ],
    "initialFacts": [
      "tool:free",
      "fault:gantry",
      "fault:trolley",
      "fault:hoist",
      "fault:container"
    ],
    "initialModules": [
      "dock-base",
      "gantry",
      "trolley",
      "hoist",
      "container"
    ],
    "goalFacts": [
      "ready:gantry",
      "ready:trolley",
      "ready:hoist",
      "ready:container"
    ],
    "absentFacts": [
      "unverified"
    ],
    "budget": 32
  },
  "answer": {
    "actionIds": [
      "isolate:container",
      "support:container",
      "unlock:container",
      "replace:container",
      "verify:container",
      "relock:container",
      "release:container",
      "isolate:hoist",
      "support:hoist",
      "unlock:hoist",
      "replace:hoist",
      "verify:hoist",
      "relock:hoist",
      "release:hoist",
      "isolate:trolley",
      "support:trolley",
      "unlock:trolley",
      "replace:trolley",
      "verify:trolley",
      "relock:trolley",
      "release:trolley",
      "isolate:gantry",
      "support:gantry",
      "unlock:gantry",
      "replace:gantry",
      "verify:gantry",
      "relock:gantry",
      "release:gantry"
    ]
  }
}
```

### 预算约束检查策略（h3-harbor-container-crane-budget-policy）

提交预算内、对所有相容世界均正确的检查决策表。

能力：预算约束检查策略；形式：policy；证据：finite-world。


```json
{
  "input": {
    "module": "trolley",
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
        "cost": 4,
        "returns": {
          "nominal": "clear",
          "fault": "alert"
        }
      },
      {
        "id": "probe",
        "cost": 3,
        "returns": {
          "nominal": "clear",
          "fault": "alert"
        }
      },
      {
        "id": "thermal",
        "cost": 0,
        "returns": {
          "nominal": "clear",
          "fault": "clear"
        }
      }
    ],
    "budget": 3
  },
  "answer": {
    "queryId": "probe",
    "decisions": {
      "clear": "continue",
      "alert": "replace"
    }
  }
}
```

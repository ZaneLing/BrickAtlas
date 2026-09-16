## D3 自适应射电观测站

### 模块识别（h3-adaptive-radio-observatory-identify）

高亮的维修模块对应哪个 ID？

能力：模块识别；形式：single-choice；证据：model-state。

- A：telescope
- B：camera-pack
- C：foundation
- D：dome

```json
{
  "input": {
    "moduleNames": [
      {
        "id": "foundation",
        "name": "Terraced observatory foundation"
      },
      {
        "id": "dome",
        "name": "Rotating segmented dome"
      },
      {
        "id": "telescope",
        "name": "Elevation telescope"
      },
      {
        "id": "camera-pack",
        "name": "Cryogenic camera pack"
      }
    ]
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 部件计数（h3-adaptive-radio-observatory-count）

模块 camera-pack 有多少个可视零件？

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
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "v0002",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "v0003",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "v0004",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "v0005",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "v0006",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "v0007",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "v0008",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "v0009",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "v0010",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "v0011",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "v0012",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "v0013",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "v0014",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "v0015",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "v0016",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "v0017",
        "moduleId": "foundation",
        "shape": "brick",
        "color": "#edf1f2"
      },
      {
        "id": "v0018",
        "moduleId": "foundation",
        "shape": "brick",
        "color": "#edf1f2"
      },
      {
        "id": "v0019",
        "moduleId": "foundation",
        "shape": "brick",
        "color": "#edf1f2"
      },
      {
        "id": "v0020",
        "moduleId": "foundation",
        "shape": "brick",
        "color": "#edf1f2"
      },
      {
        "id": "v0021",
        "moduleId": "foundation",
        "shape": "brick",
        "color": "#edf1f2"
      },
      {
        "id": "v0022",
        "moduleId": "foundation",
        "shape": "brick",
        "color": "#edf1f2"
      },
      {
        "id": "v0023",
        "moduleId": "foundation",
        "shape": "brick",
        "color": "#edf1f2"
      },
      {
        "id": "v0024",
        "moduleId": "foundation",
        "shape": "brick",
        "color": "#edf1f2"
      },
      {
        "id": "v0025",
        "moduleId": "foundation",
        "shape": "brick",
        "color": "#edf1f2"
      },
      {
        "id": "v0026",
        "moduleId": "foundation",
        "shape": "brick",
        "color": "#edf1f2"
      },
      {
        "id": "v0027",
        "moduleId": "foundation",
        "shape": "brick",
        "color": "#edf1f2"
      },
      {
        "id": "v0028",
        "moduleId": "foundation",
        "shape": "brick",
        "color": "#edf1f2"
      },
      {
        "id": "v0029",
        "moduleId": "foundation",
        "shape": "brick",
        "color": "#edf1f2"
      },
      {
        "id": "v0030",
        "moduleId": "foundation",
        "shape": "brick",
        "color": "#edf1f2"
      },
      {
        "id": "v0031",
        "moduleId": "foundation",
        "shape": "brick",
        "color": "#edf1f2"
      },
      {
        "id": "v0032",
        "moduleId": "foundation",
        "shape": "brick",
        "color": "#edf1f2"
      },
      {
        "id": "v0033",
        "moduleId": "foundation",
        "shape": "brick",
        "color": "#8c99a3"
      },
      {
        "id": "v0034",
        "moduleId": "foundation",
        "shape": "brick",
        "color": "#8c99a3"
      },
      {
        "id": "v0035",
        "moduleId": "foundation",
        "shape": "brick",
        "color": "#8c99a3"
      },
      {
        "id": "v0036",
        "moduleId": "foundation",
        "shape": "brick",
        "color": "#8c99a3"
      },
      {
        "id": "v0037",
        "moduleId": "foundation",
        "shape": "brick",
        "color": "#8c99a3"
      },
      {
        "id": "v0038",
        "moduleId": "foundation",
        "shape": "brick",
        "color": "#8c99a3"
      },
      {
        "id": "v0039",
        "moduleId": "foundation",
        "shape": "brick",
        "color": "#8c99a3"
      },
      {
        "id": "v0040",
        "moduleId": "foundation",
        "shape": "brick",
        "color": "#8c99a3"
      },
      {
        "id": "v0041",
        "moduleId": "foundation",
        "shape": "brick",
        "color": "#8c99a3"
      },
      {
        "id": "v0042",
        "moduleId": "foundation",
        "shape": "brick",
        "color": "#8c99a3"
      },
      {
        "id": "v0043",
        "moduleId": "foundation",
        "shape": "brick",
        "color": "#8c99a3"
      },
      {
        "id": "v0044",
        "moduleId": "foundation",
        "shape": "brick",
        "color": "#8c99a3"
      },
      {
        "id": "v0045",
        "moduleId": "foundation",
        "shape": "brick",
        "color": "#8c99a3"
      },
      {
        "id": "v0046",
        "moduleId": "foundation",
        "shape": "brick",
        "color": "#8c99a3"
      },
      {
        "id": "v0047",
        "moduleId": "foundation",
        "shape": "brick",
        "color": "#8c99a3"
      },
      {
        "id": "v0048",
        "moduleId": "foundation",
        "shape": "brick",
        "color": "#8c99a3"
      },
      {
        "id": "v0049",
        "moduleId": "foundation",
        "shape": "brick",
        "color": "#edf1f2"
      },
      {
        "id": "v0050",
        "moduleId": "foundation",
        "shape": "brick",
        "color": "#edf1f2"
      },
      {
        "id": "v0051",
        "moduleId": "foundation",
        "shape": "brick",
        "color": "#edf1f2"
      },
      {
        "id": "v0052",
        "moduleId": "foundation",
        "shape": "brick",
        "color": "#edf1f2"
      },
      {
        "id": "v0053",
        "moduleId": "foundation",
        "shape": "brick",
        "color": "#edf1f2"
      },
      {
        "id": "v0054",
        "moduleId": "foundation",
        "shape": "brick",
        "color": "#edf1f2"
      },
      {
        "id": "v0055",
        "moduleId": "foundation",
        "shape": "brick",
        "color": "#edf1f2"
      },
      {
        "id": "v0056",
        "moduleId": "foundation",
        "shape": "brick",
        "color": "#edf1f2"
      },
      {
        "id": "v0057",
        "moduleId": "foundation",
        "shape": "brick",
        "color": "#edf1f2"
      },
      {
        "id": "v0058",
        "moduleId": "foundation",
        "shape": "brick",
        "color": "#edf1f2"
      },
      {
        "id": "v0059",
        "moduleId": "foundation",
        "shape": "brick",
        "color": "#edf1f2"
      },
      {
        "id": "v0060",
        "moduleId": "foundation",
        "shape": "brick",
        "color": "#edf1f2"
      },
      {
        "id": "v0061",
        "moduleId": "foundation",
        "shape": "brick",
        "color": "#edf1f2"
      },
      {
        "id": "v0062",
        "moduleId": "foundation",
        "shape": "brick",
        "color": "#edf1f2"
      },
      {
        "id": "v0063",
        "moduleId": "foundation",
        "shape": "brick",
        "color": "#edf1f2"
      },
      {
        "id": "v0064",
        "moduleId": "foundation",
        "shape": "brick",
        "color": "#edf1f2"
      },
      {
        "id": "v0065",
        "moduleId": "foundation",
        "shape": "panel",
        "color": "#26323b"
      },
      {
        "id": "v0066",
        "moduleId": "dome",
        "shape": "slope",
        "color": "#2878b8"
      },
      {
        "id": "v0067",
        "moduleId": "dome",
        "shape": "slope",
        "color": "#edf1f2"
      },
      {
        "id": "v0068",
        "moduleId": "dome",
        "shape": "slope",
        "color": "#edf1f2"
      },
      {
        "id": "v0069",
        "moduleId": "dome",
        "shape": "slope",
        "color": "#edf1f2"
      },
      {
        "id": "v0070",
        "moduleId": "dome",
        "shape": "slope",
        "color": "#edf1f2"
      },
      {
        "id": "v0071",
        "moduleId": "dome",
        "shape": "slope",
        "color": "#2878b8"
      },
      {
        "id": "v0072",
        "moduleId": "dome",
        "shape": "slope",
        "color": "#edf1f2"
      },
      {
        "id": "v0073",
        "moduleId": "dome",
        "shape": "slope",
        "color": "#edf1f2"
      },
      {
        "id": "v0074",
        "moduleId": "dome",
        "shape": "slope",
        "color": "#edf1f2"
      },
      {
        "id": "v0075",
        "moduleId": "dome",
        "shape": "slope",
        "color": "#edf1f2"
      },
      {
        "id": "v0076",
        "moduleId": "dome",
        "shape": "slope",
        "color": "#2878b8"
      },
      {
        "id": "v0077",
        "moduleId": "dome",
        "shape": "slope",
        "color": "#edf1f2"
      },
      {
        "id": "v0078",
        "moduleId": "dome",
        "shape": "slope",
        "color": "#edf1f2"
      },
      {
        "id": "v0079",
        "moduleId": "dome",
        "shape": "slope",
        "color": "#edf1f2"
      },
      {
        "id": "v0080",
        "moduleId": "dome",
        "shape": "slope",
        "color": "#edf1f2"
      },
      {
        "id": "v0081",
        "moduleId": "dome",
        "shape": "slope",
        "color": "#2878b8"
      },
      {
        "id": "v0082",
        "moduleId": "dome",
        "shape": "slope",
        "color": "#edf1f2"
      },
      {
        "id": "v0083",
        "moduleId": "dome",
        "shape": "slope",
        "color": "#edf1f2"
      },
      {
        "id": "v0084",
        "moduleId": "dome",
        "shape": "slope",
        "color": "#edf1f2"
      },
      {
        "id": "v0085",
        "moduleId": "dome",
        "shape": "slope",
        "color": "#edf1f2"
      },
      {
        "id": "v0086",
        "moduleId": "dome",
        "shape": "beam",
        "color": "#26323b"
      },
      {
        "id": "v0087",
        "moduleId": "telescope",
        "shape": "cylinder",
        "color": "#edf1f2"
      },
      {
        "id": "v0088",
        "moduleId": "telescope",
        "shape": "cylinder",
        "color": "#2878b8"
      },
      {
        "id": "v0089",
        "moduleId": "telescope",
        "shape": "gear",
        "color": "#e8792e"
      },
      {
        "id": "v0090",
        "moduleId": "telescope",
        "shape": "beam",
        "color": "#26323b"
      },
      {
        "id": "v0091",
        "moduleId": "camera-pack",
        "shape": "cylinder",
        "color": "#c6cdd2"
      },
      {
        "id": "v0092",
        "moduleId": "camera-pack",
        "shape": "panel",
        "color": "#79c7d8"
      }
    ]
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 颜色识别（h3-adaptive-radio-observatory-color）

零件 v0091 的颜色值是什么？

能力：颜色识别；形式：single-choice；证据：model-state。

- A：#c6cdd2
- B：#2878b8
- C：#d43a32
- D：#f2bf3c

```json
{
  "input": {
    "part": {
      "id": "v0091",
      "moduleId": "camera-pack",
      "shape": "cylinder",
      "size": [
        1.15,
        1.1,
        1.15
      ],
      "position": [
        0,
        0,
        -0.1999999999999999
      ],
      "rotation": [
        0.7071067811865475,
        0,
        0,
        0.7071067811865476
      ],
      "color": "#c6cdd2"
    }
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 三维位置（h3-adaptive-radio-observatory-position）

模块 camera-pack 的世界包围盒中心是什么？

能力：三维位置；形式：single-choice；证据：model-state。

- A：[0,3.9921426675754312,0]
- B：[0,6.300000000000001,1.8875000000000004]
- C：[0,6.5,5.6000000000000005]
- D：[0,1.28,0]

```json
{
  "input": {
    "centers": {
      "foundation": [
        0,
        1.28,
        0
      ],
      "dome": [
        0,
        3.9921426675754312,
        0
      ],
      "telescope": [
        0,
        6.300000000000001,
        1.8875000000000004
      ],
      "camera-pack": [
        0,
        6.5,
        5.6000000000000005
      ]
    }
  },
  "answer": {
    "choiceId": "C"
  }
}
```

### 关节类型（h3-adaptive-radio-observatory-joint-type）

elevation-axis 采用什么约束类型？

能力：关节类型；形式：single-choice；证据：model-state。

- A：prismatic
- B：spring
- C：revolute
- D：fixed

```json
{
  "input": {
    "joint": {
      "id": "elevation-axis",
      "name": "Telescope elevation axis",
      "type": "revolute",
      "parent": "dome",
      "child": "telescope",
      "anchorParent": [
        2.220446049250313e-16,
        2.607857332424569,
        0
      ],
      "anchorChild": [
        0,
        0.3,
        -1.8875000000000002
      ],
      "axis": [
        1,
        0,
        0
      ],
      "limits": [
        -0.15,
        1.25
      ]
    }
  },
  "answer": {
    "choiceId": "C"
  }
}
```

### 直接连接（h3-adaptive-radio-observatory-parent）

camera-pack 的直接父模块集合是什么？

能力：直接连接；形式：single-choice；证据：model-state。

- A：["camera-pack"]
- B：[]
- C：["foundation","dome","telescope","camera-pack"]
- D：["telescope"]

```json
{
  "input": {
    "joints": [
      {
        "id": "dome-ring",
        "name": "Azimuth rotation ring",
        "type": "revolute",
        "parent": "foundation",
        "child": "dome",
        "anchorParent": [
          0,
          1.8200000000000003,
          0
        ],
        "anchorChild": [
          2.220446049250313e-16,
          -0.8921426675754309,
          0
        ],
        "axis": [
          0,
          1,
          0
        ],
        "limits": [
          -3.141592653589793,
          3.141592653589793
        ]
      },
      {
        "id": "elevation-axis",
        "name": "Telescope elevation axis",
        "type": "revolute",
        "parent": "dome",
        "child": "telescope",
        "anchorParent": [
          2.220446049250313e-16,
          2.607857332424569,
          0
        ],
        "anchorChild": [
          0,
          0.3,
          -1.8875000000000002
        ],
        "axis": [
          1,
          0,
          0
        ],
        "limits": [
          -0.15,
          1.25
        ]
      },
      {
        "id": "camera-bayonet",
        "name": "Camera bayonet",
        "type": "fixed",
        "parent": "telescope",
        "child": "camera-pack",
        "anchorParent": [
          0,
          0.1999999999999999,
          3.5125
        ],
        "anchorChild": [
          0,
          0,
          -0.1999999999999999
        ]
      }
    ]
  },
  "answer": {
    "choiceId": "D"
  }
}
```

### 基座识别（h3-adaptive-radio-observatory-anchor）

哪些模块被声明为固定基座？

能力：基座识别；形式：single-choice；证据：model-state。

- A：["foundation"]
- B：[]
- C：["foundation","dome","telescope","camera-pack"]
- D：["camera-pack"]

```json
{
  "input": {
    "modules": [
      {
        "id": "foundation",
        "name": "Terraced observatory foundation",
        "role": "foundation",
        "anchored": true,
        "mass": 20,
        "position": [
          0,
          1.28,
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
        "id": "dome",
        "name": "Rotating segmented dome",
        "role": "rotating-enclosure",
        "anchored": false,
        "mass": 9,
        "position": [
          -2.220446049250313e-16,
          3.992142667575431,
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
        "id": "telescope",
        "name": "Elevation telescope",
        "role": "instrument",
        "anchored": false,
        "mass": 4,
        "position": [
          0,
          6.3,
          1.8875000000000002
        ],
        "rotation": [
          0,
          0,
          0,
          1
        ]
      },
      {
        "id": "camera-pack",
        "name": "Cryogenic camera pack",
        "role": "service-module",
        "anchored": false,
        "mass": 1.5,
        "position": [
          0,
          6.5,
          5.6000000000000005
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
    "choiceId": "A"
  }
}
```

### 接口计数（h3-adaptive-radio-observatory-degree）

camera-pack 连接几个声明关节？平行关节分别计数。

能力：接口计数；形式：single-choice；证据：model-state。

- A：3
- B：1
- C：2
- D：0

```json
{
  "input": {
    "joints": [
      {
        "id": "dome-ring",
        "name": "Azimuth rotation ring",
        "type": "revolute",
        "parent": "foundation",
        "child": "dome",
        "anchorParent": [
          0,
          1.8200000000000003,
          0
        ],
        "anchorChild": [
          2.220446049250313e-16,
          -0.8921426675754309,
          0
        ],
        "axis": [
          0,
          1,
          0
        ],
        "limits": [
          -3.141592653589793,
          3.141592653589793
        ]
      },
      {
        "id": "elevation-axis",
        "name": "Telescope elevation axis",
        "type": "revolute",
        "parent": "dome",
        "child": "telescope",
        "anchorParent": [
          2.220446049250313e-16,
          2.607857332424569,
          0
        ],
        "anchorChild": [
          0,
          0.3,
          -1.8875000000000002
        ],
        "axis": [
          1,
          0,
          0
        ],
        "limits": [
          -0.15,
          1.25
        ]
      },
      {
        "id": "camera-bayonet",
        "name": "Camera bayonet",
        "type": "fixed",
        "parent": "telescope",
        "child": "camera-pack",
        "anchorParent": [
          0,
          0.1999999999999999,
          3.5125
        ],
        "anchorChild": [
          0,
          0,
          -0.1999999999999999
        ]
      }
    ]
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 局部改色（h3-adaptive-radio-observatory-recolor）

仅将 v0091 改成 #e8792e，其他零件不变。选择正确补丁。

能力：局部改色；形式：single-choice；证据：model-state。

- A：{"id":"v0092","color":"#e8792e"}
- B：{"id":"v0091","color":"#2878b8"}
- C：{"id":"*","color":"#e8792e"}
- D：{"id":"v0091","color":"#e8792e"}

```json
{
  "input": {
    "part": {
      "id": "v0091",
      "moduleId": "camera-pack",
      "shape": "cylinder",
      "size": [
        1.15,
        1.1,
        1.15
      ],
      "position": [
        0,
        0,
        -0.1999999999999999
      ],
      "rotation": [
        0.7071067811865475,
        0,
        0,
        0.7071067811865476
      ],
      "color": "#c6cdd2"
    }
  },
  "answer": {
    "choiceId": "D"
  }
}
```

### 补装部件（h3-adaptive-radio-observatory-add）

模块 camera-pack 缺失零件 v0091。选择与目标清单一致的补装描述。

能力：补装部件；形式：single-choice；证据：model-state。

- A：{"id":"v0091","moduleId":"camera-pack","shape":"cylinder","size":[1.15,1.1,1.15],"position":[0,0,-0.1999999999999999],"rotation":[0.7071067811865475,0,0,0.7071067811865476],"color":"#c6cdd2"}
- B：{"id":"v0091","moduleId":"foundation","shape":"cylinder","size":[1.15,1.1,1.15],"position":[0,0,-0.1999999999999999],"rotation":[0.7071067811865475,0,0,0.7071067811865476],"color":"#c6cdd2"}
- C：{"id":"v0091","moduleId":"camera-pack","shape":"cylinder","size":[3,3,3],"position":[0,0,-0.1999999999999999],"rotation":[0.7071067811865475,0,0,0.7071067811865476],"color":"#c6cdd2"}
- D：{"id":"v0091","moduleId":"camera-pack","shape":"cylinder","size":[1.15,1.1,1.15],"position":[0,0,-0.1999999999999999],"rotation":[0.7071067811865475,0,0,0.7071067811865476],"color":"#000000"}

```json
{
  "input": {
    "targetPart": {
      "id": "v0091",
      "moduleId": "camera-pack",
      "shape": "cylinder",
      "size": [
        1.15,
        1.1,
        1.15
      ],
      "position": [
        0,
        0,
        -0.1999999999999999
      ],
      "rotation": [
        0.7071067811865475,
        0,
        0,
        0.7071067811865476
      ],
      "color": "#c6cdd2"
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
      "v0092"
    ]
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 安全拆除（h3-adaptive-radio-observatory-remove）

按声明依赖图，当前可以先拆哪些叶模块？

能力：安全拆除；形式：single-choice；证据：model-state。

- A：["camera-pack"]
- B：["foundation"]
- C：[]
- D：["foundation","dome","telescope","camera-pack"]

```json
{
  "input": {
    "joints": [
      {
        "id": "dome-ring",
        "name": "Azimuth rotation ring",
        "type": "revolute",
        "parent": "foundation",
        "child": "dome",
        "anchorParent": [
          0,
          1.8200000000000003,
          0
        ],
        "anchorChild": [
          2.220446049250313e-16,
          -0.8921426675754309,
          0
        ],
        "axis": [
          0,
          1,
          0
        ],
        "limits": [
          -3.141592653589793,
          3.141592653589793
        ]
      },
      {
        "id": "elevation-axis",
        "name": "Telescope elevation axis",
        "type": "revolute",
        "parent": "dome",
        "child": "telescope",
        "anchorParent": [
          2.220446049250313e-16,
          2.607857332424569,
          0
        ],
        "anchorChild": [
          0,
          0.3,
          -1.8875000000000002
        ],
        "axis": [
          1,
          0,
          0
        ],
        "limits": [
          -0.15,
          1.25
        ]
      },
      {
        "id": "camera-bayonet",
        "name": "Camera bayonet",
        "type": "fixed",
        "parent": "telescope",
        "child": "camera-pack",
        "anchorParent": [
          0,
          0.1999999999999999,
          3.5125
        ],
        "anchorChild": [
          0,
          0,
          -0.1999999999999999
        ]
      }
    ],
    "modules": [
      "foundation",
      "dome",
      "telescope",
      "camera-pack"
    ]
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 替换选择（h3-adaptive-radio-observatory-replace）

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
        "cost": 6,
        "stiffness": 10,
        "mass": 1.5
      },
      {
        "id": "stock-1",
        "cost": 5,
        "stiffness": 7,
        "mass": 1.3
      },
      {
        "id": "stock-2",
        "cost": 8,
        "stiffness": 4,
        "mass": 1.3
      },
      {
        "id": "stock-3",
        "cost": 3,
        "stiffness": 10,
        "mass": 0.9
      }
    ],
    "maxCost": 7
  },
  "answer": {
    "choiceId": "D"
  }
}
```

### 平移纠偏（h3-adaptive-radio-observatory-translate）

观察到相对目标的平移误差 delta，选择补偿平移。

能力：平移纠偏；形式：single-choice；证据：model-state。

- A：[3,0,-2]
- B：[0,0,0]
- C：[0,2,0]
- D：[-3,0,2]

```json
{
  "input": {
    "delta": [
      3,
      0,
      -2
    ],
    "target": "camera-pack"
  },
  "answer": {
    "choiceId": "D"
  }
}
```

### 姿态纠偏（h3-adaptive-radio-observatory-rotate）

选择从当前yaw到目标yaw的最短有符号旋转；恰好180°时使用-180°。

能力：姿态纠偏；形式：single-choice；证据：model-state。

- A：-45
- B：45
- C：0
- D：90

```json
{
  "input": {
    "module": "camera-pack",
    "currentYaw": 0,
    "targetYaw": 315
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 下一步放置（h3-adaptive-radio-observatory-next-module）

已完成给定前缀，选择所有前置依赖已满足的下一模块集合。

能力：下一步放置；形式：single-choice；证据：model-state。

- A：[]
- B：["foundation","dome"]
- C：["telescope","camera-pack"]
- D：["telescope"]

```json
{
  "input": {
    "prefix": [
      "foundation",
      "dome"
    ],
    "joints": [
      {
        "id": "dome-ring",
        "name": "Azimuth rotation ring",
        "type": "revolute",
        "parent": "foundation",
        "child": "dome",
        "anchorParent": [
          0,
          1.8200000000000003,
          0
        ],
        "anchorChild": [
          2.220446049250313e-16,
          -0.8921426675754309,
          0
        ],
        "axis": [
          0,
          1,
          0
        ],
        "limits": [
          -3.141592653589793,
          3.141592653589793
        ]
      },
      {
        "id": "elevation-axis",
        "name": "Telescope elevation axis",
        "type": "revolute",
        "parent": "dome",
        "child": "telescope",
        "anchorParent": [
          2.220446049250313e-16,
          2.607857332424569,
          0
        ],
        "anchorChild": [
          0,
          0.3,
          -1.8875000000000002
        ],
        "axis": [
          1,
          0,
          0
        ],
        "limits": [
          -0.15,
          1.25
        ]
      },
      {
        "id": "camera-bayonet",
        "name": "Camera bayonet",
        "type": "fixed",
        "parent": "telescope",
        "child": "camera-pack",
        "anchorParent": [
          0,
          0.1999999999999999,
          3.5125
        ],
        "anchorChild": [
          0,
          0,
          -0.1999999999999999
        ]
      }
    ],
    "modules": [
      "foundation",
      "dome",
      "telescope",
      "camera-pack"
    ]
  },
  "answer": {
    "choiceId": "D"
  }
}
```

### 库存核算（h3-adaptive-radio-observatory-inventory）

备件库有 3 件，替换模块需 2 件，还剩多少？

能力：库存核算；形式：single-choice；证据：model-state。

- A：0
- B：4
- C：1
- D：2

```json
{
  "input": {
    "available": 3,
    "required": 2
  },
  "answer": {
    "choiceId": "C"
  }
}
```

### 子装配边界（h3-adaptive-radio-observatory-boundary）

隔离 camera-pack 需要断开哪些边界关节？

能力：子装配边界；形式：single-choice；证据：model-state。

- A：["elevation-axis"]
- B：["camera-bayonet"]
- C：[]
- D：["dome-ring","elevation-axis","camera-bayonet"]

```json
{
  "input": {
    "joints": [
      {
        "id": "dome-ring",
        "name": "Azimuth rotation ring",
        "type": "revolute",
        "parent": "foundation",
        "child": "dome",
        "anchorParent": [
          0,
          1.8200000000000003,
          0
        ],
        "anchorChild": [
          2.220446049250313e-16,
          -0.8921426675754309,
          0
        ],
        "axis": [
          0,
          1,
          0
        ],
        "limits": [
          -3.141592653589793,
          3.141592653589793
        ]
      },
      {
        "id": "elevation-axis",
        "name": "Telescope elevation axis",
        "type": "revolute",
        "parent": "dome",
        "child": "telescope",
        "anchorParent": [
          2.220446049250313e-16,
          2.607857332424569,
          0
        ],
        "anchorChild": [
          0,
          0.3,
          -1.8875000000000002
        ],
        "axis": [
          1,
          0,
          0
        ],
        "limits": [
          -0.15,
          1.25
        ]
      },
      {
        "id": "camera-bayonet",
        "name": "Camera bayonet",
        "type": "fixed",
        "parent": "telescope",
        "child": "camera-pack",
        "anchorParent": [
          0,
          0.1999999999999999,
          3.5125
        ],
        "anchorChild": [
          0,
          0,
          -0.1999999999999999
        ]
      }
    ],
    "target": "camera-pack"
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 最小干预（h3-adaptive-radio-observatory-no-op）

当前模块颜色已满足指令，且无需改变位姿。最少需要几次编辑？

能力：最小干预；形式：single-choice；证据：model-state。

- A：0
- B：1
- C：2

```json
{
  "input": {
    "module": "camera-pack"
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 全过程依赖（h3-adaptive-radio-observatory-prefix）

给定候选顺序，首次违反前置依赖的步骤是？从 0 编号，-1 表示没有违反。

能力：全过程依赖；形式：single-choice；证据：support-graph。

- A：2
- B：3
- C：1
- D：-1

```json
{
  "input": {
    "order": [
      "foundation",
      "telescope",
      "dome",
      "camera-pack"
    ],
    "joints": [
      {
        "id": "dome-ring",
        "name": "Azimuth rotation ring",
        "type": "revolute",
        "parent": "foundation",
        "child": "dome",
        "anchorParent": [
          0,
          1.8200000000000003,
          0
        ],
        "anchorChild": [
          2.220446049250313e-16,
          -0.8921426675754309,
          0
        ],
        "axis": [
          0,
          1,
          0
        ],
        "limits": [
          -3.141592653589793,
          3.141592653589793
        ]
      },
      {
        "id": "elevation-axis",
        "name": "Telescope elevation axis",
        "type": "revolute",
        "parent": "dome",
        "child": "telescope",
        "anchorParent": [
          2.220446049250313e-16,
          2.607857332424569,
          0
        ],
        "anchorChild": [
          0,
          0.3,
          -1.8875000000000002
        ],
        "axis": [
          1,
          0,
          0
        ],
        "limits": [
          -0.15,
          1.25
        ]
      },
      {
        "id": "camera-bayonet",
        "name": "Camera bayonet",
        "type": "fixed",
        "parent": "telescope",
        "child": "camera-pack",
        "anchorParent": [
          0,
          0.1999999999999999,
          3.5125
        ],
        "anchorChild": [
          0,
          0,
          -0.1999999999999999
        ]
      }
    ]
  },
  "answer": {
    "choiceId": "C"
  }
}
```

### 连续维修路径（h3-adaptive-radio-observatory-access）

根据实际 Rapier shape cast 记录，选择全部无碰撞路径。

能力：连续维修路径；形式：multiple-choice；证据：Rapier。

- A：path-2
- B：path-0
- C：path-1

```json
{
  "input": {
    "paths": [
      {
        "id": "path-0",
        "start": [
          9.399999999999999,
          6.5,
          5.6000000000000005
        ],
        "end": [
          0,
          6.5,
          5.6000000000000005
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
          0,
          11.425,
          5.6000000000000005
        ],
        "end": [
          0,
          6.5,
          5.6000000000000005
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
          0,
          6.5,
          10.350000000000001
        ],
        "end": [
          0,
          6.5,
          5.6000000000000005
        ],
        "halfExtents": [
          0.18,
          0.18,
          0.18
        ],
        "clear": true,
        "timeOfImpact": null
      }
    ],
    "simulator": "stud-inclusive conservative cuboids; anchored base; force-limited position servos; no clutch/material calibration"
  },
  "answer": {
    "choiceIds": [
      "A",
      "B",
      "C"
    ]
  }
}
```

### 支撑反事实（h3-adaptive-radio-observatory-counterfactual）

移除指定模块后，哪些其余模块失去到任一基座的关节路径？不包含被移除模块本身。

能力：支撑反事实；形式：single-choice；证据：support-graph。

- A：["dome"]
- B：[]
- C：["foundation","dome","telescope","camera-pack"]
- D：["camera-pack","telescope"]

```json
{
  "input": {
    "removed": "dome",
    "roots": [
      "foundation"
    ],
    "joints": [
      {
        "id": "dome-ring",
        "name": "Azimuth rotation ring",
        "type": "revolute",
        "parent": "foundation",
        "child": "dome",
        "anchorParent": [
          0,
          1.8200000000000003,
          0
        ],
        "anchorChild": [
          2.220446049250313e-16,
          -0.8921426675754309,
          0
        ],
        "axis": [
          0,
          1,
          0
        ],
        "limits": [
          -3.141592653589793,
          3.141592653589793
        ]
      },
      {
        "id": "elevation-axis",
        "name": "Telescope elevation axis",
        "type": "revolute",
        "parent": "dome",
        "child": "telescope",
        "anchorParent": [
          2.220446049250313e-16,
          2.607857332424569,
          0
        ],
        "anchorChild": [
          0,
          0.3,
          -1.8875000000000002
        ],
        "axis": [
          1,
          0,
          0
        ],
        "limits": [
          -0.15,
          1.25
        ]
      },
      {
        "id": "camera-bayonet",
        "name": "Camera bayonet",
        "type": "fixed",
        "parent": "telescope",
        "child": "camera-pack",
        "anchorParent": [
          0,
          0.1999999999999999,
          3.5125
        ],
        "anchorChild": [
          0,
          0,
          -0.1999999999999999
        ]
      }
    ],
    "modules": [
      "foundation",
      "dome",
      "telescope",
      "camera-pack"
    ]
  },
  "answer": {
    "choiceId": "D"
  }
}
```

### 冲击响应读数（h3-adaptive-radio-observatory-dynamic）

Rapier 实际采样轨迹中的最大平移位移是多少？按四位小数报告。

能力：冲击响应读数；形式：single-choice；证据：Rapier。

- A：0.2064
- B：0
- C：1.0064
- D：0.0064

```json
{
  "input": {
    "trace": [
      {
        "time": 0.008333333333333333,
        "displacement": 0.001663199865680958
      },
      {
        "time": 0.10833333333333334,
        "displacement": 0.006418225690291193
      },
      {
        "time": 0.20833333333333334,
        "displacement": 0.0025447712205475064
      },
      {
        "time": 0.30833333333333335,
        "displacement": 0.0017892972173478123
      },
      {
        "time": 0.4083333333333333,
        "displacement": 0.0015322098939430301
      },
      {
        "time": 0.5083333333333333,
        "displacement": 0.00025628111125773
      },
      {
        "time": 0.6083333333333333,
        "displacement": 0.0006812265144248621
      },
      {
        "time": 0.7083333333333334,
        "displacement": 0.00009927762046968697
      },
      {
        "time": 0.8083333333333333,
        "displacement": 0.00024011782269040257
      },
      {
        "time": 0.9083333333333333,
        "displacement": 0.00004792039718781467
      },
      {
        "time": 1,
        "displacement": 0.00004792039718781467
      }
    ],
    "impulse": [
      10,
      1.8,
      3.5
    ],
    "nominalDrift": 0.01287595714797323,
    "scope": "采样轨迹极值，非连续时间极值；不代表实物安全阈值"
  },
  "answer": {
    "choiceId": "D"
  }
}
```

### 关节限位推理（h3-adaptive-radio-observatory-kinematic）

下列目标位置/角度中哪些在关节声明限位内（含边界）？

能力：关节限位推理；形式：multiple-choice；证据：model-state。

- A：1.75
- B：-0.15
- C：0.55
- D：-0.65

```json
{
  "input": {
    "joint": "elevation-axis",
    "limits": [
      -0.15,
      1.25
    ],
    "units": "radians"
  },
  "answer": {
    "choiceIds": [
      "B",
      "C"
    ]
  }
}
```

### 约束故障诊断（h3-adaptive-radio-observatory-diagnosis）

已检测到端点和约束类型如下，选择匹配的全部关节。

能力：约束故障诊断；形式：multiple-choice；证据：model-state。

- A：camera-bayonet
- B：dome-ring
- C：elevation-axis

```json
{
  "input": {
    "endpoints": [
      "telescope",
      "camera-pack"
    ],
    "type": "fixed",
    "joints": [
      {
        "id": "dome-ring",
        "name": "Azimuth rotation ring",
        "type": "revolute",
        "parent": "foundation",
        "child": "dome",
        "anchorParent": [
          0,
          1.8200000000000003,
          0
        ],
        "anchorChild": [
          2.220446049250313e-16,
          -0.8921426675754309,
          0
        ],
        "axis": [
          0,
          1,
          0
        ],
        "limits": [
          -3.141592653589793,
          3.141592653589793
        ]
      },
      {
        "id": "elevation-axis",
        "name": "Telescope elevation axis",
        "type": "revolute",
        "parent": "dome",
        "child": "telescope",
        "anchorParent": [
          2.220446049250313e-16,
          2.607857332424569,
          0
        ],
        "anchorChild": [
          0,
          0.3,
          -1.8875000000000002
        ],
        "axis": [
          1,
          0,
          0
        ],
        "limits": [
          -0.15,
          1.25
        ]
      },
      {
        "id": "camera-bayonet",
        "name": "Camera bayonet",
        "type": "fixed",
        "parent": "telescope",
        "child": "camera-pack",
        "anchorParent": [
          0,
          0.1999999999999999,
          3.5125
        ],
        "anchorChild": [
          0,
          0,
          -0.1999999999999999
        ]
      }
    ]
  },
  "answer": {
    "choiceIds": [
      "A"
    ]
  }
}
```

### 主动检查收益（h3-adaptive-radio-observatory-information-gain）

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
    "module": "camera-pack",
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

### 不确定性与弃答（h3-adaptive-radio-observatory-abstention）

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
        "action": "repair"
      }
    ]
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 观测后信念更新（h3-adaptive-radio-observatory-posterior）

均匀先验，得到给定观测后，jammed 世界的后验概率是多少？

能力：观测后信念更新；形式：single-choice；证据：finite-world。

- A：0.25
- B：0
- C：0.3333333333333333
- D：0.5

```json
{
  "input": {
    "module": "camera-pack",
    "worlds": [
      "normal",
      "jammed",
      "reversed",
      "loose"
    ],
    "observationByWorld": [
      "negative",
      "negative",
      "negative",
      "negative"
    ],
    "observed": "negative"
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 多目标工程权衡（h3-adaptive-radio-observatory-pareto）

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
        "cost": 6,
        "stiffness": 10,
        "mass": 1.5
      },
      {
        "id": "stock-1",
        "cost": 5,
        "stiffness": 7,
        "mass": 1.3
      },
      {
        "id": "stock-2",
        "cost": 8,
        "stiffness": 4,
        "mass": 1.3
      },
      {
        "id": "stock-3",
        "cost": 3,
        "stiffness": 10,
        "mass": 0.9
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

### 依赖装配（h3-adaptive-radio-observatory-assembly）

提交 actionIds。执行公开前置条件与效果，达到所有目标且不超过预算；允许交换独立动作。

能力：依赖装配；形式：actions；证据：state-machine。


```json
{
  "input": {
    "initialFacts": [],
    "initialModules": [],
    "actions": [
      {
        "id": "place:camera-pack",
        "label": "安装 camera-pack",
        "requires": [
          "present:telescope"
        ],
        "forbids": [
          "present:camera-pack"
        ],
        "adds": [
          "present:camera-pack"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "camera-pack",
          "visible": true
        }
      },
      {
        "id": "place:foundation",
        "label": "安装 foundation",
        "requires": [],
        "forbids": [
          "present:foundation"
        ],
        "adds": [
          "present:foundation"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "foundation",
          "visible": true
        }
      },
      {
        "id": "place:telescope",
        "label": "安装 telescope",
        "requires": [
          "present:dome"
        ],
        "forbids": [
          "present:telescope"
        ],
        "adds": [
          "present:telescope"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "telescope",
          "visible": true
        }
      },
      {
        "id": "place:dome",
        "label": "安装 dome",
        "requires": [
          "present:foundation"
        ],
        "forbids": [
          "present:dome"
        ],
        "adds": [
          "present:dome"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "dome",
          "visible": true
        }
      }
    ],
    "goalFacts": [
      "present:foundation",
      "present:dome",
      "present:telescope",
      "present:camera-pack"
    ],
    "budget": 4,
    "semantics": "requires must hold; forbids must be absent; effects apply in order; unit action cost"
  },
  "answer": {
    "actionIds": [
      "place:foundation",
      "place:dome",
      "place:telescope",
      "place:camera-pack"
    ]
  }
}
```

### 依赖拆解（h3-adaptive-radio-observatory-disassembly）

提交 actionIds。执行公开前置条件与效果，达到所有目标且不超过预算；允许交换独立动作。

能力：依赖拆解；形式：actions；证据：state-machine。


```json
{
  "input": {
    "initialFacts": [
      "present:foundation",
      "present:dome",
      "present:telescope",
      "present:camera-pack"
    ],
    "initialModules": [
      "foundation",
      "dome",
      "telescope",
      "camera-pack"
    ],
    "actions": [
      {
        "id": "remove:dome",
        "label": "拆除 dome",
        "requires": [
          "present:dome"
        ],
        "forbids": [
          "present:telescope"
        ],
        "adds": [
          "removed:dome"
        ],
        "deletes": [
          "present:dome"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "dome",
          "visible": false
        }
      },
      {
        "id": "remove:telescope",
        "label": "拆除 telescope",
        "requires": [
          "present:telescope"
        ],
        "forbids": [
          "present:camera-pack"
        ],
        "adds": [
          "removed:telescope"
        ],
        "deletes": [
          "present:telescope"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "telescope",
          "visible": false
        }
      },
      {
        "id": "remove:foundation",
        "label": "拆除 foundation",
        "requires": [
          "present:foundation"
        ],
        "forbids": [
          "present:dome"
        ],
        "adds": [
          "removed:foundation"
        ],
        "deletes": [
          "present:foundation"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "foundation",
          "visible": false
        }
      },
      {
        "id": "remove:camera-pack",
        "label": "拆除 camera-pack",
        "requires": [
          "present:camera-pack"
        ],
        "forbids": [],
        "adds": [
          "removed:camera-pack"
        ],
        "deletes": [
          "present:camera-pack"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "camera-pack",
          "visible": false
        }
      }
    ],
    "goalFacts": [
      "removed:camera-pack",
      "removed:telescope",
      "removed:dome",
      "removed:foundation"
    ],
    "budget": 4,
    "semantics": "requires must hold; forbids must be absent; effects apply in order; unit action cost"
  },
  "answer": {
    "actionIds": [
      "remove:camera-pack",
      "remove:telescope",
      "remove:dome",
      "remove:foundation"
    ]
  }
}
```

### 承载维修（h3-adaptive-radio-observatory-service-repair）

提交 actionIds。执行公开前置条件与效果，达到所有目标且不超过预算；允许交换独立动作。

能力：承载维修；形式：actions；证据：state-machine。


```json
{
  "input": {
    "initialFacts": [
      "fault:camera-pack",
      "closed:camera-pack"
    ],
    "initialModules": [
      "foundation",
      "dome",
      "telescope",
      "camera-pack"
    ],
    "actions": [
      {
        "id": "release:camera-pack",
        "label": "release camera-pack",
        "requires": [
          "done:close:camera-pack"
        ],
        "forbids": [
          "done:release:camera-pack"
        ],
        "adds": [
          "done:release:camera-pack",
          "repaired:camera-pack"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "camera-pack"
        }
      },
      {
        "id": "replace:camera-pack",
        "label": "replace camera-pack",
        "requires": [
          "done:remove:camera-pack"
        ],
        "forbids": [
          "done:replace:camera-pack"
        ],
        "adds": [
          "done:replace:camera-pack"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "camera-pack",
          "visible": true
        }
      },
      {
        "id": "close:camera-pack",
        "label": "close camera-pack",
        "requires": [
          "done:verify:camera-pack"
        ],
        "forbids": [
          "done:close:camera-pack"
        ],
        "adds": [
          "done:close:camera-pack"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "camera-pack"
        }
      },
      {
        "id": "support:camera-pack",
        "label": "support camera-pack",
        "requires": [
          "fault:camera-pack"
        ],
        "forbids": [
          "done:support:camera-pack"
        ],
        "adds": [
          "done:support:camera-pack"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "camera-pack"
        }
      },
      {
        "id": "verify:camera-pack",
        "label": "verify camera-pack",
        "requires": [
          "done:replace:camera-pack"
        ],
        "forbids": [
          "done:verify:camera-pack"
        ],
        "adds": [
          "done:verify:camera-pack"
        ],
        "deletes": [
          "fault:camera-pack"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "camera-pack"
        }
      },
      {
        "id": "remove:camera-pack",
        "label": "remove camera-pack",
        "requires": [
          "done:open:camera-pack"
        ],
        "forbids": [
          "done:remove:camera-pack"
        ],
        "adds": [
          "done:remove:camera-pack"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "camera-pack",
          "visible": false
        }
      },
      {
        "id": "open:camera-pack",
        "label": "open camera-pack",
        "requires": [
          "done:support:camera-pack"
        ],
        "forbids": [
          "done:open:camera-pack"
        ],
        "adds": [
          "done:open:camera-pack"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "camera-pack"
        }
      }
    ],
    "goalFacts": [
      "repaired:camera-pack"
    ],
    "budget": 7,
    "semantics": "requires must hold; forbids must be absent; effects apply in order; unit action cost"
  },
  "answer": {
    "actionIds": [
      "support:camera-pack",
      "open:camera-pack",
      "remove:camera-pack",
      "replace:camera-pack",
      "verify:camera-pack",
      "close:camera-pack",
      "release:camera-pack"
    ]
  }
}
```

### 复合编辑验证（h3-adaptive-radio-observatory-compound-edit）

提交 actionIds。执行公开前置条件与效果，达到所有目标且不超过预算；允许交换独立动作。

能力：复合编辑验证；形式：actions；证据：state-machine。


```json
{
  "input": {
    "initialFacts": [
      "fault:camera-pack",
      "closed:camera-pack"
    ],
    "initialModules": [
      "foundation",
      "dome",
      "telescope",
      "camera-pack"
    ],
    "actions": [
      {
        "id": "release:camera-pack",
        "label": "release camera-pack",
        "requires": [
          "done:close:camera-pack"
        ],
        "forbids": [
          "done:release:camera-pack"
        ],
        "adds": [
          "done:release:camera-pack",
          "repaired:camera-pack"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "camera-pack"
        }
      },
      {
        "id": "close:camera-pack",
        "label": "close camera-pack",
        "requires": [
          "done:verify:camera-pack"
        ],
        "forbids": [
          "done:close:camera-pack"
        ],
        "adds": [
          "done:close:camera-pack"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "camera-pack"
        }
      },
      {
        "id": "recolor:camera-pack",
        "label": "recolor camera-pack",
        "requires": [
          "done:open:camera-pack"
        ],
        "forbids": [
          "done:recolor:camera-pack"
        ],
        "adds": [
          "done:recolor:camera-pack"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "camera-pack",
          "color": "#ea7635"
        }
      },
      {
        "id": "support:camera-pack",
        "label": "support camera-pack",
        "requires": [
          "fault:camera-pack"
        ],
        "forbids": [
          "done:support:camera-pack"
        ],
        "adds": [
          "done:support:camera-pack"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "camera-pack"
        }
      },
      {
        "id": "verify:camera-pack",
        "label": "verify camera-pack",
        "requires": [
          "done:recolor:camera-pack"
        ],
        "forbids": [
          "done:verify:camera-pack"
        ],
        "adds": [
          "done:verify:camera-pack"
        ],
        "deletes": [
          "fault:camera-pack"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "camera-pack"
        }
      },
      {
        "id": "open:camera-pack",
        "label": "open camera-pack",
        "requires": [
          "done:support:camera-pack"
        ],
        "forbids": [
          "done:open:camera-pack"
        ],
        "adds": [
          "done:open:camera-pack"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "camera-pack"
        }
      }
    ],
    "goalFacts": [
      "repaired:camera-pack"
    ],
    "budget": 6,
    "semantics": "requires must hold; forbids must be absent; effects apply in order; unit action cost"
  },
  "answer": {
    "actionIds": [
      "support:camera-pack",
      "open:camera-pack",
      "recolor:camera-pack",
      "verify:camera-pack",
      "close:camera-pack",
      "release:camera-pack"
    ]
  }
}
```

### 跨区域联合维修（h3-adaptive-radio-observatory-multi-fault）

提交 actionIds。执行公开前置条件与效果，达到所有目标且不超过预算；允许交换独立动作。

能力：跨区域联合维修；形式：actions；证据：state-machine。


```json
{
  "input": {
    "initialFacts": [
      "fault:dome",
      "closed:dome",
      "fault:telescope",
      "closed:telescope",
      "fault:camera-pack",
      "closed:camera-pack"
    ],
    "initialModules": [
      "foundation",
      "dome",
      "telescope",
      "camera-pack"
    ],
    "actions": [
      {
        "id": "remove:dome",
        "label": "remove dome",
        "requires": [
          "done:open:dome"
        ],
        "forbids": [
          "done:remove:dome"
        ],
        "adds": [
          "done:remove:dome"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "dome",
          "visible": false
        }
      },
      {
        "id": "verify:telescope",
        "label": "verify telescope",
        "requires": [
          "done:replace:telescope"
        ],
        "forbids": [
          "done:verify:telescope"
        ],
        "adds": [
          "done:verify:telescope"
        ],
        "deletes": [
          "fault:telescope"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "telescope"
        }
      },
      {
        "id": "support:telescope",
        "label": "support telescope",
        "requires": [
          "fault:telescope"
        ],
        "forbids": [
          "done:support:telescope"
        ],
        "adds": [
          "done:support:telescope"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "telescope"
        }
      },
      {
        "id": "release:camera-pack",
        "label": "release camera-pack",
        "requires": [
          "done:close:camera-pack"
        ],
        "forbids": [
          "done:release:camera-pack"
        ],
        "adds": [
          "done:release:camera-pack",
          "repaired:camera-pack"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "camera-pack"
        }
      },
      {
        "id": "release:dome",
        "label": "release dome",
        "requires": [
          "done:close:dome"
        ],
        "forbids": [
          "done:release:dome"
        ],
        "adds": [
          "done:release:dome",
          "repaired:dome"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "dome"
        }
      },
      {
        "id": "replace:camera-pack",
        "label": "replace camera-pack",
        "requires": [
          "done:remove:camera-pack"
        ],
        "forbids": [
          "done:replace:camera-pack"
        ],
        "adds": [
          "done:replace:camera-pack"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "camera-pack",
          "visible": true
        }
      },
      {
        "id": "replace:dome",
        "label": "replace dome",
        "requires": [
          "done:remove:dome"
        ],
        "forbids": [
          "done:replace:dome"
        ],
        "adds": [
          "done:replace:dome"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "dome",
          "visible": true
        }
      },
      {
        "id": "open:dome",
        "label": "open dome",
        "requires": [
          "done:support:dome"
        ],
        "forbids": [
          "done:open:dome"
        ],
        "adds": [
          "done:open:dome"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "dome"
        }
      },
      {
        "id": "close:camera-pack",
        "label": "close camera-pack",
        "requires": [
          "done:verify:camera-pack"
        ],
        "forbids": [
          "done:close:camera-pack"
        ],
        "adds": [
          "done:close:camera-pack"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "camera-pack"
        }
      },
      {
        "id": "close:dome",
        "label": "close dome",
        "requires": [
          "done:verify:dome"
        ],
        "forbids": [
          "done:close:dome"
        ],
        "adds": [
          "done:close:dome"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "dome"
        }
      },
      {
        "id": "open:telescope",
        "label": "open telescope",
        "requires": [
          "done:support:telescope"
        ],
        "forbids": [
          "done:open:telescope"
        ],
        "adds": [
          "done:open:telescope"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "telescope"
        }
      },
      {
        "id": "verify:dome",
        "label": "verify dome",
        "requires": [
          "done:replace:dome"
        ],
        "forbids": [
          "done:verify:dome"
        ],
        "adds": [
          "done:verify:dome"
        ],
        "deletes": [
          "fault:dome"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "dome"
        }
      },
      {
        "id": "release:telescope",
        "label": "release telescope",
        "requires": [
          "done:close:telescope"
        ],
        "forbids": [
          "done:release:telescope"
        ],
        "adds": [
          "done:release:telescope",
          "repaired:telescope"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "telescope"
        }
      },
      {
        "id": "replace:telescope",
        "label": "replace telescope",
        "requires": [
          "done:remove:telescope"
        ],
        "forbids": [
          "done:replace:telescope"
        ],
        "adds": [
          "done:replace:telescope"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "telescope",
          "visible": true
        }
      },
      {
        "id": "remove:telescope",
        "label": "remove telescope",
        "requires": [
          "done:open:telescope"
        ],
        "forbids": [
          "done:remove:telescope"
        ],
        "adds": [
          "done:remove:telescope"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "telescope",
          "visible": false
        }
      },
      {
        "id": "support:camera-pack",
        "label": "support camera-pack",
        "requires": [
          "fault:camera-pack"
        ],
        "forbids": [
          "done:support:camera-pack"
        ],
        "adds": [
          "done:support:camera-pack"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "camera-pack"
        }
      },
      {
        "id": "close:telescope",
        "label": "close telescope",
        "requires": [
          "done:verify:telescope"
        ],
        "forbids": [
          "done:close:telescope"
        ],
        "adds": [
          "done:close:telescope"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "telescope"
        }
      },
      {
        "id": "verify:camera-pack",
        "label": "verify camera-pack",
        "requires": [
          "done:replace:camera-pack"
        ],
        "forbids": [
          "done:verify:camera-pack"
        ],
        "adds": [
          "done:verify:camera-pack"
        ],
        "deletes": [
          "fault:camera-pack"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "camera-pack"
        }
      },
      {
        "id": "remove:camera-pack",
        "label": "remove camera-pack",
        "requires": [
          "done:open:camera-pack"
        ],
        "forbids": [
          "done:remove:camera-pack"
        ],
        "adds": [
          "done:remove:camera-pack"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "camera-pack",
          "visible": false
        }
      },
      {
        "id": "support:dome",
        "label": "support dome",
        "requires": [
          "fault:dome"
        ],
        "forbids": [
          "done:support:dome"
        ],
        "adds": [
          "done:support:dome"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "dome"
        }
      },
      {
        "id": "open:camera-pack",
        "label": "open camera-pack",
        "requires": [
          "done:support:camera-pack"
        ],
        "forbids": [
          "done:open:camera-pack"
        ],
        "adds": [
          "done:open:camera-pack"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "camera-pack"
        }
      }
    ],
    "goalFacts": [
      "repaired:dome",
      "repaired:telescope",
      "repaired:camera-pack"
    ],
    "budget": 21,
    "semantics": "requires must hold; forbids must be absent; effects apply in order; unit action cost"
  },
  "answer": {
    "actionIds": [
      "support:telescope",
      "open:telescope",
      "remove:telescope",
      "replace:telescope",
      "verify:telescope",
      "support:camera-pack",
      "close:telescope",
      "release:telescope",
      "support:dome",
      "open:dome",
      "remove:dome",
      "replace:dome",
      "verify:dome",
      "close:dome",
      "release:dome",
      "open:camera-pack",
      "remove:camera-pack",
      "replace:camera-pack",
      "verify:camera-pack",
      "close:camera-pack",
      "release:camera-pack"
    ]
  }
}
```

### 多工位资源调度（h3-adaptive-radio-observatory-scheduling）

为所有工单提交整数 starts，满足先后关系、独占工位及截止时间。

能力：多工位资源调度；形式：schedule；证据：resource-schedule。


```json
{
  "input": {
    "jobs": [
      {
        "id": "job-0",
        "module": "foundation",
        "duration": 1,
        "resource": "test-bench",
        "after": []
      },
      {
        "id": "job-1",
        "module": "dome",
        "duration": 3,
        "resource": "technician",
        "after": []
      },
      {
        "id": "job-2",
        "module": "telescope",
        "duration": 2,
        "resource": "test-bench",
        "after": [
          "job-0"
        ]
      },
      {
        "id": "job-3",
        "module": "camera-pack",
        "duration": 1,
        "resource": "technician",
        "after": [
          "job-1"
        ]
      }
    ],
    "deadline": 4
  },
  "answer": {
    "starts": {
      "job-0": 0,
      "job-1": 0,
      "job-2": 1,
      "job-3": 3
    }
  }
}
```

### 检查后条件策略（h3-adaptive-radio-observatory-policy）

提交一个检查及 observation→action 决策表，在所有相容世界中采取正确动作。

能力：检查后条件策略；形式：policy；证据：finite-world。


```json
{
  "input": {
    "module": "camera-pack",
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

### 局部坐标变换（h3-adaptive-radio-observatory-local-frame）

将模块局部点通过给定四元数与平移转换为世界点，保留五位小数。

能力：局部坐标变换；形式：single-choice；证据：model-state。

- A：[2,7.5,6.4]
- B：[1,6.5,5.4]
- C：[1,0,-0.2]

```json
{
  "input": {
    "localPoint": [
      1,
      0,
      -0.1999999999999999
    ],
    "rotationXYZW": [
      0,
      0,
      0,
      1
    ],
    "translation": [
      0,
      6.5,
      5.6000000000000005
    ]
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 正交视图投影（h3-adaptive-radio-observatory-projection）

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

### 空间相对关系（h3-adaptive-radio-observatory-relative-order）

比较B相对A在指定世界轴上的模块原点坐标。

能力：空间相对关系；形式：single-choice；证据：model-state。

- A：greater
- B：less
- C：equal

```json
{
  "input": {
    "A": {
      "id": "foundation",
      "position": [
        0,
        1.28,
        0
      ]
    },
    "B": {
      "id": "camera-pack",
      "position": [
        0,
        6.5,
        5.6000000000000005
      ]
    },
    "axis": "y"
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 约束自由度（h3-adaptive-radio-observatory-joint-axis）

仅考虑这一声明约束，不计闭环、马达与限位激活，保留多少相对运动自由度？弹簧仅施力、不消除自由度。

能力：约束自由度；形式：single-choice；证据：model-state。

- A：1
- B：0
- C：3
- D：6

```json
{
  "input": {
    "joint": {
      "id": "elevation-axis",
      "name": "Telescope elevation axis",
      "type": "revolute",
      "parent": "dome",
      "child": "telescope",
      "anchorParent": [
        2.220446049250313e-16,
        2.607857332424569,
        0
      ],
      "anchorChild": [
        0,
        0.3,
        -1.8875000000000002
      ],
      "axis": [
        1,
        0,
        0
      ],
      "limits": [
        -0.15,
        1.25
      ]
    }
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 维修间隙预算（h3-adaptive-radio-observatory-clearance-margin）

给定理想直槽净宽、工具宽度、单侧安全余量，工具是否满足横向间隙要求？

能力：维修间隙预算；形式：single-choice；证据：model-state。

- A：feasible
- B：blocked

```json
{
  "input": {
    "module": "camera-pack",
    "aperture": 0.62,
    "toolWidth": 0.55,
    "eachSideMargin": 0.05
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 载荷力矩（h3-adaptive-radio-observatory-load-moment）

绕给定原点的载荷力矩r×F是多少？采用右手系，忽略其他力。

能力：载荷力矩；形式：single-choice；证据：model-state。

- A：[0,0,0]
- B：[0,-3,0]
- C：[0,0,-9]
- D：[0,0,9]

```json
{
  "input": {
    "module": "camera-pack",
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
    "choiceId": "C"
  }
}
```

### 非均匀先验更新（h3-adaptive-radio-observatory-weighted-posterior）

先验权重未归一化，观测只保留normal和jammed，求jammed后验概率。

能力：非均匀先验更新；形式：single-choice；证据：finite-world。

- A：0.75
- B：0.5
- C：0
- D：1

```json
{
  "input": {
    "module": "camera-pack",
    "worlds": [
      "normal",
      "jammed",
      "loose"
    ],
    "weights": [
      2,
      6,
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

### 风险最小决策（h3-adaptive-radio-observatory-expected-loss）

继续运行期望损失=p×failureLoss，预防维修损失=repairCost，选择损失较低者；并列选继续。

能力：风险最小决策；形式：single-choice；证据：finite-world。

- A：repair
- B：continue

```json
{
  "input": {
    "faultProbability": 0.1,
    "repairCost": 7,
    "failureLoss": 13,
    "module": "camera-pack"
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 轨迹阈值判定（h3-adaptive-radio-observatory-trace-threshold）

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
        "displacement": 0.001663199865680958
      },
      {
        "time": 0.10833333333333334,
        "displacement": 0.006418225690291193
      },
      {
        "time": 0.20833333333333334,
        "displacement": 0.0025447712205475064
      },
      {
        "time": 0.30833333333333335,
        "displacement": 0.0017892972173478123
      },
      {
        "time": 0.4083333333333333,
        "displacement": 0.0015322098939430301
      },
      {
        "time": 0.5083333333333333,
        "displacement": 0.00025628111125773
      },
      {
        "time": 0.6083333333333333,
        "displacement": 0.0006812265144248621
      },
      {
        "time": 0.7083333333333334,
        "displacement": 0.00009927762046968697
      },
      {
        "time": 0.8083333333333333,
        "displacement": 0.00024011782269040257
      },
      {
        "time": 0.9083333333333333,
        "displacement": 0.00004792039718781467
      },
      {
        "time": 1,
        "displacement": 0.00004792039718781467
      }
    ],
    "threshold": 0.005134580552232954
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 安全联锁维修（h3-adaptive-radio-observatory-guarded-repair）

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
        "id": "release:camera-pack",
        "label": "release camera-pack",
        "requires": [
          "done:relock:camera-pack"
        ],
        "forbids": [
          "done:release:camera-pack"
        ],
        "adds": [
          "done:release:camera-pack",
          "ready:camera-pack",
          "tool:free"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "camera-pack"
        }
      },
      {
        "id": "relock:camera-pack",
        "label": "relock camera-pack",
        "requires": [
          "done:verify:camera-pack"
        ],
        "forbids": [
          "done:relock:camera-pack"
        ],
        "adds": [
          "done:relock:camera-pack"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "camera-pack"
        }
      },
      {
        "id": "verify:camera-pack",
        "label": "verify camera-pack",
        "requires": [
          "done:replace:camera-pack"
        ],
        "forbids": [
          "done:verify:camera-pack"
        ],
        "adds": [
          "done:verify:camera-pack"
        ],
        "deletes": [
          "fault:camera-pack",
          "misaligned:camera-pack"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "camera-pack"
        }
      },
      {
        "id": "replace:camera-pack",
        "label": "replace camera-pack",
        "requires": [
          "done:unlock:camera-pack"
        ],
        "forbids": [
          "done:replace:camera-pack"
        ],
        "adds": [
          "done:replace:camera-pack"
        ],
        "deletes": [],
        "cost": 2,
        "visual": {
          "moduleId": "camera-pack"
        }
      },
      {
        "id": "unlock:camera-pack",
        "label": "unlock camera-pack",
        "requires": [
          "done:support:camera-pack"
        ],
        "forbids": [
          "done:unlock:camera-pack"
        ],
        "adds": [
          "done:unlock:camera-pack"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "camera-pack"
        }
      },
      {
        "id": "support:camera-pack",
        "label": "support camera-pack",
        "requires": [
          "done:isolate:camera-pack"
        ],
        "forbids": [
          "done:support:camera-pack"
        ],
        "adds": [
          "done:support:camera-pack"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "camera-pack"
        }
      },
      {
        "id": "isolate:camera-pack",
        "label": "isolate camera-pack",
        "requires": [
          "tool:free",
          "fault:camera-pack"
        ],
        "forbids": [
          "done:isolate:camera-pack"
        ],
        "adds": [
          "done:isolate:camera-pack"
        ],
        "deletes": [
          "tool:free"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "camera-pack"
        }
      }
    ],
    "initialFacts": [
      "tool:free",
      "fault:camera-pack"
    ],
    "initialModules": [
      "foundation",
      "dome",
      "telescope",
      "camera-pack"
    ],
    "goalFacts": [
      "ready:camera-pack"
    ],
    "absentFacts": [
      "unverified"
    ],
    "budget": 8
  },
  "answer": {
    "actionIds": [
      "isolate:camera-pack",
      "support:camera-pack",
      "unlock:camera-pack",
      "replace:camera-pack",
      "verify:camera-pack",
      "relock:camera-pack",
      "release:camera-pack"
    ]
  }
}
```

### 失败状态回退（h3-adaptive-radio-observatory-rollback）

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
        "id": "resume:camera-pack",
        "label": "resume camera-pack",
        "requires": [
          "done:verify:camera-pack"
        ],
        "forbids": [
          "done:resume:camera-pack"
        ],
        "adds": [
          "done:resume:camera-pack",
          "ready:camera-pack",
          "tool:free"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "camera-pack"
        }
      },
      {
        "id": "verify:camera-pack",
        "label": "verify camera-pack",
        "requires": [
          "done:align:camera-pack"
        ],
        "forbids": [
          "done:verify:camera-pack"
        ],
        "adds": [
          "done:verify:camera-pack"
        ],
        "deletes": [
          "fault:camera-pack",
          "misaligned:camera-pack"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "camera-pack"
        }
      },
      {
        "id": "align:camera-pack",
        "label": "align camera-pack",
        "requires": [
          "done:undo:camera-pack"
        ],
        "forbids": [
          "done:align:camera-pack"
        ],
        "adds": [
          "done:align:camera-pack"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "camera-pack",
          "visible": true
        }
      },
      {
        "id": "undo:camera-pack",
        "label": "undo camera-pack",
        "requires": [
          "done:isolate:camera-pack"
        ],
        "forbids": [
          "done:undo:camera-pack"
        ],
        "adds": [
          "done:undo:camera-pack"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "camera-pack",
          "visible": false
        }
      },
      {
        "id": "isolate:camera-pack",
        "label": "isolate camera-pack",
        "requires": [
          "tool:free",
          "fault:camera-pack"
        ],
        "forbids": [
          "done:isolate:camera-pack"
        ],
        "adds": [
          "done:isolate:camera-pack"
        ],
        "deletes": [
          "tool:free"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "camera-pack"
        }
      }
    ],
    "initialFacts": [
      "tool:free",
      "fault:camera-pack",
      "misaligned:camera-pack"
    ],
    "initialModules": [
      "foundation",
      "dome",
      "telescope",
      "camera-pack"
    ],
    "goalFacts": [
      "ready:camera-pack"
    ],
    "absentFacts": [
      "unverified"
    ],
    "budget": 5
  },
  "answer": {
    "actionIds": [
      "isolate:camera-pack",
      "undo:camera-pack",
      "align:camera-pack",
      "verify:camera-pack",
      "resume:camera-pack"
    ]
  }
}
```

### 共享工具协同维修（h3-adaptive-radio-observatory-resource-repair）

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
        "id": "release:camera-pack",
        "label": "release camera-pack",
        "requires": [
          "done:relock:camera-pack"
        ],
        "forbids": [
          "done:release:camera-pack"
        ],
        "adds": [
          "done:release:camera-pack",
          "ready:camera-pack",
          "tool:free"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "camera-pack"
        }
      },
      {
        "id": "relock:camera-pack",
        "label": "relock camera-pack",
        "requires": [
          "done:verify:camera-pack"
        ],
        "forbids": [
          "done:relock:camera-pack"
        ],
        "adds": [
          "done:relock:camera-pack"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "camera-pack"
        }
      },
      {
        "id": "verify:camera-pack",
        "label": "verify camera-pack",
        "requires": [
          "done:replace:camera-pack"
        ],
        "forbids": [
          "done:verify:camera-pack"
        ],
        "adds": [
          "done:verify:camera-pack"
        ],
        "deletes": [
          "fault:camera-pack",
          "misaligned:camera-pack"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "camera-pack"
        }
      },
      {
        "id": "replace:camera-pack",
        "label": "replace camera-pack",
        "requires": [
          "done:unlock:camera-pack"
        ],
        "forbids": [
          "done:replace:camera-pack"
        ],
        "adds": [
          "done:replace:camera-pack"
        ],
        "deletes": [],
        "cost": 2,
        "visual": {
          "moduleId": "camera-pack"
        }
      },
      {
        "id": "unlock:camera-pack",
        "label": "unlock camera-pack",
        "requires": [
          "done:support:camera-pack"
        ],
        "forbids": [
          "done:unlock:camera-pack"
        ],
        "adds": [
          "done:unlock:camera-pack"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "camera-pack"
        }
      },
      {
        "id": "support:camera-pack",
        "label": "support camera-pack",
        "requires": [
          "done:isolate:camera-pack"
        ],
        "forbids": [
          "done:support:camera-pack"
        ],
        "adds": [
          "done:support:camera-pack"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "camera-pack"
        }
      },
      {
        "id": "isolate:camera-pack",
        "label": "isolate camera-pack",
        "requires": [
          "tool:free",
          "fault:camera-pack"
        ],
        "forbids": [
          "done:isolate:camera-pack"
        ],
        "adds": [
          "done:isolate:camera-pack"
        ],
        "deletes": [
          "tool:free"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "camera-pack"
        }
      },
      {
        "id": "release:telescope",
        "label": "release telescope",
        "requires": [
          "done:relock:telescope"
        ],
        "forbids": [
          "done:release:telescope"
        ],
        "adds": [
          "done:release:telescope",
          "ready:telescope",
          "tool:free"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "telescope"
        }
      },
      {
        "id": "relock:telescope",
        "label": "relock telescope",
        "requires": [
          "done:verify:telescope"
        ],
        "forbids": [
          "done:relock:telescope"
        ],
        "adds": [
          "done:relock:telescope"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "telescope"
        }
      },
      {
        "id": "verify:telescope",
        "label": "verify telescope",
        "requires": [
          "done:replace:telescope"
        ],
        "forbids": [
          "done:verify:telescope"
        ],
        "adds": [
          "done:verify:telescope"
        ],
        "deletes": [
          "fault:telescope",
          "misaligned:telescope"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "telescope"
        }
      },
      {
        "id": "replace:telescope",
        "label": "replace telescope",
        "requires": [
          "done:unlock:telescope"
        ],
        "forbids": [
          "done:replace:telescope"
        ],
        "adds": [
          "done:replace:telescope"
        ],
        "deletes": [],
        "cost": 2,
        "visual": {
          "moduleId": "telescope"
        }
      },
      {
        "id": "unlock:telescope",
        "label": "unlock telescope",
        "requires": [
          "done:support:telescope"
        ],
        "forbids": [
          "done:unlock:telescope"
        ],
        "adds": [
          "done:unlock:telescope"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "telescope"
        }
      },
      {
        "id": "support:telescope",
        "label": "support telescope",
        "requires": [
          "done:isolate:telescope"
        ],
        "forbids": [
          "done:support:telescope"
        ],
        "adds": [
          "done:support:telescope"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "telescope"
        }
      },
      {
        "id": "isolate:telescope",
        "label": "isolate telescope",
        "requires": [
          "tool:free",
          "fault:telescope"
        ],
        "forbids": [
          "done:isolate:telescope"
        ],
        "adds": [
          "done:isolate:telescope"
        ],
        "deletes": [
          "tool:free"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "telescope"
        }
      },
      {
        "id": "release:dome",
        "label": "release dome",
        "requires": [
          "done:relock:dome"
        ],
        "forbids": [
          "done:release:dome"
        ],
        "adds": [
          "done:release:dome",
          "ready:dome",
          "tool:free"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "dome"
        }
      },
      {
        "id": "relock:dome",
        "label": "relock dome",
        "requires": [
          "done:verify:dome"
        ],
        "forbids": [
          "done:relock:dome"
        ],
        "adds": [
          "done:relock:dome"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "dome"
        }
      },
      {
        "id": "verify:dome",
        "label": "verify dome",
        "requires": [
          "done:replace:dome"
        ],
        "forbids": [
          "done:verify:dome"
        ],
        "adds": [
          "done:verify:dome"
        ],
        "deletes": [
          "fault:dome",
          "misaligned:dome"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "dome"
        }
      },
      {
        "id": "replace:dome",
        "label": "replace dome",
        "requires": [
          "done:unlock:dome"
        ],
        "forbids": [
          "done:replace:dome"
        ],
        "adds": [
          "done:replace:dome"
        ],
        "deletes": [],
        "cost": 2,
        "visual": {
          "moduleId": "dome"
        }
      },
      {
        "id": "unlock:dome",
        "label": "unlock dome",
        "requires": [
          "done:support:dome"
        ],
        "forbids": [
          "done:unlock:dome"
        ],
        "adds": [
          "done:unlock:dome"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "dome"
        }
      },
      {
        "id": "support:dome",
        "label": "support dome",
        "requires": [
          "done:isolate:dome"
        ],
        "forbids": [
          "done:support:dome"
        ],
        "adds": [
          "done:support:dome"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "dome"
        }
      },
      {
        "id": "isolate:dome",
        "label": "isolate dome",
        "requires": [
          "tool:free",
          "fault:dome"
        ],
        "forbids": [
          "done:isolate:dome"
        ],
        "adds": [
          "done:isolate:dome"
        ],
        "deletes": [
          "tool:free"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "dome"
        }
      }
    ],
    "initialFacts": [
      "tool:free",
      "fault:dome",
      "fault:telescope",
      "fault:camera-pack"
    ],
    "initialModules": [
      "foundation",
      "dome",
      "telescope",
      "camera-pack"
    ],
    "goalFacts": [
      "ready:dome",
      "ready:telescope",
      "ready:camera-pack"
    ],
    "absentFacts": [
      "unverified"
    ],
    "budget": 24
  },
  "answer": {
    "actionIds": [
      "isolate:camera-pack",
      "support:camera-pack",
      "unlock:camera-pack",
      "replace:camera-pack",
      "verify:camera-pack",
      "relock:camera-pack",
      "release:camera-pack",
      "isolate:telescope",
      "support:telescope",
      "unlock:telescope",
      "replace:telescope",
      "verify:telescope",
      "relock:telescope",
      "release:telescope",
      "isolate:dome",
      "support:dome",
      "unlock:dome",
      "replace:dome",
      "verify:dome",
      "relock:dome",
      "release:dome"
    ]
  }
}
```

### 预算约束检查策略（h3-adaptive-radio-observatory-budget-policy）

提交预算内、对所有相容世界均正确的检查决策表。

能力：预算约束检查策略；形式：policy；证据：finite-world。


```json
{
  "input": {
    "module": "camera-pack",
    "worlds": [
      {
        "id": "nominal",
        "action": "continue"
      },
      {
        "id": "fault",
        "action": "tighten"
      }
    ],
    "queries": [
      {
        "id": "visual",
        "cost": 2,
        "returns": {
          "nominal": "pass",
          "fault": "fail"
        }
      },
      {
        "id": "probe",
        "cost": 0,
        "returns": {
          "nominal": "pass",
          "fault": "pass"
        }
      },
      {
        "id": "thermal",
        "cost": 3,
        "returns": {
          "nominal": "pass",
          "fault": "fail"
        }
      }
    ],
    "budget": 2
  },
  "answer": {
    "queryId": "visual",
    "decisions": {
      "pass": "continue",
      "fail": "tighten"
    }
  }
}
```

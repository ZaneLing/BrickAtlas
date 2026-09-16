## D2 仓储分流机

### 模块识别（h3-warehouse-sorter-identify）

高亮的维修模块对应哪个 ID？

能力：模块识别；形式：single-choice；证据：model-state。

- A：belt
- B：scanner
- C：diverter-gate
- D：floor

```json
{
  "input": {
    "moduleNames": [
      {
        "id": "floor",
        "name": "Sorter foundation"
      },
      {
        "id": "belt",
        "name": "Transfer conveyor"
      },
      {
        "id": "diverter-gate",
        "name": "Pivoting diverter"
      },
      {
        "id": "scanner",
        "name": "Overhead scanner"
      },
      {
        "id": "left-bin",
        "name": "Left destination bin"
      },
      {
        "id": "right-bin",
        "name": "Right destination bin"
      }
    ]
  },
  "answer": {
    "choiceId": "C"
  }
}
```

### 部件计数（h3-warehouse-sorter-count）

模块 diverter-gate 有多少个可视零件？

能力：部件计数；形式：single-choice；证据：model-state。

- A：5
- B：9
- C：6
- D：7

```json
{
  "input": {
    "parts": [
      {
        "id": "h0001",
        "moduleId": "floor",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0002",
        "moduleId": "floor",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0003",
        "moduleId": "floor",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0004",
        "moduleId": "floor",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0005",
        "moduleId": "floor",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0006",
        "moduleId": "floor",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0007",
        "moduleId": "floor",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0008",
        "moduleId": "floor",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0009",
        "moduleId": "floor",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0010",
        "moduleId": "floor",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0011",
        "moduleId": "floor",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0012",
        "moduleId": "floor",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0013",
        "moduleId": "floor",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0014",
        "moduleId": "floor",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0015",
        "moduleId": "floor",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0016",
        "moduleId": "floor",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0017",
        "moduleId": "floor",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0018",
        "moduleId": "floor",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0019",
        "moduleId": "floor",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0020",
        "moduleId": "floor",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0021",
        "moduleId": "floor",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0022",
        "moduleId": "floor",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0023",
        "moduleId": "floor",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0024",
        "moduleId": "floor",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0025",
        "moduleId": "belt",
        "shape": "plate",
        "color": "#2878b8"
      },
      {
        "id": "h0026",
        "moduleId": "belt",
        "shape": "plate",
        "color": "#2878b8"
      },
      {
        "id": "h0027",
        "moduleId": "belt",
        "shape": "plate",
        "color": "#2878b8"
      },
      {
        "id": "h0028",
        "moduleId": "belt",
        "shape": "plate",
        "color": "#2878b8"
      },
      {
        "id": "h0029",
        "moduleId": "belt",
        "shape": "plate",
        "color": "#2878b8"
      },
      {
        "id": "h0030",
        "moduleId": "belt",
        "shape": "plate",
        "color": "#2878b8"
      },
      {
        "id": "h0031",
        "moduleId": "belt",
        "shape": "plate",
        "color": "#2878b8"
      },
      {
        "id": "h0032",
        "moduleId": "belt",
        "shape": "plate",
        "color": "#2878b8"
      },
      {
        "id": "h0033",
        "moduleId": "belt",
        "shape": "plate",
        "color": "#2878b8"
      },
      {
        "id": "h0034",
        "moduleId": "belt",
        "shape": "plate",
        "color": "#2878b8"
      },
      {
        "id": "h0035",
        "moduleId": "belt",
        "shape": "plate",
        "color": "#2878b8"
      },
      {
        "id": "h0036",
        "moduleId": "belt",
        "shape": "plate",
        "color": "#2878b8"
      },
      {
        "id": "h0037",
        "moduleId": "diverter-gate",
        "shape": "beam",
        "color": "#e8792e"
      },
      {
        "id": "h0038",
        "moduleId": "diverter-gate",
        "shape": "beam",
        "color": "#e8792e"
      },
      {
        "id": "h0039",
        "moduleId": "diverter-gate",
        "shape": "beam",
        "color": "#e8792e"
      },
      {
        "id": "h0040",
        "moduleId": "diverter-gate",
        "shape": "beam",
        "color": "#e8792e"
      },
      {
        "id": "h0041",
        "moduleId": "diverter-gate",
        "shape": "beam",
        "color": "#e8792e"
      },
      {
        "id": "h0042",
        "moduleId": "diverter-gate",
        "shape": "beam",
        "color": "#e8792e"
      },
      {
        "id": "h0043",
        "moduleId": "scanner",
        "shape": "brick",
        "color": "#26323b"
      },
      {
        "id": "h0044",
        "moduleId": "scanner",
        "shape": "brick",
        "color": "#26323b"
      },
      {
        "id": "h0045",
        "moduleId": "scanner",
        "shape": "brick",
        "color": "#26323b"
      },
      {
        "id": "h0046",
        "moduleId": "scanner",
        "shape": "brick",
        "color": "#26323b"
      },
      {
        "id": "h0047",
        "moduleId": "scanner",
        "shape": "brick",
        "color": "#26323b"
      },
      {
        "id": "h0048",
        "moduleId": "scanner",
        "shape": "brick",
        "color": "#26323b"
      },
      {
        "id": "h0049",
        "moduleId": "scanner",
        "shape": "brick",
        "color": "#26323b"
      },
      {
        "id": "h0050",
        "moduleId": "scanner",
        "shape": "brick",
        "color": "#26323b"
      },
      {
        "id": "h0051",
        "moduleId": "scanner",
        "shape": "beam",
        "color": "#26323b"
      },
      {
        "id": "h0052",
        "moduleId": "scanner",
        "shape": "window",
        "color": "#79c7d8"
      },
      {
        "id": "h0053",
        "moduleId": "left-bin",
        "shape": "plate",
        "color": "#3f8a61"
      },
      {
        "id": "h0054",
        "moduleId": "left-bin",
        "shape": "plate",
        "color": "#3f8a61"
      },
      {
        "id": "h0055",
        "moduleId": "left-bin",
        "shape": "plate",
        "color": "#3f8a61"
      },
      {
        "id": "h0056",
        "moduleId": "left-bin",
        "shape": "plate",
        "color": "#3f8a61"
      },
      {
        "id": "h0057",
        "moduleId": "right-bin",
        "shape": "plate",
        "color": "#f2bf3c"
      },
      {
        "id": "h0058",
        "moduleId": "right-bin",
        "shape": "plate",
        "color": "#f2bf3c"
      },
      {
        "id": "h0059",
        "moduleId": "right-bin",
        "shape": "plate",
        "color": "#f2bf3c"
      },
      {
        "id": "h0060",
        "moduleId": "right-bin",
        "shape": "plate",
        "color": "#f2bf3c"
      }
    ]
  },
  "answer": {
    "choiceId": "C"
  }
}
```

### 颜色识别（h3-warehouse-sorter-color）

零件 h0037 的颜色值是什么？

能力：颜色识别；形式：single-choice；证据：model-state。

- A：#d43a32
- B：#f2bf3c
- C：#e8792e
- D：#2878b8

```json
{
  "input": {
    "part": {
      "id": "h0037",
      "moduleId": "diverter-gate",
      "shape": "beam",
      "size": [
        0.5,
        0.5,
        0.35
      ],
      "position": [
        -1.375,
        0,
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
    "choiceId": "C"
  }
}
```

### 三维位置（h3-warehouse-sorter-position）

模块 diverter-gate 的世界包围盒中心是什么？

能力：三维位置；形式：single-choice；证据：model-state。

- A：[0,2.025,-1.575]
- B：[1.375,1.25,0]
- C：[0,0.2,0]
- D：[0,0.8,0]

```json
{
  "input": {
    "centers": {
      "floor": [
        0,
        0.2,
        0
      ],
      "belt": [
        0,
        0.8,
        0
      ],
      "diverter-gate": [
        1.375,
        1.25,
        0
      ],
      "scanner": [
        0,
        2.025,
        -1.575
      ],
      "left-bin": [
        3,
        0.75,
        -3
      ],
      "right-bin": [
        3,
        0.75,
        3
      ]
    }
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 关节类型（h3-warehouse-sorter-joint-type）

gate-pivot 采用什么约束类型？

能力：关节类型；形式：single-choice；证据：model-state。

- A：revolute
- B：fixed
- C：prismatic
- D：spring

```json
{
  "input": {
    "joint": {
      "id": "gate-pivot",
      "name": "gate pivot",
      "type": "revolute",
      "parent": "belt",
      "child": "diverter-gate",
      "anchorParent": [
        0,
        0.44999999999999996,
        0
      ],
      "anchorChild": [
        -1.375,
        0,
        0
      ],
      "axis": [
        0,
        1,
        0
      ],
      "limits": [
        -0.7,
        0.7
      ]
    }
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 直接连接（h3-warehouse-sorter-parent）

diverter-gate 的直接父模块集合是什么？

能力：直接连接；形式：single-choice；证据：model-state。

- A：[]
- B：["floor","belt","diverter-gate","scanner","left-bin","right-bin"]
- C：["belt"]
- D：["diverter-gate"]

```json
{
  "input": {
    "joints": [
      {
        "id": "belt-drive",
        "name": "belt drive",
        "type": "prismatic",
        "parent": "floor",
        "child": "belt",
        "anchorParent": [
          0,
          0.49999999999999994,
          0
        ],
        "anchorChild": [
          0,
          -0.10000000000000009,
          0
        ],
        "axis": [
          1,
          0,
          0
        ],
        "limits": [
          -0.5,
          0.5
        ]
      },
      {
        "id": "gate-pivot",
        "name": "gate pivot",
        "type": "revolute",
        "parent": "belt",
        "child": "diverter-gate",
        "anchorParent": [
          0,
          0.44999999999999996,
          0
        ],
        "anchorChild": [
          -1.375,
          0,
          0
        ],
        "axis": [
          0,
          1,
          0
        ],
        "limits": [
          -0.7,
          0.7
        ]
      },
      {
        "id": "scanner-frame",
        "name": "scanner frame",
        "type": "fixed",
        "parent": "floor",
        "child": "scanner",
        "anchorParent": [
          0,
          0.3,
          -1.7
        ],
        "anchorChild": [
          0,
          -1.525,
          -0.125
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "left-bin-lock",
        "name": "left bin lock",
        "type": "fixed",
        "parent": "floor",
        "child": "left-bin",
        "anchorParent": [
          3,
          0.39999999999999997,
          -3
        ],
        "anchorChild": [
          0,
          -0.15000000000000002,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "right-bin-lock",
        "name": "right bin lock",
        "type": "fixed",
        "parent": "floor",
        "child": "right-bin",
        "anchorParent": [
          3,
          0.39999999999999997,
          3
        ],
        "anchorChild": [
          0,
          -0.15000000000000002,
          0
        ],
        "axis": [
          0,
          1,
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

### 基座识别（h3-warehouse-sorter-anchor）

哪些模块被声明为固定基座？

能力：基座识别；形式：single-choice；证据：model-state。

- A：[]
- B：["floor","belt","diverter-gate","scanner","left-bin","right-bin"]
- C：["diverter-gate"]
- D：["floor"]

```json
{
  "input": {
    "modules": [
      {
        "id": "floor",
        "name": "Sorter foundation",
        "role": "foundation",
        "anchored": true,
        "mass": 18,
        "position": [
          0,
          0.2,
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
        "id": "belt",
        "name": "Transfer conveyor",
        "role": "transport",
        "anchored": false,
        "mass": 5,
        "position": [
          0,
          0.8,
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
        "id": "diverter-gate",
        "name": "Pivoting diverter",
        "role": "actuator",
        "anchored": false,
        "mass": 2,
        "position": [
          1.375,
          1.25,
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
        "id": "scanner",
        "name": "Overhead scanner",
        "role": "sensor",
        "anchored": false,
        "mass": 1,
        "position": [
          0,
          2.025,
          -1.575
        ],
        "rotation": [
          0,
          0,
          0,
          1
        ]
      },
      {
        "id": "left-bin",
        "name": "Left destination bin",
        "role": "payload-zone",
        "anchored": false,
        "mass": 3,
        "position": [
          3,
          0.75,
          -3
        ],
        "rotation": [
          0,
          0,
          0,
          1
        ]
      },
      {
        "id": "right-bin",
        "name": "Right destination bin",
        "role": "payload-zone",
        "anchored": false,
        "mass": 3,
        "position": [
          3,
          0.75,
          3
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
    "choiceId": "D"
  }
}
```

### 接口计数（h3-warehouse-sorter-degree）

diverter-gate 连接几个声明关节？平行关节分别计数。

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
        "id": "belt-drive",
        "name": "belt drive",
        "type": "prismatic",
        "parent": "floor",
        "child": "belt",
        "anchorParent": [
          0,
          0.49999999999999994,
          0
        ],
        "anchorChild": [
          0,
          -0.10000000000000009,
          0
        ],
        "axis": [
          1,
          0,
          0
        ],
        "limits": [
          -0.5,
          0.5
        ]
      },
      {
        "id": "gate-pivot",
        "name": "gate pivot",
        "type": "revolute",
        "parent": "belt",
        "child": "diverter-gate",
        "anchorParent": [
          0,
          0.44999999999999996,
          0
        ],
        "anchorChild": [
          -1.375,
          0,
          0
        ],
        "axis": [
          0,
          1,
          0
        ],
        "limits": [
          -0.7,
          0.7
        ]
      },
      {
        "id": "scanner-frame",
        "name": "scanner frame",
        "type": "fixed",
        "parent": "floor",
        "child": "scanner",
        "anchorParent": [
          0,
          0.3,
          -1.7
        ],
        "anchorChild": [
          0,
          -1.525,
          -0.125
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "left-bin-lock",
        "name": "left bin lock",
        "type": "fixed",
        "parent": "floor",
        "child": "left-bin",
        "anchorParent": [
          3,
          0.39999999999999997,
          -3
        ],
        "anchorChild": [
          0,
          -0.15000000000000002,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "right-bin-lock",
        "name": "right bin lock",
        "type": "fixed",
        "parent": "floor",
        "child": "right-bin",
        "anchorParent": [
          3,
          0.39999999999999997,
          3
        ],
        "anchorChild": [
          0,
          -0.15000000000000002,
          0
        ],
        "axis": [
          0,
          1,
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

### 局部改色（h3-warehouse-sorter-recolor）

仅将 h0037 改成 #e8792e，其他零件不变。选择正确补丁。

能力：局部改色；形式：single-choice；证据：model-state。

- A：{"id":"h0037","color":"#e8792e"}
- B：{"id":"h0038","color":"#e8792e"}
- C：{"id":"h0037","color":"#2878b8"}
- D：{"id":"*","color":"#e8792e"}

```json
{
  "input": {
    "part": {
      "id": "h0037",
      "moduleId": "diverter-gate",
      "shape": "beam",
      "size": [
        0.5,
        0.5,
        0.35
      ],
      "position": [
        -1.375,
        0,
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

### 补装部件（h3-warehouse-sorter-add）

模块 diverter-gate 缺失零件 h0037。选择与目标清单一致的补装描述。

能力：补装部件；形式：single-choice；证据：model-state。

- A：{"id":"h0037","moduleId":"diverter-gate","shape":"beam","size":[0.5,0.5,0.35],"position":[-1.375,0,0],"rotation":[0,0,0,1],"color":"#000000"}
- B：{"id":"h0037","moduleId":"diverter-gate","shape":"beam","size":[0.5,0.5,0.35],"position":[-1.375,0,0],"rotation":[0,0,0,1],"color":"#e8792e"}
- C：{"id":"h0037","moduleId":"floor","shape":"beam","size":[0.5,0.5,0.35],"position":[-1.375,0,0],"rotation":[0,0,0,1],"color":"#e8792e"}
- D：{"id":"h0037","moduleId":"diverter-gate","shape":"beam","size":[3,3,3],"position":[-1.375,0,0],"rotation":[0,0,0,1],"color":"#e8792e"}

```json
{
  "input": {
    "targetPart": {
      "id": "h0037",
      "moduleId": "diverter-gate",
      "shape": "beam",
      "size": [
        0.5,
        0.5,
        0.35
      ],
      "position": [
        -1.375,
        0,
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
      "h0001",
      "h0002",
      "h0003",
      "h0004",
      "h0005",
      "h0006",
      "h0007",
      "h0008",
      "h0009",
      "h0010",
      "h0011",
      "h0012",
      "h0013",
      "h0014",
      "h0015",
      "h0016",
      "h0017",
      "h0018",
      "h0019",
      "h0020",
      "h0021",
      "h0022",
      "h0023",
      "h0024",
      "h0025",
      "h0026",
      "h0027",
      "h0028",
      "h0029",
      "h0030",
      "h0031",
      "h0032",
      "h0033",
      "h0034",
      "h0035",
      "h0036",
      "h0038",
      "h0039",
      "h0040",
      "h0041",
      "h0042",
      "h0043",
      "h0044",
      "h0045",
      "h0046",
      "h0047",
      "h0048",
      "h0049",
      "h0050",
      "h0051",
      "h0052",
      "h0053",
      "h0054",
      "h0055",
      "h0056",
      "h0057",
      "h0058",
      "h0059",
      "h0060"
    ]
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 安全拆除（h3-warehouse-sorter-remove）

按声明依赖图，当前可以先拆哪些叶模块？

能力：安全拆除；形式：single-choice；证据：model-state。

- A：["floor","belt","diverter-gate","scanner","left-bin","right-bin"]
- B：["diverter-gate","left-bin","right-bin","scanner"]
- C：["floor"]
- D：[]

```json
{
  "input": {
    "joints": [
      {
        "id": "belt-drive",
        "name": "belt drive",
        "type": "prismatic",
        "parent": "floor",
        "child": "belt",
        "anchorParent": [
          0,
          0.49999999999999994,
          0
        ],
        "anchorChild": [
          0,
          -0.10000000000000009,
          0
        ],
        "axis": [
          1,
          0,
          0
        ],
        "limits": [
          -0.5,
          0.5
        ]
      },
      {
        "id": "gate-pivot",
        "name": "gate pivot",
        "type": "revolute",
        "parent": "belt",
        "child": "diverter-gate",
        "anchorParent": [
          0,
          0.44999999999999996,
          0
        ],
        "anchorChild": [
          -1.375,
          0,
          0
        ],
        "axis": [
          0,
          1,
          0
        ],
        "limits": [
          -0.7,
          0.7
        ]
      },
      {
        "id": "scanner-frame",
        "name": "scanner frame",
        "type": "fixed",
        "parent": "floor",
        "child": "scanner",
        "anchorParent": [
          0,
          0.3,
          -1.7
        ],
        "anchorChild": [
          0,
          -1.525,
          -0.125
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "left-bin-lock",
        "name": "left bin lock",
        "type": "fixed",
        "parent": "floor",
        "child": "left-bin",
        "anchorParent": [
          3,
          0.39999999999999997,
          -3
        ],
        "anchorChild": [
          0,
          -0.15000000000000002,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "right-bin-lock",
        "name": "right bin lock",
        "type": "fixed",
        "parent": "floor",
        "child": "right-bin",
        "anchorParent": [
          3,
          0.39999999999999997,
          3
        ],
        "anchorChild": [
          0,
          -0.15000000000000002,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      }
    ],
    "modules": [
      "floor",
      "belt",
      "diverter-gate",
      "scanner",
      "left-bin",
      "right-bin"
    ]
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 替换选择（h3-warehouse-sorter-replace）

在成本上限内选择刚度最大的替换件；并列选成本低者，再并列选ID字典序最小者。

能力：替换选择；形式：single-choice；证据：model-state。

- A：stock-3
- B：stock-0
- C：stock-1
- D：stock-2

```json
{
  "input": {
    "alternatives": [
      {
        "id": "stock-0",
        "cost": 8,
        "stiffness": 6,
        "mass": 1.1
      },
      {
        "id": "stock-1",
        "cost": 8,
        "stiffness": 3,
        "mass": 1.5
      },
      {
        "id": "stock-2",
        "cost": 4,
        "stiffness": 3,
        "mass": 0.6
      },
      {
        "id": "stock-3",
        "cost": 8,
        "stiffness": 8,
        "mass": 1.8
      }
    ],
    "maxCost": 8
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 平移纠偏（h3-warehouse-sorter-translate）

观察到相对目标的平移误差 delta，选择补偿平移。

能力：平移纠偏；形式：single-choice；证据：model-state。

- A：[0,2,0]
- B：[-2,0,2]
- C：[2,0,-2]
- D：[0,0,0]

```json
{
  "input": {
    "delta": [
      2,
      0,
      -2
    ],
    "target": "diverter-gate"
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 姿态纠偏（h3-warehouse-sorter-rotate）

选择从当前yaw到目标yaw的最短有符号旋转；恰好180°时使用-180°。

能力：姿态纠偏；形式：single-choice；证据：model-state。

- A：-90
- B：-180
- C：0
- D：90

```json
{
  "input": {
    "module": "diverter-gate",
    "currentYaw": 90,
    "targetYaw": 90
  },
  "answer": {
    "choiceId": "C"
  }
}
```

### 下一步放置（h3-warehouse-sorter-next-module）

已完成给定前缀，选择所有前置依赖已满足的下一模块集合。

能力：下一步放置；形式：single-choice；证据：model-state。

- A：[]
- B：["floor","belt","scanner"]
- C：["floor"]
- D：["diverter-gate","left-bin","right-bin"]

```json
{
  "input": {
    "prefix": [
      "floor",
      "belt",
      "scanner"
    ],
    "joints": [
      {
        "id": "belt-drive",
        "name": "belt drive",
        "type": "prismatic",
        "parent": "floor",
        "child": "belt",
        "anchorParent": [
          0,
          0.49999999999999994,
          0
        ],
        "anchorChild": [
          0,
          -0.10000000000000009,
          0
        ],
        "axis": [
          1,
          0,
          0
        ],
        "limits": [
          -0.5,
          0.5
        ]
      },
      {
        "id": "gate-pivot",
        "name": "gate pivot",
        "type": "revolute",
        "parent": "belt",
        "child": "diverter-gate",
        "anchorParent": [
          0,
          0.44999999999999996,
          0
        ],
        "anchorChild": [
          -1.375,
          0,
          0
        ],
        "axis": [
          0,
          1,
          0
        ],
        "limits": [
          -0.7,
          0.7
        ]
      },
      {
        "id": "scanner-frame",
        "name": "scanner frame",
        "type": "fixed",
        "parent": "floor",
        "child": "scanner",
        "anchorParent": [
          0,
          0.3,
          -1.7
        ],
        "anchorChild": [
          0,
          -1.525,
          -0.125
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "left-bin-lock",
        "name": "left bin lock",
        "type": "fixed",
        "parent": "floor",
        "child": "left-bin",
        "anchorParent": [
          3,
          0.39999999999999997,
          -3
        ],
        "anchorChild": [
          0,
          -0.15000000000000002,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "right-bin-lock",
        "name": "right bin lock",
        "type": "fixed",
        "parent": "floor",
        "child": "right-bin",
        "anchorParent": [
          3,
          0.39999999999999997,
          3
        ],
        "anchorChild": [
          0,
          -0.15000000000000002,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      }
    ],
    "modules": [
      "floor",
      "belt",
      "diverter-gate",
      "scanner",
      "left-bin",
      "right-bin"
    ]
  },
  "answer": {
    "choiceId": "D"
  }
}
```

### 库存核算（h3-warehouse-sorter-inventory）

备件库有 14 件，替换模块需 6 件，还剩多少？

能力：库存核算；形式：single-choice；证据：model-state。

- A：9
- B：7
- C：11
- D：8

```json
{
  "input": {
    "available": 14,
    "required": 6
  },
  "answer": {
    "choiceId": "D"
  }
}
```

### 子装配边界（h3-warehouse-sorter-boundary）

隔离 diverter-gate 需要断开哪些边界关节？

能力：子装配边界；形式：single-choice；证据：model-state。

- A：["belt-drive","gate-pivot","scanner-frame","left-bin-lock","right-bin-lock"]
- B：["gate-pivot"]
- C：[]

```json
{
  "input": {
    "joints": [
      {
        "id": "belt-drive",
        "name": "belt drive",
        "type": "prismatic",
        "parent": "floor",
        "child": "belt",
        "anchorParent": [
          0,
          0.49999999999999994,
          0
        ],
        "anchorChild": [
          0,
          -0.10000000000000009,
          0
        ],
        "axis": [
          1,
          0,
          0
        ],
        "limits": [
          -0.5,
          0.5
        ]
      },
      {
        "id": "gate-pivot",
        "name": "gate pivot",
        "type": "revolute",
        "parent": "belt",
        "child": "diverter-gate",
        "anchorParent": [
          0,
          0.44999999999999996,
          0
        ],
        "anchorChild": [
          -1.375,
          0,
          0
        ],
        "axis": [
          0,
          1,
          0
        ],
        "limits": [
          -0.7,
          0.7
        ]
      },
      {
        "id": "scanner-frame",
        "name": "scanner frame",
        "type": "fixed",
        "parent": "floor",
        "child": "scanner",
        "anchorParent": [
          0,
          0.3,
          -1.7
        ],
        "anchorChild": [
          0,
          -1.525,
          -0.125
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "left-bin-lock",
        "name": "left bin lock",
        "type": "fixed",
        "parent": "floor",
        "child": "left-bin",
        "anchorParent": [
          3,
          0.39999999999999997,
          -3
        ],
        "anchorChild": [
          0,
          -0.15000000000000002,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "right-bin-lock",
        "name": "right bin lock",
        "type": "fixed",
        "parent": "floor",
        "child": "right-bin",
        "anchorParent": [
          3,
          0.39999999999999997,
          3
        ],
        "anchorChild": [
          0,
          -0.15000000000000002,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      }
    ],
    "target": "diverter-gate"
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 最小干预（h3-warehouse-sorter-no-op）

当前模块颜色已满足指令，且无需改变位姿。最少需要几次编辑？

能力：最小干预；形式：single-choice；证据：model-state。

- A：1
- B：2
- C：6
- D：0

```json
{
  "input": {
    "module": "diverter-gate"
  },
  "answer": {
    "choiceId": "D"
  }
}
```

### 全过程依赖（h3-warehouse-sorter-prefix）

给定候选顺序，首次违反前置依赖的步骤是？从 0 编号，-1 表示没有违反。

能力：全过程依赖；形式：single-choice；证据：support-graph。

- A：5
- B：0
- C：-1
- D：1

```json
{
  "input": {
    "order": [
      "left-bin",
      "floor",
      "belt",
      "scanner",
      "right-bin",
      "diverter-gate"
    ],
    "joints": [
      {
        "id": "belt-drive",
        "name": "belt drive",
        "type": "prismatic",
        "parent": "floor",
        "child": "belt",
        "anchorParent": [
          0,
          0.49999999999999994,
          0
        ],
        "anchorChild": [
          0,
          -0.10000000000000009,
          0
        ],
        "axis": [
          1,
          0,
          0
        ],
        "limits": [
          -0.5,
          0.5
        ]
      },
      {
        "id": "gate-pivot",
        "name": "gate pivot",
        "type": "revolute",
        "parent": "belt",
        "child": "diverter-gate",
        "anchorParent": [
          0,
          0.44999999999999996,
          0
        ],
        "anchorChild": [
          -1.375,
          0,
          0
        ],
        "axis": [
          0,
          1,
          0
        ],
        "limits": [
          -0.7,
          0.7
        ]
      },
      {
        "id": "scanner-frame",
        "name": "scanner frame",
        "type": "fixed",
        "parent": "floor",
        "child": "scanner",
        "anchorParent": [
          0,
          0.3,
          -1.7
        ],
        "anchorChild": [
          0,
          -1.525,
          -0.125
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "left-bin-lock",
        "name": "left bin lock",
        "type": "fixed",
        "parent": "floor",
        "child": "left-bin",
        "anchorParent": [
          3,
          0.39999999999999997,
          -3
        ],
        "anchorChild": [
          0,
          -0.15000000000000002,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "right-bin-lock",
        "name": "right bin lock",
        "type": "fixed",
        "parent": "floor",
        "child": "right-bin",
        "anchorParent": [
          3,
          0.39999999999999997,
          3
        ],
        "anchorChild": [
          0,
          -0.15000000000000002,
          0
        ],
        "axis": [
          0,
          1,
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

### 连续维修路径（h3-warehouse-sorter-access）

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
          8.760000000000002,
          1.25,
          0
        ],
        "end": [
          1.375,
          1.25,
          0
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
          1.375,
          7.475,
          0
        ],
        "end": [
          1.375,
          1.25,
          0
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
          1.375,
          1.25,
          7.96
        ],
        "end": [
          1.375,
          1.25,
          0
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

### 支撑反事实（h3-warehouse-sorter-counterfactual）

移除指定模块后，哪些其余模块失去到任一基座的关节路径？不包含被移除模块本身。

能力：支撑反事实；形式：single-choice；证据：support-graph。

- A：[]
- B：["floor","belt","diverter-gate","scanner","left-bin","right-bin"]
- C：["diverter-gate"]
- D：["belt"]

```json
{
  "input": {
    "removed": "belt",
    "roots": [
      "floor"
    ],
    "joints": [
      {
        "id": "belt-drive",
        "name": "belt drive",
        "type": "prismatic",
        "parent": "floor",
        "child": "belt",
        "anchorParent": [
          0,
          0.49999999999999994,
          0
        ],
        "anchorChild": [
          0,
          -0.10000000000000009,
          0
        ],
        "axis": [
          1,
          0,
          0
        ],
        "limits": [
          -0.5,
          0.5
        ]
      },
      {
        "id": "gate-pivot",
        "name": "gate pivot",
        "type": "revolute",
        "parent": "belt",
        "child": "diverter-gate",
        "anchorParent": [
          0,
          0.44999999999999996,
          0
        ],
        "anchorChild": [
          -1.375,
          0,
          0
        ],
        "axis": [
          0,
          1,
          0
        ],
        "limits": [
          -0.7,
          0.7
        ]
      },
      {
        "id": "scanner-frame",
        "name": "scanner frame",
        "type": "fixed",
        "parent": "floor",
        "child": "scanner",
        "anchorParent": [
          0,
          0.3,
          -1.7
        ],
        "anchorChild": [
          0,
          -1.525,
          -0.125
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "left-bin-lock",
        "name": "left bin lock",
        "type": "fixed",
        "parent": "floor",
        "child": "left-bin",
        "anchorParent": [
          3,
          0.39999999999999997,
          -3
        ],
        "anchorChild": [
          0,
          -0.15000000000000002,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "right-bin-lock",
        "name": "right bin lock",
        "type": "fixed",
        "parent": "floor",
        "child": "right-bin",
        "anchorParent": [
          3,
          0.39999999999999997,
          3
        ],
        "anchorChild": [
          0,
          -0.15000000000000002,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      }
    ],
    "modules": [
      "floor",
      "belt",
      "diverter-gate",
      "scanner",
      "left-bin",
      "right-bin"
    ]
  },
  "answer": {
    "choiceId": "C"
  }
}
```

### 冲击响应读数（h3-warehouse-sorter-dynamic）

Rapier 实际采样轨迹中的最大平移位移是多少？按四位小数报告。

能力：冲击响应读数；形式：single-choice；证据：Rapier。

- A：0.005
- B：0.205
- C：0
- D：1.005

```json
{
  "input": {
    "trace": [
      {
        "time": 0.008333333333333333,
        "displacement": 0.005004967373182012
      },
      {
        "time": 0.10833333333333334,
        "displacement": 0.000043112922369914486
      },
      {
        "time": 0.20833333333333334,
        "displacement": 0.000002574475004735177
      },
      {
        "time": 0.30833333333333335,
        "displacement": 0.0000025744731857457737
      },
      {
        "time": 0.4083333333333333,
        "displacement": 0.0000025744213445477726
      },
      {
        "time": 0.5083333333333333,
        "displacement": 0.000002573769009472926
      },
      {
        "time": 0.6083333333333333,
        "displacement": 0.0000025734645561215075
      },
      {
        "time": 0.7083333333333334,
        "displacement": 0.0000025734645561215075
      },
      {
        "time": 0.8083333333333333,
        "displacement": 0.0000025734645561215075
      },
      {
        "time": 0.9083333333333333,
        "displacement": 0.0000025734645561215075
      },
      {
        "time": 1,
        "displacement": 0.0000025734645561215075
      }
    ],
    "impulse": [
      10,
      1.8,
      3.5
    ],
    "nominalDrift": 2.384185791015625e-7,
    "scope": "采样轨迹极值，非连续时间极值；不代表实物安全阈值"
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 关节限位推理（h3-warehouse-sorter-kinematic）

下列目标位置/角度中哪些在关节声明限位内（含边界）？

能力：关节限位推理；形式：multiple-choice；证据：model-state。

- A：0
- B：-1.2
- C：1.2
- D：-0.7

```json
{
  "input": {
    "joint": "gate-pivot",
    "limits": [
      -0.7,
      0.7
    ],
    "units": "radians"
  },
  "answer": {
    "choiceIds": [
      "A",
      "D"
    ]
  }
}
```

### 约束故障诊断（h3-warehouse-sorter-diagnosis）

已检测到端点和约束类型如下，选择匹配的全部关节。

能力：约束故障诊断；形式：multiple-choice；证据：model-state。

- A：left-bin-lock
- B：gate-pivot
- C：belt-drive
- D：scanner-frame

```json
{
  "input": {
    "endpoints": [
      "belt",
      "diverter-gate"
    ],
    "type": "revolute",
    "joints": [
      {
        "id": "belt-drive",
        "name": "belt drive",
        "type": "prismatic",
        "parent": "floor",
        "child": "belt",
        "anchorParent": [
          0,
          0.49999999999999994,
          0
        ],
        "anchorChild": [
          0,
          -0.10000000000000009,
          0
        ],
        "axis": [
          1,
          0,
          0
        ],
        "limits": [
          -0.5,
          0.5
        ]
      },
      {
        "id": "gate-pivot",
        "name": "gate pivot",
        "type": "revolute",
        "parent": "belt",
        "child": "diverter-gate",
        "anchorParent": [
          0,
          0.44999999999999996,
          0
        ],
        "anchorChild": [
          -1.375,
          0,
          0
        ],
        "axis": [
          0,
          1,
          0
        ],
        "limits": [
          -0.7,
          0.7
        ]
      },
      {
        "id": "scanner-frame",
        "name": "scanner frame",
        "type": "fixed",
        "parent": "floor",
        "child": "scanner",
        "anchorParent": [
          0,
          0.3,
          -1.7
        ],
        "anchorChild": [
          0,
          -1.525,
          -0.125
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "left-bin-lock",
        "name": "left bin lock",
        "type": "fixed",
        "parent": "floor",
        "child": "left-bin",
        "anchorParent": [
          3,
          0.39999999999999997,
          -3
        ],
        "anchorChild": [
          0,
          -0.15000000000000002,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "right-bin-lock",
        "name": "right bin lock",
        "type": "fixed",
        "parent": "floor",
        "child": "right-bin",
        "anchorParent": [
          3,
          0.39999999999999997,
          3
        ],
        "anchorChild": [
          0,
          -0.15000000000000002,
          0
        ],
        "axis": [
          0,
          1,
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

### 主动检查收益（h3-warehouse-sorter-information-gain）

均匀先验四个世界，选择信息增益/成本最大的全部检查。

能力：主动检查收益；形式：multiple-choice；证据：finite-world。

- A：query-0
- B：query-2
- C：query-1

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
    "module": "diverter-gate",
    "worlds": [
      "normal",
      "jammed",
      "reversed",
      "loose"
    ]
  },
  "answer": {
    "choiceIds": [
      "C"
    ]
  }
}
```

### 不确定性与弃答（h3-warehouse-sorter-abstention）

所有相容世界是否允许同一个后续动作？选择继续执行或请求检查。

能力：不确定性与弃答；形式：single-choice；证据：finite-world。

- A：inspect
- B：commit

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
    "choiceId": "A"
  }
}
```

### 观测后信念更新（h3-warehouse-sorter-posterior）

均匀先验，得到给定观测后，jammed 世界的后验概率是多少？

能力：观测后信念更新；形式：single-choice；证据：finite-world。

- A：0.5
- B：0
- C：0.25
- D：0.3333333333333333

```json
{
  "input": {
    "module": "diverter-gate",
    "worlds": [
      "normal",
      "jammed",
      "reversed",
      "loose"
    ],
    "observationByWorld": [
      "negative",
      "positive",
      "negative",
      "positive"
    ],
    "observed": "negative"
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 多目标工程权衡（h3-warehouse-sorter-pareto）

最小成本、最小质量、最大刚度，选择完整非支配集合。

能力：多目标工程权衡；形式：multiple-choice；证据：model-state。

- A：stock-1
- B：stock-0
- C：stock-2
- D：stock-3

```json
{
  "input": {
    "alternatives": [
      {
        "id": "stock-0",
        "cost": 8,
        "stiffness": 6,
        "mass": 1.1
      },
      {
        "id": "stock-1",
        "cost": 8,
        "stiffness": 3,
        "mass": 1.5
      },
      {
        "id": "stock-2",
        "cost": 4,
        "stiffness": 3,
        "mass": 0.6
      },
      {
        "id": "stock-3",
        "cost": 8,
        "stiffness": 8,
        "mass": 1.8
      }
    ]
  },
  "answer": {
    "choiceIds": [
      "B",
      "C",
      "D"
    ]
  }
}
```

### 依赖装配（h3-warehouse-sorter-assembly）

提交 actionIds。执行公开前置条件与效果，达到所有目标且不超过预算；允许交换独立动作。

能力：依赖装配；形式：actions；证据：state-machine。


```json
{
  "input": {
    "initialFacts": [],
    "initialModules": [],
    "actions": [
      {
        "id": "place:right-bin",
        "label": "安装 right-bin",
        "requires": [
          "present:floor"
        ],
        "forbids": [
          "present:right-bin"
        ],
        "adds": [
          "present:right-bin"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "right-bin",
          "visible": true
        }
      },
      {
        "id": "place:belt",
        "label": "安装 belt",
        "requires": [
          "present:floor"
        ],
        "forbids": [
          "present:belt"
        ],
        "adds": [
          "present:belt"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "belt",
          "visible": true
        }
      },
      {
        "id": "place:left-bin",
        "label": "安装 left-bin",
        "requires": [
          "present:floor"
        ],
        "forbids": [
          "present:left-bin"
        ],
        "adds": [
          "present:left-bin"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "left-bin",
          "visible": true
        }
      },
      {
        "id": "place:floor",
        "label": "安装 floor",
        "requires": [],
        "forbids": [
          "present:floor"
        ],
        "adds": [
          "present:floor"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "floor",
          "visible": true
        }
      },
      {
        "id": "place:diverter-gate",
        "label": "安装 diverter-gate",
        "requires": [
          "present:belt"
        ],
        "forbids": [
          "present:diverter-gate"
        ],
        "adds": [
          "present:diverter-gate"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "diverter-gate",
          "visible": true
        }
      },
      {
        "id": "place:scanner",
        "label": "安装 scanner",
        "requires": [
          "present:floor"
        ],
        "forbids": [
          "present:scanner"
        ],
        "adds": [
          "present:scanner"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "scanner",
          "visible": true
        }
      }
    ],
    "goalFacts": [
      "present:floor",
      "present:belt",
      "present:scanner",
      "present:left-bin",
      "present:right-bin",
      "present:diverter-gate"
    ],
    "budget": 6,
    "semantics": "requires must hold; forbids must be absent; effects apply in order; unit action cost"
  },
  "answer": {
    "actionIds": [
      "place:floor",
      "place:right-bin",
      "place:belt",
      "place:left-bin",
      "place:diverter-gate",
      "place:scanner"
    ]
  }
}
```

### 依赖拆解（h3-warehouse-sorter-disassembly）

提交 actionIds。执行公开前置条件与效果，达到所有目标且不超过预算；允许交换独立动作。

能力：依赖拆解；形式：actions；证据：state-machine。


```json
{
  "input": {
    "initialFacts": [
      "present:floor",
      "present:belt",
      "present:diverter-gate",
      "present:scanner",
      "present:left-bin",
      "present:right-bin"
    ],
    "initialModules": [
      "floor",
      "belt",
      "diverter-gate",
      "scanner",
      "left-bin",
      "right-bin"
    ],
    "actions": [
      {
        "id": "remove:left-bin",
        "label": "拆除 left-bin",
        "requires": [
          "present:left-bin"
        ],
        "forbids": [],
        "adds": [
          "removed:left-bin"
        ],
        "deletes": [
          "present:left-bin"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "left-bin",
          "visible": false
        }
      },
      {
        "id": "remove:scanner",
        "label": "拆除 scanner",
        "requires": [
          "present:scanner"
        ],
        "forbids": [],
        "adds": [
          "removed:scanner"
        ],
        "deletes": [
          "present:scanner"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "scanner",
          "visible": false
        }
      },
      {
        "id": "remove:right-bin",
        "label": "拆除 right-bin",
        "requires": [
          "present:right-bin"
        ],
        "forbids": [],
        "adds": [
          "removed:right-bin"
        ],
        "deletes": [
          "present:right-bin"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "right-bin",
          "visible": false
        }
      },
      {
        "id": "remove:diverter-gate",
        "label": "拆除 diverter-gate",
        "requires": [
          "present:diverter-gate"
        ],
        "forbids": [],
        "adds": [
          "removed:diverter-gate"
        ],
        "deletes": [
          "present:diverter-gate"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "diverter-gate",
          "visible": false
        }
      },
      {
        "id": "remove:floor",
        "label": "拆除 floor",
        "requires": [
          "present:floor"
        ],
        "forbids": [
          "present:belt",
          "present:scanner",
          "present:left-bin",
          "present:right-bin"
        ],
        "adds": [
          "removed:floor"
        ],
        "deletes": [
          "present:floor"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "floor",
          "visible": false
        }
      },
      {
        "id": "remove:belt",
        "label": "拆除 belt",
        "requires": [
          "present:belt"
        ],
        "forbids": [
          "present:diverter-gate"
        ],
        "adds": [
          "removed:belt"
        ],
        "deletes": [
          "present:belt"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "belt",
          "visible": false
        }
      }
    ],
    "goalFacts": [
      "removed:diverter-gate",
      "removed:right-bin",
      "removed:left-bin",
      "removed:scanner",
      "removed:belt",
      "removed:floor"
    ],
    "budget": 6,
    "semantics": "requires must hold; forbids must be absent; effects apply in order; unit action cost"
  },
  "answer": {
    "actionIds": [
      "remove:left-bin",
      "remove:scanner",
      "remove:right-bin",
      "remove:diverter-gate",
      "remove:belt",
      "remove:floor"
    ]
  }
}
```

### 承载维修（h3-warehouse-sorter-service-repair）

提交 actionIds。执行公开前置条件与效果，达到所有目标且不超过预算；允许交换独立动作。

能力：承载维修；形式：actions；证据：state-machine。


```json
{
  "input": {
    "initialFacts": [
      "fault:diverter-gate",
      "closed:diverter-gate"
    ],
    "initialModules": [
      "floor",
      "belt",
      "diverter-gate",
      "scanner",
      "left-bin",
      "right-bin"
    ],
    "actions": [
      {
        "id": "replace:diverter-gate",
        "label": "replace diverter-gate",
        "requires": [
          "done:remove:diverter-gate"
        ],
        "forbids": [
          "done:replace:diverter-gate"
        ],
        "adds": [
          "done:replace:diverter-gate"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "diverter-gate",
          "visible": true
        }
      },
      {
        "id": "release:diverter-gate",
        "label": "release diverter-gate",
        "requires": [
          "done:close:diverter-gate"
        ],
        "forbids": [
          "done:release:diverter-gate"
        ],
        "adds": [
          "done:release:diverter-gate",
          "repaired:diverter-gate"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "diverter-gate"
        }
      },
      {
        "id": "support:diverter-gate",
        "label": "support diverter-gate",
        "requires": [
          "fault:diverter-gate"
        ],
        "forbids": [
          "done:support:diverter-gate"
        ],
        "adds": [
          "done:support:diverter-gate"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "diverter-gate"
        }
      },
      {
        "id": "verify:diverter-gate",
        "label": "verify diverter-gate",
        "requires": [
          "done:replace:diverter-gate"
        ],
        "forbids": [
          "done:verify:diverter-gate"
        ],
        "adds": [
          "done:verify:diverter-gate"
        ],
        "deletes": [
          "fault:diverter-gate"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "diverter-gate"
        }
      },
      {
        "id": "remove:diverter-gate",
        "label": "remove diverter-gate",
        "requires": [
          "done:open:diverter-gate"
        ],
        "forbids": [
          "done:remove:diverter-gate"
        ],
        "adds": [
          "done:remove:diverter-gate"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "diverter-gate",
          "visible": false
        }
      },
      {
        "id": "open:diverter-gate",
        "label": "open diverter-gate",
        "requires": [
          "done:support:diverter-gate"
        ],
        "forbids": [
          "done:open:diverter-gate"
        ],
        "adds": [
          "done:open:diverter-gate"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "diverter-gate"
        }
      },
      {
        "id": "close:diverter-gate",
        "label": "close diverter-gate",
        "requires": [
          "done:verify:diverter-gate"
        ],
        "forbids": [
          "done:close:diverter-gate"
        ],
        "adds": [
          "done:close:diverter-gate"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "diverter-gate"
        }
      }
    ],
    "goalFacts": [
      "repaired:diverter-gate"
    ],
    "budget": 7,
    "semantics": "requires must hold; forbids must be absent; effects apply in order; unit action cost"
  },
  "answer": {
    "actionIds": [
      "support:diverter-gate",
      "open:diverter-gate",
      "remove:diverter-gate",
      "replace:diverter-gate",
      "verify:diverter-gate",
      "close:diverter-gate",
      "release:diverter-gate"
    ]
  }
}
```

### 复合编辑验证（h3-warehouse-sorter-compound-edit）

提交 actionIds。执行公开前置条件与效果，达到所有目标且不超过预算；允许交换独立动作。

能力：复合编辑验证；形式：actions；证据：state-machine。


```json
{
  "input": {
    "initialFacts": [
      "fault:diverter-gate",
      "closed:diverter-gate"
    ],
    "initialModules": [
      "floor",
      "belt",
      "diverter-gate",
      "scanner",
      "left-bin",
      "right-bin"
    ],
    "actions": [
      {
        "id": "release:diverter-gate",
        "label": "release diverter-gate",
        "requires": [
          "done:close:diverter-gate"
        ],
        "forbids": [
          "done:release:diverter-gate"
        ],
        "adds": [
          "done:release:diverter-gate",
          "repaired:diverter-gate"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "diverter-gate"
        }
      },
      {
        "id": "support:diverter-gate",
        "label": "support diverter-gate",
        "requires": [
          "fault:diverter-gate"
        ],
        "forbids": [
          "done:support:diverter-gate"
        ],
        "adds": [
          "done:support:diverter-gate"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "diverter-gate"
        }
      },
      {
        "id": "verify:diverter-gate",
        "label": "verify diverter-gate",
        "requires": [
          "done:recolor:diverter-gate"
        ],
        "forbids": [
          "done:verify:diverter-gate"
        ],
        "adds": [
          "done:verify:diverter-gate"
        ],
        "deletes": [
          "fault:diverter-gate"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "diverter-gate"
        }
      },
      {
        "id": "open:diverter-gate",
        "label": "open diverter-gate",
        "requires": [
          "done:support:diverter-gate"
        ],
        "forbids": [
          "done:open:diverter-gate"
        ],
        "adds": [
          "done:open:diverter-gate"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "diverter-gate"
        }
      },
      {
        "id": "close:diverter-gate",
        "label": "close diverter-gate",
        "requires": [
          "done:verify:diverter-gate"
        ],
        "forbids": [
          "done:close:diverter-gate"
        ],
        "adds": [
          "done:close:diverter-gate"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "diverter-gate"
        }
      },
      {
        "id": "recolor:diverter-gate",
        "label": "recolor diverter-gate",
        "requires": [
          "done:open:diverter-gate"
        ],
        "forbids": [
          "done:recolor:diverter-gate"
        ],
        "adds": [
          "done:recolor:diverter-gate"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "diverter-gate",
          "color": "#ea7635"
        }
      }
    ],
    "goalFacts": [
      "repaired:diverter-gate"
    ],
    "budget": 6,
    "semantics": "requires must hold; forbids must be absent; effects apply in order; unit action cost"
  },
  "answer": {
    "actionIds": [
      "support:diverter-gate",
      "open:diverter-gate",
      "recolor:diverter-gate",
      "verify:diverter-gate",
      "close:diverter-gate",
      "release:diverter-gate"
    ]
  }
}
```

### 跨区域联合维修（h3-warehouse-sorter-multi-fault）

提交 actionIds。执行公开前置条件与效果，达到所有目标且不超过预算；允许交换独立动作。

能力：跨区域联合维修；形式：actions；证据：state-machine。


```json
{
  "input": {
    "initialFacts": [
      "fault:left-bin",
      "closed:left-bin",
      "fault:right-bin",
      "closed:right-bin"
    ],
    "initialModules": [
      "floor",
      "belt",
      "diverter-gate",
      "scanner",
      "left-bin",
      "right-bin"
    ],
    "actions": [
      {
        "id": "release:right-bin",
        "label": "release right-bin",
        "requires": [
          "done:close:right-bin"
        ],
        "forbids": [
          "done:release:right-bin"
        ],
        "adds": [
          "done:release:right-bin",
          "repaired:right-bin"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "right-bin"
        }
      },
      {
        "id": "close:right-bin",
        "label": "close right-bin",
        "requires": [
          "done:verify:right-bin"
        ],
        "forbids": [
          "done:close:right-bin"
        ],
        "adds": [
          "done:close:right-bin"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "right-bin"
        }
      },
      {
        "id": "open:left-bin",
        "label": "open left-bin",
        "requires": [
          "done:support:left-bin"
        ],
        "forbids": [
          "done:open:left-bin"
        ],
        "adds": [
          "done:open:left-bin"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "left-bin"
        }
      },
      {
        "id": "remove:left-bin",
        "label": "remove left-bin",
        "requires": [
          "done:open:left-bin"
        ],
        "forbids": [
          "done:remove:left-bin"
        ],
        "adds": [
          "done:remove:left-bin"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "left-bin",
          "visible": false
        }
      },
      {
        "id": "verify:right-bin",
        "label": "verify right-bin",
        "requires": [
          "done:replace:right-bin"
        ],
        "forbids": [
          "done:verify:right-bin"
        ],
        "adds": [
          "done:verify:right-bin"
        ],
        "deletes": [
          "fault:right-bin"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "right-bin"
        }
      },
      {
        "id": "remove:right-bin",
        "label": "remove right-bin",
        "requires": [
          "done:open:right-bin"
        ],
        "forbids": [
          "done:remove:right-bin"
        ],
        "adds": [
          "done:remove:right-bin"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "right-bin",
          "visible": false
        }
      },
      {
        "id": "support:left-bin",
        "label": "support left-bin",
        "requires": [
          "fault:left-bin"
        ],
        "forbids": [
          "done:support:left-bin"
        ],
        "adds": [
          "done:support:left-bin"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "left-bin"
        }
      },
      {
        "id": "replace:right-bin",
        "label": "replace right-bin",
        "requires": [
          "done:remove:right-bin"
        ],
        "forbids": [
          "done:replace:right-bin"
        ],
        "adds": [
          "done:replace:right-bin"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "right-bin",
          "visible": true
        }
      },
      {
        "id": "verify:left-bin",
        "label": "verify left-bin",
        "requires": [
          "done:replace:left-bin"
        ],
        "forbids": [
          "done:verify:left-bin"
        ],
        "adds": [
          "done:verify:left-bin"
        ],
        "deletes": [
          "fault:left-bin"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "left-bin"
        }
      },
      {
        "id": "support:right-bin",
        "label": "support right-bin",
        "requires": [
          "fault:right-bin"
        ],
        "forbids": [
          "done:support:right-bin"
        ],
        "adds": [
          "done:support:right-bin"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "right-bin"
        }
      },
      {
        "id": "close:left-bin",
        "label": "close left-bin",
        "requires": [
          "done:verify:left-bin"
        ],
        "forbids": [
          "done:close:left-bin"
        ],
        "adds": [
          "done:close:left-bin"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "left-bin"
        }
      },
      {
        "id": "release:left-bin",
        "label": "release left-bin",
        "requires": [
          "done:close:left-bin"
        ],
        "forbids": [
          "done:release:left-bin"
        ],
        "adds": [
          "done:release:left-bin",
          "repaired:left-bin"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "left-bin"
        }
      },
      {
        "id": "replace:left-bin",
        "label": "replace left-bin",
        "requires": [
          "done:remove:left-bin"
        ],
        "forbids": [
          "done:replace:left-bin"
        ],
        "adds": [
          "done:replace:left-bin"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "left-bin",
          "visible": true
        }
      },
      {
        "id": "open:right-bin",
        "label": "open right-bin",
        "requires": [
          "done:support:right-bin"
        ],
        "forbids": [
          "done:open:right-bin"
        ],
        "adds": [
          "done:open:right-bin"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "right-bin"
        }
      }
    ],
    "goalFacts": [
      "repaired:left-bin",
      "repaired:right-bin"
    ],
    "budget": 14,
    "semantics": "requires must hold; forbids must be absent; effects apply in order; unit action cost"
  },
  "answer": {
    "actionIds": [
      "support:left-bin",
      "open:left-bin",
      "remove:left-bin",
      "support:right-bin",
      "replace:left-bin",
      "verify:left-bin",
      "close:left-bin",
      "release:left-bin",
      "open:right-bin",
      "remove:right-bin",
      "replace:right-bin",
      "verify:right-bin",
      "close:right-bin",
      "release:right-bin"
    ]
  }
}
```

### 多工位资源调度（h3-warehouse-sorter-scheduling）

为所有工单提交整数 starts，满足先后关系、独占工位及截止时间。

能力：多工位资源调度；形式：schedule；证据：resource-schedule。


```json
{
  "input": {
    "jobs": [
      {
        "id": "job-0",
        "module": "floor",
        "duration": 3,
        "resource": "test-bench",
        "after": []
      },
      {
        "id": "job-1",
        "module": "belt",
        "duration": 2,
        "resource": "technician",
        "after": []
      },
      {
        "id": "job-2",
        "module": "diverter-gate",
        "duration": 1,
        "resource": "test-bench",
        "after": [
          "job-0"
        ]
      },
      {
        "id": "job-3",
        "module": "scanner",
        "duration": 3,
        "resource": "technician",
        "after": [
          "job-1"
        ]
      },
      {
        "id": "job-4",
        "module": "left-bin",
        "duration": 2,
        "resource": "test-bench",
        "after": [
          "job-2"
        ]
      },
      {
        "id": "job-5",
        "module": "right-bin",
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
      "job-3": 2,
      "job-4": 4,
      "job-5": 5
    }
  }
}
```

### 检查后条件策略（h3-warehouse-sorter-policy）

提交一个检查及 observation→action 决策表，在所有相容世界中采取正确动作。

能力：检查后条件策略；形式：policy；证据：finite-world。


```json
{
  "input": {
    "module": "diverter-gate",
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

### 局部坐标变换（h3-warehouse-sorter-local-frame）

将模块局部点通过给定四元数与平移转换为世界点，保留五位小数。

能力：局部坐标变换；形式：single-choice；证据：model-state。

- A：[-0.375,0,0]
- B：[1,1.25,0]
- C：[2.75,2.25,1]
- D：[1.75,1.25,0]

```json
{
  "input": {
    "localPoint": [
      -0.375,
      0,
      0
    ],
    "rotationXYZW": [
      0,
      1,
      0,
      6.123233995736766e-17
    ],
    "translation": [
      1.375,
      1.25,
      0
    ]
  },
  "answer": {
    "choiceId": "D"
  }
}
```

### 正交视图投影（h3-warehouse-sorter-projection）

按公开视图坐标约定，选择该世界点投影后的二维坐标。

能力：正交视图投影；形式：single-choice；证据：model-state。

- A：[3,-4]
- B：[7,3]
- C：[3,4]
- D：[0,0]

```json
{
  "input": {
    "view": "top",
    "point": [
      3,
      7,
      -4
    ],
    "convention": "front=(x,y), side=(z,y), top=(x,z)"
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 空间相对关系（h3-warehouse-sorter-relative-order）

比较B相对A在指定世界轴上的模块原点坐标。

能力：空间相对关系；形式：single-choice；证据：model-state。

- A：less
- B：equal
- C：greater

```json
{
  "input": {
    "A": {
      "id": "floor",
      "position": [
        0,
        0.2,
        0
      ]
    },
    "B": {
      "id": "right-bin",
      "position": [
        3,
        0.75,
        3
      ]
    },
    "axis": "z"
  },
  "answer": {
    "choiceId": "C"
  }
}
```

### 约束自由度（h3-warehouse-sorter-joint-axis）

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
      "id": "scanner-frame",
      "name": "scanner frame",
      "type": "fixed",
      "parent": "floor",
      "child": "scanner",
      "anchorParent": [
        0,
        0.3,
        -1.7
      ],
      "anchorChild": [
        0,
        -1.525,
        -0.125
      ],
      "axis": [
        0,
        1,
        0
      ]
    }
  },
  "answer": {
    "choiceId": "C"
  }
}
```

### 维修间隙预算（h3-warehouse-sorter-clearance-margin）

给定理想直槽净宽、工具宽度、单侧安全余量，工具是否满足横向间隙要求？

能力：维修间隙预算；形式：single-choice；证据：model-state。

- A：blocked
- B：feasible

```json
{
  "input": {
    "module": "diverter-gate",
    "aperture": 0.6,
    "toolWidth": 0.45,
    "eachSideMargin": 0.1
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 载荷力矩（h3-warehouse-sorter-load-moment）

绕给定原点的载荷力矩r×F是多少？采用右手系，忽略其他力。

能力：载荷力矩；形式：single-choice；证据：model-state。

- A：[0,0,0]
- B：[0,-2,0]
- C：[0,0,-8]
- D：[0,0,8]

```json
{
  "input": {
    "module": "diverter-gate",
    "lever": [
      2,
      3,
      0
    ],
    "force": [
      0,
      -4,
      0
    ],
    "units": "scene-length × force"
  },
  "answer": {
    "choiceId": "C"
  }
}
```

### 非均匀先验更新（h3-warehouse-sorter-weighted-posterior）

先验权重未归一化，观测只保留normal和jammed，求jammed后验概率。

能力：非均匀先验更新；形式：single-choice；证据：finite-world。

- A：0.4
- B：0.25
- C：0
- D：1

```json
{
  "input": {
    "module": "diverter-gate",
    "worlds": [
      "normal",
      "jammed",
      "loose"
    ],
    "weights": [
      3,
      2,
      3
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

### 风险最小决策（h3-warehouse-sorter-expected-loss）

继续运行期望损失=p×failureLoss，预防维修损失=repairCost，选择损失较低者；并列选继续。

能力：风险最小决策；形式：single-choice；证据：finite-world。

- A：repair
- B：continue

```json
{
  "input": {
    "faultProbability": 0.3,
    "repairCost": 1,
    "failureLoss": 10,
    "module": "diverter-gate"
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 轨迹阈值判定（h3-warehouse-sorter-trace-threshold）

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
        "displacement": 0.005004967373182012
      },
      {
        "time": 0.10833333333333334,
        "displacement": 0.000043112922369914486
      },
      {
        "time": 0.20833333333333334,
        "displacement": 0.000002574475004735177
      },
      {
        "time": 0.30833333333333335,
        "displacement": 0.0000025744731857457737
      },
      {
        "time": 0.4083333333333333,
        "displacement": 0.0000025744213445477726
      },
      {
        "time": 0.5083333333333333,
        "displacement": 0.000002573769009472926
      },
      {
        "time": 0.6083333333333333,
        "displacement": 0.0000025734645561215075
      },
      {
        "time": 0.7083333333333334,
        "displacement": 0.0000025734645561215075
      },
      {
        "time": 0.8083333333333333,
        "displacement": 0.0000025734645561215075
      },
      {
        "time": 0.9083333333333333,
        "displacement": 0.0000025734645561215075
      },
      {
        "time": 1,
        "displacement": 0.0000025734645561215075
      }
    ],
    "threshold": 0.0040039738985456095
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 安全联锁维修（h3-warehouse-sorter-guarded-repair）

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
        "id": "release:diverter-gate",
        "label": "release diverter-gate",
        "requires": [
          "done:relock:diverter-gate"
        ],
        "forbids": [
          "done:release:diverter-gate"
        ],
        "adds": [
          "done:release:diverter-gate",
          "ready:diverter-gate",
          "tool:free"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "diverter-gate"
        }
      },
      {
        "id": "relock:diverter-gate",
        "label": "relock diverter-gate",
        "requires": [
          "done:verify:diverter-gate"
        ],
        "forbids": [
          "done:relock:diverter-gate"
        ],
        "adds": [
          "done:relock:diverter-gate"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "diverter-gate"
        }
      },
      {
        "id": "verify:diverter-gate",
        "label": "verify diverter-gate",
        "requires": [
          "done:replace:diverter-gate"
        ],
        "forbids": [
          "done:verify:diverter-gate"
        ],
        "adds": [
          "done:verify:diverter-gate"
        ],
        "deletes": [
          "fault:diverter-gate",
          "misaligned:diverter-gate"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "diverter-gate"
        }
      },
      {
        "id": "replace:diverter-gate",
        "label": "replace diverter-gate",
        "requires": [
          "done:unlock:diverter-gate"
        ],
        "forbids": [
          "done:replace:diverter-gate"
        ],
        "adds": [
          "done:replace:diverter-gate"
        ],
        "deletes": [],
        "cost": 2,
        "visual": {
          "moduleId": "diverter-gate"
        }
      },
      {
        "id": "unlock:diverter-gate",
        "label": "unlock diverter-gate",
        "requires": [
          "done:support:diverter-gate"
        ],
        "forbids": [
          "done:unlock:diverter-gate"
        ],
        "adds": [
          "done:unlock:diverter-gate"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "diverter-gate"
        }
      },
      {
        "id": "support:diverter-gate",
        "label": "support diverter-gate",
        "requires": [
          "done:isolate:diverter-gate"
        ],
        "forbids": [
          "done:support:diverter-gate"
        ],
        "adds": [
          "done:support:diverter-gate"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "diverter-gate"
        }
      },
      {
        "id": "isolate:diverter-gate",
        "label": "isolate diverter-gate",
        "requires": [
          "tool:free",
          "fault:diverter-gate"
        ],
        "forbids": [
          "done:isolate:diverter-gate"
        ],
        "adds": [
          "done:isolate:diverter-gate"
        ],
        "deletes": [
          "tool:free"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "diverter-gate"
        }
      }
    ],
    "initialFacts": [
      "tool:free",
      "fault:diverter-gate"
    ],
    "initialModules": [
      "floor",
      "belt",
      "diverter-gate",
      "scanner",
      "left-bin",
      "right-bin"
    ],
    "goalFacts": [
      "ready:diverter-gate"
    ],
    "absentFacts": [
      "unverified"
    ],
    "budget": 8
  },
  "answer": {
    "actionIds": [
      "isolate:diverter-gate",
      "support:diverter-gate",
      "unlock:diverter-gate",
      "replace:diverter-gate",
      "verify:diverter-gate",
      "relock:diverter-gate",
      "release:diverter-gate"
    ]
  }
}
```

### 失败状态回退（h3-warehouse-sorter-rollback）

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
        "id": "resume:diverter-gate",
        "label": "resume diverter-gate",
        "requires": [
          "done:verify:diverter-gate"
        ],
        "forbids": [
          "done:resume:diverter-gate"
        ],
        "adds": [
          "done:resume:diverter-gate",
          "ready:diverter-gate",
          "tool:free"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "diverter-gate"
        }
      },
      {
        "id": "verify:diverter-gate",
        "label": "verify diverter-gate",
        "requires": [
          "done:align:diverter-gate"
        ],
        "forbids": [
          "done:verify:diverter-gate"
        ],
        "adds": [
          "done:verify:diverter-gate"
        ],
        "deletes": [
          "fault:diverter-gate",
          "misaligned:diverter-gate"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "diverter-gate"
        }
      },
      {
        "id": "align:diverter-gate",
        "label": "align diverter-gate",
        "requires": [
          "done:undo:diverter-gate"
        ],
        "forbids": [
          "done:align:diverter-gate"
        ],
        "adds": [
          "done:align:diverter-gate"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "diverter-gate",
          "visible": true
        }
      },
      {
        "id": "undo:diverter-gate",
        "label": "undo diverter-gate",
        "requires": [
          "done:isolate:diverter-gate"
        ],
        "forbids": [
          "done:undo:diverter-gate"
        ],
        "adds": [
          "done:undo:diverter-gate"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "diverter-gate",
          "visible": false
        }
      },
      {
        "id": "isolate:diverter-gate",
        "label": "isolate diverter-gate",
        "requires": [
          "tool:free",
          "fault:diverter-gate"
        ],
        "forbids": [
          "done:isolate:diverter-gate"
        ],
        "adds": [
          "done:isolate:diverter-gate"
        ],
        "deletes": [
          "tool:free"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "diverter-gate"
        }
      }
    ],
    "initialFacts": [
      "tool:free",
      "fault:diverter-gate",
      "misaligned:diverter-gate"
    ],
    "initialModules": [
      "floor",
      "belt",
      "diverter-gate",
      "scanner",
      "left-bin",
      "right-bin"
    ],
    "goalFacts": [
      "ready:diverter-gate"
    ],
    "absentFacts": [
      "unverified"
    ],
    "budget": 5
  },
  "answer": {
    "actionIds": [
      "isolate:diverter-gate",
      "undo:diverter-gate",
      "align:diverter-gate",
      "verify:diverter-gate",
      "resume:diverter-gate"
    ]
  }
}
```

### 共享工具协同维修（h3-warehouse-sorter-resource-repair）

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
        "id": "release:right-bin",
        "label": "release right-bin",
        "requires": [
          "done:relock:right-bin"
        ],
        "forbids": [
          "done:release:right-bin"
        ],
        "adds": [
          "done:release:right-bin",
          "ready:right-bin",
          "tool:free"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "right-bin"
        }
      },
      {
        "id": "relock:right-bin",
        "label": "relock right-bin",
        "requires": [
          "done:verify:right-bin"
        ],
        "forbids": [
          "done:relock:right-bin"
        ],
        "adds": [
          "done:relock:right-bin"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "right-bin"
        }
      },
      {
        "id": "verify:right-bin",
        "label": "verify right-bin",
        "requires": [
          "done:replace:right-bin"
        ],
        "forbids": [
          "done:verify:right-bin"
        ],
        "adds": [
          "done:verify:right-bin"
        ],
        "deletes": [
          "fault:right-bin",
          "misaligned:right-bin"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "right-bin"
        }
      },
      {
        "id": "replace:right-bin",
        "label": "replace right-bin",
        "requires": [
          "done:unlock:right-bin"
        ],
        "forbids": [
          "done:replace:right-bin"
        ],
        "adds": [
          "done:replace:right-bin"
        ],
        "deletes": [],
        "cost": 2,
        "visual": {
          "moduleId": "right-bin"
        }
      },
      {
        "id": "unlock:right-bin",
        "label": "unlock right-bin",
        "requires": [
          "done:support:right-bin"
        ],
        "forbids": [
          "done:unlock:right-bin"
        ],
        "adds": [
          "done:unlock:right-bin"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "right-bin"
        }
      },
      {
        "id": "support:right-bin",
        "label": "support right-bin",
        "requires": [
          "done:isolate:right-bin"
        ],
        "forbids": [
          "done:support:right-bin"
        ],
        "adds": [
          "done:support:right-bin"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "right-bin"
        }
      },
      {
        "id": "isolate:right-bin",
        "label": "isolate right-bin",
        "requires": [
          "tool:free",
          "fault:right-bin"
        ],
        "forbids": [
          "done:isolate:right-bin"
        ],
        "adds": [
          "done:isolate:right-bin"
        ],
        "deletes": [
          "tool:free"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "right-bin"
        }
      },
      {
        "id": "release:left-bin",
        "label": "release left-bin",
        "requires": [
          "done:relock:left-bin"
        ],
        "forbids": [
          "done:release:left-bin"
        ],
        "adds": [
          "done:release:left-bin",
          "ready:left-bin",
          "tool:free"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "left-bin"
        }
      },
      {
        "id": "relock:left-bin",
        "label": "relock left-bin",
        "requires": [
          "done:verify:left-bin"
        ],
        "forbids": [
          "done:relock:left-bin"
        ],
        "adds": [
          "done:relock:left-bin"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "left-bin"
        }
      },
      {
        "id": "verify:left-bin",
        "label": "verify left-bin",
        "requires": [
          "done:replace:left-bin"
        ],
        "forbids": [
          "done:verify:left-bin"
        ],
        "adds": [
          "done:verify:left-bin"
        ],
        "deletes": [
          "fault:left-bin",
          "misaligned:left-bin"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "left-bin"
        }
      },
      {
        "id": "replace:left-bin",
        "label": "replace left-bin",
        "requires": [
          "done:unlock:left-bin"
        ],
        "forbids": [
          "done:replace:left-bin"
        ],
        "adds": [
          "done:replace:left-bin"
        ],
        "deletes": [],
        "cost": 2,
        "visual": {
          "moduleId": "left-bin"
        }
      },
      {
        "id": "unlock:left-bin",
        "label": "unlock left-bin",
        "requires": [
          "done:support:left-bin"
        ],
        "forbids": [
          "done:unlock:left-bin"
        ],
        "adds": [
          "done:unlock:left-bin"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "left-bin"
        }
      },
      {
        "id": "support:left-bin",
        "label": "support left-bin",
        "requires": [
          "done:isolate:left-bin"
        ],
        "forbids": [
          "done:support:left-bin"
        ],
        "adds": [
          "done:support:left-bin"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "left-bin"
        }
      },
      {
        "id": "isolate:left-bin",
        "label": "isolate left-bin",
        "requires": [
          "tool:free",
          "fault:left-bin"
        ],
        "forbids": [
          "done:isolate:left-bin"
        ],
        "adds": [
          "done:isolate:left-bin"
        ],
        "deletes": [
          "tool:free"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "left-bin"
        }
      },
      {
        "id": "release:scanner",
        "label": "release scanner",
        "requires": [
          "done:relock:scanner"
        ],
        "forbids": [
          "done:release:scanner"
        ],
        "adds": [
          "done:release:scanner",
          "ready:scanner",
          "tool:free"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "scanner"
        }
      },
      {
        "id": "relock:scanner",
        "label": "relock scanner",
        "requires": [
          "done:verify:scanner"
        ],
        "forbids": [
          "done:relock:scanner"
        ],
        "adds": [
          "done:relock:scanner"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "scanner"
        }
      },
      {
        "id": "verify:scanner",
        "label": "verify scanner",
        "requires": [
          "done:replace:scanner"
        ],
        "forbids": [
          "done:verify:scanner"
        ],
        "adds": [
          "done:verify:scanner"
        ],
        "deletes": [
          "fault:scanner",
          "misaligned:scanner"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "scanner"
        }
      },
      {
        "id": "replace:scanner",
        "label": "replace scanner",
        "requires": [
          "done:unlock:scanner"
        ],
        "forbids": [
          "done:replace:scanner"
        ],
        "adds": [
          "done:replace:scanner"
        ],
        "deletes": [],
        "cost": 2,
        "visual": {
          "moduleId": "scanner"
        }
      },
      {
        "id": "unlock:scanner",
        "label": "unlock scanner",
        "requires": [
          "done:support:scanner"
        ],
        "forbids": [
          "done:unlock:scanner"
        ],
        "adds": [
          "done:unlock:scanner"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "scanner"
        }
      },
      {
        "id": "support:scanner",
        "label": "support scanner",
        "requires": [
          "done:isolate:scanner"
        ],
        "forbids": [
          "done:support:scanner"
        ],
        "adds": [
          "done:support:scanner"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "scanner"
        }
      },
      {
        "id": "isolate:scanner",
        "label": "isolate scanner",
        "requires": [
          "tool:free",
          "fault:scanner"
        ],
        "forbids": [
          "done:isolate:scanner"
        ],
        "adds": [
          "done:isolate:scanner"
        ],
        "deletes": [
          "tool:free"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "scanner"
        }
      }
    ],
    "initialFacts": [
      "tool:free",
      "fault:scanner",
      "fault:left-bin",
      "fault:right-bin"
    ],
    "initialModules": [
      "floor",
      "belt",
      "diverter-gate",
      "scanner",
      "left-bin",
      "right-bin"
    ],
    "goalFacts": [
      "ready:scanner",
      "ready:left-bin",
      "ready:right-bin"
    ],
    "absentFacts": [
      "unverified"
    ],
    "budget": 24
  },
  "answer": {
    "actionIds": [
      "isolate:right-bin",
      "support:right-bin",
      "unlock:right-bin",
      "replace:right-bin",
      "verify:right-bin",
      "relock:right-bin",
      "release:right-bin",
      "isolate:left-bin",
      "support:left-bin",
      "unlock:left-bin",
      "replace:left-bin",
      "verify:left-bin",
      "relock:left-bin",
      "release:left-bin",
      "isolate:scanner",
      "support:scanner",
      "unlock:scanner",
      "replace:scanner",
      "verify:scanner",
      "relock:scanner",
      "release:scanner"
    ]
  }
}
```

### 预算约束检查策略（h3-warehouse-sorter-budget-policy）

提交预算内、对所有相容世界均正确的检查决策表。

能力：预算约束检查策略；形式：policy；证据：finite-world。


```json
{
  "input": {
    "module": "diverter-gate",
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
        "cost": 0,
        "returns": {
          "nominal": "pass",
          "fault": "pass"
        }
      },
      {
        "id": "probe",
        "cost": 4,
        "returns": {
          "nominal": "pass",
          "fault": "fail"
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
    "budget": 3
  },
  "answer": {
    "queryId": "thermal",
    "decisions": {
      "pass": "continue",
      "fail": "tighten"
    }
  }
}
```

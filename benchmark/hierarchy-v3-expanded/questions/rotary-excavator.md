## D3 回转斗轮挖掘机

### 模块识别（h3-rotary-excavator-identify）

高亮的维修模块对应哪个 ID？

能力：模块识别；形式：single-choice；证据：model-state。

- A：service-cartridge
- B：foundation
- C：mast
- D：primary-boom

```json
{
  "input": {
    "moduleNames": [
      {
        "id": "foundation",
        "name": "foundation"
      },
      {
        "id": "mast",
        "name": "mast"
      },
      {
        "id": "primary-boom",
        "name": "primary boom"
      },
      {
        "id": "tool-head",
        "name": "tool head"
      },
      {
        "id": "control-cab",
        "name": "control cab"
      },
      {
        "id": "service-cartridge",
        "name": "service cartridge"
      },
      {
        "id": "secondary-boom",
        "name": "secondary boom"
      },
      {
        "id": "clamp",
        "name": "clamp"
      },
      {
        "id": "sliding-tray",
        "name": "sliding tray"
      },
      {
        "id": "track--1",
        "name": "track  1"
      },
      {
        "id": "track-1",
        "name": "track 1"
      }
    ]
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 部件计数（h3-rotary-excavator-count）

模块 service-cartridge 有多少个可视零件？

能力：部件计数；形式：single-choice；证据：model-state。

- A：5
- B：3
- C：7
- D：4

```json
{
  "input": {
    "parts": [
      {
        "id": "foundation-p1",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p2",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p3",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p4",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p5",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p6",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p7",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p8",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p9",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p10",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p11",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p12",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p13",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p14",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p15",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p16",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p17",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p18",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p19",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p20",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p21",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p22",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p23",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p24",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p25",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p26",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p27",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p28",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p29",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "foundation-p30",
        "moduleId": "foundation",
        "shape": "plate",
        "color": "#273e50"
      },
      {
        "id": "mast-p31",
        "moduleId": "mast",
        "shape": "brick",
        "color": "#dfebed"
      },
      {
        "id": "mast-p32",
        "moduleId": "mast",
        "shape": "brick",
        "color": "#dfebed"
      },
      {
        "id": "mast-p33",
        "moduleId": "mast",
        "shape": "brick",
        "color": "#dfebed"
      },
      {
        "id": "mast-p34",
        "moduleId": "mast",
        "shape": "brick",
        "color": "#dfebed"
      },
      {
        "id": "mast-p35",
        "moduleId": "mast",
        "shape": "brick",
        "color": "#dfebed"
      },
      {
        "id": "mast-p36",
        "moduleId": "mast",
        "shape": "brick",
        "color": "#dfebed"
      },
      {
        "id": "mast-p37",
        "moduleId": "mast",
        "shape": "brick",
        "color": "#dfebed"
      },
      {
        "id": "mast-p38",
        "moduleId": "mast",
        "shape": "brick",
        "color": "#dfebed"
      },
      {
        "id": "mast-p39",
        "moduleId": "mast",
        "shape": "brick",
        "color": "#dfebed"
      },
      {
        "id": "mast-p40",
        "moduleId": "mast",
        "shape": "brick",
        "color": "#dfebed"
      },
      {
        "id": "mast-p41",
        "moduleId": "mast",
        "shape": "brick",
        "color": "#dfebed"
      },
      {
        "id": "mast-p42",
        "moduleId": "mast",
        "shape": "brick",
        "color": "#dfebed"
      },
      {
        "id": "mast-p43",
        "moduleId": "mast",
        "shape": "brick",
        "color": "#dfebed"
      },
      {
        "id": "mast-p44",
        "moduleId": "mast",
        "shape": "brick",
        "color": "#dfebed"
      },
      {
        "id": "mast-p45",
        "moduleId": "mast",
        "shape": "brick",
        "color": "#dfebed"
      },
      {
        "id": "mast-p46",
        "moduleId": "mast",
        "shape": "brick",
        "color": "#dfebed"
      },
      {
        "id": "mast-p47",
        "moduleId": "mast",
        "shape": "brick",
        "color": "#dfebed"
      },
      {
        "id": "mast-p48",
        "moduleId": "mast",
        "shape": "brick",
        "color": "#dfebed"
      },
      {
        "id": "mast-p49",
        "moduleId": "mast",
        "shape": "brick",
        "color": "#dfebed"
      },
      {
        "id": "mast-p50",
        "moduleId": "mast",
        "shape": "brick",
        "color": "#dfebed"
      },
      {
        "id": "mast-p51",
        "moduleId": "mast",
        "shape": "brick",
        "color": "#dfebed"
      },
      {
        "id": "mast-p52",
        "moduleId": "mast",
        "shape": "brick",
        "color": "#dfebed"
      },
      {
        "id": "mast-p53",
        "moduleId": "mast",
        "shape": "brick",
        "color": "#dfebed"
      },
      {
        "id": "mast-p54",
        "moduleId": "mast",
        "shape": "brick",
        "color": "#dfebed"
      },
      {
        "id": "mast-p55",
        "moduleId": "mast",
        "shape": "brick",
        "color": "#dfebed"
      },
      {
        "id": "mast-p56",
        "moduleId": "mast",
        "shape": "brick",
        "color": "#dfebed"
      },
      {
        "id": "mast-p57",
        "moduleId": "mast",
        "shape": "brick",
        "color": "#dfebed"
      },
      {
        "id": "mast-p58",
        "moduleId": "mast",
        "shape": "brick",
        "color": "#dfebed"
      },
      {
        "id": "mast-p59",
        "moduleId": "mast",
        "shape": "brick",
        "color": "#dfebed"
      },
      {
        "id": "mast-p60",
        "moduleId": "mast",
        "shape": "brick",
        "color": "#dfebed"
      },
      {
        "id": "mast-p61",
        "moduleId": "mast",
        "shape": "brick",
        "color": "#dfebed"
      },
      {
        "id": "mast-p62",
        "moduleId": "mast",
        "shape": "brick",
        "color": "#dfebed"
      },
      {
        "id": "mast-p63",
        "moduleId": "mast",
        "shape": "brick",
        "color": "#dfebed"
      },
      {
        "id": "mast-p64",
        "moduleId": "mast",
        "shape": "brick",
        "color": "#dfebed"
      },
      {
        "id": "mast-p65",
        "moduleId": "mast",
        "shape": "brick",
        "color": "#dfebed"
      },
      {
        "id": "mast-p66",
        "moduleId": "mast",
        "shape": "brick",
        "color": "#dfebed"
      },
      {
        "id": "mast-p67",
        "moduleId": "mast",
        "shape": "beam",
        "color": "#387bb3"
      },
      {
        "id": "mast-p68",
        "moduleId": "mast",
        "shape": "beam",
        "color": "#387bb3"
      },
      {
        "id": "mast-p69",
        "moduleId": "mast",
        "shape": "beam",
        "color": "#387bb3"
      },
      {
        "id": "primary-boom-p70",
        "moduleId": "primary-boom",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "primary-boom-p71",
        "moduleId": "primary-boom",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "primary-boom-p72",
        "moduleId": "primary-boom",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "primary-boom-p73",
        "moduleId": "primary-boom",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "primary-boom-p74",
        "moduleId": "primary-boom",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "primary-boom-p75",
        "moduleId": "primary-boom",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "primary-boom-p76",
        "moduleId": "primary-boom",
        "shape": "gear",
        "color": "#273e50"
      },
      {
        "id": "tool-head-p77",
        "moduleId": "tool-head",
        "shape": "plate",
        "color": "#dc6040"
      },
      {
        "id": "tool-head-p78",
        "moduleId": "tool-head",
        "shape": "plate",
        "color": "#dc6040"
      },
      {
        "id": "tool-head-p79",
        "moduleId": "tool-head",
        "shape": "plate",
        "color": "#dc6040"
      },
      {
        "id": "tool-head-p80",
        "moduleId": "tool-head",
        "shape": "plate",
        "color": "#dc6040"
      },
      {
        "id": "tool-head-p81",
        "moduleId": "tool-head",
        "shape": "plate",
        "color": "#dc6040"
      },
      {
        "id": "tool-head-p82",
        "moduleId": "tool-head",
        "shape": "plate",
        "color": "#dc6040"
      },
      {
        "id": "tool-head-p83",
        "moduleId": "tool-head",
        "shape": "plate",
        "color": "#dc6040"
      },
      {
        "id": "tool-head-p84",
        "moduleId": "tool-head",
        "shape": "plate",
        "color": "#dc6040"
      },
      {
        "id": "tool-head-p85",
        "moduleId": "tool-head",
        "shape": "plate",
        "color": "#dc6040"
      },
      {
        "id": "tool-head-p86",
        "moduleId": "tool-head",
        "shape": "plate",
        "color": "#dc6040"
      },
      {
        "id": "tool-head-p87",
        "moduleId": "tool-head",
        "shape": "plate",
        "color": "#dc6040"
      },
      {
        "id": "tool-head-p88",
        "moduleId": "tool-head",
        "shape": "plate",
        "color": "#dc6040"
      },
      {
        "id": "tool-head-p89",
        "moduleId": "tool-head",
        "shape": "panel",
        "color": "#dc6040"
      },
      {
        "id": "tool-head-p90",
        "moduleId": "tool-head",
        "shape": "panel",
        "color": "#dc6040"
      },
      {
        "id": "control-cab-p91",
        "moduleId": "control-cab",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "control-cab-p92",
        "moduleId": "control-cab",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "control-cab-p93",
        "moduleId": "control-cab",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "control-cab-p94",
        "moduleId": "control-cab",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "control-cab-p95",
        "moduleId": "control-cab",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "control-cab-p96",
        "moduleId": "control-cab",
        "shape": "plate",
        "color": "#dfebed"
      },
      {
        "id": "control-cab-p97",
        "moduleId": "control-cab",
        "shape": "window",
        "color": "#79c7d8"
      },
      {
        "id": "control-cab-p98",
        "moduleId": "control-cab",
        "shape": "slope",
        "color": "#387bb3"
      },
      {
        "id": "service-cartridge-p99",
        "moduleId": "service-cartridge",
        "shape": "plate",
        "color": "#dc6040"
      },
      {
        "id": "service-cartridge-p100",
        "moduleId": "service-cartridge",
        "shape": "plate",
        "color": "#dc6040"
      },
      {
        "id": "service-cartridge-p101",
        "moduleId": "service-cartridge",
        "shape": "plate",
        "color": "#dc6040"
      },
      {
        "id": "service-cartridge-p102",
        "moduleId": "service-cartridge",
        "shape": "plate",
        "color": "#dc6040"
      },
      {
        "id": "secondary-boom-p103",
        "moduleId": "secondary-boom",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "secondary-boom-p104",
        "moduleId": "secondary-boom",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "secondary-boom-p105",
        "moduleId": "secondary-boom",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "secondary-boom-p106",
        "moduleId": "secondary-boom",
        "shape": "beam",
        "color": "#e9ad37"
      },
      {
        "id": "secondary-boom-p107",
        "moduleId": "secondary-boom",
        "shape": "gear",
        "color": "#273e50"
      },
      {
        "id": "clamp-p108",
        "moduleId": "clamp",
        "shape": "arch",
        "color": "#e9ad37"
      },
      {
        "id": "sliding-tray-p109",
        "moduleId": "sliding-tray",
        "shape": "plate",
        "color": "#45a080"
      },
      {
        "id": "sliding-tray-p110",
        "moduleId": "sliding-tray",
        "shape": "plate",
        "color": "#45a080"
      },
      {
        "id": "sliding-tray-p111",
        "moduleId": "sliding-tray",
        "shape": "plate",
        "color": "#45a080"
      },
      {
        "id": "sliding-tray-p112",
        "moduleId": "sliding-tray",
        "shape": "plate",
        "color": "#45a080"
      },
      {
        "id": "sliding-tray-p113",
        "moduleId": "sliding-tray",
        "shape": "plate",
        "color": "#45a080"
      },
      {
        "id": "sliding-tray-p114",
        "moduleId": "sliding-tray",
        "shape": "plate",
        "color": "#45a080"
      },
      {
        "id": "sliding-tray-p115",
        "moduleId": "sliding-tray",
        "shape": "plate",
        "color": "#45a080"
      },
      {
        "id": "sliding-tray-p116",
        "moduleId": "sliding-tray",
        "shape": "plate",
        "color": "#45a080"
      },
      {
        "id": "track--1-p117",
        "moduleId": "track--1",
        "shape": "wheel",
        "color": "#273e50"
      },
      {
        "id": "track--1-p118",
        "moduleId": "track--1",
        "shape": "wheel",
        "color": "#273e50"
      },
      {
        "id": "track--1-p119",
        "moduleId": "track--1",
        "shape": "wheel",
        "color": "#273e50"
      },
      {
        "id": "track--1-p120",
        "moduleId": "track--1",
        "shape": "beam",
        "color": "#405267"
      },
      {
        "id": "track--1-p121",
        "moduleId": "track--1",
        "shape": "beam",
        "color": "#405267"
      },
      {
        "id": "track--1-p122",
        "moduleId": "track--1",
        "shape": "beam",
        "color": "#405267"
      },
      {
        "id": "track--1-p123",
        "moduleId": "track--1",
        "shape": "beam",
        "color": "#405267"
      },
      {
        "id": "track--1-p124",
        "moduleId": "track--1",
        "shape": "beam",
        "color": "#405267"
      },
      {
        "id": "track--1-p125",
        "moduleId": "track--1",
        "shape": "beam",
        "color": "#405267"
      },
      {
        "id": "track--1-p126",
        "moduleId": "track--1",
        "shape": "beam",
        "color": "#405267"
      },
      {
        "id": "track--1-p127",
        "moduleId": "track--1",
        "shape": "beam",
        "color": "#405267"
      },
      {
        "id": "track--1-p128",
        "moduleId": "track--1",
        "shape": "beam",
        "color": "#405267"
      },
      {
        "id": "track--1-p129",
        "moduleId": "track--1",
        "shape": "beam",
        "color": "#405267"
      },
      {
        "id": "track--1-p130",
        "moduleId": "track--1",
        "shape": "beam",
        "color": "#405267"
      },
      {
        "id": "track--1-p131",
        "moduleId": "track--1",
        "shape": "beam",
        "color": "#405267"
      },
      {
        "id": "track--1-p132",
        "moduleId": "track--1",
        "shape": "beam",
        "color": "#405267"
      },
      {
        "id": "track--1-p133",
        "moduleId": "track--1",
        "shape": "beam",
        "color": "#405267"
      },
      {
        "id": "track--1-p134",
        "moduleId": "track--1",
        "shape": "beam",
        "color": "#405267"
      },
      {
        "id": "track--1-p135",
        "moduleId": "track--1",
        "shape": "beam",
        "color": "#405267"
      },
      {
        "id": "track-1-p136",
        "moduleId": "track-1",
        "shape": "wheel",
        "color": "#273e50"
      },
      {
        "id": "track-1-p137",
        "moduleId": "track-1",
        "shape": "wheel",
        "color": "#273e50"
      },
      {
        "id": "track-1-p138",
        "moduleId": "track-1",
        "shape": "wheel",
        "color": "#273e50"
      },
      {
        "id": "track-1-p139",
        "moduleId": "track-1",
        "shape": "beam",
        "color": "#405267"
      },
      {
        "id": "track-1-p140",
        "moduleId": "track-1",
        "shape": "beam",
        "color": "#405267"
      },
      {
        "id": "track-1-p141",
        "moduleId": "track-1",
        "shape": "beam",
        "color": "#405267"
      },
      {
        "id": "track-1-p142",
        "moduleId": "track-1",
        "shape": "beam",
        "color": "#405267"
      },
      {
        "id": "track-1-p143",
        "moduleId": "track-1",
        "shape": "beam",
        "color": "#405267"
      },
      {
        "id": "track-1-p144",
        "moduleId": "track-1",
        "shape": "beam",
        "color": "#405267"
      },
      {
        "id": "track-1-p145",
        "moduleId": "track-1",
        "shape": "beam",
        "color": "#405267"
      },
      {
        "id": "track-1-p146",
        "moduleId": "track-1",
        "shape": "beam",
        "color": "#405267"
      },
      {
        "id": "track-1-p147",
        "moduleId": "track-1",
        "shape": "beam",
        "color": "#405267"
      },
      {
        "id": "track-1-p148",
        "moduleId": "track-1",
        "shape": "beam",
        "color": "#405267"
      },
      {
        "id": "track-1-p149",
        "moduleId": "track-1",
        "shape": "beam",
        "color": "#405267"
      },
      {
        "id": "track-1-p150",
        "moduleId": "track-1",
        "shape": "beam",
        "color": "#405267"
      },
      {
        "id": "track-1-p151",
        "moduleId": "track-1",
        "shape": "beam",
        "color": "#405267"
      },
      {
        "id": "track-1-p152",
        "moduleId": "track-1",
        "shape": "beam",
        "color": "#405267"
      },
      {
        "id": "track-1-p153",
        "moduleId": "track-1",
        "shape": "beam",
        "color": "#405267"
      },
      {
        "id": "track-1-p154",
        "moduleId": "track-1",
        "shape": "beam",
        "color": "#405267"
      }
    ]
  },
  "answer": {
    "choiceId": "D"
  }
}
```

### 颜色识别（h3-rotary-excavator-color）

零件 service-cartridge-p99 的颜色值是什么？

能力：颜色识别；形式：single-choice；证据：model-state。

- A：#d43a32
- B：#f2bf3c
- C：#dc6040
- D：#2878b8

```json
{
  "input": {
    "part": {
      "id": "service-cartridge-p99",
      "moduleId": "service-cartridge",
      "shape": "plate",
      "position": [
        -0.5,
        -0.04999999999999999,
        -0.5
      ],
      "size": [
        0.98,
        0.28,
        0.98
      ],
      "color": "#dc6040",
      "rotation": [
        0,
        0,
        0,
        1
      ]
    }
  },
  "answer": {
    "choiceId": "C"
  }
}
```

### 三维位置（h3-rotary-excavator-position）

模块 service-cartridge 的世界包围盒中心是什么？

能力：三维位置；形式：single-choice；证据：model-state。

- A：[0.6463835548391195,7.915559217208118,-0.6]
- B：[2,0.8500000000000001,-2]
- C：[0,0.35,0]
- D：[-1.6,3.3499999999999996,-0.6000000000000001]

```json
{
  "input": {
    "centers": {
      "foundation": [
        0,
        0.35,
        0
      ],
      "mast": [
        -1.6,
        3.3499999999999996,
        -0.6000000000000001
      ],
      "primary-boom": [
        0.6463835548391195,
        7.915559217208118,
        -0.6
      ],
      "tool-head": [
        3.176502791294336,
        10.361118434416237,
        1.4
      ],
      "control-cab": [
        2,
        2.1550000000000002,
        1.7999999999999998
      ],
      "service-cartridge": [
        2,
        0.8500000000000001,
        -2
      ],
      "secondary-boom": [
        2.072131002778001,
        3.7912592304699557,
        4
      ],
      "clamp": [
        1.1354126538114302,
        5.637189707302727,
        4.8
      ],
      "sliding-tray": [
        0,
        1.85,
        3.9000000000000004
      ],
      "track--1": [
        -0.050000000000000266,
        0.7,
        -4
      ],
      "track-1": [
        -0.050000000000000266,
        0.7,
        4
      ]
    }
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 关节类型（h3-rotary-excavator-joint-type）

primary-boom-joint 采用什么约束类型？

能力：关节类型；形式：single-choice；证据：model-state。

- A：prismatic
- B：spring
- C：revolute
- D：fixed

```json
{
  "input": {
    "joint": {
      "id": "primary-boom-joint",
      "name": "primary-boom interface",
      "parent": "mast",
      "child": "primary-boom",
      "type": "revolute",
      "anchorParent": [
        0,
        2.75,
        0
      ],
      "anchorChild": [
        -2.24638355483912,
        -1.8155592172081185,
        0
      ],
      "axis": [
        0,
        0,
        1
      ],
      "limits": [
        -0.8,
        0.8
      ]
    }
  },
  "answer": {
    "choiceId": "C"
  }
}
```

### 直接连接（h3-rotary-excavator-parent）

service-cartridge 的直接父模块集合是什么？

能力：直接连接；形式：single-choice；证据：model-state。

- A：["foundation","mast","primary-boom","tool-head","control-cab","service-cartridge","secondary-boom","clamp","sliding-tray","track--1","track-1"]
- B：["foundation"]
- C：["service-cartridge"]
- D：[]

```json
{
  "input": {
    "joints": [
      {
        "id": "mast-joint",
        "name": "mast interface",
        "parent": "foundation",
        "child": "mast",
        "type": "fixed",
        "anchorParent": [
          -1.6,
          0.55,
          -0.6
        ],
        "anchorChild": [
          0,
          -2.45,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "primary-boom-joint",
        "name": "primary-boom interface",
        "parent": "mast",
        "child": "primary-boom",
        "type": "revolute",
        "anchorParent": [
          0,
          2.75,
          0
        ],
        "anchorChild": [
          -2.24638355483912,
          -1.8155592172081185,
          0
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          -0.8,
          0.8
        ]
      },
      {
        "id": "tool-head-joint",
        "name": "tool-head interface",
        "parent": "primary-boom",
        "child": "tool-head",
        "type": "revolute",
        "anchorParent": [
          2.530119236455216,
          1.8155592172081194,
          2
        ],
        "anchorChild": [
          0,
          -0.6299999999999999,
          0
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          -0.8,
          0.8
        ]
      },
      {
        "id": "control-cab-joint",
        "name": "control-cab interface",
        "parent": "foundation",
        "child": "control-cab",
        "type": "fixed",
        "anchorParent": [
          2,
          0.8499999999999999,
          1.8
        ],
        "anchorChild": [
          0,
          -0.9549999999999998,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "service-cartridge-joint",
        "name": "service-cartridge interface",
        "parent": "foundation",
        "child": "service-cartridge",
        "type": "fixed",
        "anchorParent": [
          2,
          0.45,
          -2
        ],
        "anchorChild": [
          0,
          -0.04999999999999999,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "secondary-boom-joint",
        "name": "secondary-boom interface",
        "parent": "control-cab",
        "child": "secondary-boom",
        "type": "revolute",
        "anchorParent": [
          0.7999999999999998,
          -0.1549999999999998,
          2.2
        ],
        "anchorChild": [
          0.7278689972219987,
          -1.7912592304699564,
          0
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          -0.8,
          0.8
        ]
      },
      {
        "id": "clamp-joint",
        "name": "clamp interface",
        "parent": "secondary-boom",
        "child": "clamp",
        "type": "revolute",
        "anchorParent": [
          -0.9367183489665709,
          1.8459304768327705,
          0.7999999999999998
        ],
        "anchorChild": [
          0,
          0,
          0
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          -0.8,
          0.8
        ]
      },
      {
        "id": "sliding-tray-joint",
        "name": "sliding-tray interface",
        "parent": "foundation",
        "child": "sliding-tray",
        "type": "prismatic",
        "anchorParent": [
          0,
          1.45,
          3.9
        ],
        "anchorChild": [
          0,
          -0.04999999999999999,
          0
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          -0.8,
          0.8
        ]
      },
      {
        "id": "track--1-joint",
        "name": "track--1 interface",
        "parent": "foundation",
        "child": "track--1",
        "type": "revolute",
        "anchorParent": [
          0,
          0.25,
          -4
        ],
        "anchorChild": [
          0.050000000000000266,
          -0.10000000000000003,
          0
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          -0.8,
          0.8
        ]
      },
      {
        "id": "track-1-joint",
        "name": "track-1 interface",
        "parent": "foundation",
        "child": "track-1",
        "type": "revolute",
        "anchorParent": [
          0,
          0.25,
          4
        ],
        "anchorChild": [
          0.050000000000000266,
          -0.10000000000000003,
          0
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          -0.8,
          0.8
        ]
      }
    ]
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 基座识别（h3-rotary-excavator-anchor）

哪些模块被声明为固定基座？

能力：基座识别；形式：single-choice；证据：model-state。

- A：[]
- B：["foundation","mast","primary-boom","tool-head","control-cab","service-cartridge","secondary-boom","clamp","sliding-tray","track--1","track-1"]
- C：["service-cartridge"]
- D：["foundation"]

```json
{
  "input": {
    "modules": [
      {
        "id": "foundation",
        "name": "foundation",
        "role": "frame",
        "position": [
          0,
          0.35,
          0
        ],
        "rotation": [
          0,
          0,
          0,
          1
        ],
        "anchored": true,
        "mass": 10
      },
      {
        "id": "mast",
        "name": "mast",
        "role": "frame",
        "position": [
          -1.6,
          3.35,
          -0.6
        ],
        "rotation": [
          0,
          0,
          0,
          1
        ],
        "anchored": false,
        "mass": 10
      },
      {
        "id": "primary-boom",
        "name": "primary boom",
        "role": "actuator",
        "position": [
          0.6463835548391197,
          7.915559217208119,
          -0.6
        ],
        "rotation": [
          0,
          0,
          0,
          1
        ],
        "anchored": false,
        "mass": 2
      },
      {
        "id": "tool-head",
        "name": "tool head",
        "role": "tool",
        "position": [
          3.1765027912943355,
          10.361118434416237,
          1.4
        ],
        "rotation": [
          0,
          0,
          0,
          1
        ],
        "anchored": false,
        "mass": 2
      },
      {
        "id": "control-cab",
        "name": "control cab",
        "role": "control",
        "position": [
          2,
          2.155,
          1.8
        ],
        "rotation": [
          0,
          0,
          0,
          1
        ],
        "anchored": false,
        "mass": 2
      },
      {
        "id": "service-cartridge",
        "name": "service cartridge",
        "role": "service",
        "position": [
          2,
          0.8500000000000001,
          -2
        ],
        "rotation": [
          0,
          0,
          0,
          1
        ],
        "anchored": false,
        "mass": 2
      },
      {
        "id": "secondary-boom",
        "name": "secondary boom",
        "role": "actuator",
        "position": [
          2.072131002778001,
          3.791259230469956,
          4
        ],
        "rotation": [
          0,
          0,
          0,
          1
        ],
        "anchored": false,
        "mass": 2
      },
      {
        "id": "clamp",
        "name": "clamp",
        "role": "tool",
        "position": [
          1.1354126538114302,
          5.637189707302727,
          4.8
        ],
        "rotation": [
          0,
          0,
          0,
          1
        ],
        "anchored": false,
        "mass": 2
      },
      {
        "id": "sliding-tray",
        "name": "sliding tray",
        "role": "payload",
        "position": [
          0,
          1.85,
          3.9
        ],
        "rotation": [
          0,
          0,
          0,
          1
        ],
        "anchored": false,
        "mass": 2
      },
      {
        "id": "track--1",
        "name": "track  1",
        "role": "traction",
        "position": [
          -0.050000000000000266,
          0.7,
          -4
        ],
        "rotation": [
          0,
          0,
          0,
          1
        ],
        "anchored": false,
        "mass": 2
      },
      {
        "id": "track-1",
        "name": "track 1",
        "role": "traction",
        "position": [
          -0.050000000000000266,
          0.7,
          4
        ],
        "rotation": [
          0,
          0,
          0,
          1
        ],
        "anchored": false,
        "mass": 2
      }
    ]
  },
  "answer": {
    "choiceId": "D"
  }
}
```

### 接口计数（h3-rotary-excavator-degree）

service-cartridge 连接几个声明关节？平行关节分别计数。

能力：接口计数；形式：single-choice；证据：model-state。

- A：1
- B：2
- C：0
- D：3

```json
{
  "input": {
    "joints": [
      {
        "id": "mast-joint",
        "name": "mast interface",
        "parent": "foundation",
        "child": "mast",
        "type": "fixed",
        "anchorParent": [
          -1.6,
          0.55,
          -0.6
        ],
        "anchorChild": [
          0,
          -2.45,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "primary-boom-joint",
        "name": "primary-boom interface",
        "parent": "mast",
        "child": "primary-boom",
        "type": "revolute",
        "anchorParent": [
          0,
          2.75,
          0
        ],
        "anchorChild": [
          -2.24638355483912,
          -1.8155592172081185,
          0
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          -0.8,
          0.8
        ]
      },
      {
        "id": "tool-head-joint",
        "name": "tool-head interface",
        "parent": "primary-boom",
        "child": "tool-head",
        "type": "revolute",
        "anchorParent": [
          2.530119236455216,
          1.8155592172081194,
          2
        ],
        "anchorChild": [
          0,
          -0.6299999999999999,
          0
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          -0.8,
          0.8
        ]
      },
      {
        "id": "control-cab-joint",
        "name": "control-cab interface",
        "parent": "foundation",
        "child": "control-cab",
        "type": "fixed",
        "anchorParent": [
          2,
          0.8499999999999999,
          1.8
        ],
        "anchorChild": [
          0,
          -0.9549999999999998,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "service-cartridge-joint",
        "name": "service-cartridge interface",
        "parent": "foundation",
        "child": "service-cartridge",
        "type": "fixed",
        "anchorParent": [
          2,
          0.45,
          -2
        ],
        "anchorChild": [
          0,
          -0.04999999999999999,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "secondary-boom-joint",
        "name": "secondary-boom interface",
        "parent": "control-cab",
        "child": "secondary-boom",
        "type": "revolute",
        "anchorParent": [
          0.7999999999999998,
          -0.1549999999999998,
          2.2
        ],
        "anchorChild": [
          0.7278689972219987,
          -1.7912592304699564,
          0
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          -0.8,
          0.8
        ]
      },
      {
        "id": "clamp-joint",
        "name": "clamp interface",
        "parent": "secondary-boom",
        "child": "clamp",
        "type": "revolute",
        "anchorParent": [
          -0.9367183489665709,
          1.8459304768327705,
          0.7999999999999998
        ],
        "anchorChild": [
          0,
          0,
          0
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          -0.8,
          0.8
        ]
      },
      {
        "id": "sliding-tray-joint",
        "name": "sliding-tray interface",
        "parent": "foundation",
        "child": "sliding-tray",
        "type": "prismatic",
        "anchorParent": [
          0,
          1.45,
          3.9
        ],
        "anchorChild": [
          0,
          -0.04999999999999999,
          0
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          -0.8,
          0.8
        ]
      },
      {
        "id": "track--1-joint",
        "name": "track--1 interface",
        "parent": "foundation",
        "child": "track--1",
        "type": "revolute",
        "anchorParent": [
          0,
          0.25,
          -4
        ],
        "anchorChild": [
          0.050000000000000266,
          -0.10000000000000003,
          0
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          -0.8,
          0.8
        ]
      },
      {
        "id": "track-1-joint",
        "name": "track-1 interface",
        "parent": "foundation",
        "child": "track-1",
        "type": "revolute",
        "anchorParent": [
          0,
          0.25,
          4
        ],
        "anchorChild": [
          0.050000000000000266,
          -0.10000000000000003,
          0
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          -0.8,
          0.8
        ]
      }
    ]
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 局部改色（h3-rotary-excavator-recolor）

仅将 service-cartridge-p99 改成 #e8792e，其他零件不变。选择正确补丁。

能力：局部改色；形式：single-choice；证据：model-state。

- A：{"id":"service-cartridge-p99","color":"#e8792e"}
- B：{"id":"service-cartridge-p100","color":"#e8792e"}
- C：{"id":"service-cartridge-p99","color":"#2878b8"}
- D：{"id":"*","color":"#e8792e"}

```json
{
  "input": {
    "part": {
      "id": "service-cartridge-p99",
      "moduleId": "service-cartridge",
      "shape": "plate",
      "position": [
        -0.5,
        -0.04999999999999999,
        -0.5
      ],
      "size": [
        0.98,
        0.28,
        0.98
      ],
      "color": "#dc6040",
      "rotation": [
        0,
        0,
        0,
        1
      ]
    }
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 补装部件（h3-rotary-excavator-add）

模块 service-cartridge 缺失零件 service-cartridge-p99。选择与目标清单一致的补装描述。

能力：补装部件；形式：single-choice；证据：model-state。

- A：{"id":"service-cartridge-p99","moduleId":"service-cartridge","shape":"plate","position":[-0.5,-0.04999999999999999,-0.5],"size":[0.98,0.28,0.98],"color":"#dc6040","rotation":[0,0,0,1]}
- B：{"id":"service-cartridge-p99","moduleId":"foundation","shape":"plate","position":[-0.5,-0.04999999999999999,-0.5],"size":[0.98,0.28,0.98],"color":"#dc6040","rotation":[0,0,0,1]}
- C：{"id":"service-cartridge-p99","moduleId":"service-cartridge","shape":"plate","position":[-0.5,-0.04999999999999999,-0.5],"size":[3,3,3],"color":"#dc6040","rotation":[0,0,0,1]}
- D：{"id":"service-cartridge-p99","moduleId":"service-cartridge","shape":"plate","position":[-0.5,-0.04999999999999999,-0.5],"size":[0.98,0.28,0.98],"color":"#000000","rotation":[0,0,0,1]}

```json
{
  "input": {
    "targetPart": {
      "id": "service-cartridge-p99",
      "moduleId": "service-cartridge",
      "shape": "plate",
      "position": [
        -0.5,
        -0.04999999999999999,
        -0.5
      ],
      "size": [
        0.98,
        0.28,
        0.98
      ],
      "color": "#dc6040",
      "rotation": [
        0,
        0,
        0,
        1
      ]
    },
    "existingIds": [
      "foundation-p1",
      "foundation-p2",
      "foundation-p3",
      "foundation-p4",
      "foundation-p5",
      "foundation-p6",
      "foundation-p7",
      "foundation-p8",
      "foundation-p9",
      "foundation-p10",
      "foundation-p11",
      "foundation-p12",
      "foundation-p13",
      "foundation-p14",
      "foundation-p15",
      "foundation-p16",
      "foundation-p17",
      "foundation-p18",
      "foundation-p19",
      "foundation-p20",
      "foundation-p21",
      "foundation-p22",
      "foundation-p23",
      "foundation-p24",
      "foundation-p25",
      "foundation-p26",
      "foundation-p27",
      "foundation-p28",
      "foundation-p29",
      "foundation-p30",
      "mast-p31",
      "mast-p32",
      "mast-p33",
      "mast-p34",
      "mast-p35",
      "mast-p36",
      "mast-p37",
      "mast-p38",
      "mast-p39",
      "mast-p40",
      "mast-p41",
      "mast-p42",
      "mast-p43",
      "mast-p44",
      "mast-p45",
      "mast-p46",
      "mast-p47",
      "mast-p48",
      "mast-p49",
      "mast-p50",
      "mast-p51",
      "mast-p52",
      "mast-p53",
      "mast-p54",
      "mast-p55",
      "mast-p56",
      "mast-p57",
      "mast-p58",
      "mast-p59",
      "mast-p60",
      "mast-p61",
      "mast-p62",
      "mast-p63",
      "mast-p64",
      "mast-p65",
      "mast-p66",
      "mast-p67",
      "mast-p68",
      "mast-p69",
      "primary-boom-p70",
      "primary-boom-p71",
      "primary-boom-p72",
      "primary-boom-p73",
      "primary-boom-p74",
      "primary-boom-p75",
      "primary-boom-p76",
      "tool-head-p77",
      "tool-head-p78",
      "tool-head-p79",
      "tool-head-p80",
      "tool-head-p81",
      "tool-head-p82",
      "tool-head-p83",
      "tool-head-p84",
      "tool-head-p85",
      "tool-head-p86",
      "tool-head-p87",
      "tool-head-p88",
      "tool-head-p89",
      "tool-head-p90",
      "control-cab-p91",
      "control-cab-p92",
      "control-cab-p93",
      "control-cab-p94",
      "control-cab-p95",
      "control-cab-p96",
      "control-cab-p97",
      "control-cab-p98",
      "service-cartridge-p100",
      "service-cartridge-p101",
      "service-cartridge-p102",
      "secondary-boom-p103",
      "secondary-boom-p104",
      "secondary-boom-p105",
      "secondary-boom-p106",
      "secondary-boom-p107",
      "clamp-p108",
      "sliding-tray-p109",
      "sliding-tray-p110",
      "sliding-tray-p111",
      "sliding-tray-p112",
      "sliding-tray-p113",
      "sliding-tray-p114",
      "sliding-tray-p115",
      "sliding-tray-p116",
      "track--1-p117",
      "track--1-p118",
      "track--1-p119",
      "track--1-p120",
      "track--1-p121",
      "track--1-p122",
      "track--1-p123",
      "track--1-p124",
      "track--1-p125",
      "track--1-p126",
      "track--1-p127",
      "track--1-p128",
      "track--1-p129",
      "track--1-p130",
      "track--1-p131",
      "track--1-p132",
      "track--1-p133",
      "track--1-p134",
      "track--1-p135",
      "track-1-p136",
      "track-1-p137",
      "track-1-p138",
      "track-1-p139",
      "track-1-p140",
      "track-1-p141",
      "track-1-p142",
      "track-1-p143",
      "track-1-p144",
      "track-1-p145",
      "track-1-p146",
      "track-1-p147",
      "track-1-p148",
      "track-1-p149",
      "track-1-p150",
      "track-1-p151",
      "track-1-p152",
      "track-1-p153",
      "track-1-p154"
    ]
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 安全拆除（h3-rotary-excavator-remove）

按声明依赖图，当前可以先拆哪些叶模块？

能力：安全拆除；形式：single-choice；证据：model-state。

- A：[]
- B：["foundation","mast","primary-boom","tool-head","control-cab","service-cartridge","secondary-boom","clamp","sliding-tray","track--1","track-1"]
- C：["clamp","service-cartridge","sliding-tray","tool-head","track--1","track-1"]
- D：["foundation"]

```json
{
  "input": {
    "joints": [
      {
        "id": "mast-joint",
        "name": "mast interface",
        "parent": "foundation",
        "child": "mast",
        "type": "fixed",
        "anchorParent": [
          -1.6,
          0.55,
          -0.6
        ],
        "anchorChild": [
          0,
          -2.45,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "primary-boom-joint",
        "name": "primary-boom interface",
        "parent": "mast",
        "child": "primary-boom",
        "type": "revolute",
        "anchorParent": [
          0,
          2.75,
          0
        ],
        "anchorChild": [
          -2.24638355483912,
          -1.8155592172081185,
          0
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          -0.8,
          0.8
        ]
      },
      {
        "id": "tool-head-joint",
        "name": "tool-head interface",
        "parent": "primary-boom",
        "child": "tool-head",
        "type": "revolute",
        "anchorParent": [
          2.530119236455216,
          1.8155592172081194,
          2
        ],
        "anchorChild": [
          0,
          -0.6299999999999999,
          0
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          -0.8,
          0.8
        ]
      },
      {
        "id": "control-cab-joint",
        "name": "control-cab interface",
        "parent": "foundation",
        "child": "control-cab",
        "type": "fixed",
        "anchorParent": [
          2,
          0.8499999999999999,
          1.8
        ],
        "anchorChild": [
          0,
          -0.9549999999999998,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "service-cartridge-joint",
        "name": "service-cartridge interface",
        "parent": "foundation",
        "child": "service-cartridge",
        "type": "fixed",
        "anchorParent": [
          2,
          0.45,
          -2
        ],
        "anchorChild": [
          0,
          -0.04999999999999999,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "secondary-boom-joint",
        "name": "secondary-boom interface",
        "parent": "control-cab",
        "child": "secondary-boom",
        "type": "revolute",
        "anchorParent": [
          0.7999999999999998,
          -0.1549999999999998,
          2.2
        ],
        "anchorChild": [
          0.7278689972219987,
          -1.7912592304699564,
          0
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          -0.8,
          0.8
        ]
      },
      {
        "id": "clamp-joint",
        "name": "clamp interface",
        "parent": "secondary-boom",
        "child": "clamp",
        "type": "revolute",
        "anchorParent": [
          -0.9367183489665709,
          1.8459304768327705,
          0.7999999999999998
        ],
        "anchorChild": [
          0,
          0,
          0
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          -0.8,
          0.8
        ]
      },
      {
        "id": "sliding-tray-joint",
        "name": "sliding-tray interface",
        "parent": "foundation",
        "child": "sliding-tray",
        "type": "prismatic",
        "anchorParent": [
          0,
          1.45,
          3.9
        ],
        "anchorChild": [
          0,
          -0.04999999999999999,
          0
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          -0.8,
          0.8
        ]
      },
      {
        "id": "track--1-joint",
        "name": "track--1 interface",
        "parent": "foundation",
        "child": "track--1",
        "type": "revolute",
        "anchorParent": [
          0,
          0.25,
          -4
        ],
        "anchorChild": [
          0.050000000000000266,
          -0.10000000000000003,
          0
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          -0.8,
          0.8
        ]
      },
      {
        "id": "track-1-joint",
        "name": "track-1 interface",
        "parent": "foundation",
        "child": "track-1",
        "type": "revolute",
        "anchorParent": [
          0,
          0.25,
          4
        ],
        "anchorChild": [
          0.050000000000000266,
          -0.10000000000000003,
          0
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          -0.8,
          0.8
        ]
      }
    ],
    "modules": [
      "foundation",
      "mast",
      "primary-boom",
      "tool-head",
      "control-cab",
      "service-cartridge",
      "secondary-boom",
      "clamp",
      "sliding-tray",
      "track--1",
      "track-1"
    ]
  },
  "answer": {
    "choiceId": "C"
  }
}
```

### 替换选择（h3-rotary-excavator-replace）

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
        "cost": 2,
        "stiffness": 9,
        "mass": 1.5
      },
      {
        "id": "stock-1",
        "cost": 7,
        "stiffness": 11,
        "mass": 1.5
      },
      {
        "id": "stock-2",
        "cost": 3,
        "stiffness": 7,
        "mass": 1.8
      },
      {
        "id": "stock-3",
        "cost": 7,
        "stiffness": 7,
        "mass": 1.5
      }
    ],
    "maxCost": 6
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 平移纠偏（h3-rotary-excavator-translate）

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
    "target": "service-cartridge"
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 姿态纠偏（h3-rotary-excavator-rotate）

选择从当前yaw到目标yaw的最短有符号旋转；恰好180°时使用-180°。

能力：姿态纠偏；形式：single-choice；证据：model-state。

- A：90
- B：-90
- C：0
- D：-180

```json
{
  "input": {
    "module": "service-cartridge",
    "currentYaw": 180,
    "targetYaw": 270
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 下一步放置（h3-rotary-excavator-next-module）

已完成给定前缀，选择所有前置依赖已满足的下一模块集合。

能力：下一步放置；形式：single-choice；证据：model-state。

- A：[]
- B：["foundation","mast","primary-boom","tool-head","control-cab","service-cartridge"]
- C：["secondary-boom","clamp","sliding-tray","track--1","track-1"]
- D：["secondary-boom","sliding-tray","track--1","track-1"]

```json
{
  "input": {
    "prefix": [
      "foundation",
      "mast",
      "primary-boom",
      "tool-head",
      "control-cab",
      "service-cartridge"
    ],
    "joints": [
      {
        "id": "mast-joint",
        "name": "mast interface",
        "parent": "foundation",
        "child": "mast",
        "type": "fixed",
        "anchorParent": [
          -1.6,
          0.55,
          -0.6
        ],
        "anchorChild": [
          0,
          -2.45,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "primary-boom-joint",
        "name": "primary-boom interface",
        "parent": "mast",
        "child": "primary-boom",
        "type": "revolute",
        "anchorParent": [
          0,
          2.75,
          0
        ],
        "anchorChild": [
          -2.24638355483912,
          -1.8155592172081185,
          0
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          -0.8,
          0.8
        ]
      },
      {
        "id": "tool-head-joint",
        "name": "tool-head interface",
        "parent": "primary-boom",
        "child": "tool-head",
        "type": "revolute",
        "anchorParent": [
          2.530119236455216,
          1.8155592172081194,
          2
        ],
        "anchorChild": [
          0,
          -0.6299999999999999,
          0
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          -0.8,
          0.8
        ]
      },
      {
        "id": "control-cab-joint",
        "name": "control-cab interface",
        "parent": "foundation",
        "child": "control-cab",
        "type": "fixed",
        "anchorParent": [
          2,
          0.8499999999999999,
          1.8
        ],
        "anchorChild": [
          0,
          -0.9549999999999998,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "service-cartridge-joint",
        "name": "service-cartridge interface",
        "parent": "foundation",
        "child": "service-cartridge",
        "type": "fixed",
        "anchorParent": [
          2,
          0.45,
          -2
        ],
        "anchorChild": [
          0,
          -0.04999999999999999,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "secondary-boom-joint",
        "name": "secondary-boom interface",
        "parent": "control-cab",
        "child": "secondary-boom",
        "type": "revolute",
        "anchorParent": [
          0.7999999999999998,
          -0.1549999999999998,
          2.2
        ],
        "anchorChild": [
          0.7278689972219987,
          -1.7912592304699564,
          0
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          -0.8,
          0.8
        ]
      },
      {
        "id": "clamp-joint",
        "name": "clamp interface",
        "parent": "secondary-boom",
        "child": "clamp",
        "type": "revolute",
        "anchorParent": [
          -0.9367183489665709,
          1.8459304768327705,
          0.7999999999999998
        ],
        "anchorChild": [
          0,
          0,
          0
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          -0.8,
          0.8
        ]
      },
      {
        "id": "sliding-tray-joint",
        "name": "sliding-tray interface",
        "parent": "foundation",
        "child": "sliding-tray",
        "type": "prismatic",
        "anchorParent": [
          0,
          1.45,
          3.9
        ],
        "anchorChild": [
          0,
          -0.04999999999999999,
          0
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          -0.8,
          0.8
        ]
      },
      {
        "id": "track--1-joint",
        "name": "track--1 interface",
        "parent": "foundation",
        "child": "track--1",
        "type": "revolute",
        "anchorParent": [
          0,
          0.25,
          -4
        ],
        "anchorChild": [
          0.050000000000000266,
          -0.10000000000000003,
          0
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          -0.8,
          0.8
        ]
      },
      {
        "id": "track-1-joint",
        "name": "track-1 interface",
        "parent": "foundation",
        "child": "track-1",
        "type": "revolute",
        "anchorParent": [
          0,
          0.25,
          4
        ],
        "anchorChild": [
          0.050000000000000266,
          -0.10000000000000003,
          0
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          -0.8,
          0.8
        ]
      }
    ],
    "modules": [
      "foundation",
      "mast",
      "primary-boom",
      "tool-head",
      "control-cab",
      "service-cartridge",
      "secondary-boom",
      "clamp",
      "sliding-tray",
      "track--1",
      "track-1"
    ]
  },
  "answer": {
    "choiceId": "D"
  }
}
```

### 库存核算（h3-rotary-excavator-inventory）

备件库有 10 件，替换模块需 4 件，还剩多少？

能力：库存核算；形式：single-choice；证据：model-state。

- A：9
- B：6
- C：7
- D：5

```json
{
  "input": {
    "available": 10,
    "required": 4
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 子装配边界（h3-rotary-excavator-boundary）

隔离 service-cartridge 需要断开哪些边界关节？

能力：子装配边界；形式：single-choice；证据：model-state。

- A：["mast-joint","primary-boom-joint","tool-head-joint","control-cab-joint","service-cartridge-joint","secondary-boom-joint","clamp-joint","sliding-tray-joint","track--1-joint","track-1-joint"]
- B：["primary-boom-joint"]
- C：["service-cartridge-joint"]
- D：[]

```json
{
  "input": {
    "joints": [
      {
        "id": "mast-joint",
        "name": "mast interface",
        "parent": "foundation",
        "child": "mast",
        "type": "fixed",
        "anchorParent": [
          -1.6,
          0.55,
          -0.6
        ],
        "anchorChild": [
          0,
          -2.45,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "primary-boom-joint",
        "name": "primary-boom interface",
        "parent": "mast",
        "child": "primary-boom",
        "type": "revolute",
        "anchorParent": [
          0,
          2.75,
          0
        ],
        "anchorChild": [
          -2.24638355483912,
          -1.8155592172081185,
          0
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          -0.8,
          0.8
        ]
      },
      {
        "id": "tool-head-joint",
        "name": "tool-head interface",
        "parent": "primary-boom",
        "child": "tool-head",
        "type": "revolute",
        "anchorParent": [
          2.530119236455216,
          1.8155592172081194,
          2
        ],
        "anchorChild": [
          0,
          -0.6299999999999999,
          0
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          -0.8,
          0.8
        ]
      },
      {
        "id": "control-cab-joint",
        "name": "control-cab interface",
        "parent": "foundation",
        "child": "control-cab",
        "type": "fixed",
        "anchorParent": [
          2,
          0.8499999999999999,
          1.8
        ],
        "anchorChild": [
          0,
          -0.9549999999999998,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "service-cartridge-joint",
        "name": "service-cartridge interface",
        "parent": "foundation",
        "child": "service-cartridge",
        "type": "fixed",
        "anchorParent": [
          2,
          0.45,
          -2
        ],
        "anchorChild": [
          0,
          -0.04999999999999999,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "secondary-boom-joint",
        "name": "secondary-boom interface",
        "parent": "control-cab",
        "child": "secondary-boom",
        "type": "revolute",
        "anchorParent": [
          0.7999999999999998,
          -0.1549999999999998,
          2.2
        ],
        "anchorChild": [
          0.7278689972219987,
          -1.7912592304699564,
          0
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          -0.8,
          0.8
        ]
      },
      {
        "id": "clamp-joint",
        "name": "clamp interface",
        "parent": "secondary-boom",
        "child": "clamp",
        "type": "revolute",
        "anchorParent": [
          -0.9367183489665709,
          1.8459304768327705,
          0.7999999999999998
        ],
        "anchorChild": [
          0,
          0,
          0
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          -0.8,
          0.8
        ]
      },
      {
        "id": "sliding-tray-joint",
        "name": "sliding-tray interface",
        "parent": "foundation",
        "child": "sliding-tray",
        "type": "prismatic",
        "anchorParent": [
          0,
          1.45,
          3.9
        ],
        "anchorChild": [
          0,
          -0.04999999999999999,
          0
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          -0.8,
          0.8
        ]
      },
      {
        "id": "track--1-joint",
        "name": "track--1 interface",
        "parent": "foundation",
        "child": "track--1",
        "type": "revolute",
        "anchorParent": [
          0,
          0.25,
          -4
        ],
        "anchorChild": [
          0.050000000000000266,
          -0.10000000000000003,
          0
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          -0.8,
          0.8
        ]
      },
      {
        "id": "track-1-joint",
        "name": "track-1 interface",
        "parent": "foundation",
        "child": "track-1",
        "type": "revolute",
        "anchorParent": [
          0,
          0.25,
          4
        ],
        "anchorChild": [
          0.050000000000000266,
          -0.10000000000000003,
          0
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          -0.8,
          0.8
        ]
      }
    ],
    "target": "service-cartridge"
  },
  "answer": {
    "choiceId": "C"
  }
}
```

### 最小干预（h3-rotary-excavator-no-op）

当前模块颜色已满足指令，且无需改变位姿。最少需要几次编辑？

能力：最小干预；形式：single-choice；证据：model-state。

- A：0
- B：1
- C：2
- D：4

```json
{
  "input": {
    "module": "service-cartridge"
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 全过程依赖（h3-rotary-excavator-prefix）

给定候选顺序，首次违反前置依赖的步骤是？从 0 编号，-1 表示没有违反。

能力：全过程依赖；形式：single-choice；证据：support-graph。

- A：-1
- B：0
- C：10

```json
{
  "input": {
    "order": [
      "foundation",
      "mast",
      "primary-boom",
      "tool-head",
      "control-cab",
      "service-cartridge",
      "secondary-boom",
      "clamp",
      "sliding-tray",
      "track--1",
      "track-1"
    ],
    "joints": [
      {
        "id": "mast-joint",
        "name": "mast interface",
        "parent": "foundation",
        "child": "mast",
        "type": "fixed",
        "anchorParent": [
          -1.6,
          0.55,
          -0.6
        ],
        "anchorChild": [
          0,
          -2.45,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "primary-boom-joint",
        "name": "primary-boom interface",
        "parent": "mast",
        "child": "primary-boom",
        "type": "revolute",
        "anchorParent": [
          0,
          2.75,
          0
        ],
        "anchorChild": [
          -2.24638355483912,
          -1.8155592172081185,
          0
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          -0.8,
          0.8
        ]
      },
      {
        "id": "tool-head-joint",
        "name": "tool-head interface",
        "parent": "primary-boom",
        "child": "tool-head",
        "type": "revolute",
        "anchorParent": [
          2.530119236455216,
          1.8155592172081194,
          2
        ],
        "anchorChild": [
          0,
          -0.6299999999999999,
          0
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          -0.8,
          0.8
        ]
      },
      {
        "id": "control-cab-joint",
        "name": "control-cab interface",
        "parent": "foundation",
        "child": "control-cab",
        "type": "fixed",
        "anchorParent": [
          2,
          0.8499999999999999,
          1.8
        ],
        "anchorChild": [
          0,
          -0.9549999999999998,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "service-cartridge-joint",
        "name": "service-cartridge interface",
        "parent": "foundation",
        "child": "service-cartridge",
        "type": "fixed",
        "anchorParent": [
          2,
          0.45,
          -2
        ],
        "anchorChild": [
          0,
          -0.04999999999999999,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "secondary-boom-joint",
        "name": "secondary-boom interface",
        "parent": "control-cab",
        "child": "secondary-boom",
        "type": "revolute",
        "anchorParent": [
          0.7999999999999998,
          -0.1549999999999998,
          2.2
        ],
        "anchorChild": [
          0.7278689972219987,
          -1.7912592304699564,
          0
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          -0.8,
          0.8
        ]
      },
      {
        "id": "clamp-joint",
        "name": "clamp interface",
        "parent": "secondary-boom",
        "child": "clamp",
        "type": "revolute",
        "anchorParent": [
          -0.9367183489665709,
          1.8459304768327705,
          0.7999999999999998
        ],
        "anchorChild": [
          0,
          0,
          0
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          -0.8,
          0.8
        ]
      },
      {
        "id": "sliding-tray-joint",
        "name": "sliding-tray interface",
        "parent": "foundation",
        "child": "sliding-tray",
        "type": "prismatic",
        "anchorParent": [
          0,
          1.45,
          3.9
        ],
        "anchorChild": [
          0,
          -0.04999999999999999,
          0
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          -0.8,
          0.8
        ]
      },
      {
        "id": "track--1-joint",
        "name": "track--1 interface",
        "parent": "foundation",
        "child": "track--1",
        "type": "revolute",
        "anchorParent": [
          0,
          0.25,
          -4
        ],
        "anchorChild": [
          0.050000000000000266,
          -0.10000000000000003,
          0
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          -0.8,
          0.8
        ]
      },
      {
        "id": "track-1-joint",
        "name": "track-1 interface",
        "parent": "foundation",
        "child": "track-1",
        "type": "revolute",
        "anchorParent": [
          0,
          0.25,
          4
        ],
        "anchorChild": [
          0.050000000000000266,
          -0.10000000000000003,
          0
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          -0.8,
          0.8
        ]
      }
    ]
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 连续维修路径（h3-rotary-excavator-access）

根据实际 Rapier shape cast 记录，选择全部无碰撞路径。

能力：连续维修路径；形式：multiple-choice；证据：Rapier。

- A：path-0
- B：path-1
- C：path-2

```json
{
  "input": {
    "paths": [
      {
        "id": "path-0",
        "start": [
          9.176502791294336,
          0.8500000000000001,
          -2
        ],
        "end": [
          2,
          0.8500000000000001,
          -2
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
          2,
          15.131118434416237,
          -2
        ],
        "end": [
          2,
          0.8500000000000001,
          -2
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
          2,
          0.8500000000000001,
          9.3
        ],
        "end": [
          2,
          0.8500000000000001,
          -2
        ],
        "halfExtents": [
          0.18,
          0.18,
          0.18
        ],
        "clear": false,
        "timeOfImpact": 0.4221239387989044
      }
    ],
    "simulator": "stud-inclusive conservative cuboids; anchored base; force-limited position servos; no clutch/material calibration"
  },
  "answer": {
    "choiceIds": [
      "A",
      "B"
    ]
  }
}
```

### 支撑反事实（h3-rotary-excavator-counterfactual）

移除指定模块后，哪些其余模块失去到任一基座的关节路径？不包含被移除模块本身。

能力：支撑反事实；形式：single-choice；证据：support-graph。

- A：["mast"]
- B：[]
- C：["foundation","mast","primary-boom","tool-head","control-cab","service-cartridge","secondary-boom","clamp","sliding-tray","track--1","track-1"]
- D：["primary-boom","tool-head"]

```json
{
  "input": {
    "removed": "mast",
    "roots": [
      "foundation"
    ],
    "joints": [
      {
        "id": "mast-joint",
        "name": "mast interface",
        "parent": "foundation",
        "child": "mast",
        "type": "fixed",
        "anchorParent": [
          -1.6,
          0.55,
          -0.6
        ],
        "anchorChild": [
          0,
          -2.45,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "primary-boom-joint",
        "name": "primary-boom interface",
        "parent": "mast",
        "child": "primary-boom",
        "type": "revolute",
        "anchorParent": [
          0,
          2.75,
          0
        ],
        "anchorChild": [
          -2.24638355483912,
          -1.8155592172081185,
          0
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          -0.8,
          0.8
        ]
      },
      {
        "id": "tool-head-joint",
        "name": "tool-head interface",
        "parent": "primary-boom",
        "child": "tool-head",
        "type": "revolute",
        "anchorParent": [
          2.530119236455216,
          1.8155592172081194,
          2
        ],
        "anchorChild": [
          0,
          -0.6299999999999999,
          0
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          -0.8,
          0.8
        ]
      },
      {
        "id": "control-cab-joint",
        "name": "control-cab interface",
        "parent": "foundation",
        "child": "control-cab",
        "type": "fixed",
        "anchorParent": [
          2,
          0.8499999999999999,
          1.8
        ],
        "anchorChild": [
          0,
          -0.9549999999999998,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "service-cartridge-joint",
        "name": "service-cartridge interface",
        "parent": "foundation",
        "child": "service-cartridge",
        "type": "fixed",
        "anchorParent": [
          2,
          0.45,
          -2
        ],
        "anchorChild": [
          0,
          -0.04999999999999999,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "secondary-boom-joint",
        "name": "secondary-boom interface",
        "parent": "control-cab",
        "child": "secondary-boom",
        "type": "revolute",
        "anchorParent": [
          0.7999999999999998,
          -0.1549999999999998,
          2.2
        ],
        "anchorChild": [
          0.7278689972219987,
          -1.7912592304699564,
          0
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          -0.8,
          0.8
        ]
      },
      {
        "id": "clamp-joint",
        "name": "clamp interface",
        "parent": "secondary-boom",
        "child": "clamp",
        "type": "revolute",
        "anchorParent": [
          -0.9367183489665709,
          1.8459304768327705,
          0.7999999999999998
        ],
        "anchorChild": [
          0,
          0,
          0
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          -0.8,
          0.8
        ]
      },
      {
        "id": "sliding-tray-joint",
        "name": "sliding-tray interface",
        "parent": "foundation",
        "child": "sliding-tray",
        "type": "prismatic",
        "anchorParent": [
          0,
          1.45,
          3.9
        ],
        "anchorChild": [
          0,
          -0.04999999999999999,
          0
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          -0.8,
          0.8
        ]
      },
      {
        "id": "track--1-joint",
        "name": "track--1 interface",
        "parent": "foundation",
        "child": "track--1",
        "type": "revolute",
        "anchorParent": [
          0,
          0.25,
          -4
        ],
        "anchorChild": [
          0.050000000000000266,
          -0.10000000000000003,
          0
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          -0.8,
          0.8
        ]
      },
      {
        "id": "track-1-joint",
        "name": "track-1 interface",
        "parent": "foundation",
        "child": "track-1",
        "type": "revolute",
        "anchorParent": [
          0,
          0.25,
          4
        ],
        "anchorChild": [
          0.050000000000000266,
          -0.10000000000000003,
          0
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          -0.8,
          0.8
        ]
      }
    ],
    "modules": [
      "foundation",
      "mast",
      "primary-boom",
      "tool-head",
      "control-cab",
      "service-cartridge",
      "secondary-boom",
      "clamp",
      "sliding-tray",
      "track--1",
      "track-1"
    ]
  },
  "answer": {
    "choiceId": "D"
  }
}
```

### 冲击响应读数（h3-rotary-excavator-dynamic）

Rapier 实际采样轨迹中的最大平移位移是多少？按四位小数报告。

能力：冲击响应读数；形式：single-choice；证据：Rapier。

- A：1.0073
- B：0.0073
- C：0.2073
- D：0

```json
{
  "input": {
    "trace": [
      {
        "time": 0.008333333333333333,
        "displacement": 0.00559594674894626
      },
      {
        "time": 0.10833333333333334,
        "displacement": 0.007276417923634616
      },
      {
        "time": 0.20833333333333334,
        "displacement": 0.005770755192200806
      },
      {
        "time": 0.30833333333333335,
        "displacement": 0.002118215492300024
      },
      {
        "time": 0.4083333333333333,
        "displacement": 0.00018572911562461764
      },
      {
        "time": 0.5083333333333333,
        "displacement": 0.0003473260439354856
      },
      {
        "time": 0.6083333333333333,
        "displacement": 0.00022248000358433823
      },
      {
        "time": 0.7083333333333334,
        "displacement": 0.00009502423642286626
      },
      {
        "time": 0.8083333333333333,
        "displacement": 0.000021523219896656582
      },
      {
        "time": 0.9083333333333333,
        "displacement": 0.0000018706744702428838
      },
      {
        "time": 1,
        "displacement": 0.0000018706744702428838
      }
    ],
    "impulse": [
      10,
      1.8,
      3.5
    ],
    "nominalDrift": 0.014374453448343661,
    "scope": "采样轨迹极值，非连续时间极值；不代表实物安全阈值"
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 关节限位推理（h3-rotary-excavator-kinematic）

下列目标位置/角度中哪些在关节声明限位内（含边界）？

能力：关节限位推理；形式：multiple-choice；证据：model-state。

- A：-0.8
- B：0
- C：-1.3
- D：1.3

```json
{
  "input": {
    "joint": "primary-boom-joint",
    "limits": [
      -0.8,
      0.8
    ],
    "units": "radians"
  },
  "answer": {
    "choiceIds": [
      "A",
      "B"
    ]
  }
}
```

### 约束故障诊断（h3-rotary-excavator-diagnosis）

已检测到端点和约束类型如下，选择匹配的全部关节。

能力：约束故障诊断；形式：multiple-choice；证据：model-state。

- A：service-cartridge-joint
- B：mast-joint
- C：primary-boom-joint
- D：tool-head-joint

```json
{
  "input": {
    "endpoints": [
      "foundation",
      "service-cartridge"
    ],
    "type": "fixed",
    "joints": [
      {
        "id": "mast-joint",
        "name": "mast interface",
        "parent": "foundation",
        "child": "mast",
        "type": "fixed",
        "anchorParent": [
          -1.6,
          0.55,
          -0.6
        ],
        "anchorChild": [
          0,
          -2.45,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "primary-boom-joint",
        "name": "primary-boom interface",
        "parent": "mast",
        "child": "primary-boom",
        "type": "revolute",
        "anchorParent": [
          0,
          2.75,
          0
        ],
        "anchorChild": [
          -2.24638355483912,
          -1.8155592172081185,
          0
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          -0.8,
          0.8
        ]
      },
      {
        "id": "tool-head-joint",
        "name": "tool-head interface",
        "parent": "primary-boom",
        "child": "tool-head",
        "type": "revolute",
        "anchorParent": [
          2.530119236455216,
          1.8155592172081194,
          2
        ],
        "anchorChild": [
          0,
          -0.6299999999999999,
          0
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          -0.8,
          0.8
        ]
      },
      {
        "id": "control-cab-joint",
        "name": "control-cab interface",
        "parent": "foundation",
        "child": "control-cab",
        "type": "fixed",
        "anchorParent": [
          2,
          0.8499999999999999,
          1.8
        ],
        "anchorChild": [
          0,
          -0.9549999999999998,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "service-cartridge-joint",
        "name": "service-cartridge interface",
        "parent": "foundation",
        "child": "service-cartridge",
        "type": "fixed",
        "anchorParent": [
          2,
          0.45,
          -2
        ],
        "anchorChild": [
          0,
          -0.04999999999999999,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "secondary-boom-joint",
        "name": "secondary-boom interface",
        "parent": "control-cab",
        "child": "secondary-boom",
        "type": "revolute",
        "anchorParent": [
          0.7999999999999998,
          -0.1549999999999998,
          2.2
        ],
        "anchorChild": [
          0.7278689972219987,
          -1.7912592304699564,
          0
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          -0.8,
          0.8
        ]
      },
      {
        "id": "clamp-joint",
        "name": "clamp interface",
        "parent": "secondary-boom",
        "child": "clamp",
        "type": "revolute",
        "anchorParent": [
          -0.9367183489665709,
          1.8459304768327705,
          0.7999999999999998
        ],
        "anchorChild": [
          0,
          0,
          0
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          -0.8,
          0.8
        ]
      },
      {
        "id": "sliding-tray-joint",
        "name": "sliding-tray interface",
        "parent": "foundation",
        "child": "sliding-tray",
        "type": "prismatic",
        "anchorParent": [
          0,
          1.45,
          3.9
        ],
        "anchorChild": [
          0,
          -0.04999999999999999,
          0
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          -0.8,
          0.8
        ]
      },
      {
        "id": "track--1-joint",
        "name": "track--1 interface",
        "parent": "foundation",
        "child": "track--1",
        "type": "revolute",
        "anchorParent": [
          0,
          0.25,
          -4
        ],
        "anchorChild": [
          0.050000000000000266,
          -0.10000000000000003,
          0
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          -0.8,
          0.8
        ]
      },
      {
        "id": "track-1-joint",
        "name": "track-1 interface",
        "parent": "foundation",
        "child": "track-1",
        "type": "revolute",
        "anchorParent": [
          0,
          0.25,
          4
        ],
        "anchorChild": [
          0.050000000000000266,
          -0.10000000000000003,
          0
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          -0.8,
          0.8
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

### 主动检查收益（h3-rotary-excavator-information-gain）

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
        "cost": 1,
        "returns": [
          0,
          0,
          1,
          1
        ]
      },
      {
        "id": "query-1",
        "cost": 2,
        "returns": [
          0,
          1,
          2,
          3
        ]
      },
      {
        "id": "query-2",
        "cost": 3,
        "returns": [
          0,
          0,
          0,
          1
        ]
      }
    ],
    "module": "service-cartridge",
    "worlds": [
      "normal",
      "jammed",
      "reversed",
      "loose"
    ]
  },
  "answer": {
    "choiceIds": [
      "B",
      "C"
    ]
  }
}
```

### 不确定性与弃答（h3-rotary-excavator-abstention）

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

### 观测后信念更新（h3-rotary-excavator-posterior）

均匀先验，得到给定观测后，jammed 世界的后验概率是多少？

能力：观测后信念更新；形式：single-choice；证据：finite-world。

- A：0.5
- B：0
- C：0.25
- D：0.3333333333333333

```json
{
  "input": {
    "module": "service-cartridge",
    "worlds": [
      "normal",
      "jammed",
      "reversed",
      "loose"
    ],
    "observationByWorld": [
      "negative",
      "negative",
      "positive",
      "positive"
    ],
    "observed": "negative"
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 多目标工程权衡（h3-rotary-excavator-pareto）

最小成本、最小质量、最大刚度，选择完整非支配集合。

能力：多目标工程权衡；形式：multiple-choice；证据：model-state。

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
        "cost": 2,
        "stiffness": 9,
        "mass": 1.5
      },
      {
        "id": "stock-1",
        "cost": 7,
        "stiffness": 11,
        "mass": 1.5
      },
      {
        "id": "stock-2",
        "cost": 3,
        "stiffness": 7,
        "mass": 1.8
      },
      {
        "id": "stock-3",
        "cost": 7,
        "stiffness": 7,
        "mass": 1.5
      }
    ]
  },
  "answer": {
    "choiceIds": [
      "B",
      "C"
    ]
  }
}
```

### 依赖装配（h3-rotary-excavator-assembly）

提交 actionIds。执行公开前置条件与效果，达到所有目标且不超过预算；允许交换独立动作。

能力：依赖装配；形式：actions；证据：state-machine。


```json
{
  "input": {
    "initialFacts": [],
    "initialModules": [],
    "actions": [
      {
        "id": "place:primary-boom",
        "label": "安装 primary-boom",
        "requires": [
          "present:mast"
        ],
        "forbids": [
          "present:primary-boom"
        ],
        "adds": [
          "present:primary-boom"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "primary-boom",
          "visible": true
        }
      },
      {
        "id": "place:track-1",
        "label": "安装 track-1",
        "requires": [
          "present:foundation"
        ],
        "forbids": [
          "present:track-1"
        ],
        "adds": [
          "present:track-1"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "track-1",
          "visible": true
        }
      },
      {
        "id": "place:secondary-boom",
        "label": "安装 secondary-boom",
        "requires": [
          "present:control-cab"
        ],
        "forbids": [
          "present:secondary-boom"
        ],
        "adds": [
          "present:secondary-boom"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "secondary-boom",
          "visible": true
        }
      },
      {
        "id": "place:control-cab",
        "label": "安装 control-cab",
        "requires": [
          "present:foundation"
        ],
        "forbids": [
          "present:control-cab"
        ],
        "adds": [
          "present:control-cab"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "control-cab",
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
        "id": "place:clamp",
        "label": "安装 clamp",
        "requires": [
          "present:secondary-boom"
        ],
        "forbids": [
          "present:clamp"
        ],
        "adds": [
          "present:clamp"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "clamp",
          "visible": true
        }
      },
      {
        "id": "place:service-cartridge",
        "label": "安装 service-cartridge",
        "requires": [
          "present:foundation"
        ],
        "forbids": [
          "present:service-cartridge"
        ],
        "adds": [
          "present:service-cartridge"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "service-cartridge",
          "visible": true
        }
      },
      {
        "id": "place:track--1",
        "label": "安装 track--1",
        "requires": [
          "present:foundation"
        ],
        "forbids": [
          "present:track--1"
        ],
        "adds": [
          "present:track--1"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "track--1",
          "visible": true
        }
      },
      {
        "id": "place:mast",
        "label": "安装 mast",
        "requires": [
          "present:foundation"
        ],
        "forbids": [
          "present:mast"
        ],
        "adds": [
          "present:mast"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "mast",
          "visible": true
        }
      },
      {
        "id": "place:sliding-tray",
        "label": "安装 sliding-tray",
        "requires": [
          "present:foundation"
        ],
        "forbids": [
          "present:sliding-tray"
        ],
        "adds": [
          "present:sliding-tray"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "sliding-tray",
          "visible": true
        }
      },
      {
        "id": "place:tool-head",
        "label": "安装 tool-head",
        "requires": [
          "present:primary-boom"
        ],
        "forbids": [
          "present:tool-head"
        ],
        "adds": [
          "present:tool-head"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "tool-head",
          "visible": true
        }
      }
    ],
    "goalFacts": [
      "present:foundation",
      "present:mast",
      "present:primary-boom",
      "present:tool-head",
      "present:control-cab",
      "present:service-cartridge",
      "present:secondary-boom",
      "present:clamp",
      "present:sliding-tray",
      "present:track--1",
      "present:track-1"
    ],
    "budget": 11,
    "semantics": "requires must hold; forbids must be absent; effects apply in order; unit action cost"
  },
  "answer": {
    "actionIds": [
      "place:foundation",
      "place:track-1",
      "place:control-cab",
      "place:secondary-boom",
      "place:clamp",
      "place:service-cartridge",
      "place:track--1",
      "place:mast",
      "place:primary-boom",
      "place:sliding-tray",
      "place:tool-head"
    ]
  }
}
```

### 依赖拆解（h3-rotary-excavator-disassembly）

提交 actionIds。执行公开前置条件与效果，达到所有目标且不超过预算；允许交换独立动作。

能力：依赖拆解；形式：actions；证据：state-machine。


```json
{
  "input": {
    "initialFacts": [
      "present:foundation",
      "present:mast",
      "present:primary-boom",
      "present:tool-head",
      "present:control-cab",
      "present:service-cartridge",
      "present:secondary-boom",
      "present:clamp",
      "present:sliding-tray",
      "present:track--1",
      "present:track-1"
    ],
    "initialModules": [
      "foundation",
      "mast",
      "primary-boom",
      "tool-head",
      "control-cab",
      "service-cartridge",
      "secondary-boom",
      "clamp",
      "sliding-tray",
      "track--1",
      "track-1"
    ],
    "actions": [
      {
        "id": "remove:mast",
        "label": "拆除 mast",
        "requires": [
          "present:mast"
        ],
        "forbids": [
          "present:primary-boom"
        ],
        "adds": [
          "removed:mast"
        ],
        "deletes": [
          "present:mast"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "mast",
          "visible": false
        }
      },
      {
        "id": "remove:clamp",
        "label": "拆除 clamp",
        "requires": [
          "present:clamp"
        ],
        "forbids": [],
        "adds": [
          "removed:clamp"
        ],
        "deletes": [
          "present:clamp"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "clamp",
          "visible": false
        }
      },
      {
        "id": "remove:primary-boom",
        "label": "拆除 primary-boom",
        "requires": [
          "present:primary-boom"
        ],
        "forbids": [
          "present:tool-head"
        ],
        "adds": [
          "removed:primary-boom"
        ],
        "deletes": [
          "present:primary-boom"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "primary-boom",
          "visible": false
        }
      },
      {
        "id": "remove:track-1",
        "label": "拆除 track-1",
        "requires": [
          "present:track-1"
        ],
        "forbids": [],
        "adds": [
          "removed:track-1"
        ],
        "deletes": [
          "present:track-1"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "track-1",
          "visible": false
        }
      },
      {
        "id": "remove:secondary-boom",
        "label": "拆除 secondary-boom",
        "requires": [
          "present:secondary-boom"
        ],
        "forbids": [
          "present:clamp"
        ],
        "adds": [
          "removed:secondary-boom"
        ],
        "deletes": [
          "present:secondary-boom"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "secondary-boom",
          "visible": false
        }
      },
      {
        "id": "remove:track--1",
        "label": "拆除 track--1",
        "requires": [
          "present:track--1"
        ],
        "forbids": [],
        "adds": [
          "removed:track--1"
        ],
        "deletes": [
          "present:track--1"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "track--1",
          "visible": false
        }
      },
      {
        "id": "remove:control-cab",
        "label": "拆除 control-cab",
        "requires": [
          "present:control-cab"
        ],
        "forbids": [
          "present:secondary-boom"
        ],
        "adds": [
          "removed:control-cab"
        ],
        "deletes": [
          "present:control-cab"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "control-cab",
          "visible": false
        }
      },
      {
        "id": "remove:tool-head",
        "label": "拆除 tool-head",
        "requires": [
          "present:tool-head"
        ],
        "forbids": [],
        "adds": [
          "removed:tool-head"
        ],
        "deletes": [
          "present:tool-head"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "tool-head",
          "visible": false
        }
      },
      {
        "id": "remove:sliding-tray",
        "label": "拆除 sliding-tray",
        "requires": [
          "present:sliding-tray"
        ],
        "forbids": [],
        "adds": [
          "removed:sliding-tray"
        ],
        "deletes": [
          "present:sliding-tray"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "sliding-tray",
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
          "present:mast",
          "present:control-cab",
          "present:service-cartridge",
          "present:sliding-tray",
          "present:track--1",
          "present:track-1"
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
        "id": "remove:service-cartridge",
        "label": "拆除 service-cartridge",
        "requires": [
          "present:service-cartridge"
        ],
        "forbids": [],
        "adds": [
          "removed:service-cartridge"
        ],
        "deletes": [
          "present:service-cartridge"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "service-cartridge",
          "visible": false
        }
      }
    ],
    "goalFacts": [
      "removed:track-1",
      "removed:track--1",
      "removed:sliding-tray",
      "removed:clamp",
      "removed:secondary-boom",
      "removed:service-cartridge",
      "removed:control-cab",
      "removed:tool-head",
      "removed:primary-boom",
      "removed:mast",
      "removed:foundation"
    ],
    "budget": 11,
    "semantics": "requires must hold; forbids must be absent; effects apply in order; unit action cost"
  },
  "answer": {
    "actionIds": [
      "remove:clamp",
      "remove:track-1",
      "remove:secondary-boom",
      "remove:track--1",
      "remove:control-cab",
      "remove:tool-head",
      "remove:primary-boom",
      "remove:mast",
      "remove:sliding-tray",
      "remove:service-cartridge",
      "remove:foundation"
    ]
  }
}
```

### 承载维修（h3-rotary-excavator-service-repair）

提交 actionIds。执行公开前置条件与效果，达到所有目标且不超过预算；允许交换独立动作。

能力：承载维修；形式：actions；证据：state-machine。


```json
{
  "input": {
    "initialFacts": [
      "fault:service-cartridge",
      "closed:service-cartridge"
    ],
    "initialModules": [
      "foundation",
      "mast",
      "primary-boom",
      "tool-head",
      "control-cab",
      "service-cartridge",
      "secondary-boom",
      "clamp",
      "sliding-tray",
      "track--1",
      "track-1"
    ],
    "actions": [
      {
        "id": "open:service-cartridge",
        "label": "open service-cartridge",
        "requires": [
          "done:support:service-cartridge"
        ],
        "forbids": [
          "done:open:service-cartridge"
        ],
        "adds": [
          "done:open:service-cartridge"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "service-cartridge"
        }
      },
      {
        "id": "verify:service-cartridge",
        "label": "verify service-cartridge",
        "requires": [
          "done:replace:service-cartridge"
        ],
        "forbids": [
          "done:verify:service-cartridge"
        ],
        "adds": [
          "done:verify:service-cartridge"
        ],
        "deletes": [
          "fault:service-cartridge"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "service-cartridge"
        }
      },
      {
        "id": "close:service-cartridge",
        "label": "close service-cartridge",
        "requires": [
          "done:verify:service-cartridge"
        ],
        "forbids": [
          "done:close:service-cartridge"
        ],
        "adds": [
          "done:close:service-cartridge"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "service-cartridge"
        }
      },
      {
        "id": "release:service-cartridge",
        "label": "release service-cartridge",
        "requires": [
          "done:close:service-cartridge"
        ],
        "forbids": [
          "done:release:service-cartridge"
        ],
        "adds": [
          "done:release:service-cartridge",
          "repaired:service-cartridge"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "service-cartridge"
        }
      },
      {
        "id": "remove:service-cartridge",
        "label": "remove service-cartridge",
        "requires": [
          "done:open:service-cartridge"
        ],
        "forbids": [
          "done:remove:service-cartridge"
        ],
        "adds": [
          "done:remove:service-cartridge"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "service-cartridge",
          "visible": false
        }
      },
      {
        "id": "replace:service-cartridge",
        "label": "replace service-cartridge",
        "requires": [
          "done:remove:service-cartridge"
        ],
        "forbids": [
          "done:replace:service-cartridge"
        ],
        "adds": [
          "done:replace:service-cartridge"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "service-cartridge",
          "visible": true
        }
      },
      {
        "id": "support:service-cartridge",
        "label": "support service-cartridge",
        "requires": [
          "fault:service-cartridge"
        ],
        "forbids": [
          "done:support:service-cartridge"
        ],
        "adds": [
          "done:support:service-cartridge"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "service-cartridge"
        }
      }
    ],
    "goalFacts": [
      "repaired:service-cartridge"
    ],
    "budget": 7,
    "semantics": "requires must hold; forbids must be absent; effects apply in order; unit action cost"
  },
  "answer": {
    "actionIds": [
      "support:service-cartridge",
      "open:service-cartridge",
      "remove:service-cartridge",
      "replace:service-cartridge",
      "verify:service-cartridge",
      "close:service-cartridge",
      "release:service-cartridge"
    ]
  }
}
```

### 复合编辑验证（h3-rotary-excavator-compound-edit）

提交 actionIds。执行公开前置条件与效果，达到所有目标且不超过预算；允许交换独立动作。

能力：复合编辑验证；形式：actions；证据：state-machine。


```json
{
  "input": {
    "initialFacts": [
      "fault:service-cartridge",
      "closed:service-cartridge"
    ],
    "initialModules": [
      "foundation",
      "mast",
      "primary-boom",
      "tool-head",
      "control-cab",
      "service-cartridge",
      "secondary-boom",
      "clamp",
      "sliding-tray",
      "track--1",
      "track-1"
    ],
    "actions": [
      {
        "id": "open:service-cartridge",
        "label": "open service-cartridge",
        "requires": [
          "done:support:service-cartridge"
        ],
        "forbids": [
          "done:open:service-cartridge"
        ],
        "adds": [
          "done:open:service-cartridge"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "service-cartridge"
        }
      },
      {
        "id": "verify:service-cartridge",
        "label": "verify service-cartridge",
        "requires": [
          "done:recolor:service-cartridge"
        ],
        "forbids": [
          "done:verify:service-cartridge"
        ],
        "adds": [
          "done:verify:service-cartridge"
        ],
        "deletes": [
          "fault:service-cartridge"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "service-cartridge"
        }
      },
      {
        "id": "recolor:service-cartridge",
        "label": "recolor service-cartridge",
        "requires": [
          "done:open:service-cartridge"
        ],
        "forbids": [
          "done:recolor:service-cartridge"
        ],
        "adds": [
          "done:recolor:service-cartridge"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "service-cartridge",
          "color": "#ea7635"
        }
      },
      {
        "id": "close:service-cartridge",
        "label": "close service-cartridge",
        "requires": [
          "done:verify:service-cartridge"
        ],
        "forbids": [
          "done:close:service-cartridge"
        ],
        "adds": [
          "done:close:service-cartridge"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "service-cartridge"
        }
      },
      {
        "id": "release:service-cartridge",
        "label": "release service-cartridge",
        "requires": [
          "done:close:service-cartridge"
        ],
        "forbids": [
          "done:release:service-cartridge"
        ],
        "adds": [
          "done:release:service-cartridge",
          "repaired:service-cartridge"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "service-cartridge"
        }
      },
      {
        "id": "support:service-cartridge",
        "label": "support service-cartridge",
        "requires": [
          "fault:service-cartridge"
        ],
        "forbids": [
          "done:support:service-cartridge"
        ],
        "adds": [
          "done:support:service-cartridge"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "service-cartridge"
        }
      }
    ],
    "goalFacts": [
      "repaired:service-cartridge"
    ],
    "budget": 6,
    "semantics": "requires must hold; forbids must be absent; effects apply in order; unit action cost"
  },
  "answer": {
    "actionIds": [
      "support:service-cartridge",
      "open:service-cartridge",
      "recolor:service-cartridge",
      "verify:service-cartridge",
      "close:service-cartridge",
      "release:service-cartridge"
    ]
  }
}
```

### 跨区域联合维修（h3-rotary-excavator-multi-fault）

提交 actionIds。执行公开前置条件与效果，达到所有目标且不超过预算；允许交换独立动作。

能力：跨区域联合维修；形式：actions；证据：state-machine。


```json
{
  "input": {
    "initialFacts": [
      "fault:sliding-tray",
      "closed:sliding-tray",
      "fault:track--1",
      "closed:track--1",
      "fault:track-1",
      "closed:track-1"
    ],
    "initialModules": [
      "foundation",
      "mast",
      "primary-boom",
      "tool-head",
      "control-cab",
      "service-cartridge",
      "secondary-boom",
      "clamp",
      "sliding-tray",
      "track--1",
      "track-1"
    ],
    "actions": [
      {
        "id": "replace:track-1",
        "label": "replace track-1",
        "requires": [
          "done:remove:track-1"
        ],
        "forbids": [
          "done:replace:track-1"
        ],
        "adds": [
          "done:replace:track-1"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "track-1",
          "visible": true
        }
      },
      {
        "id": "open:track-1",
        "label": "open track-1",
        "requires": [
          "done:support:track-1"
        ],
        "forbids": [
          "done:open:track-1"
        ],
        "adds": [
          "done:open:track-1"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "track-1"
        }
      },
      {
        "id": "remove:track-1",
        "label": "remove track-1",
        "requires": [
          "done:open:track-1"
        ],
        "forbids": [
          "done:remove:track-1"
        ],
        "adds": [
          "done:remove:track-1"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "track-1",
          "visible": false
        }
      },
      {
        "id": "verify:track--1",
        "label": "verify track--1",
        "requires": [
          "done:replace:track--1"
        ],
        "forbids": [
          "done:verify:track--1"
        ],
        "adds": [
          "done:verify:track--1"
        ],
        "deletes": [
          "fault:track--1"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "track--1"
        }
      },
      {
        "id": "release:track--1",
        "label": "release track--1",
        "requires": [
          "done:close:track--1"
        ],
        "forbids": [
          "done:release:track--1"
        ],
        "adds": [
          "done:release:track--1",
          "repaired:track--1"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "track--1"
        }
      },
      {
        "id": "support:sliding-tray",
        "label": "support sliding-tray",
        "requires": [
          "fault:sliding-tray"
        ],
        "forbids": [
          "done:support:sliding-tray"
        ],
        "adds": [
          "done:support:sliding-tray"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "sliding-tray"
        }
      },
      {
        "id": "verify:track-1",
        "label": "verify track-1",
        "requires": [
          "done:replace:track-1"
        ],
        "forbids": [
          "done:verify:track-1"
        ],
        "adds": [
          "done:verify:track-1"
        ],
        "deletes": [
          "fault:track-1"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "track-1"
        }
      },
      {
        "id": "remove:track--1",
        "label": "remove track--1",
        "requires": [
          "done:open:track--1"
        ],
        "forbids": [
          "done:remove:track--1"
        ],
        "adds": [
          "done:remove:track--1"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "track--1",
          "visible": false
        }
      },
      {
        "id": "release:sliding-tray",
        "label": "release sliding-tray",
        "requires": [
          "done:close:sliding-tray"
        ],
        "forbids": [
          "done:release:sliding-tray"
        ],
        "adds": [
          "done:release:sliding-tray",
          "repaired:sliding-tray"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "sliding-tray"
        }
      },
      {
        "id": "verify:sliding-tray",
        "label": "verify sliding-tray",
        "requires": [
          "done:replace:sliding-tray"
        ],
        "forbids": [
          "done:verify:sliding-tray"
        ],
        "adds": [
          "done:verify:sliding-tray"
        ],
        "deletes": [
          "fault:sliding-tray"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "sliding-tray"
        }
      },
      {
        "id": "release:track-1",
        "label": "release track-1",
        "requires": [
          "done:close:track-1"
        ],
        "forbids": [
          "done:release:track-1"
        ],
        "adds": [
          "done:release:track-1",
          "repaired:track-1"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "track-1"
        }
      },
      {
        "id": "close:track--1",
        "label": "close track--1",
        "requires": [
          "done:verify:track--1"
        ],
        "forbids": [
          "done:close:track--1"
        ],
        "adds": [
          "done:close:track--1"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "track--1"
        }
      },
      {
        "id": "replace:track--1",
        "label": "replace track--1",
        "requires": [
          "done:remove:track--1"
        ],
        "forbids": [
          "done:replace:track--1"
        ],
        "adds": [
          "done:replace:track--1"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "track--1",
          "visible": true
        }
      },
      {
        "id": "remove:sliding-tray",
        "label": "remove sliding-tray",
        "requires": [
          "done:open:sliding-tray"
        ],
        "forbids": [
          "done:remove:sliding-tray"
        ],
        "adds": [
          "done:remove:sliding-tray"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "sliding-tray",
          "visible": false
        }
      },
      {
        "id": "support:track-1",
        "label": "support track-1",
        "requires": [
          "fault:track-1"
        ],
        "forbids": [
          "done:support:track-1"
        ],
        "adds": [
          "done:support:track-1"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "track-1"
        }
      },
      {
        "id": "replace:sliding-tray",
        "label": "replace sliding-tray",
        "requires": [
          "done:remove:sliding-tray"
        ],
        "forbids": [
          "done:replace:sliding-tray"
        ],
        "adds": [
          "done:replace:sliding-tray"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "sliding-tray",
          "visible": true
        }
      },
      {
        "id": "open:track--1",
        "label": "open track--1",
        "requires": [
          "done:support:track--1"
        ],
        "forbids": [
          "done:open:track--1"
        ],
        "adds": [
          "done:open:track--1"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "track--1"
        }
      },
      {
        "id": "open:sliding-tray",
        "label": "open sliding-tray",
        "requires": [
          "done:support:sliding-tray"
        ],
        "forbids": [
          "done:open:sliding-tray"
        ],
        "adds": [
          "done:open:sliding-tray"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "sliding-tray"
        }
      },
      {
        "id": "close:track-1",
        "label": "close track-1",
        "requires": [
          "done:verify:track-1"
        ],
        "forbids": [
          "done:close:track-1"
        ],
        "adds": [
          "done:close:track-1"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "track-1"
        }
      },
      {
        "id": "support:track--1",
        "label": "support track--1",
        "requires": [
          "fault:track--1"
        ],
        "forbids": [
          "done:support:track--1"
        ],
        "adds": [
          "done:support:track--1"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "track--1"
        }
      },
      {
        "id": "close:sliding-tray",
        "label": "close sliding-tray",
        "requires": [
          "done:verify:sliding-tray"
        ],
        "forbids": [
          "done:close:sliding-tray"
        ],
        "adds": [
          "done:close:sliding-tray"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "sliding-tray"
        }
      }
    ],
    "goalFacts": [
      "repaired:sliding-tray",
      "repaired:track--1",
      "repaired:track-1"
    ],
    "budget": 21,
    "semantics": "requires must hold; forbids must be absent; effects apply in order; unit action cost"
  },
  "answer": {
    "actionIds": [
      "support:sliding-tray",
      "support:track-1",
      "open:track-1",
      "remove:track-1",
      "replace:track-1",
      "verify:track-1",
      "open:sliding-tray",
      "remove:sliding-tray",
      "replace:sliding-tray",
      "verify:sliding-tray",
      "close:track-1",
      "release:track-1",
      "support:track--1",
      "open:track--1",
      "remove:track--1",
      "replace:track--1",
      "verify:track--1",
      "close:track--1",
      "release:track--1",
      "close:sliding-tray",
      "release:sliding-tray"
    ]
  }
}
```

### 多工位资源调度（h3-rotary-excavator-scheduling）

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
        "module": "mast",
        "duration": 3,
        "resource": "technician",
        "after": []
      },
      {
        "id": "job-2",
        "module": "primary-boom",
        "duration": 3,
        "resource": "test-bench",
        "after": [
          "job-0"
        ]
      },
      {
        "id": "job-3",
        "module": "tool-head",
        "duration": 3,
        "resource": "technician",
        "after": [
          "job-1"
        ]
      },
      {
        "id": "job-4",
        "module": "control-cab",
        "duration": 3,
        "resource": "test-bench",
        "after": [
          "job-2"
        ]
      },
      {
        "id": "job-5",
        "module": "service-cartridge",
        "duration": 3,
        "resource": "technician",
        "after": [
          "job-3"
        ]
      },
      {
        "id": "job-6",
        "module": "secondary-boom",
        "duration": 1,
        "resource": "test-bench",
        "after": [
          "job-4"
        ]
      },
      {
        "id": "job-7",
        "module": "clamp",
        "duration": 1,
        "resource": "technician",
        "after": [
          "job-5"
        ]
      }
    ],
    "deadline": 10
  },
  "answer": {
    "starts": {
      "job-0": 0,
      "job-1": 0,
      "job-2": 1,
      "job-3": 3,
      "job-4": 4,
      "job-5": 6,
      "job-6": 7,
      "job-7": 9
    }
  }
}
```

### 检查后条件策略（h3-rotary-excavator-policy）

提交一个检查及 observation→action 决策表，在所有相容世界中采取正确动作。

能力：检查后条件策略；形式：policy；证据：finite-world。


```json
{
  "input": {
    "module": "service-cartridge",
    "worlds": [
      {
        "id": "normal",
        "action": "continue"
      },
      {
        "id": "loose",
        "action": "tighten"
      },
      {
        "id": "jammed",
        "action": "replace"
      }
    ],
    "budget": 1,
    "queries": [
      {
        "id": "visual",
        "cost": 1,
        "returns": {
          "normal": "signal-0",
          "loose": "signal-1",
          "jammed": "signal-2"
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
          "normal": "same",
          "loose": "same",
          "jammed": "other"
        }
      }
    ]
  },
  "answer": {
    "queryId": "visual",
    "decisions": {
      "signal-0": "continue",
      "signal-1": "tighten",
      "signal-2": "replace"
    }
  }
}
```

### 局部坐标变换（h3-rotary-excavator-local-frame）

将模块局部点通过给定四元数与平移转换为世界点，保留五位小数。

能力：局部坐标变换；形式：single-choice；证据：model-state。

- A：[2.5,0.8,-2.5]
- B：[0.5,-0.05,-0.5]
- C：[3.5,1.8,-1.5]

```json
{
  "input": {
    "localPoint": [
      0.5,
      -0.04999999999999999,
      -0.5
    ],
    "rotationXYZW": [
      0,
      0,
      0,
      1
    ],
    "translation": [
      2,
      0.8500000000000001,
      -2
    ]
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 正交视图投影（h3-rotary-excavator-projection）

按公开视图坐标约定，选择该世界点投影后的二维坐标。

能力：正交视图投影；形式：single-choice；证据：model-state。

- A：[4,9]
- B：[9,4]
- C：[4,5]
- D：[0,0]

```json
{
  "input": {
    "view": "front",
    "point": [
      4,
      9,
      -5
    ],
    "convention": "front=(x,y), side=(z,y), top=(x,z)"
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 空间相对关系（h3-rotary-excavator-relative-order）

比较B相对A在指定世界轴上的模块原点坐标。

能力：空间相对关系；形式：single-choice；证据：model-state。

- A：equal
- B：less
- C：greater

```json
{
  "input": {
    "A": {
      "id": "foundation",
      "position": [
        0,
        0.35,
        0
      ]
    },
    "B": {
      "id": "track-1",
      "position": [
        -0.050000000000000266,
        0.7,
        4
      ]
    },
    "axis": "x"
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 约束自由度（h3-rotary-excavator-joint-axis）

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
      "id": "mast-joint",
      "name": "mast interface",
      "parent": "foundation",
      "child": "mast",
      "type": "fixed",
      "anchorParent": [
        -1.6,
        0.55,
        -0.6
      ],
      "anchorChild": [
        0,
        -2.45,
        0
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

### 维修间隙预算（h3-rotary-excavator-clearance-margin）

给定理想直槽净宽、工具宽度、单侧安全余量，工具是否满足横向间隙要求？

能力：维修间隙预算；形式：single-choice；证据：model-state。

- A：blocked
- B：feasible

```json
{
  "input": {
    "module": "service-cartridge",
    "aperture": 0.52,
    "toolWidth": 0.55,
    "eachSideMargin": 0
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 载荷力矩（h3-rotary-excavator-load-moment）

绕给定原点的载荷力矩r×F是多少？采用右手系，忽略其他力。

能力：载荷力矩；形式：single-choice；证据：model-state。

- A：[0,0,0]
- B：[0,-3,0]
- C：[0,0,-6]
- D：[0,0,6]

```json
{
  "input": {
    "module": "service-cartridge",
    "lever": [
      3,
      1,
      0
    ],
    "force": [
      0,
      -2,
      0
    ],
    "units": "scene-length × force"
  },
  "answer": {
    "choiceId": "C"
  }
}
```

### 非均匀先验更新（h3-rotary-excavator-weighted-posterior）

先验权重未归一化，观测只保留normal和jammed，求jammed后验概率。

能力：非均匀先验更新；形式：single-choice；证据：finite-world。

- A：0.5
- B：0.16666666666666666
- C：0
- D：1

```json
{
  "input": {
    "module": "service-cartridge",
    "worlds": [
      "normal",
      "jammed",
      "loose"
    ],
    "weights": [
      1,
      1,
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

### 风险最小决策（h3-rotary-excavator-expected-loss）

继续运行期望损失=p×failureLoss，预防维修损失=repairCost，选择损失较低者；并列选继续。

能力：风险最小决策；形式：single-choice；证据：finite-world。

- A：repair
- B：continue

```json
{
  "input": {
    "faultProbability": 0.5,
    "repairCost": 4,
    "failureLoss": 13,
    "module": "service-cartridge"
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 轨迹阈值判定（h3-rotary-excavator-trace-threshold）

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
        "displacement": 0.00559594674894626
      },
      {
        "time": 0.10833333333333334,
        "displacement": 0.007276417923634616
      },
      {
        "time": 0.20833333333333334,
        "displacement": 0.005770755192200806
      },
      {
        "time": 0.30833333333333335,
        "displacement": 0.002118215492300024
      },
      {
        "time": 0.4083333333333333,
        "displacement": 0.00018572911562461764
      },
      {
        "time": 0.5083333333333333,
        "displacement": 0.0003473260439354856
      },
      {
        "time": 0.6083333333333333,
        "displacement": 0.00022248000358433823
      },
      {
        "time": 0.7083333333333334,
        "displacement": 0.00009502423642286626
      },
      {
        "time": 0.8083333333333333,
        "displacement": 0.000021523219896656582
      },
      {
        "time": 0.9083333333333333,
        "displacement": 0.0000018706744702428838
      },
      {
        "time": 1,
        "displacement": 0.0000018706744702428838
      }
    ],
    "threshold": 0.005821134338907693
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 安全联锁维修（h3-rotary-excavator-guarded-repair）

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
        "id": "release:service-cartridge",
        "label": "release service-cartridge",
        "requires": [
          "done:relock:service-cartridge"
        ],
        "forbids": [
          "done:release:service-cartridge"
        ],
        "adds": [
          "done:release:service-cartridge",
          "ready:service-cartridge",
          "tool:free"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "service-cartridge"
        }
      },
      {
        "id": "relock:service-cartridge",
        "label": "relock service-cartridge",
        "requires": [
          "done:verify:service-cartridge"
        ],
        "forbids": [
          "done:relock:service-cartridge"
        ],
        "adds": [
          "done:relock:service-cartridge"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "service-cartridge"
        }
      },
      {
        "id": "verify:service-cartridge",
        "label": "verify service-cartridge",
        "requires": [
          "done:replace:service-cartridge"
        ],
        "forbids": [
          "done:verify:service-cartridge"
        ],
        "adds": [
          "done:verify:service-cartridge"
        ],
        "deletes": [
          "fault:service-cartridge",
          "misaligned:service-cartridge"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "service-cartridge"
        }
      },
      {
        "id": "replace:service-cartridge",
        "label": "replace service-cartridge",
        "requires": [
          "done:unlock:service-cartridge"
        ],
        "forbids": [
          "done:replace:service-cartridge"
        ],
        "adds": [
          "done:replace:service-cartridge"
        ],
        "deletes": [],
        "cost": 2,
        "visual": {
          "moduleId": "service-cartridge"
        }
      },
      {
        "id": "unlock:service-cartridge",
        "label": "unlock service-cartridge",
        "requires": [
          "done:support:service-cartridge"
        ],
        "forbids": [
          "done:unlock:service-cartridge"
        ],
        "adds": [
          "done:unlock:service-cartridge"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "service-cartridge"
        }
      },
      {
        "id": "support:service-cartridge",
        "label": "support service-cartridge",
        "requires": [
          "done:isolate:service-cartridge"
        ],
        "forbids": [
          "done:support:service-cartridge"
        ],
        "adds": [
          "done:support:service-cartridge"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "service-cartridge"
        }
      },
      {
        "id": "isolate:service-cartridge",
        "label": "isolate service-cartridge",
        "requires": [
          "tool:free",
          "fault:service-cartridge"
        ],
        "forbids": [
          "done:isolate:service-cartridge"
        ],
        "adds": [
          "done:isolate:service-cartridge"
        ],
        "deletes": [
          "tool:free"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "service-cartridge"
        }
      }
    ],
    "initialFacts": [
      "tool:free",
      "fault:service-cartridge"
    ],
    "initialModules": [
      "foundation",
      "mast",
      "primary-boom",
      "tool-head",
      "control-cab",
      "service-cartridge",
      "secondary-boom",
      "clamp",
      "sliding-tray",
      "track--1",
      "track-1"
    ],
    "goalFacts": [
      "ready:service-cartridge"
    ],
    "absentFacts": [
      "unverified"
    ],
    "budget": 8
  },
  "answer": {
    "actionIds": [
      "isolate:service-cartridge",
      "support:service-cartridge",
      "unlock:service-cartridge",
      "replace:service-cartridge",
      "verify:service-cartridge",
      "relock:service-cartridge",
      "release:service-cartridge"
    ]
  }
}
```

### 失败状态回退（h3-rotary-excavator-rollback）

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
        "id": "resume:service-cartridge",
        "label": "resume service-cartridge",
        "requires": [
          "done:verify:service-cartridge"
        ],
        "forbids": [
          "done:resume:service-cartridge"
        ],
        "adds": [
          "done:resume:service-cartridge",
          "ready:service-cartridge",
          "tool:free"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "service-cartridge"
        }
      },
      {
        "id": "verify:service-cartridge",
        "label": "verify service-cartridge",
        "requires": [
          "done:align:service-cartridge"
        ],
        "forbids": [
          "done:verify:service-cartridge"
        ],
        "adds": [
          "done:verify:service-cartridge"
        ],
        "deletes": [
          "fault:service-cartridge",
          "misaligned:service-cartridge"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "service-cartridge"
        }
      },
      {
        "id": "align:service-cartridge",
        "label": "align service-cartridge",
        "requires": [
          "done:undo:service-cartridge"
        ],
        "forbids": [
          "done:align:service-cartridge"
        ],
        "adds": [
          "done:align:service-cartridge"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "service-cartridge",
          "visible": true
        }
      },
      {
        "id": "undo:service-cartridge",
        "label": "undo service-cartridge",
        "requires": [
          "done:isolate:service-cartridge"
        ],
        "forbids": [
          "done:undo:service-cartridge"
        ],
        "adds": [
          "done:undo:service-cartridge"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "service-cartridge",
          "visible": false
        }
      },
      {
        "id": "isolate:service-cartridge",
        "label": "isolate service-cartridge",
        "requires": [
          "tool:free",
          "fault:service-cartridge"
        ],
        "forbids": [
          "done:isolate:service-cartridge"
        ],
        "adds": [
          "done:isolate:service-cartridge"
        ],
        "deletes": [
          "tool:free"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "service-cartridge"
        }
      }
    ],
    "initialFacts": [
      "tool:free",
      "fault:service-cartridge",
      "misaligned:service-cartridge"
    ],
    "initialModules": [
      "foundation",
      "mast",
      "primary-boom",
      "tool-head",
      "control-cab",
      "service-cartridge",
      "secondary-boom",
      "clamp",
      "sliding-tray",
      "track--1",
      "track-1"
    ],
    "goalFacts": [
      "ready:service-cartridge"
    ],
    "absentFacts": [
      "unverified"
    ],
    "budget": 5
  },
  "answer": {
    "actionIds": [
      "isolate:service-cartridge",
      "undo:service-cartridge",
      "align:service-cartridge",
      "verify:service-cartridge",
      "resume:service-cartridge"
    ]
  }
}
```

### 共享工具协同维修（h3-rotary-excavator-resource-repair）

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
        "id": "release:track-1",
        "label": "release track-1",
        "requires": [
          "done:relock:track-1"
        ],
        "forbids": [
          "done:release:track-1"
        ],
        "adds": [
          "done:release:track-1",
          "ready:track-1",
          "tool:free"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "track-1"
        }
      },
      {
        "id": "relock:track-1",
        "label": "relock track-1",
        "requires": [
          "done:verify:track-1"
        ],
        "forbids": [
          "done:relock:track-1"
        ],
        "adds": [
          "done:relock:track-1"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "track-1"
        }
      },
      {
        "id": "verify:track-1",
        "label": "verify track-1",
        "requires": [
          "done:replace:track-1"
        ],
        "forbids": [
          "done:verify:track-1"
        ],
        "adds": [
          "done:verify:track-1"
        ],
        "deletes": [
          "fault:track-1",
          "misaligned:track-1"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "track-1"
        }
      },
      {
        "id": "replace:track-1",
        "label": "replace track-1",
        "requires": [
          "done:unlock:track-1"
        ],
        "forbids": [
          "done:replace:track-1"
        ],
        "adds": [
          "done:replace:track-1"
        ],
        "deletes": [],
        "cost": 2,
        "visual": {
          "moduleId": "track-1"
        }
      },
      {
        "id": "unlock:track-1",
        "label": "unlock track-1",
        "requires": [
          "done:support:track-1"
        ],
        "forbids": [
          "done:unlock:track-1"
        ],
        "adds": [
          "done:unlock:track-1"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "track-1"
        }
      },
      {
        "id": "support:track-1",
        "label": "support track-1",
        "requires": [
          "done:isolate:track-1"
        ],
        "forbids": [
          "done:support:track-1"
        ],
        "adds": [
          "done:support:track-1"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "track-1"
        }
      },
      {
        "id": "isolate:track-1",
        "label": "isolate track-1",
        "requires": [
          "tool:free",
          "fault:track-1"
        ],
        "forbids": [
          "done:isolate:track-1"
        ],
        "adds": [
          "done:isolate:track-1"
        ],
        "deletes": [
          "tool:free"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "track-1"
        }
      },
      {
        "id": "release:track--1",
        "label": "release track--1",
        "requires": [
          "done:relock:track--1"
        ],
        "forbids": [
          "done:release:track--1"
        ],
        "adds": [
          "done:release:track--1",
          "ready:track--1",
          "tool:free"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "track--1"
        }
      },
      {
        "id": "relock:track--1",
        "label": "relock track--1",
        "requires": [
          "done:verify:track--1"
        ],
        "forbids": [
          "done:relock:track--1"
        ],
        "adds": [
          "done:relock:track--1"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "track--1"
        }
      },
      {
        "id": "verify:track--1",
        "label": "verify track--1",
        "requires": [
          "done:replace:track--1"
        ],
        "forbids": [
          "done:verify:track--1"
        ],
        "adds": [
          "done:verify:track--1"
        ],
        "deletes": [
          "fault:track--1",
          "misaligned:track--1"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "track--1"
        }
      },
      {
        "id": "replace:track--1",
        "label": "replace track--1",
        "requires": [
          "done:unlock:track--1"
        ],
        "forbids": [
          "done:replace:track--1"
        ],
        "adds": [
          "done:replace:track--1"
        ],
        "deletes": [],
        "cost": 2,
        "visual": {
          "moduleId": "track--1"
        }
      },
      {
        "id": "unlock:track--1",
        "label": "unlock track--1",
        "requires": [
          "done:support:track--1"
        ],
        "forbids": [
          "done:unlock:track--1"
        ],
        "adds": [
          "done:unlock:track--1"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "track--1"
        }
      },
      {
        "id": "support:track--1",
        "label": "support track--1",
        "requires": [
          "done:isolate:track--1"
        ],
        "forbids": [
          "done:support:track--1"
        ],
        "adds": [
          "done:support:track--1"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "track--1"
        }
      },
      {
        "id": "isolate:track--1",
        "label": "isolate track--1",
        "requires": [
          "tool:free",
          "fault:track--1"
        ],
        "forbids": [
          "done:isolate:track--1"
        ],
        "adds": [
          "done:isolate:track--1"
        ],
        "deletes": [
          "tool:free"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "track--1"
        }
      },
      {
        "id": "release:sliding-tray",
        "label": "release sliding-tray",
        "requires": [
          "done:relock:sliding-tray"
        ],
        "forbids": [
          "done:release:sliding-tray"
        ],
        "adds": [
          "done:release:sliding-tray",
          "ready:sliding-tray",
          "tool:free"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "sliding-tray"
        }
      },
      {
        "id": "relock:sliding-tray",
        "label": "relock sliding-tray",
        "requires": [
          "done:verify:sliding-tray"
        ],
        "forbids": [
          "done:relock:sliding-tray"
        ],
        "adds": [
          "done:relock:sliding-tray"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "sliding-tray"
        }
      },
      {
        "id": "verify:sliding-tray",
        "label": "verify sliding-tray",
        "requires": [
          "done:replace:sliding-tray"
        ],
        "forbids": [
          "done:verify:sliding-tray"
        ],
        "adds": [
          "done:verify:sliding-tray"
        ],
        "deletes": [
          "fault:sliding-tray",
          "misaligned:sliding-tray"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "sliding-tray"
        }
      },
      {
        "id": "replace:sliding-tray",
        "label": "replace sliding-tray",
        "requires": [
          "done:unlock:sliding-tray"
        ],
        "forbids": [
          "done:replace:sliding-tray"
        ],
        "adds": [
          "done:replace:sliding-tray"
        ],
        "deletes": [],
        "cost": 2,
        "visual": {
          "moduleId": "sliding-tray"
        }
      },
      {
        "id": "unlock:sliding-tray",
        "label": "unlock sliding-tray",
        "requires": [
          "done:support:sliding-tray"
        ],
        "forbids": [
          "done:unlock:sliding-tray"
        ],
        "adds": [
          "done:unlock:sliding-tray"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "sliding-tray"
        }
      },
      {
        "id": "support:sliding-tray",
        "label": "support sliding-tray",
        "requires": [
          "done:isolate:sliding-tray"
        ],
        "forbids": [
          "done:support:sliding-tray"
        ],
        "adds": [
          "done:support:sliding-tray"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "sliding-tray"
        }
      },
      {
        "id": "isolate:sliding-tray",
        "label": "isolate sliding-tray",
        "requires": [
          "tool:free",
          "fault:sliding-tray"
        ],
        "forbids": [
          "done:isolate:sliding-tray"
        ],
        "adds": [
          "done:isolate:sliding-tray"
        ],
        "deletes": [
          "tool:free"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "sliding-tray"
        }
      },
      {
        "id": "release:clamp",
        "label": "release clamp",
        "requires": [
          "done:relock:clamp"
        ],
        "forbids": [
          "done:release:clamp"
        ],
        "adds": [
          "done:release:clamp",
          "ready:clamp",
          "tool:free"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "clamp"
        }
      },
      {
        "id": "relock:clamp",
        "label": "relock clamp",
        "requires": [
          "done:verify:clamp"
        ],
        "forbids": [
          "done:relock:clamp"
        ],
        "adds": [
          "done:relock:clamp"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "clamp"
        }
      },
      {
        "id": "verify:clamp",
        "label": "verify clamp",
        "requires": [
          "done:replace:clamp"
        ],
        "forbids": [
          "done:verify:clamp"
        ],
        "adds": [
          "done:verify:clamp"
        ],
        "deletes": [
          "fault:clamp",
          "misaligned:clamp"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "clamp"
        }
      },
      {
        "id": "replace:clamp",
        "label": "replace clamp",
        "requires": [
          "done:unlock:clamp"
        ],
        "forbids": [
          "done:replace:clamp"
        ],
        "adds": [
          "done:replace:clamp"
        ],
        "deletes": [],
        "cost": 2,
        "visual": {
          "moduleId": "clamp"
        }
      },
      {
        "id": "unlock:clamp",
        "label": "unlock clamp",
        "requires": [
          "done:support:clamp"
        ],
        "forbids": [
          "done:unlock:clamp"
        ],
        "adds": [
          "done:unlock:clamp"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "clamp"
        }
      },
      {
        "id": "support:clamp",
        "label": "support clamp",
        "requires": [
          "done:isolate:clamp"
        ],
        "forbids": [
          "done:support:clamp"
        ],
        "adds": [
          "done:support:clamp"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "clamp"
        }
      },
      {
        "id": "isolate:clamp",
        "label": "isolate clamp",
        "requires": [
          "tool:free",
          "fault:clamp"
        ],
        "forbids": [
          "done:isolate:clamp"
        ],
        "adds": [
          "done:isolate:clamp"
        ],
        "deletes": [
          "tool:free"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "clamp"
        }
      }
    ],
    "initialFacts": [
      "tool:free",
      "fault:clamp",
      "fault:sliding-tray",
      "fault:track--1",
      "fault:track-1"
    ],
    "initialModules": [
      "foundation",
      "mast",
      "primary-boom",
      "tool-head",
      "control-cab",
      "service-cartridge",
      "secondary-boom",
      "clamp",
      "sliding-tray",
      "track--1",
      "track-1"
    ],
    "goalFacts": [
      "ready:clamp",
      "ready:sliding-tray",
      "ready:track--1",
      "ready:track-1"
    ],
    "absentFacts": [
      "unverified"
    ],
    "budget": 32
  },
  "answer": {
    "actionIds": [
      "isolate:track-1",
      "support:track-1",
      "unlock:track-1",
      "replace:track-1",
      "verify:track-1",
      "relock:track-1",
      "release:track-1",
      "isolate:track--1",
      "support:track--1",
      "unlock:track--1",
      "replace:track--1",
      "verify:track--1",
      "relock:track--1",
      "release:track--1",
      "isolate:sliding-tray",
      "support:sliding-tray",
      "unlock:sliding-tray",
      "replace:sliding-tray",
      "verify:sliding-tray",
      "relock:sliding-tray",
      "release:sliding-tray",
      "isolate:clamp",
      "support:clamp",
      "unlock:clamp",
      "replace:clamp",
      "verify:clamp",
      "relock:clamp",
      "release:clamp"
    ]
  }
}
```

### 预算约束检查策略（h3-rotary-excavator-budget-policy）

提交预算内、对所有相容世界均正确的检查决策表。

能力：预算约束检查策略；形式：policy；证据：finite-world。


```json
{
  "input": {
    "module": "service-cartridge",
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
        "cost": 1,
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
        "cost": 2,
        "returns": {
          "nominal": "pass",
          "fault": "fail"
        }
      }
    ],
    "budget": 1
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

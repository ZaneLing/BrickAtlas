## D4 轨道综合对接场

### 模块识别（h3-orbital-docking-yard-identify）

高亮的维修模块对应哪个 ID？

能力：模块识别；形式：single-choice；证据：model-state。

- A：platform
- B：hub
- C：dock-arm-west
- D：airlock

```json
{
  "input": {
    "moduleNames": [
      {
        "id": "platform",
        "name": "Orbital service platform"
      },
      {
        "id": "hub",
        "name": "Pressurized docking hub"
      },
      {
        "id": "airlock",
        "name": "Service airlock"
      },
      {
        "id": "dock-arm-west",
        "name": "West articulated docking arm"
      },
      {
        "id": "dock-arm-east",
        "name": "East articulated docking arm"
      },
      {
        "id": "solar-west",
        "name": "West solar wing"
      },
      {
        "id": "solar-east",
        "name": "East solar wing"
      },
      {
        "id": "shuttle",
        "name": "Docked transfer shuttle"
      },
      {
        "id": "crane-base",
        "name": "Cargo crane pedestal"
      },
      {
        "id": "crane-boom",
        "name": "Cargo crane boom"
      },
      {
        "id": "cargo-pod",
        "name": "Transfer cargo pod"
      }
    ]
  },
  "answer": {
    "choiceId": "D"
  }
}
```

### 部件计数（h3-orbital-docking-yard-count）

模块 airlock 有多少个可视零件？

能力：部件计数；形式：single-choice；证据：model-state。

- A：9
- B：10
- C：8
- D：12

```json
{
  "input": {
    "parts": [
      {
        "id": "h0001",
        "moduleId": "platform",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0002",
        "moduleId": "platform",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0003",
        "moduleId": "platform",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0004",
        "moduleId": "platform",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0005",
        "moduleId": "platform",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0006",
        "moduleId": "platform",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0007",
        "moduleId": "platform",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0008",
        "moduleId": "platform",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0009",
        "moduleId": "platform",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0010",
        "moduleId": "platform",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0011",
        "moduleId": "platform",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0012",
        "moduleId": "platform",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0013",
        "moduleId": "platform",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0014",
        "moduleId": "platform",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0015",
        "moduleId": "platform",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0016",
        "moduleId": "platform",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0017",
        "moduleId": "platform",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0018",
        "moduleId": "platform",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0019",
        "moduleId": "platform",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0020",
        "moduleId": "platform",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0021",
        "moduleId": "platform",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0022",
        "moduleId": "platform",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0023",
        "moduleId": "platform",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0024",
        "moduleId": "platform",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0025",
        "moduleId": "platform",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0026",
        "moduleId": "platform",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0027",
        "moduleId": "platform",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0028",
        "moduleId": "platform",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0029",
        "moduleId": "platform",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0030",
        "moduleId": "platform",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0031",
        "moduleId": "platform",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0032",
        "moduleId": "platform",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0033",
        "moduleId": "platform",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0034",
        "moduleId": "platform",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0035",
        "moduleId": "platform",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0036",
        "moduleId": "platform",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0037",
        "moduleId": "platform",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0038",
        "moduleId": "platform",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0039",
        "moduleId": "platform",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0040",
        "moduleId": "platform",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0041",
        "moduleId": "platform",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0042",
        "moduleId": "platform",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0043",
        "moduleId": "platform",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0044",
        "moduleId": "platform",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0045",
        "moduleId": "platform",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0046",
        "moduleId": "platform",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0047",
        "moduleId": "platform",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0048",
        "moduleId": "platform",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0049",
        "moduleId": "platform",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0050",
        "moduleId": "platform",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0051",
        "moduleId": "platform",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0052",
        "moduleId": "platform",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0053",
        "moduleId": "platform",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0054",
        "moduleId": "platform",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0055",
        "moduleId": "platform",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0056",
        "moduleId": "platform",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0057",
        "moduleId": "platform",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0058",
        "moduleId": "platform",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0059",
        "moduleId": "platform",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0060",
        "moduleId": "platform",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0061",
        "moduleId": "platform",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0062",
        "moduleId": "platform",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0063",
        "moduleId": "platform",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0064",
        "moduleId": "platform",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0065",
        "moduleId": "platform",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0066",
        "moduleId": "platform",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0067",
        "moduleId": "platform",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0068",
        "moduleId": "platform",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0069",
        "moduleId": "platform",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0070",
        "moduleId": "platform",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0071",
        "moduleId": "platform",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0072",
        "moduleId": "platform",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0073",
        "moduleId": "platform",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0074",
        "moduleId": "platform",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0075",
        "moduleId": "platform",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0076",
        "moduleId": "platform",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0077",
        "moduleId": "platform",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0078",
        "moduleId": "platform",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0079",
        "moduleId": "platform",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0080",
        "moduleId": "platform",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0081",
        "moduleId": "hub",
        "shape": "slope",
        "color": "#edf1f2"
      },
      {
        "id": "h0082",
        "moduleId": "hub",
        "shape": "slope",
        "color": "#edf1f2"
      },
      {
        "id": "h0083",
        "moduleId": "hub",
        "shape": "slope",
        "color": "#edf1f2"
      },
      {
        "id": "h0084",
        "moduleId": "hub",
        "shape": "slope",
        "color": "#edf1f2"
      },
      {
        "id": "h0085",
        "moduleId": "hub",
        "shape": "slope",
        "color": "#edf1f2"
      },
      {
        "id": "h0086",
        "moduleId": "hub",
        "shape": "slope",
        "color": "#edf1f2"
      },
      {
        "id": "h0087",
        "moduleId": "hub",
        "shape": "slope",
        "color": "#edf1f2"
      },
      {
        "id": "h0088",
        "moduleId": "hub",
        "shape": "slope",
        "color": "#edf1f2"
      },
      {
        "id": "h0089",
        "moduleId": "hub",
        "shape": "slope",
        "color": "#edf1f2"
      },
      {
        "id": "h0090",
        "moduleId": "hub",
        "shape": "slope",
        "color": "#edf1f2"
      },
      {
        "id": "h0091",
        "moduleId": "hub",
        "shape": "slope",
        "color": "#edf1f2"
      },
      {
        "id": "h0092",
        "moduleId": "hub",
        "shape": "slope",
        "color": "#edf1f2"
      },
      {
        "id": "h0093",
        "moduleId": "hub",
        "shape": "slope",
        "color": "#edf1f2"
      },
      {
        "id": "h0094",
        "moduleId": "hub",
        "shape": "slope",
        "color": "#edf1f2"
      },
      {
        "id": "h0095",
        "moduleId": "hub",
        "shape": "slope",
        "color": "#edf1f2"
      },
      {
        "id": "h0096",
        "moduleId": "hub",
        "shape": "slope",
        "color": "#edf1f2"
      },
      {
        "id": "h0097",
        "moduleId": "hub",
        "shape": "slope",
        "color": "#edf1f2"
      },
      {
        "id": "h0098",
        "moduleId": "hub",
        "shape": "slope",
        "color": "#edf1f2"
      },
      {
        "id": "h0099",
        "moduleId": "hub",
        "shape": "slope",
        "color": "#edf1f2"
      },
      {
        "id": "h0100",
        "moduleId": "hub",
        "shape": "slope",
        "color": "#edf1f2"
      },
      {
        "id": "h0101",
        "moduleId": "hub",
        "shape": "slope",
        "color": "#edf1f2"
      },
      {
        "id": "h0102",
        "moduleId": "hub",
        "shape": "slope",
        "color": "#edf1f2"
      },
      {
        "id": "h0103",
        "moduleId": "hub",
        "shape": "slope",
        "color": "#edf1f2"
      },
      {
        "id": "h0104",
        "moduleId": "hub",
        "shape": "slope",
        "color": "#edf1f2"
      },
      {
        "id": "h0105",
        "moduleId": "hub",
        "shape": "window",
        "color": "#2878b8"
      },
      {
        "id": "h0106",
        "moduleId": "hub",
        "shape": "window",
        "color": "#2878b8"
      },
      {
        "id": "h0107",
        "moduleId": "hub",
        "shape": "window",
        "color": "#2878b8"
      },
      {
        "id": "h0108",
        "moduleId": "hub",
        "shape": "window",
        "color": "#2878b8"
      },
      {
        "id": "h0109",
        "moduleId": "hub",
        "shape": "window",
        "color": "#2878b8"
      },
      {
        "id": "h0110",
        "moduleId": "hub",
        "shape": "window",
        "color": "#2878b8"
      },
      {
        "id": "h0111",
        "moduleId": "hub",
        "shape": "window",
        "color": "#2878b8"
      },
      {
        "id": "h0112",
        "moduleId": "hub",
        "shape": "window",
        "color": "#2878b8"
      },
      {
        "id": "h0113",
        "moduleId": "hub",
        "shape": "window",
        "color": "#2878b8"
      },
      {
        "id": "h0114",
        "moduleId": "hub",
        "shape": "window",
        "color": "#2878b8"
      },
      {
        "id": "h0115",
        "moduleId": "hub",
        "shape": "window",
        "color": "#2878b8"
      },
      {
        "id": "h0116",
        "moduleId": "hub",
        "shape": "window",
        "color": "#2878b8"
      },
      {
        "id": "h0117",
        "moduleId": "hub",
        "shape": "window",
        "color": "#2878b8"
      },
      {
        "id": "h0118",
        "moduleId": "hub",
        "shape": "window",
        "color": "#2878b8"
      },
      {
        "id": "h0119",
        "moduleId": "hub",
        "shape": "window",
        "color": "#2878b8"
      },
      {
        "id": "h0120",
        "moduleId": "hub",
        "shape": "window",
        "color": "#2878b8"
      },
      {
        "id": "h0121",
        "moduleId": "hub",
        "shape": "cylinder",
        "color": "#edf1f2"
      },
      {
        "id": "h0122",
        "moduleId": "airlock",
        "shape": "plate",
        "color": "#e8792e"
      },
      {
        "id": "h0123",
        "moduleId": "airlock",
        "shape": "plate",
        "color": "#e8792e"
      },
      {
        "id": "h0124",
        "moduleId": "airlock",
        "shape": "plate",
        "color": "#e8792e"
      },
      {
        "id": "h0125",
        "moduleId": "airlock",
        "shape": "plate",
        "color": "#e8792e"
      },
      {
        "id": "h0126",
        "moduleId": "airlock",
        "shape": "plate",
        "color": "#e8792e"
      },
      {
        "id": "h0127",
        "moduleId": "airlock",
        "shape": "plate",
        "color": "#e8792e"
      },
      {
        "id": "h0128",
        "moduleId": "airlock",
        "shape": "plate",
        "color": "#e8792e"
      },
      {
        "id": "h0129",
        "moduleId": "airlock",
        "shape": "plate",
        "color": "#e8792e"
      },
      {
        "id": "h0130",
        "moduleId": "airlock",
        "shape": "plate",
        "color": "#e8792e"
      },
      {
        "id": "h0131",
        "moduleId": "dock-arm-west",
        "shape": "beam",
        "color": "#f2bf3c"
      },
      {
        "id": "h0132",
        "moduleId": "dock-arm-west",
        "shape": "beam",
        "color": "#f2bf3c"
      },
      {
        "id": "h0133",
        "moduleId": "dock-arm-west",
        "shape": "beam",
        "color": "#f2bf3c"
      },
      {
        "id": "h0134",
        "moduleId": "dock-arm-west",
        "shape": "beam",
        "color": "#f2bf3c"
      },
      {
        "id": "h0135",
        "moduleId": "dock-arm-west",
        "shape": "beam",
        "color": "#f2bf3c"
      },
      {
        "id": "h0136",
        "moduleId": "dock-arm-west",
        "shape": "beam",
        "color": "#f2bf3c"
      },
      {
        "id": "h0137",
        "moduleId": "dock-arm-west",
        "shape": "beam",
        "color": "#f2bf3c"
      },
      {
        "id": "h0138",
        "moduleId": "dock-arm-west",
        "shape": "beam",
        "color": "#f2bf3c"
      },
      {
        "id": "h0139",
        "moduleId": "dock-arm-west",
        "shape": "beam",
        "color": "#f2bf3c"
      },
      {
        "id": "h0140",
        "moduleId": "dock-arm-west",
        "shape": "beam",
        "color": "#f2bf3c"
      },
      {
        "id": "h0141",
        "moduleId": "dock-arm-west",
        "shape": "gear",
        "color": "#26323b"
      },
      {
        "id": "h0142",
        "moduleId": "dock-arm-east",
        "shape": "beam",
        "color": "#f2bf3c"
      },
      {
        "id": "h0143",
        "moduleId": "dock-arm-east",
        "shape": "beam",
        "color": "#f2bf3c"
      },
      {
        "id": "h0144",
        "moduleId": "dock-arm-east",
        "shape": "beam",
        "color": "#f2bf3c"
      },
      {
        "id": "h0145",
        "moduleId": "dock-arm-east",
        "shape": "beam",
        "color": "#f2bf3c"
      },
      {
        "id": "h0146",
        "moduleId": "dock-arm-east",
        "shape": "beam",
        "color": "#f2bf3c"
      },
      {
        "id": "h0147",
        "moduleId": "dock-arm-east",
        "shape": "beam",
        "color": "#f2bf3c"
      },
      {
        "id": "h0148",
        "moduleId": "dock-arm-east",
        "shape": "beam",
        "color": "#f2bf3c"
      },
      {
        "id": "h0149",
        "moduleId": "dock-arm-east",
        "shape": "beam",
        "color": "#f2bf3c"
      },
      {
        "id": "h0150",
        "moduleId": "dock-arm-east",
        "shape": "beam",
        "color": "#f2bf3c"
      },
      {
        "id": "h0151",
        "moduleId": "dock-arm-east",
        "shape": "beam",
        "color": "#f2bf3c"
      },
      {
        "id": "h0152",
        "moduleId": "dock-arm-east",
        "shape": "gear",
        "color": "#26323b"
      },
      {
        "id": "h0153",
        "moduleId": "solar-west",
        "shape": "panel",
        "color": "#173b63"
      },
      {
        "id": "h0154",
        "moduleId": "solar-west",
        "shape": "panel",
        "color": "#173b63"
      },
      {
        "id": "h0155",
        "moduleId": "solar-west",
        "shape": "panel",
        "color": "#173b63"
      },
      {
        "id": "h0156",
        "moduleId": "solar-west",
        "shape": "panel",
        "color": "#173b63"
      },
      {
        "id": "h0157",
        "moduleId": "solar-west",
        "shape": "panel",
        "color": "#173b63"
      },
      {
        "id": "h0158",
        "moduleId": "solar-west",
        "shape": "panel",
        "color": "#173b63"
      },
      {
        "id": "h0159",
        "moduleId": "solar-west",
        "shape": "panel",
        "color": "#173b63"
      },
      {
        "id": "h0160",
        "moduleId": "solar-west",
        "shape": "panel",
        "color": "#173b63"
      },
      {
        "id": "h0161",
        "moduleId": "solar-west",
        "shape": "panel",
        "color": "#173b63"
      },
      {
        "id": "h0162",
        "moduleId": "solar-west",
        "shape": "panel",
        "color": "#173b63"
      },
      {
        "id": "h0163",
        "moduleId": "solar-west",
        "shape": "panel",
        "color": "#173b63"
      },
      {
        "id": "h0164",
        "moduleId": "solar-west",
        "shape": "panel",
        "color": "#173b63"
      },
      {
        "id": "h0165",
        "moduleId": "solar-west",
        "shape": "panel",
        "color": "#173b63"
      },
      {
        "id": "h0166",
        "moduleId": "solar-west",
        "shape": "panel",
        "color": "#173b63"
      },
      {
        "id": "h0167",
        "moduleId": "solar-west",
        "shape": "panel",
        "color": "#173b63"
      },
      {
        "id": "h0168",
        "moduleId": "solar-west",
        "shape": "panel",
        "color": "#173b63"
      },
      {
        "id": "h0169",
        "moduleId": "solar-west",
        "shape": "panel",
        "color": "#173b63"
      },
      {
        "id": "h0170",
        "moduleId": "solar-west",
        "shape": "panel",
        "color": "#173b63"
      },
      {
        "id": "h0171",
        "moduleId": "solar-west",
        "shape": "panel",
        "color": "#173b63"
      },
      {
        "id": "h0172",
        "moduleId": "solar-west",
        "shape": "panel",
        "color": "#173b63"
      },
      {
        "id": "h0173",
        "moduleId": "solar-east",
        "shape": "panel",
        "color": "#173b63"
      },
      {
        "id": "h0174",
        "moduleId": "solar-east",
        "shape": "panel",
        "color": "#173b63"
      },
      {
        "id": "h0175",
        "moduleId": "solar-east",
        "shape": "panel",
        "color": "#173b63"
      },
      {
        "id": "h0176",
        "moduleId": "solar-east",
        "shape": "panel",
        "color": "#173b63"
      },
      {
        "id": "h0177",
        "moduleId": "solar-east",
        "shape": "panel",
        "color": "#173b63"
      },
      {
        "id": "h0178",
        "moduleId": "solar-east",
        "shape": "panel",
        "color": "#173b63"
      },
      {
        "id": "h0179",
        "moduleId": "solar-east",
        "shape": "panel",
        "color": "#173b63"
      },
      {
        "id": "h0180",
        "moduleId": "solar-east",
        "shape": "panel",
        "color": "#173b63"
      },
      {
        "id": "h0181",
        "moduleId": "solar-east",
        "shape": "panel",
        "color": "#173b63"
      },
      {
        "id": "h0182",
        "moduleId": "solar-east",
        "shape": "panel",
        "color": "#173b63"
      },
      {
        "id": "h0183",
        "moduleId": "solar-east",
        "shape": "panel",
        "color": "#173b63"
      },
      {
        "id": "h0184",
        "moduleId": "solar-east",
        "shape": "panel",
        "color": "#173b63"
      },
      {
        "id": "h0185",
        "moduleId": "solar-east",
        "shape": "panel",
        "color": "#173b63"
      },
      {
        "id": "h0186",
        "moduleId": "solar-east",
        "shape": "panel",
        "color": "#173b63"
      },
      {
        "id": "h0187",
        "moduleId": "solar-east",
        "shape": "panel",
        "color": "#173b63"
      },
      {
        "id": "h0188",
        "moduleId": "solar-east",
        "shape": "panel",
        "color": "#173b63"
      },
      {
        "id": "h0189",
        "moduleId": "solar-east",
        "shape": "panel",
        "color": "#173b63"
      },
      {
        "id": "h0190",
        "moduleId": "solar-east",
        "shape": "panel",
        "color": "#173b63"
      },
      {
        "id": "h0191",
        "moduleId": "solar-east",
        "shape": "panel",
        "color": "#173b63"
      },
      {
        "id": "h0192",
        "moduleId": "solar-east",
        "shape": "panel",
        "color": "#173b63"
      },
      {
        "id": "h0193",
        "moduleId": "shuttle",
        "shape": "slope",
        "color": "#edf1f2"
      },
      {
        "id": "h0194",
        "moduleId": "shuttle",
        "shape": "slope",
        "color": "#edf1f2"
      },
      {
        "id": "h0195",
        "moduleId": "shuttle",
        "shape": "slope",
        "color": "#edf1f2"
      },
      {
        "id": "h0196",
        "moduleId": "shuttle",
        "shape": "slope",
        "color": "#edf1f2"
      },
      {
        "id": "h0197",
        "moduleId": "shuttle",
        "shape": "slope",
        "color": "#edf1f2"
      },
      {
        "id": "h0198",
        "moduleId": "shuttle",
        "shape": "slope",
        "color": "#edf1f2"
      },
      {
        "id": "h0199",
        "moduleId": "shuttle",
        "shape": "slope",
        "color": "#edf1f2"
      },
      {
        "id": "h0200",
        "moduleId": "shuttle",
        "shape": "slope",
        "color": "#edf1f2"
      },
      {
        "id": "h0201",
        "moduleId": "shuttle",
        "shape": "slope",
        "color": "#edf1f2"
      },
      {
        "id": "h0202",
        "moduleId": "shuttle",
        "shape": "slope",
        "color": "#edf1f2"
      },
      {
        "id": "h0203",
        "moduleId": "shuttle",
        "shape": "slope",
        "color": "#edf1f2"
      },
      {
        "id": "h0204",
        "moduleId": "shuttle",
        "shape": "slope",
        "color": "#edf1f2"
      },
      {
        "id": "h0205",
        "moduleId": "shuttle",
        "shape": "wheel",
        "color": "#101820"
      },
      {
        "id": "h0206",
        "moduleId": "shuttle",
        "shape": "wheel",
        "color": "#101820"
      },
      {
        "id": "h0207",
        "moduleId": "crane-base",
        "shape": "beam",
        "color": "#e8792e"
      },
      {
        "id": "h0208",
        "moduleId": "crane-base",
        "shape": "beam",
        "color": "#e8792e"
      },
      {
        "id": "h0209",
        "moduleId": "crane-base",
        "shape": "beam",
        "color": "#e8792e"
      },
      {
        "id": "h0210",
        "moduleId": "crane-base",
        "shape": "beam",
        "color": "#e8792e"
      },
      {
        "id": "h0211",
        "moduleId": "crane-base",
        "shape": "beam",
        "color": "#e8792e"
      },
      {
        "id": "h0212",
        "moduleId": "crane-base",
        "shape": "beam",
        "color": "#e8792e"
      },
      {
        "id": "h0213",
        "moduleId": "crane-base",
        "shape": "beam",
        "color": "#e8792e"
      },
      {
        "id": "h0214",
        "moduleId": "crane-base",
        "shape": "beam",
        "color": "#e8792e"
      },
      {
        "id": "h0215",
        "moduleId": "crane-boom",
        "shape": "beam",
        "color": "#e8792e"
      },
      {
        "id": "h0216",
        "moduleId": "crane-boom",
        "shape": "beam",
        "color": "#e8792e"
      },
      {
        "id": "h0217",
        "moduleId": "crane-boom",
        "shape": "beam",
        "color": "#e8792e"
      },
      {
        "id": "h0218",
        "moduleId": "crane-boom",
        "shape": "beam",
        "color": "#e8792e"
      },
      {
        "id": "h0219",
        "moduleId": "crane-boom",
        "shape": "beam",
        "color": "#e8792e"
      },
      {
        "id": "h0220",
        "moduleId": "crane-boom",
        "shape": "beam",
        "color": "#e8792e"
      },
      {
        "id": "h0221",
        "moduleId": "crane-boom",
        "shape": "beam",
        "color": "#e8792e"
      },
      {
        "id": "h0222",
        "moduleId": "crane-boom",
        "shape": "beam",
        "color": "#e8792e"
      },
      {
        "id": "h0223",
        "moduleId": "crane-boom",
        "shape": "beam",
        "color": "#e8792e"
      },
      {
        "id": "h0224",
        "moduleId": "crane-boom",
        "shape": "beam",
        "color": "#e8792e"
      },
      {
        "id": "h0225",
        "moduleId": "cargo-pod",
        "shape": "plate",
        "color": "#d43a32"
      },
      {
        "id": "h0226",
        "moduleId": "cargo-pod",
        "shape": "plate",
        "color": "#d43a32"
      },
      {
        "id": "h0227",
        "moduleId": "cargo-pod",
        "shape": "plate",
        "color": "#d43a32"
      },
      {
        "id": "h0228",
        "moduleId": "cargo-pod",
        "shape": "plate",
        "color": "#d43a32"
      },
      {
        "id": "h0229",
        "moduleId": "cargo-pod",
        "shape": "plate",
        "color": "#d43a32"
      },
      {
        "id": "h0230",
        "moduleId": "cargo-pod",
        "shape": "plate",
        "color": "#d43a32"
      },
      {
        "id": "h0231",
        "moduleId": "cargo-pod",
        "shape": "plate",
        "color": "#d43a32"
      },
      {
        "id": "h0232",
        "moduleId": "cargo-pod",
        "shape": "plate",
        "color": "#d43a32"
      },
      {
        "id": "h0233",
        "moduleId": "cargo-pod",
        "shape": "plate",
        "color": "#d43a32"
      }
    ]
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 颜色识别（h3-orbital-docking-yard-color）

零件 h0122 的颜色值是什么？

能力：颜色识别；形式：single-choice；证据：model-state。

- A：#d43a32
- B：#f2bf3c
- C：#e8792e
- D：#2878b8

```json
{
  "input": {
    "part": {
      "id": "h0122",
      "moduleId": "airlock",
      "shape": "plate",
      "size": [
        0.92,
        0.25,
        0.92
      ],
      "position": [
        -1,
        -0.04999999999999993,
        -1
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

### 三维位置（h3-orbital-docking-yard-position）

模块 airlock 的世界包围盒中心是什么？

能力：三维位置；形式：single-choice；证据：model-state。

- A：[-7.387499999999999,2.9599999999999995,0]
- B：[0,0.85,5.2]
- C：[0,0.2,0]
- D：[0,2.2,0]

```json
{
  "input": {
    "centers": {
      "platform": [
        0,
        0.2,
        0
      ],
      "hub": [
        0,
        2.2,
        0
      ],
      "airlock": [
        0,
        0.85,
        5.2
      ],
      "dock-arm-west": [
        -7.387499999999999,
        2.9599999999999995,
        0
      ],
      "dock-arm-east": [
        7.387499999999999,
        2.9599999999999995,
        0
      ],
      "solar-west": [
        0,
        3.2,
        -6
      ],
      "solar-east": [
        0,
        3.2,
        6
      ],
      "shuttle": [
        0,
        1.15,
        -7.5
      ],
      "crane-base": [
        4.2,
        3.2499999999999996,
        3.5
      ],
      "crane-boom": [
        1.5000000000000004,
        6.975,
        3.5
      ],
      "cargo-pod": [
        0,
        1.05,
        8.3
      ]
    }
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 关节类型（h3-orbital-docking-yard-joint-type）

west-arm-pivot 采用什么约束类型？

能力：关节类型；形式：single-choice；证据：model-state。

- A：revolute
- B：fixed
- C：prismatic
- D：spring

```json
{
  "input": {
    "joint": {
      "id": "west-arm-pivot",
      "name": "west arm pivot",
      "type": "revolute",
      "parent": "hub",
      "child": "dock-arm-west",
      "anchorParent": [
        -4,
        0.39999999999999947,
        0
      ],
      "anchorChild": [
        3.3875,
        -0.3599999999999999,
        0
      ],
      "axis": [
        0,
        1,
        0
      ],
      "limits": [
        -1.2,
        1.2
      ]
    }
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 直接连接（h3-orbital-docking-yard-parent）

airlock 的直接父模块集合是什么？

能力：直接连接；形式：single-choice；证据：model-state。

- A：["airlock"]
- B：[]
- C：["platform","hub","airlock","dock-arm-west","dock-arm-east","solar-west","solar-east","shuttle","crane-base","crane-boom","cargo-pod"]
- D：["hub"]

```json
{
  "input": {
    "joints": [
      {
        "id": "hub-clamp",
        "name": "hub clamp",
        "type": "fixed",
        "parent": "platform",
        "child": "hub",
        "anchorParent": [
          0,
          0.3,
          0
        ],
        "anchorChild": [
          0,
          -1.7000000000000002,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "airlock-slide",
        "name": "airlock slide",
        "type": "prismatic",
        "parent": "hub",
        "child": "airlock",
        "anchorParent": [
          0,
          -1.2000000000000002,
          4.2
        ],
        "anchorChild": [
          0,
          0.15000000000000002,
          -1
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          -0.4,
          0.8
        ]
      },
      {
        "id": "west-arm-pivot",
        "name": "west arm pivot",
        "type": "revolute",
        "parent": "hub",
        "child": "dock-arm-west",
        "anchorParent": [
          -4,
          0.39999999999999947,
          0
        ],
        "anchorChild": [
          3.3875,
          -0.3599999999999999,
          0
        ],
        "axis": [
          0,
          1,
          0
        ],
        "limits": [
          -1.2,
          1.2
        ]
      },
      {
        "id": "east-arm-pivot",
        "name": "east arm pivot",
        "type": "revolute",
        "parent": "hub",
        "child": "dock-arm-east",
        "anchorParent": [
          4,
          0.39999999999999947,
          0
        ],
        "anchorChild": [
          -3.3875,
          -0.3599999999999999,
          0
        ],
        "axis": [
          0,
          1,
          0
        ],
        "limits": [
          -1.2,
          1.2
        ]
      },
      {
        "id": "west-solar-hinge",
        "name": "west solar hinge",
        "type": "revolute",
        "parent": "hub",
        "child": "solar-west",
        "anchorParent": [
          0,
          1,
          -3.5
        ],
        "anchorChild": [
          0,
          0,
          2.5
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
        "id": "east-solar-hinge",
        "name": "east solar hinge",
        "type": "revolute",
        "parent": "hub",
        "child": "solar-east",
        "anchorParent": [
          0,
          1,
          3.5
        ],
        "anchorChild": [
          0,
          0,
          -2.5
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
        "id": "shuttle-dock",
        "name": "shuttle dock",
        "type": "fixed",
        "parent": "platform",
        "child": "shuttle",
        "anchorParent": [
          0,
          0.6000000000000001,
          -7.5
        ],
        "anchorChild": [
          0,
          -0.34999999999999987,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "crane-pedestal",
        "name": "crane pedestal",
        "type": "revolute",
        "parent": "platform",
        "child": "crane-base",
        "anchorParent": [
          4.2,
          0.3,
          3.5
        ],
        "anchorChild": [
          0,
          -2.7499999999999996,
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
        "id": "crane-boom-hinge",
        "name": "crane boom hinge",
        "type": "revolute",
        "parent": "crane-base",
        "child": "crane-boom",
        "anchorParent": [
          0,
          3.0500000000000003,
          0
        ],
        "anchorChild": [
          2.6999999999999993,
          -0.6749999999999998,
          0
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          -0.5,
          1
        ]
      },
      {
        "id": "cargo-lock",
        "name": "cargo lock",
        "type": "fixed",
        "parent": "platform",
        "child": "cargo-pod",
        "anchorParent": [
          0,
          0.6000000000000001,
          7.3
        ],
        "anchorChild": [
          0,
          -0.25,
          -1
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
    "choiceId": "D"
  }
}
```

### 基座识别（h3-orbital-docking-yard-anchor）

哪些模块被声明为固定基座？

能力：基座识别；形式：single-choice；证据：model-state。

- A：["platform"]
- B：[]
- C：["platform","hub","airlock","dock-arm-west","dock-arm-east","solar-west","solar-east","shuttle","crane-base","crane-boom","cargo-pod"]
- D：["airlock"]

```json
{
  "input": {
    "modules": [
      {
        "id": "platform",
        "name": "Orbital service platform",
        "role": "foundation",
        "anchored": true,
        "mass": 50,
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
        "id": "hub",
        "name": "Pressurized docking hub",
        "role": "central-control",
        "anchored": false,
        "mass": 20,
        "position": [
          0,
          2.2,
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
        "id": "airlock",
        "name": "Service airlock",
        "role": "service-module",
        "anchored": false,
        "mass": 4,
        "position": [
          0,
          0.85,
          5.2
        ],
        "rotation": [
          0,
          0,
          0,
          1
        ]
      },
      {
        "id": "dock-arm-west",
        "name": "West articulated docking arm",
        "role": "actuator",
        "anchored": false,
        "mass": 6,
        "position": [
          -7.3875,
          2.9599999999999995,
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
        "id": "dock-arm-east",
        "name": "East articulated docking arm",
        "role": "actuator",
        "anchored": false,
        "mass": 6,
        "position": [
          7.3875,
          2.9599999999999995,
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
        "id": "solar-west",
        "name": "West solar wing",
        "role": "power",
        "anchored": false,
        "mass": 5,
        "position": [
          0,
          3.2,
          -6
        ],
        "rotation": [
          0,
          0,
          0,
          1
        ]
      },
      {
        "id": "solar-east",
        "name": "East solar wing",
        "role": "power",
        "anchored": false,
        "mass": 5,
        "position": [
          0,
          3.2,
          6
        ],
        "rotation": [
          0,
          0,
          0,
          1
        ]
      },
      {
        "id": "shuttle",
        "name": "Docked transfer shuttle",
        "role": "payload",
        "anchored": false,
        "mass": 9,
        "position": [
          0,
          1.15,
          -7.5
        ],
        "rotation": [
          0,
          0,
          0,
          1
        ]
      },
      {
        "id": "crane-base",
        "name": "Cargo crane pedestal",
        "role": "support",
        "anchored": false,
        "mass": 8,
        "position": [
          4.2,
          3.2499999999999996,
          3.5
        ],
        "rotation": [
          0,
          0,
          0,
          1
        ]
      },
      {
        "id": "crane-boom",
        "name": "Cargo crane boom",
        "role": "actuator",
        "anchored": false,
        "mass": 4,
        "position": [
          1.5000000000000007,
          6.975,
          3.5
        ],
        "rotation": [
          0,
          0,
          0,
          1
        ]
      },
      {
        "id": "cargo-pod",
        "name": "Transfer cargo pod",
        "role": "payload",
        "anchored": false,
        "mass": 5,
        "position": [
          0,
          1.05,
          8.3
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

### 接口计数（h3-orbital-docking-yard-degree）

airlock 连接几个声明关节？平行关节分别计数。

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
        "id": "hub-clamp",
        "name": "hub clamp",
        "type": "fixed",
        "parent": "platform",
        "child": "hub",
        "anchorParent": [
          0,
          0.3,
          0
        ],
        "anchorChild": [
          0,
          -1.7000000000000002,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "airlock-slide",
        "name": "airlock slide",
        "type": "prismatic",
        "parent": "hub",
        "child": "airlock",
        "anchorParent": [
          0,
          -1.2000000000000002,
          4.2
        ],
        "anchorChild": [
          0,
          0.15000000000000002,
          -1
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          -0.4,
          0.8
        ]
      },
      {
        "id": "west-arm-pivot",
        "name": "west arm pivot",
        "type": "revolute",
        "parent": "hub",
        "child": "dock-arm-west",
        "anchorParent": [
          -4,
          0.39999999999999947,
          0
        ],
        "anchorChild": [
          3.3875,
          -0.3599999999999999,
          0
        ],
        "axis": [
          0,
          1,
          0
        ],
        "limits": [
          -1.2,
          1.2
        ]
      },
      {
        "id": "east-arm-pivot",
        "name": "east arm pivot",
        "type": "revolute",
        "parent": "hub",
        "child": "dock-arm-east",
        "anchorParent": [
          4,
          0.39999999999999947,
          0
        ],
        "anchorChild": [
          -3.3875,
          -0.3599999999999999,
          0
        ],
        "axis": [
          0,
          1,
          0
        ],
        "limits": [
          -1.2,
          1.2
        ]
      },
      {
        "id": "west-solar-hinge",
        "name": "west solar hinge",
        "type": "revolute",
        "parent": "hub",
        "child": "solar-west",
        "anchorParent": [
          0,
          1,
          -3.5
        ],
        "anchorChild": [
          0,
          0,
          2.5
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
        "id": "east-solar-hinge",
        "name": "east solar hinge",
        "type": "revolute",
        "parent": "hub",
        "child": "solar-east",
        "anchorParent": [
          0,
          1,
          3.5
        ],
        "anchorChild": [
          0,
          0,
          -2.5
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
        "id": "shuttle-dock",
        "name": "shuttle dock",
        "type": "fixed",
        "parent": "platform",
        "child": "shuttle",
        "anchorParent": [
          0,
          0.6000000000000001,
          -7.5
        ],
        "anchorChild": [
          0,
          -0.34999999999999987,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "crane-pedestal",
        "name": "crane pedestal",
        "type": "revolute",
        "parent": "platform",
        "child": "crane-base",
        "anchorParent": [
          4.2,
          0.3,
          3.5
        ],
        "anchorChild": [
          0,
          -2.7499999999999996,
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
        "id": "crane-boom-hinge",
        "name": "crane boom hinge",
        "type": "revolute",
        "parent": "crane-base",
        "child": "crane-boom",
        "anchorParent": [
          0,
          3.0500000000000003,
          0
        ],
        "anchorChild": [
          2.6999999999999993,
          -0.6749999999999998,
          0
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          -0.5,
          1
        ]
      },
      {
        "id": "cargo-lock",
        "name": "cargo lock",
        "type": "fixed",
        "parent": "platform",
        "child": "cargo-pod",
        "anchorParent": [
          0,
          0.6000000000000001,
          7.3
        ],
        "anchorChild": [
          0,
          -0.25,
          -1
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

### 局部改色（h3-orbital-docking-yard-recolor）

仅将 h0122 改成 #e8792e，其他零件不变。选择正确补丁。

能力：局部改色；形式：single-choice；证据：model-state。

- A：{"id":"*","color":"#e8792e"}
- B：{"id":"h0122","color":"#e8792e"}
- C：{"id":"h0123","color":"#e8792e"}
- D：{"id":"h0122","color":"#2878b8"}

```json
{
  "input": {
    "part": {
      "id": "h0122",
      "moduleId": "airlock",
      "shape": "plate",
      "size": [
        0.92,
        0.25,
        0.92
      ],
      "position": [
        -1,
        -0.04999999999999993,
        -1
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
    "choiceId": "B"
  }
}
```

### 补装部件（h3-orbital-docking-yard-add）

模块 airlock 缺失零件 h0122。选择与目标清单一致的补装描述。

能力：补装部件；形式：single-choice；证据：model-state。

- A：{"id":"h0122","moduleId":"airlock","shape":"plate","size":[0.92,0.25,0.92],"position":[-1,-0.04999999999999993,-1],"rotation":[0,0,0,1],"color":"#e8792e"}
- B：{"id":"h0122","moduleId":"platform","shape":"plate","size":[0.92,0.25,0.92],"position":[-1,-0.04999999999999993,-1],"rotation":[0,0,0,1],"color":"#e8792e"}
- C：{"id":"h0122","moduleId":"airlock","shape":"plate","size":[3,3,3],"position":[-1,-0.04999999999999993,-1],"rotation":[0,0,0,1],"color":"#e8792e"}
- D：{"id":"h0122","moduleId":"airlock","shape":"plate","size":[0.92,0.25,0.92],"position":[-1,-0.04999999999999993,-1],"rotation":[0,0,0,1],"color":"#000000"}

```json
{
  "input": {
    "targetPart": {
      "id": "h0122",
      "moduleId": "airlock",
      "shape": "plate",
      "size": [
        0.92,
        0.25,
        0.92
      ],
      "position": [
        -1,
        -0.04999999999999993,
        -1
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
      "h0037",
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
      "h0060",
      "h0061",
      "h0062",
      "h0063",
      "h0064",
      "h0065",
      "h0066",
      "h0067",
      "h0068",
      "h0069",
      "h0070",
      "h0071",
      "h0072",
      "h0073",
      "h0074",
      "h0075",
      "h0076",
      "h0077",
      "h0078",
      "h0079",
      "h0080",
      "h0081",
      "h0082",
      "h0083",
      "h0084",
      "h0085",
      "h0086",
      "h0087",
      "h0088",
      "h0089",
      "h0090",
      "h0091",
      "h0092",
      "h0093",
      "h0094",
      "h0095",
      "h0096",
      "h0097",
      "h0098",
      "h0099",
      "h0100",
      "h0101",
      "h0102",
      "h0103",
      "h0104",
      "h0105",
      "h0106",
      "h0107",
      "h0108",
      "h0109",
      "h0110",
      "h0111",
      "h0112",
      "h0113",
      "h0114",
      "h0115",
      "h0116",
      "h0117",
      "h0118",
      "h0119",
      "h0120",
      "h0121",
      "h0123",
      "h0124",
      "h0125",
      "h0126",
      "h0127",
      "h0128",
      "h0129",
      "h0130",
      "h0131",
      "h0132",
      "h0133",
      "h0134",
      "h0135",
      "h0136",
      "h0137",
      "h0138",
      "h0139",
      "h0140",
      "h0141",
      "h0142",
      "h0143",
      "h0144",
      "h0145",
      "h0146",
      "h0147",
      "h0148",
      "h0149",
      "h0150",
      "h0151",
      "h0152",
      "h0153",
      "h0154",
      "h0155",
      "h0156",
      "h0157",
      "h0158",
      "h0159",
      "h0160",
      "h0161",
      "h0162",
      "h0163",
      "h0164",
      "h0165",
      "h0166",
      "h0167",
      "h0168",
      "h0169",
      "h0170",
      "h0171",
      "h0172",
      "h0173",
      "h0174",
      "h0175",
      "h0176",
      "h0177",
      "h0178",
      "h0179",
      "h0180",
      "h0181",
      "h0182",
      "h0183",
      "h0184",
      "h0185",
      "h0186",
      "h0187",
      "h0188",
      "h0189",
      "h0190",
      "h0191",
      "h0192",
      "h0193",
      "h0194",
      "h0195",
      "h0196",
      "h0197",
      "h0198",
      "h0199",
      "h0200",
      "h0201",
      "h0202",
      "h0203",
      "h0204",
      "h0205",
      "h0206",
      "h0207",
      "h0208",
      "h0209",
      "h0210",
      "h0211",
      "h0212",
      "h0213",
      "h0214",
      "h0215",
      "h0216",
      "h0217",
      "h0218",
      "h0219",
      "h0220",
      "h0221",
      "h0222",
      "h0223",
      "h0224",
      "h0225",
      "h0226",
      "h0227",
      "h0228",
      "h0229",
      "h0230",
      "h0231",
      "h0232",
      "h0233"
    ]
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 安全拆除（h3-orbital-docking-yard-remove）

按声明依赖图，当前可以先拆哪些叶模块？

能力：安全拆除；形式：single-choice；证据：model-state。

- A：["platform","hub","airlock","dock-arm-west","dock-arm-east","solar-west","solar-east","shuttle","crane-base","crane-boom","cargo-pod"]
- B：["airlock","cargo-pod","crane-boom","dock-arm-east","dock-arm-west","shuttle","solar-east","solar-west"]
- C：["platform"]
- D：[]

```json
{
  "input": {
    "joints": [
      {
        "id": "hub-clamp",
        "name": "hub clamp",
        "type": "fixed",
        "parent": "platform",
        "child": "hub",
        "anchorParent": [
          0,
          0.3,
          0
        ],
        "anchorChild": [
          0,
          -1.7000000000000002,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "airlock-slide",
        "name": "airlock slide",
        "type": "prismatic",
        "parent": "hub",
        "child": "airlock",
        "anchorParent": [
          0,
          -1.2000000000000002,
          4.2
        ],
        "anchorChild": [
          0,
          0.15000000000000002,
          -1
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          -0.4,
          0.8
        ]
      },
      {
        "id": "west-arm-pivot",
        "name": "west arm pivot",
        "type": "revolute",
        "parent": "hub",
        "child": "dock-arm-west",
        "anchorParent": [
          -4,
          0.39999999999999947,
          0
        ],
        "anchorChild": [
          3.3875,
          -0.3599999999999999,
          0
        ],
        "axis": [
          0,
          1,
          0
        ],
        "limits": [
          -1.2,
          1.2
        ]
      },
      {
        "id": "east-arm-pivot",
        "name": "east arm pivot",
        "type": "revolute",
        "parent": "hub",
        "child": "dock-arm-east",
        "anchorParent": [
          4,
          0.39999999999999947,
          0
        ],
        "anchorChild": [
          -3.3875,
          -0.3599999999999999,
          0
        ],
        "axis": [
          0,
          1,
          0
        ],
        "limits": [
          -1.2,
          1.2
        ]
      },
      {
        "id": "west-solar-hinge",
        "name": "west solar hinge",
        "type": "revolute",
        "parent": "hub",
        "child": "solar-west",
        "anchorParent": [
          0,
          1,
          -3.5
        ],
        "anchorChild": [
          0,
          0,
          2.5
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
        "id": "east-solar-hinge",
        "name": "east solar hinge",
        "type": "revolute",
        "parent": "hub",
        "child": "solar-east",
        "anchorParent": [
          0,
          1,
          3.5
        ],
        "anchorChild": [
          0,
          0,
          -2.5
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
        "id": "shuttle-dock",
        "name": "shuttle dock",
        "type": "fixed",
        "parent": "platform",
        "child": "shuttle",
        "anchorParent": [
          0,
          0.6000000000000001,
          -7.5
        ],
        "anchorChild": [
          0,
          -0.34999999999999987,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "crane-pedestal",
        "name": "crane pedestal",
        "type": "revolute",
        "parent": "platform",
        "child": "crane-base",
        "anchorParent": [
          4.2,
          0.3,
          3.5
        ],
        "anchorChild": [
          0,
          -2.7499999999999996,
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
        "id": "crane-boom-hinge",
        "name": "crane boom hinge",
        "type": "revolute",
        "parent": "crane-base",
        "child": "crane-boom",
        "anchorParent": [
          0,
          3.0500000000000003,
          0
        ],
        "anchorChild": [
          2.6999999999999993,
          -0.6749999999999998,
          0
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          -0.5,
          1
        ]
      },
      {
        "id": "cargo-lock",
        "name": "cargo lock",
        "type": "fixed",
        "parent": "platform",
        "child": "cargo-pod",
        "anchorParent": [
          0,
          0.6000000000000001,
          7.3
        ],
        "anchorChild": [
          0,
          -0.25,
          -1
        ],
        "axis": [
          0,
          1,
          0
        ]
      }
    ],
    "modules": [
      "platform",
      "hub",
      "airlock",
      "dock-arm-west",
      "dock-arm-east",
      "solar-west",
      "solar-east",
      "shuttle",
      "crane-base",
      "crane-boom",
      "cargo-pod"
    ]
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 替换选择（h3-orbital-docking-yard-replace）

在成本上限内选择刚度最大的替换件；并列选成本低者，再并列选ID字典序最小者。

能力：替换选择；形式：single-choice；证据：model-state。

- A：stock-0
- B：stock-2
- C：stock-3
- D：stock-1

```json
{
  "input": {
    "alternatives": [
      {
        "id": "stock-0",
        "cost": 2,
        "stiffness": 7,
        "mass": 1.2
      },
      {
        "id": "stock-1",
        "cost": 6,
        "stiffness": 9,
        "mass": 1.6
      },
      {
        "id": "stock-2",
        "cost": 7,
        "stiffness": 11,
        "mass": 1.2
      },
      {
        "id": "stock-3",
        "cost": 2,
        "stiffness": 7,
        "mass": 1.2
      }
    ],
    "maxCost": 6
  },
  "answer": {
    "choiceId": "D"
  }
}
```

### 平移纠偏（h3-orbital-docking-yard-translate）

观察到相对目标的平移误差 delta，选择补偿平移。

能力：平移纠偏；形式：single-choice；证据：model-state。

- A：[0,0,0]
- B：[0,2,0]
- C：[-4,0,2]
- D：[4,0,-2]

```json
{
  "input": {
    "delta": [
      4,
      0,
      -2
    ],
    "target": "airlock"
  },
  "answer": {
    "choiceId": "C"
  }
}
```

### 姿态纠偏（h3-orbital-docking-yard-rotate）

选择从当前yaw到目标yaw的最短有符号旋转；恰好180°时使用-180°。

能力：姿态纠偏；形式：single-choice；证据：model-state。

- A：-180
- B：0
- C：90
- D：-90

```json
{
  "input": {
    "module": "airlock",
    "currentYaw": 0,
    "targetYaw": 0
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 下一步放置（h3-orbital-docking-yard-next-module）

已完成给定前缀，选择所有前置依赖已满足的下一模块集合。

能力：下一步放置；形式：single-choice；证据：model-state。

- A：["platform","hub","airlock","solar-west","solar-east","dock-arm-west"]
- B：["dock-arm-east","shuttle","crane-base","crane-boom","cargo-pod"]
- C：["cargo-pod","crane-base","dock-arm-east","shuttle"]
- D：[]

```json
{
  "input": {
    "prefix": [
      "platform",
      "hub",
      "airlock",
      "solar-west",
      "solar-east",
      "dock-arm-west"
    ],
    "joints": [
      {
        "id": "hub-clamp",
        "name": "hub clamp",
        "type": "fixed",
        "parent": "platform",
        "child": "hub",
        "anchorParent": [
          0,
          0.3,
          0
        ],
        "anchorChild": [
          0,
          -1.7000000000000002,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "airlock-slide",
        "name": "airlock slide",
        "type": "prismatic",
        "parent": "hub",
        "child": "airlock",
        "anchorParent": [
          0,
          -1.2000000000000002,
          4.2
        ],
        "anchorChild": [
          0,
          0.15000000000000002,
          -1
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          -0.4,
          0.8
        ]
      },
      {
        "id": "west-arm-pivot",
        "name": "west arm pivot",
        "type": "revolute",
        "parent": "hub",
        "child": "dock-arm-west",
        "anchorParent": [
          -4,
          0.39999999999999947,
          0
        ],
        "anchorChild": [
          3.3875,
          -0.3599999999999999,
          0
        ],
        "axis": [
          0,
          1,
          0
        ],
        "limits": [
          -1.2,
          1.2
        ]
      },
      {
        "id": "east-arm-pivot",
        "name": "east arm pivot",
        "type": "revolute",
        "parent": "hub",
        "child": "dock-arm-east",
        "anchorParent": [
          4,
          0.39999999999999947,
          0
        ],
        "anchorChild": [
          -3.3875,
          -0.3599999999999999,
          0
        ],
        "axis": [
          0,
          1,
          0
        ],
        "limits": [
          -1.2,
          1.2
        ]
      },
      {
        "id": "west-solar-hinge",
        "name": "west solar hinge",
        "type": "revolute",
        "parent": "hub",
        "child": "solar-west",
        "anchorParent": [
          0,
          1,
          -3.5
        ],
        "anchorChild": [
          0,
          0,
          2.5
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
        "id": "east-solar-hinge",
        "name": "east solar hinge",
        "type": "revolute",
        "parent": "hub",
        "child": "solar-east",
        "anchorParent": [
          0,
          1,
          3.5
        ],
        "anchorChild": [
          0,
          0,
          -2.5
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
        "id": "shuttle-dock",
        "name": "shuttle dock",
        "type": "fixed",
        "parent": "platform",
        "child": "shuttle",
        "anchorParent": [
          0,
          0.6000000000000001,
          -7.5
        ],
        "anchorChild": [
          0,
          -0.34999999999999987,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "crane-pedestal",
        "name": "crane pedestal",
        "type": "revolute",
        "parent": "platform",
        "child": "crane-base",
        "anchorParent": [
          4.2,
          0.3,
          3.5
        ],
        "anchorChild": [
          0,
          -2.7499999999999996,
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
        "id": "crane-boom-hinge",
        "name": "crane boom hinge",
        "type": "revolute",
        "parent": "crane-base",
        "child": "crane-boom",
        "anchorParent": [
          0,
          3.0500000000000003,
          0
        ],
        "anchorChild": [
          2.6999999999999993,
          -0.6749999999999998,
          0
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          -0.5,
          1
        ]
      },
      {
        "id": "cargo-lock",
        "name": "cargo lock",
        "type": "fixed",
        "parent": "platform",
        "child": "cargo-pod",
        "anchorParent": [
          0,
          0.6000000000000001,
          7.3
        ],
        "anchorChild": [
          0,
          -0.25,
          -1
        ],
        "axis": [
          0,
          1,
          0
        ]
      }
    ],
    "modules": [
      "platform",
      "hub",
      "airlock",
      "dock-arm-west",
      "dock-arm-east",
      "solar-west",
      "solar-east",
      "shuttle",
      "crane-base",
      "crane-boom",
      "cargo-pod"
    ]
  },
  "answer": {
    "choiceId": "C"
  }
}
```

### 库存核算（h3-orbital-docking-yard-inventory）

备件库有 12 件，替换模块需 9 件，还剩多少？

能力：库存核算；形式：single-choice；证据：model-state。

- A：6
- B：3
- C：4
- D：2

```json
{
  "input": {
    "available": 12,
    "required": 9
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 子装配边界（h3-orbital-docking-yard-boundary）

隔离 airlock 需要断开哪些边界关节？

能力：子装配边界；形式：single-choice；证据：model-state。

- A：["hub-clamp","airlock-slide","west-arm-pivot","east-arm-pivot","west-solar-hinge","east-solar-hinge","shuttle-dock","crane-pedestal","crane-boom-hinge","cargo-lock"]
- B：["west-arm-pivot"]
- C：["airlock-slide"]
- D：[]

```json
{
  "input": {
    "joints": [
      {
        "id": "hub-clamp",
        "name": "hub clamp",
        "type": "fixed",
        "parent": "platform",
        "child": "hub",
        "anchorParent": [
          0,
          0.3,
          0
        ],
        "anchorChild": [
          0,
          -1.7000000000000002,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "airlock-slide",
        "name": "airlock slide",
        "type": "prismatic",
        "parent": "hub",
        "child": "airlock",
        "anchorParent": [
          0,
          -1.2000000000000002,
          4.2
        ],
        "anchorChild": [
          0,
          0.15000000000000002,
          -1
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          -0.4,
          0.8
        ]
      },
      {
        "id": "west-arm-pivot",
        "name": "west arm pivot",
        "type": "revolute",
        "parent": "hub",
        "child": "dock-arm-west",
        "anchorParent": [
          -4,
          0.39999999999999947,
          0
        ],
        "anchorChild": [
          3.3875,
          -0.3599999999999999,
          0
        ],
        "axis": [
          0,
          1,
          0
        ],
        "limits": [
          -1.2,
          1.2
        ]
      },
      {
        "id": "east-arm-pivot",
        "name": "east arm pivot",
        "type": "revolute",
        "parent": "hub",
        "child": "dock-arm-east",
        "anchorParent": [
          4,
          0.39999999999999947,
          0
        ],
        "anchorChild": [
          -3.3875,
          -0.3599999999999999,
          0
        ],
        "axis": [
          0,
          1,
          0
        ],
        "limits": [
          -1.2,
          1.2
        ]
      },
      {
        "id": "west-solar-hinge",
        "name": "west solar hinge",
        "type": "revolute",
        "parent": "hub",
        "child": "solar-west",
        "anchorParent": [
          0,
          1,
          -3.5
        ],
        "anchorChild": [
          0,
          0,
          2.5
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
        "id": "east-solar-hinge",
        "name": "east solar hinge",
        "type": "revolute",
        "parent": "hub",
        "child": "solar-east",
        "anchorParent": [
          0,
          1,
          3.5
        ],
        "anchorChild": [
          0,
          0,
          -2.5
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
        "id": "shuttle-dock",
        "name": "shuttle dock",
        "type": "fixed",
        "parent": "platform",
        "child": "shuttle",
        "anchorParent": [
          0,
          0.6000000000000001,
          -7.5
        ],
        "anchorChild": [
          0,
          -0.34999999999999987,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "crane-pedestal",
        "name": "crane pedestal",
        "type": "revolute",
        "parent": "platform",
        "child": "crane-base",
        "anchorParent": [
          4.2,
          0.3,
          3.5
        ],
        "anchorChild": [
          0,
          -2.7499999999999996,
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
        "id": "crane-boom-hinge",
        "name": "crane boom hinge",
        "type": "revolute",
        "parent": "crane-base",
        "child": "crane-boom",
        "anchorParent": [
          0,
          3.0500000000000003,
          0
        ],
        "anchorChild": [
          2.6999999999999993,
          -0.6749999999999998,
          0
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          -0.5,
          1
        ]
      },
      {
        "id": "cargo-lock",
        "name": "cargo lock",
        "type": "fixed",
        "parent": "platform",
        "child": "cargo-pod",
        "anchorParent": [
          0,
          0.6000000000000001,
          7.3
        ],
        "anchorChild": [
          0,
          -0.25,
          -1
        ],
        "axis": [
          0,
          1,
          0
        ]
      }
    ],
    "target": "airlock"
  },
  "answer": {
    "choiceId": "C"
  }
}
```

### 最小干预（h3-orbital-docking-yard-no-op）

当前模块颜色已满足指令，且无需改变位姿。最少需要几次编辑？

能力：最小干预；形式：single-choice；证据：model-state。

- A：9
- B：0
- C：1
- D：2

```json
{
  "input": {
    "module": "airlock"
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 全过程依赖（h3-orbital-docking-yard-prefix）

给定候选顺序，首次违反前置依赖的步骤是？从 0 编号，-1 表示没有违反。

能力：全过程依赖；形式：single-choice；证据：support-graph。

- A：-1
- B：2
- C：10
- D：1

```json
{
  "input": {
    "order": [
      "platform",
      "solar-west",
      "hub",
      "airlock",
      "solar-east",
      "dock-arm-west",
      "dock-arm-east",
      "shuttle",
      "crane-base",
      "crane-boom",
      "cargo-pod"
    ],
    "joints": [
      {
        "id": "hub-clamp",
        "name": "hub clamp",
        "type": "fixed",
        "parent": "platform",
        "child": "hub",
        "anchorParent": [
          0,
          0.3,
          0
        ],
        "anchorChild": [
          0,
          -1.7000000000000002,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "airlock-slide",
        "name": "airlock slide",
        "type": "prismatic",
        "parent": "hub",
        "child": "airlock",
        "anchorParent": [
          0,
          -1.2000000000000002,
          4.2
        ],
        "anchorChild": [
          0,
          0.15000000000000002,
          -1
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          -0.4,
          0.8
        ]
      },
      {
        "id": "west-arm-pivot",
        "name": "west arm pivot",
        "type": "revolute",
        "parent": "hub",
        "child": "dock-arm-west",
        "anchorParent": [
          -4,
          0.39999999999999947,
          0
        ],
        "anchorChild": [
          3.3875,
          -0.3599999999999999,
          0
        ],
        "axis": [
          0,
          1,
          0
        ],
        "limits": [
          -1.2,
          1.2
        ]
      },
      {
        "id": "east-arm-pivot",
        "name": "east arm pivot",
        "type": "revolute",
        "parent": "hub",
        "child": "dock-arm-east",
        "anchorParent": [
          4,
          0.39999999999999947,
          0
        ],
        "anchorChild": [
          -3.3875,
          -0.3599999999999999,
          0
        ],
        "axis": [
          0,
          1,
          0
        ],
        "limits": [
          -1.2,
          1.2
        ]
      },
      {
        "id": "west-solar-hinge",
        "name": "west solar hinge",
        "type": "revolute",
        "parent": "hub",
        "child": "solar-west",
        "anchorParent": [
          0,
          1,
          -3.5
        ],
        "anchorChild": [
          0,
          0,
          2.5
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
        "id": "east-solar-hinge",
        "name": "east solar hinge",
        "type": "revolute",
        "parent": "hub",
        "child": "solar-east",
        "anchorParent": [
          0,
          1,
          3.5
        ],
        "anchorChild": [
          0,
          0,
          -2.5
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
        "id": "shuttle-dock",
        "name": "shuttle dock",
        "type": "fixed",
        "parent": "platform",
        "child": "shuttle",
        "anchorParent": [
          0,
          0.6000000000000001,
          -7.5
        ],
        "anchorChild": [
          0,
          -0.34999999999999987,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "crane-pedestal",
        "name": "crane pedestal",
        "type": "revolute",
        "parent": "platform",
        "child": "crane-base",
        "anchorParent": [
          4.2,
          0.3,
          3.5
        ],
        "anchorChild": [
          0,
          -2.7499999999999996,
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
        "id": "crane-boom-hinge",
        "name": "crane boom hinge",
        "type": "revolute",
        "parent": "crane-base",
        "child": "crane-boom",
        "anchorParent": [
          0,
          3.0500000000000003,
          0
        ],
        "anchorChild": [
          2.6999999999999993,
          -0.6749999999999998,
          0
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          -0.5,
          1
        ]
      },
      {
        "id": "cargo-lock",
        "name": "cargo lock",
        "type": "fixed",
        "parent": "platform",
        "child": "cargo-pod",
        "anchorParent": [
          0,
          0.6000000000000001,
          7.3
        ],
        "anchorChild": [
          0,
          -0.25,
          -1
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
    "choiceId": "D"
  }
}
```

### 连续维修路径（h3-orbital-docking-yard-access）

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
          15.375,
          0.85,
          5.2
        ],
        "end": [
          0,
          0.85,
          5.2
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
          11.86,
          5.2
        ],
        "end": [
          0,
          0.85,
          5.2
        ],
        "halfExtents": [
          0.18,
          0.18,
          0.18
        ],
        "clear": false,
        "timeOfImpact": 0.7629427313804626
      },
      {
        "id": "path-2",
        "start": [
          0,
          0.85,
          13.760000000000002
        ],
        "end": [
          0,
          0.85,
          5.2
        ],
        "halfExtents": [
          0.18,
          0.18,
          0.18
        ],
        "clear": false,
        "timeOfImpact": 0.4462616443634033
      }
    ],
    "simulator": "stud-inclusive conservative cuboids; anchored base; force-limited position servos; no clutch/material calibration"
  },
  "answer": {
    "choiceIds": [
      "C"
    ]
  }
}
```

### 支撑反事实（h3-orbital-docking-yard-counterfactual）

移除指定模块后，哪些其余模块失去到任一基座的关节路径？不包含被移除模块本身。

能力：支撑反事实；形式：single-choice；证据：support-graph。

- A：[]
- B：["platform","hub","airlock","dock-arm-west","dock-arm-east","solar-west","solar-east","shuttle","crane-base","crane-boom","cargo-pod"]
- C：["airlock","dock-arm-east","dock-arm-west","solar-east","solar-west"]
- D：["hub"]

```json
{
  "input": {
    "removed": "hub",
    "roots": [
      "platform"
    ],
    "joints": [
      {
        "id": "hub-clamp",
        "name": "hub clamp",
        "type": "fixed",
        "parent": "platform",
        "child": "hub",
        "anchorParent": [
          0,
          0.3,
          0
        ],
        "anchorChild": [
          0,
          -1.7000000000000002,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "airlock-slide",
        "name": "airlock slide",
        "type": "prismatic",
        "parent": "hub",
        "child": "airlock",
        "anchorParent": [
          0,
          -1.2000000000000002,
          4.2
        ],
        "anchorChild": [
          0,
          0.15000000000000002,
          -1
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          -0.4,
          0.8
        ]
      },
      {
        "id": "west-arm-pivot",
        "name": "west arm pivot",
        "type": "revolute",
        "parent": "hub",
        "child": "dock-arm-west",
        "anchorParent": [
          -4,
          0.39999999999999947,
          0
        ],
        "anchorChild": [
          3.3875,
          -0.3599999999999999,
          0
        ],
        "axis": [
          0,
          1,
          0
        ],
        "limits": [
          -1.2,
          1.2
        ]
      },
      {
        "id": "east-arm-pivot",
        "name": "east arm pivot",
        "type": "revolute",
        "parent": "hub",
        "child": "dock-arm-east",
        "anchorParent": [
          4,
          0.39999999999999947,
          0
        ],
        "anchorChild": [
          -3.3875,
          -0.3599999999999999,
          0
        ],
        "axis": [
          0,
          1,
          0
        ],
        "limits": [
          -1.2,
          1.2
        ]
      },
      {
        "id": "west-solar-hinge",
        "name": "west solar hinge",
        "type": "revolute",
        "parent": "hub",
        "child": "solar-west",
        "anchorParent": [
          0,
          1,
          -3.5
        ],
        "anchorChild": [
          0,
          0,
          2.5
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
        "id": "east-solar-hinge",
        "name": "east solar hinge",
        "type": "revolute",
        "parent": "hub",
        "child": "solar-east",
        "anchorParent": [
          0,
          1,
          3.5
        ],
        "anchorChild": [
          0,
          0,
          -2.5
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
        "id": "shuttle-dock",
        "name": "shuttle dock",
        "type": "fixed",
        "parent": "platform",
        "child": "shuttle",
        "anchorParent": [
          0,
          0.6000000000000001,
          -7.5
        ],
        "anchorChild": [
          0,
          -0.34999999999999987,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "crane-pedestal",
        "name": "crane pedestal",
        "type": "revolute",
        "parent": "platform",
        "child": "crane-base",
        "anchorParent": [
          4.2,
          0.3,
          3.5
        ],
        "anchorChild": [
          0,
          -2.7499999999999996,
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
        "id": "crane-boom-hinge",
        "name": "crane boom hinge",
        "type": "revolute",
        "parent": "crane-base",
        "child": "crane-boom",
        "anchorParent": [
          0,
          3.0500000000000003,
          0
        ],
        "anchorChild": [
          2.6999999999999993,
          -0.6749999999999998,
          0
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          -0.5,
          1
        ]
      },
      {
        "id": "cargo-lock",
        "name": "cargo lock",
        "type": "fixed",
        "parent": "platform",
        "child": "cargo-pod",
        "anchorParent": [
          0,
          0.6000000000000001,
          7.3
        ],
        "anchorChild": [
          0,
          -0.25,
          -1
        ],
        "axis": [
          0,
          1,
          0
        ]
      }
    ],
    "modules": [
      "platform",
      "hub",
      "airlock",
      "dock-arm-west",
      "dock-arm-east",
      "solar-west",
      "solar-east",
      "shuttle",
      "crane-base",
      "crane-boom",
      "cargo-pod"
    ]
  },
  "answer": {
    "choiceId": "C"
  }
}
```

### 冲击响应读数（h3-orbital-docking-yard-dynamic）

Rapier 实际采样轨迹中的最大平移位移是多少？按四位小数报告。

能力：冲击响应读数；形式：single-choice；证据：Rapier。

- A：0.0107
- B：0.2107
- C：0
- D：1.0107

```json
{
  "input": {
    "trace": [
      {
        "time": 0.008333333333333333,
        "displacement": 0.01066908821350834
      },
      {
        "time": 0.10833333333333334,
        "displacement": 0.002672615059164524
      },
      {
        "time": 0.20833333333333334,
        "displacement": 0.00059642136226781
      },
      {
        "time": 0.30833333333333335,
        "displacement": 0.00012128014725706866
      },
      {
        "time": 0.4083333333333333,
        "displacement": 0.00000691824823787065
      },
      {
        "time": 0.5083333333333333,
        "displacement": 0.00000691824823787065
      },
      {
        "time": 0.6083333333333333,
        "displacement": 0.00000691824823787065
      },
      {
        "time": 0.7083333333333334,
        "displacement": 0.0000030648613291221717
      },
      {
        "time": 0.8083333333333333,
        "displacement": 0.0000030648613291221717
      },
      {
        "time": 0.9083333333333333,
        "displacement": 0.0000030648613291221717
      },
      {
        "time": 1,
        "displacement": 0.0000030648613291221717
      }
    ],
    "impulse": [
      10,
      1.8,
      3.5
    ],
    "nominalDrift": 0.00511307985407688,
    "scope": "采样轨迹极值，非连续时间极值；不代表实物安全阈值"
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 关节限位推理（h3-orbital-docking-yard-kinematic）

下列目标位置/角度中哪些在关节声明限位内（含边界）？

能力：关节限位推理；形式：multiple-choice；证据：model-state。

- A：-1.7
- B：1.7
- C：-1.2
- D：0

```json
{
  "input": {
    "joint": "west-arm-pivot",
    "limits": [
      -1.2,
      1.2
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

### 约束故障诊断（h3-orbital-docking-yard-diagnosis）

已检测到端点和约束类型如下，选择匹配的全部关节。

能力：约束故障诊断；形式：multiple-choice；证据：model-state。

- A：crane-boom-hinge
- B：hub-clamp
- C：airlock-slide
- D：west-arm-pivot

```json
{
  "input": {
    "endpoints": [
      "crane-base",
      "crane-boom"
    ],
    "type": "revolute",
    "joints": [
      {
        "id": "hub-clamp",
        "name": "hub clamp",
        "type": "fixed",
        "parent": "platform",
        "child": "hub",
        "anchorParent": [
          0,
          0.3,
          0
        ],
        "anchorChild": [
          0,
          -1.7000000000000002,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "airlock-slide",
        "name": "airlock slide",
        "type": "prismatic",
        "parent": "hub",
        "child": "airlock",
        "anchorParent": [
          0,
          -1.2000000000000002,
          4.2
        ],
        "anchorChild": [
          0,
          0.15000000000000002,
          -1
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          -0.4,
          0.8
        ]
      },
      {
        "id": "west-arm-pivot",
        "name": "west arm pivot",
        "type": "revolute",
        "parent": "hub",
        "child": "dock-arm-west",
        "anchorParent": [
          -4,
          0.39999999999999947,
          0
        ],
        "anchorChild": [
          3.3875,
          -0.3599999999999999,
          0
        ],
        "axis": [
          0,
          1,
          0
        ],
        "limits": [
          -1.2,
          1.2
        ]
      },
      {
        "id": "east-arm-pivot",
        "name": "east arm pivot",
        "type": "revolute",
        "parent": "hub",
        "child": "dock-arm-east",
        "anchorParent": [
          4,
          0.39999999999999947,
          0
        ],
        "anchorChild": [
          -3.3875,
          -0.3599999999999999,
          0
        ],
        "axis": [
          0,
          1,
          0
        ],
        "limits": [
          -1.2,
          1.2
        ]
      },
      {
        "id": "west-solar-hinge",
        "name": "west solar hinge",
        "type": "revolute",
        "parent": "hub",
        "child": "solar-west",
        "anchorParent": [
          0,
          1,
          -3.5
        ],
        "anchorChild": [
          0,
          0,
          2.5
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
        "id": "east-solar-hinge",
        "name": "east solar hinge",
        "type": "revolute",
        "parent": "hub",
        "child": "solar-east",
        "anchorParent": [
          0,
          1,
          3.5
        ],
        "anchorChild": [
          0,
          0,
          -2.5
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
        "id": "shuttle-dock",
        "name": "shuttle dock",
        "type": "fixed",
        "parent": "platform",
        "child": "shuttle",
        "anchorParent": [
          0,
          0.6000000000000001,
          -7.5
        ],
        "anchorChild": [
          0,
          -0.34999999999999987,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "crane-pedestal",
        "name": "crane pedestal",
        "type": "revolute",
        "parent": "platform",
        "child": "crane-base",
        "anchorParent": [
          4.2,
          0.3,
          3.5
        ],
        "anchorChild": [
          0,
          -2.7499999999999996,
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
        "id": "crane-boom-hinge",
        "name": "crane boom hinge",
        "type": "revolute",
        "parent": "crane-base",
        "child": "crane-boom",
        "anchorParent": [
          0,
          3.0500000000000003,
          0
        ],
        "anchorChild": [
          2.6999999999999993,
          -0.6749999999999998,
          0
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          -0.5,
          1
        ]
      },
      {
        "id": "cargo-lock",
        "name": "cargo lock",
        "type": "fixed",
        "parent": "platform",
        "child": "cargo-pod",
        "anchorParent": [
          0,
          0.6000000000000001,
          7.3
        ],
        "anchorChild": [
          0,
          -0.25,
          -1
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
      "A"
    ]
  }
}
```

### 主动检查收益（h3-orbital-docking-yard-information-gain）

均匀先验四个世界，选择信息增益/成本最大的全部检查。

能力：主动检查收益；形式：multiple-choice；证据：finite-world。

- A：query-1
- B：query-2
- C：query-0

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
    "module": "airlock",
    "worlds": [
      "normal",
      "jammed",
      "reversed",
      "loose"
    ]
  },
  "answer": {
    "choiceIds": [
      "A",
      "C"
    ]
  }
}
```

### 不确定性与弃答（h3-orbital-docking-yard-abstention）

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

### 观测后信念更新（h3-orbital-docking-yard-posterior）

均匀先验，得到给定观测后，jammed 世界的后验概率是多少？

能力：观测后信念更新；形式：single-choice；证据：finite-world。

- A：0.25
- B：0.5
- C：0.3333333333333333
- D：0

```json
{
  "input": {
    "module": "airlock",
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
      "positive"
    ],
    "observed": "negative"
  },
  "answer": {
    "choiceId": "C"
  }
}
```

### 多目标工程权衡（h3-orbital-docking-yard-pareto）

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
        "stiffness": 7,
        "mass": 1.2
      },
      {
        "id": "stock-1",
        "cost": 6,
        "stiffness": 9,
        "mass": 1.6
      },
      {
        "id": "stock-2",
        "cost": 7,
        "stiffness": 11,
        "mass": 1.2
      },
      {
        "id": "stock-3",
        "cost": 2,
        "stiffness": 7,
        "mass": 1.2
      }
    ]
  },
  "answer": {
    "choiceIds": [
      "A",
      "B",
      "C",
      "D"
    ]
  }
}
```

### 依赖装配（h3-orbital-docking-yard-assembly）

提交 actionIds。执行公开前置条件与效果，达到所有目标且不超过预算；允许交换独立动作。

能力：依赖装配；形式：actions；证据：state-machine。


```json
{
  "input": {
    "initialFacts": [],
    "initialModules": [],
    "actions": [
      {
        "id": "place:solar-west",
        "label": "安装 solar-west",
        "requires": [
          "present:hub"
        ],
        "forbids": [
          "present:solar-west"
        ],
        "adds": [
          "present:solar-west"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "solar-west",
          "visible": true
        }
      },
      {
        "id": "place:hub",
        "label": "安装 hub",
        "requires": [
          "present:platform"
        ],
        "forbids": [
          "present:hub"
        ],
        "adds": [
          "present:hub"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "hub",
          "visible": true
        }
      },
      {
        "id": "place:airlock",
        "label": "安装 airlock",
        "requires": [
          "present:hub"
        ],
        "forbids": [
          "present:airlock"
        ],
        "adds": [
          "present:airlock"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "airlock",
          "visible": true
        }
      },
      {
        "id": "place:shuttle",
        "label": "安装 shuttle",
        "requires": [
          "present:platform"
        ],
        "forbids": [
          "present:shuttle"
        ],
        "adds": [
          "present:shuttle"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "shuttle",
          "visible": true
        }
      },
      {
        "id": "place:cargo-pod",
        "label": "安装 cargo-pod",
        "requires": [
          "present:platform"
        ],
        "forbids": [
          "present:cargo-pod"
        ],
        "adds": [
          "present:cargo-pod"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cargo-pod",
          "visible": true
        }
      },
      {
        "id": "place:platform",
        "label": "安装 platform",
        "requires": [],
        "forbids": [
          "present:platform"
        ],
        "adds": [
          "present:platform"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "platform",
          "visible": true
        }
      },
      {
        "id": "place:solar-east",
        "label": "安装 solar-east",
        "requires": [
          "present:hub"
        ],
        "forbids": [
          "present:solar-east"
        ],
        "adds": [
          "present:solar-east"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "solar-east",
          "visible": true
        }
      },
      {
        "id": "place:dock-arm-east",
        "label": "安装 dock-arm-east",
        "requires": [
          "present:hub"
        ],
        "forbids": [
          "present:dock-arm-east"
        ],
        "adds": [
          "present:dock-arm-east"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "dock-arm-east",
          "visible": true
        }
      },
      {
        "id": "place:crane-boom",
        "label": "安装 crane-boom",
        "requires": [
          "present:crane-base"
        ],
        "forbids": [
          "present:crane-boom"
        ],
        "adds": [
          "present:crane-boom"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "crane-boom",
          "visible": true
        }
      },
      {
        "id": "place:crane-base",
        "label": "安装 crane-base",
        "requires": [
          "present:platform"
        ],
        "forbids": [
          "present:crane-base"
        ],
        "adds": [
          "present:crane-base"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "crane-base",
          "visible": true
        }
      },
      {
        "id": "place:dock-arm-west",
        "label": "安装 dock-arm-west",
        "requires": [
          "present:hub"
        ],
        "forbids": [
          "present:dock-arm-west"
        ],
        "adds": [
          "present:dock-arm-west"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "dock-arm-west",
          "visible": true
        }
      }
    ],
    "goalFacts": [
      "present:platform",
      "present:hub",
      "present:airlock",
      "present:solar-west",
      "present:solar-east",
      "present:dock-arm-west",
      "present:dock-arm-east",
      "present:shuttle",
      "present:crane-base",
      "present:crane-boom",
      "present:cargo-pod"
    ],
    "budget": 11,
    "semantics": "requires must hold; forbids must be absent; effects apply in order; unit action cost"
  },
  "answer": {
    "actionIds": [
      "place:platform",
      "place:hub",
      "place:solar-west",
      "place:airlock",
      "place:shuttle",
      "place:cargo-pod",
      "place:solar-east",
      "place:dock-arm-east",
      "place:crane-base",
      "place:crane-boom",
      "place:dock-arm-west"
    ]
  }
}
```

### 依赖拆解（h3-orbital-docking-yard-disassembly）

提交 actionIds。执行公开前置条件与效果，达到所有目标且不超过预算；允许交换独立动作。

能力：依赖拆解；形式：actions；证据：state-machine。


```json
{
  "input": {
    "initialFacts": [
      "present:platform",
      "present:hub",
      "present:airlock",
      "present:dock-arm-west",
      "present:dock-arm-east",
      "present:solar-west",
      "present:solar-east",
      "present:shuttle",
      "present:crane-base",
      "present:crane-boom",
      "present:cargo-pod"
    ],
    "initialModules": [
      "platform",
      "hub",
      "airlock",
      "dock-arm-west",
      "dock-arm-east",
      "solar-west",
      "solar-east",
      "shuttle",
      "crane-base",
      "crane-boom",
      "cargo-pod"
    ],
    "actions": [
      {
        "id": "remove:solar-west",
        "label": "拆除 solar-west",
        "requires": [
          "present:solar-west"
        ],
        "forbids": [],
        "adds": [
          "removed:solar-west"
        ],
        "deletes": [
          "present:solar-west"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "solar-west",
          "visible": false
        }
      },
      {
        "id": "remove:solar-east",
        "label": "拆除 solar-east",
        "requires": [
          "present:solar-east"
        ],
        "forbids": [],
        "adds": [
          "removed:solar-east"
        ],
        "deletes": [
          "present:solar-east"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "solar-east",
          "visible": false
        }
      },
      {
        "id": "remove:airlock",
        "label": "拆除 airlock",
        "requires": [
          "present:airlock"
        ],
        "forbids": [],
        "adds": [
          "removed:airlock"
        ],
        "deletes": [
          "present:airlock"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "airlock",
          "visible": false
        }
      },
      {
        "id": "remove:crane-base",
        "label": "拆除 crane-base",
        "requires": [
          "present:crane-base"
        ],
        "forbids": [
          "present:crane-boom"
        ],
        "adds": [
          "removed:crane-base"
        ],
        "deletes": [
          "present:crane-base"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "crane-base",
          "visible": false
        }
      },
      {
        "id": "remove:cargo-pod",
        "label": "拆除 cargo-pod",
        "requires": [
          "present:cargo-pod"
        ],
        "forbids": [],
        "adds": [
          "removed:cargo-pod"
        ],
        "deletes": [
          "present:cargo-pod"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "cargo-pod",
          "visible": false
        }
      },
      {
        "id": "remove:dock-arm-east",
        "label": "拆除 dock-arm-east",
        "requires": [
          "present:dock-arm-east"
        ],
        "forbids": [],
        "adds": [
          "removed:dock-arm-east"
        ],
        "deletes": [
          "present:dock-arm-east"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "dock-arm-east",
          "visible": false
        }
      },
      {
        "id": "remove:crane-boom",
        "label": "拆除 crane-boom",
        "requires": [
          "present:crane-boom"
        ],
        "forbids": [],
        "adds": [
          "removed:crane-boom"
        ],
        "deletes": [
          "present:crane-boom"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "crane-boom",
          "visible": false
        }
      },
      {
        "id": "remove:hub",
        "label": "拆除 hub",
        "requires": [
          "present:hub"
        ],
        "forbids": [
          "present:airlock",
          "present:dock-arm-west",
          "present:dock-arm-east",
          "present:solar-west",
          "present:solar-east"
        ],
        "adds": [
          "removed:hub"
        ],
        "deletes": [
          "present:hub"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "hub",
          "visible": false
        }
      },
      {
        "id": "remove:dock-arm-west",
        "label": "拆除 dock-arm-west",
        "requires": [
          "present:dock-arm-west"
        ],
        "forbids": [],
        "adds": [
          "removed:dock-arm-west"
        ],
        "deletes": [
          "present:dock-arm-west"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "dock-arm-west",
          "visible": false
        }
      },
      {
        "id": "remove:platform",
        "label": "拆除 platform",
        "requires": [
          "present:platform"
        ],
        "forbids": [
          "present:hub",
          "present:shuttle",
          "present:crane-base",
          "present:cargo-pod"
        ],
        "adds": [
          "removed:platform"
        ],
        "deletes": [
          "present:platform"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "platform",
          "visible": false
        }
      },
      {
        "id": "remove:shuttle",
        "label": "拆除 shuttle",
        "requires": [
          "present:shuttle"
        ],
        "forbids": [],
        "adds": [
          "removed:shuttle"
        ],
        "deletes": [
          "present:shuttle"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "shuttle",
          "visible": false
        }
      }
    ],
    "goalFacts": [
      "removed:cargo-pod",
      "removed:crane-boom",
      "removed:crane-base",
      "removed:shuttle",
      "removed:dock-arm-east",
      "removed:dock-arm-west",
      "removed:solar-east",
      "removed:solar-west",
      "removed:airlock",
      "removed:hub",
      "removed:platform"
    ],
    "budget": 11,
    "semantics": "requires must hold; forbids must be absent; effects apply in order; unit action cost"
  },
  "answer": {
    "actionIds": [
      "remove:solar-west",
      "remove:solar-east",
      "remove:airlock",
      "remove:cargo-pod",
      "remove:dock-arm-east",
      "remove:crane-boom",
      "remove:crane-base",
      "remove:dock-arm-west",
      "remove:hub",
      "remove:shuttle",
      "remove:platform"
    ]
  }
}
```

### 承载维修（h3-orbital-docking-yard-service-repair）

提交 actionIds。执行公开前置条件与效果，达到所有目标且不超过预算；允许交换独立动作。

能力：承载维修；形式：actions；证据：state-machine。


```json
{
  "input": {
    "initialFacts": [
      "fault:airlock",
      "closed:airlock"
    ],
    "initialModules": [
      "platform",
      "hub",
      "airlock",
      "dock-arm-west",
      "dock-arm-east",
      "solar-west",
      "solar-east",
      "shuttle",
      "crane-base",
      "crane-boom",
      "cargo-pod"
    ],
    "actions": [
      {
        "id": "verify:airlock",
        "label": "verify airlock",
        "requires": [
          "done:replace:airlock"
        ],
        "forbids": [
          "done:verify:airlock"
        ],
        "adds": [
          "done:verify:airlock"
        ],
        "deletes": [
          "fault:airlock"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "airlock"
        }
      },
      {
        "id": "remove:airlock",
        "label": "remove airlock",
        "requires": [
          "done:open:airlock"
        ],
        "forbids": [
          "done:remove:airlock"
        ],
        "adds": [
          "done:remove:airlock"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "airlock",
          "visible": false
        }
      },
      {
        "id": "open:airlock",
        "label": "open airlock",
        "requires": [
          "done:support:airlock"
        ],
        "forbids": [
          "done:open:airlock"
        ],
        "adds": [
          "done:open:airlock"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "airlock"
        }
      },
      {
        "id": "replace:airlock",
        "label": "replace airlock",
        "requires": [
          "done:remove:airlock"
        ],
        "forbids": [
          "done:replace:airlock"
        ],
        "adds": [
          "done:replace:airlock"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "airlock",
          "visible": true
        }
      },
      {
        "id": "close:airlock",
        "label": "close airlock",
        "requires": [
          "done:verify:airlock"
        ],
        "forbids": [
          "done:close:airlock"
        ],
        "adds": [
          "done:close:airlock"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "airlock"
        }
      },
      {
        "id": "support:airlock",
        "label": "support airlock",
        "requires": [
          "fault:airlock"
        ],
        "forbids": [
          "done:support:airlock"
        ],
        "adds": [
          "done:support:airlock"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "airlock"
        }
      },
      {
        "id": "release:airlock",
        "label": "release airlock",
        "requires": [
          "done:close:airlock"
        ],
        "forbids": [
          "done:release:airlock"
        ],
        "adds": [
          "done:release:airlock",
          "repaired:airlock"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "airlock"
        }
      }
    ],
    "goalFacts": [
      "repaired:airlock"
    ],
    "budget": 7,
    "semantics": "requires must hold; forbids must be absent; effects apply in order; unit action cost"
  },
  "answer": {
    "actionIds": [
      "support:airlock",
      "open:airlock",
      "remove:airlock",
      "replace:airlock",
      "verify:airlock",
      "close:airlock",
      "release:airlock"
    ]
  }
}
```

### 复合编辑验证（h3-orbital-docking-yard-compound-edit）

提交 actionIds。执行公开前置条件与效果，达到所有目标且不超过预算；允许交换独立动作。

能力：复合编辑验证；形式：actions；证据：state-machine。


```json
{
  "input": {
    "initialFacts": [
      "fault:airlock",
      "closed:airlock"
    ],
    "initialModules": [
      "platform",
      "hub",
      "airlock",
      "dock-arm-west",
      "dock-arm-east",
      "solar-west",
      "solar-east",
      "shuttle",
      "crane-base",
      "crane-boom",
      "cargo-pod"
    ],
    "actions": [
      {
        "id": "verify:airlock",
        "label": "verify airlock",
        "requires": [
          "done:recolor:airlock"
        ],
        "forbids": [
          "done:verify:airlock"
        ],
        "adds": [
          "done:verify:airlock"
        ],
        "deletes": [
          "fault:airlock"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "airlock"
        }
      },
      {
        "id": "open:airlock",
        "label": "open airlock",
        "requires": [
          "done:support:airlock"
        ],
        "forbids": [
          "done:open:airlock"
        ],
        "adds": [
          "done:open:airlock"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "airlock"
        }
      },
      {
        "id": "close:airlock",
        "label": "close airlock",
        "requires": [
          "done:verify:airlock"
        ],
        "forbids": [
          "done:close:airlock"
        ],
        "adds": [
          "done:close:airlock"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "airlock"
        }
      },
      {
        "id": "support:airlock",
        "label": "support airlock",
        "requires": [
          "fault:airlock"
        ],
        "forbids": [
          "done:support:airlock"
        ],
        "adds": [
          "done:support:airlock"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "airlock"
        }
      },
      {
        "id": "recolor:airlock",
        "label": "recolor airlock",
        "requires": [
          "done:open:airlock"
        ],
        "forbids": [
          "done:recolor:airlock"
        ],
        "adds": [
          "done:recolor:airlock"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "airlock",
          "color": "#ea7635"
        }
      },
      {
        "id": "release:airlock",
        "label": "release airlock",
        "requires": [
          "done:close:airlock"
        ],
        "forbids": [
          "done:release:airlock"
        ],
        "adds": [
          "done:release:airlock",
          "repaired:airlock"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "airlock"
        }
      }
    ],
    "goalFacts": [
      "repaired:airlock"
    ],
    "budget": 6,
    "semantics": "requires must hold; forbids must be absent; effects apply in order; unit action cost"
  },
  "answer": {
    "actionIds": [
      "support:airlock",
      "open:airlock",
      "recolor:airlock",
      "verify:airlock",
      "close:airlock",
      "release:airlock"
    ]
  }
}
```

### 跨区域联合维修（h3-orbital-docking-yard-multi-fault）

提交 actionIds。执行公开前置条件与效果，达到所有目标且不超过预算；允许交换独立动作。

能力：跨区域联合维修；形式：actions；证据：state-machine。


```json
{
  "input": {
    "initialFacts": [
      "fault:shuttle",
      "closed:shuttle",
      "fault:crane-base",
      "closed:crane-base",
      "fault:crane-boom",
      "closed:crane-boom",
      "fault:cargo-pod",
      "closed:cargo-pod"
    ],
    "initialModules": [
      "platform",
      "hub",
      "airlock",
      "dock-arm-west",
      "dock-arm-east",
      "solar-west",
      "solar-east",
      "shuttle",
      "crane-base",
      "crane-boom",
      "cargo-pod"
    ],
    "actions": [
      {
        "id": "verify:crane-boom",
        "label": "verify crane-boom",
        "requires": [
          "done:replace:crane-boom"
        ],
        "forbids": [
          "done:verify:crane-boom"
        ],
        "adds": [
          "done:verify:crane-boom"
        ],
        "deletes": [
          "fault:crane-boom"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "crane-boom"
        }
      },
      {
        "id": "open:cargo-pod",
        "label": "open cargo-pod",
        "requires": [
          "done:support:cargo-pod"
        ],
        "forbids": [
          "done:open:cargo-pod"
        ],
        "adds": [
          "done:open:cargo-pod"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cargo-pod"
        }
      },
      {
        "id": "support:crane-boom",
        "label": "support crane-boom",
        "requires": [
          "fault:crane-boom"
        ],
        "forbids": [
          "done:support:crane-boom"
        ],
        "adds": [
          "done:support:crane-boom"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "crane-boom"
        }
      },
      {
        "id": "release:cargo-pod",
        "label": "release cargo-pod",
        "requires": [
          "done:close:cargo-pod"
        ],
        "forbids": [
          "done:release:cargo-pod"
        ],
        "adds": [
          "done:release:cargo-pod",
          "repaired:cargo-pod"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cargo-pod"
        }
      },
      {
        "id": "replace:crane-base",
        "label": "replace crane-base",
        "requires": [
          "done:remove:crane-base"
        ],
        "forbids": [
          "done:replace:crane-base"
        ],
        "adds": [
          "done:replace:crane-base"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "crane-base",
          "visible": true
        }
      },
      {
        "id": "support:crane-base",
        "label": "support crane-base",
        "requires": [
          "fault:crane-base"
        ],
        "forbids": [
          "done:support:crane-base"
        ],
        "adds": [
          "done:support:crane-base"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "crane-base"
        }
      },
      {
        "id": "remove:crane-base",
        "label": "remove crane-base",
        "requires": [
          "done:open:crane-base"
        ],
        "forbids": [
          "done:remove:crane-base"
        ],
        "adds": [
          "done:remove:crane-base"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "crane-base",
          "visible": false
        }
      },
      {
        "id": "open:crane-base",
        "label": "open crane-base",
        "requires": [
          "done:support:crane-base"
        ],
        "forbids": [
          "done:open:crane-base"
        ],
        "adds": [
          "done:open:crane-base"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "crane-base"
        }
      },
      {
        "id": "support:cargo-pod",
        "label": "support cargo-pod",
        "requires": [
          "fault:cargo-pod"
        ],
        "forbids": [
          "done:support:cargo-pod"
        ],
        "adds": [
          "done:support:cargo-pod"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cargo-pod"
        }
      },
      {
        "id": "remove:cargo-pod",
        "label": "remove cargo-pod",
        "requires": [
          "done:open:cargo-pod"
        ],
        "forbids": [
          "done:remove:cargo-pod"
        ],
        "adds": [
          "done:remove:cargo-pod"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cargo-pod",
          "visible": false
        }
      },
      {
        "id": "release:crane-base",
        "label": "release crane-base",
        "requires": [
          "done:close:crane-base"
        ],
        "forbids": [
          "done:release:crane-base"
        ],
        "adds": [
          "done:release:crane-base",
          "repaired:crane-base"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "crane-base"
        }
      },
      {
        "id": "replace:cargo-pod",
        "label": "replace cargo-pod",
        "requires": [
          "done:remove:cargo-pod"
        ],
        "forbids": [
          "done:replace:cargo-pod"
        ],
        "adds": [
          "done:replace:cargo-pod"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cargo-pod",
          "visible": true
        }
      },
      {
        "id": "verify:shuttle",
        "label": "verify shuttle",
        "requires": [
          "done:replace:shuttle"
        ],
        "forbids": [
          "done:verify:shuttle"
        ],
        "adds": [
          "done:verify:shuttle"
        ],
        "deletes": [
          "fault:shuttle"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "shuttle"
        }
      },
      {
        "id": "support:shuttle",
        "label": "support shuttle",
        "requires": [
          "fault:shuttle"
        ],
        "forbids": [
          "done:support:shuttle"
        ],
        "adds": [
          "done:support:shuttle"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "shuttle"
        }
      },
      {
        "id": "close:shuttle",
        "label": "close shuttle",
        "requires": [
          "done:verify:shuttle"
        ],
        "forbids": [
          "done:close:shuttle"
        ],
        "adds": [
          "done:close:shuttle"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "shuttle"
        }
      },
      {
        "id": "close:crane-boom",
        "label": "close crane-boom",
        "requires": [
          "done:verify:crane-boom"
        ],
        "forbids": [
          "done:close:crane-boom"
        ],
        "adds": [
          "done:close:crane-boom"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "crane-boom"
        }
      },
      {
        "id": "replace:shuttle",
        "label": "replace shuttle",
        "requires": [
          "done:remove:shuttle"
        ],
        "forbids": [
          "done:replace:shuttle"
        ],
        "adds": [
          "done:replace:shuttle"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "shuttle",
          "visible": true
        }
      },
      {
        "id": "verify:cargo-pod",
        "label": "verify cargo-pod",
        "requires": [
          "done:replace:cargo-pod"
        ],
        "forbids": [
          "done:verify:cargo-pod"
        ],
        "adds": [
          "done:verify:cargo-pod"
        ],
        "deletes": [
          "fault:cargo-pod"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "cargo-pod"
        }
      },
      {
        "id": "verify:crane-base",
        "label": "verify crane-base",
        "requires": [
          "done:replace:crane-base"
        ],
        "forbids": [
          "done:verify:crane-base"
        ],
        "adds": [
          "done:verify:crane-base"
        ],
        "deletes": [
          "fault:crane-base"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "crane-base"
        }
      },
      {
        "id": "close:cargo-pod",
        "label": "close cargo-pod",
        "requires": [
          "done:verify:cargo-pod"
        ],
        "forbids": [
          "done:close:cargo-pod"
        ],
        "adds": [
          "done:close:cargo-pod"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cargo-pod"
        }
      },
      {
        "id": "release:shuttle",
        "label": "release shuttle",
        "requires": [
          "done:close:shuttle"
        ],
        "forbids": [
          "done:release:shuttle"
        ],
        "adds": [
          "done:release:shuttle",
          "repaired:shuttle"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "shuttle"
        }
      },
      {
        "id": "remove:crane-boom",
        "label": "remove crane-boom",
        "requires": [
          "done:open:crane-boom"
        ],
        "forbids": [
          "done:remove:crane-boom"
        ],
        "adds": [
          "done:remove:crane-boom"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "crane-boom",
          "visible": false
        }
      },
      {
        "id": "open:shuttle",
        "label": "open shuttle",
        "requires": [
          "done:support:shuttle"
        ],
        "forbids": [
          "done:open:shuttle"
        ],
        "adds": [
          "done:open:shuttle"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "shuttle"
        }
      },
      {
        "id": "release:crane-boom",
        "label": "release crane-boom",
        "requires": [
          "done:close:crane-boom"
        ],
        "forbids": [
          "done:release:crane-boom"
        ],
        "adds": [
          "done:release:crane-boom",
          "repaired:crane-boom"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "crane-boom"
        }
      },
      {
        "id": "open:crane-boom",
        "label": "open crane-boom",
        "requires": [
          "done:support:crane-boom"
        ],
        "forbids": [
          "done:open:crane-boom"
        ],
        "adds": [
          "done:open:crane-boom"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "crane-boom"
        }
      },
      {
        "id": "close:crane-base",
        "label": "close crane-base",
        "requires": [
          "done:verify:crane-base"
        ],
        "forbids": [
          "done:close:crane-base"
        ],
        "adds": [
          "done:close:crane-base"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "crane-base"
        }
      },
      {
        "id": "replace:crane-boom",
        "label": "replace crane-boom",
        "requires": [
          "done:remove:crane-boom"
        ],
        "forbids": [
          "done:replace:crane-boom"
        ],
        "adds": [
          "done:replace:crane-boom"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "crane-boom",
          "visible": true
        }
      },
      {
        "id": "remove:shuttle",
        "label": "remove shuttle",
        "requires": [
          "done:open:shuttle"
        ],
        "forbids": [
          "done:remove:shuttle"
        ],
        "adds": [
          "done:remove:shuttle"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "shuttle",
          "visible": false
        }
      }
    ],
    "goalFacts": [
      "repaired:shuttle",
      "repaired:crane-base",
      "repaired:crane-boom",
      "repaired:cargo-pod"
    ],
    "budget": 28,
    "semantics": "requires must hold; forbids must be absent; effects apply in order; unit action cost"
  },
  "answer": {
    "actionIds": [
      "support:crane-boom",
      "support:crane-base",
      "open:crane-base",
      "remove:crane-base",
      "replace:crane-base",
      "support:cargo-pod",
      "open:cargo-pod",
      "remove:cargo-pod",
      "replace:cargo-pod",
      "support:shuttle",
      "verify:cargo-pod",
      "verify:crane-base",
      "close:cargo-pod",
      "release:cargo-pod",
      "open:shuttle",
      "open:crane-boom",
      "remove:crane-boom",
      "close:crane-base",
      "release:crane-base",
      "replace:crane-boom",
      "verify:crane-boom",
      "close:crane-boom",
      "release:crane-boom",
      "remove:shuttle",
      "replace:shuttle",
      "verify:shuttle",
      "close:shuttle",
      "release:shuttle"
    ]
  }
}
```

### 多工位资源调度（h3-orbital-docking-yard-scheduling）

为所有工单提交整数 starts，满足先后关系、独占工位及截止时间。

能力：多工位资源调度；形式：schedule；证据：resource-schedule。


```json
{
  "input": {
    "jobs": [
      {
        "id": "job-0",
        "module": "platform",
        "duration": 1,
        "resource": "test-bench",
        "after": []
      },
      {
        "id": "job-1",
        "module": "hub",
        "duration": 3,
        "resource": "technician",
        "after": []
      },
      {
        "id": "job-2",
        "module": "airlock",
        "duration": 3,
        "resource": "test-bench",
        "after": [
          "job-0"
        ]
      },
      {
        "id": "job-3",
        "module": "dock-arm-west",
        "duration": 1,
        "resource": "technician",
        "after": [
          "job-1"
        ]
      },
      {
        "id": "job-4",
        "module": "dock-arm-east",
        "duration": 3,
        "resource": "test-bench",
        "after": [
          "job-2"
        ]
      },
      {
        "id": "job-5",
        "module": "solar-west",
        "duration": 2,
        "resource": "technician",
        "after": [
          "job-3"
        ]
      },
      {
        "id": "job-6",
        "module": "solar-east",
        "duration": 1,
        "resource": "test-bench",
        "after": [
          "job-4"
        ]
      },
      {
        "id": "job-7",
        "module": "shuttle",
        "duration": 3,
        "resource": "technician",
        "after": [
          "job-5"
        ]
      },
      {
        "id": "job-8",
        "module": "crane-base",
        "duration": 3,
        "resource": "test-bench",
        "after": [
          "job-6"
        ]
      },
      {
        "id": "job-9",
        "module": "crane-boom",
        "duration": 3,
        "resource": "technician",
        "after": [
          "job-7"
        ]
      }
    ],
    "deadline": 12
  },
  "answer": {
    "starts": {
      "job-0": 0,
      "job-1": 0,
      "job-2": 1,
      "job-3": 3,
      "job-4": 4,
      "job-5": 4,
      "job-6": 7,
      "job-7": 6,
      "job-8": 8,
      "job-9": 9
    }
  }
}
```

### 检查后条件策略（h3-orbital-docking-yard-policy）

提交一个检查及 observation→action 决策表，在所有相容世界中采取正确动作。

能力：检查后条件策略；形式：policy；证据：finite-world。


```json
{
  "input": {
    "module": "airlock",
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

### 局部坐标变换（h3-orbital-docking-yard-local-frame）

将模块局部点通过给定四元数与平移转换为世界点，保留五位小数。

能力：局部坐标变换；形式：single-choice；证据：model-state。

- A：[1,1.8,5.2]
- B：[0,0.8,4.2]
- C：[0,-0.05,-1]

```json
{
  "input": {
    "localPoint": [
      0,
      -0.04999999999999993,
      -1
    ],
    "rotationXYZW": [
      0,
      0,
      0,
      1
    ],
    "translation": [
      0,
      0.85,
      5.2
    ]
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 正交视图投影（h3-orbital-docking-yard-projection）

按公开视图坐标约定，选择该世界点投影后的二维坐标。

能力：正交视图投影；形式：single-choice；证据：model-state。

- A：[5,6]
- B：[0,0]
- C：[5,11]
- D：[11,5]

```json
{
  "input": {
    "view": "front",
    "point": [
      5,
      11,
      -6
    ],
    "convention": "front=(x,y), side=(z,y), top=(x,z)"
  },
  "answer": {
    "choiceId": "C"
  }
}
```

### 空间相对关系（h3-orbital-docking-yard-relative-order）

比较B相对A在指定世界轴上的模块原点坐标。

能力：空间相对关系；形式：single-choice；证据：model-state。

- A：greater
- B：less
- C：equal

```json
{
  "input": {
    "A": {
      "id": "platform",
      "position": [
        0,
        0.2,
        0
      ]
    },
    "B": {
      "id": "cargo-pod",
      "position": [
        0,
        1.05,
        8.3
      ]
    },
    "axis": "x"
  },
  "answer": {
    "choiceId": "C"
  }
}
```

### 约束自由度（h3-orbital-docking-yard-joint-axis）

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
      "id": "west-arm-pivot",
      "name": "west arm pivot",
      "type": "revolute",
      "parent": "hub",
      "child": "dock-arm-west",
      "anchorParent": [
        -4,
        0.39999999999999947,
        0
      ],
      "anchorChild": [
        3.3875,
        -0.3599999999999999,
        0
      ],
      "axis": [
        0,
        1,
        0
      ],
      "limits": [
        -1.2,
        1.2
      ]
    }
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 维修间隙预算（h3-orbital-docking-yard-clearance-margin）

给定理想直槽净宽、工具宽度、单侧安全余量，工具是否满足横向间隙要求？

能力：维修间隙预算；形式：single-choice；证据：model-state。

- A：feasible
- B：blocked

```json
{
  "input": {
    "module": "airlock",
    "aperture": 0.62,
    "toolWidth": 0.65,
    "eachSideMargin": 0
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 载荷力矩（h3-orbital-docking-yard-load-moment）

绕给定原点的载荷力矩r×F是多少？采用右手系，忽略其他力。

能力：载荷力矩；形式：single-choice；证据：model-state。

- A：[0,0,16]
- B：[0,0,0]
- C：[0,-4,0]
- D：[0,0,-16]

```json
{
  "input": {
    "module": "airlock",
    "lever": [
      4,
      1,
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
    "choiceId": "D"
  }
}
```

### 非均匀先验更新（h3-orbital-docking-yard-weighted-posterior）

先验权重未归一化，观测只保留normal和jammed，求jammed后验概率。

能力：非均匀先验更新；形式：single-choice；证据：finite-world。

- A：0.1111111111111111
- B：0
- C：1
- D：0.25

```json
{
  "input": {
    "module": "airlock",
    "worlds": [
      "normal",
      "jammed",
      "loose"
    ],
    "weights": [
      3,
      1,
      5
    ],
    "compatible": [
      "normal",
      "jammed"
    ]
  },
  "answer": {
    "choiceId": "D"
  }
}
```

### 风险最小决策（h3-orbital-docking-yard-expected-loss）

继续运行期望损失=p×failureLoss，预防维修损失=repairCost，选择损失较低者；并列选继续。

能力：风险最小决策；形式：single-choice；证据：finite-world。

- A：continue
- B：repair

```json
{
  "input": {
    "faultProbability": 0.1,
    "repairCost": 4,
    "failureLoss": 16,
    "module": "airlock"
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 轨迹阈值判定（h3-orbital-docking-yard-trace-threshold）

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
        "displacement": 0.01066908821350834
      },
      {
        "time": 0.10833333333333334,
        "displacement": 0.002672615059164524
      },
      {
        "time": 0.20833333333333334,
        "displacement": 0.00059642136226781
      },
      {
        "time": 0.30833333333333335,
        "displacement": 0.00012128014725706866
      },
      {
        "time": 0.4083333333333333,
        "displacement": 0.00000691824823787065
      },
      {
        "time": 0.5083333333333333,
        "displacement": 0.00000691824823787065
      },
      {
        "time": 0.6083333333333333,
        "displacement": 0.00000691824823787065
      },
      {
        "time": 0.7083333333333334,
        "displacement": 0.0000030648613291221717
      },
      {
        "time": 0.8083333333333333,
        "displacement": 0.0000030648613291221717
      },
      {
        "time": 0.9083333333333333,
        "displacement": 0.0000030648613291221717
      },
      {
        "time": 1,
        "displacement": 0.0000030648613291221717
      }
    ],
    "threshold": 0.008535270570806672
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 安全联锁维修（h3-orbital-docking-yard-guarded-repair）

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
        "id": "release:airlock",
        "label": "release airlock",
        "requires": [
          "done:relock:airlock"
        ],
        "forbids": [
          "done:release:airlock"
        ],
        "adds": [
          "done:release:airlock",
          "ready:airlock",
          "tool:free"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "airlock"
        }
      },
      {
        "id": "relock:airlock",
        "label": "relock airlock",
        "requires": [
          "done:verify:airlock"
        ],
        "forbids": [
          "done:relock:airlock"
        ],
        "adds": [
          "done:relock:airlock"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "airlock"
        }
      },
      {
        "id": "verify:airlock",
        "label": "verify airlock",
        "requires": [
          "done:replace:airlock"
        ],
        "forbids": [
          "done:verify:airlock"
        ],
        "adds": [
          "done:verify:airlock"
        ],
        "deletes": [
          "fault:airlock",
          "misaligned:airlock"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "airlock"
        }
      },
      {
        "id": "replace:airlock",
        "label": "replace airlock",
        "requires": [
          "done:unlock:airlock"
        ],
        "forbids": [
          "done:replace:airlock"
        ],
        "adds": [
          "done:replace:airlock"
        ],
        "deletes": [],
        "cost": 2,
        "visual": {
          "moduleId": "airlock"
        }
      },
      {
        "id": "unlock:airlock",
        "label": "unlock airlock",
        "requires": [
          "done:support:airlock"
        ],
        "forbids": [
          "done:unlock:airlock"
        ],
        "adds": [
          "done:unlock:airlock"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "airlock"
        }
      },
      {
        "id": "support:airlock",
        "label": "support airlock",
        "requires": [
          "done:isolate:airlock"
        ],
        "forbids": [
          "done:support:airlock"
        ],
        "adds": [
          "done:support:airlock"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "airlock"
        }
      },
      {
        "id": "isolate:airlock",
        "label": "isolate airlock",
        "requires": [
          "tool:free",
          "fault:airlock"
        ],
        "forbids": [
          "done:isolate:airlock"
        ],
        "adds": [
          "done:isolate:airlock"
        ],
        "deletes": [
          "tool:free"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "airlock"
        }
      }
    ],
    "initialFacts": [
      "tool:free",
      "fault:airlock"
    ],
    "initialModules": [
      "platform",
      "hub",
      "airlock",
      "dock-arm-west",
      "dock-arm-east",
      "solar-west",
      "solar-east",
      "shuttle",
      "crane-base",
      "crane-boom",
      "cargo-pod"
    ],
    "goalFacts": [
      "ready:airlock"
    ],
    "absentFacts": [
      "unverified"
    ],
    "budget": 8
  },
  "answer": {
    "actionIds": [
      "isolate:airlock",
      "support:airlock",
      "unlock:airlock",
      "replace:airlock",
      "verify:airlock",
      "relock:airlock",
      "release:airlock"
    ]
  }
}
```

### 失败状态回退（h3-orbital-docking-yard-rollback）

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
        "id": "resume:airlock",
        "label": "resume airlock",
        "requires": [
          "done:verify:airlock"
        ],
        "forbids": [
          "done:resume:airlock"
        ],
        "adds": [
          "done:resume:airlock",
          "ready:airlock",
          "tool:free"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "airlock"
        }
      },
      {
        "id": "verify:airlock",
        "label": "verify airlock",
        "requires": [
          "done:align:airlock"
        ],
        "forbids": [
          "done:verify:airlock"
        ],
        "adds": [
          "done:verify:airlock"
        ],
        "deletes": [
          "fault:airlock",
          "misaligned:airlock"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "airlock"
        }
      },
      {
        "id": "align:airlock",
        "label": "align airlock",
        "requires": [
          "done:undo:airlock"
        ],
        "forbids": [
          "done:align:airlock"
        ],
        "adds": [
          "done:align:airlock"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "airlock",
          "visible": true
        }
      },
      {
        "id": "undo:airlock",
        "label": "undo airlock",
        "requires": [
          "done:isolate:airlock"
        ],
        "forbids": [
          "done:undo:airlock"
        ],
        "adds": [
          "done:undo:airlock"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "airlock",
          "visible": false
        }
      },
      {
        "id": "isolate:airlock",
        "label": "isolate airlock",
        "requires": [
          "tool:free",
          "fault:airlock"
        ],
        "forbids": [
          "done:isolate:airlock"
        ],
        "adds": [
          "done:isolate:airlock"
        ],
        "deletes": [
          "tool:free"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "airlock"
        }
      }
    ],
    "initialFacts": [
      "tool:free",
      "fault:airlock",
      "misaligned:airlock"
    ],
    "initialModules": [
      "platform",
      "hub",
      "airlock",
      "dock-arm-west",
      "dock-arm-east",
      "solar-west",
      "solar-east",
      "shuttle",
      "crane-base",
      "crane-boom",
      "cargo-pod"
    ],
    "goalFacts": [
      "ready:airlock"
    ],
    "absentFacts": [
      "unverified"
    ],
    "budget": 5
  },
  "answer": {
    "actionIds": [
      "isolate:airlock",
      "undo:airlock",
      "align:airlock",
      "verify:airlock",
      "resume:airlock"
    ]
  }
}
```

### 共享工具协同维修（h3-orbital-docking-yard-resource-repair）

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
        "id": "release:cargo-pod",
        "label": "release cargo-pod",
        "requires": [
          "done:relock:cargo-pod"
        ],
        "forbids": [
          "done:release:cargo-pod"
        ],
        "adds": [
          "done:release:cargo-pod",
          "ready:cargo-pod",
          "tool:free"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cargo-pod"
        }
      },
      {
        "id": "relock:cargo-pod",
        "label": "relock cargo-pod",
        "requires": [
          "done:verify:cargo-pod"
        ],
        "forbids": [
          "done:relock:cargo-pod"
        ],
        "adds": [
          "done:relock:cargo-pod"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cargo-pod"
        }
      },
      {
        "id": "verify:cargo-pod",
        "label": "verify cargo-pod",
        "requires": [
          "done:replace:cargo-pod"
        ],
        "forbids": [
          "done:verify:cargo-pod"
        ],
        "adds": [
          "done:verify:cargo-pod"
        ],
        "deletes": [
          "fault:cargo-pod",
          "misaligned:cargo-pod"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "cargo-pod"
        }
      },
      {
        "id": "replace:cargo-pod",
        "label": "replace cargo-pod",
        "requires": [
          "done:unlock:cargo-pod"
        ],
        "forbids": [
          "done:replace:cargo-pod"
        ],
        "adds": [
          "done:replace:cargo-pod"
        ],
        "deletes": [],
        "cost": 2,
        "visual": {
          "moduleId": "cargo-pod"
        }
      },
      {
        "id": "unlock:cargo-pod",
        "label": "unlock cargo-pod",
        "requires": [
          "done:support:cargo-pod"
        ],
        "forbids": [
          "done:unlock:cargo-pod"
        ],
        "adds": [
          "done:unlock:cargo-pod"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cargo-pod"
        }
      },
      {
        "id": "support:cargo-pod",
        "label": "support cargo-pod",
        "requires": [
          "done:isolate:cargo-pod"
        ],
        "forbids": [
          "done:support:cargo-pod"
        ],
        "adds": [
          "done:support:cargo-pod"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "cargo-pod"
        }
      },
      {
        "id": "isolate:cargo-pod",
        "label": "isolate cargo-pod",
        "requires": [
          "tool:free",
          "fault:cargo-pod"
        ],
        "forbids": [
          "done:isolate:cargo-pod"
        ],
        "adds": [
          "done:isolate:cargo-pod"
        ],
        "deletes": [
          "tool:free"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "cargo-pod"
        }
      },
      {
        "id": "release:crane-boom",
        "label": "release crane-boom",
        "requires": [
          "done:relock:crane-boom"
        ],
        "forbids": [
          "done:release:crane-boom"
        ],
        "adds": [
          "done:release:crane-boom",
          "ready:crane-boom",
          "tool:free"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "crane-boom"
        }
      },
      {
        "id": "relock:crane-boom",
        "label": "relock crane-boom",
        "requires": [
          "done:verify:crane-boom"
        ],
        "forbids": [
          "done:relock:crane-boom"
        ],
        "adds": [
          "done:relock:crane-boom"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "crane-boom"
        }
      },
      {
        "id": "verify:crane-boom",
        "label": "verify crane-boom",
        "requires": [
          "done:replace:crane-boom"
        ],
        "forbids": [
          "done:verify:crane-boom"
        ],
        "adds": [
          "done:verify:crane-boom"
        ],
        "deletes": [
          "fault:crane-boom",
          "misaligned:crane-boom"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "crane-boom"
        }
      },
      {
        "id": "replace:crane-boom",
        "label": "replace crane-boom",
        "requires": [
          "done:unlock:crane-boom"
        ],
        "forbids": [
          "done:replace:crane-boom"
        ],
        "adds": [
          "done:replace:crane-boom"
        ],
        "deletes": [],
        "cost": 2,
        "visual": {
          "moduleId": "crane-boom"
        }
      },
      {
        "id": "unlock:crane-boom",
        "label": "unlock crane-boom",
        "requires": [
          "done:support:crane-boom"
        ],
        "forbids": [
          "done:unlock:crane-boom"
        ],
        "adds": [
          "done:unlock:crane-boom"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "crane-boom"
        }
      },
      {
        "id": "support:crane-boom",
        "label": "support crane-boom",
        "requires": [
          "done:isolate:crane-boom"
        ],
        "forbids": [
          "done:support:crane-boom"
        ],
        "adds": [
          "done:support:crane-boom"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "crane-boom"
        }
      },
      {
        "id": "isolate:crane-boom",
        "label": "isolate crane-boom",
        "requires": [
          "tool:free",
          "fault:crane-boom"
        ],
        "forbids": [
          "done:isolate:crane-boom"
        ],
        "adds": [
          "done:isolate:crane-boom"
        ],
        "deletes": [
          "tool:free"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "crane-boom"
        }
      },
      {
        "id": "release:crane-base",
        "label": "release crane-base",
        "requires": [
          "done:relock:crane-base"
        ],
        "forbids": [
          "done:release:crane-base"
        ],
        "adds": [
          "done:release:crane-base",
          "ready:crane-base",
          "tool:free"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "crane-base"
        }
      },
      {
        "id": "relock:crane-base",
        "label": "relock crane-base",
        "requires": [
          "done:verify:crane-base"
        ],
        "forbids": [
          "done:relock:crane-base"
        ],
        "adds": [
          "done:relock:crane-base"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "crane-base"
        }
      },
      {
        "id": "verify:crane-base",
        "label": "verify crane-base",
        "requires": [
          "done:replace:crane-base"
        ],
        "forbids": [
          "done:verify:crane-base"
        ],
        "adds": [
          "done:verify:crane-base"
        ],
        "deletes": [
          "fault:crane-base",
          "misaligned:crane-base"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "crane-base"
        }
      },
      {
        "id": "replace:crane-base",
        "label": "replace crane-base",
        "requires": [
          "done:unlock:crane-base"
        ],
        "forbids": [
          "done:replace:crane-base"
        ],
        "adds": [
          "done:replace:crane-base"
        ],
        "deletes": [],
        "cost": 2,
        "visual": {
          "moduleId": "crane-base"
        }
      },
      {
        "id": "unlock:crane-base",
        "label": "unlock crane-base",
        "requires": [
          "done:support:crane-base"
        ],
        "forbids": [
          "done:unlock:crane-base"
        ],
        "adds": [
          "done:unlock:crane-base"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "crane-base"
        }
      },
      {
        "id": "support:crane-base",
        "label": "support crane-base",
        "requires": [
          "done:isolate:crane-base"
        ],
        "forbids": [
          "done:support:crane-base"
        ],
        "adds": [
          "done:support:crane-base"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "crane-base"
        }
      },
      {
        "id": "isolate:crane-base",
        "label": "isolate crane-base",
        "requires": [
          "tool:free",
          "fault:crane-base"
        ],
        "forbids": [
          "done:isolate:crane-base"
        ],
        "adds": [
          "done:isolate:crane-base"
        ],
        "deletes": [
          "tool:free"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "crane-base"
        }
      },
      {
        "id": "release:shuttle",
        "label": "release shuttle",
        "requires": [
          "done:relock:shuttle"
        ],
        "forbids": [
          "done:release:shuttle"
        ],
        "adds": [
          "done:release:shuttle",
          "ready:shuttle",
          "tool:free"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "shuttle"
        }
      },
      {
        "id": "relock:shuttle",
        "label": "relock shuttle",
        "requires": [
          "done:verify:shuttle"
        ],
        "forbids": [
          "done:relock:shuttle"
        ],
        "adds": [
          "done:relock:shuttle"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "shuttle"
        }
      },
      {
        "id": "verify:shuttle",
        "label": "verify shuttle",
        "requires": [
          "done:replace:shuttle"
        ],
        "forbids": [
          "done:verify:shuttle"
        ],
        "adds": [
          "done:verify:shuttle"
        ],
        "deletes": [
          "fault:shuttle",
          "misaligned:shuttle"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "shuttle"
        }
      },
      {
        "id": "replace:shuttle",
        "label": "replace shuttle",
        "requires": [
          "done:unlock:shuttle"
        ],
        "forbids": [
          "done:replace:shuttle"
        ],
        "adds": [
          "done:replace:shuttle"
        ],
        "deletes": [],
        "cost": 2,
        "visual": {
          "moduleId": "shuttle"
        }
      },
      {
        "id": "unlock:shuttle",
        "label": "unlock shuttle",
        "requires": [
          "done:support:shuttle"
        ],
        "forbids": [
          "done:unlock:shuttle"
        ],
        "adds": [
          "done:unlock:shuttle"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "shuttle"
        }
      },
      {
        "id": "support:shuttle",
        "label": "support shuttle",
        "requires": [
          "done:isolate:shuttle"
        ],
        "forbids": [
          "done:support:shuttle"
        ],
        "adds": [
          "done:support:shuttle"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "shuttle"
        }
      },
      {
        "id": "isolate:shuttle",
        "label": "isolate shuttle",
        "requires": [
          "tool:free",
          "fault:shuttle"
        ],
        "forbids": [
          "done:isolate:shuttle"
        ],
        "adds": [
          "done:isolate:shuttle"
        ],
        "deletes": [
          "tool:free"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "shuttle"
        }
      }
    ],
    "initialFacts": [
      "tool:free",
      "fault:shuttle",
      "fault:crane-base",
      "fault:crane-boom",
      "fault:cargo-pod"
    ],
    "initialModules": [
      "platform",
      "hub",
      "airlock",
      "dock-arm-west",
      "dock-arm-east",
      "solar-west",
      "solar-east",
      "shuttle",
      "crane-base",
      "crane-boom",
      "cargo-pod"
    ],
    "goalFacts": [
      "ready:shuttle",
      "ready:crane-base",
      "ready:crane-boom",
      "ready:cargo-pod"
    ],
    "absentFacts": [
      "unverified"
    ],
    "budget": 32
  },
  "answer": {
    "actionIds": [
      "isolate:cargo-pod",
      "support:cargo-pod",
      "unlock:cargo-pod",
      "replace:cargo-pod",
      "verify:cargo-pod",
      "relock:cargo-pod",
      "release:cargo-pod",
      "isolate:crane-boom",
      "support:crane-boom",
      "unlock:crane-boom",
      "replace:crane-boom",
      "verify:crane-boom",
      "relock:crane-boom",
      "release:crane-boom",
      "isolate:crane-base",
      "support:crane-base",
      "unlock:crane-base",
      "replace:crane-base",
      "verify:crane-base",
      "relock:crane-base",
      "release:crane-base",
      "isolate:shuttle",
      "support:shuttle",
      "unlock:shuttle",
      "replace:shuttle",
      "verify:shuttle",
      "relock:shuttle",
      "release:shuttle"
    ]
  }
}
```

### 预算约束检查策略（h3-orbital-docking-yard-budget-policy）

提交预算内、对所有相容世界均正确的检查决策表。

能力：预算约束检查策略；形式：policy；证据：finite-world。


```json
{
  "input": {
    "module": "airlock",
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
        "cost": 2,
        "returns": {
          "nominal": "pass",
          "fault": "fail"
        }
      },
      {
        "id": "thermal",
        "cost": 1,
        "returns": {
          "nominal": "pass",
          "fault": "fail"
        }
      }
    ],
    "budget": 1
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

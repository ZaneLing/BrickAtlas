## D4 月面样品精炼站

### 模块识别（h3-lunar-sample-refinery-identify）

高亮的维修模块对应哪个 ID？

能力：模块识别；形式：single-choice；证据：model-state。

- A：loading-arm
- B：pad
- C：habitat
- D：crusher

```json
{
  "input": {
    "moduleNames": [
      {
        "id": "pad",
        "name": "Lunar refinery pad"
      },
      {
        "id": "habitat",
        "name": "Pressurized control habitat"
      },
      {
        "id": "crusher",
        "name": "Sample crusher"
      },
      {
        "id": "conveyor",
        "name": "Sealed transfer conveyor"
      },
      {
        "id": "centrifuge",
        "name": "Rotary separator"
      },
      {
        "id": "solar-a",
        "name": "North solar wing"
      },
      {
        "id": "solar-b",
        "name": "South solar wing"
      },
      {
        "id": "tank-a",
        "name": "Feedstock tank"
      },
      {
        "id": "tank-b",
        "name": "Product tank"
      },
      {
        "id": "sample-rover",
        "name": "Sample transfer rover"
      },
      {
        "id": "loading-arm",
        "name": "Refinery loading arm"
      },
      {
        "id": "silo",
        "name": "Processed sample silo"
      }
    ]
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 部件计数（h3-lunar-sample-refinery-count）

模块 loading-arm 有多少个可视零件？

能力：部件计数；形式：single-choice；证据：model-state。

- A：11
- B：8
- C：9
- D：7

```json
{
  "input": {
    "parts": [
      {
        "id": "h0001",
        "moduleId": "pad",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0002",
        "moduleId": "pad",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0003",
        "moduleId": "pad",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0004",
        "moduleId": "pad",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0005",
        "moduleId": "pad",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0006",
        "moduleId": "pad",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0007",
        "moduleId": "pad",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0008",
        "moduleId": "pad",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0009",
        "moduleId": "pad",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0010",
        "moduleId": "pad",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0011",
        "moduleId": "pad",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0012",
        "moduleId": "pad",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0013",
        "moduleId": "pad",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0014",
        "moduleId": "pad",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0015",
        "moduleId": "pad",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0016",
        "moduleId": "pad",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0017",
        "moduleId": "pad",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0018",
        "moduleId": "pad",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0019",
        "moduleId": "pad",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0020",
        "moduleId": "pad",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0021",
        "moduleId": "pad",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0022",
        "moduleId": "pad",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0023",
        "moduleId": "pad",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0024",
        "moduleId": "pad",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0025",
        "moduleId": "pad",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0026",
        "moduleId": "pad",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0027",
        "moduleId": "pad",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0028",
        "moduleId": "pad",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0029",
        "moduleId": "pad",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0030",
        "moduleId": "pad",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0031",
        "moduleId": "pad",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0032",
        "moduleId": "pad",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0033",
        "moduleId": "pad",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0034",
        "moduleId": "pad",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0035",
        "moduleId": "pad",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0036",
        "moduleId": "pad",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0037",
        "moduleId": "pad",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0038",
        "moduleId": "pad",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0039",
        "moduleId": "pad",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0040",
        "moduleId": "pad",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0041",
        "moduleId": "pad",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0042",
        "moduleId": "pad",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0043",
        "moduleId": "pad",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0044",
        "moduleId": "pad",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0045",
        "moduleId": "pad",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0046",
        "moduleId": "pad",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0047",
        "moduleId": "pad",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0048",
        "moduleId": "pad",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0049",
        "moduleId": "pad",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0050",
        "moduleId": "pad",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0051",
        "moduleId": "pad",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0052",
        "moduleId": "pad",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0053",
        "moduleId": "pad",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0054",
        "moduleId": "pad",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0055",
        "moduleId": "pad",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0056",
        "moduleId": "pad",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0057",
        "moduleId": "pad",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0058",
        "moduleId": "pad",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0059",
        "moduleId": "pad",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0060",
        "moduleId": "pad",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0061",
        "moduleId": "pad",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0062",
        "moduleId": "pad",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0063",
        "moduleId": "pad",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0064",
        "moduleId": "pad",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0065",
        "moduleId": "pad",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0066",
        "moduleId": "pad",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0067",
        "moduleId": "pad",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0068",
        "moduleId": "pad",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0069",
        "moduleId": "pad",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0070",
        "moduleId": "pad",
        "shape": "plate",
        "color": "#8c99a3"
      },
      {
        "id": "h0071",
        "moduleId": "habitat",
        "shape": "slope",
        "color": "#edf1f2"
      },
      {
        "id": "h0072",
        "moduleId": "habitat",
        "shape": "slope",
        "color": "#edf1f2"
      },
      {
        "id": "h0073",
        "moduleId": "habitat",
        "shape": "slope",
        "color": "#edf1f2"
      },
      {
        "id": "h0074",
        "moduleId": "habitat",
        "shape": "slope",
        "color": "#edf1f2"
      },
      {
        "id": "h0075",
        "moduleId": "habitat",
        "shape": "slope",
        "color": "#edf1f2"
      },
      {
        "id": "h0076",
        "moduleId": "habitat",
        "shape": "slope",
        "color": "#edf1f2"
      },
      {
        "id": "h0077",
        "moduleId": "habitat",
        "shape": "slope",
        "color": "#edf1f2"
      },
      {
        "id": "h0078",
        "moduleId": "habitat",
        "shape": "slope",
        "color": "#edf1f2"
      },
      {
        "id": "h0079",
        "moduleId": "habitat",
        "shape": "slope",
        "color": "#edf1f2"
      },
      {
        "id": "h0080",
        "moduleId": "habitat",
        "shape": "slope",
        "color": "#edf1f2"
      },
      {
        "id": "h0081",
        "moduleId": "habitat",
        "shape": "slope",
        "color": "#edf1f2"
      },
      {
        "id": "h0082",
        "moduleId": "habitat",
        "shape": "slope",
        "color": "#edf1f2"
      },
      {
        "id": "h0083",
        "moduleId": "habitat",
        "shape": "slope",
        "color": "#edf1f2"
      },
      {
        "id": "h0084",
        "moduleId": "habitat",
        "shape": "slope",
        "color": "#edf1f2"
      },
      {
        "id": "h0085",
        "moduleId": "habitat",
        "shape": "slope",
        "color": "#edf1f2"
      },
      {
        "id": "h0086",
        "moduleId": "habitat",
        "shape": "slope",
        "color": "#edf1f2"
      },
      {
        "id": "h0087",
        "moduleId": "habitat",
        "shape": "slope",
        "color": "#edf1f2"
      },
      {
        "id": "h0088",
        "moduleId": "habitat",
        "shape": "slope",
        "color": "#edf1f2"
      },
      {
        "id": "h0089",
        "moduleId": "habitat",
        "shape": "slope",
        "color": "#edf1f2"
      },
      {
        "id": "h0090",
        "moduleId": "habitat",
        "shape": "slope",
        "color": "#edf1f2"
      },
      {
        "id": "h0091",
        "moduleId": "habitat",
        "shape": "cylinder",
        "color": "#edf1f2"
      },
      {
        "id": "h0092",
        "moduleId": "habitat",
        "shape": "window",
        "color": "#79c7d8"
      },
      {
        "id": "h0093",
        "moduleId": "habitat",
        "shape": "window",
        "color": "#79c7d8"
      },
      {
        "id": "h0094",
        "moduleId": "habitat",
        "shape": "window",
        "color": "#79c7d8"
      },
      {
        "id": "h0095",
        "moduleId": "crusher",
        "shape": "plate",
        "color": "#e8792e"
      },
      {
        "id": "h0096",
        "moduleId": "crusher",
        "shape": "plate",
        "color": "#e8792e"
      },
      {
        "id": "h0097",
        "moduleId": "crusher",
        "shape": "plate",
        "color": "#e8792e"
      },
      {
        "id": "h0098",
        "moduleId": "crusher",
        "shape": "plate",
        "color": "#e8792e"
      },
      {
        "id": "h0099",
        "moduleId": "crusher",
        "shape": "plate",
        "color": "#e8792e"
      },
      {
        "id": "h0100",
        "moduleId": "crusher",
        "shape": "plate",
        "color": "#e8792e"
      },
      {
        "id": "h0101",
        "moduleId": "crusher",
        "shape": "plate",
        "color": "#e8792e"
      },
      {
        "id": "h0102",
        "moduleId": "crusher",
        "shape": "plate",
        "color": "#e8792e"
      },
      {
        "id": "h0103",
        "moduleId": "crusher",
        "shape": "plate",
        "color": "#e8792e"
      },
      {
        "id": "h0104",
        "moduleId": "crusher",
        "shape": "gear",
        "color": "#26323b"
      },
      {
        "id": "h0105",
        "moduleId": "crusher",
        "shape": "gear",
        "color": "#26323b"
      },
      {
        "id": "h0106",
        "moduleId": "crusher",
        "shape": "gear",
        "color": "#26323b"
      },
      {
        "id": "h0107",
        "moduleId": "crusher",
        "shape": "gear",
        "color": "#26323b"
      },
      {
        "id": "h0108",
        "moduleId": "crusher",
        "shape": "gear",
        "color": "#26323b"
      },
      {
        "id": "h0109",
        "moduleId": "crusher",
        "shape": "gear",
        "color": "#26323b"
      },
      {
        "id": "h0110",
        "moduleId": "crusher",
        "shape": "gear",
        "color": "#26323b"
      },
      {
        "id": "h0111",
        "moduleId": "crusher",
        "shape": "gear",
        "color": "#26323b"
      },
      {
        "id": "h0112",
        "moduleId": "conveyor",
        "shape": "plate",
        "color": "#2878b8"
      },
      {
        "id": "h0113",
        "moduleId": "conveyor",
        "shape": "plate",
        "color": "#2878b8"
      },
      {
        "id": "h0114",
        "moduleId": "conveyor",
        "shape": "plate",
        "color": "#2878b8"
      },
      {
        "id": "h0115",
        "moduleId": "conveyor",
        "shape": "plate",
        "color": "#2878b8"
      },
      {
        "id": "h0116",
        "moduleId": "conveyor",
        "shape": "plate",
        "color": "#2878b8"
      },
      {
        "id": "h0117",
        "moduleId": "conveyor",
        "shape": "plate",
        "color": "#2878b8"
      },
      {
        "id": "h0118",
        "moduleId": "conveyor",
        "shape": "plate",
        "color": "#2878b8"
      },
      {
        "id": "h0119",
        "moduleId": "conveyor",
        "shape": "plate",
        "color": "#2878b8"
      },
      {
        "id": "h0120",
        "moduleId": "conveyor",
        "shape": "plate",
        "color": "#2878b8"
      },
      {
        "id": "h0121",
        "moduleId": "conveyor",
        "shape": "plate",
        "color": "#2878b8"
      },
      {
        "id": "h0122",
        "moduleId": "conveyor",
        "shape": "plate",
        "color": "#2878b8"
      },
      {
        "id": "h0123",
        "moduleId": "conveyor",
        "shape": "plate",
        "color": "#2878b8"
      },
      {
        "id": "h0124",
        "moduleId": "conveyor",
        "shape": "plate",
        "color": "#2878b8"
      },
      {
        "id": "h0125",
        "moduleId": "conveyor",
        "shape": "plate",
        "color": "#2878b8"
      },
      {
        "id": "h0126",
        "moduleId": "conveyor",
        "shape": "plate",
        "color": "#2878b8"
      },
      {
        "id": "h0127",
        "moduleId": "conveyor",
        "shape": "plate",
        "color": "#2878b8"
      },
      {
        "id": "h0128",
        "moduleId": "conveyor",
        "shape": "plate",
        "color": "#2878b8"
      },
      {
        "id": "h0129",
        "moduleId": "conveyor",
        "shape": "plate",
        "color": "#2878b8"
      },
      {
        "id": "h0130",
        "moduleId": "centrifuge",
        "shape": "panel",
        "color": "#d43a32"
      },
      {
        "id": "h0131",
        "moduleId": "centrifuge",
        "shape": "panel",
        "color": "#d43a32"
      },
      {
        "id": "h0132",
        "moduleId": "centrifuge",
        "shape": "panel",
        "color": "#d43a32"
      },
      {
        "id": "h0133",
        "moduleId": "centrifuge",
        "shape": "panel",
        "color": "#d43a32"
      },
      {
        "id": "h0134",
        "moduleId": "centrifuge",
        "shape": "panel",
        "color": "#d43a32"
      },
      {
        "id": "h0135",
        "moduleId": "centrifuge",
        "shape": "panel",
        "color": "#d43a32"
      },
      {
        "id": "h0136",
        "moduleId": "centrifuge",
        "shape": "panel",
        "color": "#d43a32"
      },
      {
        "id": "h0137",
        "moduleId": "centrifuge",
        "shape": "panel",
        "color": "#d43a32"
      },
      {
        "id": "h0138",
        "moduleId": "centrifuge",
        "shape": "panel",
        "color": "#d43a32"
      },
      {
        "id": "h0139",
        "moduleId": "centrifuge",
        "shape": "panel",
        "color": "#d43a32"
      },
      {
        "id": "h0140",
        "moduleId": "centrifuge",
        "shape": "panel",
        "color": "#d43a32"
      },
      {
        "id": "h0141",
        "moduleId": "centrifuge",
        "shape": "panel",
        "color": "#d43a32"
      },
      {
        "id": "h0142",
        "moduleId": "centrifuge",
        "shape": "cylinder",
        "color": "#c6cdd2"
      },
      {
        "id": "h0143",
        "moduleId": "solar-a",
        "shape": "panel",
        "color": "#173b63"
      },
      {
        "id": "h0144",
        "moduleId": "solar-a",
        "shape": "panel",
        "color": "#173b63"
      },
      {
        "id": "h0145",
        "moduleId": "solar-a",
        "shape": "panel",
        "color": "#173b63"
      },
      {
        "id": "h0146",
        "moduleId": "solar-a",
        "shape": "panel",
        "color": "#173b63"
      },
      {
        "id": "h0147",
        "moduleId": "solar-a",
        "shape": "panel",
        "color": "#173b63"
      },
      {
        "id": "h0148",
        "moduleId": "solar-a",
        "shape": "panel",
        "color": "#173b63"
      },
      {
        "id": "h0149",
        "moduleId": "solar-a",
        "shape": "panel",
        "color": "#173b63"
      },
      {
        "id": "h0150",
        "moduleId": "solar-a",
        "shape": "panel",
        "color": "#173b63"
      },
      {
        "id": "h0151",
        "moduleId": "solar-a",
        "shape": "panel",
        "color": "#173b63"
      },
      {
        "id": "h0152",
        "moduleId": "solar-a",
        "shape": "panel",
        "color": "#173b63"
      },
      {
        "id": "h0153",
        "moduleId": "solar-a",
        "shape": "panel",
        "color": "#173b63"
      },
      {
        "id": "h0154",
        "moduleId": "solar-a",
        "shape": "panel",
        "color": "#173b63"
      },
      {
        "id": "h0155",
        "moduleId": "solar-a",
        "shape": "panel",
        "color": "#173b63"
      },
      {
        "id": "h0156",
        "moduleId": "solar-a",
        "shape": "panel",
        "color": "#173b63"
      },
      {
        "id": "h0157",
        "moduleId": "solar-a",
        "shape": "panel",
        "color": "#173b63"
      },
      {
        "id": "h0158",
        "moduleId": "solar-a",
        "shape": "panel",
        "color": "#173b63"
      },
      {
        "id": "h0159",
        "moduleId": "solar-a",
        "shape": "panel",
        "color": "#173b63"
      },
      {
        "id": "h0160",
        "moduleId": "solar-a",
        "shape": "panel",
        "color": "#173b63"
      },
      {
        "id": "h0161",
        "moduleId": "solar-b",
        "shape": "panel",
        "color": "#173b63"
      },
      {
        "id": "h0162",
        "moduleId": "solar-b",
        "shape": "panel",
        "color": "#173b63"
      },
      {
        "id": "h0163",
        "moduleId": "solar-b",
        "shape": "panel",
        "color": "#173b63"
      },
      {
        "id": "h0164",
        "moduleId": "solar-b",
        "shape": "panel",
        "color": "#173b63"
      },
      {
        "id": "h0165",
        "moduleId": "solar-b",
        "shape": "panel",
        "color": "#173b63"
      },
      {
        "id": "h0166",
        "moduleId": "solar-b",
        "shape": "panel",
        "color": "#173b63"
      },
      {
        "id": "h0167",
        "moduleId": "solar-b",
        "shape": "panel",
        "color": "#173b63"
      },
      {
        "id": "h0168",
        "moduleId": "solar-b",
        "shape": "panel",
        "color": "#173b63"
      },
      {
        "id": "h0169",
        "moduleId": "solar-b",
        "shape": "panel",
        "color": "#173b63"
      },
      {
        "id": "h0170",
        "moduleId": "solar-b",
        "shape": "panel",
        "color": "#173b63"
      },
      {
        "id": "h0171",
        "moduleId": "solar-b",
        "shape": "panel",
        "color": "#173b63"
      },
      {
        "id": "h0172",
        "moduleId": "solar-b",
        "shape": "panel",
        "color": "#173b63"
      },
      {
        "id": "h0173",
        "moduleId": "solar-b",
        "shape": "panel",
        "color": "#173b63"
      },
      {
        "id": "h0174",
        "moduleId": "solar-b",
        "shape": "panel",
        "color": "#173b63"
      },
      {
        "id": "h0175",
        "moduleId": "solar-b",
        "shape": "panel",
        "color": "#173b63"
      },
      {
        "id": "h0176",
        "moduleId": "solar-b",
        "shape": "panel",
        "color": "#173b63"
      },
      {
        "id": "h0177",
        "moduleId": "solar-b",
        "shape": "panel",
        "color": "#173b63"
      },
      {
        "id": "h0178",
        "moduleId": "solar-b",
        "shape": "panel",
        "color": "#173b63"
      },
      {
        "id": "h0179",
        "moduleId": "tank-a",
        "shape": "cylinder",
        "color": "#f2bf3c"
      },
      {
        "id": "h0180",
        "moduleId": "tank-a",
        "shape": "cylinder",
        "color": "#f2bf3c"
      },
      {
        "id": "h0181",
        "moduleId": "tank-a",
        "shape": "cylinder",
        "color": "#f2bf3c"
      },
      {
        "id": "h0182",
        "moduleId": "tank-a",
        "shape": "cylinder",
        "color": "#f2bf3c"
      },
      {
        "id": "h0183",
        "moduleId": "tank-a",
        "shape": "cylinder",
        "color": "#f2bf3c"
      },
      {
        "id": "h0184",
        "moduleId": "tank-b",
        "shape": "cylinder",
        "color": "#3f8a61"
      },
      {
        "id": "h0185",
        "moduleId": "tank-b",
        "shape": "cylinder",
        "color": "#3f8a61"
      },
      {
        "id": "h0186",
        "moduleId": "tank-b",
        "shape": "cylinder",
        "color": "#3f8a61"
      },
      {
        "id": "h0187",
        "moduleId": "tank-b",
        "shape": "cylinder",
        "color": "#3f8a61"
      },
      {
        "id": "h0188",
        "moduleId": "tank-b",
        "shape": "cylinder",
        "color": "#3f8a61"
      },
      {
        "id": "h0189",
        "moduleId": "sample-rover",
        "shape": "plate",
        "color": "#edf1f2"
      },
      {
        "id": "h0190",
        "moduleId": "sample-rover",
        "shape": "plate",
        "color": "#edf1f2"
      },
      {
        "id": "h0191",
        "moduleId": "sample-rover",
        "shape": "plate",
        "color": "#edf1f2"
      },
      {
        "id": "h0192",
        "moduleId": "sample-rover",
        "shape": "plate",
        "color": "#edf1f2"
      },
      {
        "id": "h0193",
        "moduleId": "sample-rover",
        "shape": "plate",
        "color": "#edf1f2"
      },
      {
        "id": "h0194",
        "moduleId": "sample-rover",
        "shape": "plate",
        "color": "#edf1f2"
      },
      {
        "id": "h0195",
        "moduleId": "sample-rover",
        "shape": "plate",
        "color": "#edf1f2"
      },
      {
        "id": "h0196",
        "moduleId": "sample-rover",
        "shape": "plate",
        "color": "#edf1f2"
      },
      {
        "id": "h0197",
        "moduleId": "sample-rover",
        "shape": "plate",
        "color": "#edf1f2"
      },
      {
        "id": "h0198",
        "moduleId": "sample-rover",
        "shape": "plate",
        "color": "#edf1f2"
      },
      {
        "id": "h0199",
        "moduleId": "sample-rover",
        "shape": "plate",
        "color": "#edf1f2"
      },
      {
        "id": "h0200",
        "moduleId": "sample-rover",
        "shape": "plate",
        "color": "#edf1f2"
      },
      {
        "id": "h0201",
        "moduleId": "sample-rover",
        "shape": "wheel",
        "color": "#101820"
      },
      {
        "id": "h0202",
        "moduleId": "sample-rover",
        "shape": "wheel",
        "color": "#101820"
      },
      {
        "id": "h0203",
        "moduleId": "sample-rover",
        "shape": "wheel",
        "color": "#101820"
      },
      {
        "id": "h0204",
        "moduleId": "sample-rover",
        "shape": "wheel",
        "color": "#101820"
      },
      {
        "id": "h0205",
        "moduleId": "loading-arm",
        "shape": "beam",
        "color": "#e8792e"
      },
      {
        "id": "h0206",
        "moduleId": "loading-arm",
        "shape": "beam",
        "color": "#e8792e"
      },
      {
        "id": "h0207",
        "moduleId": "loading-arm",
        "shape": "beam",
        "color": "#e8792e"
      },
      {
        "id": "h0208",
        "moduleId": "loading-arm",
        "shape": "beam",
        "color": "#e8792e"
      },
      {
        "id": "h0209",
        "moduleId": "loading-arm",
        "shape": "beam",
        "color": "#e8792e"
      },
      {
        "id": "h0210",
        "moduleId": "loading-arm",
        "shape": "beam",
        "color": "#e8792e"
      },
      {
        "id": "h0211",
        "moduleId": "loading-arm",
        "shape": "beam",
        "color": "#e8792e"
      },
      {
        "id": "h0212",
        "moduleId": "loading-arm",
        "shape": "beam",
        "color": "#e8792e"
      },
      {
        "id": "h0213",
        "moduleId": "silo",
        "shape": "cylinder",
        "color": "#a94872"
      },
      {
        "id": "h0214",
        "moduleId": "silo",
        "shape": "cylinder",
        "color": "#a94872"
      },
      {
        "id": "h0215",
        "moduleId": "silo",
        "shape": "cylinder",
        "color": "#a94872"
      },
      {
        "id": "h0216",
        "moduleId": "silo",
        "shape": "cylinder",
        "color": "#a94872"
      },
      {
        "id": "h0217",
        "moduleId": "silo",
        "shape": "cylinder",
        "color": "#a94872"
      },
      {
        "id": "h0218",
        "moduleId": "silo",
        "shape": "cylinder",
        "color": "#a94872"
      }
    ]
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 颜色识别（h3-lunar-sample-refinery-color）

零件 h0205 的颜色值是什么？

能力：颜色识别；形式：single-choice；证据：model-state。

- A：#f2bf3c
- B：#e8792e
- C：#2878b8
- D：#d43a32

```json
{
  "input": {
    "part": {
      "id": "h0205",
      "moduleId": "loading-arm",
      "shape": "beam",
      "size": [
        0.5,
        0.6,
        0.5
      ],
      "position": [
        -1.2999999999999998,
        -2.225481111790155,
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
    "choiceId": "B"
  }
}
```

### 三维位置（h3-lunar-sample-refinery-position）

模块 loading-arm 的世界包围盒中心是什么？

能力：三维位置；形式：single-choice；证据：model-state。

- A：[0,0.2,0]
- B：[-3.2000000000000006,1.6999999999999997,0]
- C：[0,1.475,-2.5575]
- D：[3.0999999999999996,3.5254811117901554,-2.3]

```json
{
  "input": {
    "centers": {
      "pad": [
        0,
        0.2,
        0
      ],
      "habitat": [
        -3.2000000000000006,
        1.6999999999999997,
        0
      ],
      "crusher": [
        0,
        1.475,
        -2.5575
      ],
      "conveyor": [
        0.3250000000000002,
        1.32,
        -1.65
      ],
      "centrifuge": [
        3,
        2.9,
        0
      ],
      "solar-a": [
        0,
        1.2,
        -5
      ],
      "solar-b": [
        0,
        1.2,
        5
      ],
      "tank-a": [
        5,
        2.1999999999999997,
        2.8
      ],
      "tank-b": [
        6.7,
        2.1999999999999997,
        2.8
      ],
      "sample-rover": [
        0,
        0.7875,
        3.605
      ],
      "loading-arm": [
        3.0999999999999996,
        3.5254811117901554,
        -2.3
      ],
      "silo": [
        5.8,
        2.55,
        -3
      ]
    }
  },
  "answer": {
    "choiceId": "D"
  }
}
```

### 关节类型（h3-lunar-sample-refinery-joint-type）

centrifuge-shaft 采用什么约束类型？

能力：关节类型；形式：single-choice；证据：model-state。

- A：spring
- B：revolute
- C：fixed
- D：prismatic

```json
{
  "input": {
    "joint": {
      "id": "centrifuge-shaft",
      "name": "centrifuge shaft",
      "type": "revolute",
      "parent": "conveyor",
      "child": "centrifuge",
      "anchorParent": [
        2.675,
        1.5799999999999998,
        1.65
      ],
      "anchorChild": [
        0,
        0,
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
    }
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 直接连接（h3-lunar-sample-refinery-parent）

loading-arm 的直接父模块集合是什么？

能力：直接连接；形式：single-choice；证据：model-state。

- A：["loading-arm"]
- B：[]
- C：["pad","habitat","crusher","conveyor","centrifuge","solar-a","solar-b","tank-a","tank-b","sample-rover","loading-arm","silo"]
- D：["crusher"]

```json
{
  "input": {
    "joints": [
      {
        "id": "habitat-mount",
        "name": "habitat mount",
        "type": "fixed",
        "parent": "pad",
        "child": "habitat",
        "anchorParent": [
          -3.2,
          0.3,
          0
        ],
        "anchorChild": [
          4.440892098500626e-16,
          -1.1999999999999997,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "crusher-mount",
        "name": "crusher mount",
        "type": "fixed",
        "parent": "pad",
        "child": "crusher",
        "anchorParent": [
          0,
          0.3,
          -3
        ],
        "anchorChild": [
          0,
          -0.9750000000000001,
          -0.4424999999999999
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "conveyor-drive",
        "name": "conveyor drive",
        "type": "prismatic",
        "parent": "crusher",
        "child": "conveyor",
        "anchorParent": [
          0,
          -0.375,
          -0.14250000000000007
        ],
        "anchorChild": [
          -0.3250000000000002,
          -0.21999999999999997,
          -1.05
        ],
        "axis": [
          1,
          0,
          0
        ],
        "limits": [
          -0.4,
          0.4
        ]
      },
      {
        "id": "centrifuge-shaft",
        "name": "centrifuge shaft",
        "type": "revolute",
        "parent": "conveyor",
        "child": "centrifuge",
        "anchorParent": [
          2.675,
          1.5799999999999998,
          1.65
        ],
        "anchorChild": [
          0,
          0,
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
        "id": "solar-a-hinge",
        "name": "solar a hinge",
        "type": "revolute",
        "parent": "pad",
        "child": "solar-a",
        "anchorParent": [
          0,
          1,
          -5
        ],
        "anchorChild": [
          0,
          0,
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
        "id": "solar-b-hinge",
        "name": "solar b hinge",
        "type": "revolute",
        "parent": "pad",
        "child": "solar-b",
        "anchorParent": [
          0,
          1,
          5
        ],
        "anchorChild": [
          0,
          0,
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
        "id": "tank-a-lock",
        "name": "tank a lock",
        "type": "fixed",
        "parent": "pad",
        "child": "tank-a",
        "anchorParent": [
          5,
          0.3,
          2.8
        ],
        "anchorChild": [
          0,
          -1.6999999999999997,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "tank-b-lock",
        "name": "tank b lock",
        "type": "fixed",
        "parent": "pad",
        "child": "tank-b",
        "anchorParent": [
          6.7,
          0.3,
          2.8
        ],
        "anchorChild": [
          0,
          -1.6999999999999997,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "rover-dock",
        "name": "rover dock",
        "type": "fixed",
        "parent": "pad",
        "child": "sample-rover",
        "anchorParent": [
          0,
          0.49999999999999994,
          3
        ],
        "anchorChild": [
          0,
          -0.08749999999999991,
          -0.605
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "arm-shoulder",
        "name": "arm shoulder",
        "type": "revolute",
        "parent": "crusher",
        "child": "loading-arm",
        "anchorParent": [
          1.8,
          -0.17500000000000004,
          0.2575000000000003
        ],
        "anchorChild": [
          -1.2999999999999998,
          -2.225481111790155,
          0
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          -0.2,
          1.1
        ]
      },
      {
        "id": "silo-lock",
        "name": "silo lock",
        "type": "fixed",
        "parent": "pad",
        "child": "silo",
        "anchorParent": [
          5.8,
          0.3,
          -3
        ],
        "anchorChild": [
          0,
          -2.05,
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
    "choiceId": "D"
  }
}
```

### 基座识别（h3-lunar-sample-refinery-anchor）

哪些模块被声明为固定基座？

能力：基座识别；形式：single-choice；证据：model-state。

- A：["loading-arm"]
- B：["pad"]
- C：[]
- D：["pad","habitat","crusher","conveyor","centrifuge","solar-a","solar-b","tank-a","tank-b","sample-rover","loading-arm","silo"]

```json
{
  "input": {
    "modules": [
      {
        "id": "pad",
        "name": "Lunar refinery pad",
        "role": "foundation",
        "anchored": true,
        "mass": 55,
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
        "id": "habitat",
        "name": "Pressurized control habitat",
        "role": "control",
        "anchored": false,
        "mass": 16,
        "position": [
          -3.2000000000000006,
          1.6999999999999997,
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
        "id": "crusher",
        "name": "Sample crusher",
        "role": "processor",
        "anchored": false,
        "mass": 8,
        "position": [
          0,
          1.475,
          -2.5575
        ],
        "rotation": [
          0,
          0,
          0,
          1
        ]
      },
      {
        "id": "conveyor",
        "name": "Sealed transfer conveyor",
        "role": "transport",
        "anchored": false,
        "mass": 5,
        "position": [
          0.3250000000000002,
          1.32,
          -1.65
        ],
        "rotation": [
          0,
          0,
          0,
          1
        ]
      },
      {
        "id": "centrifuge",
        "name": "Rotary separator",
        "role": "actuator",
        "anchored": false,
        "mass": 7,
        "position": [
          3,
          2.9,
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
        "id": "solar-a",
        "name": "North solar wing",
        "role": "power",
        "anchored": false,
        "mass": 4,
        "position": [
          0,
          1.2,
          -5
        ],
        "rotation": [
          0,
          0,
          0,
          1
        ]
      },
      {
        "id": "solar-b",
        "name": "South solar wing",
        "role": "power",
        "anchored": false,
        "mass": 4,
        "position": [
          0,
          1.2,
          5
        ],
        "rotation": [
          0,
          0,
          0,
          1
        ]
      },
      {
        "id": "tank-a",
        "name": "Feedstock tank",
        "role": "storage",
        "anchored": false,
        "mass": 5,
        "position": [
          5,
          2.1999999999999997,
          2.8
        ],
        "rotation": [
          0,
          0,
          0,
          1
        ]
      },
      {
        "id": "tank-b",
        "name": "Product tank",
        "role": "storage",
        "anchored": false,
        "mass": 5,
        "position": [
          6.7,
          2.1999999999999997,
          2.8
        ],
        "rotation": [
          0,
          0,
          0,
          1
        ]
      },
      {
        "id": "sample-rover",
        "name": "Sample transfer rover",
        "role": "payload",
        "anchored": false,
        "mass": 5,
        "position": [
          0,
          0.7874999999999999,
          3.605
        ],
        "rotation": [
          0,
          0,
          0,
          1
        ]
      },
      {
        "id": "loading-arm",
        "name": "Refinery loading arm",
        "role": "service-module",
        "anchored": false,
        "mass": 3,
        "position": [
          3.0999999999999996,
          3.5254811117901554,
          -2.3
        ],
        "rotation": [
          0,
          0,
          0,
          1
        ]
      },
      {
        "id": "silo",
        "name": "Processed sample silo",
        "role": "storage",
        "anchored": false,
        "mass": 5,
        "position": [
          5.8,
          2.55,
          -3
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

### 接口计数（h3-lunar-sample-refinery-degree）

loading-arm 连接几个声明关节？平行关节分别计数。

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
        "id": "habitat-mount",
        "name": "habitat mount",
        "type": "fixed",
        "parent": "pad",
        "child": "habitat",
        "anchorParent": [
          -3.2,
          0.3,
          0
        ],
        "anchorChild": [
          4.440892098500626e-16,
          -1.1999999999999997,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "crusher-mount",
        "name": "crusher mount",
        "type": "fixed",
        "parent": "pad",
        "child": "crusher",
        "anchorParent": [
          0,
          0.3,
          -3
        ],
        "anchorChild": [
          0,
          -0.9750000000000001,
          -0.4424999999999999
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "conveyor-drive",
        "name": "conveyor drive",
        "type": "prismatic",
        "parent": "crusher",
        "child": "conveyor",
        "anchorParent": [
          0,
          -0.375,
          -0.14250000000000007
        ],
        "anchorChild": [
          -0.3250000000000002,
          -0.21999999999999997,
          -1.05
        ],
        "axis": [
          1,
          0,
          0
        ],
        "limits": [
          -0.4,
          0.4
        ]
      },
      {
        "id": "centrifuge-shaft",
        "name": "centrifuge shaft",
        "type": "revolute",
        "parent": "conveyor",
        "child": "centrifuge",
        "anchorParent": [
          2.675,
          1.5799999999999998,
          1.65
        ],
        "anchorChild": [
          0,
          0,
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
        "id": "solar-a-hinge",
        "name": "solar a hinge",
        "type": "revolute",
        "parent": "pad",
        "child": "solar-a",
        "anchorParent": [
          0,
          1,
          -5
        ],
        "anchorChild": [
          0,
          0,
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
        "id": "solar-b-hinge",
        "name": "solar b hinge",
        "type": "revolute",
        "parent": "pad",
        "child": "solar-b",
        "anchorParent": [
          0,
          1,
          5
        ],
        "anchorChild": [
          0,
          0,
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
        "id": "tank-a-lock",
        "name": "tank a lock",
        "type": "fixed",
        "parent": "pad",
        "child": "tank-a",
        "anchorParent": [
          5,
          0.3,
          2.8
        ],
        "anchorChild": [
          0,
          -1.6999999999999997,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "tank-b-lock",
        "name": "tank b lock",
        "type": "fixed",
        "parent": "pad",
        "child": "tank-b",
        "anchorParent": [
          6.7,
          0.3,
          2.8
        ],
        "anchorChild": [
          0,
          -1.6999999999999997,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "rover-dock",
        "name": "rover dock",
        "type": "fixed",
        "parent": "pad",
        "child": "sample-rover",
        "anchorParent": [
          0,
          0.49999999999999994,
          3
        ],
        "anchorChild": [
          0,
          -0.08749999999999991,
          -0.605
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "arm-shoulder",
        "name": "arm shoulder",
        "type": "revolute",
        "parent": "crusher",
        "child": "loading-arm",
        "anchorParent": [
          1.8,
          -0.17500000000000004,
          0.2575000000000003
        ],
        "anchorChild": [
          -1.2999999999999998,
          -2.225481111790155,
          0
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          -0.2,
          1.1
        ]
      },
      {
        "id": "silo-lock",
        "name": "silo lock",
        "type": "fixed",
        "parent": "pad",
        "child": "silo",
        "anchorParent": [
          5.8,
          0.3,
          -3
        ],
        "anchorChild": [
          0,
          -2.05,
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

### 局部改色（h3-lunar-sample-refinery-recolor）

仅将 h0205 改成 #e8792e，其他零件不变。选择正确补丁。

能力：局部改色；形式：single-choice；证据：model-state。

- A：{"id":"*","color":"#e8792e"}
- B：{"id":"h0205","color":"#e8792e"}
- C：{"id":"h0206","color":"#e8792e"}
- D：{"id":"h0205","color":"#2878b8"}

```json
{
  "input": {
    "part": {
      "id": "h0205",
      "moduleId": "loading-arm",
      "shape": "beam",
      "size": [
        0.5,
        0.6,
        0.5
      ],
      "position": [
        -1.2999999999999998,
        -2.225481111790155,
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
    "choiceId": "B"
  }
}
```

### 补装部件（h3-lunar-sample-refinery-add）

模块 loading-arm 缺失零件 h0205。选择与目标清单一致的补装描述。

能力：补装部件；形式：single-choice；证据：model-state。

- A：{"id":"h0205","moduleId":"loading-arm","shape":"beam","size":[3,3,3],"position":[-1.2999999999999998,-2.225481111790155,0],"rotation":[0,0,0,1],"color":"#e8792e"}
- B：{"id":"h0205","moduleId":"loading-arm","shape":"beam","size":[0.5,0.6,0.5],"position":[-1.2999999999999998,-2.225481111790155,0],"rotation":[0,0,0,1],"color":"#000000"}
- C：{"id":"h0205","moduleId":"loading-arm","shape":"beam","size":[0.5,0.6,0.5],"position":[-1.2999999999999998,-2.225481111790155,0],"rotation":[0,0,0,1],"color":"#e8792e"}
- D：{"id":"h0205","moduleId":"pad","shape":"beam","size":[0.5,0.6,0.5],"position":[-1.2999999999999998,-2.225481111790155,0],"rotation":[0,0,0,1],"color":"#e8792e"}

```json
{
  "input": {
    "targetPart": {
      "id": "h0205",
      "moduleId": "loading-arm",
      "shape": "beam",
      "size": [
        0.5,
        0.6,
        0.5
      ],
      "position": [
        -1.2999999999999998,
        -2.225481111790155,
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
      "h0122",
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
      "h0218"
    ]
  },
  "answer": {
    "choiceId": "C"
  }
}
```

### 安全拆除（h3-lunar-sample-refinery-remove）

按声明依赖图，当前可以先拆哪些叶模块？

能力：安全拆除；形式：single-choice；证据：model-state。

- A：["centrifuge","habitat","loading-arm","sample-rover","silo","solar-a","solar-b","tank-a","tank-b"]
- B：["pad"]
- C：[]
- D：["pad","habitat","crusher","conveyor","centrifuge","solar-a","solar-b","tank-a","tank-b","sample-rover","loading-arm","silo"]

```json
{
  "input": {
    "joints": [
      {
        "id": "habitat-mount",
        "name": "habitat mount",
        "type": "fixed",
        "parent": "pad",
        "child": "habitat",
        "anchorParent": [
          -3.2,
          0.3,
          0
        ],
        "anchorChild": [
          4.440892098500626e-16,
          -1.1999999999999997,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "crusher-mount",
        "name": "crusher mount",
        "type": "fixed",
        "parent": "pad",
        "child": "crusher",
        "anchorParent": [
          0,
          0.3,
          -3
        ],
        "anchorChild": [
          0,
          -0.9750000000000001,
          -0.4424999999999999
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "conveyor-drive",
        "name": "conveyor drive",
        "type": "prismatic",
        "parent": "crusher",
        "child": "conveyor",
        "anchorParent": [
          0,
          -0.375,
          -0.14250000000000007
        ],
        "anchorChild": [
          -0.3250000000000002,
          -0.21999999999999997,
          -1.05
        ],
        "axis": [
          1,
          0,
          0
        ],
        "limits": [
          -0.4,
          0.4
        ]
      },
      {
        "id": "centrifuge-shaft",
        "name": "centrifuge shaft",
        "type": "revolute",
        "parent": "conveyor",
        "child": "centrifuge",
        "anchorParent": [
          2.675,
          1.5799999999999998,
          1.65
        ],
        "anchorChild": [
          0,
          0,
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
        "id": "solar-a-hinge",
        "name": "solar a hinge",
        "type": "revolute",
        "parent": "pad",
        "child": "solar-a",
        "anchorParent": [
          0,
          1,
          -5
        ],
        "anchorChild": [
          0,
          0,
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
        "id": "solar-b-hinge",
        "name": "solar b hinge",
        "type": "revolute",
        "parent": "pad",
        "child": "solar-b",
        "anchorParent": [
          0,
          1,
          5
        ],
        "anchorChild": [
          0,
          0,
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
        "id": "tank-a-lock",
        "name": "tank a lock",
        "type": "fixed",
        "parent": "pad",
        "child": "tank-a",
        "anchorParent": [
          5,
          0.3,
          2.8
        ],
        "anchorChild": [
          0,
          -1.6999999999999997,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "tank-b-lock",
        "name": "tank b lock",
        "type": "fixed",
        "parent": "pad",
        "child": "tank-b",
        "anchorParent": [
          6.7,
          0.3,
          2.8
        ],
        "anchorChild": [
          0,
          -1.6999999999999997,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "rover-dock",
        "name": "rover dock",
        "type": "fixed",
        "parent": "pad",
        "child": "sample-rover",
        "anchorParent": [
          0,
          0.49999999999999994,
          3
        ],
        "anchorChild": [
          0,
          -0.08749999999999991,
          -0.605
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "arm-shoulder",
        "name": "arm shoulder",
        "type": "revolute",
        "parent": "crusher",
        "child": "loading-arm",
        "anchorParent": [
          1.8,
          -0.17500000000000004,
          0.2575000000000003
        ],
        "anchorChild": [
          -1.2999999999999998,
          -2.225481111790155,
          0
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          -0.2,
          1.1
        ]
      },
      {
        "id": "silo-lock",
        "name": "silo lock",
        "type": "fixed",
        "parent": "pad",
        "child": "silo",
        "anchorParent": [
          5.8,
          0.3,
          -3
        ],
        "anchorChild": [
          0,
          -2.05,
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
      "pad",
      "habitat",
      "crusher",
      "conveyor",
      "centrifuge",
      "solar-a",
      "solar-b",
      "tank-a",
      "tank-b",
      "sample-rover",
      "loading-arm",
      "silo"
    ]
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 替换选择（h3-lunar-sample-refinery-replace）

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
        "cost": 7,
        "stiffness": 4,
        "mass": 1.2
      },
      {
        "id": "stock-1",
        "cost": 5,
        "stiffness": 7,
        "mass": 1.6
      },
      {
        "id": "stock-2",
        "cost": 7,
        "stiffness": 7,
        "mass": 1.2
      },
      {
        "id": "stock-3",
        "cost": 6,
        "stiffness": 10,
        "mass": 0.7
      }
    ],
    "maxCost": 6
  },
  "answer": {
    "choiceId": "D"
  }
}
```

### 平移纠偏（h3-lunar-sample-refinery-translate）

观察到相对目标的平移误差 delta，选择补偿平移。

能力：平移纠偏；形式：single-choice；证据：model-state。

- A：[0,2,0]
- B：[-4,0,2]
- C：[4,0,-2]
- D：[0,0,0]

```json
{
  "input": {
    "delta": [
      4,
      0,
      -2
    ],
    "target": "loading-arm"
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 姿态纠偏（h3-lunar-sample-refinery-rotate）

选择从当前yaw到目标yaw的最短有符号旋转；恰好180°时使用-180°。

能力：姿态纠偏；形式：single-choice；证据：model-state。

- A：90
- B：135
- C：-135
- D：0

```json
{
  "input": {
    "module": "loading-arm",
    "currentYaw": 135,
    "targetYaw": 270
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 下一步放置（h3-lunar-sample-refinery-next-module）

已完成给定前缀，选择所有前置依赖已满足的下一模块集合。

能力：下一步放置；形式：single-choice；证据：model-state。

- A：[]
- B：["pad","habitat","crusher","conveyor","centrifuge","solar-a"]
- C：["pad"]
- D：["loading-arm","sample-rover","silo","solar-b","tank-a","tank-b"]

```json
{
  "input": {
    "prefix": [
      "pad",
      "habitat",
      "crusher",
      "conveyor",
      "centrifuge",
      "solar-a"
    ],
    "joints": [
      {
        "id": "habitat-mount",
        "name": "habitat mount",
        "type": "fixed",
        "parent": "pad",
        "child": "habitat",
        "anchorParent": [
          -3.2,
          0.3,
          0
        ],
        "anchorChild": [
          4.440892098500626e-16,
          -1.1999999999999997,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "crusher-mount",
        "name": "crusher mount",
        "type": "fixed",
        "parent": "pad",
        "child": "crusher",
        "anchorParent": [
          0,
          0.3,
          -3
        ],
        "anchorChild": [
          0,
          -0.9750000000000001,
          -0.4424999999999999
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "conveyor-drive",
        "name": "conveyor drive",
        "type": "prismatic",
        "parent": "crusher",
        "child": "conveyor",
        "anchorParent": [
          0,
          -0.375,
          -0.14250000000000007
        ],
        "anchorChild": [
          -0.3250000000000002,
          -0.21999999999999997,
          -1.05
        ],
        "axis": [
          1,
          0,
          0
        ],
        "limits": [
          -0.4,
          0.4
        ]
      },
      {
        "id": "centrifuge-shaft",
        "name": "centrifuge shaft",
        "type": "revolute",
        "parent": "conveyor",
        "child": "centrifuge",
        "anchorParent": [
          2.675,
          1.5799999999999998,
          1.65
        ],
        "anchorChild": [
          0,
          0,
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
        "id": "solar-a-hinge",
        "name": "solar a hinge",
        "type": "revolute",
        "parent": "pad",
        "child": "solar-a",
        "anchorParent": [
          0,
          1,
          -5
        ],
        "anchorChild": [
          0,
          0,
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
        "id": "solar-b-hinge",
        "name": "solar b hinge",
        "type": "revolute",
        "parent": "pad",
        "child": "solar-b",
        "anchorParent": [
          0,
          1,
          5
        ],
        "anchorChild": [
          0,
          0,
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
        "id": "tank-a-lock",
        "name": "tank a lock",
        "type": "fixed",
        "parent": "pad",
        "child": "tank-a",
        "anchorParent": [
          5,
          0.3,
          2.8
        ],
        "anchorChild": [
          0,
          -1.6999999999999997,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "tank-b-lock",
        "name": "tank b lock",
        "type": "fixed",
        "parent": "pad",
        "child": "tank-b",
        "anchorParent": [
          6.7,
          0.3,
          2.8
        ],
        "anchorChild": [
          0,
          -1.6999999999999997,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "rover-dock",
        "name": "rover dock",
        "type": "fixed",
        "parent": "pad",
        "child": "sample-rover",
        "anchorParent": [
          0,
          0.49999999999999994,
          3
        ],
        "anchorChild": [
          0,
          -0.08749999999999991,
          -0.605
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "arm-shoulder",
        "name": "arm shoulder",
        "type": "revolute",
        "parent": "crusher",
        "child": "loading-arm",
        "anchorParent": [
          1.8,
          -0.17500000000000004,
          0.2575000000000003
        ],
        "anchorChild": [
          -1.2999999999999998,
          -2.225481111790155,
          0
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          -0.2,
          1.1
        ]
      },
      {
        "id": "silo-lock",
        "name": "silo lock",
        "type": "fixed",
        "parent": "pad",
        "child": "silo",
        "anchorParent": [
          5.8,
          0.3,
          -3
        ],
        "anchorChild": [
          0,
          -2.05,
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
      "pad",
      "habitat",
      "crusher",
      "conveyor",
      "centrifuge",
      "solar-a",
      "solar-b",
      "tank-a",
      "tank-b",
      "sample-rover",
      "loading-arm",
      "silo"
    ]
  },
  "answer": {
    "choiceId": "D"
  }
}
```

### 库存核算（h3-lunar-sample-refinery-inventory）

备件库有 14 件，替换模块需 8 件，还剩多少？

能力：库存核算；形式：single-choice；证据：model-state。

- A：7
- B：5
- C：9
- D：6

```json
{
  "input": {
    "available": 14,
    "required": 8
  },
  "answer": {
    "choiceId": "D"
  }
}
```

### 子装配边界（h3-lunar-sample-refinery-boundary）

隔离 loading-arm 需要断开哪些边界关节？

能力：子装配边界；形式：single-choice；证据：model-state。

- A：[]
- B：["habitat-mount","crusher-mount","conveyor-drive","centrifuge-shaft","solar-a-hinge","solar-b-hinge","tank-a-lock","tank-b-lock","rover-dock","arm-shoulder","silo-lock"]
- C：["centrifuge-shaft"]
- D：["arm-shoulder"]

```json
{
  "input": {
    "joints": [
      {
        "id": "habitat-mount",
        "name": "habitat mount",
        "type": "fixed",
        "parent": "pad",
        "child": "habitat",
        "anchorParent": [
          -3.2,
          0.3,
          0
        ],
        "anchorChild": [
          4.440892098500626e-16,
          -1.1999999999999997,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "crusher-mount",
        "name": "crusher mount",
        "type": "fixed",
        "parent": "pad",
        "child": "crusher",
        "anchorParent": [
          0,
          0.3,
          -3
        ],
        "anchorChild": [
          0,
          -0.9750000000000001,
          -0.4424999999999999
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "conveyor-drive",
        "name": "conveyor drive",
        "type": "prismatic",
        "parent": "crusher",
        "child": "conveyor",
        "anchorParent": [
          0,
          -0.375,
          -0.14250000000000007
        ],
        "anchorChild": [
          -0.3250000000000002,
          -0.21999999999999997,
          -1.05
        ],
        "axis": [
          1,
          0,
          0
        ],
        "limits": [
          -0.4,
          0.4
        ]
      },
      {
        "id": "centrifuge-shaft",
        "name": "centrifuge shaft",
        "type": "revolute",
        "parent": "conveyor",
        "child": "centrifuge",
        "anchorParent": [
          2.675,
          1.5799999999999998,
          1.65
        ],
        "anchorChild": [
          0,
          0,
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
        "id": "solar-a-hinge",
        "name": "solar a hinge",
        "type": "revolute",
        "parent": "pad",
        "child": "solar-a",
        "anchorParent": [
          0,
          1,
          -5
        ],
        "anchorChild": [
          0,
          0,
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
        "id": "solar-b-hinge",
        "name": "solar b hinge",
        "type": "revolute",
        "parent": "pad",
        "child": "solar-b",
        "anchorParent": [
          0,
          1,
          5
        ],
        "anchorChild": [
          0,
          0,
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
        "id": "tank-a-lock",
        "name": "tank a lock",
        "type": "fixed",
        "parent": "pad",
        "child": "tank-a",
        "anchorParent": [
          5,
          0.3,
          2.8
        ],
        "anchorChild": [
          0,
          -1.6999999999999997,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "tank-b-lock",
        "name": "tank b lock",
        "type": "fixed",
        "parent": "pad",
        "child": "tank-b",
        "anchorParent": [
          6.7,
          0.3,
          2.8
        ],
        "anchorChild": [
          0,
          -1.6999999999999997,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "rover-dock",
        "name": "rover dock",
        "type": "fixed",
        "parent": "pad",
        "child": "sample-rover",
        "anchorParent": [
          0,
          0.49999999999999994,
          3
        ],
        "anchorChild": [
          0,
          -0.08749999999999991,
          -0.605
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "arm-shoulder",
        "name": "arm shoulder",
        "type": "revolute",
        "parent": "crusher",
        "child": "loading-arm",
        "anchorParent": [
          1.8,
          -0.17500000000000004,
          0.2575000000000003
        ],
        "anchorChild": [
          -1.2999999999999998,
          -2.225481111790155,
          0
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          -0.2,
          1.1
        ]
      },
      {
        "id": "silo-lock",
        "name": "silo lock",
        "type": "fixed",
        "parent": "pad",
        "child": "silo",
        "anchorParent": [
          5.8,
          0.3,
          -3
        ],
        "anchorChild": [
          0,
          -2.05,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      }
    ],
    "target": "loading-arm"
  },
  "answer": {
    "choiceId": "D"
  }
}
```

### 最小干预（h3-lunar-sample-refinery-no-op）

当前模块颜色已满足指令，且无需改变位姿。最少需要几次编辑？

能力：最小干预；形式：single-choice；证据：model-state。

- A：1
- B：2
- C：8
- D：0

```json
{
  "input": {
    "module": "loading-arm"
  },
  "answer": {
    "choiceId": "D"
  }
}
```

### 全过程依赖（h3-lunar-sample-refinery-prefix）

给定候选顺序，首次违反前置依赖的步骤是？从 0 编号，-1 表示没有违反。

能力：全过程依赖；形式：single-choice；证据：support-graph。

- A：1
- B：11
- C：0
- D：-1

```json
{
  "input": {
    "order": [
      "silo",
      "pad",
      "habitat",
      "crusher",
      "conveyor",
      "centrifuge",
      "solar-a",
      "solar-b",
      "tank-a",
      "tank-b",
      "sample-rover",
      "loading-arm"
    ],
    "joints": [
      {
        "id": "habitat-mount",
        "name": "habitat mount",
        "type": "fixed",
        "parent": "pad",
        "child": "habitat",
        "anchorParent": [
          -3.2,
          0.3,
          0
        ],
        "anchorChild": [
          4.440892098500626e-16,
          -1.1999999999999997,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "crusher-mount",
        "name": "crusher mount",
        "type": "fixed",
        "parent": "pad",
        "child": "crusher",
        "anchorParent": [
          0,
          0.3,
          -3
        ],
        "anchorChild": [
          0,
          -0.9750000000000001,
          -0.4424999999999999
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "conveyor-drive",
        "name": "conveyor drive",
        "type": "prismatic",
        "parent": "crusher",
        "child": "conveyor",
        "anchorParent": [
          0,
          -0.375,
          -0.14250000000000007
        ],
        "anchorChild": [
          -0.3250000000000002,
          -0.21999999999999997,
          -1.05
        ],
        "axis": [
          1,
          0,
          0
        ],
        "limits": [
          -0.4,
          0.4
        ]
      },
      {
        "id": "centrifuge-shaft",
        "name": "centrifuge shaft",
        "type": "revolute",
        "parent": "conveyor",
        "child": "centrifuge",
        "anchorParent": [
          2.675,
          1.5799999999999998,
          1.65
        ],
        "anchorChild": [
          0,
          0,
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
        "id": "solar-a-hinge",
        "name": "solar a hinge",
        "type": "revolute",
        "parent": "pad",
        "child": "solar-a",
        "anchorParent": [
          0,
          1,
          -5
        ],
        "anchorChild": [
          0,
          0,
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
        "id": "solar-b-hinge",
        "name": "solar b hinge",
        "type": "revolute",
        "parent": "pad",
        "child": "solar-b",
        "anchorParent": [
          0,
          1,
          5
        ],
        "anchorChild": [
          0,
          0,
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
        "id": "tank-a-lock",
        "name": "tank a lock",
        "type": "fixed",
        "parent": "pad",
        "child": "tank-a",
        "anchorParent": [
          5,
          0.3,
          2.8
        ],
        "anchorChild": [
          0,
          -1.6999999999999997,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "tank-b-lock",
        "name": "tank b lock",
        "type": "fixed",
        "parent": "pad",
        "child": "tank-b",
        "anchorParent": [
          6.7,
          0.3,
          2.8
        ],
        "anchorChild": [
          0,
          -1.6999999999999997,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "rover-dock",
        "name": "rover dock",
        "type": "fixed",
        "parent": "pad",
        "child": "sample-rover",
        "anchorParent": [
          0,
          0.49999999999999994,
          3
        ],
        "anchorChild": [
          0,
          -0.08749999999999991,
          -0.605
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "arm-shoulder",
        "name": "arm shoulder",
        "type": "revolute",
        "parent": "crusher",
        "child": "loading-arm",
        "anchorParent": [
          1.8,
          -0.17500000000000004,
          0.2575000000000003
        ],
        "anchorChild": [
          -1.2999999999999998,
          -2.225481111790155,
          0
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          -0.2,
          1.1
        ]
      },
      {
        "id": "silo-lock",
        "name": "silo lock",
        "type": "fixed",
        "parent": "pad",
        "child": "silo",
        "anchorParent": [
          5.8,
          0.3,
          -3
        ],
        "anchorChild": [
          0,
          -2.05,
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

### 连续维修路径（h3-lunar-sample-refinery-access）

根据实际 Rapier shape cast 记录，选择全部无碰撞路径。

能力：连续维修路径；形式：multiple-choice；证据：Rapier。

- A：path-2
- B：path-1
- C：path-0

```json
{
  "input": {
    "paths": [
      {
        "id": "path-0",
        "start": [
          11.3,
          3.5254811117901554,
          -2.3
        ],
        "end": [
          3.0999999999999996,
          3.5254811117901554,
          -2.3
        ],
        "halfExtents": [
          0.18,
          0.18,
          0.18
        ],
        "clear": false,
        "timeOfImpact": 0.5634146332740784
      },
      {
        "id": "path-1",
        "start": [
          3.0999999999999996,
          10.05096222358031,
          -2.3
        ],
        "end": [
          3.0999999999999996,
          3.5254811117901554,
          -2.3
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
          3.0999999999999996,
          3.5254811117901554,
          10.45
        ],
        "end": [
          3.0999999999999996,
          3.5254811117901554,
          -2.3
        ],
        "halfExtents": [
          0.18,
          0.18,
          0.18
        ],
        "clear": false,
        "timeOfImpact": 0.7270587682723999
      }
    ],
    "simulator": "stud-inclusive conservative cuboids; anchored base; force-limited position servos; no clutch/material calibration"
  },
  "answer": {
    "choiceIds": [
      "B"
    ]
  }
}
```

### 支撑反事实（h3-lunar-sample-refinery-counterfactual）

移除指定模块后，哪些其余模块失去到任一基座的关节路径？不包含被移除模块本身。

能力：支撑反事实；形式：single-choice；证据：support-graph。

- A：["pad","habitat","crusher","conveyor","centrifuge","solar-a","solar-b","tank-a","tank-b","sample-rover","loading-arm","silo"]
- B：["centrifuge","conveyor","loading-arm"]
- C：["crusher"]
- D：[]

```json
{
  "input": {
    "removed": "crusher",
    "roots": [
      "pad"
    ],
    "joints": [
      {
        "id": "habitat-mount",
        "name": "habitat mount",
        "type": "fixed",
        "parent": "pad",
        "child": "habitat",
        "anchorParent": [
          -3.2,
          0.3,
          0
        ],
        "anchorChild": [
          4.440892098500626e-16,
          -1.1999999999999997,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "crusher-mount",
        "name": "crusher mount",
        "type": "fixed",
        "parent": "pad",
        "child": "crusher",
        "anchorParent": [
          0,
          0.3,
          -3
        ],
        "anchorChild": [
          0,
          -0.9750000000000001,
          -0.4424999999999999
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "conveyor-drive",
        "name": "conveyor drive",
        "type": "prismatic",
        "parent": "crusher",
        "child": "conveyor",
        "anchorParent": [
          0,
          -0.375,
          -0.14250000000000007
        ],
        "anchorChild": [
          -0.3250000000000002,
          -0.21999999999999997,
          -1.05
        ],
        "axis": [
          1,
          0,
          0
        ],
        "limits": [
          -0.4,
          0.4
        ]
      },
      {
        "id": "centrifuge-shaft",
        "name": "centrifuge shaft",
        "type": "revolute",
        "parent": "conveyor",
        "child": "centrifuge",
        "anchorParent": [
          2.675,
          1.5799999999999998,
          1.65
        ],
        "anchorChild": [
          0,
          0,
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
        "id": "solar-a-hinge",
        "name": "solar a hinge",
        "type": "revolute",
        "parent": "pad",
        "child": "solar-a",
        "anchorParent": [
          0,
          1,
          -5
        ],
        "anchorChild": [
          0,
          0,
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
        "id": "solar-b-hinge",
        "name": "solar b hinge",
        "type": "revolute",
        "parent": "pad",
        "child": "solar-b",
        "anchorParent": [
          0,
          1,
          5
        ],
        "anchorChild": [
          0,
          0,
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
        "id": "tank-a-lock",
        "name": "tank a lock",
        "type": "fixed",
        "parent": "pad",
        "child": "tank-a",
        "anchorParent": [
          5,
          0.3,
          2.8
        ],
        "anchorChild": [
          0,
          -1.6999999999999997,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "tank-b-lock",
        "name": "tank b lock",
        "type": "fixed",
        "parent": "pad",
        "child": "tank-b",
        "anchorParent": [
          6.7,
          0.3,
          2.8
        ],
        "anchorChild": [
          0,
          -1.6999999999999997,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "rover-dock",
        "name": "rover dock",
        "type": "fixed",
        "parent": "pad",
        "child": "sample-rover",
        "anchorParent": [
          0,
          0.49999999999999994,
          3
        ],
        "anchorChild": [
          0,
          -0.08749999999999991,
          -0.605
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "arm-shoulder",
        "name": "arm shoulder",
        "type": "revolute",
        "parent": "crusher",
        "child": "loading-arm",
        "anchorParent": [
          1.8,
          -0.17500000000000004,
          0.2575000000000003
        ],
        "anchorChild": [
          -1.2999999999999998,
          -2.225481111790155,
          0
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          -0.2,
          1.1
        ]
      },
      {
        "id": "silo-lock",
        "name": "silo lock",
        "type": "fixed",
        "parent": "pad",
        "child": "silo",
        "anchorParent": [
          5.8,
          0.3,
          -3
        ],
        "anchorChild": [
          0,
          -2.05,
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
      "pad",
      "habitat",
      "crusher",
      "conveyor",
      "centrifuge",
      "solar-a",
      "solar-b",
      "tank-a",
      "tank-b",
      "sample-rover",
      "loading-arm",
      "silo"
    ]
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 冲击响应读数（h3-lunar-sample-refinery-dynamic）

Rapier 实际采样轨迹中的最大平移位移是多少？按四位小数报告。

能力：冲击响应读数；形式：single-choice；证据：Rapier。

- A：0
- B：1.0041
- C：0.0041
- D：0.2041

```json
{
  "input": {
    "trace": [
      {
        "time": 0.008333333333333333,
        "displacement": 0.004092667794880611
      },
      {
        "time": 0.10833333333333334,
        "displacement": 0.000010793506916340001
      },
      {
        "time": 0.20833333333333334,
        "displacement": 7.153458795344365e-7
      },
      {
        "time": 0.30833333333333335,
        "displacement": 7.168779931424477e-7
      },
      {
        "time": 0.4083333333333333,
        "displacement": 4.805630277527855e-7
      },
      {
        "time": 0.5083333333333333,
        "displacement": 4.780378086330159e-7
      },
      {
        "time": 0.6083333333333333,
        "displacement": 4.800900202084339e-7
      },
      {
        "time": 0.7083333333333334,
        "displacement": 4.800900202084339e-7
      },
      {
        "time": 0.8083333333333333,
        "displacement": 4.800900202084339e-7
      },
      {
        "time": 0.9083333333333333,
        "displacement": 4.800900202084339e-7
      },
      {
        "time": 1,
        "displacement": 4.800900202084339e-7
      }
    ],
    "impulse": [
      10,
      1.8,
      3.5
    ],
    "nominalDrift": 0.00021837138424291982,
    "scope": "采样轨迹极值，非连续时间极值；不代表实物安全阈值"
  },
  "answer": {
    "choiceId": "C"
  }
}
```

### 关节限位推理（h3-lunar-sample-refinery-kinematic）

下列目标位置/角度中哪些在关节声明限位内（含边界）？

能力：关节限位推理；形式：multiple-choice；证据：model-state。

- A：-3.141592653589793
- B：0
- C：-3.641592653589793
- D：3.641592653589793

```json
{
  "input": {
    "joint": "centrifuge-shaft",
    "limits": [
      -3.141592653589793,
      3.141592653589793
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

### 约束故障诊断（h3-lunar-sample-refinery-diagnosis）

已检测到端点和约束类型如下，选择匹配的全部关节。

能力：约束故障诊断；形式：multiple-choice；证据：model-state。

- A：centrifuge-shaft
- B：conveyor-drive
- C：habitat-mount
- D：crusher-mount

```json
{
  "input": {
    "endpoints": [
      "crusher",
      "conveyor"
    ],
    "type": "prismatic",
    "joints": [
      {
        "id": "habitat-mount",
        "name": "habitat mount",
        "type": "fixed",
        "parent": "pad",
        "child": "habitat",
        "anchorParent": [
          -3.2,
          0.3,
          0
        ],
        "anchorChild": [
          4.440892098500626e-16,
          -1.1999999999999997,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "crusher-mount",
        "name": "crusher mount",
        "type": "fixed",
        "parent": "pad",
        "child": "crusher",
        "anchorParent": [
          0,
          0.3,
          -3
        ],
        "anchorChild": [
          0,
          -0.9750000000000001,
          -0.4424999999999999
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "conveyor-drive",
        "name": "conveyor drive",
        "type": "prismatic",
        "parent": "crusher",
        "child": "conveyor",
        "anchorParent": [
          0,
          -0.375,
          -0.14250000000000007
        ],
        "anchorChild": [
          -0.3250000000000002,
          -0.21999999999999997,
          -1.05
        ],
        "axis": [
          1,
          0,
          0
        ],
        "limits": [
          -0.4,
          0.4
        ]
      },
      {
        "id": "centrifuge-shaft",
        "name": "centrifuge shaft",
        "type": "revolute",
        "parent": "conveyor",
        "child": "centrifuge",
        "anchorParent": [
          2.675,
          1.5799999999999998,
          1.65
        ],
        "anchorChild": [
          0,
          0,
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
        "id": "solar-a-hinge",
        "name": "solar a hinge",
        "type": "revolute",
        "parent": "pad",
        "child": "solar-a",
        "anchorParent": [
          0,
          1,
          -5
        ],
        "anchorChild": [
          0,
          0,
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
        "id": "solar-b-hinge",
        "name": "solar b hinge",
        "type": "revolute",
        "parent": "pad",
        "child": "solar-b",
        "anchorParent": [
          0,
          1,
          5
        ],
        "anchorChild": [
          0,
          0,
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
        "id": "tank-a-lock",
        "name": "tank a lock",
        "type": "fixed",
        "parent": "pad",
        "child": "tank-a",
        "anchorParent": [
          5,
          0.3,
          2.8
        ],
        "anchorChild": [
          0,
          -1.6999999999999997,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "tank-b-lock",
        "name": "tank b lock",
        "type": "fixed",
        "parent": "pad",
        "child": "tank-b",
        "anchorParent": [
          6.7,
          0.3,
          2.8
        ],
        "anchorChild": [
          0,
          -1.6999999999999997,
          0
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "rover-dock",
        "name": "rover dock",
        "type": "fixed",
        "parent": "pad",
        "child": "sample-rover",
        "anchorParent": [
          0,
          0.49999999999999994,
          3
        ],
        "anchorChild": [
          0,
          -0.08749999999999991,
          -0.605
        ],
        "axis": [
          0,
          1,
          0
        ]
      },
      {
        "id": "arm-shoulder",
        "name": "arm shoulder",
        "type": "revolute",
        "parent": "crusher",
        "child": "loading-arm",
        "anchorParent": [
          1.8,
          -0.17500000000000004,
          0.2575000000000003
        ],
        "anchorChild": [
          -1.2999999999999998,
          -2.225481111790155,
          0
        ],
        "axis": [
          0,
          0,
          1
        ],
        "limits": [
          -0.2,
          1.1
        ]
      },
      {
        "id": "silo-lock",
        "name": "silo lock",
        "type": "fixed",
        "parent": "pad",
        "child": "silo",
        "anchorParent": [
          5.8,
          0.3,
          -3
        ],
        "anchorChild": [
          0,
          -2.05,
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

### 主动检查收益（h3-lunar-sample-refinery-information-gain）

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
    "module": "loading-arm",
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

### 不确定性与弃答（h3-lunar-sample-refinery-abstention）

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
        "action": "continue"
      }
    ]
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 观测后信念更新（h3-lunar-sample-refinery-posterior）

均匀先验，得到给定观测后，jammed 世界的后验概率是多少？

能力：观测后信念更新；形式：single-choice；证据：finite-world。

- A：0.3333333333333333
- B：0
- C：0.25
- D：0.5

```json
{
  "input": {
    "module": "loading-arm",
    "worlds": [
      "normal",
      "jammed",
      "reversed",
      "loose"
    ],
    "observationByWorld": [
      "positive",
      "positive",
      "negative",
      "positive"
    ],
    "observed": "positive"
  },
  "answer": {
    "choiceId": "A"
  }
}
```

### 多目标工程权衡（h3-lunar-sample-refinery-pareto）

最小成本、最小质量、最大刚度，选择完整非支配集合。

能力：多目标工程权衡；形式：multiple-choice；证据：model-state。

- A：stock-2
- B：stock-1
- C：stock-3
- D：stock-0

```json
{
  "input": {
    "alternatives": [
      {
        "id": "stock-0",
        "cost": 7,
        "stiffness": 4,
        "mass": 1.2
      },
      {
        "id": "stock-1",
        "cost": 5,
        "stiffness": 7,
        "mass": 1.6
      },
      {
        "id": "stock-2",
        "cost": 7,
        "stiffness": 7,
        "mass": 1.2
      },
      {
        "id": "stock-3",
        "cost": 6,
        "stiffness": 10,
        "mass": 0.7
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

### 依赖装配（h3-lunar-sample-refinery-assembly）

提交 actionIds。执行公开前置条件与效果，达到所有目标且不超过预算；允许交换独立动作。

能力：依赖装配；形式：actions；证据：state-machine。


```json
{
  "input": {
    "initialFacts": [],
    "initialModules": [],
    "actions": [
      {
        "id": "place:conveyor",
        "label": "安装 conveyor",
        "requires": [
          "present:crusher"
        ],
        "forbids": [
          "present:conveyor"
        ],
        "adds": [
          "present:conveyor"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "conveyor",
          "visible": true
        }
      },
      {
        "id": "place:centrifuge",
        "label": "安装 centrifuge",
        "requires": [
          "present:conveyor"
        ],
        "forbids": [
          "present:centrifuge"
        ],
        "adds": [
          "present:centrifuge"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "centrifuge",
          "visible": true
        }
      },
      {
        "id": "place:solar-a",
        "label": "安装 solar-a",
        "requires": [
          "present:pad"
        ],
        "forbids": [
          "present:solar-a"
        ],
        "adds": [
          "present:solar-a"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "solar-a",
          "visible": true
        }
      },
      {
        "id": "place:tank-a",
        "label": "安装 tank-a",
        "requires": [
          "present:pad"
        ],
        "forbids": [
          "present:tank-a"
        ],
        "adds": [
          "present:tank-a"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "tank-a",
          "visible": true
        }
      },
      {
        "id": "place:tank-b",
        "label": "安装 tank-b",
        "requires": [
          "present:pad"
        ],
        "forbids": [
          "present:tank-b"
        ],
        "adds": [
          "present:tank-b"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "tank-b",
          "visible": true
        }
      },
      {
        "id": "place:sample-rover",
        "label": "安装 sample-rover",
        "requires": [
          "present:pad"
        ],
        "forbids": [
          "present:sample-rover"
        ],
        "adds": [
          "present:sample-rover"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "sample-rover",
          "visible": true
        }
      },
      {
        "id": "place:pad",
        "label": "安装 pad",
        "requires": [],
        "forbids": [
          "present:pad"
        ],
        "adds": [
          "present:pad"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "pad",
          "visible": true
        }
      },
      {
        "id": "place:silo",
        "label": "安装 silo",
        "requires": [
          "present:pad"
        ],
        "forbids": [
          "present:silo"
        ],
        "adds": [
          "present:silo"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "silo",
          "visible": true
        }
      },
      {
        "id": "place:crusher",
        "label": "安装 crusher",
        "requires": [
          "present:pad"
        ],
        "forbids": [
          "present:crusher"
        ],
        "adds": [
          "present:crusher"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "crusher",
          "visible": true
        }
      },
      {
        "id": "place:habitat",
        "label": "安装 habitat",
        "requires": [
          "present:pad"
        ],
        "forbids": [
          "present:habitat"
        ],
        "adds": [
          "present:habitat"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "habitat",
          "visible": true
        }
      },
      {
        "id": "place:solar-b",
        "label": "安装 solar-b",
        "requires": [
          "present:pad"
        ],
        "forbids": [
          "present:solar-b"
        ],
        "adds": [
          "present:solar-b"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "solar-b",
          "visible": true
        }
      },
      {
        "id": "place:loading-arm",
        "label": "安装 loading-arm",
        "requires": [
          "present:crusher"
        ],
        "forbids": [
          "present:loading-arm"
        ],
        "adds": [
          "present:loading-arm"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "loading-arm",
          "visible": true
        }
      }
    ],
    "goalFacts": [
      "present:pad",
      "present:habitat",
      "present:crusher",
      "present:conveyor",
      "present:centrifuge",
      "present:solar-a",
      "present:solar-b",
      "present:tank-a",
      "present:tank-b",
      "present:sample-rover",
      "present:loading-arm",
      "present:silo"
    ],
    "budget": 12,
    "semantics": "requires must hold; forbids must be absent; effects apply in order; unit action cost"
  },
  "answer": {
    "actionIds": [
      "place:pad",
      "place:solar-a",
      "place:tank-a",
      "place:tank-b",
      "place:sample-rover",
      "place:silo",
      "place:crusher",
      "place:conveyor",
      "place:centrifuge",
      "place:habitat",
      "place:solar-b",
      "place:loading-arm"
    ]
  }
}
```

### 依赖拆解（h3-lunar-sample-refinery-disassembly）

提交 actionIds。执行公开前置条件与效果，达到所有目标且不超过预算；允许交换独立动作。

能力：依赖拆解；形式：actions；证据：state-machine。


```json
{
  "input": {
    "initialFacts": [
      "present:pad",
      "present:habitat",
      "present:crusher",
      "present:conveyor",
      "present:centrifuge",
      "present:solar-a",
      "present:solar-b",
      "present:tank-a",
      "present:tank-b",
      "present:sample-rover",
      "present:loading-arm",
      "present:silo"
    ],
    "initialModules": [
      "pad",
      "habitat",
      "crusher",
      "conveyor",
      "centrifuge",
      "solar-a",
      "solar-b",
      "tank-a",
      "tank-b",
      "sample-rover",
      "loading-arm",
      "silo"
    ],
    "actions": [
      {
        "id": "remove:silo",
        "label": "拆除 silo",
        "requires": [
          "present:silo"
        ],
        "forbids": [],
        "adds": [
          "removed:silo"
        ],
        "deletes": [
          "present:silo"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "silo",
          "visible": false
        }
      },
      {
        "id": "remove:loading-arm",
        "label": "拆除 loading-arm",
        "requires": [
          "present:loading-arm"
        ],
        "forbids": [],
        "adds": [
          "removed:loading-arm"
        ],
        "deletes": [
          "present:loading-arm"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "loading-arm",
          "visible": false
        }
      },
      {
        "id": "remove:solar-a",
        "label": "拆除 solar-a",
        "requires": [
          "present:solar-a"
        ],
        "forbids": [],
        "adds": [
          "removed:solar-a"
        ],
        "deletes": [
          "present:solar-a"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "solar-a",
          "visible": false
        }
      },
      {
        "id": "remove:conveyor",
        "label": "拆除 conveyor",
        "requires": [
          "present:conveyor"
        ],
        "forbids": [
          "present:centrifuge"
        ],
        "adds": [
          "removed:conveyor"
        ],
        "deletes": [
          "present:conveyor"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "conveyor",
          "visible": false
        }
      },
      {
        "id": "remove:sample-rover",
        "label": "拆除 sample-rover",
        "requires": [
          "present:sample-rover"
        ],
        "forbids": [],
        "adds": [
          "removed:sample-rover"
        ],
        "deletes": [
          "present:sample-rover"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "sample-rover",
          "visible": false
        }
      },
      {
        "id": "remove:crusher",
        "label": "拆除 crusher",
        "requires": [
          "present:crusher"
        ],
        "forbids": [
          "present:conveyor",
          "present:loading-arm"
        ],
        "adds": [
          "removed:crusher"
        ],
        "deletes": [
          "present:crusher"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "crusher",
          "visible": false
        }
      },
      {
        "id": "remove:habitat",
        "label": "拆除 habitat",
        "requires": [
          "present:habitat"
        ],
        "forbids": [],
        "adds": [
          "removed:habitat"
        ],
        "deletes": [
          "present:habitat"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "habitat",
          "visible": false
        }
      },
      {
        "id": "remove:tank-b",
        "label": "拆除 tank-b",
        "requires": [
          "present:tank-b"
        ],
        "forbids": [],
        "adds": [
          "removed:tank-b"
        ],
        "deletes": [
          "present:tank-b"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "tank-b",
          "visible": false
        }
      },
      {
        "id": "remove:solar-b",
        "label": "拆除 solar-b",
        "requires": [
          "present:solar-b"
        ],
        "forbids": [],
        "adds": [
          "removed:solar-b"
        ],
        "deletes": [
          "present:solar-b"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "solar-b",
          "visible": false
        }
      },
      {
        "id": "remove:tank-a",
        "label": "拆除 tank-a",
        "requires": [
          "present:tank-a"
        ],
        "forbids": [],
        "adds": [
          "removed:tank-a"
        ],
        "deletes": [
          "present:tank-a"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "tank-a",
          "visible": false
        }
      },
      {
        "id": "remove:pad",
        "label": "拆除 pad",
        "requires": [
          "present:pad"
        ],
        "forbids": [
          "present:habitat",
          "present:crusher",
          "present:solar-a",
          "present:solar-b",
          "present:tank-a",
          "present:tank-b",
          "present:sample-rover",
          "present:silo"
        ],
        "adds": [
          "removed:pad"
        ],
        "deletes": [
          "present:pad"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "pad",
          "visible": false
        }
      },
      {
        "id": "remove:centrifuge",
        "label": "拆除 centrifuge",
        "requires": [
          "present:centrifuge"
        ],
        "forbids": [],
        "adds": [
          "removed:centrifuge"
        ],
        "deletes": [
          "present:centrifuge"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "centrifuge",
          "visible": false
        }
      }
    ],
    "goalFacts": [
      "removed:silo",
      "removed:loading-arm",
      "removed:sample-rover",
      "removed:tank-b",
      "removed:tank-a",
      "removed:solar-b",
      "removed:solar-a",
      "removed:centrifuge",
      "removed:conveyor",
      "removed:crusher",
      "removed:habitat",
      "removed:pad"
    ],
    "budget": 12,
    "semantics": "requires must hold; forbids must be absent; effects apply in order; unit action cost"
  },
  "answer": {
    "actionIds": [
      "remove:silo",
      "remove:loading-arm",
      "remove:solar-a",
      "remove:sample-rover",
      "remove:habitat",
      "remove:tank-b",
      "remove:solar-b",
      "remove:tank-a",
      "remove:centrifuge",
      "remove:conveyor",
      "remove:crusher",
      "remove:pad"
    ]
  }
}
```

### 承载维修（h3-lunar-sample-refinery-service-repair）

提交 actionIds。执行公开前置条件与效果，达到所有目标且不超过预算；允许交换独立动作。

能力：承载维修；形式：actions；证据：state-machine。


```json
{
  "input": {
    "initialFacts": [
      "fault:loading-arm",
      "closed:loading-arm"
    ],
    "initialModules": [
      "pad",
      "habitat",
      "crusher",
      "conveyor",
      "centrifuge",
      "solar-a",
      "solar-b",
      "tank-a",
      "tank-b",
      "sample-rover",
      "loading-arm",
      "silo"
    ],
    "actions": [
      {
        "id": "replace:loading-arm",
        "label": "replace loading-arm",
        "requires": [
          "done:remove:loading-arm"
        ],
        "forbids": [
          "done:replace:loading-arm"
        ],
        "adds": [
          "done:replace:loading-arm"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "loading-arm",
          "visible": true
        }
      },
      {
        "id": "open:loading-arm",
        "label": "open loading-arm",
        "requires": [
          "done:support:loading-arm"
        ],
        "forbids": [
          "done:open:loading-arm"
        ],
        "adds": [
          "done:open:loading-arm"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "loading-arm"
        }
      },
      {
        "id": "support:loading-arm",
        "label": "support loading-arm",
        "requires": [
          "fault:loading-arm"
        ],
        "forbids": [
          "done:support:loading-arm"
        ],
        "adds": [
          "done:support:loading-arm"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "loading-arm"
        }
      },
      {
        "id": "remove:loading-arm",
        "label": "remove loading-arm",
        "requires": [
          "done:open:loading-arm"
        ],
        "forbids": [
          "done:remove:loading-arm"
        ],
        "adds": [
          "done:remove:loading-arm"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "loading-arm",
          "visible": false
        }
      },
      {
        "id": "release:loading-arm",
        "label": "release loading-arm",
        "requires": [
          "done:close:loading-arm"
        ],
        "forbids": [
          "done:release:loading-arm"
        ],
        "adds": [
          "done:release:loading-arm",
          "repaired:loading-arm"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "loading-arm"
        }
      },
      {
        "id": "close:loading-arm",
        "label": "close loading-arm",
        "requires": [
          "done:verify:loading-arm"
        ],
        "forbids": [
          "done:close:loading-arm"
        ],
        "adds": [
          "done:close:loading-arm"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "loading-arm"
        }
      },
      {
        "id": "verify:loading-arm",
        "label": "verify loading-arm",
        "requires": [
          "done:replace:loading-arm"
        ],
        "forbids": [
          "done:verify:loading-arm"
        ],
        "adds": [
          "done:verify:loading-arm"
        ],
        "deletes": [
          "fault:loading-arm"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "loading-arm"
        }
      }
    ],
    "goalFacts": [
      "repaired:loading-arm"
    ],
    "budget": 7,
    "semantics": "requires must hold; forbids must be absent; effects apply in order; unit action cost"
  },
  "answer": {
    "actionIds": [
      "support:loading-arm",
      "open:loading-arm",
      "remove:loading-arm",
      "replace:loading-arm",
      "verify:loading-arm",
      "close:loading-arm",
      "release:loading-arm"
    ]
  }
}
```

### 复合编辑验证（h3-lunar-sample-refinery-compound-edit）

提交 actionIds。执行公开前置条件与效果，达到所有目标且不超过预算；允许交换独立动作。

能力：复合编辑验证；形式：actions；证据：state-machine。


```json
{
  "input": {
    "initialFacts": [
      "fault:loading-arm",
      "closed:loading-arm"
    ],
    "initialModules": [
      "pad",
      "habitat",
      "crusher",
      "conveyor",
      "centrifuge",
      "solar-a",
      "solar-b",
      "tank-a",
      "tank-b",
      "sample-rover",
      "loading-arm",
      "silo"
    ],
    "actions": [
      {
        "id": "open:loading-arm",
        "label": "open loading-arm",
        "requires": [
          "done:support:loading-arm"
        ],
        "forbids": [
          "done:open:loading-arm"
        ],
        "adds": [
          "done:open:loading-arm"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "loading-arm"
        }
      },
      {
        "id": "recolor:loading-arm",
        "label": "recolor loading-arm",
        "requires": [
          "done:open:loading-arm"
        ],
        "forbids": [
          "done:recolor:loading-arm"
        ],
        "adds": [
          "done:recolor:loading-arm"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "loading-arm",
          "color": "#ea7635"
        }
      },
      {
        "id": "support:loading-arm",
        "label": "support loading-arm",
        "requires": [
          "fault:loading-arm"
        ],
        "forbids": [
          "done:support:loading-arm"
        ],
        "adds": [
          "done:support:loading-arm"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "loading-arm"
        }
      },
      {
        "id": "release:loading-arm",
        "label": "release loading-arm",
        "requires": [
          "done:close:loading-arm"
        ],
        "forbids": [
          "done:release:loading-arm"
        ],
        "adds": [
          "done:release:loading-arm",
          "repaired:loading-arm"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "loading-arm"
        }
      },
      {
        "id": "close:loading-arm",
        "label": "close loading-arm",
        "requires": [
          "done:verify:loading-arm"
        ],
        "forbids": [
          "done:close:loading-arm"
        ],
        "adds": [
          "done:close:loading-arm"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "loading-arm"
        }
      },
      {
        "id": "verify:loading-arm",
        "label": "verify loading-arm",
        "requires": [
          "done:recolor:loading-arm"
        ],
        "forbids": [
          "done:verify:loading-arm"
        ],
        "adds": [
          "done:verify:loading-arm"
        ],
        "deletes": [
          "fault:loading-arm"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "loading-arm"
        }
      }
    ],
    "goalFacts": [
      "repaired:loading-arm"
    ],
    "budget": 6,
    "semantics": "requires must hold; forbids must be absent; effects apply in order; unit action cost"
  },
  "answer": {
    "actionIds": [
      "support:loading-arm",
      "open:loading-arm",
      "recolor:loading-arm",
      "verify:loading-arm",
      "close:loading-arm",
      "release:loading-arm"
    ]
  }
}
```

### 跨区域联合维修（h3-lunar-sample-refinery-multi-fault）

提交 actionIds。执行公开前置条件与效果，达到所有目标且不超过预算；允许交换独立动作。

能力：跨区域联合维修；形式：actions；证据：state-machine。


```json
{
  "input": {
    "initialFacts": [
      "fault:tank-b",
      "closed:tank-b",
      "fault:sample-rover",
      "closed:sample-rover",
      "fault:loading-arm",
      "closed:loading-arm",
      "fault:silo",
      "closed:silo"
    ],
    "initialModules": [
      "pad",
      "habitat",
      "crusher",
      "conveyor",
      "centrifuge",
      "solar-a",
      "solar-b",
      "tank-a",
      "tank-b",
      "sample-rover",
      "loading-arm",
      "silo"
    ],
    "actions": [
      {
        "id": "close:tank-b",
        "label": "close tank-b",
        "requires": [
          "done:verify:tank-b"
        ],
        "forbids": [
          "done:close:tank-b"
        ],
        "adds": [
          "done:close:tank-b"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "tank-b"
        }
      },
      {
        "id": "replace:silo",
        "label": "replace silo",
        "requires": [
          "done:remove:silo"
        ],
        "forbids": [
          "done:replace:silo"
        ],
        "adds": [
          "done:replace:silo"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "silo",
          "visible": true
        }
      },
      {
        "id": "close:silo",
        "label": "close silo",
        "requires": [
          "done:verify:silo"
        ],
        "forbids": [
          "done:close:silo"
        ],
        "adds": [
          "done:close:silo"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "silo"
        }
      },
      {
        "id": "replace:loading-arm",
        "label": "replace loading-arm",
        "requires": [
          "done:remove:loading-arm"
        ],
        "forbids": [
          "done:replace:loading-arm"
        ],
        "adds": [
          "done:replace:loading-arm"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "loading-arm",
          "visible": true
        }
      },
      {
        "id": "open:loading-arm",
        "label": "open loading-arm",
        "requires": [
          "done:support:loading-arm"
        ],
        "forbids": [
          "done:open:loading-arm"
        ],
        "adds": [
          "done:open:loading-arm"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "loading-arm"
        }
      },
      {
        "id": "release:silo",
        "label": "release silo",
        "requires": [
          "done:close:silo"
        ],
        "forbids": [
          "done:release:silo"
        ],
        "adds": [
          "done:release:silo",
          "repaired:silo"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "silo"
        }
      },
      {
        "id": "support:loading-arm",
        "label": "support loading-arm",
        "requires": [
          "fault:loading-arm"
        ],
        "forbids": [
          "done:support:loading-arm"
        ],
        "adds": [
          "done:support:loading-arm"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "loading-arm"
        }
      },
      {
        "id": "remove:silo",
        "label": "remove silo",
        "requires": [
          "done:open:silo"
        ],
        "forbids": [
          "done:remove:silo"
        ],
        "adds": [
          "done:remove:silo"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "silo",
          "visible": false
        }
      },
      {
        "id": "remove:loading-arm",
        "label": "remove loading-arm",
        "requires": [
          "done:open:loading-arm"
        ],
        "forbids": [
          "done:remove:loading-arm"
        ],
        "adds": [
          "done:remove:loading-arm"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "loading-arm",
          "visible": false
        }
      },
      {
        "id": "open:sample-rover",
        "label": "open sample-rover",
        "requires": [
          "done:support:sample-rover"
        ],
        "forbids": [
          "done:open:sample-rover"
        ],
        "adds": [
          "done:open:sample-rover"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "sample-rover"
        }
      },
      {
        "id": "replace:sample-rover",
        "label": "replace sample-rover",
        "requires": [
          "done:remove:sample-rover"
        ],
        "forbids": [
          "done:replace:sample-rover"
        ],
        "adds": [
          "done:replace:sample-rover"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "sample-rover",
          "visible": true
        }
      },
      {
        "id": "remove:sample-rover",
        "label": "remove sample-rover",
        "requires": [
          "done:open:sample-rover"
        ],
        "forbids": [
          "done:remove:sample-rover"
        ],
        "adds": [
          "done:remove:sample-rover"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "sample-rover",
          "visible": false
        }
      },
      {
        "id": "verify:silo",
        "label": "verify silo",
        "requires": [
          "done:replace:silo"
        ],
        "forbids": [
          "done:verify:silo"
        ],
        "adds": [
          "done:verify:silo"
        ],
        "deletes": [
          "fault:silo"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "silo"
        }
      },
      {
        "id": "release:loading-arm",
        "label": "release loading-arm",
        "requires": [
          "done:close:loading-arm"
        ],
        "forbids": [
          "done:release:loading-arm"
        ],
        "adds": [
          "done:release:loading-arm",
          "repaired:loading-arm"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "loading-arm"
        }
      },
      {
        "id": "open:tank-b",
        "label": "open tank-b",
        "requires": [
          "done:support:tank-b"
        ],
        "forbids": [
          "done:open:tank-b"
        ],
        "adds": [
          "done:open:tank-b"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "tank-b"
        }
      },
      {
        "id": "support:silo",
        "label": "support silo",
        "requires": [
          "fault:silo"
        ],
        "forbids": [
          "done:support:silo"
        ],
        "adds": [
          "done:support:silo"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "silo"
        }
      },
      {
        "id": "release:tank-b",
        "label": "release tank-b",
        "requires": [
          "done:close:tank-b"
        ],
        "forbids": [
          "done:release:tank-b"
        ],
        "adds": [
          "done:release:tank-b",
          "repaired:tank-b"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "tank-b"
        }
      },
      {
        "id": "remove:tank-b",
        "label": "remove tank-b",
        "requires": [
          "done:open:tank-b"
        ],
        "forbids": [
          "done:remove:tank-b"
        ],
        "adds": [
          "done:remove:tank-b"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "tank-b",
          "visible": false
        }
      },
      {
        "id": "close:loading-arm",
        "label": "close loading-arm",
        "requires": [
          "done:verify:loading-arm"
        ],
        "forbids": [
          "done:close:loading-arm"
        ],
        "adds": [
          "done:close:loading-arm"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "loading-arm"
        }
      },
      {
        "id": "close:sample-rover",
        "label": "close sample-rover",
        "requires": [
          "done:verify:sample-rover"
        ],
        "forbids": [
          "done:close:sample-rover"
        ],
        "adds": [
          "done:close:sample-rover"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "sample-rover"
        }
      },
      {
        "id": "open:silo",
        "label": "open silo",
        "requires": [
          "done:support:silo"
        ],
        "forbids": [
          "done:open:silo"
        ],
        "adds": [
          "done:open:silo"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "silo"
        }
      },
      {
        "id": "replace:tank-b",
        "label": "replace tank-b",
        "requires": [
          "done:remove:tank-b"
        ],
        "forbids": [
          "done:replace:tank-b"
        ],
        "adds": [
          "done:replace:tank-b"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "tank-b",
          "visible": true
        }
      },
      {
        "id": "verify:sample-rover",
        "label": "verify sample-rover",
        "requires": [
          "done:replace:sample-rover"
        ],
        "forbids": [
          "done:verify:sample-rover"
        ],
        "adds": [
          "done:verify:sample-rover"
        ],
        "deletes": [
          "fault:sample-rover"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "sample-rover"
        }
      },
      {
        "id": "release:sample-rover",
        "label": "release sample-rover",
        "requires": [
          "done:close:sample-rover"
        ],
        "forbids": [
          "done:release:sample-rover"
        ],
        "adds": [
          "done:release:sample-rover",
          "repaired:sample-rover"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "sample-rover"
        }
      },
      {
        "id": "support:tank-b",
        "label": "support tank-b",
        "requires": [
          "fault:tank-b"
        ],
        "forbids": [
          "done:support:tank-b"
        ],
        "adds": [
          "done:support:tank-b"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "tank-b"
        }
      },
      {
        "id": "verify:tank-b",
        "label": "verify tank-b",
        "requires": [
          "done:replace:tank-b"
        ],
        "forbids": [
          "done:verify:tank-b"
        ],
        "adds": [
          "done:verify:tank-b"
        ],
        "deletes": [
          "fault:tank-b"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "tank-b"
        }
      },
      {
        "id": "verify:loading-arm",
        "label": "verify loading-arm",
        "requires": [
          "done:replace:loading-arm"
        ],
        "forbids": [
          "done:verify:loading-arm"
        ],
        "adds": [
          "done:verify:loading-arm"
        ],
        "deletes": [
          "fault:loading-arm"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "loading-arm"
        }
      },
      {
        "id": "support:sample-rover",
        "label": "support sample-rover",
        "requires": [
          "fault:sample-rover"
        ],
        "forbids": [
          "done:support:sample-rover"
        ],
        "adds": [
          "done:support:sample-rover"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "sample-rover"
        }
      }
    ],
    "goalFacts": [
      "repaired:tank-b",
      "repaired:sample-rover",
      "repaired:loading-arm",
      "repaired:silo"
    ],
    "budget": 28,
    "semantics": "requires must hold; forbids must be absent; effects apply in order; unit action cost"
  },
  "answer": {
    "actionIds": [
      "support:loading-arm",
      "open:loading-arm",
      "remove:loading-arm",
      "replace:loading-arm",
      "support:silo",
      "open:silo",
      "remove:silo",
      "replace:silo",
      "verify:silo",
      "close:silo",
      "release:silo",
      "support:tank-b",
      "open:tank-b",
      "remove:tank-b",
      "replace:tank-b",
      "verify:tank-b",
      "close:tank-b",
      "release:tank-b",
      "verify:loading-arm",
      "close:loading-arm",
      "release:loading-arm",
      "support:sample-rover",
      "open:sample-rover",
      "remove:sample-rover",
      "replace:sample-rover",
      "verify:sample-rover",
      "close:sample-rover",
      "release:sample-rover"
    ]
  }
}
```

### 多工位资源调度（h3-lunar-sample-refinery-scheduling）

为所有工单提交整数 starts，满足先后关系、独占工位及截止时间。

能力：多工位资源调度；形式：schedule；证据：resource-schedule。


```json
{
  "input": {
    "jobs": [
      {
        "id": "job-0",
        "module": "pad",
        "duration": 1,
        "resource": "test-bench",
        "after": []
      },
      {
        "id": "job-1",
        "module": "habitat",
        "duration": 3,
        "resource": "technician",
        "after": []
      },
      {
        "id": "job-2",
        "module": "crusher",
        "duration": 2,
        "resource": "test-bench",
        "after": [
          "job-0"
        ]
      },
      {
        "id": "job-3",
        "module": "conveyor",
        "duration": 3,
        "resource": "technician",
        "after": [
          "job-1"
        ]
      },
      {
        "id": "job-4",
        "module": "centrifuge",
        "duration": 3,
        "resource": "test-bench",
        "after": [
          "job-2"
        ]
      },
      {
        "id": "job-5",
        "module": "solar-a",
        "duration": 2,
        "resource": "technician",
        "after": [
          "job-3"
        ]
      },
      {
        "id": "job-6",
        "module": "solar-b",
        "duration": 3,
        "resource": "test-bench",
        "after": [
          "job-4"
        ]
      },
      {
        "id": "job-7",
        "module": "tank-a",
        "duration": 2,
        "resource": "technician",
        "after": [
          "job-5"
        ]
      },
      {
        "id": "job-8",
        "module": "tank-b",
        "duration": 2,
        "resource": "test-bench",
        "after": [
          "job-6"
        ]
      },
      {
        "id": "job-9",
        "module": "sample-rover",
        "duration": 3,
        "resource": "technician",
        "after": [
          "job-7"
        ]
      }
    ],
    "deadline": 13
  },
  "answer": {
    "starts": {
      "job-0": 0,
      "job-1": 0,
      "job-2": 1,
      "job-3": 3,
      "job-4": 3,
      "job-5": 6,
      "job-6": 6,
      "job-7": 8,
      "job-8": 9,
      "job-9": 10
    }
  }
}
```

### 检查后条件策略（h3-lunar-sample-refinery-policy）

提交一个检查及 observation→action 决策表，在所有相容世界中采取正确动作。

能力：检查后条件策略；形式：policy；证据：finite-world。


```json
{
  "input": {
    "module": "loading-arm",
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

### 局部坐标变换（h3-lunar-sample-refinery-local-frame）

将模块局部点通过给定四元数与平移转换为世界点，保留五位小数。

能力：局部坐标变换；形式：single-choice；证据：model-state。

- A：[4.1,2.3,-1.6]
- B：[3.1,1.3,-2.6]
- C：[-0.3,-2.22548,0]
- D：[2.8,1.3,-2.3]

```json
{
  "input": {
    "localPoint": [
      -0.2999999999999998,
      -2.225481111790155,
      0
    ],
    "rotationXYZW": [
      0,
      0.7071067811865476,
      0,
      -0.7071067811865475
    ],
    "translation": [
      3.0999999999999996,
      3.5254811117901554,
      -2.3
    ]
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 正交视图投影（h3-lunar-sample-refinery-projection）

按公开视图坐标约定，选择该世界点投影后的二维坐标。

能力：正交视图投影；形式：single-choice；证据：model-state。

- A：[11,5]
- B：[5,6]
- C：[0,0]
- D：[5,11]

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
    "choiceId": "D"
  }
}
```

### 空间相对关系（h3-lunar-sample-refinery-relative-order）

比较B相对A在指定世界轴上的模块原点坐标。

能力：空间相对关系；形式：single-choice；证据：model-state。

- A：equal
- B：greater
- C：less

```json
{
  "input": {
    "A": {
      "id": "pad",
      "position": [
        0,
        0.2,
        0
      ]
    },
    "B": {
      "id": "silo",
      "position": [
        5.8,
        2.55,
        -3
      ]
    },
    "axis": "x"
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 约束自由度（h3-lunar-sample-refinery-joint-axis）

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
      "id": "silo-lock",
      "name": "silo lock",
      "type": "fixed",
      "parent": "pad",
      "child": "silo",
      "anchorParent": [
        5.8,
        0.3,
        -3
      ],
      "anchorChild": [
        0,
        -2.05,
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
    "choiceId": "A"
  }
}
```

### 维修间隙预算（h3-lunar-sample-refinery-clearance-margin）

给定理想直槽净宽、工具宽度、单侧安全余量，工具是否满足横向间隙要求？

能力：维修间隙预算；形式：single-choice；证据：model-state。

- A：blocked
- B：feasible

```json
{
  "input": {
    "module": "loading-arm",
    "aperture": 0.71,
    "toolWidth": 0.65,
    "eachSideMargin": 0
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 载荷力矩（h3-lunar-sample-refinery-load-moment）

绕给定原点的载荷力矩r×F是多少？采用右手系，忽略其他力。

能力：载荷力矩；形式：single-choice；证据：model-state。

- A：[0,0,0]
- B：[0,-4,0]
- C：[0,0,-24]
- D：[0,0,24]

```json
{
  "input": {
    "module": "loading-arm",
    "lever": [
      4,
      1,
      0
    ],
    "force": [
      0,
      -6,
      0
    ],
    "units": "scene-length × force"
  },
  "answer": {
    "choiceId": "C"
  }
}
```

### 非均匀先验更新（h3-lunar-sample-refinery-weighted-posterior）

先验权重未归一化，观测只保留normal和jammed，求jammed后验概率。

能力：非均匀先验更新；形式：single-choice；证据：finite-world。

- A：0.2857142857142857
- B：0
- C：1
- D：0.4444444444444444

```json
{
  "input": {
    "module": "loading-arm",
    "worlds": [
      "normal",
      "jammed",
      "loose"
    ],
    "weights": [
      5,
      4,
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

### 风险最小决策（h3-lunar-sample-refinery-expected-loss）

继续运行期望损失=p×failureLoss，预防维修损失=repairCost，选择损失较低者；并列选继续。

能力：风险最小决策；形式：single-choice；证据：finite-world。

- A：continue
- B：repair

```json
{
  "input": {
    "faultProbability": 0.4,
    "repairCost": 2,
    "failureLoss": 16,
    "module": "loading-arm"
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 轨迹阈值判定（h3-lunar-sample-refinery-trace-threshold）

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
        "displacement": 0.004092667794880611
      },
      {
        "time": 0.10833333333333334,
        "displacement": 0.000010793506916340001
      },
      {
        "time": 0.20833333333333334,
        "displacement": 7.153458795344365e-7
      },
      {
        "time": 0.30833333333333335,
        "displacement": 7.168779931424477e-7
      },
      {
        "time": 0.4083333333333333,
        "displacement": 4.805630277527855e-7
      },
      {
        "time": 0.5083333333333333,
        "displacement": 4.780378086330159e-7
      },
      {
        "time": 0.6083333333333333,
        "displacement": 4.800900202084339e-7
      },
      {
        "time": 0.7083333333333334,
        "displacement": 4.800900202084339e-7
      },
      {
        "time": 0.8083333333333333,
        "displacement": 4.800900202084339e-7
      },
      {
        "time": 0.9083333333333333,
        "displacement": 4.800900202084339e-7
      },
      {
        "time": 1,
        "displacement": 4.800900202084339e-7
      }
    ],
    "threshold": 0.004911201353856733
  },
  "answer": {
    "choiceId": "B"
  }
}
```

### 安全联锁维修（h3-lunar-sample-refinery-guarded-repair）

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
        "id": "release:loading-arm",
        "label": "release loading-arm",
        "requires": [
          "done:relock:loading-arm"
        ],
        "forbids": [
          "done:release:loading-arm"
        ],
        "adds": [
          "done:release:loading-arm",
          "ready:loading-arm",
          "tool:free"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "loading-arm"
        }
      },
      {
        "id": "relock:loading-arm",
        "label": "relock loading-arm",
        "requires": [
          "done:verify:loading-arm"
        ],
        "forbids": [
          "done:relock:loading-arm"
        ],
        "adds": [
          "done:relock:loading-arm"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "loading-arm"
        }
      },
      {
        "id": "verify:loading-arm",
        "label": "verify loading-arm",
        "requires": [
          "done:replace:loading-arm"
        ],
        "forbids": [
          "done:verify:loading-arm"
        ],
        "adds": [
          "done:verify:loading-arm"
        ],
        "deletes": [
          "fault:loading-arm",
          "misaligned:loading-arm"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "loading-arm"
        }
      },
      {
        "id": "replace:loading-arm",
        "label": "replace loading-arm",
        "requires": [
          "done:unlock:loading-arm"
        ],
        "forbids": [
          "done:replace:loading-arm"
        ],
        "adds": [
          "done:replace:loading-arm"
        ],
        "deletes": [],
        "cost": 2,
        "visual": {
          "moduleId": "loading-arm"
        }
      },
      {
        "id": "unlock:loading-arm",
        "label": "unlock loading-arm",
        "requires": [
          "done:support:loading-arm"
        ],
        "forbids": [
          "done:unlock:loading-arm"
        ],
        "adds": [
          "done:unlock:loading-arm"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "loading-arm"
        }
      },
      {
        "id": "support:loading-arm",
        "label": "support loading-arm",
        "requires": [
          "done:isolate:loading-arm"
        ],
        "forbids": [
          "done:support:loading-arm"
        ],
        "adds": [
          "done:support:loading-arm"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "loading-arm"
        }
      },
      {
        "id": "isolate:loading-arm",
        "label": "isolate loading-arm",
        "requires": [
          "tool:free",
          "fault:loading-arm"
        ],
        "forbids": [
          "done:isolate:loading-arm"
        ],
        "adds": [
          "done:isolate:loading-arm"
        ],
        "deletes": [
          "tool:free"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "loading-arm"
        }
      }
    ],
    "initialFacts": [
      "tool:free",
      "fault:loading-arm"
    ],
    "initialModules": [
      "pad",
      "habitat",
      "crusher",
      "conveyor",
      "centrifuge",
      "solar-a",
      "solar-b",
      "tank-a",
      "tank-b",
      "sample-rover",
      "loading-arm",
      "silo"
    ],
    "goalFacts": [
      "ready:loading-arm"
    ],
    "absentFacts": [
      "unverified"
    ],
    "budget": 8
  },
  "answer": {
    "actionIds": [
      "isolate:loading-arm",
      "support:loading-arm",
      "unlock:loading-arm",
      "replace:loading-arm",
      "verify:loading-arm",
      "relock:loading-arm",
      "release:loading-arm"
    ]
  }
}
```

### 失败状态回退（h3-lunar-sample-refinery-rollback）

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
        "id": "resume:loading-arm",
        "label": "resume loading-arm",
        "requires": [
          "done:verify:loading-arm"
        ],
        "forbids": [
          "done:resume:loading-arm"
        ],
        "adds": [
          "done:resume:loading-arm",
          "ready:loading-arm",
          "tool:free"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "loading-arm"
        }
      },
      {
        "id": "verify:loading-arm",
        "label": "verify loading-arm",
        "requires": [
          "done:align:loading-arm"
        ],
        "forbids": [
          "done:verify:loading-arm"
        ],
        "adds": [
          "done:verify:loading-arm"
        ],
        "deletes": [
          "fault:loading-arm",
          "misaligned:loading-arm"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "loading-arm"
        }
      },
      {
        "id": "align:loading-arm",
        "label": "align loading-arm",
        "requires": [
          "done:undo:loading-arm"
        ],
        "forbids": [
          "done:align:loading-arm"
        ],
        "adds": [
          "done:align:loading-arm"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "loading-arm",
          "visible": true
        }
      },
      {
        "id": "undo:loading-arm",
        "label": "undo loading-arm",
        "requires": [
          "done:isolate:loading-arm"
        ],
        "forbids": [
          "done:undo:loading-arm"
        ],
        "adds": [
          "done:undo:loading-arm"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "loading-arm",
          "visible": false
        }
      },
      {
        "id": "isolate:loading-arm",
        "label": "isolate loading-arm",
        "requires": [
          "tool:free",
          "fault:loading-arm"
        ],
        "forbids": [
          "done:isolate:loading-arm"
        ],
        "adds": [
          "done:isolate:loading-arm"
        ],
        "deletes": [
          "tool:free"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "loading-arm"
        }
      }
    ],
    "initialFacts": [
      "tool:free",
      "fault:loading-arm",
      "misaligned:loading-arm"
    ],
    "initialModules": [
      "pad",
      "habitat",
      "crusher",
      "conveyor",
      "centrifuge",
      "solar-a",
      "solar-b",
      "tank-a",
      "tank-b",
      "sample-rover",
      "loading-arm",
      "silo"
    ],
    "goalFacts": [
      "ready:loading-arm"
    ],
    "absentFacts": [
      "unverified"
    ],
    "budget": 5
  },
  "answer": {
    "actionIds": [
      "isolate:loading-arm",
      "undo:loading-arm",
      "align:loading-arm",
      "verify:loading-arm",
      "resume:loading-arm"
    ]
  }
}
```

### 共享工具协同维修（h3-lunar-sample-refinery-resource-repair）

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
        "id": "release:silo",
        "label": "release silo",
        "requires": [
          "done:relock:silo"
        ],
        "forbids": [
          "done:release:silo"
        ],
        "adds": [
          "done:release:silo",
          "ready:silo",
          "tool:free"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "silo"
        }
      },
      {
        "id": "relock:silo",
        "label": "relock silo",
        "requires": [
          "done:verify:silo"
        ],
        "forbids": [
          "done:relock:silo"
        ],
        "adds": [
          "done:relock:silo"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "silo"
        }
      },
      {
        "id": "verify:silo",
        "label": "verify silo",
        "requires": [
          "done:replace:silo"
        ],
        "forbids": [
          "done:verify:silo"
        ],
        "adds": [
          "done:verify:silo"
        ],
        "deletes": [
          "fault:silo",
          "misaligned:silo"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "silo"
        }
      },
      {
        "id": "replace:silo",
        "label": "replace silo",
        "requires": [
          "done:unlock:silo"
        ],
        "forbids": [
          "done:replace:silo"
        ],
        "adds": [
          "done:replace:silo"
        ],
        "deletes": [],
        "cost": 2,
        "visual": {
          "moduleId": "silo"
        }
      },
      {
        "id": "unlock:silo",
        "label": "unlock silo",
        "requires": [
          "done:support:silo"
        ],
        "forbids": [
          "done:unlock:silo"
        ],
        "adds": [
          "done:unlock:silo"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "silo"
        }
      },
      {
        "id": "support:silo",
        "label": "support silo",
        "requires": [
          "done:isolate:silo"
        ],
        "forbids": [
          "done:support:silo"
        ],
        "adds": [
          "done:support:silo"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "silo"
        }
      },
      {
        "id": "isolate:silo",
        "label": "isolate silo",
        "requires": [
          "tool:free",
          "fault:silo"
        ],
        "forbids": [
          "done:isolate:silo"
        ],
        "adds": [
          "done:isolate:silo"
        ],
        "deletes": [
          "tool:free"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "silo"
        }
      },
      {
        "id": "release:loading-arm",
        "label": "release loading-arm",
        "requires": [
          "done:relock:loading-arm"
        ],
        "forbids": [
          "done:release:loading-arm"
        ],
        "adds": [
          "done:release:loading-arm",
          "ready:loading-arm",
          "tool:free"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "loading-arm"
        }
      },
      {
        "id": "relock:loading-arm",
        "label": "relock loading-arm",
        "requires": [
          "done:verify:loading-arm"
        ],
        "forbids": [
          "done:relock:loading-arm"
        ],
        "adds": [
          "done:relock:loading-arm"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "loading-arm"
        }
      },
      {
        "id": "verify:loading-arm",
        "label": "verify loading-arm",
        "requires": [
          "done:replace:loading-arm"
        ],
        "forbids": [
          "done:verify:loading-arm"
        ],
        "adds": [
          "done:verify:loading-arm"
        ],
        "deletes": [
          "fault:loading-arm",
          "misaligned:loading-arm"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "loading-arm"
        }
      },
      {
        "id": "replace:loading-arm",
        "label": "replace loading-arm",
        "requires": [
          "done:unlock:loading-arm"
        ],
        "forbids": [
          "done:replace:loading-arm"
        ],
        "adds": [
          "done:replace:loading-arm"
        ],
        "deletes": [],
        "cost": 2,
        "visual": {
          "moduleId": "loading-arm"
        }
      },
      {
        "id": "unlock:loading-arm",
        "label": "unlock loading-arm",
        "requires": [
          "done:support:loading-arm"
        ],
        "forbids": [
          "done:unlock:loading-arm"
        ],
        "adds": [
          "done:unlock:loading-arm"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "loading-arm"
        }
      },
      {
        "id": "support:loading-arm",
        "label": "support loading-arm",
        "requires": [
          "done:isolate:loading-arm"
        ],
        "forbids": [
          "done:support:loading-arm"
        ],
        "adds": [
          "done:support:loading-arm"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "loading-arm"
        }
      },
      {
        "id": "isolate:loading-arm",
        "label": "isolate loading-arm",
        "requires": [
          "tool:free",
          "fault:loading-arm"
        ],
        "forbids": [
          "done:isolate:loading-arm"
        ],
        "adds": [
          "done:isolate:loading-arm"
        ],
        "deletes": [
          "tool:free"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "loading-arm"
        }
      },
      {
        "id": "release:sample-rover",
        "label": "release sample-rover",
        "requires": [
          "done:relock:sample-rover"
        ],
        "forbids": [
          "done:release:sample-rover"
        ],
        "adds": [
          "done:release:sample-rover",
          "ready:sample-rover",
          "tool:free"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "sample-rover"
        }
      },
      {
        "id": "relock:sample-rover",
        "label": "relock sample-rover",
        "requires": [
          "done:verify:sample-rover"
        ],
        "forbids": [
          "done:relock:sample-rover"
        ],
        "adds": [
          "done:relock:sample-rover"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "sample-rover"
        }
      },
      {
        "id": "verify:sample-rover",
        "label": "verify sample-rover",
        "requires": [
          "done:replace:sample-rover"
        ],
        "forbids": [
          "done:verify:sample-rover"
        ],
        "adds": [
          "done:verify:sample-rover"
        ],
        "deletes": [
          "fault:sample-rover",
          "misaligned:sample-rover"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "sample-rover"
        }
      },
      {
        "id": "replace:sample-rover",
        "label": "replace sample-rover",
        "requires": [
          "done:unlock:sample-rover"
        ],
        "forbids": [
          "done:replace:sample-rover"
        ],
        "adds": [
          "done:replace:sample-rover"
        ],
        "deletes": [],
        "cost": 2,
        "visual": {
          "moduleId": "sample-rover"
        }
      },
      {
        "id": "unlock:sample-rover",
        "label": "unlock sample-rover",
        "requires": [
          "done:support:sample-rover"
        ],
        "forbids": [
          "done:unlock:sample-rover"
        ],
        "adds": [
          "done:unlock:sample-rover"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "sample-rover"
        }
      },
      {
        "id": "support:sample-rover",
        "label": "support sample-rover",
        "requires": [
          "done:isolate:sample-rover"
        ],
        "forbids": [
          "done:support:sample-rover"
        ],
        "adds": [
          "done:support:sample-rover"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "sample-rover"
        }
      },
      {
        "id": "isolate:sample-rover",
        "label": "isolate sample-rover",
        "requires": [
          "tool:free",
          "fault:sample-rover"
        ],
        "forbids": [
          "done:isolate:sample-rover"
        ],
        "adds": [
          "done:isolate:sample-rover"
        ],
        "deletes": [
          "tool:free"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "sample-rover"
        }
      },
      {
        "id": "release:tank-b",
        "label": "release tank-b",
        "requires": [
          "done:relock:tank-b"
        ],
        "forbids": [
          "done:release:tank-b"
        ],
        "adds": [
          "done:release:tank-b",
          "ready:tank-b",
          "tool:free"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "tank-b"
        }
      },
      {
        "id": "relock:tank-b",
        "label": "relock tank-b",
        "requires": [
          "done:verify:tank-b"
        ],
        "forbids": [
          "done:relock:tank-b"
        ],
        "adds": [
          "done:relock:tank-b"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "tank-b"
        }
      },
      {
        "id": "verify:tank-b",
        "label": "verify tank-b",
        "requires": [
          "done:replace:tank-b"
        ],
        "forbids": [
          "done:verify:tank-b"
        ],
        "adds": [
          "done:verify:tank-b"
        ],
        "deletes": [
          "fault:tank-b",
          "misaligned:tank-b"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "tank-b"
        }
      },
      {
        "id": "replace:tank-b",
        "label": "replace tank-b",
        "requires": [
          "done:unlock:tank-b"
        ],
        "forbids": [
          "done:replace:tank-b"
        ],
        "adds": [
          "done:replace:tank-b"
        ],
        "deletes": [],
        "cost": 2,
        "visual": {
          "moduleId": "tank-b"
        }
      },
      {
        "id": "unlock:tank-b",
        "label": "unlock tank-b",
        "requires": [
          "done:support:tank-b"
        ],
        "forbids": [
          "done:unlock:tank-b"
        ],
        "adds": [
          "done:unlock:tank-b"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "tank-b"
        }
      },
      {
        "id": "support:tank-b",
        "label": "support tank-b",
        "requires": [
          "done:isolate:tank-b"
        ],
        "forbids": [
          "done:support:tank-b"
        ],
        "adds": [
          "done:support:tank-b"
        ],
        "deletes": [],
        "cost": 1,
        "visual": {
          "moduleId": "tank-b"
        }
      },
      {
        "id": "isolate:tank-b",
        "label": "isolate tank-b",
        "requires": [
          "tool:free",
          "fault:tank-b"
        ],
        "forbids": [
          "done:isolate:tank-b"
        ],
        "adds": [
          "done:isolate:tank-b"
        ],
        "deletes": [
          "tool:free"
        ],
        "cost": 1,
        "visual": {
          "moduleId": "tank-b"
        }
      }
    ],
    "initialFacts": [
      "tool:free",
      "fault:tank-b",
      "fault:sample-rover",
      "fault:loading-arm",
      "fault:silo"
    ],
    "initialModules": [
      "pad",
      "habitat",
      "crusher",
      "conveyor",
      "centrifuge",
      "solar-a",
      "solar-b",
      "tank-a",
      "tank-b",
      "sample-rover",
      "loading-arm",
      "silo"
    ],
    "goalFacts": [
      "ready:tank-b",
      "ready:sample-rover",
      "ready:loading-arm",
      "ready:silo"
    ],
    "absentFacts": [
      "unverified"
    ],
    "budget": 32
  },
  "answer": {
    "actionIds": [
      "isolate:silo",
      "support:silo",
      "unlock:silo",
      "replace:silo",
      "verify:silo",
      "relock:silo",
      "release:silo",
      "isolate:loading-arm",
      "support:loading-arm",
      "unlock:loading-arm",
      "replace:loading-arm",
      "verify:loading-arm",
      "relock:loading-arm",
      "release:loading-arm",
      "isolate:sample-rover",
      "support:sample-rover",
      "unlock:sample-rover",
      "replace:sample-rover",
      "verify:sample-rover",
      "relock:sample-rover",
      "release:sample-rover",
      "isolate:tank-b",
      "support:tank-b",
      "unlock:tank-b",
      "replace:tank-b",
      "verify:tank-b",
      "relock:tank-b",
      "release:tank-b"
    ]
  }
}
```

### 预算约束检查策略（h3-lunar-sample-refinery-budget-policy）

提交预算内、对所有相容世界均正确的检查决策表。

能力：预算约束检查策略；形式：policy；证据：finite-world。


```json
{
  "input": {
    "module": "loading-arm",
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
        "cost": 0,
        "returns": {
          "nominal": "clear",
          "fault": "clear"
        }
      },
      {
        "id": "probe",
        "cost": 2,
        "returns": {
          "nominal": "clear",
          "fault": "alert"
        }
      },
      {
        "id": "thermal",
        "cost": 1,
        "returns": {
          "nominal": "clear",
          "fault": "alert"
        }
      }
    ],
    "budget": 1
  },
  "answer": {
    "queryId": "thermal",
    "decisions": {
      "clear": "continue",
      "alert": "replace"
    }
  }
}
```

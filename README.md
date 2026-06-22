# AgriSense
My 2026 Waterloo-Wellington Science and Engineering Fair (WWSEF) Project<br><br>
## presentation board
![presentation board](https://raw.githubusercontent.com/personion222/plant-spec/refs/heads/main/assets/img3.jpeg)

## device
3D printed frame ([OnShape CAD model](https://cad.onshape.com/documents/f6b1d8f23361934da0d3398c/w/97189431fad67bf53bf5594f/e/c6ea907d86fddfd0cd7ceaf9?renderMode=0&uiState=6a39b664db39404c24688b18)). firmware for apriltag detection runs on an [OpenMV Cam STM32H7 MCU](https://openmv.io/products/openmv-cam-h7), and an [AS7265x Spectral Sensor](https://ams-osram.com/products/sensor-solutions/ambient-light-color-spectral-proximity-sensors/ams-as7265x-smart-spectral-sensor) is used for multispectral sensing
![circuit](https://raw.githubusercontent.com/personion222/plant-spec/refs/heads/main/assets/img1.jpeg)
![example](https://raw.githubusercontent.com/personion222/plant-spec/refs/heads/main/assets/img2.jpeg)

## software
the attached custom-built JavaScript web tool is used for configuration and analyzing the data stored on the onboard microSD card
|general analytics page|detail analytics page|config page|
| :---: | :---: | :---: |
|![example](https://raw.githubusercontent.com/personion222/plant-spec/refs/heads/main/assets/img5.png)|![example](https://raw.githubusercontent.com/personion222/plant-spec/refs/heads/main/assets/img4.png)|![example](https://raw.githubusercontent.com/personion222/plant-spec/refs/heads/main/assets/img6.png)|
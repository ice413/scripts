#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

#define SCREEN_WIDTH 64
#define SCREEN_HEIGHT 32
#define OLED_RESET    -1
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);

#define CLK 2       // Rotary Encoder Clock (A)
#define DT 3        // Rotary Encoder Data (B)
#define SW 4        // Rotary Encoder Button (Mute)
#define DS1802_CLK 6  // DS1802 Clock
#define DS1802_UD 7   // DS1802 Up/Down
#define DS1802_MUTE 5 // DS1802 Mute

bool muteState = false;
int volume = 15;  // Initial volume (0-63)
int balance = 0;  // Balance (-10 to 10)
bool balanceMode = false;
int lastEncoderState;

void setup() {
    pinMode(CLK, INPUT_PULLUP);
    pinMode(DT, INPUT_PULLUP);
    pinMode(SW, INPUT_PULLUP);
    pinMode(DS1802_CLK, OUTPUT);
    pinMode(DS1802_UD, OUTPUT);
    pinMode(DS1802_MUTE, OUTPUT);

    digitalWrite(DS1802_MUTE, HIGH);  // Start unmuted
    lastEncoderState = digitalRead(CLK);

    // Initialize OLED Display
    if (!display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) {  // 0x3C is the typical I2C address
        while (true);  // Halt if OLED fails
    }
    display.clearDisplay();
    updateOLED();
}

void loop() {
    // Read encoder button (mute toggle)
    if (digitalRead(SW) == LOW) {
        delay(50); // Debounce
        if (digitalRead(SW) == LOW) {
            muteState = !muteState;
            digitalWrite(DS1802_MUTE, muteState ? LOW : HIGH);
            updateOLED();
            while (digitalRead(SW) == LOW); // Wait for release
        }
    }

    // Check if encoder is rotated
    int encoderState = digitalRead(CLK);
    if (encoderState != lastEncoderState) {
        if (digitalRead(DT) != encoderState) {
            if (balanceMode) balance = constrain(balance + 1, -10, 10);
            else volume = constrain(volume + 1, 0, 63);
        } else {
            if (balanceMode) balance = constrain(balance - 1, -10, 10);
            else volume = constrain(volume - 1, 0, 63);
        }

        updateVolume();
        updateOLED();
        lastEncoderState = encoderState;
    }

    // Hold button to switch to balance mode
    if (digitalRead(SW) == LOW) {
        delay(500);  // Long press detection
        if (digitalRead(SW) == LOW) {
            balanceMode = !balanceMode;
            updateOLED();
            while (digitalRead(SW) == LOW); // Wait for release
        }
    }
}

// Function to update DS1802 volume levels
void updateVolume() {
    int logVolume = pow(10, (volume / 63.0) * log10(63)); // Logarithmic mapping

    int leftVol = logVolume + (balance < 0 ? balance : 0);
    int rightVol = logVolume - (balance > 0 ? balance : 0);

    sendToDS1802(leftVol);
    sendToDS1802(rightVol);
}

// Function to send volume to DS1802
void sendToDS1802(int vol) {
    for (int i = 0; i < 7; i++) {
        digitalWrite(DS1802_CLK, LOW);
        digitalWrite(DS1802_UD, (vol & (1 << i)) ? HIGH : LOW);
        digitalWrite(DS1802_CLK, HIGH);
    }
}

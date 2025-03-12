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
#define DS1802_D 7   // DS1802 Data (D)
#define DS1802_MUTE 5 // DS1802 Mute

bool muteState = false;
int volume = 15;  // Initial volume (0-63)
int balance = 0;  // Balance (-10 to 10)
bool balanceMode = false;
int lastEncoderState;

void setup() {
    Serial.begin(9600);
    pinMode(CLK, INPUT_PULLUP);
    pinMode(DT, INPUT_PULLUP);
    pinMode(SW, INPUT_PULLUP);
    pinMode(DS1802_CLK, OUTPUT);
    pinMode(DS1802_D, OUTPUT);
    pinMode(DS1802_MUTE, OUTPUT);

    digitalWrite(DS1802_MUTE, HIGH);  // Start unmuted
    lastEncoderState = digitalRead(CLK);

    // Initialize OLED Display
    if (!display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) {
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
    int leftVol = volume + (balance < 0 ? balance : 0);
    int rightVol = volume - (balance > 0 ? balance : 0);

    leftVol = constrain(leftVol, 0, 63);
    rightVol = constrain(rightVol, 0, 63);

    sendToDS1802(leftVol);
    sendToDS1802(rightVol);
}

// Function to send volume to DS1802
void sendToDS1802(int vol) {
    for (int i = 6; i >= 0; i--) {  // Send MSB first
        digitalWrite(DS1802_CLK, LOW);
        digitalWrite(DS1802_D, (vol & (1 << i)) ? HIGH : LOW);
        digitalWrite(DS1802_CLK, HIGH);
    }
}

// Function to update OLED display
void updateOLED() {
    display.clearDisplay();
    display.setTextSize(1);
    display.setTextColor(SSD1306_WHITE);
    display.setCursor(0, 0);
    display.print("Vol: ");
    display.print(volume);
    Serial.print("Vol : ");
    Serial.println(volume);
    
    display.setCursor(0, 10);
    display.print("Bal: ");
    display.print(balance);
    Serial.print("Bal : ");
    Serial.println(balance);
    
    display.setCursor(0, 20);
    display.print(muteState ? "Muted" : "Unmuted");
    Serial.println(muteState ? "Muted" : "Unmuted");
    
    display.display();
}
